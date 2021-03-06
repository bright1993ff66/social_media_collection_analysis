import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from data_paths import figures_path, count_daily_hour_path
from cities_bounds import cities_dict_foreign, cities_dict_china


class PlotRatioCities(object):
    """
    Create objects for plotting
    """
    def __init__(self, city_name, location, plot_color):
        """
        Initialize the object for plotting
        :param city_name: the name of the city
        :param location: the location saving the count dataframe
        :param plot_color: the string used to specify the color for plot
        """
        self.city_name = city_name
        self.data_loc = location
        self.count_filename = '(UTC){}_count_combine.csv'.format(self.city_name)
        self.plot_color = plot_color


def create_day_plot_for_one_count(dataframe: pd.DataFrame, title: str, start_date: datetime,
                                  end_date: datetime, save_filename: str, in_china=True) -> None:
    """
    Create the number of traffic relevant weibos in each day plot
    :param dataframe: a Weibo dataframe
    :param title: the title of the figure
    :param start_date: the start date of the studied time
    :param end_date: the end date of the studied time
    :param save_filename: the saved figure filename in local directory
    :param in_china: if this city is in China or not
    :return: None. The figure is saved to local
    """
    dataframe_copy = dataframe.copy()
    if 'count' not in dataframe_copy:
        count_col_string = 'open_space_count'
    else:
        count_col_string = 'count'
    count_list = []
    days = mdates.drange(start_date, end_date, timedelta(days=1))
    for day_index, xtick in zip(list(range((end_date - start_date).days)), days):
        check_date = start_date + timedelta(days=day_index)
        check_year, check_month, check_day = check_date.year, check_date.month, check_date.day
        dataframe_year = dataframe_copy.loc[dataframe_copy['year'] == check_year]
        dataframe_month = dataframe_year.loc[dataframe_year['month'] == check_month]
        dataframe_day = dataframe_month.loc[dataframe_month['day'] == check_day]
        count_list.append(sum(list(dataframe_day[count_col_string])))

    # Create the line plot
    day_figure, day_axis = plt.subplots(1, 1, figsize=(20, 8))
    day_axis.plot(days, count_list, color='black')

    # xaxis setting
    day_axis.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
    day_axis.xaxis.set_major_locator(mdates.DayLocator(interval=30))
    day_axis.set_xlabel('Date')

    # yaxis setting
    day_axis.set_ylabel('Count')

    # Set the title and save figure
    day_axis.set_facecolor('white')
    day_axis.margins(0)
    day_axis.set_title(title)

    # Set the top and right axis to be invisible:
    # https://stackoverflow.com/questions/925024/how-can-i-remove-the-top-and-right-axis-in-matplotlib
    day_axis.spines['right'].set_visible(False)
    day_axis.spines['top'].set_visible(False)

    # Auto format dates in the x-axis
    day_figure.autofmt_xdate()

    # Save the figure to the local directory
    if in_china:
        day_figure.savefig(os.path.join(figures_path, 'china', save_filename), bbox_inches='tight')
    else:
        day_figure.savefig(os.path.join(figures_path, 'foreign', save_filename), bbox_inches='tight')


def create_day_plot_for_mul_counts(dataframe: pd.DataFrame, title: str, start_date: datetime,
                                   end_date: datetime, city_name: str, save_filename: str) -> None:
    """
    Create the number of traffic relevant weibos in each day plot
    :param dataframe: a Weibo dataframe
    :param title: the title of the figure
    :param start_date: the start date of the studied time
    :param end_date: the end date of the studied time
    :param city_name: the name of the processing city
    :param save_filename: the saved figure filename in local directory
    :return: None. The figure is saved to local
    """
    dataframe_copy = dataframe.copy()
    if 'count' not in dataframe_copy:
        count_col_string = 'open_space_count'
    else:
        count_col_string = 'count'
    open_space_count, total_count = [], []
    days = mdates.drange(start_date, end_date, timedelta(days=1))
    for day_index, xtick in zip(list(range((end_date - start_date).days)), days):
        check_date = start_date + timedelta(days=day_index)
        check_year, check_month, check_day = check_date.year, check_date.month, check_date.day
        dataframe_year = dataframe_copy.loc[dataframe_copy['year'] == check_year]
        dataframe_month = dataframe_year.loc[dataframe_year['month'] == check_month]
        dataframe_day = dataframe_month.loc[dataframe_month['day'] == check_day]
        if sum(list(dataframe_day[count_col_string])) == 0:
            open_space_count.append(0)
        else:
            open_space_count.append(np.log(sum(list(dataframe_day[count_col_string]))))

        if sum(list(dataframe_day['total_count'])) == 0:
            total_count.append(0)
        else:
            total_count.append(np.log(sum(list(dataframe_day['total_count']))))

    # Create the line plot
    day_figure, day_axis = plt.subplots(1, 1, figsize=(20, 8))
    day_axis.plot(days, open_space_count, color='red', label='Geocoded Tweets Posted in Open Space')
    day_axis.plot(days, total_count, color='blue', linestyle='--', label='All Geocoded Tweets')

    # xaxis setting
    day_axis.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
    day_axis.xaxis.set_major_locator(mdates.DayLocator(interval=30))
    day_axis.set_xlabel('Date')

    # yaxis setting
    day_axis.set_ylabel('log(Count)')

    # Set the title, legend, and save figure
    day_axis.set_facecolor('white')
    day_axis.margins(0)
    day_axis.set_title(title)
    day_figure.autofmt_xdate()
    day_axis.legend()
    if city_name in cities_dict_foreign:
        day_figure.savefig(os.path.join(figures_path, 'foreign', save_filename), bbox_inches='tight')
    elif city_name in cities_dict_china:
        day_figure.savefig(os.path.join(figures_path, 'china', save_filename), bbox_inches='tight')
    else:
        raise ValueError('The city name is not correctly specified!It should be either in '
                         'cities_dict_foreign or cities_dict_china')


