#!/usr/bin/env python3
"""Complex types - mixed list """
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
     a type-annotated function sum_mixed_list which takes a
     list mxd_lst of integers and floats and
     returns their sum as a float
    """
    converted_list = [float(ele) for ele in mxd_lst]
    return sum(converted_list)
