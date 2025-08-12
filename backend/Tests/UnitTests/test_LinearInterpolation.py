# -*- coding: utf-8 -*-
#test_LinearInterpolation.py
#-------------------------------
# Created By: Christian Quintero
# Last Updated: 08/12/2025
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


def create_test_data():

    # the index to use for the data frames
    index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='20s')

    # various gaps, limit of 5
    # 6 NaNs -> do not interpolate
    data1 = [1.0, nan, nan, nan, 5.0, nan, nan, nan, nan, nan, nan, 12.0, nan, nan, 15.0, 16.0, 17.0, 18.0, nan, 20.0] 
    df1 = DataFrame({'test_col': data1}, index=index)

    # various gaps, limit of 3
    # 4 NaNs -> do not interpolate
    data2 = [1.0, 2.0, nan, nan, nan, 6.0, 7.0, 8.0, nan, 10.0, nan, nan, 13.0, 14.0, 15.0, nan, nan, nan, nan, 20.0]
    df2 = DataFrame({'test_col': data2}, index=index)

    # various gaps, limit of 8
    # 9 NaNs -> do not interpolate
    data3 = [1.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 11.0, nan, nan, nan, nan, nan, nan, nan, nan, 20.0]
    df3 = DataFrame({'test_col': data3}, index=index)

    # starts with NaNs, limit of 10
    # 1 NaN -> do not interpolate, no starting value
    data4 = [nan, 2.0, nan, nan, nan, nan, nan, nan, 9.0, 10.0, nan, nan, 13.0, 14.0, nan, 16.0, 17.0, nan, nan, 20.0]
    df4 = DataFrame({'test_col': data4}, index=index)

    # ends with NaNs, limit of 2
    # 2 NaNs -> do not interpolate, no ending value
    data5 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, nan, nan, 17.0, 18.0, nan, nan]
    df5 = DataFrame({'test_col': data5}, index=index)

    # starts and ends with NaNs, limit of 5
    # 1 NaN -> do not interpolate, no starting value
    # 2 NaNs -> do not interpolate, no ending value
    data6 = [nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, nan, nan, nan, nan, nan, 13.0, 14.0, 15.0, nan, nan, 18.0, nan, nan]
    df6 = DataFrame({'test_col': data6}, index=index)

    # no NaNs, limit of 5
    data7 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    df7 = DataFrame({'test_col': data7}, index=index)

    # all NaN gaps > limt, limit of 4
    # do not interpolate any NaNs
    data8 = [1.0, nan, nan, nan, nan, nan, 7.0, nan, nan, nan, nan, nan, 13.0, nan, nan, nan, nan, nan, 19.0, 20.0]
    df8 = DataFrame({'test_col': data8}, index=index)

    return (df1, df2, df3, df4, df5, df6, df7, df8)
    

