def condition_equal(example: list[str], attribute: int, value: str) -> bool:
    return example[attribute] == value


def condition_smaller(example: list[str], attribute: int, value: str) -> bool:
    return example[attribute] < value


def condition_smaller_or_equal(example: list[str], attribute: int, value: str) -> bool:
    return example[attribute] <= value


def condition_greater(example: list[str], attribute: int, value: str) -> bool:
    return example[attribute] > value


def condition_greater_or_equal(example: list[str], attribute: int, value: str) -> bool:
    return example[attribute] >= value