def plot_ratio(count_dataframe: pd.DataFrame, select_column_name: str, start_date: datetime, end_date: datetime,
               color_string: str, figure_save_path: str, save_filename: str):
    """
    Plot the percentage of geocoded tweets posted in the open space
    :param count_dataframe: the pandas dataframe saving the number of tweets posted in each hour
    :param select_column_name: the column name selected to plot
    :param start_date: the start date for plotting
    :param end_date: the end date for plotting
    :param color_string: the string used to specify the color of the line
    :param figure_save_path: the path used to save the figure
    :param save_filename: the saved filename
    :return: None. The created figure is saved to the local directory
    """
    count_list, check_time_list = [], []
    dataframe_copy = count_dataframe.copy()
    hours = mdates.drange(start_date, end_date, timedelta(hours=1))

    # Specify the column names for the day information
    if 'date' in count_dataframe:
        day_column_name = 'date'
    elif 'day' in count_dataframe:
        day_column_name = 'day'
    else:
        raise ValueError("The day column name should be either 'date' or 'day'")

    # Count the number of tweets in each hour
    for hour_index, xtick in zip(list(range(int((end_date - start_date).total_seconds()/3600)+1)), hours):
        check_time = start_date + timedelta(hours=hour_index)
        check_year, check_month, check_day, check_hour = check_time.year, check_time.month, check_time.day,\
                                                         check_time.hour
        dataframe_year = dataframe_copy.loc[dataframe_copy['year'] == check_year]
        dataframe_month = dataframe_year.loc[dataframe_year['month'] == check_month]
        dataframe_day = dataframe_month.loc[dataframe_month[day_column_name] == check_day]
        dataframe_hour = dataframe_day.loc[dataframe_day['hour'] == check_hour]
        count_list.append(list(dataframe_hour[select_column_name])[0])
        check_time_list.append(check_time)

    # Create the line plot
    figure, axis = plt.subplots(1, 1, figsize=(20, 8), dpi=300)
    axis.plot(hours, count_list, color=color_string)

    # xaxis setting
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d-%H'))
    axis.xaxis.set_major_locator(mdates.DayLocator(interval=30))
    axis.set_xlabel('Date', size=25)

    # yaxis setting
    ytick_vals = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    axis.set_yticks(ytick_vals)
    axis.set_yticklabels([str(val) for val in ytick_vals], size=20)
    axis.set_ylabel('Ratio', size=25)

    # Set the title and save figure
    axis.set_facecolor('white')
    axis.margins(0)

    # Set the top and right axis to be invisible:
    # https://stackoverflow.com/questions/925024/how-can-i-remove-the-top-and-right-axis-in-matplotlib
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)

    # Auto format dates in the x-axis
    figure.autofmt_xdate()

    figure.savefig(os.path.join(figure_save_path, save_filename))


def plot_hist(dataframe, select_column_name: str, color_string: str, figure_save_path: str, save_filename: str):
    """
    Plot the histogram of a column
    :param dataframe: the pandas dataframe saving the number of tweets posted in each hour
    :param select_column_name: the column name selected to plot
    :param color_string: the string used to specify the color of the line
    :param figure_save_path: the path used to save the figure
    :param save_filename: the saved filename
    :return: None. The created figure is saved to the local directory
    """
    count_list = list(dataframe[select_column_name])

    figure, axis = plt.subplots(1, 1, figsize=(10, 8), dpi=300)
    axis.hist(count_list, color=color_string)

    # Set the top and right axis to be invisible:
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)

    figure.savefig(os.path.join(figure_save_path, save_filename))