def create_expected_data():
    """Create expected data for group 1."""

    # the index to use for the data frames
    index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='20s')

    # various gaps, limit of 5
    # 6 NaNs -> do not interpolate
    expected_data1 = [1.0, 2.0, 3.0, 4.0, 5.0, nan, nan, nan, nan, nan, nan, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    expected_df1 = DataFrame({'test_col': expected_data1}, index=index)

    # various gaps, limit of 3
    # 4 NaNs -> do not interpolate
    expected_data2 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, nan, nan, nan, nan, 20.0]
    expected_df2 = DataFrame({'test_col': expected_data2}, index=index)

    # various gaps, limit of 8
    # 9 NaNs -> do not interpolate
    expected_data3 = [1.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    expected_df3 = DataFrame({'test_col': expected_data3}, index=index)

    # starts with NaNs, limit of 10
    # 1 NaN -> do not interpolate, no starting value
    expected_data4 = [nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    expected_df4 = DataFrame({'test_col': expected_data4}, index=index)

    # ends with NaNs, limit of 2
    # 2 NaNs -> do not interpolate, no ending value
    expected_data5 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, nan, nan]
    expected_df5 = DataFrame({'test_col': expected_data5}, index=index)

    # starts and ends with NaNs, limit of 5
    # 1 NaN -> do not interpolate, no starting value
    # 2 NaNs -> do not interpolate, no ending value
    expected_data6 = [nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, nan, nan]
    expected_df6 = DataFrame({'test_col': expected_data6}, index=index)

    # no NaNs, limit of 5
    expected_data7 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    expected_df7 = DataFrame({'test_col': expected_data7}, index=index)

    # all NaN gaps > limt, limit of 4
    # do not interpolate any NaNs
    expected_data8 = [1.0, nan, nan, nan, nan, nan, 7.0, nan, nan, nan, nan, nan, 13.0, nan, nan, nan, nan, nan, 19.0, 20.0]
    expected_df8 = DataFrame({'test_col': expected_data8}, index=index)

    return (expected_df1, expected_df2, expected_df3, expected_df4,
            expected_df5, expected_df6, expected_df7, expected_df8)


# Create test data and expected data
test_df1, test_df2, test_df3, test_df4, test_df5, test_df6, test_df7, test_df8 = create_test_data()
expected_df1, expected_df2, expected_df3, expected_df4, expected_df5, expected_df6, expected_df7, expected_df8 = create_expected_data()


# test various limits with different NaN cases
@pytest.mark.parametrize("test_df, expected_df, col_name, interpolation_interval, limit", [
    (test_df1, expected_df1, 'test_col', 20, 5),            # various gaps, limit of 5
    (test_df2, expected_df2, 'test_col', 20, 3),            # various gaps, limit of 3
    (test_df3, expected_df3, 'test_col', 20, 8),            # various gaps, limit of 8
    (test_df4, expected_df4, 'test_col', 20, 10),           # starts with NaNs, limit of 10
    (test_df5, expected_df5, 'test_col', 20, 2),            # ends with NaNs, limit of 2
    (test_df6, expected_df6, 'test_col', 20, 5),            # starts and ends with NaNs, limit of 5
    (test_df7, expected_df7, 'test_col', 20, 5),            # no NaNs, limit of 5
    (test_df8, expected_df8, 'test_col', 20, 4),            # all NaN gaps > limt, limit of 4
])
def test_different_limits(test_df: DataFrame, expected_df: DataFrame, col_name: str, interpolation_interval: int, limit: int):
    """Test linear interpolation with different limits and various NaN cases."""

    
    kwargs = {
        "col_name": col_name,                                # col to interpolate
        "interpolation_interval": interpolation_interval,    # difference in time between 2 periods, in seconds
        "limit": limit                                       # max number of consecutive NaNs to interpolate
    }

    # call the post processing factory to do the work
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare the data frames 
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)


# test invalid column names
# the actual column name would be 'test_col' since that is what the data frames are created with in the 
# create_test_data and create_expected_data functions.
@pytest.mark.parametrize("test_df, expected_df, col_name, interpolation_interval, limit", [
    (test_df1, expected_df1, 'Welcome', 20, 5),            
    (test_df2, expected_df2, 'to', 20, 3),           
    (test_df3, expected_df3, 'the', 20, 8),            
    (test_df4, expected_df4, 'python', 20, 10),         
    (test_df5, expected_df5, 'tests', 20, 2),           
    (test_df6, expected_df6, 'for', 20, 5),          
    (test_df7, expected_df7, 'this', 20, 5),           
    (test_df8, expected_df8, 'file', 20, 4),            
])
def test_invalid_column_name(test_df: DataFrame, expected_df: DataFrame, col_name: str, interpolation_interval: int, limit: int):
    """Test linear interpolation with an invalid column name."""

    kwargs = {
        "col_name": col_name,                                # col to interpolate
        "interpolation_interval": interpolation_interval,    # difference in time between 2 periods, in seconds
        "limit": limit                                       # max number of consecutive NaNs to interpolate
    }

    # a KeyError should be raised since the column name does not exist in the data frame
    with pytest.raises(KeyError):
        result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)



