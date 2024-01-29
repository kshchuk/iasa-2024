from enum import Enum, auto

import matplotlib.pyplot as plt
import pandas as pd


def plot_features_evolution(data_frame: pd.DataFrame, features: list[str], time: list[str]):
    """
    Plots features evolution over time for the whole dataset and for the first year.

    :param data_frame: (pd.DataFrame) Dataframe with features.
    :param features: (list[str]) List of features to plot.
    :param time: (list[str]) List of time values.
    :return: None
    """
    plot_features = data_frame[features]
    plot_features.index = time
    plot_features.plot(subplots=True)
    plt.suptitle("Features evolution over time: " + time[0].__str__() + " - " + time[-1].__str__())

    plot_features = data_frame[features][:365]
    plot_features.index = time[:365]
    plot_features.plot(subplots=True)
    plt.suptitle("Features evolution over time: " + time[0].__str__() + " - " + time[365].__str__())

    plt.show()


def print_statistics(data_frame: pd.DataFrame, features: list[str]):
    """
    Prints statistics for the given features.

    :param data_frame: (pd.DataFrame) Dataframe with features.
    :param features: (list[str]) List of features to plot.
    :return: None
    """
    print(data_frame[features].describe().transpose())

class DataFrameType(Enum):
    Daily = auto()
    Hourly = auto()