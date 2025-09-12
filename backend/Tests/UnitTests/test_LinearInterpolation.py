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
import sys
sys.path.append('/app/backend')

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

def test_same_index_limit_5():

    test_data = [1.0, nan, nan, nan, nan, nan, 7.0, nan, 9.0, nan, nan, nan, nan, nan, nan, 16.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=16, freq='3600s')  
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # hour 1-5: 5 hours of nans, limit 5 hours -> interpolate
    # hour 7: 1 hour of nans, limit 5 hours -> interpolate
    # hour 9-14: 6 hours of nans, limit 5 hours -> do not interpolate

    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, nan, nan, nan, nan, nan, nan, 16.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=16, freq='3600s')
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


def test_same_index_limit_3():

    test_data = [1.0, nan, nan, nan, nan, 6.0, nan, 8.0, nan, nan, nan, 12.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=12, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # hour 1-4: 4 hours of nans, limit 3 hours -> do not interpolate
    # hour 6: 1 hour of nans, limit 3 hours -> interpolate
    # hour 8-10: 3 hours of nans, limit 3 hours -> interpolate
    expected_data = [1.0, nan, nan, nan, nan, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=12, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 10800                   # 3 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_same_index_limit_8():

    test_data = [1.0, nan, nan, nan, nan, nan, nan, nan, nan, 10.0, nan, nan, nan, 14.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 24.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=24, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # hour 1-9: 8 hours of nans, limit 8 hours -> interpolate
    # hour 14-22: 9 hours of nans, limit 8 hours -> do not interpolate
    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 24.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=24, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 28800                   # 8 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_same_index_start_nans():

    test_data = [nan, nan, 3.0, nan, 5.0, nan, nan, 8.0, nan, 10.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)
    
    # Gap Analysis
    # Start with NaNs: do not interpolate
    # hour 3: 1 hour of nans, limit 3 hours -> interpolate

    expected_data = [nan, nan, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 10800                   # 3 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_same_index_end_nans():
    
    test_data = [1.0, 2.0, 3.0, nan, 5.0, nan, nan, 8.0, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # hour 3: 1 hour of nans, limit 3 hours -> interpolate
    # hour 5-6: 2 hours of nans, limit 3 hours -> interpolate
    # End with NaNs: do not interpolate

    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 10800                   # 3 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_same_index_start_end_nans():

    test_data = [nan, nan, 3.0, nan, 5.0, nan, nan, 8.0, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Gap Analysis
    # Start with NaNs: do not interpolate
    # hour 3: 1 hour of nans, limit 3 hours -> interpolate
    # hour 5-6: 2 hours of nans, limit 3 hours -> interpolate
    # End with NaNs: do not interpolate

    expected_data = [nan, nan, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,  
        "limit": 10800                   # 3 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


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
        "limit": 10800                   # 3 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


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
        "limit": 10800                   # 3 hours
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


"""
The second section tests various NaN cases and limits with a smaller interpolation interval than the index. 
This will cause new NaNs to be added to the data series during the interpolation process.

For example, if the test_index is set to a frequency of 1 hour (3600 seconds), but the interpolation interval is set to 30 minutes (1800 seconds),
this causes new NaNs to be added to the data series during the interpolation process, and then the new NaN gaps are checked against the limit value
to determine to interpolate or not. 

Each test will have a comment showing what the reindexed data would look like with an explanation on how the gaps are analyzed.
"""


def test_lower_interval_limit_12():

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

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_lower_interval_limit_6():

    test_data = [1.0, nan, 3.0, nan, nan, 6.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=6, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Reindexing at 20 minute intervals (1200s):
    # Original: 6 hourly points spanning 5 hours (0 to 5 hours)
    # New: 5 hours × 3 intervals per hour + 1 = 16 points
    # Positions in reindexed series:
    # Index 0  (00:00): 1.0 (original position 0)
    # Index 1  (00:20): nan (new)
    # Index 2  (00:40): nan (new)  
    # Index 3  (01:00): nan (original position 1, was nan)
    # Index 4  (01:20): nan (new)
    # Index 5  (01:40): nan (new)
    # Index 6  (02:00): 3.0 (original position 2)
    # Index 7  (02:20): nan (new)
    # Index 8  (02:40): nan (new)
    # Index 9  (03:00): nan (original position 3, was nan)
    # Index 10 (03:20): nan (new)
    # Index 11 (03:40): nan (new)
    # Index 12 (04:00): nan (original position 4, was nan)
    # Index 13 (04:20): nan (new)
    # Index 14 (04:40): nan (new)
    # Index 15 (05:00): 6.0 (original position 5)

    # Gap Analysis:
    # 1.0 to 3.0: 5 NaNs, limit 6 -> interpolate
    # 3.0 to 6.0: 8 NaNs, limit 6 -> do not interpolate

    # fractions are used for precision
    expected_data = [1.0, 4.0/3.0, 5.0/3.0, 2.0, 7.0/3.0, 8.0/3.0, 3.0, nan, nan, nan, nan, nan, nan, nan, nan, 6.0]

    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=16, freq='1200s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 1200,  # 20 minutes
        "limit": 6
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_lower_interval_limit_7():
    

    test_data = [1.0, nan, 3.0, nan, nan, 6.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=6, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # reindexing at 15 minute intervals (900 seconds):
    # [1.0, nan, nan, nan, nan, nan, nan, nan, 3.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 6.0]

    # Gap Analysis:
    # 1.0 to 3.0: 7 NaNs, limit 7 -> interpolate
    # 3.0 to 6.0: 11 NaNs, limit 7 -> do not interpolate

    expected_data = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 6.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=21, freq='900s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 900,  # 15 minutes
        "limit": 7
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_lower_interval_start_nans():

    test_data = [nan, nan, 3.0, nan, 5.0, 6.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=6, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Reindexing at 30 minute intervals (1800s):
    # [nan, nan, nan, nan, 3.0, nan, nan, nan, 5.0, nan, 6.0]

    # Gap Analysis:
    # Start with NaNs: do not interpolate
    # 3.0 to 5.0: 3 NaNs, limit 3 -> interpolate
    # 5.0 to 6.0: 1 NaN, limit 3 -> interpolate

    expected_data = [nan, nan, nan, nan, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=11, freq='1800s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 1800,  # 30 minutes
        "limit": 3
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_lower_interval_end_nans():

    test_data = [1.0, 2.0, nan, nan, 5.0, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=6, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Reindexing at 30 minute intervals (1800s):
    # [1.0, nan, 2.0, nan, nan, nan, nan, nan, 5.0, nan, nan]

    # Gap Analysis:
    # 1.0 to 2.0: 1 NaN, limit 3 -> interpolate
    # 2.0 to 5.0: 5 NaNs, limit 3 -> do not interpolate
    # End with NaNs: do not interpolate

    expected_data = [1.0, 1.5, 2.0, nan, nan, nan, nan, nan, 5.0, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=11, freq='1800s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 1800,  # 30 minutes
        "limit": 3
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_lower_interval_start_end_nans():

    test_data = [nan, nan, 3.0, nan, 5.0, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=6, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Reindexing at 30 minute intervals (1800s):
    # [nan, nan, nan, nan, 3.0, nan, nan, nan, 5.0, nan, nan]

    # Gap Analysis:
    # Start with NaNs: do not interpolate
    # 3.0 to 5.0: 3 NaNs, limit 3 -> interpolate
    # End with NaNs: do not interpolate

    expected_data = [nan, nan, nan, nan, 3.0, 3.5, 4.0, 4.5, 5.0, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=11, freq='1800s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 1800,  # 30 minutes
        "limit": 3
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_lower_interval_no_nans():

    test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # reindex to 20 minute intervals (1200s):
    # [1.0, nan, nan, 2.0, nan, nan, 3.0, nan, nan, 4.0, nan, nan, 5.0]
    expected_data = [1.0, 1.3333333333, 1.6666666667, 2.0, 2.3333333333, 2.6666666667, 3.0, 3.3333333333, 3.6666666667, 4.0, 4.3333333333, 4.6666666667, 5.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='1200s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 1200,  # 20 minutes
        "limit": 3
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_lower_interval_all_nans():
    """
    This test ensures nothing happens when all values are NaNs. This is because we only interpolate
    the inside of 2 real values, never the start or end of a series. 

    This test uses a really big limit, to ensure that the interpolation does not happen. 
    """

    # 3 minutes of data, with a 1 minute interval
    test_data = [nan, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=3, freq='60s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # reindexing at 10 second intervals):
    # [nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]

    expected_data = [nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=13, freq='10s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 10,  # 10 seconds
        "limit": 1000  # big limit to ensure no interpolation happens
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


"""
This next section tests various NaN cases with a higher interpolation interval.

NOTE:: When reindexing at a higher interval, data that is not aligned with the new interval will be dropped from the series.
A warning will be logged when data is dropped due to reindexing.
"""

def test_higher_interval_basic():

    test_data = [1.0, nan, nan, nan, 5.0, nan, 7.0, nan, 9.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=9, freq='3600s')  
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # after reindexing at 2 hour intervals (7200 seconds), data gets dropped:
    # [1.0, nan, 5.0, 7.0, 9.0] from hour 0, hour 2, hour 4, hour 6, hour 8

    # Gap Analysis
    # 1.0 to 5.0: 1 NaN, limit 5 -> interpolate
    # this causes 3.0 to be interpolated in the reindexed data making
    # [1.0, 3.0, 5.0, 7.0, 9.0] 
    # then because of the joining to preserve data, the df looks like this:

    expected_data = [1.0, nan, 3.0, nan, 5.0, nan, 7.0, nan, 9.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=9, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,  # 2 hours
        "limit": 5
    }

    # call post process factory to do the post process
    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_higher_interval_limit_3():
    test_data = [1.0, nan, nan, nan, nan, nan, 7.0, nan, 9.0, nan, nan, nan, nan, nan, nan, 16.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=16, freq='3600s')  
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # After reindexing to 2-hour intervals (7200s):
    # Only even hours: 00:00->1.0, 02:00->nan, 04:00->nan, 06:00->7.0, 08:00->9.0, 
    # 10:00->nan, 12:00->nan, 14:00->nan, 15:00 gets dropped (not on 2-hr grid)
    # So reindexed: [1.0, nan, nan, 7.0, 9.0, nan, nan, nan]

    # Gap Analysis on reindexed data:
    # 1.0 to 7.0: 2 NaNs, limit 3 -> interpolate
    # 7.0 to 9.0: 0 NaNs -> no gap
    # 9.0 to end: 3 NaNs, no end value -> don't interpolate

    expected_data = [1.0, nan, 3.0, nan, 5.0, nan, 7.0, nan, 9.0, nan, nan, nan, nan, nan, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=16, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,  # 2 hours
        "limit": 3
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_higher_interval_7min_to_9min_reindexing(caplog):
    """
    This test is for checking what happens when the index and interpolation interval are aligned very badly. 
    In this case, the index is at 7 minute intervals, and the interpolation interval is at 9 minute intervals. 
    This causes a lot of data loss, and would generate a warning in the log about significant data loss.

    Considering that we are only interpolating over a small real life time period, minutes within a single hour, 
    the limit can be higher. In this test, a limit of 10 means we can interpolate up to 90 minutes of real time missing data, 
    which is fine in practice. 
    """
    
    # 7-minute intervals
    test_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='420s')  # 7 minutes
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # Create the expected index by combining original 7-minute intervals with 9-minute intervals
    # Original 7-minute timestamps: 0:00, 0:07, 0:14, 0:21, 0:28, 0:35, 0:42, 0:49, 0:56, 1:03
    original_timestamps = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='420s')
    
    # 9-minute reindexing timestamps: 0:00, 0:09, 0:18, 0:27, 0:36, 0:45, 0:54, 1:03
    reindex_timestamps = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=8, freq='540s')
    
    # Combine and sort all unique timestamps
    all_timestamps = original_timestamps.union(reindex_timestamps).sort_values()
    
    # After reindexing to 9-minute intervals:
    # Only values at 00:00 and 01:03 would be preserved
    # which causes the reindex array to look like
    # [1.0, nan, nan, nan, nan, nan, 10.0]
    # 00:00->1.0, 00:09->nan, 00:18->nan, 00:27->nan, 00:36->nan, 00:45->nan, 01:03->10.0
    #
    # Gap Analysis
    # 1.0 to 10.0: 5 NaNs, limit 10 -> interpolate
    # [1.0, 9/7 + 1, 18/7 + 1, 27/7 + 1, 36/7 + 1, 45/7 + 1, 54/7 + 1, 10.0]

    # 0:00 -> 1.0
    # 0:07 -> nan           (from original 7 minute interval)
    # 0:09 -> 9/7 + 1       (from reindexing to 9 minute interval)
    # 0:14 -> nan           (from original 7 minute interval)
    # 0:18 -> 18/7 + 1      (from reindexing to 9 minute interval)
    # 0:21 -> nan           (from original 7 minute interval)
    # 0:27 -> 27/7 + 1      (from reindexing to 9 minute interval)
    # 0:28 -> nan           (from original 7 minute interval)
    # 0:35 -> nan           (from original 7 minute interval)
    # 0:36 -> 36/7 + 1      (from reindexing to 9 minute interval)
    # 0:42 -> nan           (from original 7 minute interval)
    # 0:45 -> 45/7 + 1      (from reindexing to 9 minute interval)
    # 0:49 -> nan           (from original 7 minute interval)
    # 0:54 -> 54/7 + 1      (from reindexing to 9 minute interval)
    # 0:56 -> nan           (from original 7 minute interval)
    # 1:03 -> 10.0

    
    # combined 7 and 9 minutes timestamps, where the 9 minute intervals got interpolated
    # and the 7 minute stamps got dropped and replaced as nans
    expected_data = [1.0, nan, 9/7 + 1, nan, 18/7 + 1, nan, 27/7 + 1, nan, nan, 36/7 + 1, nan, 45/7 + 1, nan, 54/7 + 1, nan,  10.0] 
    expected_index = all_timestamps
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col", 
        "interpolation_interval": 540,  # 9 minutes
        "limit": 10
    }

    # Capture warning logs
    with caplog.at_level(logging.WARNING):
        result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    
    # Verify the data loss warning was logged
    warning_messages = [record.message for record in caplog.records if record.levelname == "WARNING"]
    assert any("Data loss during reindexing" in msg for msg in warning_messages)
    assert any("8 values lost in column 'test_col'" in msg for msg in warning_messages)

    # compare
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_higher_interval_start_nans():
    test_data = [nan, nan, nan, nan, 5.0, nan, 7.0, 8.0, 9.0, 10.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # After reindexing to 2-hour intervals:
    # 00:00->nan, 02:00->nan, 04:00->5.0, 06:00->7.0, 08:00->9.0
    # Reindexed: [nan, nan, 5.0, 7.0, 9.0]

    # Gap Analysis:
    # Start with NaNs: don't interpolate
    # 5.0 to 7.0: 0 NaNs -> no gap
    # 7.0 to 9.0: 0 NaNs -> no gap

    expected_data = [nan, nan, nan, nan, 5.0, nan, 7.0, nan, 9.0, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,  # 2 hours
        "limit": 5
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_higher_interval_end_nans():
    test_data = [1.0, nan, nan, nan, nan, nan, nan, nan, 9.0, nan, 11.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 22.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=22, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # After reindexing to 2-hour intervals:
    # 00:00->1.0, 02:00->nan, 04:00->nan, 06:00->nan, 08:00->9.0, 10:00->11.0, 
    # 12:00->nan, 14:00->nan, 16:00->nan, 18:00->nan, 20:00->nan
    # Note: 22.0 at hour 21 gets dropped (not on 2-hr grid)
    # Reindexed: [1.0, nan, nan, nan, 9.0, 11.0, nan, nan, nan, nan, nan]

    # Gap Analysis:
    # 1.0 to 9.0: 3 NaNs, limit 5 -> interpolate  
    # 9.0 to 11.0: 0 NaNs -> no gap
    # 11.0 to end: NaNs at end -> don't interpolate

    expected_data = [1.0, nan, 3.0, nan, 5.0, nan, 7.0, nan, 9.0, nan, 11.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=22, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,  # 2 hours
        "limit": 5
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_higher_interval_start_end_nans():
    test_data = [nan, nan, 3.0, nan, 5.0, nan, nan, 8.0, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # After reindexing to 2-hour intervals:
    # 00:00->nan, 02:00->3.0, 04:00->5.0, 06:00->nan, 08:00->nan
    # Reindexed: [nan, 3.0, 5.0, nan, nan]

    # Gap Analysis:
    # Start with NaNs: don't interpolate
    # 3.0 to 5.0: 0 NaNs -> no gap
    # 5.0 to end: NaNs at end -> don't interpolate

    expected_data = [nan, nan, 3.0, nan, 5.0, nan, nan, nan, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,  # 2 hours
        "limit": 3
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)



def test_higher_interval_no_nan():
    test_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # After reindexing to 2-hour intervals:
    # 00:00->1.0, 02:00->3.0, 04:00->5.0, 06:00->7.0, 08:00->9.0
    # Reindexed: [1.0, 3.0, 5.0, 7.0, 9.0] (no NaNs, no interpolation needed)

    expected_data = [1.0, nan, 3.0, nan, 5.0, nan, 7.0, nan, 9.0, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,  # 2 hours
        "limit": 3
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_higher_interval_all_nans():
    test_data = [nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # After reindexing to 2-hour intervals:
    # All values remain NaN, no interpolation possible

    expected_data = [nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,  # 2 hours
        "limit": 5
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_higher_interval_large_gap():
    test_data = [1.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 16.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=16, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)

    # After reindexing to 3-hour intervals:
    # 00:00->1.0, 03:00->nan, 06:00->nan, 09:00->nan, 12:00->nan, 15:00->16.0
    # Reindexed: [1.0, nan, nan, nan, nan, 16.0]

    # Gap Analysis:
    # 1.0 to 16.0: 4 NaNs, limit 2 -> don't interpolate

    expected_data = [1.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, 16.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=16, freq='3600s')
    expected_df = DataFrame({'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 10800,  # 3 hours
        "limit": 2
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


"""
This last section tests that the validate_args function correctly raises exceptions for various invalid inputs.
"""

def test_validate_args_invalid_dataframe_type():
    """Test that validate_args raises TypeError for non-DataFrame input."""
    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": 3
    }
    
    with pytest.raises(TypeError):
        result_df = post_process_factory("Hello World", "LinearInterpolation", kwargs)


def test_validate_args_empty_dataframe():
    """Test that validate_args raises ValueError for empty DataFrame."""
    empty_df = DataFrame()
    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": 3
    }
    
    with pytest.raises(ValueError):
        result_df = post_process_factory(empty_df, "LinearInterpolation", kwargs)


def test_validate_args_non_datetime_index():
    """Test that validate_args raises TypeError for non-DatetimeIndex."""
    invalid_index_df = DataFrame({'test_col': [1.0, 2.0, 3.0, 4.0, 5.0]}, index=[1, 2, 3, 4, 5])
    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": 3
    }
    
    with pytest.raises(TypeError):
        result_df = post_process_factory(invalid_index_df, "LinearInterpolation", kwargs)


def test_validate_args_invalid_column_name_type():
    """Test that validate_args raises TypeError for non-string column name."""
    test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)
    
    kwargs = {
        "col_name": 123,  # Invalid type
        "interpolation_interval": 3600,
        "limit": 3
    }
    
    with pytest.raises(TypeError):
        result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)


def test_validate_args_column_not_found():
    """Test that validate_args raises KeyError for non-existent column."""
    test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)
    
    kwargs = {
        "col_name": "nonexistent_col",
        "interpolation_interval": 3600,
        "limit": 3
    }
    
    with pytest.raises(KeyError):
        result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)


def test_validate_args_invalid_interpolation_interval_type():
    """Test that validate_args raises TypeError for non-integer interpolation_interval."""
    test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)
    
    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": "Hello World",  # Invalid type
        "limit": 3
    }
    
    with pytest.raises(TypeError):
        result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)


def test_validate_args_invalid_limit_type():
    """Test that validate_args raises TypeError for non-integer limit."""
    test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)
    
    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": "Hello World"  # Invalid type
    }
    
    with pytest.raises(TypeError):
        result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)


def test_validate_args_negative_interpolation_interval():
    """Test that validate_args raises ValueError for negative interpolation_interval."""
    test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)
    
    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": -100,  # Invalid value
        "limit": 3
    }
    
    with pytest.raises(ValueError):
        result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)


def test_validate_args_negative_limit():
    """Test that validate_args raises ValueError for negative limit."""
    test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame({'test_col': test_data}, index=test_index)
    
    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": -1  # Invalid value
    }
    
    with pytest.raises(ValueError):
        result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

