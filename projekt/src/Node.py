from dataclasses import dataclass
from typing import Type
import numpy as np
from src.utilities import average
from src.Attributes import Attribute, AttributeType, ATTRIBUTE_TYPE
from src.conditions import condition_equal, condition_smaller_or_equal


@dataclass
class Node:
    attribute = None  # number of an attribute
    attribute_value: int = None
    _condition: callable = None
    _left_child: Type["Node"] = None
    _right_child: Type["Node"] = None
    is_leaf: bool = True
    _data: list = None

    @staticmethod
    def find_best_split(attributes: list[Attribute], data: list, min_samples_leaf: int) -> tuple:
        """Return attribute and value for the best split in data"""

        def get_nominal_split_values(attribute: Attribute, data: list):
            return list(set([exampl[attribute.value] for exampl in data]))  # all unique values of attribute

        def get_numeric_split_values(attribute: Attribute, data: list):
            unique_values = list(set([exmpl[attribute.value] for exmpl in data]))
            sorted_values = sorted(unique_values)
            split_values = [(sorted_values[i] + sorted_values[i + 1]) / 2 for i in range(len(sorted_values) - 1)]
            return split_values

        best = None
        best_varience_reduction = -float("inf")
        current_varience = np.var([exampl[Attribute.RENT.value] for exampl in data])
        for attrib in attributes:
            if ATTRIBUTE_TYPE.get(attrib) == AttributeType.NOMINAL:
                values = get_nominal_split_values(attrib, data)
                condition = condition_equal
            else:
                values = get_numeric_split_values(attrib, data)
                condition = condition_smaller_or_equal
            for value in values:
                left_data, right_data = Node._split_data(condition, attrib, value, data)
                if len(left_data) < min_samples_leaf or len(right_data) < min_samples_leaf:
                    continue
                left_varience = np.var([exampl[Attribute.RENT.value] for exampl in left_data]) * len(left_data) / len(data)
                right_varience = np.var([exampl[Attribute.RENT.value] for exampl in right_data]) * len(right_data) / len(data)
                varience_reduction = current_varience - (left_varience + right_varience)
                if varience_reduction > best_varience_reduction:
                    best = (attrib, value)
                    best_varience_reduction = varience_reduction
        return best

    def print(self, depth: int = 0) -> None:
        padding = "\t" * depth
        if self.is_leaf:
            print(f"{padding}Leaf containing {len(self._data)} elements")
        else:
            print(f"{padding}Node: attribute: {self.attribute}, value: {self.attribute_value}")
            self.left_child.print(depth + 1)
            self.right_child.print(depth + 1)

    @staticmethod
    def _split_data(condition: callable, attribute, attribute_value, data: list) -> tuple:
        """Split given data due to given condition. Returns: data that meet given condition, data that don't meet the condition."""
        left_child_data = []
        right_child_data = []
        for example in data:
            if condition(example, attribute.value, attribute_value):
                left_child_data.append(example)
            else:
                right_child_data.append(example)
        return left_child_data, right_child_data

    def get_values(self) -> list:
        return [exampl[Attribute.RENT] for exampl in self._data]

    def regress(self, example) -> int:
        """If the node is a leaf, then return approximate value. If not we go down the tree with the example."""
        if self.is_leaf:
            # print(f"in leaf, values: {[exampl[Attribute.RENT.value] for exampl in self._data]}")
            return average([exmpl[Attribute.RENT.value] for exmpl in self._data])
        # print(f"split condition: {self.attribute} {self._condition.__name__} {self.attribute_value}")
        attribute_num = self.attribute.value if self.attribute.value < Attribute.RENT.value else self.attribute.value - 1
        if self._condition(example, attribute_num, self.attribute_value):
            # print(f"going left")
            return self.left_child.regress(example)
        else:
            # print(f"going right")
            return self.right_child.regress(example)

    def _make_leaf(self, data: list) -> None:
        self._data = data

    def build(self, attributes: list, data: list, depth: int, min_samples_leaf) -> None:
        # end of the tree - current node is a leaf
        if depth == 0:
            return self._make_leaf(data)

        if len(data) < min_samples_leaf:
            return self._make_leaf(data)

        best = Node.find_best_split(attributes, data, min_samples_leaf)
        if best is None:
            """The only reason for that is that all the examples from given data have the same values on each given attribute.
            In that case we can't make a split and the current node has to be a leaf"""
            return self._make_leaf(data)
        self.attribute, self.attribute_value = best

        # get attribute and its value for the best split
        # set condition '=' for nominal attributes and '<=' for ordinal attributes
        if ATTRIBUTE_TYPE.get(self.attribute.value) == AttributeType.NOMINAL:
            self._condition = condition_equal
        else:
            self._condition = condition_smaller_or_equal

        left_child_data, right_child_data = Node._split_data(self._condition, self.attribute, self.attribute_value, data)
        if not left_child_data or not right_child_data:
            return self._make_leaf(data)
        # make a split
        self.is_leaf = False
        self.left_child = Node()
        self.left_child.build(attributes, left_child_data, depth - 1, min_samples_leaf)
        self.right_child = Node()
        self.right_child.build(attributes, right_child_data, depth - 1, min_samples_leaf)
