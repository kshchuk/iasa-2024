import pandas as pd
from prophet import Prophet


class ProphetDailyModel:
    """
    Prophet model.
    """

    def __init__(self):
        self._model = Prophet()

    def fit(self, df: pd.DataFrame):
        """
        Fit Prophet model.

        :param df: (pd.DataFrame) Dataframe with the
        :return: (Prophet) Prophet model.
        """
        pass


    def predict(self, model: Prophet, periods: int) -> pd.DataFrame:
        """
        Predict using Prophet model.

        :param model: (Prophet) Prophet model.
        :param periods: (int) Number of periods to predict.
        :return: (pd.DataFrame) Dataframe with predictions.
        """
        pass

