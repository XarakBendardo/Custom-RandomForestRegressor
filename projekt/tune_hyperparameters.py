import random
from src.DataProcessor import DataProcessor
from src.Attributes import Attribute
from src.RandomForest import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
from src.utilities import get_results_path


def create_combinations() -> list:
    # PARAMETERS

    def_trees_numb = 50
    def_max_depth = 10
    def_attribs_in_tree = 29
    def_bootstrap_size = 0.3
    def_min_samples_leaf = 2

    trees_numb = [100, 150, 200, 300, 400]
    max_depth = [3, 5, 7, 20, 30, 100]
    attribs_in_tree = [5, 10, 15, 20]
    bootstrap_size = [0.1, 0.3, 0.6, 0.9]
    min_samples_leaf = [2, 5]  # min_samples_split fr

    combinations = [
        {
            "trees_numb": def_trees_numb,
            "max_depth": def_max_depth,
            "attribs_in_tree": def_attribs_in_tree,
            "bootstrap_size": def_bootstrap_size,
            "min_samples_leaf": def_min_samples_leaf,
        }
    ]
    combinations += [
        {
            "trees_numb": tn,
            "max_depth": def_max_depth,
            "attribs_in_tree": def_attribs_in_tree,
            "bootstrap_size": def_bootstrap_size,
            "min_samples_leaf": def_min_samples_leaf,
        }
        for tn in trees_numb
    ]
    combinations += [
        {
            "trees_numb": def_trees_numb,
            "max_depth": md,
            "attribs_in_tree": def_attribs_in_tree,
            "bootstrap_size": def_bootstrap_size,
            "min_samples_leaf": def_min_samples_leaf,
        }
        for md in max_depth
    ]
    combinations += [
        {
            "trees_numb": def_trees_numb,
            "max_depth": def_max_depth,
            "attribs_in_tree": at,
            "bootstrap_size": def_bootstrap_size,
            "min_samples_leaf": def_min_samples_leaf,
        }
        for at in attribs_in_tree
    ]
    combinations += [
        {
            "trees_numb": def_trees_numb,
            "max_depth": def_max_depth,
            "attribs_in_tree": def_attribs_in_tree,
            "bootstrap_size": bs,
            "min_samples_leaf": def_min_samples_leaf,
        }
        for bs in bootstrap_size
    ]
    combinations += [
        {
            "trees_numb": def_trees_numb,
            "max_depth": def_max_depth,
            "attribs_in_tree": def_attribs_in_tree,
            "bootstrap_size": def_bootstrap_size,
            "min_samples_leaf": msl,
        }
        for msl in min_samples_leaf
    ]
    return combinations


def check_hyperparameters(
    train: list, val: list, test: list, trees_numb: int, max_depth: int, attribs_in_tree: int, bootstrap_size: float, min_samples_leaf: int
) -> dict:
    f = RandomForestRegressor()
    f.fit(
        data=train,
        trees_numb=trees_numb,
        max_depth=max_depth,
        attribs_in_tree=attribs_in_tree,
        bootstrap_size=bootstrap_size,
        min_samples_leaf=min_samples_leaf,
    )

    results = {}

    for data_set, name in [(train, "train"), (val, "val"), (test, "test")]:
        y_predicted = []
        y = []

        for e in data_set:
            e_copy = e.copy()
            e_copy.pop(Attribute.RENT.value)
            pred = f.regress(e_copy)
            y_predicted.append(pred)
            y.append(e[Attribute.RENT.value])

        r2 = r2_score(y, y_predicted)
        mae = mean_absolute_error(y, y_predicted)
        results[name] = {"r2": r2, "mae": mae}
    return results


def main():
    DataProcessor.get_transformed_data_from_file()
    test, train = DataProcessor.split_set(test_size=0.3)
    random.shuffle(test)
    test = test[: (len(test) // 3)]
    val = test[(len(test) // 3) :]

    results_list = []
    combinations = create_combinations()

    for i, comb in enumerate(combinations):
        print(f"{i+1} out of {len(combinations)} combinations")
        results = {}
        results["params"] = comb
        results["results"] = check_hyperparameters(train, val, test, **comb)
        print(results["results"])
        results_list.append(results)

    results_list.sort(key=lambda x: x["results"]["val"]["mae"])

    df = pd.DataFrame(results_list)

    with open(get_results_path(), "a") as f:
        df.to_json(f, orient="records", lines=True)


if __name__ == "__main__":
    main()
