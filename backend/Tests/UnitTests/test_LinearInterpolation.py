# -*- coding: utf-8 -*-
#test_LinearInterpolation.py
#-------------------------------
# Created By: Christian Quintero
# Last Updated: 09/12/2025
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
"""  

def test_basic_interpolation():
    """
    This tests basic interpolation with a small limit for simplicity.
    """

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


def test_limit_5hours():
    """
    This test ensures that interpolation happens correctly with a limit of 5 hours.
    """

    test_data = [1.0, nan, nan, nan, nan, nan, 7.0, nan, nan, nan, nan, nan, nan, 14.0, nan, nan, nan, 18.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=18, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # analysis
    # hours 1-5 (5 hours of nans), limit 5 hours -> interpolate
    # hours 7-12 (6 hours of nans), limit 5 hours -> do not interpolate
    # hours 14-16 (2 hours of nans), limit 5 hours -> interpolate
    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, nan, nan, nan, nan, nan, nan, 14.0, 15.0, 16.0, 17.0, 18.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=18, freq='3600s')
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


def test_no_interpolation():
    """
    This test ensures that no interpolation happens when every nan duration is > limit.
    """    

    test_data = [1.0, nan, nan, nan, nan, nan, nan, 8.0, nan, nan, nan, nan, nan, nan,
                15.0, nan, nan, nan, nan, nan, nan, 22.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=22, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # all gaps last for 6 hours, limit is 5 hours -> do not interpolate
    expected_data = [1.0, nan, nan, nan, nan, nan, nan, 8.0, nan, nan, nan, nan, nan, nan,
                     15.0, nan, nan, nan, nan, nan, nan, 22.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=22, freq='3600s')
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


def test_no_nans():
    """
    This test ensures that no interpolation happens when there are no nans.
    """    

    test_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
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


def test_all_nans():
    """
    This test ensures that no interpolation happens when all values are nans.
    """    

    test_data = [nan, nan, nan, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    expected_data = [nan, nan, nan, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=5, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  # 1 hour
        "limit": 3600                    # 1 hour
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


# end section one
