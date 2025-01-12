"""Times utilities."""
from typing import Callable
import time
from functools import wraps


def timeit(method: Callable) -> Callable:
    """This timeit function is a wrapper for performance analysis.

    Should return the time taken for a function to run,
    :param method: the function that it takes as an input
    :return: timed

    Example:
        Usage example::
            import src.time_wrapper as twr
            @twr.timeit

    """

    @wraps(method)
    def timed(*args, **kw) -> any:
        ts = time.perf_counter()
        result = method(*args, **kw)
        te = time.perf_counter()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = te - ts
        else:
            print("%r  %2.5f s\n" % (method.__name__, (te - ts)))
        return result

    return timed
