import os
import rasterio
import geopandas as gpd
import pandas as pd
from pyproj import Transformer

from data_paths import ndvi_path
from cities_bounds import cities_dict_foreign, open_space_saving_path


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


def compute_rater_for_points(point_filename: str, raster_filename: str, read_csv_file: bool = True):
    """
    Compute the raster value for each point in the shapefile. For more information, please check:
    https://gis.stackexchange.com/questions/317391/python-extract-raster-values-at-point-locations/324830
    :param point_filename: the full path to the point filename
    :param raster_filename: the full path of the NDVI raster .tif file
    :param read_csv_file: boolean. read the csv file or not
    :return: the point shapefile with raster value
    """
    # Open the raster and store metadata
    src = rasterio.open(raster_filename)
    src_crs = src.crs.to_epsg()  # Get the coordinate system for the raster file saving the NDVI value
    transformer = Transformer.from_crs(crs_from="epsg:4326", crs_to=src_crs, always_xy=False)

    # Read points from shapefile
    if read_csv_file:
        pts = pd.read_csv(point_filename)
    else:
        pts = gpd.read_file(point_filename)
    pts = pts[['lat', 'lon']]
    pts.index = range(len(pts))
    coords = [(x, y) for x, y in zip(pts.lat, pts.lon)]
    transformed_coords = [transformer.transform(coord[0], coord[1]) for coord in coords]

    # Sample the raster at every point location and store values in DataFrame
    pts['Raster_Value'] = [x[0] for x in src.sample(transformed_coords, masked=True)]

    return pts


def main_foreign(save_path):
    """
    Get the NDVI raster value for each geocoded tweet posted in open space
    :return: None. The NDVI raster value for each geocoded tweet is saved to a specified local directory
    """
    tif_files = [file for file in os.listdir(ndvi_path) if file.endswith('.tif')]
    print('The raster files: {}'.format(tif_files))

    for city in cities_dict_foreign:
        print('-'*20)
        print('Coping with the city: {}'.format(city))
        # Get all the csv files saving tweets posted in open space
        city_open_space_tweet_path = os.path.join(open_space_saving_path, city)
        csv_files = [file for file in os.listdir(city_open_space_tweet_path) if (
                file.endswith('.csv')) and (city in file)]
        print('The csv file is: {}'.format(csv_files))
        # Get the raster value for each geocoded tweet
        for csv_file in csv_files:
            output_file = compute_rater_for_points(
                point_filename=os.path.join(city_open_space_tweet_path, csv_file),
                raster_filename=os.path.join(ndvi_path, '{}_NDVI.tif'.format(city)),
                read_csv_file=True)
            source_file = pd.read_csv(os.path.join(city_open_space_tweet_path, csv_file), encoding='utf-8').copy()
            raster_values = list(output_file['Raster_Value'])
            source_file['raster_val'] = raster_values
            if os.path.exists(os.path.join(save_path, city)):
                source_file.to_csv(os.path.join(save_path, city, csv_file[:-4] + '_with_raster.csv'), encoding='utf-8')
            else:
                os.mkdir(os.path.join(save_path, city))
                source_file.to_csv(os.path.join(save_path, city, csv_file[:-4] + '_with_raster.csv'), encoding='utf-8')
            print('The file {} has been processed'.format(csv_file))
        print('-\n' * 20)


if __name__ == '__main__':
    saving_path = r'D:\Projects\Heat_tweets\codes\open_space_with_raster'
    main_foreign(save_path=saving_path)
