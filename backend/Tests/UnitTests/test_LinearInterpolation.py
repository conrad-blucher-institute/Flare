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


"""
This section tests linear interpolation with different limits
and various NaN cases but keeps the same interpolation interval.

This sections data frames are also used to test invalid column names in the next section.
"""
def create_limit_test_data():
    """Create test data for limit testing."""

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
    

def create_limit_expected_data():
    """Create expected data for limit testing."""

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


# Create test data for limits with various NaN cases
limit_test_df1, limit_test_df2, limit_test_df3, limit_test_df4, limit_test_df5, limit_test_df6, limit_test_df7, limit_test_df8 = create_limit_test_data()

# Create expected data for limits with various NaN cases
expected_limit_df1, expected_limit_df2, expected_limit_df3, expected_limit_df4, expected_limit_df5, expected_limit_df6, expected_limit_df7, expected_limit_df8 = create_limit_expected_data()

# test various limits with different NaN cases
@pytest.mark.parametrize("test_df, expected_df, col_name, interpolation_interval, limit", [
    (limit_test_df1, expected_limit_df1, 'test_col', 20, 5),            # various gaps, limit of 5
    (limit_test_df2, expected_limit_df2, 'test_col', 20, 3),            # various gaps, limit of 3
    (limit_test_df3, expected_limit_df3, 'test_col', 20, 8),            # various gaps, limit of 8
    (limit_test_df4, expected_limit_df4, 'test_col', 20, 10),           # starts with NaNs, limit of 10
    (limit_test_df5, expected_limit_df5, 'test_col', 20, 2),            # ends with NaNs, limit of 2
    (limit_test_df6, expected_limit_df6, 'test_col', 20, 5),            # starts and ends with NaNs, limit of 5
    (limit_test_df7, expected_limit_df7, 'test_col', 20, 5),            # no NaNs, limit of 5
    (limit_test_df8, expected_limit_df8, 'test_col', 20, 4),            # all NaN gaps > limit, limit of 4
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


"""
This section tests linear interpolation with invalid column names. 
This uses the same DFs from the previous section, but with different column names.

These should all raise a KeyError in the post_process_factory.
"""

# test invalid column names
# the actual column name would be 'test_col' since that is what the data frames are created with in the 
# create_test_data and create_expected_data functions.
@pytest.mark.parametrize("test_df, expected_df, col_name, interpolation_interval, limit", [
    (limit_test_df1, expected_limit_df1, 'Welcome', 20, 5),            
    (limit_test_df2, expected_limit_df2, 'to', 20, 3),           
    (limit_test_df3, expected_limit_df3, 'the', 20, 8),            
    (limit_test_df4, expected_limit_df4, 'python', 20, 10),         
    (limit_test_df5, expected_limit_df5, 'tests', 20, 2),           
    (limit_test_df6, expected_limit_df6, 'for', 20, 5),          
    (limit_test_df7, expected_limit_df7, 'this', 20, 5),           
    (limit_test_df8, expected_limit_df8, 'file', 20, 4),            
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


"""
In this section, different interpolation intervals are tested with the previous NaN cases and limits.

The interval does not change the interpolation logic or affect the expected values.
Only the spacing of the timestamps in the index changes. Therefore, the previous data is resued, but with different intervals.

"""
def create_higher_interval_test_data():

    """Create test data for interval testing."""

    # various gaps, limit of 5
    # 6 NaNs -> do not interpolate
    # 1 hour interval
    data1 = [1.0, nan, nan, nan, 5.0, nan, nan, nan, nan, nan, nan, 12.0, nan, nan, 15.0, 16.0, 17.0, 18.0, nan, 20.0] 
    index1 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='3600s') 
    df1 = DataFrame({'test_col': data1}, index=index1)

    # various gaps, limit of 3
    # 4 NaNs -> do not interpolate
    # 3 hour interval
    data2 = [1.0, 2.0, nan, nan, nan, 6.0, 7.0, 8.0, nan, 10.0, nan, nan, 13.0, 14.0, 15.0, nan, nan, nan, nan, 20.0]
    index2 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='10800s')
    df2 = DataFrame({'test_col': data2}, index=index2)

    # various gaps, limit of 8
    # 9 NaNs -> do not interpolate
    # 1 day interval
    data3 = [1.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 11.0, nan, nan, nan, nan, nan, nan, nan, nan, 20.0]
    index3 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='86400s') 
    df3 = DataFrame({'test_col': data3}, index=index3)

    # starts with NaNs, limit of 10
    # 1 NaN -> do not interpolate, no starting value
    # 12 hour interval
    data4 = [nan, 2.0, nan, nan, nan, nan, nan, nan, 9.0, 10.0, nan, nan, 13.0, 14.0, nan, 16.0, 17.0, nan, nan, 20.0]
    index4 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='43200s') 
    df4 = DataFrame({'test_col': data4}, index=index4)

    # ends with NaNs, limit of 2
    # 2 NaNs -> do not interpolate, no ending value
    # 2 hour interval
    data5 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, nan, nan, 17.0, 18.0, nan, nan]
    index5 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='7200s') 
    df5 = DataFrame({'test_col': data5}, index=index5)

    # starts and ends with NaNs, limit of 5
    # 1 NaN -> do not interpolate, no starting value
    # 2 NaNs -> do not interpolate, no ending value
    # 30 minute interval
    data6 = [nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, nan, nan, nan, nan, nan, 13.0, 14.0, 15.0, nan, nan, 18.0, nan, nan]
    index6 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='1800s') 
    df6 = DataFrame({'test_col': data6}, index=index6)

    # no NaNs, limit of 5
    # 6 hour interval
    data7 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    index7 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='21600s') 
    df7 = DataFrame({'test_col': data7}, index=index7)

    # all NaN gaps > limt, limit of 4
    # do not interpolate any NaNs
    # 4 hour interval
    data8 = [1.0, nan, nan, nan, nan, nan, 7.0, nan, nan, nan, nan, nan, 13.0, nan, nan, nan, nan, nan, 19.0, 20.0]
    index8 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='14400s') 
    df8 = DataFrame({'test_col': data8}, index=index8 )

    return (df1, df2, df3, df4, df5, df6, df7, df8)



    

