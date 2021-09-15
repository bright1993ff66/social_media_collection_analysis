import os
import pytz
import numpy as np

from data_paths import geocoded_save_path

# The happyplaces and Weibo path should contain all the names
# of cities as the folder name
happyplaces_path = r'/home/data_center/Social_Media/happyplacestweets'
weibo_path = r'/home/haoliang/projects/count_tweet/geocoded_weibos_heat_weibo'

# Specify the shapefile path
shapefiles_path = r'/home/haoliang/projects/count_tweet/shapefiles'
# The path below used to save the tweets posted in the open space
open_space_saving_path = r'/home/haoliang/projects/count_tweet/open_space'

# The bounding boxes of cities
# lon_min, lat_min, lon_max, lat_max
# For foreign cities
san_francisco_box = [-123.5342, 36.8929, -121.2092, 38.8644]
new_york_box = [-74.262714, 40.492848, -73.693046, 40.919761]
los_angeles_box = [-118.959390, 33.699516, -117.625837, 34.837462]
chicago_box = [-87.939723, 41.633757, -87.520393, 42.031771]
atlanta_box = [-84.559331, 33.643597, -84.282973, 33.890698]
boston_box = [-71.369441, 42.118187, -70.849632, 42.502023]
london_box = [-0.535917, 51.279854, 0.352602, 51.682671]
netherlands_box = [3.358, 50.7504, 7.2275, 53.5552]
hong_kong_box = [113.835078, 22.153388, 114.406957, 22.561968]
bangkok_box = [99.782410, 13.383219, 101.006581, 14.317204]
tokyo_box = [138.795382, 35.036245, 140.606039, 36.339124]
singapore_box = [103.573672, 1.151331, 104.106509, 1.480834]
riyadh_box = [46.236731, 24.234349, 47.368077, 25.207854]
mumbai_box = [72.768807, 18.886899, 72.994909, 19.276115]
jakarta_box = [106.685344, -6.381976, 106.977405, -6.078168]
dhaka_box = [90.316881, 23.659243, 90.518876, 23.904298]
kuala_lumpur_box = [101.2181, 2.5938, 101.9696, 3.4024]
melbourne_box = [144.362568, -38.256869, 145.788045, -37.447964]
auckland_box = [174.441513, -37.075613, 175.325474, -36.651444]
wales_box = [-5.618042, 51.320780, -2.645919, 53.470180]
taipei_box = [121.429889, 24.953611, 121.674861, 25.218833]
tricity_box = [18.354115, 54.260080, 18.948665, 54.586999]
paris_box = [2.223266, 48.815541, 2.474577, 48.907088]
vancouver_box = [-123.233099, 49.195055, -123.016806, 49.319192]
madrid_box = [-4.133461, 40.184777, -3.212349, 40.760370]
johannesburg_box = [27.7100, -26.5300, 28.2200, -25.8900]
saopaulo_box = [-46.995647, -24.025362, -46.309350, -23.338671]
# For cities in China
shanghai_box = [120.8469, 30.6852, 122.2435, 31.8881]
beijing_box = [115.3949, 39.4383, 117.5125, 41.0649]
hangzhou_box = [118.335, 29.177, 120.714, 30.566]
chengdu_box = [102.980, 30.088, 104.896, 31.443]
shenzhen_box = [113.7012, 22.4099, 114.6767, 22.9299]
tianjin_box = [116.6954, 38.5546, 118.0701, 40.2549]
changsha_box = [111.8848, 27.8500, 114.2585, 28.6683]
shenyang_box = [122.428, 41.193, 123.821, 43.049]
zhengzhou_box = [112.695, 35.004, 114.241, 34.251]

