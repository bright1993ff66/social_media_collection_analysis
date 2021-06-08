# This Python file uses the following encoding: utf-8
from datetime import datetime
from collections import Counter
import pytz
import pandas as pd
import os
import numpy as np


def transform_datetime_string_time_to_datetime(string, timezone_info):
    """
    :param string: the string which records the time of the posted tweets(this string's timezone is HK time)
    :param timezone_info: the pytz time zone information for this time string object
    :return: a datetime object which could get access to the year, month, day easily
    """
    datetime_object = datetime.strptime(string, '%a %b %d %H:%M:%S +0800 %Y')
    return datetime_object.astimezone(timezone_info)


def transform_string_time_to_datetime(time_string, target_time_zone, convert_utc_time=True):
    """
    Transform the string time to the datetime
    :param time_string: a time string
    :param target_time_zone: the target time zone
    :param convert_utc_time: whether transfer the datetime object to utc first. If the origin time string is recorded
    in UTC time, set convert_utc_time = True
    :return:
    """
    datetime_object = datetime.strptime(time_string, "%a %b %d %H:%M:%S %z %Y")
    if convert_utc_time:
        final_time_object = datetime_object.replace(tzinfo=pytz.utc).astimezone(target_time_zone)
    else:
        final_time_object = datetime_object.astimezone(target_time_zone)
    return final_time_object
	
	
def get_time_attributes(dataframe: pd.DataFrame, datetime_obj_colname: str):
    """
    Get the time attributes based on the time object saved in dataframe
    :param dataframe: a pandas dataframe saving the tweets
    :param datetime_obj_colname: the colname of the tweet dataframe saving the time object
    :return: a dataframe with time attributes for each tweet, including year, month, day, weekday, hour, minute, and second
    """
    dataframe_copy = dataframe.copy()
    dataframe_copy['year'] = dataframe_copy.apply(lambda row: row[datetime_obj_colname].year, axis=1)
    dataframe_copy['month'] = dataframe_copy.apply(lambda row: row[datetime_obj_colname].month, axis=1)
    dataframe_copy['day'] = dataframe_copy.apply(lambda row: row[datetime_obj_colname].day, axis=1)
    dataframe_copy['weekday'] = dataframe_copy.apply(lambda row: row[datetime_obj_colname].weekday(), axis=1)
    dataframe_copy['hour'] = dataframe_copy.apply(lambda row: row[datetime_obj_colname].hour, axis=1)
    dataframe_copy['minute'] = dataframe_copy.apply(lambda row: row[datetime_obj_colname].minute, axis=1)
    dataframe_copy['second'] = dataframe_copy.apply(lambda row: row[datetime_obj_colname].second, axis=1)
    return dataframe_copy


def read_csv_columns(path: str, filename: str, dtype_convert_dict: dict):
    """
    Load a csv file saved locally considering only specific columns.
    This function will only consider the columns saved as the keys of dtype_convert_dict
    :param path: the path for the csv file
    :param filename: the name of the csv file
    :param dtype_convert_dict: datatype convert dict
    :return: a pandas dataframe
    """
    considered_columns = list(dtype_convert_dict.keys())
    dataframe = pd.read_csv(os.path.join(path, filename), usecols=considered_columns, dtype=dtype_convert_dict,
                            encoding='utf-8')
    return dataframe


def convert_dtypes_dataframe(dataframe: pd.DataFrame, convert_dict: dict) -> pd.DataFrame:
    """
    Convert the datatype of one or multiple columns of a pandas dataframe
    :param dataframe: a pandas dataframe
    :param convert_dict: a python dictionary saving the target type of each column. For instance:
    convert_dict = {'id_str': np.int64,
                    'user_id_str': np.int64
                   }
    :return: a pandas dataframe with converted columns
    """
    dataframe_converted = dataframe.astype(convert_dict)
    return dataframe_converted


def rename_dataframe(dataframe: pd.DataFrame, rename_dict: dict) -> pd.DataFrame:
    """
    Rename the dataframe based on a dictionary
    :param dataframe: a pandas dataframe
    :param rename_dict: a python dictionary saving the target name of each original columns. For instance:
    convert_dict = {'T_i_t': 'Treatment',
                    'user_id_str': 'User ids'
                   }
    :return: a pandas dataframe with renamed columns
    """
    dataframe_renamed = dataframe.rename(columns=rename_dict)
    return dataframe_renamed


def merge_dict(sum_dict, a_dict: Counter):
    """
    Merge a sum dictionary and a dictionary for a csv file
    Args:
        sum_dict: the sum_dict records the total number of tweets found in one city
        a_dict: a counter dict for a csv tweet file
    Returns: a sum_dict which has added values from a_dict
    """
    if a_dict == Counter():
        return sum_dict
    for key in a_dict:
        if key not in sum_dict:
            sum_dict[key] = a_dict[key]
        else:
            sum_dict[key] += a_dict[key]
    return sum_dict


