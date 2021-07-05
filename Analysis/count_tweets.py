# encoding = 'utf-8'
import os
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import pytz
import pandas as pd
import geopandas as gpd

import data_paths
from cities_bounds import cities_dict_foreign, open_space_saving_path
from utils import transform_time_string_to_utc_time, transform_string_time_to_datetime, merge_dict, \
    create_dataframe_from_dict, sum_dataframe_list_count, column_dtype_dict
from visualizations import create_day_plot_for_one_count, create_hour_weekday_plot

# Cope with some bad latitude and longitude data
lat_lon_start_tuple = tuple([str(val) for val in range(10)] + ['-'])
print(lat_lon_start_tuple)

# Used column names and data types
considered_colnames = list(column_dtype_dict.keys())
dtype_dict = {'user_id_str': str, 'id_str': str, 'text': str,
              'created_at': str, 'verified': str, 'lang': str, 'url': str}
print('The considered columns in the tweet dataframe: {}'.format(considered_colnames))
print('The convert datatypes: {}'.format(dtype_dict))


class CountTweets(object):
    """
    Count the number of geocoded tweets and all the tweets posted in one city
    """

    saving_path_for_month = data_paths.count_tweet_month_path

    def __init__(self, city_name, city_profile_dict, start_time, end_time, utc_or_not):
        assert city_name in city_profile_dict, 'The name of the city is not right!'
        self.city_name = city_name  # the name of city
        self.city_bounding_box = city_profile_dict[city_name][0]  # load the predefined bounding box
        self.city_timezone = city_profile_dict[city_name][1]  # load the local timezone information
        self.city_loc = city_profile_dict[city_name][2]  # load the location of data
        self.city_shapefile_loc = city_profile_dict[city_name][5]  # load the shapefile of the city
        self.count_in_utc = utc_or_not  # use the utc time for counting or not
        self.considered_year_list = ['2016', '2017', '2018', '2019', '2020']
        self.considered_quarter_list = ['Q1', 'Q2', 'Q3', 'Q4']
        self.start_time = start_time
        self.end_time = end_time
        # load the detected bot ids
        if type(city_profile_dict[city_name][4]) == set:
            self.bot_ids = city_profile_dict[city_name][4]
        elif type(city_profile_dict[city_name][4]) == str:
            self.bot_ids = np.load(os.path.join(city_profile_dict[city_name][4]), allow_pickle=True).item()

    def count_geocoded_tweets_hour(self):

        """
        Count the geocoded tweets (lat and lon) posted in each hour of the study time
        :return: a pandas dataframe saving the number of tweets posted in each hour of the study time
        """

        # Create a dictionary to save the number of tweets posted in each hour
        considered_geocoded_time_count_dict = defaultdict()

        # Count the tweets...
        for year in self.considered_year_list:
            csv_path = os.path.join(self.city_loc, year)
            try:
                for csv_file in os.listdir(csv_path):
                    print('Coping with the file: {}'.format(csv_file))
                    try:
                        dataframe = pd.read_csv(open(os.path.join(csv_path, csv_file),
                                                     encoding='utf-8',
                                                     errors='ignore'),
                                                usecols=considered_colnames,
                                                dtype=dtype_dict)
                        geocoded_dataframe = dataframe.loc[~dataframe['lat'].isnull()]
                        # print(geocoded_dataframe['lat'].dtype.name)
                        geocoded_without_duplicates = geocoded_dataframe.drop_duplicates(subset=['id_str'])
                        geocoded_without_bot = geocoded_without_duplicates.loc[
                            ~geocoded_without_duplicates['user_id_str'].isin(self.bot_ids)]
                        # geocoded_in_box = self.find_tweet_in_bounding_box(geocoded_without_bot,
                        #                                                   bounding_box_vals=self.city_bounding_box)
                        geocoded_tweet_city = self.find_tweet_in_city(dataframe=geocoded_without_bot)

                        # Process the dataframe with lat and lon
                        if geocoded_tweet_city.shape[0] == 0:
                            geocoded_tweet_counter = Counter()
                        else:
                            geocoded_tweet_city_copy = geocoded_tweet_city.copy()
                            if self.count_in_utc:
                                geocoded_tweet_city_copy['clean_time'] = geocoded_tweet_city_copy.apply(
                                    lambda row: transform_time_string_to_utc_time(time_string=row['created_at']),
                                    axis=1)
                            else:
                                geocoded_tweet_city_copy['clean_time'] = geocoded_tweet_city_copy.apply(
                                    lambda row: transform_string_time_to_datetime(
                                        time_string=row['created_at'], target_time_zone=self.city_timezone), axis=1)
                            geocoded_tweet_city_copy['year_month_day_hour_weekday'] = geocoded_tweet_city_copy.apply(
                                lambda row: str(row['clean_time'].year) + '_' + str(
                                    row['clean_time'].month) + '_' + str(
                                    row['clean_time'].day) + '_' + str(
                                    row['clean_time'].hour) + '_' + str(row['clean_time'].weekday()), axis=1)

                            geocoded_tweet_counter = Counter(geocoded_tweet_city_copy['year_month_day_hour_weekday'])
                        considered_geocoded_time_count_dict = merge_dict(sum_dict=considered_geocoded_time_count_dict,
                                                                         a_dict=geocoded_tweet_counter)
                    except KeyError:
                        print('The csv file: {} does not have any column names.Ignore'.format(csv_file))
                    except ValueError:
                        print('ValueError occurs for file: {}. Ignore.'.format(csv_file))
                    except pd.errors.ParserError:
                        print('Parser error occurred in file: {}. Ignore.'.format(csv_file))
                print('The year: {} has been processed'.format(year))
                print('Geocoded count dict: {}'.format(considered_geocoded_time_count_dict))
            except FileNotFoundError:
                print('There is no {} folder in local'.format(str(year)))
        count_dataframe = create_dataframe_from_dict(dict_data=considered_geocoded_time_count_dict)
        default_dataframe_each_hour = self.create_count_dataframe()
        final_count = pd.merge(left=count_dataframe, right=default_dataframe_each_hour,
                               on=['year', 'month', 'day', 'hour', 'weekday'], how='right')
        final_count['total_count_x'] = final_count['total_count_x'].fillna(0)  # fill the NA as zero
        final_count_droped = final_count.drop(['total_count_y'], axis=1)
        final_count_renamed = final_count_droped.rename(columns={'total_count_x': 'total_count'})
        return final_count_renamed

    def count_geocoded_place_tweets_hour(self):

        """
        Count the geocoded place tweets (place_lat and place_lon) posted in each hour of the study time
        :return: a pandas dataframe saving the number of tweets posted in each hour of the study time
        """

        # Create a dictionary to save the number of tweets posted in each hour
        geocoded_place_time_count_dict = defaultdict()

        # Count the tweets...
        for year in self.considered_year_list:
            csv_path = os.path.join(self.city_loc, year)
            try:
                for csv_file in os.listdir(csv_path):
                    print('Coping with the file: {}'.format(csv_file))
                    try:
                        dataframe = pd.read_csv(open(os.path.join(csv_path, csv_file), encoding='utf-8',
                                                     errors='ignore'), usecols=considered_colnames,
                                                dtype=dtype_dict)
                        geocoded_place_dataframe = dataframe.loc[~dataframe['place_lat'].isnull()]
                        geocoded_without_duplicates = geocoded_place_dataframe.drop_duplicates(subset=['id_str'])
                        geocoded_without_bot = geocoded_without_duplicates.loc[
                            ~geocoded_without_duplicates['user_id_str'].isin(self.bot_ids)]
                        # geocoded_in_box = self.find_tweet_in_bounding_box(geocoded_without_bot,
                        #                                                   bounding_box_vals=self.city_bounding_box)
                        geocoded_place_tweet_city = self.find_tweet_place_in_city(geocoded_without_bot)

                        # Process the dataframe with lat and lon
                        if geocoded_place_tweet_city.shape[0] == 0:
                            geocoded_tweet_counter = Counter()
                        else:
                            geocoded_tweet_city_copy = geocoded_place_tweet_city.copy()
                            if self.count_in_utc:
                                geocoded_tweet_city_copy['clean_time'] = geocoded_tweet_city_copy.apply(
                                    lambda row: transform_time_string_to_utc_time(time_string=row['created_at']),
                                    axis=1)
                            else:
                                geocoded_tweet_city_copy['clean_time'] = geocoded_tweet_city_copy.apply(
                                    lambda row: transform_string_time_to_datetime(
                                        time_string=row['created_at'], target_time_zone=self.city_timezone), axis=1)
                            geocoded_tweet_city_copy['year_month_day_hour_weekday'] = geocoded_tweet_city_copy.apply(
                                lambda row: str(row['clean_time'].year) + '_' + str(
                                    row['clean_time'].month) + '_' + str(
                                    row['clean_time'].day) + '_' + str(
                                    row['clean_time'].hour) + '_' + str(row['clean_time'].weekday()), axis=1)
                            geocoded_tweet_counter = Counter(geocoded_tweet_city_copy['year_month_day_hour_weekday'])
                        geocoded_place_time_count_dict = merge_dict(sum_dict=geocoded_place_time_count_dict,
                                                                    a_dict=geocoded_tweet_counter)
                    except KeyError:
                        print('The csv file: {} does not have any colnames.Ignore'.format(csv_file))
                    except ValueError:
                        print('ValueError occurs for file: {}. Ignore.'.format(csv_file))
                    except pd.errors.ParserError:
                        print('Parser error occurred in file: {}. Ignore.'.format(csv_file))
                print('The year: {} has been processed'.format(year))
                print('Geocoded count dict: {}'.format(geocoded_place_time_count_dict))
            except FileNotFoundError:
                print('There is no {} folder in local'.format(str(year)))
        count_place_dataframe = create_dataframe_from_dict(dict_data=geocoded_place_time_count_dict)
        default_dataframe_each_hour = self.create_count_dataframe()
        final_count = pd.merge(left=count_place_dataframe, right=default_dataframe_each_hour,
                               on=['year', 'month', 'day', 'hour', 'weekday'], how='right')
        final_count['total_count_x'] = final_count['total_count_x'].fillna(0)  # fill the NA as zero
        final_count_droped = final_count.drop(['total_count_y'], axis=1)
        final_count_renamed = final_count_droped.rename(columns={'total_count_x': 'total_count'})
        return final_count_renamed

    def count_tweets_monthly(self):
        """
        Count the geocoded and all the tweets posted in one city
        Returns:
        """
        print('Set up the counting dictionary...')
        considered_geocoded_time_count_dict = defaultdict()
        considered_all_time_count_dict = defaultdict()
        key_vals = []
        for year in self.considered_year_list:
            for month in range(1, 13):
                considered_geocoded_time_count_dict[str(year) + '_' + str(month)] = 0
                considered_all_time_count_dict[str(year) + '_' + str(month)] = 0
                key_vals.append(str(year) + '_' + str(month))
        print('Done!')
        for year in self.considered_year_list:
            csv_path = os.path.join(self.city_loc, year)
            try:
                for csv_file in os.listdir(csv_path):
                    print('Coping with the file: {}'.format(csv_file))
                    try:
                        dataframe = pd.read_csv(open(os.path.join(csv_path, csv_file), encoding='utf-8',
                                                     errors='ignore'), usecols=considered_colnames, dtype=dtype_dict)
                        geocoded_dataframe = dataframe.loc[~dataframe['lat'].isnull()]
                        geocoded_place_dataframe = dataframe.loc[~dataframe['place_lat'].isnull()]

                        geocoded_without_duplicates = geocoded_dataframe.drop_duplicates(subset=['id_str'])
                        geocoded_without_bot = geocoded_without_duplicates.loc[
                            ~geocoded_without_duplicates['user_id_str'].isin(self.bot_ids)]
                        geocoded_tweet_city = self.find_tweet_in_city(geocoded_without_bot)

                        geocoded_place_without_duplicates = geocoded_place_dataframe.drop_duplicates(
                            subset=['id_str'])
                        geocoded_place_without_bot = geocoded_place_without_duplicates.loc[
                            ~geocoded_place_without_duplicates['user_id_str'].isin(self.bot_ids)]
                        geocoded_place_tweet_city = self.find_tweet_place_in_city(geocoded_place_without_bot)

                        # Process the dataframe with lat and lon
                        if geocoded_tweet_city.shape[0] == 0:
                            geocoded_tweet_city_copy = pd.DataFrame()
                            geocoded_tweet_counter = Counter()
                        else:
                            geocoded_tweet_city_copy = geocoded_tweet_city.copy()
                            if self.count_in_utc:
                                geocoded_tweet_city_copy['clean_time'] = geocoded_tweet_city_copy.apply(
                                    lambda row: transform_time_string_to_utc_time(time_string=row['created_at']),
                                    axis=1)
                            else:
                                geocoded_tweet_city_copy['clean_time'] = geocoded_tweet_city_copy.apply(
                                    lambda row: transform_string_time_to_datetime(time_string=row['created_at'],
                                                                                  target_time_zone=self.city_timezone),
                                    axis=1)
                            geocoded_tweet_city_copy['year_month'] = geocoded_tweet_city_copy.apply(
                                lambda row: str(row['clean_time'].year) + '_' + str(row['clean_time'].month), axis=1)
                            geocoded_tweet_counter = Counter(geocoded_tweet_city_copy['year_month'])

                        # Process the dataframe with place_lat and place_lon
                        if geocoded_place_tweet_city.shape[0] == 0:
                            geocoded_place_tweet_city_copy = pd.DataFrame()
                        else:
                            geocoded_place_tweet_city_copy = geocoded_place_tweet_city.copy()
                            if self.count_in_utc:
                                geocoded_place_tweet_city_copy['clean_time'] = geocoded_place_tweet_city_copy.apply(
                                    lambda row: transform_time_string_to_utc_time(row['created_at']), axis=1)
                            else:
                                geocoded_place_tweet_city_copy['clean_time'] = geocoded_place_tweet_city_copy.apply(
                                    lambda row: transform_string_time_to_datetime(row['created_at'],
                                                                                  target_time_zone=self.city_timezone),
                                    axis=1)
                            geocoded_place_tweet_city_copy['year_month'] = geocoded_place_tweet_city_copy.apply(
                                lambda row: str(row['clean_time'].year) + '_' + str(row['clean_time'].month), axis=1)

                        combined_tweet = pd.concat([geocoded_tweet_city_copy, geocoded_place_tweet_city_copy], axis=0)
                        if 'year_month' in combined_tweet:
                            combined_tweet_without_duplicates = combined_tweet.drop_duplicates(subset='id_str')
                            all_tweet_counter = Counter(combined_tweet_without_duplicates['year_month'])
                        else:
                            all_tweet_counter = Counter()
                        considered_geocoded_time_count_dict = merge_dict(considered_geocoded_time_count_dict,
                                                                         geocoded_tweet_counter)
                        considered_all_time_count_dict = merge_dict(considered_all_time_count_dict, all_tweet_counter)
                    except KeyError:
                        print('The csv file: {} does not have any colnames.Ignore'.format(csv_file))
                    except ValueError:
                        print('ValueError occurs for file: {}. Ignore.'.format(csv_file))
                    except pd.errors.ParserError:
                        print('Parser error occurred in file: {}. Ignore.'.format(csv_file))
                print('The year: {} has been processed'.format(year))
                print('Geocoded count dict: {}'.format(considered_geocoded_time_count_dict))
                print('All count dict: {}'.format(considered_all_time_count_dict))
            except FileNotFoundError:
                print('There is no {} folder in local'.format(str(year)))
        # Save the counts to local directory
        count_dataframe = pd.DataFrame(columns=['time', 'geocoded_count', 'all_count'])
        count_dataframe['time'] = key_vals
        count_dataframe['geocoded_count'] = [considered_geocoded_time_count_dict[key] for key in key_vals]
        count_dataframe['all_count'] = [considered_all_time_count_dict[key] for key in key_vals]
        if self.count_in_utc:
            count_dataframe.to_csv(os.path.join(self.saving_path_for_month, self.city_name + '(UTC)_tweet_count.csv'),
                                   encoding='utf-8')
        else:
            count_dataframe.to_csv(os.path.join(self.saving_path_for_month, self.city_name + 'tweet_count.csv'),
                                   encoding='utf-8')

    def get_tweets_from_id_set(self, tweet_id_set, save_path, save_filename):
        """
        Get the tweets by the tweet id(int64)
        Args:
            tweet_id_set: a Python set saving the interested tweet ids
            save_path: the path used to save the selected dataframe
            save_filename: the filename of the selected dataframe
        Returns: None
        """
        select_data_list = []
        for year in self.considered_year_list:
            print('Coping with the year: {}'.format(year))
            if year not in os.listdir(self.city_loc):
                print('We have not collected tweets or do not consider tweets posted in {}'.format(year))
                continue
            csv_file_path = os.path.join(self.city_loc, year)
            for file in os.listdir(csv_file_path):
                try:
                    dataframe = pd.read_csv(os.path.join(csv_file_path, file), encoding='utf-8',
                                            usecols=considered_colnames, dtype=dtype_dict)
                    assert dataframe['id_str'].dtype.name == 'int64', "The dtype of the column 'id_str' is not right!"
                    dataframe_select = dataframe.loc[dataframe['id_str'].isin(tweet_id_set)]
                    select_data_list.append(dataframe_select)
                except ValueError:
                    print('ValueError occurred when reading file: {}. Ignore'.format(file))
                    continue
                except pd.errors.ParserError:
                    print('Parser error occurred in file: {}. Ignore.'.format(file))
                    continue
        result_dataframe = pd.concat(select_data_list, axis=0)
        result_dataframe_reindex = result_dataframe.reset_index(drop=True)
        result_dataframe_without_duplicates = result_dataframe_reindex.drop_duplicates(subset=['id_str'], keep='first')
        if self.count_in_utc:
            result_dataframe_without_duplicates.to_csv(os.path.join(save_path, '(UTC)' + save_filename),
                                                       encoding='utf-8')
        else:
            result_dataframe_without_duplicates.to_csv(os.path.join(save_path, save_filename), encoding='utf-8')

    def get_missing_times(self):
        """
        Get the missing time ranges when collecting the tweets
        :return:
        """
        question_list = []
        for year in self.considered_year_list:
            csv_path = os.path.join(self.city_loc, year)
            try:
                files = os.listdir(csv_path)
                for index in range(len(files) - 1):
                    cur_month_string, cur_day_string, cur_hour_string = files[index][-12:-10], files[index][-10:-8], \
                                                                        files[index][-8:-6]
                    cur_datetime = datetime(year=int(year), month=int(cur_month_string),
                                            day=int(cur_day_string), hour=int(cur_hour_string))
                    next_month_string, next_day_string, next_hour_string = files[index + 1][-12:-10], \
                                                                           files[index + 1][-10:-8], \
                                                                           files[index + 1][-8:-6]
                    next_datetime = datetime(year=int(year), month=int(next_month_string),
                                             day=int(next_day_string), hour=int(next_hour_string))
                    if (next_datetime - cur_datetime).total_seconds() > 10800:  # If the time gap is bigger than 3 hours
                        print('Something wrong with the file: {}'.format(files[index + 1]))
                        question_list.append('from {} to {}'.format(str(cur_datetime), str(next_datetime)))
            except FileNotFoundError:
                print('We have not collected tweets posted in year: {}'.format(year))
        miss_dataframe = pd.DataFrame(columns=[self.city_name])
        miss_dataframe[self.city_name] = question_list
        return miss_dataframe

    def create_count_dataframe(self):
        """
        Create the count dataframe based on the starting time and the ending time
        :return: a pandas dataframe saving the default number of Weibos posted in each hour
        """
        cur_time = self.start_time
        result_dataframe = pd.DataFrame()
        year_list, month_list, weekday_list = [], [], []
        day_list, hour_list = [], []
        while self.end_time != cur_time:
            check_time_year, check_time_month = cur_time.year, cur_time.month
            check_time_day, check_time_hour = cur_time.day, cur_time.hour
            check_time_weekday = cur_time.weekday()
            year_list.append(check_time_year)
            month_list.append(check_time_month)
            day_list.append(check_time_day)
            hour_list.append(check_time_hour)
            weekday_list.append(check_time_weekday)
            cur_time = cur_time + timedelta(hours=1)
        result_dataframe['year'] = year_list
        result_dataframe['month'] = month_list
        result_dataframe['day'] = day_list
        result_dataframe['hour'] = hour_list
        result_dataframe['weekday'] = weekday_list
        result_dataframe['total_count'] = [0] * len(year_list)
        return result_dataframe

    def find_tweet_in_city(self, dataframe):
        """
        Find the tweets posted in the city based on the 'lat' and 'lon' columns
        :param dataframe: a pandas dataframe saving the geocoded tweets
        :return: tweets posted in the city
        """
        if (dataframe['lat'].dtype.name != 'float64') or (dataframe['lon'].dtype.name != 'float64'):
            print('Something wrong with the datatype of latitude and longitude...')
            dataframe_copy = dataframe.copy()
            dataframe_copy['lat'] = dataframe_copy['lat'].astype(str)
            dataframe_copy['lon'] = dataframe_copy['lon'].astype(str)
            dataframe_copy_select = dataframe_copy[dataframe_copy['lat'].str.startswith(
                lat_lon_start_tuple)]
            dataframe_final = dataframe_copy_select[dataframe_copy_select['lon'].str.startswith(
                lat_lon_start_tuple)].copy()
            dataframe_final['lat'] = dataframe_final['lat'].astype(np.float64)
            dataframe_final['lon'] = dataframe_final['lon'].astype(np.float64)
        else:
            dataframe_final = dataframe.copy()
        geocoded_tweet_gdf = gpd.GeoDataFrame(dataframe_final,
                                              geometry=gpd.points_from_xy(dataframe_final.lon,
                                                                          dataframe_final.lat))
        geocoded_tweet_gdf = geocoded_tweet_gdf.set_crs(epsg=4326, inplace=True)
        city_shape = gpd.read_file(self.city_shapefile_loc)
        city_shape_4326 = city_shape.to_crs(epsg=4326)
        joined_data_final = CountTweets.spatial_join(tweet_gdf=geocoded_tweet_gdf, shape_area=city_shape_4326)
        return joined_data_final.reset_index(drop=True)

    @staticmethod
    def find_tweet_in_bounding_box(dataframe, bounding_box_vals):
        """
        Find the geocoded tweets posted in one city's bounding box based on the 'lat' and 'lon' columns
        Args:
            dataframe: a tweet pandas dataframe
            bounding_box_vals: the bounding box of the studied city

        Returns:

        """
        lat_min, lat_max = bounding_box_vals[1], bounding_box_vals[3]
        lon_min, lon_max = bounding_box_vals[0], bounding_box_vals[2]
        # Cope with some bad rows where the geoinformation is stored as a strange string
        if (dataframe['lat'].dtype.name != 'float64') or (dataframe['lon'].dtype.name != 'float64'):
            print('Something wrong with the datatype of latitude and longitude...')
            dataframe_copy = dataframe.copy()
            dataframe_copy['lat'] = dataframe_copy['lat'].astype(str)
            dataframe_copy['lon'] = dataframe_copy['lon'].astype(str)
            dataframe_copy_select = dataframe_copy[dataframe_copy['lat'].str.startswith(
                lat_lon_start_tuple)]
            dataframe_final = dataframe_copy_select[dataframe_copy_select['lon'].str.startswith(
                lat_lon_start_tuple)].copy()
            dataframe_final['lat'] = dataframe_final['lat'].astype(np.float64)
            dataframe_final['lon'] = dataframe_final['lon'].astype(np.float64)
        else:
            dataframe_final = dataframe.copy()
        decision1 = (dataframe_final['lat'] >= lat_min) & (dataframe_final['lat'] <= lat_max)
        decision2 = (dataframe_final['lon'] >= lon_min) & (dataframe_final['lon'] <= lon_max)
        data_in_city = dataframe_final[decision1 & decision2]
        assert type(data_in_city) == pd.DataFrame, 'The output type of dataframe is not right.'
        return data_in_city.reset_index(drop=True)

    def find_tweet_place_in_city(self, dataframe):
        """
        Find the tweets posted in the city based on the 'place_lat' and 'place_lon' columns
        :param dataframe: a pandas dataframe saving the geocoded tweets
        :return: tweets posted in the city
        """
        if (dataframe['place_lat'].dtype.name != 'float64') or (dataframe['place_lon'].dtype.name != 'float64'):
            print('Something wrong with the datatype of latitude and longitude...')
            dataframe_copy = dataframe.copy()
            dataframe_copy['place_lat'] = dataframe_copy['place_lat'].astype(str)
            dataframe_copy['place_lon'] = dataframe_copy['place_lon'].astype(str)
            dataframe_copy_select = dataframe_copy[dataframe_copy['place_lat'].str.startswith(
                lat_lon_start_tuple)]
            dataframe_final = dataframe_copy_select[dataframe_copy_select['place_lon'].str.startswith(
                lat_lon_start_tuple)].copy()
            dataframe_final['place_lat'] = dataframe_final['place_lat'].astype(np.float64)
            dataframe_final['place_lon'] = dataframe_final['place_lon'].astype(np.float64)
        else:
            dataframe_final = dataframe.copy()
        geocoded_tweet_gdf = gpd.GeoDataFrame(dataframe_final,
                                              geometry=gpd.points_from_xy(dataframe_final.place_lon,
                                                                          dataframe_final.place_lat))
        geocoded_tweet_gdf = geocoded_tweet_gdf.set_crs(epsg=4326, inplace=True)
        city_shape = gpd.read_file(self.city_shapefile_loc)
        city_shape_4326 = city_shape.to_crs(epsg=4326)
        joined_data_final = CountTweets.spatial_join(tweet_gdf=geocoded_tweet_gdf, shape_area=city_shape_4326)
        return joined_data_final.reset_index(drop=True)

    @staticmethod
    def find_tweet_place_in_bounding_box(dataframe, bounding_box_vals):
        """
        Find the tweets in the city's bounding box based on the 'place_lat' and 'place_lon' columns
        Args:
            dataframe: a tweet pandas dataframe
            bounding_box_vals: the bounding box of the studied city

        Returns:

        """
        lat_min, lat_max = bounding_box_vals[1], bounding_box_vals[3]
        lon_min, lon_max = bounding_box_vals[0], bounding_box_vals[2]
        # Cope with some bad rows where the geoinformation is stored as a strange string
        if (dataframe['place_lat'].dtype.name != 'float64') or (dataframe['place_lon'].dtype.name != 'float64'):
            print('The geoinformation of this dataframe is not saved correctly')
            dataframe_copy = dataframe.copy()
            dataframe_copy['place_lat'] = dataframe['place_lat'].astype(str)
            dataframe_copy['place_lon'] = dataframe['place_lon'].astype(str)
            dataframe_copy_select = dataframe_copy[dataframe_copy['place_lat'].str.startswith(
                lat_lon_start_tuple)]
            dataframe_final = dataframe_copy_select[dataframe_copy_select['place_lon'].str.startswith(
                lat_lon_start_tuple)].copy()
            dataframe_final['place_lat'] = dataframe_final['place_lat'].astype(np.float64)
            dataframe_final['place_lon'] = dataframe_final['place_lon'].astype(np.float64)
        else:
            dataframe_final = dataframe.copy()
        decision1 = (dataframe_final['place_lat'] >= lat_min) & (dataframe_final['place_lat'] <= lat_max)
        decision2 = (dataframe_final['place_lon'] >= lon_min) & (dataframe_final['place_lon'] <= lon_max)
        data_in_city = dataframe_final[decision1 & decision2]
        assert type(data_in_city) == pd.DataFrame, 'The output type of dataframe is not right.'
        return data_in_city.reset_index(drop=True)

    @staticmethod
    def spatial_join(tweet_gdf, shape_area):
        """
        Find the tweets posted in one city's open space
        :param tweet_gdf: the geopandas dataframe saving the tweets
        :param shape_area: the shapefile of a studied area, such as city, open space, etc
        :return: tweets posted in open space
        """
        assert tweet_gdf.crs == shape_area.crs, 'The coordinate systems do not match!'
        joined_data = gpd.sjoin(left_df=tweet_gdf, right_df=shape_area, op='within')
        joined_data_final = joined_data.drop_duplicates(subset=['id_str'])
        return joined_data_final


