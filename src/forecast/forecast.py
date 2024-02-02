from weather_prediction.weather_predictor import WeatherPredictor
from weather_prediction.weather_code.weather_code_prediction import WeatherCodesPredictor
import datetime


class WeatherForecast:
    def __init__(self):
        self.weather_predictor = WeatherPredictor()
        self.weather_code_predictor = WeatherCodesPredictor()

    def predict(self, user_input):
        is_hourly = user_input['type'] == 'Hourly'
        lon = user_input['lon']
        lat = user_input['lan']
        start_date = user_input['from']
        days