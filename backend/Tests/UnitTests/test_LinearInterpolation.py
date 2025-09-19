# -*- coding: utf-8 -*-
#test_LinearInterpolation.py
#-------------------------------
# Created By: Christian Quintero
# Last Updated: 09/16/2025
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

    We can interpolate a gap of 6 hours in between real values though.
    """
    test_data = [nan, 1.0, 2.0, nan, nan, nan, nan, nan, 8.0, nan]
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=10, freq='3600s')
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    expected_data = [nan, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, nan]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=10, freq='3600s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": 21600                   # 6 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_limit_6_hours():
    """
    Tests that gaps of 6 hours are interpolated as expected.
    """

    test_data = [0.0, nan, nan, nan, nan, nan, 6.0, nan, nan, nan, nan, nan, nan, nan, 14.0, nan, nan, nan, 18.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=19, freq='3600s')
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # analysis
    # 00:00 - 06:00 = 6 hour gap -> interpolate, exactly at the limit
    # 06:00 - 14:00 = 8 hour gap -> do not interpolate, over the limit
    # 14:00 - 18:00 = 4 hour gap -> interpolate, under the limit
    expected_data = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, nan, nan, nan, nan, nan, nan, nan, 14.0, 15.0, 16.0, 17.0, 18.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=19, freq='3600s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 3600,
        "limit": 21600                   # 6 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_limit_3_hours():
    """
    Tests that gaps of 3 hours are interpolated as expected using a 30 minute frequency.

    Ex) 00:00 00:30 01:00 01:30 02:00 02:30 03:00... 
    where 0.0 is at hour 00:00, 3.0 is at hour 03:00, 5.0 is at hour 05:00, and 9.0 is at hour 09:00
    """
    test_data = [0.0, nan, nan, nan, nan, nan, 3.0, nan, nan, nan, 5.0, nan, nan, nan, nan, nan, nan, nan, 9.0]
    test_index = date_range(datetime(2025, 1, 1, 0, 0), periods=19, freq='1800s')
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # analysis
    # 00:00 - 03:00 = 3 hour gap -> interpolate, exactly at the limit
    # 03:00 - 05:00 = 2 hour gap -> interpolate, under the limit
    # 05:00 - 09:00 = 4 hour gap -> do not interpolate, over the limit
    expected_data = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, nan, nan, nan, nan, nan, nan, nan, 9.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=19, freq='1800s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 1800,    # 30 minutes
        "limit": 10800                     # 3 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


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

    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


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
        "limit": 21600                   # 6 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)

    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_higher_interval():
    """
    When interpolating from a lower frequency to a higher frequency, the union of the original and new timestamps is taken.
    Then interpolation is performed on the new timestamps depending on how many hours (in seconds) we can interpolate.
    Finally, the data is reindexed to the requested frequency and returns a series where timestamps that landed on the interval
    are kept and original timestamps (regardless of whether they had a value or a nan) are set to nan if they did not land on the interval.
    """

    # data at random intervals
    # hours 00:00, 02:00, 04:00, 05:00, 10:00, 15:00
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

    # reindexed and union to every 3 hours (10800 seconds)
    # [0.0,  2.0,  nan,  4.0,  5.0,  nan,  nan,  10.0  nan  15.0] 
    # 00:00 02:00 03:00 04:00 05:00 06:00 09:00 10:00 12:00 15:00
    #
    #
    # 02:00 to 04:00 = 2 hour gap -> interpolate
    # 05:00 to 10:00 = 5 hour gap -> do not interpolate
    # 10:00 to 15:00 = 5 hour gap -> do not interpolate
    # 
    # interpolated data
    # [0.0, 2.0, 3.0, 4.0, 5.0, nan, nan, 10.0, nan, 15.0]
    #
    # final reindex to every 3 hours (keep values on 3 hour intervals and insert nans elsewhere)
    # 00:00 02:00 03:00 04:00 05:00 06:00 09:00 10:00 12:00 15:00
    #  0.0   nan   3.0   nan   nan    nan   nan   nan  nan  15.0

    expected_data = [0.0, nan, 3.0, nan, nan, nan, nan, nan, nan, 15.0]
    expected_index = [
        datetime(2025, 1, 1, 0, 0),  # original
        datetime(2025, 1, 1, 2, 0),  # original
        datetime(2025, 1, 1, 3, 0),  # new
        datetime(2025, 1, 1, 4, 0),  # original
        datetime(2025, 1, 1, 5, 0),  # original
        datetime(2025, 1, 1, 6, 0),  # new
        datetime(2025, 1, 1, 9, 0),  # new
        datetime(2025, 1, 1, 10, 0), # original
        datetime(2025, 1, 1, 12, 0), # new
        datetime(2025, 1, 1, 15, 0), # original
    ]
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col", 
        "interpolation_interval": 10800,    # 3 hours
        "limit": 14400                      # 4 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)


def test_higher_irregular_interval():
    """
    Tests interpolation when the original data has an irregular interval and we reindex to a higher frequency.
    When reindexing, we ensure that the reindex starts with the first timestamp originally present, and ends with the last timestamp originally present.

    In this case, the first data point is 00:10 so the first reindex will add timestamps every 2 hours after that
    (02:10, 04:10, etc) until the last timestamp of 09:00.

    In the final reindex, we only keep the values that landed on the 2 hour intervals (00:10, 02:10, 04:10, 06:10, 08:10) and all other 
    original timestamps that didn't land on the interval (01:40, 02:15, 04:50, 09:00) are set to nan. 
    """

    # Original irregular data points
    test_index = [
        datetime(2025, 1, 1, 0, 10),
        datetime(2025, 1, 1, 1, 40),
        datetime(2025, 1, 1, 2, 15),
        datetime(2025, 1, 1, 4, 50),
        datetime(2025, 1, 1, 9, 0),
    ]
    test_data = [0.0, 1.0, 2.0, 5.0, 9.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # Original
    # 00:10 01:40 02:15 04:50 09:00
    #  0.0   1.0   2.0   5.0   9.0
    #
    # reindex to every 2 hours (7200 seconds)
    # 00:10 01:40 02:10 02:15 04:10 04:50 06:10 08:10 09:00 
    # 0.0    1.0   nan   2.0   nan   5.0   nan   nan   9.0   
    #
    # 01:40 to 02:15 = 35 min gap -> interpolate
    # 02:15 to 04:50 = 2 hr 35 min gap -> interpolate
    # 04:50 to 09:00 = 4 hr 10 min gap -> do not interpolate
    #
    # interpolated data
    # 00:10 01:40 02:10 02:15 04:10 04:50 06:10 08:10 09:00 
    # 0.0    1.0  1.857  2.0  4.225  5.0   nan   nan   9.0   
    #
    # final reindex to every 2 hours (keep values on 2 hour intervals and insert nans elsewhere)
    # 00:10 01:40 02:10 02:15 04:10 04:50 06:10 08:10 09:00 
    #  0.0   nan  1.857  nan  3.857  nan   nan   nan   nan  
    expected_data = [0.0, nan, 1.857142857, nan, 4.225806451, nan, nan, nan, nan]
    expected_index = [
        datetime(2025, 1, 1, 0, 10), # original timestamp   
        datetime(2025, 1, 1, 1, 40), # original timestamp
        datetime(2025, 1, 1, 2, 10), # new from reindexing
        datetime(2025, 1, 1, 2, 15), # original timestamp
        datetime(2025, 1, 1, 4, 10), # new from reindexing
        datetime(2025, 1, 1, 4, 50), # original timestamp
        datetime(2025, 1, 1, 6, 10), # new from reindexing
        datetime(2025, 1, 1, 8, 10), # new from reindexing
        datetime(2025, 1, 1, 9, 0),  # original timestamp
    ]
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,   # 2 hours
        "limit": 10800                    # 3 hours 
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    print(result_df)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_lower_interval():
    """
    Tests interpolation when reindexing to a lower interval (30 minutes).
    This is a simpler test to ensure lower interval reindexing works as expected.
    All original timestamps land on the 30 minute intervals so no original timestamps are set to nan in the final reindex.
    """
    
    test_index = [
        datetime(2025, 1, 1, 0, 0),      
        datetime(2025, 1, 1, 2, 0), 
        datetime(2025, 1, 1, 5, 0),   
        datetime(2025, 1, 1, 6, 0),     
    ]
    test_data = [0.0, 2.0, 5.0, 6.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # original
    # 00:00 02:00 05:00 06:00
    # 0.0    2.0   5.0   6.0
    #
    # reindex to every 30 minutes (1800 seconds)
    # 00:00 00:30 01:00 01:30 02:00 02:30 03:00 03:30 04:00 04:30 05:00 05:30 06:00
    # 0.0    nan   nan   nan   2.0   nan   nan   nan   nan    nan  5.0   nan   6.0
    #
    # 00:00 to 02:00 = 2 hour gap -> interpolate
    # 02:00 to 05:00 = 3 hour gap -> interpolate
    # 05:00 to 06:00 = 1 hour gap -> interpolate
    #
    # interpolated data
    # 00:00 00:30 01:00 01:30 02:00 02:30 03:00 03:30 04:00 04:30 05:00 05:30 06:00
    # 0.0   0.5   1.0   1.5   2.0   2.5   3.0   3.5   4.0   4.5   5.0   5.5   6.0
    # 
    # final reindex to every 30 minutes (keep values on 30 minute intervals and insert nans elsewhere)
    # 00:00 00:30 01:00 01:30 02:00 02:30 03:00 03:30 04:00 04:30 05:00 05:30 06:00
    # 0.0   0.5   1.0   1.5   2.0   2.5   3.0   3.5   4.0   4.5   5.0   5.5   6.0
    expected_data = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), periods=13, freq='1800s')
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 1800,    # 30 minutes
        "limit": 10800                     # 3 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_lower_irregular_interval():
    """
    Tests interpolation when the original data has an irregular interval.
    """

    test_interval = [
        datetime(2025, 1, 1, 0, 15), # 00:15
        datetime(2025, 1, 1, 1, 15), # 01:15
        datetime(2025, 1, 1, 1, 45), # 01:45
        datetime(2025, 1, 1, 2, 28), # 02:28
        datetime(2025, 1, 1, 3, 9),  # 03:09
    ]

    test_data = [0.0, 1.0, 2.0, 3.0, 4.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_interval)

    # reindex to every 30 minutes (1800 seconds)
    # 00:15 00:45 01:15 01:45 02:15 02:28 02:45 03:09
    # 0.0    nan   1.0   2.0   nan   3.0   nan   4.0
    #
    # 00:15 to 01:15 = 1 hour gap -> interpolate
    # 01:45 to 02:28 = 43 min gap -> interpolate
    # 02:28 to 03:09 = 41 min gap -> interpolate
    #
    # interpolated data
    # 00:15 00:45 01:15 01:45 02:15 02:28 02:45 03:09
    # 0.0   0.5   1.0   2.0   2.4   3.0   3.5   4.0
    #
    # reindex to every 30 minutes (keep values on 30 minute intervals and insert nans elsewhere)
    # 00:15 00:45 01:15 01:45 02:15 02:28 02:45 03:09
    # 0.0    0.5   1.0   2.0  2.697   nan   3.414    nan
    expected_data = [0.0, 0.5, 1.0, 2.0, 2.697674419, nan, 3.414634146, nan]    
    expected_index = [
        datetime(2025, 1, 1, 0, 15), # original timestamp
        datetime(2025, 1, 1, 0, 45), # new from reindexing
        datetime(2025, 1, 1, 1, 15), # original timestamp
        datetime(2025, 1, 1, 1, 45), # original timestamp
        datetime(2025, 1, 1, 2, 15), # new from reindexing
        datetime(2025, 1, 1, 2, 28), # original timestamp
        datetime(2025, 1, 1, 2, 45), # new from reindexing
        datetime(2025, 1, 1, 3, 9),  # original timestamp
    ]
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 1800,      # 30 minutes
        "limit": 3600                       # 1 hour
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_limit_integrity():
    """
    For lack of a better name, this test ensures that the limit works exactly as inteded when there is a
    gap that is 1 second over the limit and should not be interpolated.
    This test is also another example of ensuring reindexing works as expected when using random timestamps
    and reindexing to a random interval.
    """

    # random timestamps
    test_index = [
        datetime(2025, 1, 1, 0, 6),
        datetime(2025, 1, 1, 0, 17),
        datetime(2025, 1, 1, 0, 30),
        datetime(2025, 1, 1, 0, 45),
        datetime(2025, 1, 1, 1, 0),
        datetime(2025, 1, 1, 1, 56),
        datetime(2025, 1, 1, 2, 10),
        datetime(2025, 1, 1, 2, 39)      
    ]
    test_data = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # reindex to every 11 minutes (660 seconds)
    # 00:06 00:17 00:28 00:30 00:39 00:45 00:50 01:00 01:01 01:12 01:23 01:34 01:45 01:56 02:07 02:10 02:18 02:29 02:39
    # 0.0   1.0   nan   2.0   nan   3.0   nan   4.0   nan   nan   nan   nan   nan   5.0   nan    6.0   nan   nan   7.0 
    #
    # 00:17 to 00:30 = 13 min gap -> interpolate
    # 00:30 to 00:45 = 15 min gap -> interpolate
    # 00:45 to 01:00 = 15 min gap -> interpolate
    # 01:00 to 01:56 = 56 min gap -> do not interpolate (1 second over the limit of 3359 seconds)
    # 01:56 to 02:10 = 14 min gap -> interpolate
    # 02:10 to 02:39 = 29 min gap -> interpolate
    #
    # interpolated data
    # 00:06 00:17 00:28 00:30 00:39 00:45 00:50 01:00 01:01 01:12 01:23 01:34 01:45 01:56 02:07 02:10 02:18 02:29 02:39
    # 0.0   1.0  1.846  2.0  2.600  3.0  3.333  4.0   nan   nan   nan   nan   nan   5.0  5.785   6.0  6.275 6.655 7.0
    #
    # final reindex to every 11 minutes (keep values on 11 minute intervals and insert nans elsewhere)
    # 00:06 00:17 00:28 00:30 00:39 00:45 00:50 01:00 01:01 01:12 01:23 01:34 01:45 01:56 02:07 02:10 02:18 02:29 02:39
    # 0.0   1.0   1.846  nan  2.600 nan   3.333  nan   nan   nan   nan   nan   nan   5.0  5.785  nan  6.275 6.655  nan

    expected_data = [0.0, 1.0, 1.846153846, nan, 2.600000000, nan, 3.333333333,
                      nan, nan, nan, nan, nan, nan, 5.0, 5.785714286, nan, 6.275862069, 6.655172414, nan]
    expected_index = [
        datetime(2025, 1, 1, 0, 6),   # original timestamp
        datetime(2025, 1, 1, 0, 17),  # original timestamp
        datetime(2025, 1, 1, 0, 28),  # new from reindexing
        datetime(2025, 1, 1, 0, 30),  # original timestamp
        datetime(2025, 1, 1, 0, 39),  # new from reindexing
        datetime(2025, 1, 1, 0, 45),  # original timestamp
        datetime(2025, 1, 1, 0, 50),  # new from reindexing
        datetime(2025, 1, 1, 1, 0),   # original timestamp
        datetime(2025, 1, 1, 1, 1),   # new from reindexing
        datetime(2025, 1, 1, 1, 12),  # new from reindexing
        datetime(2025, 1, 1, 1, 23),  # new from reindexing
        datetime(2025, 1, 1, 1, 34),  # new from reindexing
        datetime(2025, 1, 1, 1, 45),  # new from reindexing
        datetime(2025, 1, 1, 1, 56),  # original timestamp
        datetime(2025, 1, 1, 2, 7),   # new from reindexing
        datetime(2025, 1, 1, 2, 10),  # original timestamp
        datetime(2025, 1, 1, 2, 18),  # new from reindexing
        datetime(2025, 1, 1, 2, 29),  # new from reindexing
        datetime(2025, 1, 1, 2, 39),  # original timestamp
    ]
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 660,      # 11 minutes
        "limit": 3359                       # 55 minutes and 59 seconds
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)







