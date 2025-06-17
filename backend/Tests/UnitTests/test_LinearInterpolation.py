# -*- coding: utf-8 -*-
#test_LinearInterpolation.py
#-------------------------------
# Created By: Matthew Kastl
#----------------------------------
"""This file tests the ImmediateArithmeticOperation PPC 
 """ 
#----------------------------------
# 
#
import sys
sys.path.append('/app/backend')

import pytest
from math import isclose
from pandas import DataFrame, date_range, read_csv, Series
from numpy import nan
from datetime import datetime
from PostProcessing.IPostProcessing import post_process_factory


series = {'data6Min': [val for val in range(101)]} # 10 hours of 5min data
index = date_range(datetime(2024, 1, 1, 0, 0, 0), periods=len(series['data6Min']), freq='6min')
df_6min = DataFrame(series, index=index)

series = {'data5hr': [val for val in range(3)]} # 10 hours of 5min data
index = date_range(datetime(2024, 1, 1, 0, 0, 0), periods=len(series['data5hr']), freq='5h')
df_5hr = DataFrame(series, index=index)

series = {'data1hr': [val for val in range(11)]} # 10 hours of 5min data
index = date_range(datetime(2024, 1, 1, 0, 0, 0), periods=len(series['data1hr']), freq='1h')
df_1hr = DataFrame(series, index=index)

one_hour_to_six_min_interpolation = df_6min.join(df_1hr, how='outer')['data1hr'].interpolate(method='time')
five_hour_to_ten_hour_interpolation = df_1hr.join(df_5hr, how='outer')['data5hr'].interpolate(method='time')


@pytest.mark.parametrize("df_data, col_name, interpolation_interval, limit, expected_results", [
    # Tests interpolation into a dataframe of the same index resolution
    (df_6min.join(df_1hr, how='outer'), 'data1hr', 360, 500, one_hour_to_six_min_interpolation), 
    # Tests interpolation into a dataframe with a higher index resolution
    (df_6min.join(df_1hr, how='outer').join(df_5hr, how='outer'), 'data5hr', 3600, 500, five_hour_to_ten_hour_interpolation), 
    # Tests interpolation into a dataframe with a lower index resolution
    (df_1hr.join(df_5hr, how='outer'), 'data1hr', 360, 500, one_hour_to_six_min_interpolation),
])
def test_post_process_data(df_data: DataFrame, col_name: str, interpolation_interval: int, limit: int, expected_results: Series):
    """This function tests that the interpolation function is generating the correct values as requested.
    """

    call = "LinearInterpolation"
    kwargs = {
        "col_name": col_name,
        "interpolation_interval": interpolation_interval,
        "limit": limit
    }

    # Call the factory to get the resolver and pass it the fake input data and the post process call
    df_data = post_process_factory(df_data, call, kwargs)

    # Unpack the resulting components
    result = df_data[col_name].dropna().tolist()
    expected = expected_results.tolist()

    # Iterate through the resulting components checking if they were calculated correctly
    for actual, expected in zip(result, expected):
        tolerance = 1e-5
        if not isclose(actual, expected, abs_tol=tolerance):
            assert False
    assert True



@pytest.mark.parametrize("df_data, col_name, interpolation_interval, limit, expected_results", [
    # Tests interpolation into a dataframe of the same index resolution
    (df_6min.join(df_1hr, how='outer'), 'data1hr', 360, 500, 101), 
    # Tests interpolation into a dataframe with a higher index resolution
    (df_6min.join(df_1hr, how='outer').join(df_5hr, how='outer'), 'data5hr', 3600, 500, 101), 
    # Tests interpolation into a dataframe with a lower index resolution
    (df_1hr.join(df_5hr, how='outer'), 'data1hr', 360, 500, 101),
])
def test_post_process_data_indexing(df_data: DataFrame, col_name: str, interpolation_interval: int, limit: int, expected_results: Series):
    """This function tests that no bad reindexing side effects are occurring.
    """

    call = "LinearInterpolation"
    kwargs = {
        "col_name": col_name,
        "interpolation_interval": interpolation_interval,
        "limit": limit
    }

    # Call the factory to get the resolver and pass it the fake input data and the post process call
    df_data = post_process_factory(df_data, call, kwargs)
    assert len(df_data) == expected_results

