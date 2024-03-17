from dataclasses import dataclass
import random
from src.Node import Node
from src.Attributes import Attribute, ATTRIBUTES_FOR_MODEL


@dataclass
class DecisionTree:
    _root: Node = None


    @staticmethod
    def choose_attributes(attrib_num: int) -> int:
        """Select attrib_num random attributes to build tree"""
        attributes = [attribute for attribute in ATTRIBUTES_FOR_MODEL]
        return random.sample(attributes, attrib_num)


    def print(self) -> None:
        self._root.print()


    def build(self, data: list, attrib_number: int, depth: int, min_samples_leaf: int) -> None:
        """Build a regression tree based on given data"""
        self._root = Node()
        attributes = DecisionTree.choose_attributes(attrib_number)
        self._root.build(attributes, data, depth, min_samples_leaf)


    def regress(self, example: list[str]) -> int:
        """Predict an output value"""
        return self._root.regress(example)
