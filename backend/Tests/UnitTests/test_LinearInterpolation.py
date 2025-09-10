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

def test_real_scenario_NDFD():
    """
    This test uses some real NDFD data made from a CSV file.
    The timestamps start at 2025-09-15 01:00:00 and go up to 2025-09-15 13:00:00 with hourly frequency.
    We have a real value at 01:00 (29.0), 07:00 (28.0), and 13:00 (31.0).
    With 5 hours of NaNs between each gap.

    By subtracting the time difference between the two real values, we get 6 hours (21600 seconds)
    meaning we have real data points every 6 hours. With a limit of 6 hours, we should only interpolate 
    the 5 hours of NaNs in between each real value.
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

# end section one

if __name__ == "__main__":
    pytest.main([__file__])