import random
from src.Attributes import ATTRIBUTES_FOR_MODEL, Attribute
from src.utilities import average
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor as rfsklearn
import pickle
import os
from copy import deepcopy

SAVE_DIR = os.path.join(os.path.dirname(__file__), "save")


def main():
    with open(f"{SAVE_DIR}/model.pkl", "rb") as file:
        model = pickle.load(file)

    with open(f"{SAVE_DIR}/test_data.pkl", "rb") as file:
        test = pickle.load(file)

    y_test_predicted = []
    y_test = []

    length = len(test)
    for i, e in enumerate(test):
        rent = e.pop(Attribute.RENT.value)
        pred = model.regress(e)
        y_test_predicted.append(pred)
        y_test.append(rent)
        print(f"Calculating TEST mae {int(100*((i + 1)/length))}%", end="\r")

    data = deepcopy(model.get_data())

    X_train = []
    y_train = []
    for e in data:
        rent = e.pop(Attribute.RENT.value)
        X_train.append(e)
        y_train.append(rent)

    sklearn_model = rfsklearn(n_estimators=300)
    sklearn_model.fit(X_train, y_train)
    sklearn_predicted = sklearn_model.predict(test)
    sklearn_train_predicted = sklearn_model.predict(X_train)

    y_train_predicted = []
    length = len(X_train)
    for i, e in enumerate(X_train):
        pred = model.regress(e)
        y_train_predicted.append(pred)
        print(f"Calculating TRAIN mae {int(100*((i + 1)/length))}%", end="\r")

    os.system("clear")

    print("\nCustom model:")
    r2 = r2_score(y_test, y_test_predicted)
    print("Calculated TEST R^2 score:", r2)
    mae = mean_absolute_error(y_test, y_test_predicted)
    print("Calculated TEST MAE:", mae)

    r2 = r2_score(y_train, y_train_predicted)
    print("Calculated TRAIN R^2 score:", r2)
    mae = mean_absolute_error(y_train, y_train_predicted)
    print("Calculated TRAIN MAE:", mae)

    print("\nSklearn model:")
    r2 = r2_score(y_test, sklearn_predicted)
    print("Calculated TEST R^2 score:", r2)
    mae = mean_absolute_error(y_test, sklearn_predicted)
    print("Calculated TEST MAE:", mae)

    r2 = r2_score(y_train, sklearn_train_predicted)
    print("Calculated TRAIN R^2 score:", r2)
    mae = mean_absolute_error(y_train, sklearn_train_predicted)
    print("Calculated TRAIN MAE:", mae)

if __name__ == "__main__":
    main()