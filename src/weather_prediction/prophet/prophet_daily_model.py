from typing import Dict, Any

import pandas as pd
from pandas import DataFrame
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from sklearn.metrics import mean_absolute_error as MAE

PREDICT_TO_HISTORY_RATIO = 0.2


class ProphetDailyModel:
    """
    Prophet model. Used to predict all variables for the weather in the future.

    Independent variables are predicted independently. Other variables are
    predicted using the predicted independent variables as regressors.
    """

    def __init__(self, df: DataFrame, regressors: list[str]):
        """
        Initialize Prophet model.

        :param df: (pd.DataFrame) Dataframe with features.
        :param regressors: (list[str]) List of independent variables.
        """
        self._df = df
        self._regressors = regressors

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

    def predict(self, periods: int, start_date: str) -> pd.DataFrame:
        """
        Predict using Prophet model.

        First, predict the independent variables. Then, predict the other variables
        using the predicted independent variables as regressors.

        :param start_date: (str) Start date for the prediction.
        :param periods: (int) Number of periods to predict.
        :return: (pd.DataFrame) Dataframe with predictions.
        """
        future_with_regressors = self._create_empty_future(periods, start_date)
        only_future = future_with_regressors[["ds"]].copy()

        # create a dictionary to hold the different independent variable forecasts
        for regressor in self._regressors:
            train = self._df[["ds", regressor]].copy()
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
            train = self._df[["ds", variable]].copy()
            train = train.rename(columns={variable: "y"})

            # create a new Prophet models
            variable_model = Prophet()
            for regressor in self._regressors:
                variable_model.add_regressor(regressor)
                train[regressor] = self._df[regressor]
            variable_model.fit(train)

            variable_future = variable_model.predict(future_with_regressors)

            complete_future[variable] = variable_future["yhat"]

        return complete_future

    @staticmethod
    def test(period: int, df: pd.DataFrame, regressors: list[str]) -> dict[str, dict[str, Any]]:
        """Test the prediction

        Currently, calculates the average MAE for each variable.

        :param period: (int) Number of period to predict.
        :param df: (pd.DataFrame) Dataframe with features.
        :param regressors: (list[str]) List of independent variables.
        :return: (dict[str, dict[str, Any]]) Dictionary with validation metrics for each variable.
        """
        test_size = period
        train_size = int(test_size / PREDICT_TO_HISTORY_RATIO)

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

            start_ds = df.iloc[i + train_size - 1]["ds"]  # start forecasting from

            model = ProphetDailyModel(train, regressors)
            forecast = model.predict(test_size, start_ds)
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
    def _create_empty_future(periods: int, start) -> pd.DataFrame:
        """
        Create empty future dataframe.

        :param periods: (int) Number of periods to generate.
        :return: (pd.DataFrame) Empty dataframe with future dates.
        """
        future = pd.DataFrame()
        future["ds"] = pd.date_range(start=start, periods=periods + 1, freq="D")[1:]
        return future
