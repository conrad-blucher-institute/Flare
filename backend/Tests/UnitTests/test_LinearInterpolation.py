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

    # reindexed to every 3 hours (10800 seconds)
    # [0.0,  nan,  nan  nan,  nan   15.0]
    # 00:00 03:00 06:00 09:00 12:00 15:00
    #
    # after the union of indices:
    # [0.0,  2.0,  nan,  4.0,  5.0,  nan,  nan, 10.0, nan,  15.0]
    # 00:00 02:00 03:00 04:00 05:00 06:00 09:00 10:00 12:00 15:00
    #
    # 02:00 to 04:00 = 2 hour gap -> interpolate
    # 05:00 to 10:00 = 5 hour gap -> do not interpolate
    # 10:00 to 15:00 = 5 hour gap -> do not interpolate
    expected_data = [0.0, 2.0, 3.0, 4.0, 5.0, nan, nan, 10.0, nan, 15.0]
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
        "limit": 14400                      # 4 hours
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-5, check_freq=False)


def test_higher_irregular_interval():
    """
    Tests interpolation when the original data has an irregular interval and we reindex to a higher frequency.
    """

    # Original irregular data points
    test_index = [
        datetime(2025, 1, 1, 0, 10),
        datetime(2025, 1, 1, 1, 40),
        datetime(2025, 1, 1, 2, 15),
        datetime(2025, 1, 1, 4, 50),
        datetime(2025, 1, 1, 9, 0),
    ]
    test_data = [0.0, 1.5, 2.0, 5.0, 9.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # Reindex every 2 hours (7200 seconds)
    # New grid would be: 00:10, 02:10, 04:10, 06:10, 08:10
    # After union with original: 
    # 00:10 (0.0), 01:40 (1.5), 02:10 (NaN), 02:15 (2.0), 04:10 (NaN),
    # 04:50 (5.0), 06:10 (NaN), 08:10 (NaN), 09:00 (9.0)
    #
    # Gap analysis:
    # - 01:40 → 02:15 = 35 min → interpolate
    # - 02:15 → 04:50 ≈ 2h35m → do not interpolate (over 2h limit)
    # - 04:50 → 09:00 = 4h10m → do not interpolate
    expected_index = [
        datetime(2025, 1, 1, 0, 10),  # original
        datetime(2025, 1, 1, 1, 40),  # original
        datetime(2025, 1, 1, 2, 10),   # new
        datetime(2025, 1, 1, 2, 15),  # original
        datetime(2025, 1, 1, 4, 10),   # new
        datetime(2025, 1, 1, 4, 50),  # original
        datetime(2025, 1, 1, 6, 10),   # new
        datetime(2025, 1, 1, 8, 10),   # new
        datetime(2025, 1, 1, 9, 0),   # original
    ]
    expected_data = [
        0.0,    
        1.5,   
        1.9285714285714286,   
        2.0,    
        nan,    
        5.0,    
        nan,   
        nan,    
        9.0,    
    ]
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 7200,   # 2 hours
        "limit": 7200                     # 2 hours max interpolation gap
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)


def test_lower_interval():
    """
    Tests interpolation when reindexing to a lower interval (30 minutes).
    """
    
    test_index = [
        datetime(2025, 1, 1, 0, 0),      
        datetime(2025, 1, 1, 2, 0),    
        datetime(2025, 1, 1, 6, 0),     
    ]
    test_data = [0.0, 2.0, 6.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_index)

    # reindex to every 30 minutes (1800 seconds)
    # reindexed_data = [0.0, nan, nan, nan, 2.0, nan, nan, nan, nan, nan, nan, nan, 6.0]
    #
    # 00:00 to 02:00 = 2 hour gap -> interpolate
    # 02:00 to 06:00 = 4 hour gap -> do not interpolate
    expected_data = [0.0, 0.5, 1.0, 1.5, 2.0, nan, nan, nan, nan, nan, nan, nan, 6.0]
    expected_index = date_range(datetime(2025, 1, 1, 0, 0), datetime(2025, 1, 1, 6, 0), freq='30min')
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
        datetime(2025, 1, 1, 0, 15),
        datetime(2025, 1, 1, 0, 17),
        datetime(2025, 1, 1, 0, 23),
        datetime(2025, 1, 1, 0, 28),
        datetime(2025, 1, 1, 0, 45),
        datetime(2025, 1, 1, 1, 0),
    ]

    test_data = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    test_df = DataFrame(data={'test_col': test_data}, index=test_interval)

    # reindex to every 5 minutes (300 seconds)
    # reindexed_data = [0.0, 1.0, nan, 2.0, nan, 3.0, nan, nan, nan, 4.0, nan, nan, 5.0]
    # 00:15 to 00:17 = 2 min gap -> interpolate
    # 00:17 to 00:23 = 6 min gap -> interpolate
    # 00:23 to 00:28 = 5 min gap -> interpolate
    # 00:28 to 00:45 = 17 min gap -> do not interpolate
    # 00:45 to 01:00 = 15 min gap -> do not interpolate
    expected_data = [0.0, 1.0, 1.5, 2.0, 2.4, 3.0, nan, nan, nan, 4.0, nan, nan, 5.0]
    
    expected_index = [
        datetime(2025, 1, 1, 0, 15), # original timestamp
        datetime(2025, 1, 1, 0, 17), # original timestamp
        datetime(2025, 1, 1, 0, 20), # new from reindexing
        datetime(2025, 1, 1, 0, 23), # original timestamp
        datetime(2025, 1, 1, 0, 25), # new from reindexing
        datetime(2025, 1, 1, 0, 28), # original timestamp
        datetime(2025, 1, 1, 0, 30), # new from reindexing
        datetime(2025, 1, 1, 0, 35), # new from reindexing
        datetime(2025, 1, 1, 0, 40), # new from reindexing
        datetime(2025, 1, 1, 0, 45), # original timestamp
        datetime(2025, 1, 1, 0, 50), # new from reindexing
        datetime(2025, 1, 1, 0, 55), # new from reindexing
        datetime(2025, 1, 1, 1, 0), # original timestamp
    ]
    expected_df = DataFrame(data={'test_col': expected_data}, index=expected_index)

    kwargs = {
        "col_name": "test_col",
        "interpolation_interval": 300,     # 5 minutes
        "limit": 600                       # 10 minutes
    }

    result_df = post_process_factory(test_df, "LinearInterpolation", kwargs)
    pd.testing.assert_frame_equal(result_df, expected_df, rtol=1e-9, check_freq=False)






