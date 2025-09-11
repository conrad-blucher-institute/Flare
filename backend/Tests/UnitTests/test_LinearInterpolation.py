# -*- coding: utf-8 -*-
#test_LinearInterpolation.py
#-------------------------------
# Created By: Christian Quintero
# Last Updated: 09/11/2025
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


"""
This next section tests reindexing when the interval is higher than our index frequency.
"""

def test_higher_interval():
    """
    A basic test to ensure reindexing works when the interval is higher than the index frequency.
    """
    test_data = [1.0, nan, nan, nan, 5.0, nan, nan, nan, 9.0, nan, nan, nan, 13.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='3600s')     
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # interpolated data before reindexing
    # all nans are interpolated because they are all within the 3 hour limit
    #
    # interpolated_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0]
    # interpolated_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='3600s')
    # interpolated_df = DataFrame({'test_col': interpolated_data}, index=interpolated_index)
    #
    # after reindexing to every 3 hours, we only keep hours that land on 3 hour intervals
    # reindexed_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=5, freq='10800s')   # 3 hour frequency
    # reindexed_data = [1.0, 4.0, 7.0, 10.0, 13.0]                                            # hours 0, 3, 6, 9, 12
    # join back with original df 
    # 
    # the result is that the original non-nan values are merged with the reindexed interpolated values
    # and nans are placed where there is no data in both the original and reindexed dataframes
    expected_data = [1.0, nan, nan, 4.0, 5.0, nan, 7.0, nan, 9.0, 10.0, nan, nan, 13.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 10800,  # 3 hours
        "limit": 10800                    # 3 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)
    
       
def test_real_NDFD_data():
    """
    This test uses real NDFD data returned from calling NDFD without interpolating.
    This is to check that the code is working as expected, because Flare refues to interpolate 
    data as expected, so to ensure the code is working, we use real data that has been manually checked.
    """
    test_data = [28.0, 28.0, 28.0, 28.0, 28.0, 29.0, 30.0, 30.0, 31.0, 31.0, 31.0,
                  31.0, 31.0, 31.0, 31.0, 30.0, 30.0, 30.0, 30.0, 30.0, 29.0, 29.0, 29.0, 29.0, 29.0,
                  28.0, 28.0, 28.0, 28.0, 29.0, 30.0, 30.0, 29.0, 31.0, 31.0, 30.0, 32.0,
                  30.0, 30.0, 30.0, 30.0, 29.0, 30.0, 29.0, 29.0, 29.0, 29.0, 28.0, 29.0,
                  28.0, 28.0, 28.0, 27.0, 29.0, 30.0, 29.0, 29.0, 31.0, 31.0, 30.0, 32.0, 
                  30.0, 30.0, 30.0, 30.0, 29.0, 29.0, 29.0, 29.0, 29.0, 29.0, 28.0, 28.0,
                  28.0, 28.0, 28.0, 28.0, 29.0, 29.0, 29.0, 29.0, 31.0, 31.0, 30.0, 30.0,
                  30.0, 31.0, 30.0, 30.0, 29.0, 29.0, 29.0, 29.0, 29.0, 29.0, 28.0, 28.0,
                  28.0, 28.0, 28.0, 28.0, 29.0, 29.0, 29.0, 29.0, 31.0, 31.0, 30.0, 30.0,
                  30.0, 30.0, 30.0, 30.0, 29.0, 29.0, 29.0, 29.0, 29.0, 29.0, 28.0, 28.0,
                  28.0, 28.0, 27.0, 27.0, 28.0, nan, nan, nan, 30.0, nan, nan, nan, nan, nan, 30.0,
                  nan, nan, nan, nan, nan, 29.0, nan, nan, nan, nan, nan, 27.0, nan, nan, nan, nan, nan, 30.0,
                  nan, nan, nan, nan, nan, 30.0, nan, nan, nan, nan, nan, nan, nan, nan, 30.0]
    test_index = date_range(datetime(2025, 9, 15, 1, 0, 0), periods=len(test_data), freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    expected_data = [28.0, 28.0, 28.0, 28.0, 28.0, 29.0, 30.0, 30.0, 31.0, 31.0, 31.0,
                  31.0, 31.0, 31.0, 31.0, 30.0, 30.0, 30.0, 30.0, 30.0, 29.0, 29.0, 29.0, 29.0, 29.0,
                  28.0, 28.0, 28.0, 28.0, 29.0, 30.0, 30.0, 29.0, 31.0, 31.0, 30.0, 32.0,
                  30.0, 30.0, 30.0, 30.0, 29.0, 30.0, 29.0, 29.0, 29.0, 29.0, 28.0, 29.0,
                  28.0, 28.0, 28.0, 27.0, 29.0, 30.0, 29.0, 29.0, 31.0, 31.0, 30.0, 32.0, 
                  30.0, 30.0, 30.0, 30.0, 29.0, 29.0, 29.0, 29.0, 29.0, 29.0, 28.0, 28.0,
                  28.0, 28.0, 28.0, 28.0, 29.0, 29.0, 29.0, 29.0, 31.0, 31.0, 30.0, 30.0,
                  30.0, 31.0, 30.0, 30.0, 29.0, 29.0, 29.0, 29.0, 29.0, 29.0, 28.0, 28.0,
                  28.0, 28.0, 28.0, 28.0, 29.0, 29.0, 29.0, 29.0, 31.0, 31.0, 30.0, 30.0,
                  30.0, 30.0, 30.0, 30.0, 29.0, 29.0, 29.0, 29.0, 29.0, 29.0, 28.0, 28.0,
                  28.0, 28.0, 27.0, 27.0, 28.0, 28.5, 29.0, 29.5, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0,
                  29.83333333, 29.66666667, 29.5, 29.33333333, 29.16666667, 29.0, 28.66666667, 28.33333333,
                  28.0, 27.66666667, 27.33333333, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5, 30.0,
                  30.0, 30.0, 30.0, 30.0, 30.0, 30.0, nan, nan, nan, nan, nan, nan, nan, nan, 30.0]
    expected_index = date_range(datetime(2025, 9, 15, 1, 0, 0), periods=len(expected_data), freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  # 1 hour
        "limit": 18000                   # 5 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    result_df = result_df

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_real_scenario():
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
