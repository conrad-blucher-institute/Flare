# -*- coding: utf-8 -*-
#test_SummaryStatistics.py
#-------------------------------
# Created By: Anointiyae Beasley
#----------------------------------
"""This file tests the SummaryStatistics post-processing class.
"""
#----------------------------------
#
import sys
sys.path.append('/app/backend')

import pytest
from pandas import DataFrame
from PostProcessing.IPostProcessing import post_process_factory

# Fake dataframe 
test_df = DataFrame()
test_df['col1'] = [1, 2, 3, 4, 5]
test_df['col2'] = [10, 20, 30, 40, 50]
test_df['col3'] = [7, 8, 9, 10, 11]

# Expected values
expected_summary = {
    "median": {'col1': 3.0, 'col2': 30.0, 'col3': 9.0},
    "max": {'col1': 5, 'col2': 50, 'col3': 11},
    "mean": {'col1': 3.0, 'col2': 30.0, 'col3': 9.0}
}

@pytest.mark.parametrize("stat_key", ["median", "max", "mean"])
def test_summary_statistics(stat_key: str):
    """This function tests the post process method in the SummaryStatistics post process class.
    """

    call = "SummaryStatistics"
    kwargs = {}  # No args needed for this one

    # Run post process
    result_df = post_process_factory(test_df, call, kwargs)

    # Compare each column's value to expected value
    for col in expected_summary[stat_key]:
        actual = result_df.loc[stat_key, col]
        expected = expected_summary[stat_key][col]
        tolerance = 1e-5
        assert abs(actual - expected) < tolerance
