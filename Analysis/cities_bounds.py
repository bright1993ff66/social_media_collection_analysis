import os
import pytz

# The project path
heat_tweet_path = r'XXX'
# The happyplaces_path should contain all the names of cities as the folder name
happyplaces_path = r'XXX'
# The path below used to save the tweets posted in the open space
open_space_saving_path = r'XXX'

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
johannesburg_box = [27.935249, -26.241503, 28.143009, -26.100564]
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
netherland_timezone, netherland_loc = pytz.timezone('Europe/Amsterdam'), os.path.join(happyplaces_path, 'Netherlands')
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
beijing_timezone, beijing_loc = pytz.timezone('Asia/Shanghai'), os.path.join(happyplaces_path, 'Beijing')
tianjin_timezone, tianjin_loc = pytz.timezone('Asia/Shanghai'), os.path.join(happyplaces_path, 'Tianjin')
changsha_timezone, changsha_loc = pytz.timezone('Asia/Shanghai'), os.path.join(happyplaces_path, 'Changsha')
chengdu_timezone, chengdu_loc = pytz.timezone('Asia/Shanghai'), os.path.join(happyplaces_path, 'Chengdu')
hangzhou_timezone, hangzhou_loc = pytz.timezone('Asia/Shanghai'), os.path.join(happyplaces_path, 'Hangzhou')
shanghai_timezone, shanghai_loc = pytz.timezone('Asia/Shanghai'), os.path.join(happyplaces_path, 'Shanghai')
shenyang_timezone, shenyang_loc = pytz.timezone('Asia/Shanghai'), os.path.join(happyplaces_path, 'Shenyang')
shenzhen_timezone, shenzhen_loc = pytz.timezone('Asia/Shanghai'), os.path.join(happyplaces_path, 'Shenzhen')
zhengzhou_timezone, zhengzhou_loc = pytz.timezone('Asia/Shanghai'), os.path.join(happyplaces_path, 'Zhengzhou')

# Load the bot ids in each city
atlanta_bot_ids = np.load(os.path.join(atlanta_loc, 'atlanta_bot_ids.npy'), allow_pickle=True).item()
boston_bot_ids = None
bangkok_bot_ids = None
chicago_bot_ids = None
hong_kong_bot_ids = None
jakarta_bot_ids = None
dhaka_bot_ids = None
kuala_lumpur_bot_ids = None
los_angeles_bot_ids = None
london_bot_ids = None
madrid_bot_ids = None
johannesburg_bot_ids = None
saopaulo_bot_ids = None
melbourne_bot_ids = None
auckland_bot_ids = None
wales_bot_ids = None
netherland_bot_ids = None
new_york_bot_ids = np.load(os.path.join(new_york_loc, 'bot_ids.npy'), allow_pickle=True).item()
paris_bot_ids = None
vancouver_bot_ids = None
riyadh_bot_ids = None
mumbai_bot_ids = None
san_francisco_bot_ids = None
singapore_bot_ids = None
taipei_bot_ids = None
tokyo_bot_ids = None
tricity_bot_ids = None


