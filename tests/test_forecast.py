from forecast.forecast import WeatherForecast


def test_weather_forecast():
    user_input = {
        "lon": 50.42,
        "lat": 30.54,
        "type": 'Daily',
        "from": "2020-01-01",
        "to": "2020-01-07"
    }

    weather_forecast = WeatherForecast()
    result = weather_forecast.predict(user_input)
    assert result