def create_dataframe_from_dict(dict_data):
    """
    Create the hourly tweet count dataframe
    :param dict_data: a python dict saving the number of tweets posted in each hour in a city
    :return: a pandas dataframe saving the number of tweets
    """
    keys = list(dict_data.keys())
    vals = [dict_data[key] for key in keys]
    dataframe = pd.DataFrame(columns=['time', 'total_count'])
    dataframe['time'] = keys
    dataframe['total_count'] = vals
    dataframe['year'] = dataframe.apply(lambda row: np.int(row['time'].split('_')[0]), axis=1)
    dataframe['month'] = dataframe.apply(lambda row: np.int(row['time'].split('_')[1]), axis=1)
    dataframe['day'] = dataframe.apply(lambda row: np.int(row['time'].split('_')[2]), axis=1)
    dataframe['hour'] = dataframe.apply(lambda row: np.int(row['time'].split('_')[3]), axis=1)
    dataframe['weekday'] = dataframe.apply(lambda row: np.int(row['time'].split('_')[4]), axis=1)
    dataframe['datetime'] = dataframe.apply(
        lambda row: datetime(int(row['year']), int(row['month']), int(row['day']), int(row['hour'])), axis=1)
    dataframe_sorted = dataframe.sort_values(by='datetime')
    dataframe_final = dataframe_sorted.drop(['datetime', 'time'], axis=1)
    return dataframe_final


def sum_dataframe_list_count(dataframe_list: list) -> pd.DataFrame:
    """
    Create the sum dataframe for the open space tweet count pandas dataframes
    :param dataframe_list: a python list containing the pandas tweet dataframe
    :return: a dataframe saving the number of tweets posted in each hour
    """
    for dataframe in dataframe_list:
        assert 'open_space_count' in dataframe, 'The dataframe should contain the count of tweets in open space'
    combined_dataframe = dataframe_list[0][['year', 'month', 'day', 'hour', 'weekday']]
    sum_dataframes_list = [dataframe[['open_space_count']] for dataframe in dataframe_list]
    sum_dataframe = sum(sum_dataframes_list)
    result_dataframe = pd.concat([combined_dataframe, sum_dataframe], axis=1)
    return result_dataframe


def combine_total_and_open_space_count(total_df: pd.DataFrame, open_space_df: pd.DataFrame):
    """
    Combine the tweet count dataframes
    :param total_df: the dataframe saving tweet count for the whole city
    :param open_space_df: the dataframe saving tweet count for the open space
    :return: a combined pandas dataframe saving the combined tweet count
    """
    year_col, month_col, day_col = 'year', 'month', 'day'
    hour_col, weekday_col = 'hour', 'weekday'

    # Check whether two dataframes have columns needed
    assert year_col in total_df and month_col in total_df, "Dataframe lacks {}, {} info".format(year_col, month_col)
    assert day_col in total_df and weekday_col in total_df, "Dataframe lacks {}, {} info".format(day_col, weekday_col)
    assert hour_col in total_df, "Dataframe lacks {} info".format(hour_col)
    assert year_col in open_space_df and month_col in open_space_df, "Dataframe lacks {}, {} info".format(year_col,
                                                                                                          month_col)
    assert day_col in open_space_df and weekday_col in open_space_df, "Dataframe lacks {}, {} info".format(day_col,
                                                                                                           weekday_col)
    assert hour_col in open_space_df, "Dataframe lacks {} info".format(hour_col)

    # Check whether two dataframes have the corresponding count columns
    assert 'total_count' in total_df, "Dataframe saving tweet count must have a column named 'total_count'"
    assert 'count' in open_space_df, "Dataframe saving tweets posted in open space must have a column named 'count'"

    # merge two dataframes
    total_df_select = total_df[['year', 'month', 'day', 'hour', 'weekday', 'total_count']]
    open_space_df_select = open_space_df[['year', 'month', 'day', 'hour', 'weekday', 'count']]
    result_dataframe = pd.merge(open_space_df_select, total_df_select, how='left',
                                left_on=['year', 'month', 'day', 'hour', 'weekday'],
                                right_on=['year', 'month', 'day', 'hour', 'weekday'])
    # Compute the percentage of tweets posted in open space
    result_dataframe['percent'] = result_dataframe['count'] / result_dataframe['total_count']
    # Fill the NA values with 0
    result_dataframe['total_count'] = result_dataframe['total_count'].fillna(0)
    result_dataframe['percent'] = result_dataframe['percent'].fillna(0)
    return result_dataframe
