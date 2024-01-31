import argparse
import requests_cache
from pandas import DataFrame
from retry_requests import retry
import pandas as pd
import openmeteo_requests

from src.utils.analyses_utils import plot_features_evolution, prepare_data, DataFrameType
from src.utils.analyses_utils import print_statistics
from src.weather_prediction.prophet.prophet_model import ProphetWeatherPredictionModel


all_daily_features = ["weather_code", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
                      "sunshine_duration", "precipitation_sum", "precipitation_hours", "wind_speed_10m_max",
                      "wind_gusts_10m_max", "wind_direction_10m_dominant"]

daily_discrete_features = ["weather_code", "wind_direction_10m_dominant"]
daily_regressors = ["temperature_2m_mean", "precipitation_sum", "wind_speed_10m_max"]


all_hourly_features = ["temperature_2m", "relative_humidity_2m", "precipitation", "weather_code", "surface_pressure",
                       "cloud_cover", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"]

hourly_discrete_features = ["weather_code", "wind_direction_10m"]
hourly_regressors = ["temperature_2m", "surface_pressure", "wind_speed_10m"]


class ApiClient:
    """
    Api Client for OpenMeteo API.
    """

    def __init__(self):
        # Setup the Open-Meteo API client with cache and retry on error
        self._cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
        self._retry_session = retry(self._cache_session, retries=5, backoff_factor=0.2)
        self._openmeteo = openmeteo_requests.Client(session=self._retry_session)

    def get_daily_weather_history(self, lat: float, lon: float, start: str, end: str) -> DataFrame:
        """
        Get weather history for specific location.

        :param lat: (float) Latitude.
        :param lon: (float) Longitude.
        :param start: (str) Start date ISO 8601, e.g. start=2024-01-12.
        :param end: (str) End date ISO 8601, e.g. end=2024-01-26.
        :return: (dict) Weather history.
        """
        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start,
            "end_date": end,
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
                      "sunshine_duration", "precipitation_sum", "precipitation_hours", "wind_speed_10m_max",
                      "wind_gusts_10m_max", "wind_direction_10m_dominant"]
        }
        responses = self._openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_weather_code = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
        daily_temperature_2m_mean = daily.Variables(3).ValuesAsNumpy()
        daily_sunshine_duration = daily.Variables(4).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(5).ValuesAsNumpy()
        daily_precipitation_hours = daily.Variables(6).ValuesAsNumpy()
        daily_wind_speed_10m_max = daily.Variables(7).ValuesAsNumpy()
        daily_wind_gusts_10m_max = daily.Variables(8).ValuesAsNumpy()
        daily_wind_direction_10m_dominant = daily.Variables(9).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s"),
            end=pd.to_datetime(daily.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )}

        daily_data["weather_code"] = daily_weather_code
        daily_data["temperature_2m_max"] = daily_temperature_2m_max
        daily_data["temperature_2m_min"] = daily_temperature_2m_min
        daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
        daily_data["sunshine_duration"] = daily_sunshine_duration
        daily_data["precipitation_sum"] = daily_precipitation_sum
        daily_data["precipitation_hours"] = daily_precipitation_hours
        daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
        daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
        daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

        daily_dataframe = pd.DataFrame(data=daily_data)
        return daily_dataframe

    def get_hourly_weather_history(self, lat: float, lon: float, start: str, end: str) -> DataFrame:
        """
        Get hourly weather history for specific location.

        :param lat: (float) Latitude.
        :param lon: (float) Longitude.
        :param start: (str) Start date ISO 8601, e.g. start=2024-01-12.
        :param end: (str) End date ISO 8601, e.g. end=2024-01-26.
        :return: (dict) Weather history.
        """
        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start,
            "end_date": end,
            "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "weather_code", "surface_pressure",
                       "cloud_cover", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"]
        }
        responses = self._openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()
        hourly_surface_pressure = hourly.Variables(4).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(5).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(6).ValuesAsNumpy()
        hourly_wind_direction_10m = hourly.Variables(7).ValuesAsNumpy()
        hourly_wind_gusts_10m = hourly.Variables(8).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
        hourly_data["precipitation"] = hourly_precipitation
        hourly_data["weather_code"] = hourly_weather_code
        hourly_data["surface_pressure"] = hourly_surface_pressure
        hourly_data["cloud_cover"] = hourly_cloud_cover
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
        hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m

        hourly_dataframe = pd.DataFrame(data=hourly_data)
        return hourly_dataframe


def main():
    parser = argparse.ArgumentParser(description="Make Api Request")

    # default values are for Kyiv
    parser.add_argument(
        "--lat", help="Latitude", required=False, dest="lat", default=50.450001
    )
    parser.add_argument(
        "--lon", help="Longitude", required=False, dest="lon", default=30.523333
    )
    parser.add_argument(
        "--start", help="Start time (ISO 8601) ",
        required=False, dest="start", default="2021-01-26"
    )
    parser.add_argument(
        "--end", help="End time (ISO 8601) ",
        required=False, dest="end", default="2024-01-26"
    )

    args = parser.parse_args()

    api_client = ApiClient()
    weather_history = api_client.get_hourly_weather_history(args.lat, args.lon, args.start, args.end)
    pd.set_option('display.max_columns', None)

    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)

    print(weather_history.head())
    print(weather_history.tail())

    # date = weather_history["date"].tolist()
    # plot_features_evolution(weather_history, all_hourly_features, date)
    print_statistics(weather_history, all_hourly_features)

    weather_history = prepare_data(weather_history, hourly_discrete_features)

    hourly_model = ProphetWeatherPredictionModel(weather_history, DataFrameType.Hourly, hourly_regressors)

    #print(hourly_model.validate())

    forecast = hourly_model.predict(24, weather_history["ds"].max(), 1000)
    print("Forecast:")
    print(forecast)

    print(ProphetWeatherPredictionModel.test(24, weather_history, DataFrameType.Hourly, hourly_regressors, 1000))

if __name__ == "__main__":
    main()