# The timezone of foreign cities and local location of corresponding tweets
san_francisco_timezone, san_francisco_loc = pytz.timezone('America/Los_Angeles'), os.path.join(happyplaces_path, 'SF')
new_york_timezone, new_york_loc = pytz.timezone('America/New_York'), os.path.join(happyplaces_path, 'NY')
los_angeles_timezone, los_angeles_loc = pytz.timezone('America/Los_Angeles'), os.path.join(happyplaces_path, 'LA')
chicago_timezone, chicago_loc = pytz.timezone('America/Chicago'), os.path.join(happyplaces_path, 'Chicago')
atlanta_timezone, atlanta_loc = pytz.timezone('America/New_York'), os.path.join(happyplaces_path, 'Atlanta-Boston')
boston_timezone, boston_loc = pytz.timezone('America/New_York'), os.path.join(happyplaces_path, 'Atlanta-Boston')
london_timezone, london_loc = pytz.timezone('Europe/London'), os.path.join(happyplaces_path, 'London')
netherlands_timezone, netherlands_loc = pytz.timezone('Europe/Amsterdam'), os.path.join(happyplaces_path, 'Netherlands')
hong_kong_timezone, hong_kong_loc = pytz.timezone('Hongkong'), os.path.join(happyplaces_path, 'HongKong')
bangkok_timezone, bangkok_loc = pytz.timezone('Asia/Bangkok'), os.path.join(happyplaces_path, 'Bangkok')
tokyo_timezone, tokyo_loc = pytz.timezone('Asia/Tokyo'), os.path.join(happyplaces_path, 'Tokyo')
singapore_timezone, singapore_loc = pytz.timezone('Singapore'), os.path.join(happyplaces_path, 'Singapore_raw')
riyadh_timezone, riyadh_loc = pytz.timezone('Asia/Riyadh'), os.path.join(happyplaces_path, 'Riyadh-Mumbai')
mumbai_timezone, mumbai_loc = pytz.timezone('Asia/Kolkata'), os.path.join(happyplaces_path, 'Riyadh-Mumbai')
jakarta_timezone, jakarta_loc = pytz.timezone('Asia/Jakarta'), os.path.join(happyplaces_path, 'Jakata-Dhaka-Kuala')
dhaka_timezone, dhaka_loc = pytz.timezone('Asia/Dhaka'), os.path.join(happyplaces_path, 'Jakata-Dhaka-Kuala')
kuala_lumpur_timezone, kuala_lumpur_loc = pytz.timezone('Asia/Kuala_Lumpur'), os.path.join(
    happyplaces_path, 'Jakata-Dhaka-Kuala')
melbourne_timezone, melbourne_loc = pytz.timezone('Australia/Melbourne'), os.path.join(
    happyplaces_path, 'Melbourne-Auckland-Wales')
auckland_timezone, auckland_loc = pytz.timezone('Pacific/Auckland'), os.path.join(
    happyplaces_path, 'Melbourne-Auckland-Wales')
wales_timezone, wales_loc = pytz.timezone('Europe/London'), os.path.join(happyplaces_path, 'Melbourne-Auckland-Wales')
taipei_timezone, taipei_loc = pytz.timezone('Asia/Taipei'), os.path.join(happyplaces_path, 'Taipei')
tricity_timezone, tricity_loc = pytz.timezone('Europe/Warsaw'), os.path.join(happyplaces_path, 'Tricity')
paris_timezone, paris_loc = pytz.timezone('Europe/Paris'), os.path.join(happyplaces_path, 'Paris-Vancouver')
vancouver_timezone, vancouver_loc = pytz.timezone('America/Vancouver'), os.path.join(
    happyplaces_path, 'Paris-Vancouver')
madrid_timezone, madrid_loc = pytz.timezone('Europe/Madrid'), os.path.join(happyplaces_path, 'Mad-John-Sao')
johannesburg_timezone, johannesburg_loc = pytz.timezone('Africa/Johannesburg'), os.path.join(
    happyplaces_path, 'Mad-John-Sao')
saopaulo_timezone, saopaulo_loc = pytz.timezone('America/Sao_Paulo'), os.path.join(happyplaces_path, 'Mad-John-Sao')
# The timezone of foreign cities and local location of corresponding tweets
beijing_timezone, beijing_loc = pytz.timezone('Asia/Shanghai'), weibo_path
tianjin_timezone, tianjin_loc = pytz.timezone('Asia/Shanghai'), weibo_path
changsha_timezone, changsha_loc = pytz.timezone('Asia/Shanghai'), weibo_path
chengdu_timezone, chengdu_loc = pytz.timezone('Asia/Shanghai'), weibo_path
hangzhou_timezone, hangzhou_loc = pytz.timezone('Asia/Shanghai'), weibo_path
shanghai_timezone, shanghai_loc = pytz.timezone('Asia/Shanghai'), weibo_path
shenyang_timezone, shenyang_loc = pytz.timezone('Asia/Shanghai'), weibo_path
shenzhen_timezone, shenzhen_loc = pytz.timezone('Asia/Shanghai'), weibo_path
zhengzhou_timezone, zhengzhou_loc = pytz.timezone('Asia/Shanghai'), weibo_path

