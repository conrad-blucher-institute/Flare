# -*- coding: utf-8 -*-
#test_LinearInterpolation.py
#-------------------------------
# Created By: Christian Quintero
# Last Updated: 08/05/2025
#----------------------------------
"""This file tests the LinearInterpolation PPC 
    
    Important: It should be noted that at the time of writing this (08/05/2025), the linear interpolationg
    is expected to work by counting where gaps of 5 consecutive NaNs will occur, and interpolating over those gaps
    between 2 real values. If the gap between 2 real values has 6+ NaNs, no linear interpolation should occur, and any gap 
    <= 5 should be interpolated.
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

# This method makes some dummy test data with various lengths and has various NaN streak lengths
# to be used to test that the interpolation is working as expected.
def create_test_data():
    """Create test DataFrames with intentional NaN streaks of various lengths"""
    
    # Create a time index
    index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='1min')
    
    # Test case 1: Mixed short and long streaks.
    data1 = [1.0, nan, nan, nan, 5.0, nan, nan, nan, nan, nan, nan, 12.0, nan, nan, 15.0, 16.0, nan, nan, nan, nan]
    df1 = DataFrame({'test_col': data1}, index=index)
    
    # Test case 2: Exactly at the limit
    data2 = [1.0, nan, nan, nan, nan, nan, 7.0, nan, nan, nan, nan, nan, 14.0]
    index2 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='1min')
    df2 = DataFrame({'test_col': data2}, index=index2)
    
    # Test case 3: Single NaN values (should always interpolate)
    data3 = [1.0, nan, 3.0, nan, 5.0, nan, 7.0]
    index3 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=7, freq='1min')
    df3 = DataFrame({'test_col': data3}, index=index3)
    
    # Test case 4: NaN streaks at beginning and end (edge cases)
    data4 = [nan, nan, nan, 4.0, nan, nan, nan, nan, nan, 10.0, nan, nan, nan]
    index4 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='1min')
    df4 = DataFrame({'test_col': data4}, index=index4)

    # Test case 5: Clear long streak that definitely shouldn't interpolate
    data5 = [1.0, nan, nan, nan, nan, nan, nan, nan, 9.0] 
    index5 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=9, freq='1min')
    df5 = DataFrame({'test_col': data5}, index=index5)

    return df1, df2, df3, df4, df5


def create_expected_data():
    """Creates the expected data frames to be compared to the test data"""
    
    # Create the same time indices as the test data
    index  = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='1min')
    index2 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='1min')
    index3 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=7, freq='1min')
    index4 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='1min')
    index5 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=9, freq='1min')
    
    # Expected case 1: Mixed short and long streaks
    # Original: [1.0, nan, nan, nan, 5.0, nan, nan, nan, nan, nan, nan, 12.0, nan, nan, 15.0, 16.0, nan, nan, nan, nan]
    # Gap 1: 3 NaNs between 1.0 and 5.0 → interpolate (2.0, 3.0, 4.0)
    # Gap 2: 6 NaNs between 5.0 and 12.0 → DON'T interpolate (leave as NaN)
    # Gap 3: 2 NaNs between 12.0 and 15.0 → interpolate (13.0, 14.0)
    # Gap 4: 4 NaNs at end after 16.0 → leave as NaN (no endpoint to interpolate to)
    expected_data1 = [1.0, 2.0, 3.0, 4.0, 5.0, nan, nan, nan, nan, nan, nan, 12.0, 13.0, 14.0, 15.0, 16.0, nan, nan, nan, nan]
    expected_df1 = DataFrame({'test_col': expected_data1}, index=index)
    
    # Expected case 2: Exactly at the limit
    # Original: [1.0, nan, nan, nan, nan, nan, 7.0, nan, nan, nan, nan, nan, 14.0]
    # Gap 1: 5 NaNs between 1.0 and 7.0 → interpolate (2.0, 3.0, 4.0, 5.0, 6.0)
    # Gap 2: 5 NaNs between 7.0 and 14.0 → interpolate 
    # Step size for gap 2: (14.0 - 7.0) / 6 = 7.0 / 6 ≈ 1.1667
    # Values: 7 + 1.1667 = 8.1667, 7 + 2*1.1667 = 9.3333, 7 + 3*1.1667 = 10.5, 7 + 4*1.1667 = 11.6667, 7 + 5*1.1667 = 12.8333
    expected_data2 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.166666666666666, 9.333333333333334, 10.5, 11.666666666666666, 12.833333333333334, 14.0]
    expected_df2 = DataFrame({'test_col': expected_data2}, index=index2)


    # Expected case 3: Single NaN values (should always interpolate)
    # Original: [1.0, nan, 3.0, nan, 5.0, nan, 7.0]
    # All gaps are 1 NaN → interpolate all
    expected_data3 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    expected_df3 = DataFrame({'test_col': expected_data3}, index=index3)
    
    # Expected case 4: NaN streaks at beginning and end (edge cases)
    # Original: [nan, nan, nan, 4.0, nan, nan, nan, nan, nan, 10.0, nan, nan, nan]
    # Gap 1: 3 NaNs at beginning → leave as NaN (no starting point)
    # Gap 2: 5 NaNs between 4.0 and 10.0 → interpolate
    # Step size: (10.0 - 4.0) / 6 = 6.0 / 6 = 1.0
    # Values: 4 + 1 = 5.0, 4 + 2 = 6.0, 4 + 3 = 7.0, 4 + 4 = 8.0, 4 + 5 = 9.0
    # Gap 3: 3 NaNs at end → leave as NaN (no endpoint)
    expected_data4 = [nan, nan, nan, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, nan, nan, nan]
    expected_df4 = DataFrame({'test_col': expected_data4}, index=index4)
    
    # Expected case 5: Clear long streak that definitely shouldn't interpolate
    # Original: [1.0, nan, nan, nan, nan, nan, nan, nan, 9.0]
    # Gap: 7 NaNs between 1.0 and 9.0 → DON'T interpolate (≥6 NaNs)
    expected_data5 = [1.0, nan, nan, nan, nan, nan, nan, nan, 9.0]
    expected_df5 = DataFrame({'test_col': expected_data5}, index=index5)

    return expected_df1, expected_df2, expected_df3, expected_df4, expected_df5


# Create the test data and expected data frames
test_df1, test_df2, test_df3, test_df4, test_df5 = create_test_data()
expected_df1, expected_df2, expected_df3, expected_df4, expected_df5 = create_expected_data()


@pytest.mark.parametrize("test_df, expected_df, col_name, interpolation_interval, limit", [
    (test_df1, expected_df1, "test_col", 60, 5),
    (test_df2, expected_df2, "test_col", 60, 5),
    (test_df3, expected_df3, "test_col", 60, 5),
    (test_df4, expected_df4, "test_col", 60, 5),
    (test_df5, expected_df5, "test_col", 60, 5)

])
def test_interpolation(test_df: DataFrame, expected_df: DataFrame, col_name: str, interpolation_interval: int, limit: int):
    """Test Linear Interpolation PPC with the first test data frame"""

    kwargs = {
        "col_name": col_name,                                # col to interpolate
        "interpolation_interval": interpolation_interval,    #
        "limit": limit                                       # how many consecutive NaNs to interpolate over
    }


    # call the post processing factory with to interpolate the first test data frame
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    

    # compare the data frames 
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)
