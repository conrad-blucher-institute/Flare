# -*- coding: utf-8 -*-
#test_LinearInterpolation.py
#-------------------------------
# Created By: Christian Quintero
# Last Updated: 08/13/2025
#----------------------------------
"""
This file tests the LinearInterpolation PPC 
""" 
#----------------------------------
# 
#
import sys
sys.path.append('/app/backend')

import pytest
import pandas as pd
from math import isclose
from pandas import DataFrame, date_range, read_csv, Series
from numpy import nan
from datetime import datetime
from PostProcessing.IPostProcessing import post_process_factory

"""
The first section tests various NaN cases with the same interval as the index

index frequency is 1 hour (3600 seconds), and the interpolation interval is also set to 3600 seconds.
"""  

def test_same_index_limit_5():

    test_data = [1.0, nan, nan, nan, nan, nan, 7.0, nan, 9.0, nan, nan, nan, nan, nan, nan, 16.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=16, freq='3600s')  
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # 1.0 to 7.0: 5 NaNs, limit 5 -> interpolate
    # 7.0 to 9.0: 1 NaN, limit 5 -> interpolate
    # 9.0 to 16.0: 6 NaNs, limit 5 -> do not interpolate

    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, nan, nan, nan, nan, nan, nan, 16.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=16, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  # 1 hour
        "limit": 5
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)


def test_same_index_limit_3():

    test_data = [1.0, nan, nan, nan, nan, 6.0, nan, 8.0, nan, nan, nan, 12.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=12, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # 1.0 to 6.0: 4 NaNs, limit 3 -> do not interpolate
    # 6.0 to 8.0: 1 NaN, limit 3 -> interpolate
    # 8.0 to 12.0: 3 NaNs, limit 3 -> interpolate

    expected_data = [1.0, nan, nan, nan, nan, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=12, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 3
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)


def test_same_index_limit_8():

    test_data = [1.0, nan, nan, nan, nan, nan, nan, nan, nan, 10.0, nan, nan, nan, 14.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 24.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=24, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # 1.0 to 10.0: 8 NaNs, limit 8 -> interpolate
    # 10.0 to 14.0: 3 NaNs, limit 8 -> interpolate
    # 14.0 to 24.0: 9 NaNs, limit 8 -> do not interpolate
    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 24.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=24, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 8
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)


def test_same_index_start_nans():

    test_data = [nan, nan, 3.0, nan, 5.0, nan, nan, 8.0, nan, 10.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)
    
    # Gap Analysis
    # Start with NaNs: do not interpolate
    # 3.0 to 5.0: 1 NaN, limit 3 -> interpolate
    # 5.0 to 8.0: 2 NaNs, limit 3 -> interpolate
    # 8.0 to 10.0: 1 NaN, limit 3 -> interpolate

    expected_data = [nan, nan, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 3
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)


def test_same_index_end_nans():
    
    test_data = [1.0, 2.0, 3.0, nan, 5.0, nan, nan, 8.0, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # 3.0 to 5.0: 1 NaN, limit 3 -> interpolate
    # 5.0 to 8.0: 2 NaNs, limit 3 -> interpolate
    # 8.0 to end: do not interpolate, no end value

    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 3
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)


def test_same_index_start_end_nans():

    test_data = [nan, nan, 3.0, nan, 5.0, nan, nan, 8.0, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # Start with NaNs: do not interpolate
    # 3.0 to 5.0: 1 NaN, limit 3 -> interpolate
    # 5.0 to 8.0: 2 NaNs, limit 3 -> interpolate
    # End with NaNs: do not interpolate

    expected_data = [nan, nan, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 3
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)


def test_same_index_no_nan():
    """This test ensures nothing happens when there is no NaNs to interpolate."""

    test_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # No NaNs, no interpolation needed
    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 3
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)


def test_same_index_all_nans():
    """
    This test ensures nothing happens when all values are NaNs. This is because we only interpolate
    the inside of 2 real values, never the start or end of a series. 
    """

    test_data = [nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # All NaNs, no interpolation needed
    expected_data = [nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 3
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)



"""
The second section tests various NaN cases and limits with a smaller interpolation interval than the index. 
This will cause new NaNs to be added to the data series during the interpolation process.

For example, the test_index is set to a frequency of 1 hour (3600 seconds), but the interpolation interval is set to 30 minutes (1800 seconds).
This causes new NaNs to be added to the data series during the interpolation process, and then the new NaN gaps are checked against the limit value
to determine to interpolate or not. 

Each test will have a comment showing what the reindexed data would look like with an explanation on how the gaps are analyzed.
"""

def test_lower_index_limit_12():

    # originally, these values are for every hour, so the reindexing at every half hour, will add a NaN in between each value here
    test_data = [1.0, nan, 3.0, nan, nan, nan, nan, nan, nan, 10.0, nan, nan, nan, nan, nan, 16.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=16, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # reindexing at 30 minute intervals :
    # [1.0, nan, nan, nan, 3.0, nan, nan, nan, nan, nan,
    #  nan, nan, nan, nan, nan, nan, nan, nan, 10.0, nan,
    #  nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 16.0]

    # Gap Analysis
    # 1.0 to 3.0: 3 NaNs, limit 12 -> interpolate
    # 3.0 to 10.0: 13 NaNs, limit 12 -> do not interpolate
    # 10.0 to 16.0: 11 NaNs, limit 12 -> interpolate
    expected_data = [1.0, 1.5, 2.0, 2.5, 3.0, nan, nan, nan, nan, nan,
                      nan, nan, nan, nan, nan, nan, nan, nan, 10.0, 10.5,
                        11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0]
                        
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=31, freq='1800s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 1800,  # 30 minutes, causes the reindexing to add NaNs
        "limit": 12
    }

   
    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    print("Expected Seres:\n", expected_df['test_col'])
    print("Result Series:\n", result_df['test_col'])

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)



