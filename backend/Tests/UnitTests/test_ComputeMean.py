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
        "df, targetSeries, outKey, dropOutlierValues, thresholdDeviationFromMedian",
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
                "combined-series",
                False, # dropOutlierValues
                None # thresholdDeviationFromMedian
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
                None, # outKey,
                False, # dropOutlierValues
                None # thresholdDeviationFromMedian
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
                    "series-five"   # doesn't exist in the input df
                ],
                "combined-series",
                False, # dropOutlierValues
                None # thresholdDeviationFromMedian
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
                "combined-series",
                False, # dropOutlierValues
                None # thresholdDeviationFromMedian
            ),
            # test a true dropOutlierValues with no threshold; df should remain unchanged
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
                "combined-series",
                True, # dropOutlierValues
                None # thresholdDeviationFromMedian
            ),
            # test a true dropOutlierValues with a negative threshold; df should remain unchanged
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
                "combined-series",
                True, # dropOutlierValues
                -1.0 # thresholdDeviationFromMedian
            )
        ],
        ids = [
            "None_target_series",
            "None_outKey",
            "Missing_target_series",
            "Empty_target_series",
            "no-threshold",
            "negative-threshold"
        ]
    )
    def test_invalid_args(self, df: DataFrame, targetSeries: list[str], outKey: str, dropOutlierValues: bool, thresholdDeviationFromMedian: float):
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
                    "combined-series": [None, None, None, None]
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
    def test_compute_mean_no_outliers(self, df, targetSeries: list[str], outKey: str, expected_df):
        """
        Test that the ComputeMean post processing class correctly computes the mean of the target series.
        """
        expected_idx = date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 3), freq='1h')

        compute_mean = ComputeMean()
        result_df = compute_mean.post_process(df, targetSeries, outKey)
        assert "combined-series" in result_df.columns, "The output DataFrame should contain the new mean series column."
        assert result_df.equals(expected_df), "The computed mean series does not match the expected values."
        assert result_df.index.equals(expected_idx), "The index of the output DataFrame should match the expected index."


    @pytest.mark.parametrize(
        "df, targetSeries, outKey, expected_df, drop, threshold",
        [
            (
                DataFrame({
                    "series-one": [1, 2, 3, 4, 5],
                    "series-two": [5, 6, 7, 8, 100],
                    "series-three": [9, 10, 11, 12, 13]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 4), freq='1h')),
                [
                    "series-one",
                    "series-two",
                    "series-three"
                ],
                "combined-series",
                DataFrame({
                    # first 3 series should be unchanged
                    "series-one": [1, 2, 3, 4, 5],
                    "series-two": [5, 6, 7, 8, 100],
                    "series-three": [9, 10, 11, 12, 13],
                    # 100 should be ignored in the mean calculation for the last row, so the mean should be (5 + 13)/2 = 9.0
                    "combined-series": [5.0, 6.0, 7.0, 8.0, 9.0]
                }, 
                # the index should be the same since we aren't dropping any rows, just ignoring outliers in the mean calculation
                index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 4), freq='1h')),
                True, # dropOutlierValues
                10.0 # values 10 or farther from median are not used in the mean calculation
            ),
            # test with values that are exactly at the threshold; they should not be in the mean calculation
            (
                DataFrame({
                    "series-one":   [1, 6, 11, 16, 21],
                    "series-two":   [2, 7, 12, 17, 22],
                    "series-three": [3, 8, 13, 18, 23],
                    "series-four":  [4, 9, 14, 19, 24],
                    "series-five":  [5, 10, 15, 20, 25]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 4), freq='1h')),
                [
                    "series-one",
                    "series-two",
                    "series-three",
                    "series-four",
                    "series-five",
                ],
                "combined-series",
                DataFrame({
                    "series-one":   [1, 6, 11, 16, 21],
                    "series-two":   [2, 7, 12, 17, 22],
                    "series-three": [3, 8, 13, 18, 23],
                    "series-four":  [4, 9, 14, 19, 24],
                    "series-five":  [5, 10, 15, 20, 25],

                    # t1 - median = 3, mean = (2 + 3 + 4) / 3 = 3, 1 and 5 are exactly 2 away from the median, so they are ignored in the mean calculation
                    # t2 - median = 8, mean = (7 + 8 + 9) / 3 = 8, 6 and 10 ignored
                    # t3 - median 13, mean = (12 + 13 + 14) / 3 = 13, 11 and 15 ignored
                    # t4 - median 18, mean = (17 + 18 + 19) / 3 = 18, 16 and 20 ignored
                    # t5 - median 23, mean = (22 + 23 + 24) / 3 = 23, 21 and 25 ignored
                    "combined-series": [3.0, 8.0, 13.0, 18.0, 23.0]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 4), freq='1h')),
                True, # dropOutlierValues
                2
            ),
            # no values are far enough from the median to be dropped so a plain average is done
            (
                DataFrame({
                    "series-one":   [10, 20, 30, 40, 50],
                    "series-two":   [11, 21, 31, 41, 51],
                    "series-three": [12, 22, 32, 42, 52]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 4), freq='1h')),
                [
                    "series-one",
                    "series-two",
                    "series-three"
                ],
                "combined-series",
                DataFrame({
                    "series-one":   [10, 20, 30, 40, 50],
                    "series-two":   [11, 21, 31, 41, 51],
                    "series-three": [12, 22, 32, 42, 52],
                    # median/deviations are the same shape at every timestamp (1, 0, 1), all < 5, so nothing is dropped
                    "combined-series": [11.0, 21.0, 31.0, 41.0, 51.0]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 4), freq='1h')),
                True, # dropOutlierValues
                5.0
            ),
            # two outliers on opposite sides of the median get dropped in the same row
            (
                DataFrame({
                    "series-one":   [5, 5, 5, 5, 5],
                    "series-two":   [5, 5, 5, 5, 5],
                    "series-three": [5, 5, 5, 5, 5],
                    "series-four":  [50, 50, 50, 50, 50],
                    "series-five":  [-40, -40, -40, -40, -40]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 4), freq='1h')),
                [
                    "series-one",
                    "series-two",
                    "series-three",
                    "series-four",
                    "series-five",
                ],
                "combined-series",
                DataFrame({
                    "series-one":   [5, 5, 5, 5, 5],
                    "series-two":   [5, 5, 5, 5, 5],
                    "series-three": [5, 5, 5, 5, 5],
                    "series-four":  [50, 50, 50, 50, 50],
                    "series-five":  [-40, -40, -40, -40, -40],
                    # median = 5, deviations = [0, 0, 0, 45, 45]; 50 and -40 are both >= 10 away, so mean = (5+5+5)/3 = 5.0
                    "combined-series": [5.0, 5.0, 5.0, 5.0, 5.0]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 4), freq='1h')),
                True, # dropOutlierValues
                10.0
            ),
            # every value in the row is far enough from the median to be dropped
            (
                DataFrame({
                    "series-one":   [1, 1, 1, 1, 1],
                    "series-two":   [2, 2, 2, 2, 2],
                    "series-three": [3, 3, 3, 3, 3],
                    "series-four":  [4, 4, 4, 4, 4]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 4), freq='1h')),
                [
                    "series-one",
                    "series-two",
                    "series-three",
                    "series-four",
                ],
                "combined-series",
                DataFrame({
                    "series-one":   [1, 1, 1, 1, 1],
                    "series-two":   [2, 2, 2, 2, 2],
                    "series-three": [3, 3, 3, 3, 3],
                    "series-four":  [4, 4, 4, 4, 4],
                    # median = 2.5, deviations = [1.5, 0.5, 0.5, 1.5]; all >= 0.5, so every value is dropped
                    "combined-series": [None, None, None, None, None]
                }, index=date_range(datetime(2026, 1, 1, 0), datetime(2026, 1, 1, 4), freq='1h')),
                True, # dropOutlierValues
                0.5
            ),
        ],
        ids = [
            "basic_outlier",
            "exact_threshold",
            "no_outliers",
            "outliers_on_ends",
            "all_outliers"
        ]
    )
    def test_compute_mean_with_outliers(self, df, targetSeries, outKey, expected_df, drop, threshold):
        """
        test the compute mean class with dropOutlierValues set to true and a thresholdDeviationFromMedian specified
        """

        compute_mean = ComputeMean()
        result_df = compute_mean.post_process(df, targetSeries, outKey, dropOutlierValues=drop, thresholdDeviationFromMedian=threshold)
        assert "combined-series" in result_df.columns, "The output DataFrame should contain the new mean series column."
        assert result_df.equals(expected_df), "The computed mean series does not match the expected values."
