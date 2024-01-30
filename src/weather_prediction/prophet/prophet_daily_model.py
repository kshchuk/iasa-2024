import pandas as pd
from pandas import DataFrame
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics

from src.utils.path_utils import debugger_is_active


class ProphetDailyModel:
    """
    Prophet model.
    """

    def __init__(self):
        self._model = Prophet()

    def train(self, df: pd.DataFrame) -> None:
        """
        Train the Prophet model.

        :param df: (pd.DataFrame) train set.
        :return: (float) MAE value.
        """
        df = df.rename(columns={"date": "ds", "temperature_2m_mean": "y"})

        # TODO: parametrize
        self._model.add_regressor("weather_code")
        self._model.add_regressor("temperature_2m_max")
        self._model.add_regressor("temperature_2m_min")
        self._model.add_regressor("sunshine_duration")
        self._model.add_regressor("precipitation_sum")
        self._model.add_regressor("precipitation_hours")
        self._model.add_regressor("wind_speed_10m_max")
        self._model.add_regressor("wind_gusts_10m_max")
        self._model.add_regressor("wind_direction_10m_dominant")

        self._model.fit(df)

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate the Prophet model using cross validation.

        :param df: (pd.DataFrame) Dataframe with features.
        :return: (pd.DataFrame) Dataframe with validation metrics.
        """
        if df.shape[0] > 1000:
            df_cv = cross_validation(self._model, initial="1000 days", horizon="7 days")
        elif df.shape[0] > 100:
            df_cv = cross_validation(self._model, initial="100 days", horizon="7 days")
        elif df.shape[0] > 10:
            df_cv = cross_validation(self._model, initial="10 days", horizon="1 day")
        if df_cv is not None:
            df_p = performance_metrics(df_cv)
            return df_p

    def predict(self, periods: int, regressors: pd.DataFrame) -> pd.DataFrame:
        """
        Predict using Prophet model.

        :param periods: (int) Number of periods to predict.
        :param regressors: (pd.DataFrame) Regressors for prediction.
        :return: (pd.DataFrame) Dataframe with predictions.
        """
        future = self._model.make_future_dataframe(periods=periods)
        future = pd.concat([future, regressors], axis=1)
        forecast = self._model.predict(future)
        return forecast