# the location to the open space shapefiles for foreign cities
atlanta_area = os.path.join(atlanta_loc, 'shapefiles', 'Atlanta_GreenSpace.shp')
boston_area = os.path.join(boston_loc, 'shapefiles', 'Boston_OpenspaceUpdate.shp')
bangkok_area = os.path.join(bangkok_loc, 'shapefiles', 'Bankok_GreenSpace.shp')
chicago_area = os.path.join(chicago_loc, 'shapefiles', 'Chicago_Greenspace.shp')
hong_kong_area = os.path.join(hong_kong_loc, 'shapefiles', 'HK_Openspace.shp')
jakarta_area = os.path.join(jakarta_loc, 'shapefiles', 'Jakarta_Openspace.shp')
dhaka_area = os.path.join(dhaka_loc, 'shapefiles', 'Dhaka_Opensapce.shp')
kuala_lumpur_area = os.path.join(kuala_lumpur_loc, 'shapefiles', 'KualaLumpur_Openspace.shp')
los_angeles_area = os.path.join(los_angeles_loc, 'shapefiles', 'LA_Openspace.shp')
london_area = os.path.join(london_loc, 'shapefiles', 'London_Openspace_F.shp')
madrid_area = os.path.join(madrid_loc, 'shapefiles', 'Madrid_Openspace.shp')
johannesburg_area = os.path.join(johannesburg_loc, 'shapefiles', 'Johannesburg_Openspace.shp')
saopaulo_area = os.path.join(saopaulo_loc, 'shapefiles', 'SP_Openspace.shp')
melbourne_area = os.path.join(melbourne_loc, 'shapefiles', 'Melbourne_Openspace.shp')
auckland_area = os.path.join(auckland_loc, 'shapefiles', 'Auckland_Greenspace.shp')
wales_area = os.path.join(wales_loc, 'shapefiles', 'Wales_OpenSpace.shp')
netherland_area = os.path.join(netherland_loc, 'shapefiles', 'netherlands_greenspace.shp')
new_york_area = os.path.join(new_york_loc, 'shapefiles', 'Greenspace.shp')
paris_area = os.path.join(paris_loc, 'shapefiles', 'Paris_Openspace.shp')
vancouver_area = os.path.join(vancouver_loc, 'shapefiles', 'Vancouver_Openspace.shp')
riyadh_area = os.path.join(riyadh_loc, 'shapefiles', 'Riyadh_Openspace.shp')
mumbai_area = os.path.join(mumbai_loc, 'shapefiles', 'Mumbai_OpenSpaceF.shp')
san_francisco_area = os.path.join(san_francisco_loc, 'shapefiles', 'Bay_Openspace.shp')
singapore_area = os.path.join(singapore_loc, 'shapefiles', 'Singapore4326.shp')
taipei_area = os.path.join(taipei_loc, 'shapefiles', 'Taipei_OpenSpace_F.shp')
tokyo_area = os.path.join(tokyo_loc, 'shapefiles', 'Tokyo_Openspace.shp')
tricity_area = os.path.join(tricity_loc, 'shapefiles', 'Tricity_OpenSpace.shp')

# the location of the open space shapefiles for Chinese cities
# OneDrive location: Heat and Tweet/Tweet and Heat Sharing/data/GS_By_City_NoBuffer_China
beijing_area = os.path.join(beijing_loc, 'shapefiles', 'beijing_greenspace.shp')
tianjin_area = os.path.join(tianjin_loc, 'shapefiles', 'tianjin_greenspace.shp')
changsha_area = os.path.join(changsha_loc, 'shapefiles', 'changsha_greenspace.shp')
chengdu_area = os.path.join(chengdu_loc, 'shapefiles', 'chengdu_greenspace.shp')
hangzhou_area = os.path.join(hangzhou_loc, 'shapefiles', 'hangzhou_greenspace.shp')
shanghai_area = os.path.join(shanghai_loc, 'shapefiles', 'shanghai_greenspace.shp')
shenyang_area = os.path.join(shenyang_loc, 'shapefiles', 'shenyang_greenspace.shp')
shenzhen_area = os.path.join(shenzhen_loc, 'shapefiles', 'shenzhen_greenspace.shp')
zhengzhou_area = os.path.join(zhengzhou_loc, 'shapefiles', 'zhengzhou_greenspace.shp')

