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

def test_basic_interpolation():
    """
    A very basic test to ensure basic interpolation is working.
    """

    test_data = [1.0, nan, 3.0, nan, 5.0, nan, 7.0, nan, 9.0, nan, 11.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=11, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # 1.0 to 3.0:  1 hour gap, limit 3 hours -> interpolate
    # 3.0 to 5.0:  1 hour gap, limit 3 hours -> interpolate
    # 5.0 to 7.0:  1 hour gap, limit 3 hours -> interpolate
    # 7.0 to 9.0:  1 hour gap, limit 3 hours -> interpolate
    # 9.0 to 11.0: 1 hour gap, limit 3 hours -> interpolate
    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=11, freq='3600s')
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

def test_3hour_interpolation():
    """
    Test a limit of 3 hours. There is a gap exactly at 3 hours, one gap over 3 hours, and one gap under 3 hours.
    """

    test_data = [1.0, nan, nan, nan, nan, 6.0, nan, 8.0, nan, nan, nan, 12.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=12, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # 1.0 to 6.0:   4 hour gap, limit 3 hours -> do not interpolate
    # 6.0 to 8.0:   1 hour gap, limit 3 hours -> interpolate
    # 8.0 to 12.0:  3 hour gap, limit 3 hours -> interpolate
    expected_data = [1.0, nan, nan, nan, nan, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=12, freq='3600s')
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

def test_5hour_interpolation():
    """
    Test a limit of 5 hours. There is a gap exactly at 5 hours, one gap over 5 hours, and one gap under 5 hours.
    """
    
    test_data = [1.0, nan, nan, 4.0, nan, nan, nan, nan, nan, nan, 11.0, nan, nan, nan, nan, nan, 17.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=17, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # 1.0 to 4.0:   2 hour gap, limit 5 hours -> interpolate
    # 4.0 to 11.0:  6 hour gap, limit 5 hours -> do not interpolate
    # 11.0 to 17.0: 5 hour gap, limit 5 hours -> interpolate
    expected_data = [1.0, 2.0, 3.0, 4.0, nan, nan, nan, nan, nan, nan, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=17, freq='3600s')
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

def test_7hour_interpolation():
    """
    Test a limit of 7 hours. There is a gap exactly at 7 hours, one gap over 7 hours, and one gap under 7 hours.
    """

    test_data = [1.0, nan, nan, nan, nan, nan, nan, nan, 9.0, nan, nan, nan, nan,
                  nan, nan, nan, nan, 18.0, nan, nan, nan, nan, nan, 24.0]
    
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=24, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # 1.0 to 9.0:   7 hour gap, limit 7 hours -> interpolate
    # 9.0 to 18.0:  8 hour gap, limit 7 hours -> do not interpolate
    # 18.0 to 24.0: 5 hour gap, limit 7 hours -> interpolate
    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, nan, nan, nan, nan,
                     nan, nan, nan, nan, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=24, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)


    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  # 1 hour
        "limit": 25200                   # 7 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)

def test_no_interpolation():
    """
    Tests when all time gaps are over the limit, so no interpolation should occur.
    The limit is set to 5 hours, but there are 6 hours of missing data between each pair of known values
    -> no interpolation should occur.
    """
    test_data = [1.0, nan, nan, nan, nan, nan, nan, 8.0, nan, nan, nan, nan, nan, nan, 15.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=15, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # 1.0 to 8.0:  6 hour gap, limit 5 hours -> do not interpolate
    # 8.0 to 15.0: 6 hour gap, limit 5 hours -> do not interpolate
    expected_data = [1.0, nan, nan, nan, nan, nan, nan, 8.0, nan, nan, nan, nan, nan, nan, 15.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=15, freq='3600s')
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

def test_start_end_nans_interpolation():
    """
    This test ensures that NaNs at the start and end of the series are not interpolated.
    We only interpolate NaNs between two real values.
    """

    test_data = [nan, nan, 3.0, nan, 5.0, nan, nan, 8.0, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # Start with NaNs: do not interpolate
    # 3.0 to 5.0: 1 hour gap, limit 3 hours -> interpolate
    # 5.0 to 8.0: 2 hour gap, limit 3 hours -> interpolate
    # End with NaNs: do not interpolate
    expected_data = [nan, nan, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
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