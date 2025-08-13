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

