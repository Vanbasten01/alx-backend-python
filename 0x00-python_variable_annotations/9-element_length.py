#!/usr/bin/env python3
"""Let's duck type an iterable object """
from typing import Iterable, List, Tuple, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Annotated the below function’s parameters and returned
    values with the appropriate types.
        def element_length(lst):
            return [(i, len(i)) for i in lst]
    """
    return [(i, len(i)) for i in lst]