class CountTweetsOpenSpace(object):

    def __init__(self, city_name: str, data_loc: str, start_time: datetime, end_time: datetime, utc_or_not: bool,
                 timezone: pytz.timezone, save_loc: str, save_filename: str, bot_ids: set):
        """
        Count the tweets posted in one city's open space
        :param city_name: the name of the studied city
        :param data_loc: the local directory of the csv file saving the tweets
        :param start_time: the start time for tweet counting
        :param end_time: the end time for tweet counting
        :param utc_or_not: counting in UTC time or not; if not, we would conduct counting based on local timezone
        :param timezone: the timezone of the studied city
        :param save_loc: the save location in the local directory
        :param save_filename: the save filename
        """
        self.city_name = city_name
        self.data_loc = data_loc
        self.timezone = timezone
        self.save_loc = save_loc
        self.start_time = start_time
        self.end_time = end_time
        self.count_in_utc = utc_or_not
        self.save_filename = save_filename
        self.bot_ids = bot_ids

    def count_tweets_hourly(self, day_title: str, hour_title: str, weekday_title: str, day_filename: str,
                            hour_filename: str, weekday_filename: str) -> pd.DataFrame:
        """
        Count the number of tweets posted in each hour of a open space in the studied city
        :return: None. The result is saved in the specified local directory
        """
        result_dataframe_list = []
        # start_time = datetime(2016, 5, 1, 0, 0, 0, tzinfo=self.timezone)
        # end_time = datetime(2020, 12, 31, 0, 0, 0, tzinfo=self.timezone)
        for file in os.listdir(self.data_loc):
            cur_time = self.start_time
            if file.endswith('.csv'):
                print('Analyzing the file {} saving the tweets posted in open space...'.format(file))
                dataframe = pd.read_csv(os.path.join(self.data_loc, file), encoding='utf-8',
                                        usecols=considered_colnames, dtype=dtype_dict)
                dataframe_without_bot = dataframe.loc[~dataframe['user_id_str'].isin(self.bot_ids)]
                # Get the local time and year, month, day, hour attributes
                print('Coping with the time attributes...')
                if self.count_in_utc:
                    dataframe_without_bot['clean_time'] = dataframe_without_bot.apply(
                        lambda row: transform_time_string_to_utc_time(row['created_at']), axis=1)
                else:
                    dataframe_without_bot['clean_time'] = dataframe_without_bot.apply(
                        lambda row: transform_string_time_to_datetime(row['created_at'],
                                                                      target_time_zone=self.timezone), axis=1)
                dataframe_without_bot['year'] = dataframe_without_bot.apply(lambda row: row['clean_time'].year, axis=1)
                dataframe_without_bot['month'] = dataframe_without_bot.apply(lambda row: row['clean_time'].month,
                                                                             axis=1)
                dataframe_without_bot['day'] = dataframe_without_bot.apply(lambda row: row['clean_time'].day, axis=1)
                dataframe_without_bot['hour'] = dataframe_without_bot.apply(lambda row: row['clean_time'].hour, axis=1)
                print('Done!')

                # Count the number of tweets in each hour
                print('Counting the number of tweets posted in each hour...')
                result_count_list = []
                result_time_list = []

                while self.end_time != cur_time:
                    print('Coping with the time: {}'.format(cur_time))
                    check_time_year, check_time_month = cur_time.year, cur_time.month
                    check_time_day, check_time_hour = cur_time.day, cur_time.hour
                    dataframe_year_month = dataframe_without_bot.loc[
                        (dataframe_without_bot['year'] == check_time_year) & (
                                dataframe_without_bot['month'] == check_time_month)]
                    dataframe_day_hour = dataframe_year_month.loc[
                        (dataframe_year_month['day'] == check_time_day) & (dataframe_year_month['hour'] ==
                                                                           check_time_hour)]
                    result_time_list.append(cur_time)
                    result_count_list.append(dataframe_day_hour.shape[0])
                    cur_time = cur_time + timedelta(hours=1)
                result_dataframe = pd.DataFrame(columns=['year', 'month', 'day', 'hour', 'open_space_count'])
                result_dataframe['year'] = [timestamp.year for timestamp in result_time_list]
                result_dataframe['month'] = [timestamp.month for timestamp in result_time_list]
                result_dataframe['day'] = [timestamp.day for timestamp in result_time_list]
                result_dataframe['hour'] = [timestamp.hour for timestamp in result_time_list]
                result_dataframe['weekday'] = [timestamp.weekday() for timestamp in result_time_list]
                result_dataframe['open_space_count'] = result_count_list
                result_dataframe_list.append(result_dataframe)
        combined_result_dataframe = sum_dataframe_list_count(result_dataframe_list)
        if self.count_in_utc:
            print('Counting the number of tweets on each day...')
            create_day_plot_for_one_count(combined_result_dataframe, title=day_title,
                                          start_date=self.start_time, end_date=self.end_time,
                                          save_filename='(UTC)' + day_filename, in_china=False)
            print('Done! Counting the number of tweets in each hour and weekday...')
            create_hour_weekday_plot(combined_result_dataframe, title_hour=hour_title, title_weekday=weekday_title,
                                     color_hour='#FB8072', color_weekday='#80B1D3',
                                     hour_save_filename='(UTC)' + hour_filename,
                                     weekday_save_filename='(UTC)' + weekday_filename, in_china=False)
        else:
            print('Counting the number of tweets on each day...')
            create_day_plot_for_one_count(combined_result_dataframe, title=day_title,
                                          start_date=self.start_time, end_date=self.end_time,
                                          save_filename=day_filename, in_china=False)
            print('Done! Counting the number of tweets in each hour and weekday...')
            create_hour_weekday_plot(combined_result_dataframe, title_hour=hour_title, title_weekday=weekday_title,
                                     color_hour='#FB8072', color_weekday='#80B1D3', hour_save_filename=hour_filename,
                                     weekday_save_filename=weekday_filename, in_china=False)
        print('Done!')
        if os.path.exists(os.path.join(self.save_loc, self.city_name)):
            if self.count_in_utc:
                combined_result_dataframe.to_csv(os.path.join(self.save_loc, self.city_name,
                                                              '(UTC)' + self.save_filename), encoding='utf-8')
            else:
                combined_result_dataframe.to_csv(os.path.join(self.save_loc, self.city_name,
                                                              self.save_filename), encoding='utf-8')
        else:
            os.mkdir(os.path.join(self.save_loc, self.city_name))
            if self.count_in_utc:
                combined_result_dataframe.to_csv(os.path.join(self.save_loc, self.city_name,
                                                              '(UTC)' + self.save_filename), encoding='utf-8')
            else:
                combined_result_dataframe.to_csv(os.path.join(self.save_loc, self.city_name,
                                                              self.save_filename), encoding='utf-8')
        return combined_result_dataframe


