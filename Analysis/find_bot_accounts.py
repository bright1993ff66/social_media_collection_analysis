# basics
import pandas as pd
import os
import numpy as np
from collections import Counter
from datetime import datetime
import pytz

# visualization
from matplotlib import pyplot as plt

# Load the count tweet class and city profile
from count_tweets import CountTweets
from cities_bounds import cities_dict_foreign


def get_all_geocoded_tweets_in_city(city_name: str, saving_path: str, save_filename: str):
    """
    Get all the geocoded tweets posted in a city
    :param city_name: the name of a city
    :param saving_path: the saving path
    :param save_filename: the saved filename
    :return: None. The created dataframe is saved to a local directory
    """
    assert city_name in cities_dict_foreign, 'The city name should be in the city profile dictionary'
    city_tweet_obj = CountTweets(city_name=city_name, city_profile_dict=cities_dict_foreign,
                                 start_time=datetime(2016, 5, 1, tzinfo=pytz.utc),
                                 end_time=datetime(2020, 12, 31, tzinfo=pytz.utc),
                                 utc_or_not=True)
    dataframe_list = []
    for considered_year in city_tweet_obj.considered_year_list:
        print('Coping with the year: {}'.format(considered_year))
        csv_path = os.path.join(city_tweet_obj.city_loc, considered_year)
        try:
            for csv_file_name in os.listdir(csv_path):
                print('Coping with the file: {}'.format(csv_file_name))
                try:
                    dataframe = pd.read_csv(open(os.path.join(csv_path, csv_file_name), 
                                                 encoding='utf-8', errors='ignore'),
                                            usecols=['user_id_str', 'id_str', 'lat', 'lon'],
                                            dtype={'user_id_str': str, 'id_str': str})
                    geocoded_dataframe = dataframe.loc[~dataframe['lat'].isnull()]
                    geocoded_without_duplicates = geocoded_dataframe.drop_duplicates(subset=['id_str'])
                    geocoded_tweet_city = CountTweets.find_tweet_in_city(
                        geocoded_without_duplicates, bounding_box_vals=city_tweet_obj.city_bounding_box)
                    dataframe_list.append(geocoded_tweet_city)
                except KeyError:
                    print('The csv file: {} does not have any column names. Ignore'.format(csv_file_name))
                except ValueError:
                    print('ValueError occurs for file: {}. Ignore.'.format(csv_file_name))
                except pd.errors.ParserError:
                    print('Parser error occurred in file: {}. Ignore.'.format(csv_file_name))
            print('The year: {} has been processed'.format(considered_year))
            concat_geocoded_data = pd.concat(dataframe_list, axis=0)
            concat_geocoded_data.to_csv(os.path.join(saving_path, considered_year + save_filename), encoding='utf-8')
            # Release memory
            del concat_geocoded_data
            dataframe_list = []
        except FileNotFoundError:
            print('There is no {} folder in local'.format(str(considered_year)))


def count_user_tweet(dataframe: pd.DataFrame):
    """
    Count the users and the number of tweets they post.
    Bot accounts are likely to post many tweets in a long time
    :param dataframe: a tweet dataframe
    :return: a pandas dataframe saving the number of tweets posted by each user
    """
    user_set = set(dataframe['user_id_str'])
    user_list, tweet_count_list, tweet_pos_percent_list = [], [], []
    for user in user_set:
        data_select = dataframe.loc[dataframe['user_id_str'] == user].copy()
        if data_select.shape[0] > 0:
            user_list.append(user)
            data_select['pos'] = data_select.apply(lambda row: (row.lat, row.lon), axis=1)
            _, most_common_count = Counter(data_select['pos']).most_common()[0]
            tweet_count_list.append(data_select.shape[0])
            tweet_pos_percent_list.append(most_common_count / len(set(data_select['id_str'])))
    count_data = pd.DataFrame()
    count_data['user_id'] = user_list
    count_data['count'] = tweet_count_list
    count_data['loc_percent'] = tweet_pos_percent_list
    count_data_final = count_data.sort_values(by='count', ascending=False).reset_index(drop=True)
    return count_data_final


def get_bot_users(count_dataframe: pd.DataFrame, save_path: str, save_filename: str):
    """
    Get the user ids that are bot accounts. Some works for reference:
    https://www.mdpi.com/2078-2489/9/5/102/htm
    https://www.sciencedirect.com/science/article/pii/S0001457517302269
    :param count_dataframe: the pandas dataframe counting the tweet count and loc percent
    :param save_path: the path to the save the bot user ids
    :param save_filename: the name of the saved file
    :return: None. The bot ids are saved to the local directory
    """
    assert 'count' in count_dataframe, 'The count dataframe should have a column named count'
    assert 'loc_percent' in count_dataframe, 'The count dataframe should have a column named loc_percent'

    tweet_count_mean = np.mean(count_dataframe['count'])
    tweet_count_std = np.std(count_dataframe['count'])
    threshold = tweet_count_mean + 2 * tweet_count_std
    decision = (count_dataframe['count'] > threshold) & (count_dataframe['loc_percent'] > 0.6)
    bot_count_dataframe = count_dataframe[decision]
    bot_ids = np.array(list(set(bot_count_dataframe['user_id'])))
    print('We have got {} bots'.format(len(bot_ids)))
    print('They posted {} tweets'.format(sum(bot_count_dataframe['count'])))
    np.save(os.path.join(save_path, save_filename), bot_ids)


def plot_tweet_count_dist(count_dataframe: pd.DataFrame, percentile: float):
    """
    Plot the histogram of the number of tweets posted by users
    :param count_dataframe: a pandas dataframe saving the number of tweets posted by each user
    :param percentile: the interested percentile
    :return: None.
    """
    assert 'user_id' in count_dataframe, "The count dataframe saves the user id"
    assert 'count' in count_dataframe, "The count saves the number of appearance"
    assert 50 < percentile <= 99, "Please set an appropriate percentile: 50 < percentile <= 99"

    threshold = np.percentile(list(count_dataframe['count']), percentile)

    figure, axis = plt.subplots(1, 1, figsize=(10, 8), dpi=300)
    count_dataframe['count'].hist(ax=axis, color='blue')
    axis.axvline(threshold, color='black')
    axis.text(200, 3000, "Threshold: {}".format(threshold))
    axis.grid(False)
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    plt.show()