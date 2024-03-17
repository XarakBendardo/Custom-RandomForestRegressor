from dataclasses import dataclass
import random
from copy import deepcopy
import numpy as np
from src.DecisionTree import DecisionTree
from src.utilities import average
from sklearn.metrics import mean_squared_error


@dataclass
class RandomForestRegressor:
    _data: list = None
    _trees: list[DecisionTree] = None

    def fit(
        self,
        data: list,
        trees_numb: int = 50,
        max_depth: int = 10,
        attribs_in_tree: int = 4,
        bootstrap_size: float = 0.1,
        min_samples_leaf: int = 5,
        ranges_numb: int = 5,
    ) -> None:
        self._data = deepcopy(data)
        n_trees = 0
        self._trees = []
        bootstrap_size = int(len(self._data) * bootstrap_size)
        while n_trees < trees_numb:
            # batch = random.sample(data, k=bootstrap_size)
            batch = self._get_batch(bootstrap_size, ranges_numb)
            tree = DecisionTree()
            tree.build(batch, attribs_in_tree, max_depth, min_samples_leaf)
            self._trees.append(tree)
            n_trees += 1
            print(f"Progress: {round((n_trees*100)/trees_numb)} % trees trained", end="\r")

    def _get_batch(self, size: int, ranges_numb: int) -> list:
        batch = []
        if len(self._trees) == 0:
            batch = random.sample(self._data, k=size)
        else:
            regressed = []
            for example in self._data:
                regressed.append([example, self.regress(example)])
            regressed.sort(key=lambda x: mean_squared_error([x[0][0]], [x[1]]), reverse=True)
            rank_size = len(regressed) // ranges_numb
            for i in range(len(regressed)):
                regressed[i].append(i // rank_size)
            while len(batch) < size:
                x1_ind, x2_ind = np.random.choice(len(regressed), size=2, replace=False)
                x1 = regressed[x1_ind]
                x2 = regressed[x2_ind]
                if x1[2] < x2[2]:
                    batch.append(x1[0])
                    regressed.pop(x1_ind)
                elif x1[2] > x2[2]:
                    batch.append(x2[0])
                    regressed.pop(x2_ind)
                else:
                    x_added = random.choice([x2, x1])
                    batch.append(x_added[0])
                    regressed.remove(x_added)
        return batch

    def regress(self, example: list) -> int:
        return int(average([tree.regress(example) for tree in self._trees]))

    def get_trees(self) -> list:
        return self._trees

    def get_data(self) -> list:
        return self._data