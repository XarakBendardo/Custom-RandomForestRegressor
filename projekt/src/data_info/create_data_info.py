"""
Script for checking some information of the data like minimum and maximum values of the columns or number of unique values in the columns.
"""

import pandas as pd

try:
    data = pd.read_csv("data.csv", sep=",")
except FileNotFoundError:
    try:
        data = pd.read_csv("resources/data.csv", sep=",")
    except FileNotFoundError:
        data = pd.read_csv("../resources/data.csv", sep=",")


print(f"Number of rows: {len(data)}\n")

for column in data.columns[1:]:
    print(f"{column} description:")
    print(data[column].describe())
    print(f"null values: {data[column].isnull().sum()}")
    print(f"empty values: {len(data[data[column] == ''])}")
    if column in [
        "Area Type",
        "City",
        "Furnishing Status",
        "Tenant Preferred",
        "Point of Contact",
    ]:
        print(f"unique values: {data[column].unique()}")
    print("")
