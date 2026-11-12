"""
test_Statistics.py

Tests the Statistics post processing class.

docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_Statistics.py -v

Created by: CJ Quintero
Created on: 11/10/2026
"""
import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch, call

from runtimeContext import thread_storage
from PostProcessing.PostProcessingClasses.Statistics import Statistics

import numpy as np
from pandas import DataFrame
from pandas.testing import assert_frame_equal, assert_index_equal


@pytest.fixture(autouse=True)
def mock_logger():
    with patch('PostProcessing.PostProcessingClasses.Statistics.thread_storage') as mock_thread_storage:
        mock_logger = MagicMock()
        mock_thread_storage.logger = mock_logger
        yield mock_logger

class TestStatistics:
    """testing suite for the Statistics post processing class"""

    @pytest.mark.parametrize(
        "percentiles, input_df, expected_df",
        [
            (
                [0, 5, 25, 50, 75, 95, 100],
                DataFrame({
                    "Air Temperature Predictions": [
                        [1, 2, 3, 4, 5],
                        [6, 7, 8, 9, 10],
                    ]
                }),
                DataFrame({
                    "Air Temperature Predictions": [
                        [1, 2, 3, 4, 5],
                        [6, 7, 8, 9, 10],
                    ],
                    "Air Temperature Predictions p0": [1.0, 6.0],
                    "Air Temperature Predictions p5": [1.2, 6.2],
                    "Air Temperature Predictions p25": [2.0, 7.0],
                    "Air Temperature Predictions p50": [3.0, 8.0],
                    "Air Temperature Predictions p75": [4.0, 9.0],
                    "Air Temperature Predictions p95": [4.8, 9.8],
                    "Air Temperature Predictions p100": [5.0, 10.0],
                }),
            ),
            (
                [10, 90],
                DataFrame({
                    "Air Temperature Predictions": [
                        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                        [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                    ],
                }),
                DataFrame({
                    "Air Temperature Predictions": [
                        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                        [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                    ],
                    "Air Temperature Predictions p10": [1.9, 11.9, 21.9],
                    "Air Temperature Predictions p90": [9.1, 19.1, 29.1],
                }),
            )
        ],
        ids=[
            "multiple_percentiles",
            "10_90_percentiles"
        ]
    )
    def test_percentiles(self, percentiles, input_df, expected_df):
        """
        tests the requested percentiles are calculated correctly for each row in the specified column
        
        docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_Statistics.py::TestStatistics::test_percentiles -v
        """
        result_df = Statistics().post_process(
            input_df,
            "Air Temperature Predictions",
            percentiles=percentiles
        )
        assert_frame_equal(result_df, expected_df)


    @pytest.mark.parametrize(
        "statistics, input_df, expected_df",
        [
            (
                ["min", "max", "mean", "median", "std", "var"],
                DataFrame({
                    "Air Temperature Predictions": [
                        [1, 2, 3, 4, 5],
                        [6, 7, 8, 9, 10],
                        [11, 12, 13, 14, 15]
                    ]
                }),
                DataFrame({
                    "Air Temperature Predictions": [
                        [1, 2, 3, 4, 5],
                        [6, 7, 8, 9, 10],
                        [11, 12, 13, 14, 15],
                    ],
                    "Air Temperature Predictions min": [1, 6, 11],
                    "Air Temperature Predictions max": [5, 10, 15],
                    "Air Temperature Predictions mean": [3.0, 8.0, 13.0],
                    "Air Temperature Predictions median": [3.0, 8.0, 13.0],
                    "Air Temperature Predictions std": [1.4142135623730951, 1.4142135623730951, 1.4142135623730951],
                    "Air Temperature Predictions var": [2.0, 2.0, 2.0],
                }),
            )
        ],
        ids=[
            "all_statistics"
        ]
    )
    def test_statistics(self, statistics, input_df, expected_df):
        """
        tests the requested statistics are calculated correctly for each row in the specified column

        docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_Statistics.py::TestStatistics::test_statistics -v
        """
        result_df = Statistics().post_process(
            input_df,
            "Air Temperature Predictions",
            statistics=statistics
        )
        assert_frame_equal(result_df, expected_df, rtol=1e-8)


    def test_min_max_median_equals_percentiles(self):
        """
        tests that min, max, and median statistics match the corresponding percentiles.
            min = 0th percentile
            median = 50th percentile
            max = 100th percentile

        docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_Statistics.py::TestStatistics::test_min_max_median_equals_percentiles -v
        """

        input_df = DataFrame({
            "Air Temperature Predictions": [
                [1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15]
            ]
        })

        statistics_df = Statistics().post_process(
            input_df,
            "Air Temperature Predictions",
            statistics=["min", "max", "median"]
        )
        percentiles_df = Statistics().post_process(
            input_df,
            "Air Temperature Predictions",
            percentiles=[0, 50, 100]
        )

        assert statistics_df['Air Temperature Predictions min'].to_list() == percentiles_df['Air Temperature Predictions p0'].to_list()
        assert statistics_df['Air Temperature Predictions median'].to_list() == percentiles_df['Air Temperature Predictions p50'].to_list()
        assert statistics_df['Air Temperature Predictions max'].to_list() == percentiles_df['Air Temperature Predictions p100'].to_list()


    def test_bad_percentiles(self, mock_logger):
        """
        tests that percentiles < 0 or > 100 are not included in the final output

        docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_Statistics.py::TestStatistics::test_bad_percentiles -v
        """
        input_df = DataFrame({
            "Air Temperature Predictions": [
                [1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15]
            ]
        })

        result_df = Statistics().post_process(
            input_df,
            "Air Temperature Predictions",
            percentiles=[-1, 101]
        )

        # no change since the invalid percentiles shouldn't have been added
        assert_frame_equal(result_df, input_df)
        assert mock_logger.log_error.call_args_list == [
            call('Invalid percentile: -1'),
            call('Invalid percentile: 101')
        ]


    def test_bad_statistics(self, mock_logger):
        """
        tests that invalid statistics are not included in the final output

        docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_Statistics.py::TestStatistics::test_bad_statistics -v
        """
        input_df = DataFrame({
            "Air Temperature Predictions": [
                [1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15]
            ]
        })

        result_df = Statistics().post_process(
            input_df,
            "Air Temperature Predictions",
            statistics=["invalid"]
        )

        # no change since the invalid statistic shouldn't have been added
        assert_frame_equal(result_df, input_df)
        mock_logger.log_error.assert_called_once_with('Invalid statistic: invalid')


    def test_no_statistics_or_percentiles(self, mock_logger):
        """
        tests that when no statistics or percentiles are requested, the input dataframe remains unchanged

        docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_Statistics.py::TestStatistics::test_no_statistics_or_percentiles -v
        """
        input_df = DataFrame({
            "Air Temperature Predictions": [
                [1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15]
            ]
        })

        result_df = Statistics().post_process(
            input_df,
            "Air Temperature Predictions"
        )

        assert_frame_equal(result_df, input_df)
        mock_logger.log_error.assert_called_once_with('No statistics or percentiles requested')


    def test_statistics_dont_affect_other_cols(self):
        """
        tests that statistics don't affect other columns

        docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_Statistics.py::TestStatistics::test_statistics_dont_affect_other_cols -v
        """
        input_df = DataFrame({
            "Air Temperature Predictions": [
                [1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15]
            ],
            "Other Column": [
                [np.nan, 200, 300, 400, np.nan],
                [600, np.nan, 800, np.nan, np.nan],
                [1100]
            ]
        }, index=[
                datetime(2026, 11, 10, 0),
                datetime(2026, 11, 10, 1),
                datetime(2026, 11, 10, 2)
            ]
        )

        result_df = Statistics().post_process(
            input_df,
            "Air Temperature Predictions",
            statistics=["median"]
        )

        assert input_df["Other Column"].equals(result_df["Other Column"])
        assert 'Air Temperature Predictions median' in result_df
        assert_index_equal(result_df.index, input_df.index)

    
    def test_empty_row(self):
        """
        tests that empty rows are handled correctly by inserting a NaN

        docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_Statistics.py::TestStatistics::test_empty_row -v
        """

        input_df = DataFrame({
            "Air Temperature Predictions": [
                [1, 2, 3, 4, 5],
                None,
                [11, 12, 13, 14, 15]
            ]
        })

        result_df = Statistics().post_process(
            input_df,
            "Air Temperature Predictions",
            statistics=["median"]
        )

        expected_df = DataFrame({
            "Air Temperature Predictions": [
                [1, 2, 3, 4, 5],
                None,
                [11, 12, 13, 14, 15]
            ],
            "Air Temperature Predictions median": [
                3,
                np.nan,
                13
            ]
        })

        assert_frame_equal(result_df, expected_df)


    def test_empty_list_args(self, mock_logger):
        """
        tests that empty list arguments are handled correctly

        docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_Statistics.py::TestStatistics::test_empty_list_args -v
        """
        input_df = DataFrame({
            "Air Temperature Predictions": [
                [1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15]
            ]
        })

        result_df = Statistics().post_process(
            input_df,
            "Air Temperature Predictions",
            statistics=[],
            percentiles=[]
        )

        # result should match the input
        assert_frame_equal(result_df, input_df)
        mock_logger.log_error.assert_called_once_with('No statistics or percentiles requested')
