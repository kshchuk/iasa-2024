from weather_prediction.weather_code.weather_code_prediction import WeatherCodesPredictor
import pandas as pd
from utils.path_utils import ParentPath
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def test_weather_code():
    base_dir = ParentPath().config_path
    filepath = f"{base_dir}/" + "resource/test/kyiv_data.json"
    df = pd.read_json(filepath)
    x_history, x_predict = train_test_split(df)
    regressors = ['temperature_2m_mean', 'wind_speed_10m_max', 'precipitation_sum', 'precipitation_hours']
    predicted = WeatherCodesPredictor.get_weather_codes_frame(x_history, x_predict, regressors)
    expected = WeatherCodesPredictor.replace_weather_codes(x_predict['weather_code'])
    accuracy = accuracy_score(expected, predicted)
    assert accuracy > 0.5
