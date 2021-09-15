import os
import rasterio
import geopandas as gpd
import pandas as pd
import numpy as np
from pyproj import Transformer
import pytz

from data_paths import ndvi_path, raster_save_path
from cities_bounds import cities_dict_foreign, open_space_saving_path,cities_dict_china, cities_dict_netherland
from utils import column_dtype_dict, read_csv_columns, transform_string_time_to_datetime, get_time_attributes
from spatial_analysis import FindTweetsOpenSpace


def raster_overview(path: str, file_name: str):
    """
    Create an overview of a raster file
    :param path: the path to a raster file
    :param file_name: the name of a raster file
    :return:
    """
    with rasterio.open(os.path.join(path, file_name)) as src:
        print(src.width, src.height)  # Height and Width
        print(src.crs)  # The Coordinate System
        print(src.transform)  # The Affine Transform
        print(src.count)  # Number of Raster
        print(src.indexes)  # Raster Index


def compute_raster_for_points(point_filename: str, raster_filename: str,
                              bot_ids: set,
                              read_csv_file: bool = True,
                              process_tweet: bool = True):
    """
    Compute the raster value for each point in the shapefile. For more
    information, please check:
    https://gis.stackexchange.com/questions/317391/python-extract-raster-values-at-point-locations/324830
    :param point_filename: the full path to the point filename
    :param raster_filename: the full path of the NDVI raster .tif file
    :param bot_ids: a python set containing the bot ids
    :param read_csv_file: boolean. read the csv file or not
    :return: the point shapefile with raster value
    """
    # Open the raster and store metadata
    src = rasterio.open(raster_filename)
    src_crs = src.crs.to_epsg()
    # Get the coordinate system for the raster
    # file saving the NDVI value
    transformer = Transformer.from_crs(crs_from="epsg:4326", crs_to=src_crs,
                                       always_xy=False)

    # Read points from shapefile
    if read_csv_file:
        if process_tweet:
            pts = pd.read_csv(point_filename, usecols=['user_id_str', 'id_str',
                                                       'text', 'created_at',
                                                       'lat', 'lon',
                                                       'place_lat',
                                                       'place_lon', 'verified',
                                                       'lang', 'url'],
                              dtype={'user_id_str': str})
        else:
            pts = pd.read_csv(point_filename, usecols=['user_id_str', 'id_str',
                                                       'text', 'created_at',
                                                       'lat', 'lon', 'url'])

    else:
        pts = gpd.read_file(point_filename)
    pts_without_bot = pts.loc[~pts['user_id_str'].isin(bot_ids)].copy()
    pts_processed = FindTweetsOpenSpace.preprocess_geoinfo(pts_without_bot)

    pts_processed.index = range(len(pts_processed))
    coords = [(x, y) for x, y in zip(pts_processed.lat, pts_processed.lon)]
    transformed_coords = [transformer.transform(coord[0], coord[1])
                          for coord in coords]

    # Sample the raster at every point location and store values in DataFrame
    pts_processed['Raster_Value'] = [x[0] for x in src.sample(
        transformed_coords, masked=True)]

    return pts_processed


