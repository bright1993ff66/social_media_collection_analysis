# encoding = 'utf-8'
# Basics
import os
import numpy as np
import pytz
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import pandas as pd

# For spatial analysis
import geopandas as gpd

# For path and functions for visualizations
import data_paths
from cities_bounds import cities_dict_china, open_space_saving_path
from utils import transform_string_time_to_datetime, merge_dict, create_dataframe_from_dict, sum_dataframe_list_count
from visualizations import create_day_plot_for_one_count, create_hour_weekday_plot


# Cope with some bad latitude and longitude data
lat_lon_start_tuple = tuple([str(val) for val in range(10)] + ['-'])
print(lat_lon_start_tuple)


class CountWeibos(object):
    """
    Count the number of geocoded Weibos posted in one city
    """

    def __init__(self, city_name, city_profile_dict, start_time, end_time,
                 save_loc: str, save_filename: str, utc_or_not: bool = True):
        assert city_name in city_profile_dict, 'The name of the city is not right!'
        self.city_name = city_name
        self.city_bounding_box = city_profile_dict[city_name][0]
        self.city_timezone = city_profile_dict[city_name][1]
        self.city_loc = city_profile_dict[city_name][2]
        self.city_open_space = city_profile_dict[city_name][3]
        if type(city_profile_dict[city_name][4]) == str:
            self.bot_ids = np.load(city_profile_dict[city_name][4],
                                   allow_pickle=True)
        else:
            self.bot_ids = city_profile_dict[city_name][4]
        self.start_time = start_time
        self.end_time = end_time
        self.save_loc = save_loc
        self.save_filename = save_filename
        self.utc_or_not = utc_or_not
        self.city_shapefile_loc = city_profile_dict[city_name][5]

    def count_geocoded_weibos_hour(self):

        """
        Count the geocoded weibos (lat and lon) posted in each hour of the study time
        :return: a pandas dataframe saving the number of Weibos posted in each hour of the study time
        """

        # Create a dictionary to save the number of Weibos posted in each hour
        considered_geocoded_time_count_dict = defaultdict()

        # Count the Weibos...
        csv_path = self.city_loc
        for csv_file in list(filter(lambda f: f.endswith('.csv'), os.listdir(csv_path))):
            try:
                print('Counting the Weibos posted in city for file: {}'.format(csv_file))
                dataframe = pd.read_csv(os.path.join(csv_path, csv_file), encoding='utf-8', index_col=0, dtype='str')
                geocoded_dataframe = dataframe.loc[~dataframe['lat'].isnull()]
                data_renamed = geocoded_dataframe.rename(columns={'latitude': 'lat', 'longitude': 'lon',
                                                                  'weibo_id': 'id_str',
                                                                  'author_id': 'user_id_str'})
                geocoded_without_duplicates = data_renamed.drop_duplicates(subset=['id_str'])
                geocoded_without_bot = geocoded_without_duplicates.loc[
                    ~geocoded_without_duplicates['user_id_str'].isin(self.bot_ids)]
                geocoded_weibo_city = self.find_weibo_in_city(dataframe=geocoded_without_bot)

                # Process the dataframe with lat and lon
                if geocoded_weibo_city.shape[0] == 0:
                    geocoded_weibo_counter = Counter()
                else:
                    geocoded_weibo_city_copy = geocoded_weibo_city.copy()
                    geocoded_weibo_city_copy['local_time'] = geocoded_weibo_city_copy.apply(
                        lambda row: transform_string_time_to_datetime(
                            time_string=row['created_at'], target_time_zone=self.city_timezone,
                            convert_utc_time=False), axis=1)
                    geocoded_weibo_city_copy['year_month_day_hour_weekday'] = geocoded_weibo_city_copy.apply(
                        lambda row: str(row['local_time'].year) + '_' + str(
                            row['local_time'].month) + '_' + str(
                            row['local_time'].day) + '_' + str(
                            row['local_time'].hour) + '_' + str(row['local_time'].weekday()), axis=1)
                    geocoded_weibo_counter = Counter(geocoded_weibo_city_copy['year_month_day_hour_weekday'])
                considered_geocoded_time_count_dict = merge_dict(sum_dict=considered_geocoded_time_count_dict,
                                                                 a_dict=geocoded_weibo_counter)
            #except KeyError:
                #print('The csv file: {} does not have any colnames.Ignore'.format(csv_file))
            except ValueError:
                print('ValueError occurs for file: {}. Ignore.'.format(csv_file))
            except pd.errors.ParserError:
                print('Parser error occurred in file: {}. Ignore.'.format(csv_file))
        # print('Geocoded count dict: {}'.format(considered_geocoded_time_count_dict))
        count_dataframe = create_dataframe_from_dict(dict_data=considered_geocoded_time_count_dict)
        default_dataframe_each_hour = self.create_count_dataframe()
        final_count = pd.merge(left=count_dataframe, right=default_dataframe_each_hour,
                               on=['year', 'month', 'day', 'hour', 'weekday'], how='right')
        final_count['total_count_x'] = final_count['total_count_x'].fillna(0)
        final_count_droped = final_count.drop(['total_count_y'], axis=1)
        final_count_renamed = final_count_droped.rename(columns={'total_count_x': 'total_count'})
        # Save the combined file to the local directory
        print('Done!')
        if os.path.exists(os.path.join(self.save_loc, self.city_name)):
            final_count_renamed.to_csv(os.path.join(self.save_loc, self.city_name, self.save_filename),
                                             encoding='utf-8')
        else:
            os.mkdir(os.path.join(self.save_loc, self.city_name))
            final_count_renamed.to_csv(os.path.join(self.save_loc, self.city_name, self.save_filename),
                                             encoding='utf-8')
        return final_count_renamed

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

    def get_weibo_from_id_set(self, weibo_id_set, save_path, save_filename):
        """
        Get the weibos by the weibo id(int64)
        Args:
            weibo_id_set: a Python set saving the interested weibo ids
            save_path: the path used to save the selected dataframe
            save_filename: the filename of the selected dataframe
        Returns: None
        """
        select_data_list = []
        csv_file_path = os.path.join(self.city_loc, 'weibos')
        for file in list(filter(lambda f: f.endswith('.csv'), os.listdir(csv_file_path))):
            try:
                dataframe = pd.read_csv(os.path.join(csv_file_path, file), encoding='utf-8', index_col=0, dtype='str')
                data_renamed = dataframe.rename(columns={'latitude': 'lat', 'longitude': 'lon', 'weibo_id': 'id_str'})
                geocoded_weibo_city = data_renamed.drop_duplicates(subset=['id_str'])
                geocoded_weibo_city['id_str'] = geocoded_weibo_city['id_str'].astype(np.int64)
                dataframe_select = dataframe.loc[dataframe['id_str'].isin(weibo_id_set)]
                select_data_list.append(dataframe_select)
            except ValueError:
                print('ValueError occurred when reading file: {}. Ignore'.format(file))
                continue
            except pd.errors.ParserError:
                print('Parser error occurred in file: {}. Ignore.'.format(file))
                continue
        result_dataframe = pd.concat(select_data_list, axis=0)
        result_dataframe_reindex = result_dataframe.reset_index(drop=True)
        result_dataframe_reindex.to_csv(os.path.join(save_path, save_filename),
                                        encoding='utf-8')


    def find_weibo_in_city(self, dataframe):
        """
        Find the tweets posted in the city based on the 'lat' and 'lon' columns
        :param dataframe: a pandas dataframe saving the geocoded tweets
        :return: tweets posted in the city
        """
        assert 'lat' in dataframe, "The dataframe should contain latitude info"
        assert 'lon' in dataframe, "The dataframe should contain longitude info"
        if (dataframe['lat'].dtype.name != 'float64') or (dataframe['lon'].dtype.name != 'float64'):
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
        joined_data_final = CountWeibos.spatial_join(tweet_gdf=geocoded_tweet_gdf, shape_area=city_shape_4326)
        return joined_data_final.reset_index(drop=True)


    def find_weibo_in_bounding_box(self, dataframe):
        """
        Find the geocoded weibos posted in one city's bounding box based on the 'lat' and 'lon' columns
        Args:
            dataframe: a weibo pandas dataframe
            bounding_box_vals: the bounding box of the studied city
        Returns:

        """
        lat_min, lat_max = self.bounding_box_vals[1], self.bounding_box_vals[3]
        lon_min, lon_max = self.bounding_box_vals[0], self.bounding_box_vals[2]
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