def create_interval_expected_data():    
    """Create expected data for interval testing."""

    # the index to use for each data frame
    index1 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='3600s')    # 1 hour
    index2 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='10800s')   # 3 hours
    index3 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='86400s')   # 1 day
    index4 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='43200s')   # 12 hours
    index5 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='7200s')    # 2 hours
    index6 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='1800s')    # 30 minutes
    index7 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='21600s')   # 6 hours
    index8 = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=20, freq='14400s')   # 4 hours

    # various gaps, limit of 5
    # 6 NaNs -> do not interpolate
    # 1 hour interval
    expected_data1 = [1.0, 2.0, 3.0, 4.0, 5.0, nan, nan, nan, nan, nan, nan, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    expected_df1 = DataFrame({'test_col': expected_data1}, index=index1)

    # various gaps, limit of 3
    # 4 NaNs -> do not interpolate
    # 3 hour interval
    expected_data2 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, nan, nan, nan, nan, 20.0]
    expected_df2 = DataFrame({'test_col': expected_data2}, index=index2)

    # various gaps, limit of 8
    # 9 NaNs -> do not interpolate
    # 1 day interval
    expected_data3 = [1.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    expected_df3 = DataFrame({'test_col': expected_data3}, index=index3)

    # starts with NaNs, limit of 10
    # 1 NaN -> do not interpolate, no starting value
    # 12 hour interval
    expected_data4 = [nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    expected_df4 = DataFrame({'test_col': expected_data4}, index=index4)

    # ends with NaNs, limit of 2
    # 2 NaNs -> do not interpolate, no ending value
    # 2 hour interval
    expected_data5 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, nan, nan]
    expected_df5 = DataFrame({'test_col': expected_data5}, index=index5)

    # starts and ends with NaNs, limit of 5
    # 1 NaN -> do not interpolate, no starting value
    # 2 NaNs -> do not interpolate, no ending value
    # 30 minute interval
    expected_data6 = [nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, nan, nan]
    expected_df6 = DataFrame({'test_col': expected_data6}, index=index6)

    # no NaNs, limit of 5
    # 6 hour interval
    expected_data7 = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    expected_df7 = DataFrame({'test_col': expected_data7}, index=index7)

    # all NaN gaps > limt, limit of 4
    # do not interpolate any NaNs
    # 4 hour interval
    expected_data8 = [1.0, nan, nan, nan, nan, nan, 7.0, nan, nan, nan, nan, nan, 13.0, nan, nan, nan, nan, nan, 19.0, 20.0]
    expected_df8 = DataFrame({'test_col': expected_data8}, index=index8)

    return (expected_df1, expected_df2, expected_df3, expected_df4,
            expected_df5, expected_df6, expected_df7, expected_df8)


# make the test data for intervals
high_df1 , high_df2, high_df3, high_df4, high_df5, high_df6, high_df7, high_df8 = create_higher_interval_test_data()

# make the expected data for intervals
expected_high1, expected_high2, expected_high3, expected_high4, expected_high5, expected_high6, expected_high7, expected_high8 = create_interval_expected_data()

@pytest.mark.parametrize("test_df, expected_df, col_name, interpolation_interval, limit", [
    (high_df1, expected_high1, 'test_col', 3600, 5),            # 1 hour interval, various gaps, limit of 5
    (high_df2, expected_high2, 'test_col', 10800, 3),           # 3 hour interval, various gaps, limit of 3, 
    (high_df3, expected_high3, 'test_col', 86400, 8),           # 1 day interval, various gaps, limit of 8, 
    (high_df4, expected_high4, 'test_col', 43200, 10),          # 12 hour interval, starts with NaNs, limit of 10, 
    (high_df5, expected_high5, 'test_col', 7200, 2),            # 2 hour interval, ends with NaNs, limit of 2, 
    (high_df6, expected_high6, 'test_col', 1800, 5),            # 30 minute interval, starts and ends with NaNs, limit of 5, 
    (high_df7, expected_high7, 'test_col', 21600, 5),           # 6 hour interval, no NaNs, limit of 5, 
    (high_df8, expected_high8, 'test_col', 14400, 4),           # 4 hour interval, all NaN gaps > limit, limit of 4, 
])
def test_different_intervals(test_df: DataFrame, expected_df: DataFrame, col_name: str, interpolation_interval: int, limit: int):
    """Test linear interpolation with different intervals, various NaN cases, and different limits."""

    kwargs = {
        "col_name": col_name,                                # col to interpolate
        "interpolation_interval": interpolation_interval,    # difference in time between 2 periods, in seconds
        "limit": limit                                       # max number of consecutive NaNs to interpolate
    }

    # call the post processing factory to do the work
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare the data frames 
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9)