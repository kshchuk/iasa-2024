import argparse
import requests_cache
from pandas import DataFrame
from retry_requests import retry
import pandas as pd
import openmeteo_requests

from src.utils.analyses_utils import plot_features_evolution
from src.utils.analyses_utils import print_statistics


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
                      "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean",
                      "daylight_duration", "sunshine_duration", "precipitation_sum", "rain_sum",
                      "snowfall_sum", "precipitation_hours", "wind_speed_10m_max", "wind_gusts_10m_max",
                      "wind_direction_10m_dominant"]
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
        daily_apparent_temperature_max = daily.Variables(4).ValuesAsNumpy()
        daily_apparent_temperature_min = daily.Variables(5).ValuesAsNumpy()
        daily_apparent_temperature_mean = daily.Variables(6).ValuesAsNumpy()
        daily_daylight_duration = daily.Variables(7).ValuesAsNumpy()
        daily_sunshine_duration = daily.Variables(8).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(9).ValuesAsNumpy()
        daily_rain_sum = daily.Variables(10).ValuesAsNumpy()
        daily_snowfall_sum = daily.Variables(11).ValuesAsNumpy()
        daily_precipitation_hours = daily.Variables(12).ValuesAsNumpy()
        daily_wind_speed_10m_max = daily.Variables(13).ValuesAsNumpy()
        daily_wind_gusts_10m_max = daily.Variables(14).ValuesAsNumpy()
        daily_wind_direction_10m_dominant = daily.Variables(15).ValuesAsNumpy()

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
        daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
        daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
        daily_data["apparent_temperature_mean"] = daily_apparent_temperature_mean
        daily_data["daylight_duration"] = daily_daylight_duration
        daily_data["sunshine_duration"] = daily_sunshine_duration
        daily_data["precipitation_sum"] = daily_precipitation_sum
        daily_data["rain_sum"] = daily_rain_sum
        daily_data["snowfall_sum"] = daily_snowfall_sum
        daily_data["precipitation_hours"] = daily_precipitation_hours
        daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
        daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
        daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

        daily_dataframe = pd.DataFrame(data=daily_data)
        return daily_dataframe

    def get_hourly_data(self, lat: float, lon: float, start: str, end: str) -> DataFrame:
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
            "latitude": 52.52,
            "longitude": 13.41,
            "start_date": "2024-01-12",
            "end_date": "2024-01-26",
            "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature",
                       "precipitation", "rain", "snowfall", "snow_depth", "weather_code", "pressure_msl",
                       "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high",
                       "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_speed_10m", "wind_speed_100m",
                       "wind_direction_10m", "wind_direction_100m", "wind_gusts_10m"]
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
        hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
        hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
        hourly_rain = hourly.Variables(5).ValuesAsNumpy()
        hourly_snowfall = hourly.Variables(6).ValuesAsNumpy()
        hourly_snow_depth = hourly.Variables(7).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(8).ValuesAsNumpy()
        hourly_pressure_msl = hourly.Variables(9).ValuesAsNumpy()
        hourly_surface_pressure = hourly.Variables(10).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(11).ValuesAsNumpy()
        hourly_cloud_cover_low = hourly.Variables(12).ValuesAsNumpy()
        hourly_cloud_cover_mid = hourly.Variables(13).ValuesAsNumpy()
        hourly_cloud_cover_high = hourly.Variables(14).ValuesAsNumpy()
        hourly_et0_fao_evapotranspiration = hourly.Variables(15).ValuesAsNumpy()
        hourly_vapour_pressure_deficit = hourly.Variables(16).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(17).ValuesAsNumpy()
        hourly_wind_speed_100m = hourly.Variables(18).ValuesAsNumpy()
        hourly_wind_direction_10m = hourly.Variables(19).ValuesAsNumpy()
        hourly_wind_direction_100m = hourly.Variables(20).ValuesAsNumpy()
        hourly_wind_gusts_10m = hourly.Variables(21).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
        hourly_data["dew_point_2m"] = hourly_dew_point_2m
        hourly_data["apparent_temperature"] = hourly_apparent_temperature
        hourly_data["precipitation"] = hourly_precipitation
        hourly_data["rain"] = hourly_rain
        hourly_data["snowfall"] = hourly_snowfall
        hourly_data["snow_depth"] = hourly_snow_depth
        hourly_data["weather_code"] = hourly_weather_code
        hourly_data["pressure_msl"] = hourly_pressure_msl
        hourly_data["surface_pressure"] = hourly_surface_pressure
        hourly_data["cloud_cover"] = hourly_cloud_cover
        hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
        hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
        hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
        hourly_data["et0_fao_evapotranspiration"] = hourly_et0_fao_evapotranspiration
        hourly_data["vapour_pressure_deficit"] = hourly_vapour_pressure_deficit
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["wind_speed_100m"] = hourly_wind_speed_100m
        hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
        hourly_data["wind_direction_100m"] = hourly_wind_direction_100m
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
        required=False, dest="start", default="2021-01-12"
    )
    parser.add_argument(
        "--end", help="End time (ISO 8601) ",
        required=False, dest="end", default="2024-01-26"
    )

    args = parser.parse_args()

    api_client = ApiClient()
    weather_history = api_client.get_daily_weather_history(args.lat, args.lon, args.start, args.end)
    pd.set_option('display.max_columns', None)

    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)

    print(weather_history.head())

    visualise_features = ["temperature_2m_mean", "apparent_temperature_mean", "sunshine_duration", "precipitation_sum",
                "precipitation_hours", "wind_speed_10m_max", "wind_direction_10m_dominant"]

    all_features = ["weather_code", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
                      "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean",
                      "daylight_duration", "sunshine_duration", "precipitation_sum", "rain_sum",
                      "snowfall_sum", "precipitation_hours", "wind_speed_10m_max", "wind_gusts_10m_max",
                      "wind_direction_10m_dominant"]

    date = weather_history["date"].tolist()
    plot_features_evolution(weather_history, all_features, date)
    print_statistics(weather_history, all_features)


if __name__ == "__main__":
    main()
