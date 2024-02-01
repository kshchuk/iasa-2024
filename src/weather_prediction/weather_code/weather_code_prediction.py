from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pandas as pd


class WeatherCodesPredictor:
    @staticmethod
    def get_weather_codes(historical_data_json: str,
                          to_predict: pd.DataFrame,
                          include_regressors: list,
                          codes_column='weather_code',
                          include_regressors_predict=None):
        """

        :param historical_data_json: historical weather data from api (as json string)
        :param to_predict: dataframe of weather forecast, for which weather codes have to be predicted
        :param include_regressors: list of regressors to use in the model (extracted from historical data)
        :param codes_column: (default='weather_code') name of the column with weather codes (historical data)
        :param include_regressors_predict (default=None) regressors to use in prediction.
        If None, include_regressors will be used
        :return: list of weather types in order that matches to_predict dataframe
        """
        df = pd.read_json(historical_data_json)
        return WeatherCodesPredictor._predict(df, to_predict, include_regressors, codes_column,
                                              include_regressors_predict)

    @staticmethod
    def get_weather_codes_frame(historical_data_frame, to_predict, include_regressors, codes_column='weather_code',
                                include_regressors_predict=None):
        """

                :param historical_data_frame: historical weather data from api (as dataframe)
                :param to_predict: dataframe of weather forecast, for which weather codes have to be predicted
                :param include_regressors: list of regressors to use in the model (extracted from historical data)
                :param codes_column: (default='weather_code') name of the column with weather codes (historical data)
                :param include_regressors_predict (default=None) regressors to use in prediction.
                If None, include_regressors will be used
                :return: list of weather types in order that matches to_predict dataframe
                """
        return WeatherCodesPredictor._predict(historical_data_frame, to_predict, include_regressors,
                                              codes_column, include_regressors_predict)

    @staticmethod
    def _predict(df, to_predict, include_regressors, codes_column, include_regressors_predict):
        if not include_regressors_predict:
            include_regressors_predict = include_regressors
        x_train = df[include_regressors]
        x_predict = to_predict[include_regressors_predict]
        y = df[codes_column]

        y = WeatherCodesPredictor.replace_weather_codes(y)

        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_train)
        x_predict_scaled = scaler.transform(x_predict)

        model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
        model.fit(x_train_scaled, y)

        return model.predict(x_predict_scaled)

    @staticmethod
    def replace_weather_codes(y):
        """
        Substitutes similar weather types with one general type (e.g. "Light rain", "Heavy rain" -> "Rain")
        Weather codes definition: https://open-meteo.com/en/docs
        :param y: Sequence of weather codes
        :return: Normalized weather codes
        """
        replacements ={
            0: 'clear',
            1: 'cloudy',
            2: 'cloudy',
            3: 'cloudy',
            45: 'foggy',
            48: 'foggy',
            51: 'drizzle',
            53: 'drizzle',
            55: 'drizzle',
            56: 'drizzle',
            57: 'drizzle',
            61: 'rain',
            63: 'rain',
            65: 'rain',
            66: 'rain',
            67: 'rain',
            71: 'snow',
            73: 'snow',
            75: 'snow',
            77: 'snow',
            80: 'rain showers',
            81: 'rain showers',
            82: 'rain showers',
            85: 'snow showers',
            86: 'snow showers',
            95: 'thunderstorm',
            96: 'thunderstorm',
            99: 'thunderstorm',
        }

        replace_dict = {
            2: 1,
            3: 1,
            45: 48,
            53: 51,
            55: 51,
            56: 51,
            57: 51,
            63: 61,
            65: 61,
            66: 61,
            67: 61,
            73: 71,
            75: 71,
            81: 80,
            82: 80,
            85: 86,
            96: 95,
            99: 95
        }
        y_mapped = y.map(replacements).fillna('unknown')
        return y_mapped.astype(str)