class CountWeibosOpenSpace(object):

    def __init__(self, city_name: str, cities_profile_dict: dict,
                 start_time: datetime, end_time: datetime,
                 save_loc: str, save_filename: str, utc_or_not: bool):
        """
        Count the Weibos posted in one city's open space
        :param city_name: the name of the studied city
        :param cities_profile_dict: a dictionary saving the profile
        information of this city
        :param start_time: the starting time that this counting
        process considered
        :param end_time: the ending time that this counting process considered
        :param save_loc: the save location in the local directory
        :param save_filename: the save filename
        """
        self.city_name = city_name
        if utc_or_not:
            self.timezone = pytz.utc
        else:
            self.timezone = cities_profile_dict[city_name][1]
        self.data_loc = os.path.join(open_space_saving_path, self.city_name)
        self.start_time = start_time
        self.end_time = end_time
        self.save_loc = save_loc
        self.save_filename = save_filename
        bot_ids = np.load(os.path.join(os.getcwd(), "weibo_bots_final.npy"),
                          allow_pickle=True)
        self.bot_ids = bot_ids

    def count_weibos_hourly(self, day_title: str, hour_title: str,
                            weekday_title: str, day_filename: str,
                            hour_filename: str,
                            weekday_filename: str) -> pd.DataFrame:
        """
        Count the number of Weibos posted in each hour of a open space in the studied city
        :return: None. The result is saved in the specified local directory
        """
        result_dataframe_list = []
        for file in os.listdir(self.data_loc):
            cur_time = self.start_time
            if file.endswith('.csv'):
                print('Counting the Weibos posted in open space for file: {}'.format(file))
                dataframe = pd.read_csv(os.path.join(self.data_loc, file), encoding='utf-8', index_col=0, dtype='str')
                # Get the local time and year, month, day, hour attributes
                dataframe['local_time'] = dataframe.apply(
                    lambda row: transform_string_time_to_datetime(row['created_at'], target_time_zone=self.timezone,
                                                                  convert_utc_time=False), axis=1)
                dataframe['year'] = dataframe.apply(lambda row: row['local_time'].year, axis=1)
                dataframe['month'] = dataframe.apply(lambda row: row['local_time'].month, axis=1)
                dataframe['day'] = dataframe.apply(lambda row: row['local_time'].day, axis=1)
                dataframe['hour'] = dataframe.apply(lambda row: row['local_time'].hour, axis=1)
                print('Done!')

                # Count the number of Weibos in each hour
                print('Counting the number of Weibos posted in each hour...')
                result_count_list = []
                result_time_list = []

                while self.end_time != cur_time:
                    check_time_year, check_time_month = cur_time.year, cur_time.month
                    check_time_day, check_time_hour = cur_time.day, cur_time.hour
                    dataframe_year_month = dataframe.loc[
                        (dataframe['year'] == check_time_year) & (dataframe['month'] == check_time_month)]
                    dataframe_day_hour = dataframe_year_month.loc[
                        (dataframe_year_month['day'] == check_time_day) & (
                                dataframe_year_month['hour'] == check_time_hour)]
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

        # Create the hour, day, and weekday plots
        print('Plotting the number of Weibos on each day...')
        create_day_plot_for_one_count(combined_result_dataframe, title=day_title, start_date=self.start_time,
                                      end_date=self.end_time, save_filename=day_filename, in_china=True)
        print('Done! Plotting the number of Weibos in each hour and weekday...')
        create_hour_weekday_plot(combined_result_dataframe, title_hour=hour_title, title_weekday=weekday_title,
                                 color_hour='#FB8072', color_weekday='#80B1D3', hour_save_filename=hour_filename,
                                 weekday_save_filename=weekday_filename, in_china=True)

        # Save the combined file to the local directory
        print('Done!')
        if os.path.exists(os.path.join(self.save_loc, self.city_name)):
            combined_result_dataframe.to_csv(os.path.join(self.save_loc, self.city_name, self.save_filename),
                                             encoding='utf-8')
        else:
            os.mkdir(os.path.join(self.save_loc, self.city_name))
            combined_result_dataframe.to_csv(os.path.join(self.save_loc, self.city_name, self.save_filename),
                                             encoding='utf-8')
        return combined_result_dataframe


