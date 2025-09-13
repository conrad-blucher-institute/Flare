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


def test_start_end_nans():
    """
    Ensures no interpolation happens when NaNs are at the start or end of the data.
    """
    test_data = [nan, 2, nan, 4, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    expected_data = [nan, 2, 3, 4, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=5, freq='3600s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": 7200                   # 2 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)


def test_limit_5_hours():
    """
    Tests that nan gaps that last 5 hours or less are interpolated, while gaps longer than 5 hours are not.
    """
    test_data = [1.0, nan, nan, nan, nan, nan, 7.0, nan, nan, nan, nan, 12.0, nan, nan, nan, nan, nan, nan, 19.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=19, freq='3600s')
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # analysis
    # 5 hours of NaNs between 1.0 and 7.0 -> interpolate
    # 4 hours of NaNs between 7.0 and 12.0 -> interpolate
    # 6 hours of NaNs between 12.0 and 19.0 -> do not interpolate (limit is 5 hours)
    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, nan, nan, nan, nan, nan, nan, 19.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=19, freq='3600s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": 18000                   # 5 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)


def test_limit_3_hours():
    """
    Tests that nan gaps that last 3 hours or less are interpolated, while gaps longer than 3 hours are not.
    """
    test_data = [1.0, nan, nan, 4.0, nan, nan, nan, nan, 9.0, nan, nan, nan, 13.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=13, freq='3600s')
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # analysis
    # 2 hours of NaNs between 1.0 and 4.0 -> interpolate
    # 4 hours of NaNs between 4.0 and 9.0 -> do not interpolate (limit is 3 hours)
    # 3 hours of NaNs between 9.0 and 13.0 -> interpolate
    expected_data = [1.0, 2.0, 3.0, 4.0, nan, nan, nan, nan, 9.0, 10.0, 11.0, 12.0, 13.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=13, freq='3600s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": 10800                   # 3 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)


def test_no_nans():
    """
    Ensures no interpolation happens when there are no NaNs in the data.
    """
    test_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    expected_data = [1.0, 2.0, 3.0, 4.0, 5.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=5, freq='3600s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": 7200                   # 2 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)


def test_all_nans():
    """
    Ensures no interpolation happens when all values are NaN. This is because we only
    interpolate between real values.
    """
    test_data = [nan, nan, nan, nan, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=5, freq='3600s')
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    expected_data = [nan, nan, nan, nan, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=5, freq='3600s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": 7200                   # 2 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)


def test_higher_interval():
    """
    When interpolating from a lower frequency to a higher frequency, the union of original and new timestamps is taken.
    Then interpolation is performed on the new timestamps depending on how many hours (in seconds) we can interpolate.
    """

    # data at random intervals
    test_index = [
        datetime(2025, 1, 1, 0, 0),
        datetime(2025, 1, 1, 2, 0),
        datetime(2025, 1, 1, 4, 0),
        datetime(2025, 1, 1, 5, 0),
        datetime(2025, 1, 1, 10, 0),
        datetime(2025, 1, 1, 15, 0),
    ]
    test_data = [0.0, 2.0, 4.0, 5.0, 10.0, 15.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # reindexed to every 3 hours (10800 seconds)
    # reindexing to 3 hours:
    # [0.0, nan, nan, nan, nan, 15.0] for timestamps 00:00 03:00 06:00 09:00 12:00 15:00
    #
    # after the union of indices:
    # [0.0, 2.0, nan, 4.0, 5.0, nan, nan, 10.0, nan, 15.0]
    # for timestamps 00:00 02:00 03:00 04:00 05:00 06:00 09:00 10:00 12:00 15:00
    #
    # 1 hour gap from 02:00 to 04:00: hour 03:00 is missing -> interpolate
    # 4 hour gap from 05:00 to 10:00, due to 06:00 and 09:00 missing -> don't interpolate bc from hour 06:00 to 10:00 is 4 hours of missing data
    # 3 hour gap from 10.0 to 15.0 from missing 12:00 -> interpolate
    expected_data = [0.0, 2.0, 3.0, 4.0, 5.0, nan, nan, 10.0, 12.0, 15.0]
    expected_index = [
        datetime(2025, 1, 1, 0, 0),     # from original index
        datetime(2025, 1, 1, 2, 0),     # from original index
        datetime(2025, 1, 1, 3, 0),     # new from reindexing
        datetime(2025, 1, 1, 4, 0),     # from original index
        datetime(2025, 1, 1, 5, 0),     # from original index
        datetime(2025, 1, 1, 6, 0),     # new from reindexing
        datetime(2025, 1, 1, 9, 0),     # new from reindexing
        datetime(2025, 1, 1, 10, 0),    # from original index
        datetime(2025, 1, 1, 12, 0),    # new from reindexing
        datetime(2025, 1, 1, 15, 0)     # from original index
    ]
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col", 
        "interpolation_interval": 10800,    # 3 hours
        "limit": 10800                      # 3 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)



def test_preserve_original_values_when_reindexing():
    """
    Ensures that when reindexing from a lower frequency (1h) to a higher interval (2h),
    all original timestamps are still present and all original values remain unchanged.
    """
    test_data = [1.0, nan, nan, 4.0, nan, nan, nan, nan, 9.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=9, freq='3600s')
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,  # reindex to 2-hour intervals
        "limit": 21600                   # 6 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # 1. All original timestamps must be present
    for ts in test_df.index:
        assert ts in result_df.index, f"Original timestamp {ts} missing after reindexing."

    # 2. Original non-NaN values must be preserved exactly
    for ts, val in test_df['test_col'].dropna().items():
        result_val = result_df.loc[ts, 'test_col']
        assert result_val == val, f"Original value at {ts} changed: expected {val}, got {result_val}"


def test_lower_interval():
    """
    When interpolating from a higher frequency to a lower frequency, nans are inserted into the reindexed data.
    Linear interpolation is performed on this new array depending on how many hours (in seconds) we can interpolate.
    Finally, the original timestamps are outer joined with the new interpolated timestamps to preserve the original timestamps
    """

    test_data = [1.0, nan, nan, 4.0, nan, nan, nan, nan, 9.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=9, freq='3600s')  
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # reindexed to every 30 minutes (1800 seconds)
    # reindexed_data = [1.0, nan, nan, nan, nan, nan, 4.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 9.0]
    #
    # 2.5 hours from 1.0 to 4.0 -> interpolate
    # 4.5 hours from 4.0 to 9.0 -> don't interpolate

    # interpolated_data = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 9.0]

    expected_data = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, 9.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=17, freq='1800s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 1800,    # 30 minutes
        "limit": 10800                     # 3 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)


def test_preserve_original_values_when_downsampling():
    """
    Ensures that when reindexing from a higher frequency (30 min) to a lower interval (2h),
    all original timestamps are still present and all original values remain unchanged.
    """
    # Original data at 30-minute intervals
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=9, freq='1800s')
    test_data = [1.0, nan, 2.0, nan, 3.0, nan, 4.0, nan, 5.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,  # reindex to 2-hour intervals
        "limit": 14400                   # 4 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    # 1. All original timestamps must be present
    for ts in test_df.index:
        assert ts in result_df.index, f"Original timestamp {ts} missing after reindexing."

    # 2. Original non-NaN values must be preserved exactly
    for ts, val in test_df['test_col'].dropna().items():
        result_val = result_df.loc[ts, 'test_col']
        assert result_val == val, f"Original value at {ts} changed: expected {val}, got {result_val}"


def test_irregular_timestamps():
    """
    Tests interpolation on a DataFrame with irregular timestamps. The data has values for certain hours, then we reindex to every hour,
    adding nans where we don't have data for that hour. Then we interpolate based on the limit.
    """

    test_index = [
        datetime(2025, 1, 1, 0, 0),                         
        datetime(2025, 1, 1, 1, 0),
        datetime(2025, 1, 1, 2, 0),
        datetime(2025, 1, 1, 4, 0), # 1 hour nan gap from previous,
        datetime(2025, 1, 1, 7, 0), # 2 hour nan gap from previous,
        datetime(2025, 1, 1, 8, 0), 
        datetime(2025, 1, 1, 14, 0), # 6 hour nan gap from previous,
        datetime(2025, 1, 1, 21, 0)  # 7 hour nan gap from previous,
    ]
    test_data = [0.0, 1.0, 2.0, 4.0, 7.0, 8.0, 14.0, 21.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # reindex to every hour (3600 seconds)
    # reindexed_data = [0.0, 1.0, 2.0, nan, 4.0, nan, nan, 7.0, 8.0, nan, nan, nan, nan, nan, 14.0, nan, nan, nan, nan, nan, nan, 21.0]

    # 1 hour gap from 2.0 to 4.0 -> interpolate
    # 2 hour gap from 4.0 to 7.0 -> interpolate
    # 5 hour gap from 8.0 to 14.0 -> interpolate
    # 6 hour gap from 14.0 to 21.0 -> don't interpolate (limit is 5 hours)

    expected_data = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, nan, nan, nan, nan, nan, nan, 21.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=22, freq='3600s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,    # 1 hour
        "limit": 18000                     # 5 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)


def test_irregular_timestamps_higher_interval():
    """
    Tests interpolation when reindexing to a higher interval (3 hours).
    Original data has irregular timestamps. After reindexing, only timestamps
    that fall exactly on the 3-hour grid are kept, then interpolation is applied
    according to the limit.
    """

    test_index = [
        datetime(2025, 1, 1, 0, 0),                         
        datetime(2025, 1, 1, 1, 0),
        datetime(2025, 1, 1, 2, 0),
        datetime(2025, 1, 1, 4, 0), # 1 hour nan gap from previous,
        datetime(2025, 1, 1, 7, 0), # 2 hour nan gap from previous,
        datetime(2025, 1, 1, 8, 0), 
        datetime(2025, 1, 1, 14, 0), # 6 hour nan gap from previous,
        datetime(2025, 1, 1, 21, 0)  # 7 hour nan gap from previous,
    ]
    test_data = [0.0, 1.0, 2.0, 4.0, 7.0, 8.0, 14.0, 21.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # reindex to every 2 hours (7200 seconds)
    # reindexed_data = [0.0, 2.0, 4.0, nan, 8.0, nan, nan, 14.0, nan, nan, nan]

    # 2 hour gap from 4.0 to 6.0 -> interpolate
    # 4 hour gap from 8.0 to 14.0 -> interpolate
    # ends with nans -> don't interpolate

    # interpolated data = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, nan, nan, nan]

    # join back with original
    
    expected_index = [
        datetime(2025, 1, 1, 0, 0),     # from original timestamp
        datetime(2025, 1, 1, 1, 0),     # from original timestamp
        datetime(2025, 1, 1, 2, 0),     # from original timestamp
        datetime(2025, 1, 1, 4, 0),     # from original timestamp
        datetime(2025, 1, 1, 6, 0),     # from reindexed timestamp
        datetime(2025, 1, 1, 7, 0),     # from original timestamp
        datetime(2025, 1, 1, 8, 0),     # from original timestamp
        datetime(2025, 1, 1, 10, 0),    # from reindexed timestamp
        datetime(2025, 1, 1, 12, 0),    # from reindexed timestamp                    
        datetime(2025, 1, 1, 14, 0),    # from original timestamp
        datetime(2025, 1, 1, 16, 0),    # from reindexed timestamp
        datetime(2025, 1, 1, 18, 0),    # from reindexed timestamp
        datetime(2025, 1, 1, 20, 0),    # from reindexed timestamp
        datetime(2025, 1, 1, 21, 0),    # from original timestamp
    ]
    expected_data = [0.0, 1.0, 2.0, 4.0, 6.0, 7.0, 8.0, 10.0, 12.0, 14.0, nan, nan, nan, 21.0]
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,    # 2 hours
        "limit": 14400                    # 4 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)


