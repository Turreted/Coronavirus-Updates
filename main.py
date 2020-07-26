import os
import sys
import pandas
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from pandas.plotting import register_matplotlib_converters
import pickle
import pprint

datadict = {}

register_matplotlib_converters()

dir_path = os.path.dirname(os.path.realpath(__file__))
download_exe = os.path.abspath(dir_path + '/data/download.sh')
datapath = dir_path + '/data/'

def update_files():
    current_dir = os.getcwd()
    os.chdir(datapath)
    os.system(download_exe)
    os.chdir(current_dir)

update_files()

confirmed_data_path = os.path.join(datapath, 'Confirmed.csv', )
recovered_data_path = os.path.join(datapath, 'Recovered.csv')
deaths_data_path = os.path.join(datapath, 'Deaths.csv')



def get_recent_data(df: pandas.DataFrame) -> int:
    colunm_name = df.columns[-1]
    values = df[colunm_name].values
    return np.sum(np.array(values))


def get_condensed_data(df: pandas.DataFrame) -> np.array:
    """
    Strips away country / region and returns data as numpy array
    """
    ret_array = []
    for col in df.columns[4:]:
        ret_array.append(int(df[col].sum()))

    return np.array(ret_array)


def get_rates(df: pandas.DataFrame) -> tuple:
    """
    returns the current rate of change and the average rate of change
    """
    df_condensed = get_condensed_data(df)
    differences = np.ediff1d(df_condensed)

    average_diff = np.mean(differences)
    current_diff = df_condensed[-1] - df_condensed[-2] 

    return (current_diff, round(average_diff, 2))


def get_data_by_country(df: pandas.DataFrame) -> dict:
    ret_dict = {}
    current_values = df[df.columns[-1]].values
    countries = df['Country/Region'].values
    for country in countries:
        if country not in list(ret_dict.keys()):
            ret_dict.update({country: 0})

    for i in range(len(current_values)):
        country_occurance = countries[i]
        value = current_values[i]
        ret_dict[country_occurance] += value

    return ret_dict


def dataframe_by_country(df: pandas.DataFrame, country_name: str):
    for i, country in enumerate(df['Country/Region'].values):
        if country != country_name:
            df = df.drop(i)
    return df


def graph(df: pandas.DataFrame, name: str, title=None):
    dates = list(df.columns)[4:]
    dates = [date.split(' ')[0] for date in dates]
    values = get_condensed_data(df)

    fig, ax = plt.subplots()
    xticks = np.arange(len(dates))
    ax.plot(xticks, values)
    
    ax_xticks = xticks[::int(len(xticks)/10)]
    ax_xticks[-1] = xticks[-1]

    ax_dates = dates[::int(len(dates)/10)]
    ax_dates[-1] = dates[-1]

    plt.xticks(ax_xticks, ax_dates, rotation=30)
    plt.ticklabel_format(style='plain', axis='y')
    ax.set_title(title)
    plt.savefig(name)





recovered_df = pandas.read_csv(recovered_data_path)
deaths_df = pandas.read_csv(deaths_data_path)
cases_df = pandas.read_csv(confirmed_data_path)
US_df = dataframe_by_country(cases_df, "US")


current_cases = get_recent_data(cases_df)
current_deaths = get_recent_data(deaths_df)
curent_recovered = get_recent_data(recovered_df)

datadict.update({'Infected': current_cases})
datadict.update({'Deaths': current_deaths})
datadict.update({'Recovered': curent_recovered})

# print("{: >20} {: >20} {: >20}".format("CASES", "DEATHS", "RECOVERIES"))
# print("{: >20} {: >20} {: >20}".format(current_cases, current_deaths, curent_recovered))

def eval_word(diff):
    if diff > 0:
        return "more" 
    else:
        return "fewer"

current_diff, average_diff = get_rates(cases_df)
datadict.update({'info1': f'{current_diff} {eval_word(current_diff)} people were infected today. The average rate of infection is {average_diff} people per day.'})

current_diff, average_diff = get_rates(deaths_df)
datadict.update({'info2':f'{current_diff} {eval_word(current_diff)} people were killed today. The average rate of death is {average_diff} people per day.'})

current_diff, average_diff = get_rates(recovered_df)
datadict.update({'info3':f'{current_diff} {eval_word(current_diff)} people recovered today. The average rate of recovery is {average_diff} people per day.'})

infections_by_contry = get_data_by_country(cases_df)
datadict.update({'Countries': infections_by_contry})

graph(recovered_df, 'recovered.png', title='Total Recovered')
graph(cases_df, 'infected.png', title='Confirmed Cases')
graph(deaths_df, 'killed.png', title='Total Deaths')
graph(US_df, 'US_cases.png', title='Confirmed Cases in the U.S.')



with open('data.pickle', 'wb') as handle:
    pickle.dump(datadict, handle, protocol=pickle.HIGHEST_PROTOCOL)