# Load the bot ids in each city
atlanta_bot_ids = os.path.join(geocoded_save_path, 'atlanta',
                               'atlanta_bot_ids.npy')
boston_bot_ids = os.path.join(geocoded_save_path, 'boston',
                              'boston_bot_ids.npy')
bangkok_bot_ids = os.path.join(geocoded_save_path, 'bangkok',
                               'bangkok_bot_ids.npy')
chicago_bot_ids = os.path.join(geocoded_save_path, 'chicago',
                               'chicago_bot_ids.npy')
hong_kong_bot_ids = os.path.join(geocoded_save_path, 'hong_kong',
                                 'hong_kong_bot_ids.npy')
jakarta_bot_ids = os.path.join(geocoded_save_path, 'jakarta',
                               'jakarta_bot_ids.npy')
dhaka_bot_ids = os.path.join(geocoded_save_path, 'dhaka',
                             'dhaka_bot_ids.npy')
kuala_lumpur_bot_ids = os.path.join(geocoded_save_path,
                                    'kuala_lumper',
                                    'kuala_lumper_bot_ids.npy')
los_angeles_bot_ids = os.path.join(geocoded_save_path,
                                   'los_angeles',
                                   'los_angeles_bot_ids.npy')
london_bot_ids = os.path.join(geocoded_save_path,
                              'london',
                              'london_bot_ids.npy')
madrid_bot_ids = os.path.join(geocoded_save_path,
                              'madrid',
                              'madrid_bot_ids.npy')
johannesburg_bot_ids = os.path.join(geocoded_save_path,
                                    'johannesburg',
                                    'johannesburg_bot_ids.npy')
saopaulo_bot_ids = os.path.join(geocoded_save_path,
                                'sao_paulo',
                                'sao_paulo_bot_ids.npy')
melbourne_bot_ids = os.path.join(geocoded_save_path,
                                 'melbourne',
                                 'melbourne_bot_ids.npy')
auckland_bot_ids = os.path.join(geocoded_save_path,
                                'auckland',
                                'auckland_bot_ids.npy')
wales_bot_ids = os.path.join(geocoded_save_path,
                             'wales',
                             'wales_bot_ids.npy')
netherlands_bot_ids = os.path.join(geocoded_save_path,
                                   'netherlands',
                                   'netherlands_bot_ids.npy')
new_york_bot_ids = os.path.join(geocoded_save_path,
                                'new_york',
                                'new_york_bot_ids.npy')
paris_bot_ids = os.path.join(geocoded_save_path,
                             'paris',
                             'paris_bot_ids.npy')
vancouver_bot_ids = os.path.join(geocoded_save_path,
                                 'vancouver',
                                 'vancouver_bot_ids.npy')
riyadh_bot_ids = os.path.join(geocoded_save_path,
                              'riyadh',
                              'riyadh_bot_ids.npy')
mumbai_bot_ids = os.path.join(geocoded_save_path,
                              'mumbai',
                              'mumbai_bot_ids.npy')
san_francisco_bot_ids = os.path.join(geocoded_save_path,
                                     'san_francisco',
                                     'san_francisco_bot_ids.npy')
singapore_bot_ids = os.path.join(geocoded_save_path,
                                 'singapore',
                                 'singapore_bot_ids.npy')
taipei_bot_ids = os.path.join(geocoded_save_path,
                              'taipei',
                              'taipei_bot_ids.npy')
tokyo_bot_ids = os.path.join(geocoded_save_path,
                             'tokyo',
                             'tokyo_bot_ids.npy')
tricity_bot_ids = os.path.join(geocoded_save_path,
                               'tricity',
                               'tricity_bot_ids.npy')
# To do: get the bot ids for each city
beijing_bot_ids = os.path.join(os.getcwd(), 'weibo_bots_final.npy')
tianjin_bot_ids = os.path.join(os.getcwd(), 'weibo_bots_final.npy')
changsha_bot_ids = os.path.join(os.getcwd(), 'weibo_bots_final.npy')
chengdu_bot_ids = os.path.join(os.getcwd(), 'weibo_bots_final.npy')
hangzhou_bot_ids = os.path.join(os.getcwd(), 'weibo_bots_final.npy')
shanghai_bot_ids = os.path.join(os.getcwd(), 'weibo_bots_final.npy')
shenyang_bot_ids = os.path.join(os.getcwd(), 'weibo_bots_final.npy')
shenzhen_bot_ids = os.path.join(os.getcwd(), 'weibo_bots_final.npy')
zhengzhou_bot_ids = os.path.join(os.getcwd(), 'weibo_bots_final.npy')

