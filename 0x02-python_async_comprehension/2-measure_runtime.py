#!/usr/bin/env python3
""" module for the coroutine measure_runtime """

from asyncio import gather
from time import perf_counter

async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime() -> float:
    """
    coroutine that will execute async_comprehension four times
    in parallel using asyncio.gather.
    measure_runtime should measure the total runtime and return it.
    """
    start = perf_counter()
    await gather(*(async_comprehension() for _ in range(4)))
    return perf_counter() - start