def main_foreign_raster(save_path, considered_cities=None,
                        city_profile=cities_dict_foreign):
    """
    Get the NDVI raster value for each geocoded tweet posted in open space
    :return: None. The NDVI raster value for each geocoded tweet is saved to
    a specified local directory
    """
    tif_files = [file for file in os.listdir(ndvi_path) if file.endswith('.tif')]
    print('The raster files: {}'.format(tif_files))

    for city in city_profile:
        if city in considered_cities:
            print('-'*20)
            print('Coping with the city: {}'.format(city))
            # Get all the csv files saving tweets posted in open space
            city_open_space_tweet_path = os.path.join(open_space_saving_path, city)
            csv_files = [file for file in os.listdir(city_open_space_tweet_path) if (file.endswith('.csv')) and (city in file)]
            print('Considered csv files: {}'.format(csv_files))
            # Get the raster value for each geocoded tweet
            for csv_file in csv_files:
                if 'netherland' in city:
                    output_file = compute_raster_for_points(
                        point_filename=os.path.join(city_open_space_tweet_path, csv_file),
                        raster_filename=os.path.join(ndvi_path, 'netherlands_NDVI.tif'),
                        bot_ids=set(np.load(city_profile[city][4],
                                        allow_pickle=True).tolist()),
                        read_csv_file=True, process_tweet=True)
                else:
                    output_file = compute_raster_for_points(
                        point_filename=os.path.join(city_open_space_tweet_path, csv_file),
                        raster_filename=os.path.join(ndvi_path, '{}_NDVI.tif'.format(city)),
                        bot_ids=set(np.load(city_profile[city][4],
                                        allow_pickle=True).tolist()),
                        read_csv_file=True, process_tweet=True)

                output_file['utc_time'] = output_file.apply(
                    lambda row: transform_string_time_to_datetime(row['created_at'],
                                                                  convert_utc_time=True,
                                                                  target_time_zone=pytz.utc), axis=1)
                output_file_with_time = get_time_attributes(output_file, datetime_obj_colname='utc_time')

                if os.path.exists(os.path.join(save_path, city)):
                    output_file_with_time.to_csv(os.path.join(save_path, city, csv_file[:-4] + '_with_raster.csv'),
                                                 encoding='utf-8')
                else:
                    os.mkdir(os.path.join(save_path, city))
                    output_file_with_time.to_csv(os.path.join(save_path, city, csv_file[:-4] + '_with_raster.csv'),
                                                 encoding='utf-8')
                print('The file {} has been processed'.format(csv_file))
            print('-' * 20)
            print('\n')
        else:
            print('We do not consider {} this time.'.format(city))


def main_china_raster(save_path: str, considered_cities=None,
                      city_profile=cities_dict_china):
    """
    Get the NDVI raster value for each geocoded tweet posted in open space
    save_path: the path used to save the output to the local directory
    considered_cities: a set containing the considered cities
    city_profile: a python dict containing the basic information for each
    mainland Chinese cities
    :return: None. The NDVI raster value for each geocoded tweet is saved to
    a specified local directory
    """
    for city in city_profile:
        if city in considered_cities:
            print('-'*20)
            print('Coping with the city: {}'.format(city))
            # Get all the csv files saving tweets posted in open space
            city_open_space_weibo_path = os.path.join(open_space_saving_path,
                                                      city)
            csv_files = [file for file in os.listdir(
                city_open_space_weibo_path) if (
                    file.endswith('.csv')) and (city in file)]
            weibo_bot_ids = np.load("weibo_bots_final.npy", allow_pickle=True)
            print('Considered csv files: {}'.format(csv_files))
            # Get the raster value for each geocoded tweet
            for csv_file in csv_files:
                output_file = compute_raster_for_points(
                    point_filename=os.path.join(city_open_space_weibo_path,
                                                csv_file),
                    raster_filename=os.path.join(ndvi_path,
                                                 '{}_NDVI.tif'.format(city)),
                    bot_ids=weibo_bot_ids,
                    read_csv_file=True, process_tweet=False)

                output_file['utc_time'] = output_file.apply(
                    lambda row: transform_string_time_to_datetime(
                        row['created_at'], convert_utc_time=True,
                        target_time_zone=pytz.utc), axis=1)
                output_file_with_time = get_time_attributes(
                    output_file, datetime_obj_colname='utc_time')

                if os.path.exists(os.path.join(save_path, city)):
                    output_file_with_time.to_csv(os.path.join(
                        save_path, city, csv_file[:-4] + '_with_raster.csv'),
                                                 encoding='utf-8')
                else:
                    os.mkdir(os.path.join(save_path, city))
                    output_file_with_time.to_csv(os.path.join(
                        save_path, city, csv_file[:-4] + '_with_raster.csv'),
                                                 encoding='utf-8')
                print('The file {} has been processed'.format(csv_file))
            print('-' * 20)
            print('\n')
        else:
            print('We do not consider {} this time.'.format(city))


if __name__ == '__main__':
    considered_cities_foreign = set(cities_dict_foreign.keys())
    considered_cities_foreign.remove('netherlands')
    main_foreign_raster(save_path=raster_save_path,
                       considered_cities = considered_cities_foreign,
                       city_profile=cities_dict_foreign)
