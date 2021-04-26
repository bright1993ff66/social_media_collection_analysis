# Social Media Data Collection and Analysis

## 1. Introduction

This repository saves data and codes for the social media data (including Twitter and Weibo) collection and analysis.

## 2. Data Collection

All the codes for social media data collection can be found in [Data_Collection](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/tree/master/Data_Collection) folder.

For Twitter data, the secret key and access token are required. Please visit [Twitter Developer Page](https://developer.twitter.com/en) for more information about registering the Twitter developer account and getting the access key and token.

For the Weibo data, this GitHub repository - [WeiboSpider](https://github.com/dataabc/weiboSpider) offers codes to collect the Weibo data based on user ids. The Weibo crawler requires to register the cookie. The detailed steps of generating the cookie is given [here](https://github.com/dataabc/weiboSpider/blob/master/docs/cookie.md).

## 3. Social Media Data Analysis

The [Analysis](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/tree/master/Analysis) folder saves the codes for Twitter & Weibo data analysis.

- The [cities_bounds.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/cities_bounds.py) saves the profiles of each city, including the bounding box, timezone, path to the tweet data, open space shapefile.
- The [count_tweets.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/count_tweets.py) and [count_weibos.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/count_weibos.py) have the codes for counting the tweets posted in the cities and their open space.
- The [spatial_analysis.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/spatial_analysis.py) stores the codes of finding the tweets or Weibos posted in a city's open space, based on the [geopandas spatial join function](https://geopandas.org/gallery/spatial_joins.html).
- The [visualizations.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/visualizations.py) saves the functions to plotting the number of tweets or Weibos posted in the city and in the city's open space.
- The [utils.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/utils.py) and [data_paths.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/data_paths.py) saves some help functions and paths for this project..

## 4. Other Data Sources

The following links give the source of other data sources for urban data analysis:

- [ChinaAdminDivisionSHP](https://github.com/GaryBikini/ChinaAdminDivisonSHP): Chinese administrative division vector diagram, Shapefile format, four levels: country, province, city, district/county
- [bbike openstreetmap extractor](https://extract.bbbike.org/): The OpenStreetMap data extractor
- [Hong Kong Monthly Traffic and Transport Digest](https://www.td.gov.hk/en/transport_in_hong_kong/transport_figures/monthly_traffic_and_transport_digest/index.html): The monthly key statistics of HK transportation data

## 5. Requirements

The following packages should be considered before managing this project:

- Python 3.7 or later
- R 3.4.1 or later
- Spatial data analysis: [geopandas](https://geopandas.org/)
- Data frame and computation: [numpy](https://numpy.org/) and [pandas](https://pandas.pydata.org/)
- Visualizations: [matplotlib](https://matplotlib.org/stable/index.html)



