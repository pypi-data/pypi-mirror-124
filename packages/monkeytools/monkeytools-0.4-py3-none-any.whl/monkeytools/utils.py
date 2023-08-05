"""
A collection of utility functions that are used throughout the package.
"""

def check_array(given_array):
    """Check that `given_array` is a list and contains only numeric values."""

    if not isinstance(given_array, list):
        raise TypeError("`given_array` must be a list")

    if not all(isinstance(x, (int, float)) for x in given_array):
        raise TypeError(
            "`given_array` contains non-numeric values. "
            "All items must be either integers or floats."
            )