# the location to the open space shapefiles for foreign cities
atlanta_area = os.path.join(shapefiles_path, 'atlanta_greenspace.shp')
boston_area = os.path.join(shapefiles_path, 'boston_greenspace.shp')
bangkok_area = os.path.join(shapefiles_path, 'bankok_greenspace.shp')
chicago_area = os.path.join(shapefiles_path, 'chicago_greenspace.shp')
hong_kong_area = os.path.join(shapefiles_path, 'hongkong_greenspace.shp')
jakarta_area = os.path.join(shapefiles_path, 'jakarta_greenspace.shp')
dhaka_area = os.path.join(shapefiles_path, 'dhaka_greenspace.shp')
kuala_lumpur_area = os.path.join(shapefiles_path
                                 ,'kualalumpur_greenspace.shp')
greater_kuala_lumpur_area = os.path.join(
    shapefiles_path,'greaterkualalumpur_greenspace.shp')
los_angeles_area = os.path.join(shapefiles_path,
                                'losangeles_greenspace.shp')
london_area = os.path.join(shapefiles_path, 'london_greenspace.shp')
madrid_area = os.path.join(shapefiles_path, 'madrid_greenspace.shp')
johannesburg_area = os.path.join(johannesburg_loc, 'shapefiles',
                                 'johannesburg_greenspace.shp')
melbourne_area = os.path.join(shapefiles_path, 'melbourne_greenspace.shp')
auckland_area = os.path.join(shapefiles_path, 'auckland_greenspace.shp')
wales_area = os.path.join(shapefiles_path, 'wales_greenspace.shp')
netherlands_area = os.path.join(shapefiles_path, 'netherlands_greenspace.shp')
netherland_open_spaces = [os.path.join(shapefiles_path, file) for file in os.listdir(shapefiles_path) if
                          ('netherland_green' in file) and (file.endswith('.shp'))]
new_york_area = os.path.join(shapefiles_path, 'newyork_greenspace.shp')
paris_area = os.path.join(shapefiles_path, 'paris_greenspace.shp')
vancouver_area = os.path.join(shapefiles_path, 'vancouver_greenspace.shp')
riyadh_area = os.path.join(shapefiles_path, 'riyadh_greenspace.shp')
mumbai_area = os.path.join(shapefiles_path, 'mumbai_greenspace.shp')
saopaulo_area = os.path.join(shapefiles_path, 'saopaulo_greenspace.shp')
bay_area_green = os.path.join(shapefiles_path, 'bay_greenspace.shp')
san_francisco_area_green = os.path.join(shapefiles_path,
                                        'sanfrancisco_greenspace.shp')
singapore_area = os.path.join(shapefiles_path,'singapore_greenspace.shp')
taipei_area = os.path.join(shapefiles_path, 'taipei_greenspace.shp')
tokyo_area = os.path.join(shapefiles_path, 'tokyo_greenspace.shp')
tricity_area = os.path.join(shapefiles_path, 'tricity_greenspace.shp')

# the location to the city shapefile for foreign cities
atlanta_city = os.path.join(shapefiles_path, 'atlanta_border.shp')
boston_city = os.path.join(shapefiles_path, 'boston_border.shp')
bangkok_city = os.path.join(shapefiles_path, 'bankok_border.shp')
chicago_city = os.path.join(shapefiles_path, 'chicago_border.shp')
hong_kong_city = os.path.join(shapefiles_path, 'hongkong_border.shp')
jakarta_city = os.path.join(shapefiles_path, 'jakarta_border.shp')
dhaka_city = os.path.join(shapefiles_path, 'dhaka_border.shp')
kuala_lumpur_city = os.path.join(shapefiles_path,
                                 'kualalumpur_border.shp')
greater_kuala_lumpur_city = os.path.join(shapefiles_path,
                                         'greaterkualalumpur_border.shp')
los_angeles_city = os.path.join(shapefiles_path,
                                'losangeles_border.shp')
london_city = os.path.join(shapefiles_path, 'london_border.shp')
madrid_city = os.path.join(shapefiles_path, 'madrid_border.shp')
johannesburg_city = os.path.join(shapefiles_path,
                                 'johannesburg_border.shp')
