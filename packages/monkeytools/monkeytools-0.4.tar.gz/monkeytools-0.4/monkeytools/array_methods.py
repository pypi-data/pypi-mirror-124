"""
A collection of array-based algorithms
1. Find maximum sub-array
    - https://en.wikipedia.org/wiki/Maximum_subarray_problem

Author: Matthew R. DeVerna
"""
from .utils import check_array

def max_subarray_kadane(given_array):
    """
    Find a contiguous subarray with the largest sum.

    Note: This algorithm is implemented with Kadane's algorithm with a slight
        change (we do not add 1 to the best_end)
        - https://en.wikipedia.org/wiki/Maximum_subarray_problem#Kadane's_algorithm

    Complexity:
    ----------
    - O(n)

    Parameters:
    ----------
    - given_array (list) : a numerical sequence

    Returns:
    ----------
    - best_sum (int) : the total sum between `best_start` and `best_end`
    - best_start (int) : the first index in the largest sub-array (inclusive)
    - best_end (int) : the last index in the largest sub-array (inclusive)

    Exceptions:
    ----------
    - TypeError

    Example:
    ----------
    lst = [-45, -78, -2, -60, 27, 21, 71, 80, 22, 59]
    max_subarray(lst)

    # Output
    (280, 4, 10)

    Where 280 is the sum between lst[4] (27, inclusive) and lst[9] (59, inclusive)
    """
    # Ensure array is a list and contains only numeric values
    check_array(given_array)

    best_sum = float('-inf')
    best_start = best_end = None
    current_sum = 0
    for current_end, x in enumerate(given_array):
        if current_sum <= 0:
            # Start a new sequence at the current element
            current_start = current_end
            current_sum = x
        else:
            # Extend the existing sequence with the current element
            current_sum += x

        if current_sum > best_sum:
            best_sum = current_sum
            best_start = current_start
            best_end = current_end

    return best_sum, best_start, best_end