def main_count_weibos(count_in_utc: bool, count_cities_mainland: set):
    """
    Main function to count the Weibos posted in the Chinese mainland city and
    open space
    :param: count_in_utc: whether count in utc or not
    :param: count_cities_mainland: a Python set saving the considered Chinese
    cities
    :return: None. The tweet counting in each hour is saved to local directory.
    The created figures are saved to the local directory.
    """
    for city in cities_dict_china:
        if city in count_cities_mainland:
            print('Coping with the city: {}'.format(city))
            if count_in_utc:
                timezone_info = pytz.utc
            else:
                timezone_info = cities_dict_china[city][1]
            count_weibo_obj = CountWeibos(city_name=city,
                                          city_profile_dict=cities_dict_china,
                                          save_loc=data_paths.count_daily_hour_path,
                                          save_filename=city + '_in_city_hour.csv',
                                          start_time=datetime(2011, 3, 1, 0, 0, 0, tzinfo=timezone_info),
                                          end_time=datetime(2015, 1, 1, 0, 0, 0, tzinfo=timezone_info),
                                          utc_or_not=True)
            count_weibo_open_space = CountWeibosOpenSpace(
                city_name=city, cities_profile_dict=cities_dict_china,
                start_time=datetime(2011, 3, 1, 0, 0, 0, tzinfo=timezone_info),
                end_time=datetime(2015, 1, 1, 0, 0, 0, tzinfo=timezone_info),
                save_loc=data_paths.count_daily_hour_path,
                save_filename=city + '_open_space_hour.csv',
                utc_or_not=True)
            geocoded_count_data = count_weibo_obj.count_geocoded_weibos_hour()
            geocoded_open_space_data = count_weibo_open_space.count_weibos_hourly(
                day_title='Number of Weibos Posted in {} Open Space on Each Day'.format(city),
                hour_title='Number of Weibos Posted in {} Open Space in Each Hour'.format(city),
                weekday_title='Number of Weibos Posted in {} Open Space on Each Weekday'.format(city),
                day_filename='{}_open_space_day.png'.format(city),
                hour_filename='{}_open_space_hour.png'.format(city),
                weekday_filename='{}_open_space_weekday.png'.format(city))
            final_data = pd.merge(left=geocoded_count_data, right=geocoded_open_space_data,
                                  on=['year', 'month', 'day', 'hour', 'weekday'])
            final_data['percent'] = (final_data['open_space_count']/final_data['total_count']).replace(
                to_replace=[np.inf, np.nan], value=-9999)  # For the situations when no tweet is posted in the city
            if os.path.exists(os.path.join(data_paths.count_daily_hour_path, city)):
                final_data.to_csv(
                    os.path.join(data_paths.count_daily_hour_path, city, '{}_combined.csv'.format(city)),
                    encoding='utf-8')
            else:
                os.mkdir(os.path.join(data_paths.count_daily_hour_path, city))
                final_data.to_csv(
                    os.path.join(data_paths.count_daily_hour_path, city, '{}_combined.csv'.format(city)),
                    encoding='utf-8')
        else:
            print("We don't consider city: {} now".format(city))


if __name__ == '__main__':
    considered_cities = {'shanghai'}
    main_count_weibos(count_in_utc=True,
                      count_cities_mainland=considered_cities)
