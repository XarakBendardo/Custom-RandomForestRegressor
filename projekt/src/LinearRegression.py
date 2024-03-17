from src.Attributes import Attribute
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np


class LinearRegressionModel:
    def __init__(self, data: list):
        self._selected_columns = [
            Attribute.MILEAGE.value,
            Attribute.REG_YEAR.value,
            Attribute.PREV_OWNERS.value,
        ]
        self.model = LinearRegression()
        self._prepare_data(data)
        self._train_model()

    def _prepare_data(self, data: list) -> None:
        all_data = pd.DataFrame(data)
        self.to_predict = all_data[all_data[Attribute.PREV_OWNERS.value].isnull()]
        data_to_learn = all_data[all_data[Attribute.PREV_OWNERS.value].notnull()]
        data_to_learn = data_to_learn[self._selected_columns]
        self.train_data, self.test_data = train_test_split(
            data_to_learn, test_size=0.1, random_state=42
        )

    def _train_model(self) -> None:
        self.model.fit(
            self.train_data.drop(columns=[Attribute.PREV_OWNERS.value]),
            self.train_data[Attribute.PREV_OWNERS.value],
        )

    def predict(self) -> list:
        to_predict = self.to_predict[self._selected_columns]
        to_predict = to_predict.drop(columns=[Attribute.PREV_OWNERS.value])
        predicted = self.model.predict(to_predict)
        return np.round(predicted).astype(int)

    def predict_example(self, example: list) -> int:
        return self.model.predict([example]).astype(int)[0]

    def evaluate(self) -> float:
        y_true = self.test_data[Attribute.PREV_OWNERS.value]
        y_predict = self.model.predict(
            self.test_data.drop(columns=[Attribute.PREV_OWNERS.value])
        )
        mse = mean_squared_error(y_true, y_predict)
        return mse

    def compare_with_random(self) -> str:
        mse_model = self.evaluate()
        y_random = np.random.randint(1, 5, size=len(self.test_data))
        mse = mean_squared_error(self.test_data[Attribute.PREV_OWNERS.value], y_random)
        return f"Model MSE: {mse_model}\nRandom MSE: {mse}"
