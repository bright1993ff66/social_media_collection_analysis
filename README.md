# Social Media Data Collection and Analysis

## 1. Introduction

This repository saves data and codes for the social media data (including Twitter and Weibo) collection and analysis.

## 2. Data Collection and Preprocessing

### 2.1 Twitter and Weibo Data Collection

All the codes for social media data collection can be found in [Data_Collection](https://github.com/bright1993ff66/social_media_collection_analysis/tree/master/Data_Collection) folder.

For Twitter data, we use the Twitter Streaming API to collect the tweets. the secret key and access token are required. Please visit [Twitter Developer Page](https://developer.twitter.com/en) for more information about registering the Twitter developer account and getting the access key and token.

For the Weibo data, this GitHub repository - [WeiboSpider](https://github.com/dataabc/weiboSpider) offers codes to collect the Weibo data based on user ids. The Weibo crawler requires to register the cookie. The detailed steps of generating the cookie is given [here](https://github.com/dataabc/weiboSpider/blob/master/docs/cookie.md).

### 2.2 Data Overview

We started collecting the Twitter data from May 2018. Please visit the [Tweet_Summary_Table.xlsx](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Tweet_Summary_Table.xlsx) for more specific information about the number of all tweets & geocoded tweets posted in the cities.

For the Weibo data, we only collected Weibos between August 2011 and September 2014. The number of geocoded Weibos posted in the bounding boxes of major cities are given in [Geocoded_Weibo_Major_Cities_Summaries.csv](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Geocoded_Weibo_Major_Cities_Summaries.csv).

### 2.3 Data Preprocessing

The general data preprocessing steps involve the following steps:

<u>For the user information</u>:

- Remove the bot accounts. We use the following rules to delete the bot accounts ([Coşkun & Özturan, 2018](https://www.mdpi.com/2078-2489/9/5/102/htm)):
  - whose number of tweets is 2 standard deviations away from the mean of the users from that city
  - whose most identified geographic footprint (latitude & longitude pair) accounts for over 60% of all the footprints

<u>For the spatial and semantic information</u>:

- Remove the messages not containing the latitude and longitude information. 
- Only consider the messages posted within, for instance, the city boundary
- Only extract the messages posted in some specific languages (e.g., English and Chinese)

<u>For the temporal information</u>:

- Convert the time string to the structured python [datetime](https://docs.python.org/3/library/datetime.html) object

The specific steps of data preprocessing are given in [Tweet_filtering.ipynb](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/Tweet_filtering.ipynb).

### 2.4 Raw Data Storage

All the collected Twitter data is stored in the server. Please login to the server and visit the following directory to get the tweets posted in each city:

- /home/data_center/Social_Media/happyplacestweets

The Weibo data is currently stored on a hard drive. Please contact the owner of this repository to retrieve the Weibo data.

## 3. Social Media Data Analysis

The [Analysis](https://github.com/bright1993ff66/social_media_collection_analysis/tree/master/Analysis) folder saves the codes for Twitter & Weibo data analysis.

- The [Tweet_Data_Description.ipynb](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/Tweet_Data_Description.ipynb) saves a description of collected tweet data and some basic time, text, and spatial analysis.
- The [Tweet_filtering.ipynb](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/Tweet_filtering.ipynb) saves the general tweet filtering process, including considering tweets posted in preferred languages, keeping the geocoded tweets, and removing the bot accounts.
- The [cities_bounds.py](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/cities_bounds.py) saves the profiles of each city, including the bounding box, timezone, path to the tweet data, open space shapefile.
- The [count_tweets.py](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/count_tweets.py) and [count_weibos.py](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/count_weibos.py) have the codes for counting the tweets posted in the cities and their open space.
- The [spatial_analysis.py](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/spatial_analysis.py) stores the codes of finding the tweets or Weibos posted in a city's open space, based on the [geopandas spatial join function](https://geopandas.org/gallery/spatial_joins.html).
- The [find_bot_accounts.py](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/find_bot_accounts.py) presents some functions to find the bot accounts. Here are some papers for reference:
  - [#europehappinessmap: A Framework for Multi-Lingual Sentiment Analysis via Social Media Big Data (A Twitter Case Study)](https://www.mdpi.com/2078-2489/9/5/102/htm)
  - [Incorporating twitter-based human activity information in spatial analysis of crashes in urban areas](https://www.sciencedirect.com/science/article/pii/S0001457517302269)
- The [visualizations.py](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/visualizations.py) saves the functions to plotting the number of tweets or Weibos posted in the city and in the city's open space.
- The [geopandas introduction page](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/geopandas_intro.ipynb) presents some basic spatial analysis conducted by using [geopandas](https://geopandas.org/).
- The [utils.py](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/utils.py) and [data_paths.py](https://github.com/bright1993ff66/social_media_collection_analysis/blob/master/Analysis/data_paths.py) saves some help functions and paths for this project.

The [Data Collection](https://github.com/bright1993ff66/social_media_collection_analysis/tree/master/Data_Collection) folder saves codes to collect the Twitter data.

The [Shapefiles](https://github.com/bright1993ff66/social_media_collection_analysis/tree/master/Shapefiles) folder contains the shapefiles for the spatial analysis.
- HK_tpu_project: epsg=2326

## 4. Requirements

The following packages should be considered before managing this project:

- Python 3.7 or later (for social media data analysis)
- R 3.4.1 or later (for Twitter data collection)
- Spatial data analysis: [geopandas](https://geopandas.org/), [rasterio](https://rasterio.readthedocs.io/en/latest/), [pyproj](https://pyproj4.github.io/pyproj/stable/), [ArcGIS](https://www.arcgis.com/index.html), [QGIS](https://qgis.org/en/site/)
  - The installation process for [geopandas](https://geopandas.org/) on windows is quite complicated, especially with pip. Please check [this stackoverflow post](https://stackoverflow.com/questions/56958421/pip-install-geopandas-on-windows) for more information.
  - The [rasterio](https://rasterio.readthedocs.io/en/latest/) package conducts computation for the raster data.
  - The [pyproj](https://pyproj4.github.io/pyproj/stable/) is used for coordinate transformation.
  - [ArcGIS](https://www.arcgis.com/index.html) and [QGIS](https://qgis.org/en/site/) can be used for map editing and simple spatial data analysis.
- Data frame and computation: [numpy](https://numpy.org/) and [pandas](https://pandas.pydata.org/)
- Cope with time: [datetime](https://docs.python.org/3/library/datetime.html) and [pytz](https://pypi.org/project/pytz/). A list of [pytz](https://pypi.org/project/pytz/) time zone is given [here](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)
- Visualizations: [matplotlib](https://matplotlib.org/stable/index.html)


## 5. Other Data Sources

The following links give the source of other data sources for urban data analysis:

### 5.1 World

- [Satellite Imagery Datasets](https://github.com/chrieke/awesome-satellite-imagery-datasets): List of aerial and satellite imagery datasets with annotations for computer vision and deep learning.
- [Openstreetmap](https://www.openstreetmap.org/#map=11/22.3567/114.1363): Map of a world with various information, including land use, Point-of-Interests (POIs), etc. The package [OSMPythonTools](https://wiki.openstreetmap.org/wiki/OSMPythonTools) offers a neat way to access the Openstreetmap through a Python API

### 5.2 Chinese Cities

- [ChinaAdminDivisionSHP](https://github.com/GaryBikini/ChinaAdminDivisonSHP): Chinese administrative division vector diagram, Shapefile format, four levels: country, province, city, district/county
- [Hong Kong Monthly Traffic and Transport Digest](https://www.td.gov.hk/en/transport_in_hong_kong/transport_figures/monthly_traffic_and_transport_digest/index.html): The monthly key statistics of HK transportation data
- [Hong Kong Census Data](https://www.bycensus2016.gov.hk/en/bc-dp-tpu.html): Census data for Hong Kong, including population, median income, etc.
- [GoPUP](http://doc.gopup.cn/#/README): A very useful tool to collect the data in China, such as Weibo index data, Baidu index data, and Baidu search data

### 5.3 Foreign cities

- [bbike openstreetmap extractor](https://extract.bbbike.org/): The OpenStreetMap data extractor
- [New York Open Data](https://opendata.cityofnewyork.us/data/): New York Open Data is free public data published by New York City agencies and other partners for research. Other US cities such as Chicago also offers [Chicago Data Portal](https://data.cityofchicago.org/)

## 6. Reference

Here is a list of reference:

1. [#europehappinessmap: A Framework for Multi-Lingual Sentiment Analysis via Social Media Big Data (A Twitter Case Study)](https://www.mdpi.com/2078-2489/9/5/102/htm)
1. [Incorporating twitter-based human activity information in spatial analysis of crashes in urban areas](https://www.sciencedirect.com/science/article/pii/S0001457517302269)
1. [WeiboSpider](https://github.com/dataabc/weiboSpider).
1. [Twitter Developer Page](https://developer.twitter.com/en).
2. [Python – User object in Tweepy](https://www.geeksforgeeks.org/python-user-object-in-tweepy/).

Please visit the [reference.bib](https://gitlab.com/li_lishuai_group/changhaoliang/social_media_data_collection_analysis/-/blob/master/reference.bib) for the bibtex citations.

