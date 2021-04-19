# Social Media Data Collection and Analysis

## 1. Introduction

This repository saves data and codes for the social media data (including Twitter and Weibo) collection and analysis.

## 2. Data Collection

All the codes for Twitter data collection can be found in [Data_Collection](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/tree/master/Data_Collection) folder.

For Twitter data, the secret key and access token are required. Please visit [Twitter Developer Page](https://developer.twitter.com/en) for more information about registering the developer account and getting the key and token information.

## 3. Social Media Data Analysis

The [Analysis](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/tree/master/Analysis) folder saves the codes for Twitter & Weibo data analysis.

- The [cities_bounds.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/cities_bounds.py) saves the profiles of each city, including the bounding box, timezone, path to the tweet data, open space shapefile.
- The [count_tweets.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/count_tweets.py) and [count_weibos.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/count_weibos.py) have the codes for counting the tweets posted in open space.
- The [spatial_analysis.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/spatial_analysis.py) stores the codes of finding the tweets or Weibos posted in a city's open space, based on the [geopandas spatial join function](https://geopandas.org/gallery/spatial_joins.html).
- The [visualizations.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/visualizations.py) saves the functions to plotting the number of tweets or Weibos posted in the city and in the city's open space.
- The [utils.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/utils.py) and [data_paths.py](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/Analysis/data_paths.py) saves some help functions and paths for this project.

## 4. Requirements

The following packages should be considered before managing this project:

- Python 3.7 or later
- R 3.4.1 or later
- Spatial data analysis: [geopandas](https://geopandas.org/)
- Data frame and computation: [numpy](https://numpy.org/) and [pandas](https://pandas.pydata.org/)
- Visualizations: [matplotlib](https://matplotlib.org/stable/index.html)



