import os


def average(x: list) -> float:
    return sum(x) / len(x)


def get_data_path():
    absolute_path = os.path.dirname(__file__)
    relative_path = "../resources/data.csv"
    return os.path.join(absolute_path, relative_path)


def get_transformed_data_path():
    absolute_path = os.path.dirname(__file__)
    relative_path = "../resources/transformed_data.csv"
    return os.path.join(absolute_path, relative_path)


def get_results_path():
    absolute_path = os.path.dirname(__file__)
    relative_path = "../out/results.jsonl"
    return os.path.join(absolute_path, relative_path)
