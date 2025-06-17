# -*- coding: utf-8 -*-
#test_ArithmeticOperation.py
#-------------------------------
# Created By: Matthew Kastl
#----------------------------------
"""This file tests the ArithmeticOperation PPC 
 """ 
#----------------------------------
# 
#
import sys
sys.path.append('/app/backend')

import pytest
from math import isclose
from pandas import DataFrame
from PostProcessing.IPostProcessing import post_process_factory

# Numeric test data
first = [1.5, 2.5, 3.5, 4.5, 5.5]
second = [1, 2, 3, 4, 5]
addition = [2.5, 4.5, 6.5, 8.5, 10.5]
subtraction = [.5, .5, .5, .5, .5]
multiplication = [1.5, 5.0, 10.5, 18.0, 27.5]
division = [1.5, 1.25, 1.166666666667, 1.125, 1.1]
modulo = [.5, .5, .5, .5, .5]

# Fake dataframe hydrated with fake data
test_df = DataFrame()
test_df['first'] = first
test_df['second'] = second

@pytest.mark.parametrize("test_df, operation, expected_results", [
    (test_df, 'addition', addition),
    (test_df, 'subtraction', subtraction),
    (test_df, 'multiplication', multiplication),
    (test_df, 'division', division),
    (test_df, 'modulo', modulo),
])
def test_post_process_data(test_df: DataFrame, operation: str, expected_results: list[float]):
    """This function tests the post process method in the Arithmetic Operation post process class.
    """

    call = "ArithmeticOperation"
    kwargs = {
        "op": operation,
        "left_col_key": "first",
        "right_col_key": "second",
        "out_col_key": "result"   
    }

    # Call the factory to get the resolver and pass it the fake input data and the post process call
    test_df = post_process_factory(test_df, call, kwargs)

    # Unpack the resulting components
    result = test_df['result'].tolist()

    # Iterate through the resulting components checking if they were calculated correctly
    for actual, expected in zip(result, expected_results):
        tolerance = 1e-5
        if not isclose(actual, expected, abs_tol=tolerance):
            assert False
    assert True