def create_hour_weekday_plot(dataframe: pd.DataFrame, color_hour: str, color_weekday: str, title_hour: str,
                             title_weekday: str, hour_save_filename: str, weekday_save_filename: str,
                             in_china=True) -> None:
    """
    Create the hour and weekday time distribution plot
    :param dataframe: a dataframe saving the number of tweets or Weibos in each hour
    :param color_hour: the color for the hour plot
    :param color_weekday: the color for the weekday plot
    :param title_hour: The title for the hour's figure
    :param title_weekday: The title for the weekday's figure
    :param hour_save_filename: the name of the saved figure for hourly plot
    :param weekday_save_filename: the name of the saved figure for weekday plot
    :param in_china: if this city is in China or not
    """
    assert 'weekday' in dataframe and 'hour' in dataframe, 'The dataframe should contain hour and weekday info'
    dataframe_copy = dataframe.copy()
    if 'count' not in dataframe_copy:
        count_col_string = 'open_space_count'
    else:
        count_col_string = 'count'
    # Get the values for the bar plot
    fig_hour, axis_hour = plt.subplots(1, 1, figsize=(10, 8))
    fig_weekday, axis_weekday = plt.subplots(1, 1, figsize=(10, 8))
    hours_name_list, weekday_names_list = list(range(0, 24)), list(range(7))
    hours_value_list, weekdays_value_list = [], []
    for hour in hours_name_list:
        data_select = dataframe_copy.loc[dataframe_copy['hour'] == hour]
        hours_value_list.append(sum(list(data_select[count_col_string])))
    for weekday in weekday_names_list:
        data_select = dataframe_copy.loc[dataframe_copy['weekday'] == weekday]
        weekdays_value_list.append(sum(list(data_select[count_col_string])))

    # create bar plot
    axis_hour.bar(hours_name_list, hours_value_list, color=color_hour, edgecolor='white')
    axis_weekday.bar(weekday_names_list, weekdays_value_list, color=color_weekday, edgecolor='white')

    # # Display the bar values in the bar plot
    # for hour_name, hour_val in zip(hours_name_list, hours_value_list):
    #     axis_hour.text(x=hour_name-0.3, y=hour_val + 20, s = "{}".format(hour_val), color='black', fontsize=10)
    # for weekday_name, weekday_val in zip(weekday_names_list, weekdays_value_list):
    #     axis_weekday.text(x=weekday_name-0.2, y=weekday_val + 20, s="{}".format(weekday_val),
    #     color='black', fontsize=10)

    # Set axis tokens
    axis_hour.set_xticks(list(range(24)))
    axis_hour.set_xlabel('Hour')
    axis_hour.set_ylabel('Count')
    axis_hour.set_title(title_hour)
    axis_weekday.set_xticks(list(range(7)))
    axis_weekday.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
    axis_weekday.set_xlabel('Weekday')
    axis_weekday.set_ylabel('Count')
    axis_weekday.set_title(title_weekday)

    # Change the plot background color and hide grids
    axis_hour.set_facecolor('white')
    axis_hour.grid(False)
    axis_weekday.set_facecolor('white')
    axis_weekday.grid(False)

    # # Set the ylim
    # axis_hour.set_ylim(bottom=np.percentile(hours_value_list, 50))
    # axis_weekday.set_ylim(bottom=np.percentile(weekdays_value_list, 50))

    # Tight the figures and save
    fig_hour.tight_layout()
    fig_weekday.tight_layout()

    # Set the top and right axis to be invisible:
    # https://stackoverflow.com/questions/925024/how-can-i-remove-the-top-and-right-axis-in-matplotlib
    axis_hour.spines['right'].set_visible(False)
    axis_hour.spines['top'].set_visible(False)
    axis_weekday.spines['right'].set_visible(False)
    axis_weekday.spines['top'].set_visible(False)

    if in_china:
        fig_hour.savefig(os.path.join(figures_path, 'china', hour_save_filename), bbox_inches='tight')
        fig_weekday.savefig(os.path.join(figures_path, 'china', weekday_save_filename), bbox_inches='tight')
    else:
        fig_hour.savefig(os.path.join(figures_path, 'foreign', hour_save_filename), bbox_inches='tight')
        fig_weekday.savefig(os.path.join(figures_path, 'foreign', weekday_save_filename), bbox_inches='tight')