saopaulo_city = os.path.join(shapefiles_path,'saopaulo_border.shp')
melbourne_city = os.path.join(shapefiles_path,'melbourne_border.shp')
auckland_city = os.path.join(shapefiles_path, 'auckland_border.shp')
wales_city = os.path.join(shapefiles_path, 'wales_border.shp')
netherlands_city = os.path.join(shapefiles_path, 'netherlands_border.shp')
new_york_city = os.path.join(shapefiles_path,'newyork_border.shp')
paris_city = os.path.join(shapefiles_path, 'paris_border.shp')
vancouver_city = os.path.join(shapefiles_path, 'vancouver_border.shp')
riyadh_city = os.path.join(shapefiles_path, 'riyadh_border.shp')
mumbai_city = os.path.join(shapefiles_path, 'mumbai_border.shp')
san_francisco_city = os.path.join(shapefiles_path,
                                  'sanfrancisco_border.shp')
bay_area_city = os.path.join(shapefiles_path,
                             'bay_border.shp')
singapore_city = os.path.join(shapefiles_path,'singapore_border.shp')
taipei_city = os.path.join(shapefiles_path,'taipei_border.shp')
tokyo_city = os.path.join(shapefiles_path, 'tokyo_border.shp')
tricity_city = os.path.join(shapefiles_path, 'tricity_border.shp')

# the location of the open space shapefiles for Chinese cities
# TODO: Add the cities open space shapefile to server
beijing_area = os.path.join(shapefiles_path, 'beijing_greenspace.shp')
tianjin_area = os.path.join(shapefiles_path, 'tianjin_greenspace.shp')
changsha_area = os.path.join(shapefiles_path, 'changsha_greenspace.shp')
chengdu_area = os.path.join(shapefiles_path, 'chengdu_greenspace.shp')
hangzhou_area = os.path.join(shapefiles_path, 'hangzhou_greenspace.shp')
shanghai_area = os.path.join(shapefiles_path, 'shanghai_greenspace.shp')
shenyang_area = os.path.join(shapefiles_path, 'shenyang_greenspace.shp')
shenzhen_area = os.path.join(shapefiles_path, 'shenzhen_greenspace.shp')
zhengzhou_area = os.path.join(shapefiles_path, 'zhengzhou_greenspace.shp')

# TODO: Add the mainland cities' city boundary
beijing_city = None
tianjin_city = None
changsha_city = None
chengdu_city = None
hangzhou_city = None
shanghai_city = os.path.join(shapefiles_path, 'shanghai_border.shp')
shenyang_city = None
shenzhen_city = None
zhengzhou_city = None