def main_count_tweets(count_in_utc: bool = True, considered_city_names=None):
    """
    Main function to count the tweets in both the city and the open space
    :param count_in_utc: count the tweets in UTC time or not
    :param considered_city_names: a set containing the names of processed cities
    :return: None. The tweet count summary and figures have been saved to local directory
    """
    if considered_city_names is None:
        considered_city_names = {}
    for city in cities_dict_foreign:
        if city in considered_city_names:
            print("Coping with the city: {}".format(city))

            if count_in_utc:
                timezone = pytz.utc
            else:
                timezone = cities_dict_foreign[city][1]

            if type(cities_dict_foreign[city][4]) == set:
                city_bot_ids = cities_dict_foreign[city][4]
            elif type(cities_dict_foreign[city][4]) == str:
                city_bot_ids = np.load(cities_dict_foreign[city][4], allow_pickle=True).item()
            else:
                raise ValueError("The bot ids are not loaded correctly!")

            # Count the tweets posted within the city
            count_obj = CountTweets(city_name=city, city_profile_dict=cities_dict_foreign,
                                    start_time=datetime(2016, 5, 1, tzinfo=timezone),
                                    end_time=datetime(2020, 12, 31, tzinfo=timezone),
                                    utc_or_not=count_in_utc)
            geocoded_count_dataframe = count_obj.count_geocoded_tweets_hour()
            if os.path.exists(os.path.join(data_paths.count_daily_hour_path, city)):
                if count_obj.count_in_utc:
                    geocoded_count_dataframe.to_csv(os.path.join(data_paths.count_daily_hour_path, city,
                                                                 '(UTC){}_hour_count.csv'.format(city)))
                else:
                    geocoded_count_dataframe.to_csv(os.path.join(data_paths.count_daily_hour_path, city,
                                                                 '{}_hour_count.csv'.format(city)))
            else:
                os.mkdir(os.path.join(data_paths.count_daily_hour_path, city))
                if count_obj.count_in_utc:
                    geocoded_count_dataframe.to_csv(os.path.join(data_paths.count_daily_hour_path, city,
                                                                 '(UTC){}_hour_count.csv'.format(city)))
                else:
                    geocoded_count_dataframe.to_csv(os.path.join(data_paths.count_daily_hour_path, city,
                                                                 '{}_hour_count.csv'.format(city)))

            # Count the number of tweets posted in the open space of one city
            open_space_count_obj = CountTweetsOpenSpace(city_name=city,
                                                        data_loc=os.path.join(open_space_saving_path, city),
                                                        start_time=datetime(2016, 5, 1, tzinfo=timezone),
                                                        end_time=datetime(2020, 12, 31, tzinfo=timezone),
                                                        timezone=timezone,
                                                        save_loc=data_paths.count_daily_hour_path,
                                                        save_filename='{}_open_space_tweet_count.csv'.format(city),
                                                        utc_or_not=count_in_utc,
                                                        bot_ids=city_bot_ids)
            combined_open_space_dataframe = open_space_count_obj.count_tweets_hourly(
                day_title='Number of Tweets Posted in {} Open Space on Each Day'.format(city),
                hour_title='Number of Tweets Posted in {} Open Space in Each Hour'.format(city),
                weekday_title='Number of Tweets Posted in {} Open Space on Each Weekday'.format(city),
                day_filename='{}_open_space_day.png'.format(city), hour_filename='{}_open_space_hour.png'.format(city),
                weekday_filename='{}_open_space_weekday.png'.format(city))

            # Combine the result and save
            count_final = pd.merge(left=geocoded_count_dataframe, right=combined_open_space_dataframe,
                                   on=['year', 'month', 'day', 'hour', 'weekday'])
            count_final['percent'] = (count_final['open_space_count'] / count_final['total_count']).replace(
                to_replace=[np.inf, np.nan], value=-9999)  # For the situations when no tweet is posted in the city
            if os.path.exists(os.path.join(data_paths.count_daily_hour_path, city)):
                if count_obj.count_in_utc:
                    count_final.to_csv((os.path.join(data_paths.count_daily_hour_path, city,
                                                     '(UTC){}_count_combine.csv'.format(city))))
                else:
                    count_final.to_csv((os.path.join(data_paths.count_daily_hour_path, city,
                                                     '{}_count_combine.csv'.format(city))))
            else:
                os.mkdir(os.path.join(data_paths.count_daily_hour_path, city))
                if count_obj.count_in_utc:
                    count_final.to_csv((os.path.join(data_paths.count_daily_hour_path, city,
                                                     '(UTC){}_count_combine.csv'.format(city))))
                else:
                    count_final.to_csv((os.path.join(data_paths.count_daily_hour_path, city,
                                                     '{}_count_combine.csv'.format(city))))
        else:
            print('Tweets posted in {} have been counted'.format(city))


if __name__ == '__main__':
    considered_cities = {'hong_kong'}
    main_count_tweets(count_in_utc=True, considered_city_names=considered_cities)
