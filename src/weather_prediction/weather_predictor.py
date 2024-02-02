import asyncio

import pandas as pd

from api.api_client import ApiClient
from utils.analyses_utils import prepare_data, DataFrameType
from weather_prediction.features import daily_discrete_features, daily_regressors, hourly_discrete_features, \
    hourly_regressors
from weather_prediction.prophet.prophet_model import ProphetWeatherPredictionModel

daily_train_size = 1000   # how many days to use for training
hourly_train_size = 1000  # how many hours to use for training


class WeatherPredictor:
    """Class for predicting weather"""

    def __init__(self):
        self._api_client = ApiClient()

    def predict_weather(self, lat: float, lon: float, start: str,
                        hours: int = 0,
                        days: int = 0) -> pd.DataFrame | dict[str, pd.DataFrame]:
        """Predict weather for specific location.

        :param lat: (float) Latitude.
        :param lon: (float) Longitude.
        :param start: (str) Start date ISO 8601 from which the prediction will be started, e.g. start=2024-01-12
        :param hours: (int) Number of hours to predict.
        :param days: (int) Number of days to predict.
        :return: (dict) Predicted weather. Keys: "HOURLY", "DAILY".
        """
        global hourly_prediction, daily_prediction, hourly_df, daily_df
        assert hours > 0 or days > 0, "At least one of hours or days must be greater than 0."

        if hours > 0:
            end = pd.Timestamp(start) + pd.Timedelta(days=hours // 24 + (1 if hours % 24 > 0 else 0))
            hourly_prediction, hourly_df = self._predict_hourly_weather(lat, lon, start, end.__str__())
        if days > 0:
            end = pd.Timestamp(start) + pd.Timedelta(days=days)
            daily_prediction, daily_df = self._predict_daily_weather(lat, lon, start, end.__str__())

        if hours > 0 and days > 0:
            return {DataFrameType.HourlyPrediction.value: hourly_prediction, DataFrameType.DailyPrediction.value: daily_prediction,
                    DataFrameType.HourlyHistory.value: hourly_df, DataFrameType.DailyHistory.value: daily_df}
        elif hours > 0:
            return {DataFrameType.HourlyPrediction.value: hourly_prediction,
                    DataFrameType.HourlyHistory.value: hourly_df}
        elif days > 0:
            return {DataFrameType.DailyPrediction.value: daily_prediction,
                    DataFrameType.DailyHistory.value: daily_df}
        else:
            return {}

    def calculate_metrics(self, lat: float, lon: float, start: str, end: str) -> dict[str, pd.DataFrame]:
        """Calculate metrics for specific location.

        :param lat: (float) Latitude.
        :param lon: (float) Longitude.
        :param start: (str) Start date ISO 8601 from which the prediction will be started, e.g. start=2024-01-12
        :param end: (str) End date ISO 8601 to which the prediction will be made, e.g. end=2024-01-26
        :return: (dict) Metrics. Keys: "HOURLY", "DAILY".
        """
        pass

    def get_actual_data(self, lat: float, lon: float, start: str,
                        hours: int = 0,
                        days: int = 0) -> pd.DataFrame | dict[str, pd.DataFrame]:
        """Get actual weather data for specific location."""
        assert hours > 0 or days > 0, "At least one of hours or days must be greater than 0."
        global hourly_df, daily_df

        if hours > 0:
            end = pd.Timestamp(start).date()
            hourly_df = self._api_client.get_hourly_weather_history(lat, lon, start.__str__(), end.__str__())
        if days > 0:
            end = pd.Timestamp(start).date()
            daily_df = self._api_client.get_daily_weather_history(lat, lon, start.__str__(), end.__str__())

        if hours > 0 and days > 0:
            return {DataFrameType.HourlyHistory.value: hourly_df, DataFrameType.DailyHistory.value: daily_df}
        elif hours > 0:
            return {DataFrameType.HourlyHistory.value: hourly_df}
        elif days > 0:
            return {DataFrameType.DailyHistory.value: daily_df}
        else:
            return {}

    def _predict_daily_weather(self, lat: float, lon: float, start: str, end: str) -> (pd.DataFrame, pd.DataFrame):
        """
        Predict daily weather for specific location.

        :param lat: (float) Latitude.
        :param lon: (float) Longitude.
        :param start: (str) Start date to predict ISO 8601, e.g. start=2024-01-12
        :param end: (str) End date to predict ISO 8601, e.g. end=2024-01-26.
        :return: (dict) Predicted daily weather.
        """
        df_start = (pd.to_datetime(start) - pd.Timedelta(days=daily_train_size)).date()
        df_end = (pd.to_datetime(start) - pd.Timedelta(days=1)).date()
        df = self._api_client.get_daily_weather_history(lat, lon, df_start.__str__(), df_end.__str__())
        df = prepare_data(df, daily_discrete_features)

        daily_model = ProphetWeatherPredictionModel(df, DataFrameType.DailyHistory, daily_regressors)

        period = pd.to_datetime(end) - pd.to_datetime(start)
        start_date = pd.to_datetime(start)
        return (daily_model.predict(period.days, start_date.__str__(), daily_train_size), df)

    def _predict_hourly_weather(self, lat: float, lon: float, start: str, end: str) -> (pd.DataFrame, pd.DataFrame):
        """
        Predict hourly weather for specific location.

        :param lat: (float) Latitude.
        :param lon: (float) Longitude.
        :param start: (str) Start date to predict ISO 8601, e.g. start=2024-01-12.
        :param end: (str) End date to predict ISO 8601, e.g. end=2024-01-26.
        :return: (dict) Predicted hourly weather.
        """
        df_start = (pd.to_datetime(start) - pd.Timedelta(days=hourly_train_size // 24)).date()
        df_end = (pd.to_datetime(start) - pd.Timedelta(days=1)).date()
        df = self._api_client.get_hourly_weather_history(lat, lon, df_start.__str__(), df_end.__str__())
        df = prepare_data(df, hourly_discrete_features)

        hourly_model = ProphetWeatherPredictionModel(df, DataFrameType.HourlyHistory, hourly_regressors)

        period = pd.to_datetime(end) - pd.to_datetime(start)
        start_date = pd.to_datetime(start)
        return hourly_model.predict(period.days * 24, start_date.__str__(), hourly_train_size), df


# pd.set_option('display.max_columns', None)

# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.width', None)

# predictor = WeatherPredictor()
# prediction = predictor.predict_weather(-11.754611883149868, 19.918700267723633, "2021-01-01", hours=24, days=1)

# actual = predictor.get_actual_data(-11.754611883149868, 19.918700267723633, "2021-01-01", hours=24, days=1)

# print(actual)


# print(prediction[DataFrameType.DailyPrediction.value])
# print(prediction[DataFrameType.DailyHistory.value])
# print(prediction[DataFrameType.HourlyPrediction.value])
# print(prediction[DataFrameType.HourlyHistory.value])
