# Main functions to count the tweets
from spatial_analysis import main_china
from count_weibos import main_count_weibos
from cities_bounds import cities_dict_china, open_space_saving_path
from extract_raster import main_china_raster

from data_paths import raster_save_path

if __name__ == '__main__':
    # List some cities
    considered_cities_set = {'shanghai'}

    print('Finding the tweets posted in open space...')
    main_china(considered_cities=considered_cities_set,
               cities_profile=cities_dict_china,
               save_threshold=30000,
               open_space_save_path=open_space_saving_path)
    print('Counting the tweets in the cities and open spaces...')
    main_count_weibos(count_in_utc=True,
                      count_cities_mainland=considered_cities_set)
    print('Computing the raster values...')
    main_china_raster(save_path=raster_save_path,
                      considered_cities=considered_cities_set)
