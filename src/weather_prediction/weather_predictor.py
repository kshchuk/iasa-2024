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
        global hourly_prediction, daily_prediction
        assert hours > 0 or days > 0, "At least one of hours or days must be greater than 0."

        loop = asyncio.get_event_loop()

        if hours > 0:
            end = pd.Timestamp(start) + pd.Timedelta(days=hours // 24 + (1 if hours % 24 > 0 else 0))
            hourly_prediction = loop.run_until_complete(self._predict_hourly_weather(lat, lon, start, end.__str__()))
        if days > 0:
            end = pd.Timestamp(start) + pd.Timedelta(days=days)
            daily_prediction = loop.run_until_complete(self._predict_daily_weather(lat, lon, start, end.__str__()))

        if hours > 0 and days > 0:
            return {DataFrameType.Hourly.value: hourly_prediction, DataFrameType.Daily.value: daily_prediction}
        elif hours > 0:
            return {DataFrameType.Hourly.value: hourly_prediction}
        else:
            return {DataFrameType.Daily.value: daily_prediction}

    def calculate_metrics(self, lat: float, lon: float, start: str, end: str) -> dict[str, pd.DataFrame]:
        """Calculate metrics for specific location.

        :param lat: (float) Latitude.
        :param lon: (float) Longitude.
        :param start: (str) Start date ISO 8601 from which the prediction will be started, e.g. start=2024-01-12
        :param end: (str) End date ISO 8601 to which the prediction will be made, e.g. end=2024-01-26
        :return: (dict) Metrics. Keys: "HOURLY", "DAILY".
        """
        pass

    async def _predict_daily_weather(self, lat: float, lon: float, start: str, end: str) -> pd.DataFrame:
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

        daily_model = ProphetWeatherPredictionModel(df, DataFrameType.Daily, daily_regressors)

        period = pd.to_datetime(end) - pd.to_datetime(start)
        start_date = pd.to_datetime(start)
        return daily_model.predict(period.days, start_date.__str__(), daily_train_size)

    async def _predict_hourly_weather(self, lat: float, lon: float, start: str, end: str) -> pd.DataFrame:
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

        hourly_model = ProphetWeatherPredictionModel(df, DataFrameType.Hourly, hourly_regressors)

        period = pd.to_datetime(end) - pd.to_datetime(start)
        start_date = pd.to_datetime(start)
        return hourly_model.predict(period.days * 24, start_date.__str__(), hourly_train_size)


pd.set_option('display.max_columns', None)

pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

predictor = WeatherPredictor()
prediction = predictor.predict_weather(47.3769, 8.5417, "2021-01-01", hours=26, days=3)
print(prediction["HOURLY"])
print(prediction["DAILY"])
