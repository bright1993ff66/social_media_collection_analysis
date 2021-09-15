import os
import time
from collections import Counter
import multiprocessing as mp
import numpy as np
import pandas as pd

from cities_bounds import weibo_path


def compute_threshold(count_dataframe: pd.DataFrame):
    """
    Compute the threshold for identifying the Weibo bot account
    :param dataframe: a dataframe saving the number of Weibos posted by each
    Weibo user
    :return: a threshold for identifying the Weibo bot account
    """
    mean_count = np.mean(count_dataframe['count'])
    std_count = np.std(count_dataframe['count'])
    threshold = mean_count + 2 * std_count
    return threshold


def count_user_weibo(dataframe: pd.DataFrame):
    """
    Count the users and the number of weibos they post.
    Bot accounts are likely to post many tweets in a long time
    :param dataframe: a weibo dataframe
    :return: a pandas dataframe saving the number of weibos posted by each user
    """
    author_id_counter = Counter(dataframe['author_id'])
    return pd.DataFrame(author_id_counter.items(),
                        columns=['author_id', 'count'])


def get_weibos_from_users(user_arr, data_path=weibo_path):
    """
    Get weibos posted by a set of users.
    :param user_arr: the array containing the user ids
    :param data_path: the data path saving the collected Weibos
    :return: a pandas dataframe saving the tweets posted by interested users
    """

    dataframe_list = []
    print("Coping with the id arr: {}".format(user_arr))
    for index, file in enumerate(os.listdir(data_path)):
        print('Coping with the {}th file'.format(index+1))
        dataframe = pd.read_csv(os.path.join(data_path, file),
                                encoding='utf-8', index_col=0)
        dataframe_select = dataframe.loc[dataframe['author_id'].isin(user_arr)]
        dataframe_list.append(dataframe_select)
    concat_data = pd.concat(dataframe_list, axis=0).reset_index(drop=True)
    return concat_data


def parallelize(cpu_num: int, id_arr: np.array, save_path: str):
    """
    Parallelize the processes of finding the tweets. Run the codes as:
        parallelize(cpu_num=20, id_arr=weibo_ids, save_path=saving_path)
    :param cpu_num: the number of cpus used to run
    :param id_arr: the numpy array saving author ids
    :param save_path: the path used to save the generated data
    :return: None. The generated dataframe is saved to a directory
    """
    pool = mp.Pool(processes=cpu_num)
    id_arr_chunks = np.array_split(id_arr, cpu_num)
    # Apply the function in parallel
    chunk_processes = [pool.apply_async(get_weibos_from_users,
                                        args=(user_id_arr, weibo_path))
                       for user_id_arr in id_arr_chunks]
    chunk_results = [chunk.get() for chunk in chunk_processes]
    for result in chunk_results:
        for author_id, dataframe in result.groupby('author_id'):
            dataframe.to_csv(os.path.join(
                save_path, '{}.csv'.format(author_id)))


def get_user_count_dataframe(weibo_data_path: str):
    """
    Count the users and the number of weibos they post given a data path.
    Bot accounts are likely to post many tweets in a long time
    :param weibo_data_path: the path containing the weibo data
    :return: a pandas dataframe saving the number of weibos posted by each user
    """
    weibo_files = os.listdir(weibo_data_path)
    sum_weibo_user_count = pd.DataFrame()
    for file in weibo_files:
        print('Coping with the file: {}'.format(file))
        weibo_dataframe = pd.read_csv(os.path.join(weibo_data_path, file),
                                      encoding='utf-8', index_col=0)
        count_dataframe = count_user_weibo(dataframe=weibo_dataframe)
        count_dataframe = count_dataframe.set_index(['author_id'])
        sum_weibo_user_count = sum_weibo_user_count.add(count_dataframe,
                                                        fill_value=0)
    sum_weibo_user_reindex = sum_weibo_user_count.reset_index()
    return sum_weibo_user_reindex


def find_bot_accounts(count_dataframe):
    """
    Find the Weibo bot accounts
    To be updated...
    :param count_dataframe: pandas dataframe saving the # of Weibos posted
    by each user
    """
    bot_threshold = compute_threshold(count_dataframe=count_dataframe)
    bot_dataframe = count_dataframe.loc[
        count_dataframe['count'] >= bot_threshold]
    bot_ids = np.array(list(bot_dataframe['author_id']))
    return bot_ids


def get_final_bot_ids(user_data_path: str):
    """
    Get the final bot ids based on geographic footprints
    :param: user_data_path: the Weibo data path
    :return: a numpy array saving the final bot ids
    """
    files = os.listdir(user_data_path)
    bot_id_list = []
    for file in files:
        print('Coping with the file: {}'.format(file))
        dataframe = pd.read_csv(os.path.join(user_data_path, file),
                                index_col=0, encoding='utf-8')
        dataframe['pos'] = dataframe.apply(
            lambda row: (row.lat, row.lon), axis=1)
        _, most_common_count = Counter(
            dataframe['pos']).most_common()[0]
        percent = most_common_count/len(set(dataframe['weibo_id']))
        if percent >= 0.6:
            author_id = list(dataframe['author_id'])[0]
            bot_id_list.append(author_id)
    return np.array(bot_id_list)


if __name__ == '__main__':
    start_time = time.time()
    cur_dir = os.getcwd()
    saving_path = os.path.join(cur_dir, 'weibo_from_users')
    # Get the number of tweets posted by each user
    count_data = get_user_count_dataframe(weibo_data_path=weibo_path)
    count_data.to_csv("count_weibo_user.csv", encoding='utf-8')
    count_data = pd.read_csv("count_weibo_user.csv", index_col=0,
                             encoding='utf-8')
    # Find the candidate bot ids
    bot_ids = find_bot_accounts(count_data)
    np.save("weibo_bot_ids.npy", bot_ids)
    weibo_ids = np.load("weibo_bot_ids.npy", allow_pickle=True)
    # Get all the Weibos posted by candidate bot accounts
    parallelize(cpu_num=20, id_arr=weibo_ids, save_path=saving_path)
    # Find the bot Weibo accounts and save to local directory
    final_bot_accounts = get_final_bot_ids(
        user_data_path=saving_path)
    np.save("weibo_bots_final.npy", final_bot_accounts)
    end_time = time.time()
    print("Total time: {}".format((end_time - start_time)/3600))