# final cities dicts: Use this dictionary in a loop
cities_dict_foreign = {
    'san_francisco': [san_francisco_box, san_francisco_timezone, san_francisco_loc, san_francisco_area_green,
                      san_francisco_bot_ids, san_francisco_city],
    'bay_area':[san_francisco_box, san_francisco_timezone, san_francisco_loc, bay_area_green,
                      san_francisco_bot_ids, bay_area_city],
    'new_york': [new_york_box, new_york_timezone, new_york_loc, new_york_area, new_york_bot_ids, new_york_city],
    'los_angeles': [los_angeles_box, los_angeles_timezone, los_angeles_loc, los_angeles_area, los_angeles_bot_ids,
                    los_angeles_city],
    'chicago': [chicago_box, chicago_timezone, chicago_loc, chicago_area, chicago_bot_ids, chicago_city],
    'atlanta': [atlanta_box, atlanta_timezone, atlanta_loc, atlanta_area, atlanta_bot_ids, atlanta_city],
    'boston': [boston_box, boston_timezone, boston_loc, boston_area, boston_bot_ids, boston_city],
    'london': [london_box, london_timezone, london_loc, london_area, london_bot_ids, london_city],
    'netherlands': [netherlands_box, netherlands_timezone, netherlands_loc, netherlands_area, netherlands_bot_ids, netherlands_city],
    'hong_kong': [hong_kong_box, hong_kong_timezone, hong_kong_loc, hong_kong_area, hong_kong_bot_ids, hong_kong_city],
    'bangkok': [bangkok_box, bangkok_timezone, bangkok_loc, bangkok_area, bangkok_bot_ids, bangkok_city],
    'tokyo': [tokyo_box, tokyo_timezone, tokyo_loc, tokyo_area, tokyo_bot_ids, tokyo_city],
    'singapore': [singapore_box, singapore_timezone, singapore_loc, singapore_area, singapore_bot_ids, singapore_city],
    'riyadh': [riyadh_box, riyadh_timezone, riyadh_loc, riyadh_area, riyadh_bot_ids, riyadh_city],
    'mumbai': [mumbai_box, mumbai_timezone, mumbai_loc, mumbai_area, mumbai_bot_ids, mumbai_city],
    'jakarta': [jakarta_box, jakarta_timezone, jakarta_loc, jakarta_area, jakarta_bot_ids, jakarta_city],
    'dhaka': [dhaka_box, dhaka_timezone, dhaka_loc, dhaka_area, dhaka_bot_ids, dhaka_city],
    'kuala_lumper': [kuala_lumpur_box, kuala_lumpur_timezone, kuala_lumpur_loc, kuala_lumpur_area,
                     kuala_lumpur_bot_ids, kuala_lumpur_city],
    'greater_kuala_lumper': [kuala_lumpur_box, kuala_lumpur_timezone, kuala_lumpur_loc, greater_kuala_lumpur_area,
                         kuala_lumpur_bot_ids, greater_kuala_lumpur_city],
    'melbourne': [melbourne_box, melbourne_timezone, melbourne_loc, melbourne_area, melbourne_bot_ids, melbourne_city],
    'auckland': [auckland_box, auckland_timezone, auckland_loc, auckland_area, auckland_bot_ids, auckland_city],
    'wales': [wales_box, wales_timezone, wales_loc, wales_area, wales_bot_ids, wales_city],
    'taipei': [taipei_box, taipei_timezone, taipei_loc, taipei_area, taipei_bot_ids, taipei_city],
    'tricity': [tricity_box, tricity_timezone, tricity_loc, tricity_area, tricity_bot_ids, tricity_city],
    'paris': [paris_box, paris_timezone, paris_loc, paris_area, paris_bot_ids, paris_city],
    'vancouver': [vancouver_box, vancouver_timezone, vancouver_loc, vancouver_area, vancouver_bot_ids, vancouver_city],
    'madrid': [madrid_box, madrid_timezone, madrid_loc, madrid_area, madrid_bot_ids, madrid_city],
    'johannesburg': [johannesburg_box, johannesburg_timezone, johannesburg_loc, johannesburg_area,
                     johannesburg_bot_ids, johannesburg_city],
    'sao_paulo': [saopaulo_box, saopaulo_timezone, saopaulo_loc, saopaulo_area, saopaulo_bot_ids, saopaulo_city]}


cities_dict_netherland = {'netherland_{}'.format(file[-5]):
                          [netherlands_box, netherlands_timezone,
                            netherlands_loc, file,
                            netherlands_bot_ids, netherlands_city] for file in netherland_open_spaces}


cities_dict_china = {
    'beijing': [beijing_box, beijing_timezone, beijing_loc, beijing_area,
                beijing_bot_ids, beijing_city],
    'changsha': [changsha_box, changsha_timezone, changsha_loc, changsha_area,
                 changsha_bot_ids, changsha_city],
    'chengdu': [chengdu_box, chengdu_timezone, chengdu_loc, chengdu_area,
                chengdu_bot_ids, chengdu_city],
    'hangzhou': [hangzhou_box, hangzhou_timezone, hangzhou_loc, hangzhou_area,
                 hangzhou_bot_ids, hangzhou_city],
    'shanghai': [shanghai_box, shanghai_timezone, shanghai_loc, shanghai_area,
                 shanghai_bot_ids, shanghai_city],
    'shenyang': [shenyang_box, shenyang_timezone, shenyang_loc, shenyang_area,
                 shenyang_bot_ids, shenyang_city],
    'shenzhen': [shenzhen_box, shenzhen_timezone, shenzhen_loc, shenzhen_area,
                 shenzhen_bot_ids, shenzhen_city],
    'tianjin': [tianjin_box, tianjin_timezone, tianjin_loc, tianjin_area,
                tianjin_bot_ids, tianjin_city],
    'zhengzhou': [zhengzhou_box, zhengzhou_timezone, zhengzhou_loc,
                  zhengzhou_area, zhengzhou_bot_ids, zhengzhou_city]}

if __name__ == '__main__':
    print(netherland_open_spaces)
    print(cities_dict_netherland.keys())
    print(cities_dict_netherland['netherland_5'])
    print(os.listdir(weibo_path))
    print(cities_dict_china.keys())
