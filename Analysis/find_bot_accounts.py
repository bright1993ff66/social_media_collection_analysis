import pandas as pd
import os
import numpy as np
from collections import Counter

from matplotlib import pyplot as plt

from utils import column_dtype_dict, read_csv_columns
from data_paths import project_code_path


def count_user_tweet(dataframe):
    """
    Count the users and the number of tweets they post.
    Bot accounts are likely to post many tweets in a long time
    :param dataframe: a tweet dataframe
    :return: a pandas dataframe saving the number of tweets posted by each user
    """
    user_set = set(dataframe['user_id_str'])
    user_list, tweet_count_list, tweet_pos_percent_list = [], [], []
    for user in user_set:
        user_list.append(user)
        data_select = dataframe.loc[dataframe['user_id_str'] == user].copy()
        data_select['pos'] = data_select.apply(lambda row: (row.lat, row.lon), axis=1)
        _, most_common_num = Counter(data_select['pos']).most_common()[0]
        tweet_count_list.append(data_select.shape[0])
        tweet_pos_percent_list.append(most_common_num/len(set(data_select['id_str'])))
    count_data = pd.DataFrame()
    count_data['user_id'] = user_list
    count_data['count'] = tweet_count_list
    count_data['loc_percent'] = tweet_pos_percent_list
    count_data_final = count_data.sort_values(by='count', ascending=False).reset_index(drop=True)
    return count_data_final


def plot_tweet_count_dist(count_dataframe, percentile: float):
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


if __name__ == '__main__':
    check_path_atlanta = r'D:\Projects\Heat_tweets\codes\open_space\atlanta'
    check_file = r'atlanta_1.csv'
    data = read_csv_columns(path=check_path_atlanta, filename=check_file,
                            dtype_convert_dict=column_dtype_dict)
    count_data = count_user_tweet(data)
    count_data.to_excel(os.path.join(project_code_path, 'check_count.xlsx'))
    # print(count_data.sample(10))
    plot_tweet_count_dist(count_data, percentile=95)