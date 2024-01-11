#!/usr/bin/env python3
"""Complex types - list of floats"""


def sum_list(input_list: list[float]) -> float:
    """ a type-annotated function sum_list which takes a list
    input_list of floats as argument and returns their sum as a float.
    """
    total_sum: float = 0
    for num in input_list:
        total_sum += num
    return total_sum