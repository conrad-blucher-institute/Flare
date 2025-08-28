# -*- coding: utf-8 -*-
# test_Combine.py
#-------------------------------
# Created By: Matthew Kastl
#----------------------------------
"""This file tests the Combine PPC 
 """ 
#----------------------------------
# 
#

import pytest
from math import isclose
from pandas import DataFrame, date_range, isna
from PostProcessing.IPostProcessing import post_process_factory
from numpy import nan

# Numeric test data

test_df = DataFrame({
        's1': [nan, nan, nan, nan, nan],
        's2': [1, 1, 1, 1, 1],
        's3': [2, 2, 2, nan, nan],
        's4': [nan, nan, nan, 3,3],
        's5': [4, 4, 4, 4, nan],
    },
    index= date_range('2023-01-01', periods=5)
)



@pytest.mark.parametrize("test_df, left, right, expected_results", [
    (test_df.copy(), 's1', 's2', [1, 1, 1, 1, 1]), # Tests left preference over nan
    (test_df.copy(), 's3', 's4', [2, 2, 2, 3, 3]), # Tests right choice when nan in left
    (test_df.copy(), 's3', 's2', [2, 2, 2, 1, 1]), # Tests right never chosen when left value
    (test_df.copy(), 's3', 's5', [2, 2, 2, 4, nan]), # Tests nan persisting if in left and right
])
def test_post_process_data(test_df: DataFrame, left: str, right: str, expected_results: list[any]):
    """This function tests the post process method in the Arithmetic Operation post process class.
    """

    key = "Combine"
    kwargs = {
        "left_col_key": left,
        "right_col_key": right,
    }

    # Call the factory to get the resolver and pass it the fake input data and the post process call
    test_df = post_process_factory(test_df, key, kwargs)

    # Unpack the resulting components
    result = test_df[left].tolist()

    # Iterate through the resulting components checking if they were calculated correctly
    for actual, expected in zip(result, expected_results):
        
        tolerance = 1e-5
        if isna(actual) and isna(expected):  # Protects against nan comparison.
            pass
        elif not isclose(actual, expected, abs_tol=tolerance):
            assert False
    assert True
