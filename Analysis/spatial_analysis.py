import os
import numpy as np
import pandas as pd
import geopandas as gpd
from cities_bounds import cities_dict_foreign, open_space_saving_path, cities_dict_china
from utils import column_dtype_dict
from count_tweets import CountTweets

# Cope with some bad latitude and longitude data
lat_lon_start_tuple = tuple([str(val) for val in range(10)] + ['-'])
print(lat_lon_start_tuple)

# Used column names and data types for tweets
considered_colnames = list(column_dtype_dict.keys())
dtype_dict = {'user_id_str': str, 'id_str': str, 'text': str,
              'created_at': str, 'verified': str, 'lang': str, 'url': str}
print('The considered columns in the tweet dataframe: {}'.format(considered_colnames))
print('The convert datatypes: {}'.format(dtype_dict))


class FindTweetsOpenSpace(object):
    considered_years = [str(year) for year in range(2016, 2021, 1)]

    def __init__(self, city_name, open_space_data: gpd.geodataframe,
                 tweet_data: pd.DataFrame, city_profile):
        """
        Initialize the object
        :param city_name: the name of the city
        :param open_space_data: the shapefile of the open space of a city
        :param tweet_data: the tweet pandas dataframe having latitude and longitude information
        :param city_profile: the dictionary containing the profile of a city
        """
        self.city_name = city_name
        self.open_space = open_space_data
        self.tweets = tweet_data
        self.city_shapefile_loc = city_profile[city_name][5]

    def find_tweets_in_open_space(self):
        """
        Find the tweets posted in one city's open space
        :return: tweets posted in open space
        """
        tweets_in_city = self.find_tweet_in_city()
        tweets_in_city = tweets_in_city.drop(['index_right'], axis=1)
        joined_data = gpd.sjoin(left_df=tweets_in_city, right_df=self.open_space, op='within')
        joined_data_final = joined_data.drop_duplicates(subset=['id_str'])
        return joined_data_final

    def find_tweet_in_city(self):
        """
        Find the tweets posted in the city based on the 'lat' and 'lon' columns
        :param dataframe: a pandas dataframe saving the geocoded tweets
        :return: tweets posted in the city
        """
        if (self.tweets['lat'].dtype.name != 'float64') or (self.tweets['lon'].dtype.name != 'float64'):
            dataframe_copy = self.tweets.copy()
            dataframe_copy['lat'] = dataframe_copy['lat'].astype(str)
            dataframe_copy['lon'] = dataframe_copy['lon'].astype(str)
            dataframe_copy_select = dataframe_copy[dataframe_copy['lat'].str.startswith(
                lat_lon_start_tuple)]
            dataframe_final = dataframe_copy_select[dataframe_copy_select['lon'].str.startswith(
                lat_lon_start_tuple)].copy()
            dataframe_final['lat'] = dataframe_final['lat'].astype(np.float64)
            dataframe_final['lon'] = dataframe_final['lon'].astype(np.float64)
        else:
            dataframe_final = self.tweets.copy()
        geocoded_tweet_gdf = gpd.GeoDataFrame(dataframe_final,
                                              geometry=gpd.points_from_xy(dataframe_final.lon,
                                                                          dataframe_final.lat))
        geocoded_tweet_gdf = geocoded_tweet_gdf.set_crs(epsg=4326, inplace=True)
        city_shape = gpd.read_file(self.city_shapefile_loc)
        city_shape_4326 = city_shape.to_crs(epsg=4326)
        joined_data_final = CountTweets.spatial_join(tweet_gdf=geocoded_tweet_gdf, shape_area=city_shape_4326)
        return joined_data_final.reset_index(drop=True)

    @staticmethod
    def preprocess_geoinfo(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Some geo-information is not saved correctly. Preprocess the geo-information
        :param dataframe: a pandas dataframe saving the geocoded tweets
        :return: a pandas dataframe with correct location information
        """
        if (dataframe['lat'].dtype.name != 'float64') or (dataframe['lon'].dtype.name != 'float64'):
            dataframe_copy = dataframe.copy()
            dataframe_copy['lat'] = dataframe_copy['lat'].astype(str)
            dataframe_copy['lon'] = dataframe_copy['lon'].astype(str)
            dataframe_copy_select = dataframe_copy[
                dataframe_copy['lat'].str.startswith(lat_lon_start_tuple)]
            dataframe_final = dataframe_copy_select[
                dataframe_copy_select['lon'].str.startswith(lat_lon_start_tuple)].copy()
            dataframe_final['lat'] = dataframe_final['lat'].astype(np.float64)
            dataframe_final['lon'] = dataframe_final['lon'].astype(np.float64)
        else:
            dataframe_final = dataframe.copy()
        return dataframe_final

    @staticmethod
    def find_tweet_in_box(dataframe, bounding_box_values) -> pd.DataFrame:
        """
        Find the geocoded tweets posted in one city
        Args:
            dataframe: a tweet pandas dataframe
            bounding_box_values: the bounding box of the studied city
        Returns:
        """
        lat_min, lat_max = bounding_box_values[1], bounding_box_values[3]
        lon_min, lon_max = bounding_box_values[0], bounding_box_values[2]
        # Cope with some bad rows where the geoinformation is stored as a strange string
        if (dataframe['lat'].dtype.name != 'float64') or (dataframe['lon'].dtype.name != 'float64'):
            print('The geoinformation of this dataframe is not saved correctly')
            dataframe_copy = dataframe.copy()
            dataframe_copy['lat'] = dataframe_copy['lat'].astype(str)
            dataframe_copy['lon'] = dataframe_copy['lon'].astype(str)
            dataframe_copy_select = dataframe_copy[
                dataframe_copy['lat'].str.startswith(lat_lon_start_tuple)]
            dataframe_final = dataframe_copy_select[
                dataframe_copy_select['lon'].str.startswith(lat_lon_start_tuple)]
            dataframe_final['lat'] = dataframe_final['lat'].astype(np.float64)
            dataframe_final['lon'] = dataframe_final['lon'].astype(np.float64)
        else:
            dataframe_final = dataframe.copy()
        decision1 = (dataframe_final['lat'] >= lat_min) & (dataframe_final['lat'] <= lat_max)
        decision2 = (dataframe_final['lon'] >= lon_min) & (dataframe_final['lon'] <= lon_max)
        data_in_city = dataframe_final[decision1 & decision2]
        assert type(data_in_city) == pd.DataFrame, 'The output type of dataframe is not right.'
        return data_in_city

    @staticmethod
    def find_tweet_place_in_box(dataframe, bounding_box_values):
        """
        Find the tweets in the city based on the 'place_lat' and 'place_lon' columns
        Args:
            dataframe: a tweet pandas dataframe
            bounding_box_values: the bounding box of the studied city
        Returns:
        """
        lat_min, lat_max = bounding_box_values[1], bounding_box_values[3]
        lon_min, lon_max = bounding_box_values[0], bounding_box_values[2]
        # Cope with some bad rows where the geoinformation is stored as a strange string
        if (dataframe['place_lat'].dtype.name != 'float64') or (dataframe['place_lon'].dtype.name != 'float64'):
            print('The geoinformation of this dataframe is not saved correctly')
            dataframe_copy = dataframe.copy()
            dataframe_copy['place_lat'] = dataframe['place_lat'].astype(str)
            dataframe_copy['place_lon'] = dataframe['place_lon'].astype(str)
            dataframe_copy_select = dataframe_copy[
                dataframe_copy['place_lat'].str.startswith(lat_lon_start_tuple)]
            dataframe_final = dataframe_copy_select[
                dataframe_copy_select['place_lon'].str.startswith(lat_lon_start_tuple)]
            dataframe_final['place_lat'] = dataframe_final['place_lat'].astype(np.float64)
            dataframe_final['place_lon'] = dataframe_final['place_lon'].astype(np.float64)
        else:
            dataframe_final = dataframe.copy()
        decision1 = (dataframe_final['place_lat'] >= lat_min) & (dataframe_final['place_lat'] <= lat_max)
        decision2 = (dataframe_final['place_lon'] >= lon_min) & (dataframe_final['place_lon'] <= lon_max)
        data_in_city = dataframe_final[decision1 & decision2]
        assert type(data_in_city) == pd.DataFrame, 'The output type of dataframe is not right.'
        return data_in_city


def main_foreign(considered_cities: set, cities_profile: dict, save_threshold: int, open_space_save_path: str):
    """
    The main function to find the tweets posted in open space of foreign cities
    :param considered_cities: a python set saving the name of the cities you want to process
    :param cities_profile: a python dictionary saving the bounding box, timezone, tweet data location,
    and open space shapefile
    :param save_threshold: a threshold that let the program save the tweets posted in open space
    :param open_space_save_path: the path used to save the tweets posted in open space
    :return: None. The tweets posted in open space are saved to local directory
    """
    consider_years = [str(year) for year in [2016, 2017, 2018, 2019, 2020, 2021]]
    for studied_city in cities_profile:
        print('Coping with the city: {}'.format(studied_city))
        if studied_city in considered_cities:
            tweet_num_counter, file_counter = 0, 0
            print('Load the open space data...')
            open_space = gpd.read_file(cities_profile[studied_city][3],
                                       encoding='utf-8')
            open_space_4326 = open_space.to_crs(epsg=4326)
            print('Done! Start processing the tweets...')
            data_list = []
            for year in consider_years:
                if year in os.listdir(os.path.join(cities_profile[studied_city][2])):
                    print('For the tweets posted in {}'.format(year))
                    csv_path = os.path.join(cities_profile[studied_city][2], year)
                    for file in os.listdir(csv_path):
                        try:
                            data = pd.read_csv(open(os.path.join(csv_path, file), encoding='utf-8', errors='ignore'),
                                               usecols=considered_colnames, dtype=dtype_dict)
                            geocoded_data = data.loc[~data['lat'].isna()]
                            # geocoded_in_box = CountTweets.find_tweet_in_bounding_box(
                            #     dataframe=geocoded_final, bounding_box_vals=cities_profile[studied_city][0])
                            find_obj = FindTweetsOpenSpace(open_space_data=open_space_4326,
                                                           tweet_data=geocoded_data,
                                                           city_name=studied_city,
                                                           city_profile=cities_profile)
                            tweets_in_open_space = find_obj.find_tweets_in_open_space()
                            data_list.append(tweets_in_open_space)
                            tweet_num_counter += tweets_in_open_space.shape[0]
                            if tweet_num_counter > save_threshold:
                                print('Found {} tweets posted in open space. Saving...'.format(tweet_num_counter))
                                file_counter += 1
                                concat_data = pd.concat(data_list, axis=0)
                                concat_data = concat_data.to_crs(epsg=4326)  # set the crs of the tweets in open space
                                if os.path.exists(os.path.join(open_space_save_path, studied_city)):
                                    concat_data.to_file(os.path.join(open_space_save_path, studied_city,
                                                                     '{}_{}.shp'.format(studied_city,
                                                                                        file_counter)),
                                                       encoding='utf-8')
                                    concat_data.to_csv(os.path.join(open_space_save_path, studied_city,
                                                                    '{}_{}.csv'.format(studied_city,
                                                                                       file_counter)),
                                                      encoding='utf-8')
                                else:
                                    os.mkdir(os.path.join(open_space_save_path, studied_city))
                                    concat_data.to_file(os.path.join(open_space_save_path, studied_city,
                                                                     '{}_{}.shp'.format(studied_city,
                                                                                        file_counter)),
                                                       encoding='utf-8')
                                    concat_data.to_csv(os.path.join(open_space_save_path, studied_city,
                                                                    '{}_{}.csv'.format(studied_city,
                                                                                       file_counter)),
                                                      encoding='utf-8')
                                print('Done!')
                                data_list = []
                                tweet_num_counter = 0
                        except ValueError:
                            print('ValueError occurs for file: {}. Ignore.'.format(file))
                        except pd.errors.ParserError:
                            print('Parser error occurred in file: {}. Ignore.'.format(file))
                        except KeyError:
                            print('The file {} has some column errors. Ignore'.format(file))
            concat_data = pd.concat(data_list, axis=0)
            concat_data = concat_data.to_crs(epsg=4326)  # set the crs of the tweets in open space

            if os.path.exists(os.path.join(open_space_save_path, studied_city)):
                concat_data.to_file(
                    os.path.join(open_space_save_path, studied_city,
                                 '{}_final.shp'.format(studied_city)),
                    encoding='utf-8')
                concat_data.to_csv(
                    os.path.join(open_space_save_path, studied_city, '{}_final.csv'.format(studied_city)),
                    encoding='utf-8')
            else:
                os.mkdir(os.path.join(open_space_save_path, studied_city))
                concat_data.to_file(
                    os.path.join(open_space_save_path, studied_city,
                                 '{}_final.shp'.format(studied_city)),
                    encoding='utf-8')
                concat_data.to_csv(
                    os.path.join(open_space_save_path, studied_city, '{}_final.csv'.format(studied_city)),
                    encoding='utf-8')


def main_china(considered_cities: set, cities_profile: dict, save_threshold: int, open_space_save_path: str):
    """
    The main function to find the Weibos posted in open space of Chinese cities
    :param considered_cities: a python set saving the name of the cities you want to process
    :param cities_profile: a python dictionary saving the bounding box, timezone, tweet data location,
    and open space shapefile
    :param save_threshold: a threshold that let the program save the tweets posted in open space
    :param open_space_save_path: the path used to save the tweets posted in open space
    :return: None. The tweets posted in open space are saved to local directory
    """
    for studied_city in cities_profile:
        print('Coping with the city: {}'.format(studied_city))
        if studied_city in considered_cities:
            weibo_num_counter, file_counter = 0, 0
            print('Load the open space data...')
            open_space = gpd.read_file(cities_profile[studied_city][3],
                                       encoding='utf-8')
            open_space_4326 = open_space.to_crs(epsg=4326)
            print('Done! Start processing the Weibos...')
            data_list = []
            csv_path = cities_profile[studied_city][2]
            print('The Weibo data path is: {}'.format(csv_path))
            for file in os.listdir(csv_path):
                print('Coping with the file: {}'.format(file))
                try:
                    data = pd.read_csv(os.path.join(csv_path, file), encoding='utf-8', dtype='str')
                    data_renamed = data.rename(columns={'latitude': 'lat', 'longitude': 'lon',
                                                        'weibo_id': 'id_str',
                                                        'author_id': 'user_id_str'})
                    geocoded_data = data_renamed.loc[~data_renamed['lat'].isna()]
                    find_obj = FindTweetsOpenSpace(open_space_data=open_space_4326,
                                                   tweet_data=geocoded_data,
                                                   city_name=studied_city,
                                                   city_profile=cities_profile)
                    weibos_in_open_space = find_obj.find_tweets_in_open_space()
                    data_list.append(weibos_in_open_space)
                    weibo_num_counter += weibos_in_open_space.shape[0]
                    if weibo_num_counter > save_threshold:
                        print('Found {} tweets posted in open space. Saving...'.format(weibo_num_counter))
                        file_counter += 1
                        concat_data = pd.concat(data_list, axis=0)
                        concat_data = concat_data.to_crs(epsg=4326)  # set the crs of the tweets in open space
                        if os.path.exists(os.path.join(open_space_save_path, studied_city)):
                            concat_data.to_file(os.path.join(open_space_save_path, studied_city,
                                                             '{}_{}.shp'.format(studied_city,
                                                                                file_counter)),
                                               encoding='utf-8')
                            concat_data.to_csv(os.path.join(open_space_save_path, studied_city,
                                                            '{}_{}.csv'.format(studied_city,
                                                                               file_counter)),
                                              encoding='utf-8')
                        else:
                            os.mkdir(os.path.join(open_space_save_path, studied_city))
                            concat_data.to_file(os.path.join(open_space_save_path, studied_city,
                                                             '{}_{}.shp'.format(studied_city,
                                                                                file_counter)),
                                               encoding='utf-8')
                            concat_data.to_csv(os.path.join(open_space_save_path, studied_city,
                                                            '{}_{}.csv'.format(studied_city,
                                                                               file_counter)),
                                              encoding='utf-8')

                        print('Done!')
                        data_list = []
                        weibo_num_counter = 0
                except ValueError:
                    print('ValueError occurs for file: {}. Ignore.'.format(file))
                except pd.errors.ParserError:
                    print('Parser error occurred in file: {}. Ignore.'.format(file))
                # except KeyError:
                #     print('The file {} has some column errors. Ignore'.format(file))
            if len(data_list) != 0:
                concat_data = pd.concat(data_list, axis=0)
                concat_data = concat_data.to_crs(epsg=4326)  # set the crs of the tweets in open space
                if os.path.exists(os.path.join(open_space_save_path, studied_city)):
                    concat_data.to_file(
                        os.path.join(open_space_save_path, studied_city,
                                     '{}_final.shp'.format(studied_city)),
                        encoding='utf-8')
                    concat_data.to_csv(
                        os.path.join(open_space_save_path, studied_city, '{}_final.csv'.format(studied_city)),
                        encoding='utf-8')
                else:
                    os.mkdir(os.path.join(open_space_save_path, studied_city))
                    concat_data.to_file(
                        os.path.join(open_space_save_path, studied_city,
                                     '{}_final.shp'.format(studied_city)),
                        encoding='utf-8')
                    concat_data.to_csv(
                        os.path.join(open_space_save_path, studied_city, '{}_final.csv'.format(studied_city)),
                        encoding='utf-8')

        else:
            print('The profile of the city {} has been prepared yet.'.format(studied_city))


if __name__ == '__main__':
    # Find the Weibos posted in Chinese cities' open space
    considered_chinese_set = {'shanghai'}
    main_china(considered_chinese_set, cities_profile=cities_dict_china, save_threshold=50000,
               open_space_save_path = open_space_saving_path)