# final cities dicts: Use this dictionary in a loop
# [bounding box info, timezone info, location of tweets, loc of the data of this city, path to open space shapefile]
# To be updated: add the bot ids
cities_dict_foreign = {
    'san_francisco': [san_francisco_box, san_francisco_timezone, san_francisco_loc, san_francisco_area,
                      san_francisco_bot_ids],
    'new_york': [new_york_box, new_york_timezone, new_york_loc, new_york_area, new_york_bot_ids],
    'los_angeles': [los_angeles_box, los_angeles_timezone, los_angeles_loc, los_angeles_area, los_angeles_bot_ids],
    'chicago': [chicago_box, chicago_timezone, chicago_loc, chicago_area, chicago_bot_ids],
    'atlanta': [atlanta_box, atlanta_timezone, atlanta_loc, atlanta_area, atlanta_bot_ids],
    'boston': [boston_box, boston_timezone, boston_loc, boston_area, boston_bot_ids],
    'london': [london_box, london_timezone, london_loc, london_area, london_bot_ids],
    'netherlands': [netherland_box, netherland_timezone, netherland_loc, netherland_area, netherland_bot_ids],
    'hong_kong': [hong_kong_box, hong_kong_timezone, hong_kong_loc, hong_kong_area, hong_kong_bot_ids],
    'bangkok': [bangkok_box, bangkok_timezone, bangkok_loc, bangkok_area, bangkok_bot_ids],
    'tokyo': [tokyo_box, tokyo_timezone, tokyo_loc, tokyo_area, tokyo_bot_ids],
    'singapore': [singapore_box, singapore_timezone, singapore_loc, singapore_area, singapore_bot_ids],
    'riyadh': [riyadh_box, riyadh_timezone, riyadh_loc, riyadh_area, riyadh_bot_ids],
    'mumbai': [mumbai_box, mumbai_timezone, mumbai_loc, mumbai_area, mumbai_bot_ids],
    'jakarta': [jakarta_box, jakarta_timezone, jakarta_loc, jakarta_area, jakarta_bot_ids],
    'dhaka': [dhaka_box, dhaka_timezone, dhaka_loc, dhaka_area, dhaka_bot_ids],
    'kuala_lumper': [kuala_lumpur_box, kuala_lumpur_timezone, kuala_lumpur_loc, kuala_lumpur_area,
                     kuala_lumpur_bot_ids],
    'melbourne': [melbourne_box, melbourne_timezone, melbourne_loc, melbourne_area, melbourne_bot_ids],
    'auckland': [auckland_box, auckland_timezone, auckland_loc, auckland_area, auckland_bot_ids],
    'wales': [wales_box, wales_timezone, wales_loc, wales_area, wales_bot_ids],
    'taipei': [taipei_box, taipei_timezone, taipei_loc, taipei_area, taipei_bot_ids],
    'tricity': [tricity_box, tricity_timezone, tricity_loc, tricity_area, tricity_bot_ids],
    'paris': [paris_box, paris_timezone, paris_loc, paris_area, paris_bot_ids],
    'vancouver': [vancouver_box, vancouver_timezone, vancouver_loc, vancouver_area, vancouver_bot_ids],
    'madrid': [madrid_box, madrid_timezone, madrid_loc, madrid_area, madrid_bot_ids],
    'johannesburg': [johannesburg_box, johannesburg_timezone, johannesburg_loc, johannesburg_area,
                     johannesburg_bot_ids],
    'sao_paulo': [saopaulo_box, saopaulo_timezone, saopaulo_loc, saopaulo_area, saopaulo_bot_ids]}

cities_dict_china = {
    'beijing': [beijing_box, beijing_timezone, beijing_loc, beijing_area],
    'changsha': [changsha_box, changsha_timezone, changsha_loc, changsha_area],
    'chengdu': [chengdu_box, chengdu_timezone, chengdu_loc, chengdu_area],
    'hangzhou': [hangzhou_box, hangzhou_timezone, hangzhou_loc, hangzhou_area],
    'shanghai': [shanghai_box, shanghai_timezone, shanghai_loc, shanghai_area],
    'shenyang': [shenyang_box, shenyang_timezone, shenyang_loc, shenyang_area],
    'shenzhen': [shenzhen_box, shenzhen_timezone, shenzhen_loc, shenzhen_area],
    'tianjin': [tianjin_box, tianjin_timezone, tianjin_loc, tianjin_area],
    'zhengzhou': [zhengzhou_box, zhengzhou_timezone, zhengzhou_loc, zhengzhou_area]}
