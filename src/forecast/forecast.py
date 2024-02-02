from weather_prediction.weather_predictor import WeatherPredictor
from weather_prediction.weather_code.weather_code_prediction import WeatherCodesPredictor
from utils.analyses_utils import DataFrameType
import datetime


class WeatherForecast:
    def __init__(self):
        self.weather_predictor = WeatherPredictor()
        self.weather_code_predictor = WeatherCodesPredictor()
        self.include_regressors_daily = ['temperature_2m_mean', 'wind_speed_10m_max',
                                         'precipitation_sum', 'precipitation_hours']

    def predict(self, user_input):
        if user_input['type'] == 'Hourly':
            is_hourly = True
        elif user_input['type'] == 'Daily':
            is_hourly = False
        else:
            raise ValueError("User input type is neither Hourly nor Daily!")
        lon = user_input['lon']
        lat = user_input['lat']
        start_date_str = user_input['from']
        end_date_str = user_input['to']

        start_date_obj = self._transform_date(start_date_str)
        end_date_obj = self._transform_date(end_date_str)

        if start_date_obj > end_date_obj:
            start_date_obj, end_date_obj = end_date_obj, start_date_obj
            start_date_str, end_date_str = end_date_str, start_date_str

        distance_days = (end_date_obj - start_date_obj).days
        if is_hourly:
            return self._get_for_hours(lat, lon, start_date_str, distance_days)
        else:
            return self._get_for_days(lat, lon, start_date_str, distance_days)

    def _transform_date(self, date_str):
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

    def _get_for_hours(self, lat, lon, start_date_str, distance_days):
        prediction_dict = (self.weather_predictor.
                           predict_weather(lat, lon, start_date_str
                                           , days=0, hours=distance_days * 24))
        history = prediction_dict[DataFrameType.HourlyHistory]
        prediction = prediction_dict[DataFrameType.HourlyPrediction]
        weather_codes = self.weather_code_predictor.get_weather_codes_frame(
            history, prediction, self.include_regressors_daily
        )
        prediction['weather_code']=weather_codes
        actual_data = self.weather_predictor.get_actual_data(lat, lon, start_date_str, days=0, hours=distance_days*24)

        return prediction, actual_data[DataFrameType.HourlyHistory]

    def _get_for_days(self, lat, lon, start_date_str, distance_days):
        actual_data = self.weather_predictor.get_actual_data(lat, lon, start_date_str, days=distance_days, hours=0)
        prediction_dict = (self.weather_predictor.
                           predict_weather(lat, lon, start_date_str,
                                           days=distance_days, hours=0))
        history = prediction_dict[DataFrameType.DailyHistory.value]
        prediction = prediction_dict[DataFrameType.DailyPrediction.value]
        weather_codes = self.weather_code_predictor.get_weather_codes_frame(
            history, prediction, self.include_regressors_daily
        )
        prediction['weather_code'] = weather_codes
        print('WITH WEATHER CODES', len(prediction))
        actual_daily = actual_data[DataFrameType.DailyHistory.value]
        return prediction, actual_daily