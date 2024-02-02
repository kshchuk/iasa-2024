from weather_prediction.weather_predictor import WeatherPredictor
from weather_prediction.weather_code.weather_code_prediction import WeatherCodesPredictor
import datetime


class WeatherForecast:
    def __init__(self):
        self.weather_predictor = WeatherPredictor()
        self.weather_code_predictor = WeatherCodesPredictor()

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
            prediction = (self.weather_predictor.
                          predict_weather(lat, lon, start_date_str, days=0, hours=distance_days*24))["HOURLY_PREDICTION"]
        else:
            prediction = (self.weather_predictor.
                          predict_weather(lat, lon, start_date_str, days=distance_days,hours=0))["DAILY_PREDICTION"]
        prediction['weather_code'] = 'cloudy'
        return prediction

    def _transform_date(self, date_str):
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()