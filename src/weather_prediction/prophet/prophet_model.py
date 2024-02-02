from typing import Any

import pandas as pd
from pandas import DataFrame
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from sklearn.metrics import mean_absolute_error as MAE

from utils.analyses_utils import DataFrameType


class ProphetWeatherPredictionModel:
    """
    Prophet model. Used to predict all variables for the weather in the future.

    Independent variables are predicted independently. Other variables are
    predicted using the predicted independent variables as regressors.
    """

    def __init__(self, df: DataFrame, df_type: DataFrameType, regressors: list[str]):
        """
        Initialize Prophet model.

        :param df: (pd.DataFrame) Dataframe with features.
        :param df_type: (DataFrameType) Type of the dataframe (Daily or Hourly)
        :param regressors: (list[str]) List of independent variables.
        """
        self._df = df
        self._regressors = regressors
        self._df_type = df_type

    def validate(self) -> dict[str, DataFrame]:
        """
        Validate each variable using cross validation on the dataset regressors.

        :return: (dict[str, DataFrame]) Dictionary with validation metrics for each variable.
        """
        metrics = {}
        for regressor in self._regressors:
            train = self._df[["ds", regressor]].copy()
            train = train.rename(columns={regressor: "y"})

            # create a new Prophet model
            regressor_model = Prophet()
            regressor_model.fit(train)

            # cross validation
            cv_results = cross_validation(regressor_model, initial="1000 days", period="180 days", horizon="365 days")
            metrics[regressor] = performance_metrics(cv_results)

        other_variables = [column for column in self._df.columns if column not in self._regressors and column != "ds"]
        for variable in other_variables:
            train = self._df[["ds", variable]].copy()
            train = train.rename(columns={variable: "y"})

            # create a new Prophet model
            variable_model = Prophet()
            for regressor in self._regressors:
                variable_model.add_regressor(regressor)
                train[regressor] = self._df[regressor]
            variable_model.fit(train)

            # cross validation
            cv_results = cross_validation(variable_model, initial="1000 days", period="180 days", horizon="365 days")
            metrics[variable] = performance_metrics(cv_results)

        return metrics

    def predict(self, periods: int, start_date: str, train_size: int) -> pd.DataFrame:
        """
        Predict using Prophet model.

        First, predict the independent variables. Then, predict the other variables
        using the predicted independent variables as regressors.

        :param start_date: (str) Start date for the prediction.
        :param periods: (int) Number of periods to predict. (hours or days)
        :param train_size: (int) Number of periods to use for training.
        :return: (pd.DataFrame) Dataframe with predictions.
        :raises ValueError: If the DataFrameType is unknown.
        """
        if self._df_type == DataFrameType.DailyHistory:
            start_train_date = pd.to_datetime(start_date) - pd.DateOffset(days=train_size)
            end_train_date = pd.to_datetime(start_date) - pd.DateOffset(days=1)
        elif self._df_type == DataFrameType.HourlyHistory:
            start_train_date = pd.to_datetime(start_date) - pd.DateOffset(hours=train_size)
            end_train_date = pd.to_datetime(start_date) - pd.DateOffset(hours=1)
        else:
            raise ValueError("Unknown DataFrameType")

        train_data = self._df[(self._df["ds"] >= start_train_date) & (self._df["ds"] <= end_train_date)]

        future_with_regressors = self._create_empty_future(periods, start_date, self._df_type)
        only_future = future_with_regressors[["ds"]].copy()

        # create a dictionary to hold the different independent variable forecasts
        for regressor in self._regressors:
            train = train_data[["ds", regressor]].copy()
            train = train.rename(columns={regressor: "y"})

            # create a new Prophet model
            regressor_model = Prophet()
            regressor_model.fit(train)

            regressor_future = regressor_model.predict(only_future)

            # add the forecast to the dictionary
            future_with_regressors[regressor] = regressor_future["yhat"]

        # now calculate the forecasts for the other variables
        complete_future = future_with_regressors.copy()

        other_variables = [column for column in self._df.columns if column not in self._regressors and column != "ds"]
        for variable in other_variables:
            train = train_data[["ds", variable]].copy()
            train = train.rename(columns={variable: "y"})

            # create a new Prophet models
            variable_model = Prophet()
            for regressor in self._regressors:
                variable_model.add_regressor(regressor)
                train[regressor] = train_data[regressor]
            variable_model.fit(train)

            variable_future = variable_model.predict(future_with_regressors)

            complete_future[variable] = variable_future["yhat"]

        return complete_future

    @staticmethod
    def test(period: int,
             df: pd.DataFrame, df_type: DataFrameType,
             regressors: list[str],
             train_size: int = 100) -> dict[str, dict[str, Any]]:

        """Test the prediction

        Currently, calculates the average MAE for each variable by splitting the dataset
        into chunks of size (train_size + period) and predicting the next period.

        :param period: (int) Number of period to predict. (days)
        :param df: (pd.DataFrame) Dataframe with features.
        :param df_type: (DataFrameType) Type of the dataframe (Daily or Hourly)
        :param regressors: (list[str]) List of independent variables.
        :param train_size: (int) Number of periods to use for training.
        :return: (dict[str, dict[str, Any]]) Dictionary with validation metrics for each variable.
        """
        test_size = period

        testing_period_size = test_size + train_size

        # calculate the validation metrics for each variable on
        # each bunch of dates (testing_period_size) in the dataset
        variables = df.columns

        predicted = {variable: [] for variable in variables}
        actual = {variable: [] for variable in variables}
        for i in range(0, len(df) - testing_period_size, testing_period_size):
            train = df[i:i + train_size].copy()
            test_date_index = i + testing_period_size - 1
            test_date = df.iloc[test_date_index]

            start_ds = df.iloc[i + train_size]["ds"]  # start forecasting from

            model = ProphetWeatherPredictionModel(train, df_type, regressors)
            forecast = model.predict(test_size, start_ds, train_size)
            predicted_date = forecast.iloc[-1]

            assert test_date["ds"] == predicted_date["ds"]

            for variable in variables:
                actual[variable].append(test_date[variable])
                predicted[variable].append(predicted_date[variable])

        metrics = {"MAE": {}}
        for variable in variables:
            metrics["MAE"][variable] = MAE(actual[variable], predicted[variable])

        return metrics

    @staticmethod
    def _create_empty_future(periods: int, start, df_type: DataFrameType) -> pd.DataFrame:
        """
        Create empty future dataframe.

        :param periods: (int) Number of periods to predict.
        :return: (pd.DataFrame) Empty dataframe with future dates.
        """
        future = pd.DataFrame()
        if df_type == DataFrameType.DailyHistory:
            future["ds"] = pd.date_range(start=start, periods=periods, freq="D")
        elif df_type == DataFrameType.HourlyHistory:
            future["ds"] = pd.date_range(start=start, periods=periods, freq="h")
        return future
