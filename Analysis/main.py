import os
from spatial_analysis import main_foreign
from count_tweets import main_count_tweets
from cities_bounds import cities_dict_foreign, open_space_saving_path
from extract_raster import main_foreign_raster

from data_paths import raster_save_path

if __name__ == '__main__':
    considered_cities_set = {'hong_kong'}
    print('Finding the tweets posted in open space...')
    main_foreign(considered_cities=considered_cities_set, cities_profile=cities_dict_foreign,
                 save_threshold=30000, open_space_save_path=open_space_saving_path)
    print('Counting the tweets in the cities and open spaces...')
    main_count_tweets(count_in_utc=True, considered_city_names=considered_cities_set)
    print('Computing the raster values...')
    main_foreign_raster(save_path=raster_save_path, considered_cities=considered_cities_set)