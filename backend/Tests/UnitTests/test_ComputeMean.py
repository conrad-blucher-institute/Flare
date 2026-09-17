# -*- coding: utf-8 -*-
# test_ComputeMean.py
#-------------------------------
# Created By: CJ Quintero
# Created On: 09/17/2026
#-------------------------------
"""
This module tests the ComputeMean post processing class

docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_ComputeMean.py -v
"""
#-------------------------------
import pytest
from datetime import datetime

from runtimeContext import thread_storage
from PostProcessing.PostProcessingClasses.ComputeMean import ComputeMean

from pandas import DataFrame, date_range
from numpy import nan


class FakeLogger():
    def log_info(self, msg):
        pass


@pytest.fixture(autouse=True)
def fake_thread_logger():
    thread_storage.logger = FakeLogger()
    yield thread_storage.logger


class TestComputeMean():
    """
    Test suite for the ComputeMean post processing class

    docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_ComputeMean.py -v
    """

    @pytest.mark.parametrize(
        "df, targetSeries, outKey",
        [
            # test None target series; df should remain unchanged
            (
                DataFrame({
                    "series-one": [1, 2, 3, 4],
                    "series-two": [5, 6, 7, 8],
                    "series-three": [9, 10, 11, 12],
                    "series-four": [13, 14, 15, 16]
                }),
                None, # targetSeries
                "combined-series"
            ),
            # test None outKey; df should remain unchanged
            (
                DataFrame({
                    "series-one": [1, 2, 3, 4],
                    "series-two": [5, 6, 7, 8],
                    "series-three": [9, 10, 11, 12],
                    "series-four": [13, 14, 15, 16]
                }),
                [
                    "series-one",
                    "series-two",
                    "series-three",
                    "series-four"
                ],
                None # outKey
            ),
            # test a missing target series; df should remain unchanged
            (
                DataFrame({
                    "series-one": [1, 2, 3, 4],
                    "series-two": [5, 6, 7, 8],
                    "series-three": [9, 10, 11, 12],
                    "series-four": [13, 14, 15, 16]
                }),
                [
                    "series-one",
                    "series-two",
                    "series-three"
                ],
                "combined-series"
            ),
            # test empty target series; df should remain unchanged
            (
                DataFrame({
                    "series-one": [1, 2, 3, 4],
                    "series-two": [5, 6, 7, 8],
                    "series-three": [9, 10, 11, 12],
                    "series-four": [13, 14, 15, 16]
                }),
                [], # empty targetSeries
                "combined-series"
            )
        ],
        ids = [
            "None_target_series",
            "None_outKey",
            "Missing_target_series",
            "Empty_target_series"
        ]
    )
    def test_invalid_args(self, df: DataFrame, targetSeries: list[str], outKey: str):
        """
        Test that the ComputeMean post processing class correctly handles invalid arguments.
        The input df should be unchanged.
        """
        compute_mean = ComputeMean()
        result_df = compute_mean.post_process(df, targetSeries, outKey)
        assert result_df is df, "DataFrame returned should be the same object as the input DataFrame for invalid arguments."
        assert result_df.equals(df), "DataFrame should remain unchanged for invalid arguments."


    @pytest.mark.parametrize(
        "df, targetSeries, outKey, expected_df",
        [
            # df should have new mean series appended
            (
                DataFrame({
                    "series-one": [1, 2, 3, 4],
                    "series-two": [5, 6, 7, 8],
                    "series-three": [9, 10, 11, 12],
                    "series-four": [13, 14, 15, 16]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 3), freq='1h')),
                [
                    "series-one",
                    "series-two",
                    "series-three",
                    "series-four"
                ],
                "combined-series",
                DataFrame({
                    "series-one": [1, 2, 3, 4],
                    "series-two": [5, 6, 7, 8],
                    "series-three": [9, 10, 11, 12],
                    "series-four": [13, 14, 15, 16],
                    "combined-series": [7.0, 8.0, 9.0, 10.0]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 3), freq='1h'))
            ),
            # missing values in target series; the mean should be computed ignoring NaN values
            (
                DataFrame({
                    "series-one": [1, 2, nan, 4],
                    "series-two": [5, nan, 7, 8],
                    "series-three": [nan, 10, 11, 12],
                    "series-four": [13, 14, 15, nan]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 3), freq='1h')),
                [
                    "series-one",
                    "series-two",
                    "series-three",
                    "series-four"
                ],
                "combined-series",
                DataFrame({
                    "series-one":      [1,   2,    nan, 4],
                    "series-two":      [5,   None, 7,   8],
                    "series-three":    [nan, 10,   11,  12],
                    "series-four":     [13,  14,   15,  None],
                    "combined-series": [6.333333333333333, 8.666666666666666, 11.0, 8.0]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 3), freq='1h'))
            ),
            # 1 valid series
            (
                DataFrame({
                    "series-one": [1, 2, 3, 4],
                    "series-two": [None, None, None, None],
                    "series-three": [nan, nan, nan, nan],
                    "series-four": [nan, nan, nan, nan]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 3), freq='1h')),
                [
                    "series-one",
                    "series-two",
                    "series-three",
                    "series-four"
                ],
                "combined-series",
                DataFrame({
                    "series-one":      [1, 2, 3, 4],
                    "series-two":      [None, None, None, None],
                    "series-three":    [nan, nan, nan, nan],
                    "series-four":     [nan, nan, nan, nan],
                    "combined-series": [1.0, 2.0, 3.0, 4.0]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 3), freq='1h'))
            ),
            # all invalid series so the computed column is all nans
            (
                DataFrame({
                    "series-one": ['', '', '', ''],
                    "series-two": ['', '', '', ''],
                    "series-three": ['', '', '', ''],
                    "series-four": ['', '', '', '']
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 3), freq='1h')),
                [
                    "series-one",
                    "series-two",
                    "series-three",
                    "series-four"
                ],
                "combined-series",
                DataFrame({
                    "series-one": ['', '', '', ''],
                    "series-two": ['', '', '', ''],
                    "series-three": ['', '', '', ''],
                    "series-four": ['', '', '', ''],
                    "combined-series": [nan, nan, nan, nan]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 3), freq='1h'))
            ),
        ],
        ids = [
            "basic_test",
            "missing_values",
            "one_valid_series",
            "all_invalid_series"
        ]
    )
    def test_compute_mean(self, df, targetSeries: list[str], outKey: str, expected_df):
        """
        Test that the ComputeMean post processing class correctly computes the mean of the target series.
        """
        expected_idx = date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 3), freq='1h')

        compute_mean = ComputeMean()
        result_df = compute_mean.post_process(df, targetSeries, outKey)
        assert "combined-series" in result_df.columns, "The output DataFrame should contain the new mean series column."
        assert result_df.equals(expected_df), "The computed mean series does not match the expected values."
        assert result_df.index.equals(expected_idx), "The index of the output DataFrame should match the expected index."