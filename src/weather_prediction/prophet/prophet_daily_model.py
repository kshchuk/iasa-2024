import pandas as pd
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
        Train and validate the Prophet model.

        :param df: (pd.DataFrame) train set.
        :return: (float) MAE value.
        """
        df = df.rename(columns={"date": "ds", "temperature_2m_mean": "y"})
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

        if debugger_is_active():
            df_cv = None
            if df.shape[0] > 1000:
                df_cv = cross_validation(self._model, initial="1000 days", horizon="7 days")
            elif df.shape[0] > 100:
                df_cv = cross_validation(self._model, initial="100 days", horizon="7 days")
            elif df.shape[0] > 10:
                df_cv = cross_validation(self._model, initial="10 days", horizon="1 day")
            if df_cv is not None:
                df_p = performance_metrics(df_cv)
                print(df_p)

    def predict(self, periods: int) -> pd.DataFrame:
        """
        Predict using Prophet model.

        :param periods: (int) Number of periods to predict.
        :return: (pd.DataFrame) Dataframe with predictions.
        """
        future = self._model.make_future_dataframe(periods=periods)
        forecast = self._model.predict(future)
        return forecast


