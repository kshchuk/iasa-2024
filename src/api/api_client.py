import argparse
import os
import requests_cache
from pandas import DataFrame
from retry_requests import retry
import pandas as pd
import openmeteo_requests

class ApiClient:
    """
    Api Client for OpenMeteo API.
    """
    def __init__(self):
        pass

    def get_weather_history(self, lat: float, lon: float, start: str, end: str) -> DataFrame:
        """
        Get weather history for specific location.

        :param lat: (float) Latitude.
        :param lon: (float) Longitude.
        :param start: (str) Start date ISO 8601, e.g. start=2024-01-12.
        :param end: (str) End date ISO 8601, e.g. end=2024-01-26.
        :return: (dict) Weather history.
        """
        cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": lat,
            "longitude": 13.41,
            "start_date": "2024-01-12",
            "end_date": "2024-01-26",
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
                      "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean", "sunrise",
                      "sunset", "daylight_duration", "sunshine_duration", "precipitation_sum", "rain_sum",
                      "snowfall_sum", "precipitation_hours", "wind_speed_10m_max", "wind_gusts_10m_max",
                      "wind_direction_10m_dominant"]
        }
        responses = openmeteo.weather_api(url, params=params)

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
        daily_sunrise = daily.Variables(7).ValuesAsNumpy()
        daily_sunset = daily.Variables(8).ValuesAsNumpy()
        daily_daylight_duration = daily.Variables(9).ValuesAsNumpy()
        daily_sunshine_duration = daily.Variables(10).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(11).ValuesAsNumpy()
        daily_rain_sum = daily.Variables(12).ValuesAsNumpy()
        daily_snowfall_sum = daily.Variables(13).ValuesAsNumpy()
        daily_precipitation_hours = daily.Variables(14).ValuesAsNumpy()
        daily_wind_speed_10m_max = daily.Variables(15).ValuesAsNumpy()
        daily_wind_gusts_10m_max = daily.Variables(16).ValuesAsNumpy()
        daily_wind_direction_10m_dominant = daily.Variables(17).ValuesAsNumpy()

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
        daily_data["sunrise"] = daily_sunrise
        daily_data["sunset"] = daily_sunset
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


def main():
    parser = argparse.ArgumentParser(description="Make Api Request")

    # default values are for Kyiv
    parser.add_argument(
        "--lat", help="Latitude", required=True, dest="lat", default=50.450001
    )
    parser.add_argument(
        "--lon", help="Longitude", required=True, dest="lon", default=30.523333
    )
    parser.add_argument(
        "--start", help="Start time (ISO 8601) ",
        required=True, dest="start", default="2024-01-12"
    )
    parser.add_argument(
        "--end", help="End time (ISO 8601) ",
        required=True, dest="end", default="2024-01-26"
    )

    args = parser.parse_args()

    api_client = ApiClient()
    weather_history = api_client.get_weather_history(args.lat, args.lon, args.start, args.end)

    print(weather_history)


if __name__ == "__main__":
    main()
