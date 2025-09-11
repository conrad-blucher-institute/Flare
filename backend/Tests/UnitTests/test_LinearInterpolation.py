# -*- coding: utf-8 -*-
#test_LinearInterpolation.py
#-------------------------------
# Created By: Christian Quintero
# Last Updated: 08/29/2025
#----------------------------------
"""
This file tests the LinearInterpolation PPC 
""" 
#----------------------------------
# 
#

import pytest
import pandas as pd
import logging
from pandas import DataFrame, date_range
from numpy import nan
from datetime import datetime
from PostProcessing.IPostProcessing import post_process_factory

"""
The first section tests various NaN cases with the same interval as the index

index frequency is 1 hour (3600 seconds), and the interpolation interval is also set to 3600 seconds.
"""  

def test_real_scenario_NDFD():
    """
    This test uses some real NDFD data made from a CSV file.
    The timestamps start at 2025-09-15 01:00:00 and go up to 2025-09-15 13:00:00 with hourly frequency.
    We have a real value at 01:00 (29.0), 07:00 (28.0), and 13:00 (31.0).
    With 5 hours of NaNs between each gap.

    By subtracting the time difference between the real value after a nan gap, and the first nan in the gap,
    we can determine the nan gap duration. In this case, we have nans for 5 hours,
    hours 2-6 and hours 8-12. Since the limit is set to 5 hours (18000 seconds),
    we expect these 5 hour nan gaps to be interpolated.
    """
    test_data = [29.0, nan, nan, nan, nan, nan, 28.0, nan, nan, nan, nan, nan, 31.0]
    test_index = date_range(datetime(2025, 9, 15, 1, 0, 0), periods=13, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    expected_data = [29.0, 28.83333333, 28.66666667, 28.5, 28.33333333, 28.16666667, 28.0,
                     28.5, 29.0, 29.5, 30.0, 30.5, 31.0]
    expected_index = date_range(datetime(2025, 9, 15, 1, 0, 0), periods=13, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  # 1 hour
        "limit": 18000                   # 5 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)

def test_basic_interpolation():
    """
    This tests basic interpolation with a small limit for simplicity.
    """

    # the test index starts at 2025-01-01 00:00:00 and goes up to 2025-01-01 12:00:00 with hourly frequency.
    # We have real values at 00:00 (1.0), 04:00 (5.0), 07:00 (8.0), and 12:00 (13.0).
    # with nans from hours 1-3 (3 hours of nans) between hour 0 (1.0) and hour 4 (5.0),
    # hours 5-6 (2 hours of nans) between hour 4 (5.0) and hour 7 (8.0),
    # and hours 8-11 (4 hours of nans) between hour 7 (8.0) and hour 12 (13.0).
    test_data = [1.0, nan, nan, nan, 5.0, nan, nan, 8.0, nan, nan, nan, nan, 13.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # analysis
    # hours 1-3 (3 hours of nans) between hour 0 (1.0) and hour 4 (5.0), limit 3 hours -> interpolate
    # hours 5-6 (2 hours of nans) between hour 4 (5.0) and hour 7 (8.0), limit 3 hours -> interpolate
    # hours 8-11 (4 hours of nans) between hour 7 (8.0) and hour 12 (13.0), limit 3 hours -> do not interpolate
    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, nan, nan, nan, nan, 13.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  # 1 hour
        "limit": 10800                   # 3 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)

def test_start_end_nans():

    """
    This test ensure no interpolation happens when nans start or end the series.
    """

    test_data = [nan, nan, 3.0, nan, 5.0, nan, nan, nan, nan, 10.0, nan, nan, nan, 14.0, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=15, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # analysis
    # hours 0-1 (2 hours of nans) at start -> do not interpolate
    # hours 3 (1 hour of nans) between hour 2 (3.0) and hour 4 (5.0), limit 3 hours -> interpolate
    # hours 5-8 (4 hours of nans) between hour 4 (5.0) and hour 9 (10.0), limit 3 hours -> do not interpolate
    # hours 10-12 (3 hours of nans) between hour 9 (10.0) and hour 13 (14.0), limit 3 hours -> interpolate
    # hour 14 (1 hour of nans) at end -> do not interpolate
    expected_data = [nan, nan, 3.0, 4.0, 5.0, nan, nan, nan, nan, 10.0, 11.0, 12.0, 13.0, 14.0, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=15, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  # 1 hour
        "limit": 10800                   # 3 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)

# end section one
