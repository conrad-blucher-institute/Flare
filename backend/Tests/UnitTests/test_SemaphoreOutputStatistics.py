# -*- coding: utf-8 -*-
# test_SemaphoreOutputStatistics.py
# Created By: Christian Quintero
# Created On: 05/18/2026
"""
Tests the SemaphoreOutputStatistics class functions

docker exec flare-backend python3 -m pytest ./backend/Tests/UnitTests/test_SemaphoreOutputStatistics.py -s

NOTE:: reads the env "SEMAPHORE_API_URL" for the base url to hit.
"""
import pytest
from pandas import DataFrame
from numpy import nan
from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch
from Ingestion.IngestionClasses.SemaphoreOutputStatistics import SemaphoreOutputStatistics

# fixture for the logger
@pytest.fixture(autouse=True)
def mock_logger():
    with patch('Ingestion.IngestionClasses.SemaphoreOutputStatistics.thread_storage') as mock_storage:
        mock_storage.logger = MagicMock()
        yield mock_storage

@pytest.mark.parametrize("response, expected", [
    # all valid responses
    (
        # test response
        {
            "model1": {
                "modelName": "Model1_6hr",
                "timeGenerated": "2026-01-01T12:00:00",
                "p1": 1,
                "p5": 2,
                "p10": 3,
                "p25": 4,
                "p50": 5,
                "p75": 6,
                "p90": 7,
                "p95": 8,
                "p99": 9,
                "min": 10,
                "max": 11,
                "mean": 12,
                "std_dev": 13
            },
            "model2": {
                "modelName": "Model2_12hr",
                "timeGenerated": "2026-01-01T12:00:00",
                "p1": 1,
                "p5": 2,
                "p10": 3,
                "p25": 4,
                "p50": 5,
                "p75": 6,
                "p90": 7,
                "p95": 8,
                "p99": 9,
                "min": 10,
                "max": 11,
                "mean": 12,
                "std_dev": 13
            }
        },
        # expected output
        {
            "model1": {
                "modelName": "Model1_6hr",
                "timeGenerated": "2026-01-01T12:00:00",
                "p1": 1,
                "p5": 2,
                "p10": 3,
                "p25": 4,
                "p50": 5,
                "p75": 6,
                "p90": 7,
                "p95": 8,
                "p99": 9,
                "min": 10,
                "max": 11,
                "mean": 12,
                "std_dev": 13
            },
            "model2": {
                "modelName": "Model2_12hr",
                "timeGenerated": "2026-01-01T12:00:00",
                "p1": 1,
                "p5": 2,
                "p10": 3,
                "p25": 4,
                "p50": 5,
                "p75": 6,
                "p90": 7,
                "p95": 8,
                "p99": 9,
                "min": 10,
                "max": 11,
                "mean": 12,
                "std_dev": 13
            }
        }
    ),

    # some null response
    (
        {
            "model1": {
                "modelName": "Model1_6hr",
                "timeGenerated": "2026-01-01T12:00:00",
                "p1": 1,
                "p5": 2,
                "p10": 3,
                "p25": 4,
                "p50": 5,
                "p75": 6,
                "p90": 7,
                "p95": 8,
                "p99": 9,
                "min": 10,
                "max": 11,
                "mean": 12,
                "std_dev": 13
            },
            "model_that_doesnt_exit": None
        },
        {
            "model1": {
                "modelName": "Model1_6hr",
                "timeGenerated": "2026-01-01T12:00:00",
                "p1": 1,
                "p5": 2,
                "p10": 3,
                "p25": 4,
                "p50": 5,
                "p75": 6,
                "p90": 7,
                "p95": 8,
                "p99": 9,
                "min": 10,
                "max": 11,
                "mean": 12,
                "std_dev": 13
            }
        }
    ),

    # all null responses
    (
        {
            "model_that_doesnt_exit": None,
            "another_model_that_doesnt_exist": None
        },
        None
    )],
    ids=[
        "all_valid_responses",
        "some_null_response",
        "all_null_responses"
    ]
)
def test_validate_response(response, expected):
    """
    tests the validate_response function of the SemaphoreOutputStatistics class to ensure
    the null responses are filtered out properly

    :param response: dict[str, dict] - the response from the API request that needs to be validated
    :param expected: dict[str, dict] - the expected output from the validate_response function given the input response
    """

    sos = SemaphoreOutputStatistics()
    result = sos._SemaphoreOutputStatistics__validate_response(response)
    assert result == expected


@pytest.mark.parametrize("ongoing_df, response, expected_df", [
    # test adding data to an empty dataframe
    (
        # the ongoing dataframe to add to
        DataFrame(),
        # the validated response to add to the dataframe
        {
            "model1_6hr": {
                "modelName": "Model1_6hr",
                "timeGenerated": "2026-01-01T12:00:00",
                "p1": 1,
                "p5": 2,
                "p10": 3,
                "p25": 4,
                "p50": 5,
                "p75": 6,
                "p90": 7,
                "p95": 8,
                "p99": 9,
                "min": 10,
                "max": 11,
                "mean": 12,
                "std_dev": 13
            }
        },
        # the expected dataframe after adding the data
        DataFrame(
            {
                'Water Temperature Prediction p1': [1],
                'Water Temperature Prediction p5': [2],
                'Water Temperature Prediction p10': [3],
                'Water Temperature Prediction p25': [4],
                'Water Temperature Prediction p50': [5],
                'Water Temperature Prediction p75': [6],
                'Water Temperature Prediction p90': [7],
                'Water Temperature Prediction p95': [8],
                'Water Temperature Prediction p99': [9],
                'Water Temperature Prediction min': [10],
                'Water Temperature Prediction max': [11],
                'Water Temperature Prediction mean': [12],
                'Water Temperature Prediction std_dev': [13]
            },
            # this index is 18 hours because the lead time in this test is 6 hours
            # added onto the time generated to get (12:00 + 6 hours = 18:00)
            index=[datetime(2026, 1, 1, 18, 0, tzinfo=None)]
        )
    ),
    # test adding data to a non-empty df
    (
        # ongoing
        DataFrame({
            'Air Temperature Prediction': [50],
        },
        index=[datetime(2026, 1, 1, 12, 0, tzinfo=None)]
        ),
        # response
        {
            "model1_12hr": {
                "modelName": "Model1_12hr",
                "timeGenerated": "2026-01-01T12:00:00",
                "p1": 20,
                "p5": 21,
                "p10": 22,
                "p25": 23,
                "p50": 24,
                "p75": 25,
                "p90": 26,
                "p95": 27,
                "p99": 28,
                "min": 29,
                "max": 30,
                "mean": 31,
                "std_dev": 32
            }
        },
        # expected df
        DataFrame({
            'Air Temperature Prediction': [50, nan],
            'Water Temperature Prediction p1': [nan, 20],
            'Water Temperature Prediction p5': [nan, 21],
            'Water Temperature Prediction p10': [nan, 22],
            'Water Temperature Prediction p25': [nan, 23],
            'Water Temperature Prediction p50': [nan, 24],
            'Water Temperature Prediction p75': [nan, 25],
            'Water Temperature Prediction p90': [nan, 26],
            'Water Temperature Prediction p95': [nan, 27],
            'Water Temperature Prediction p99': [nan, 28],
            'Water Temperature Prediction min': [nan, 29],
            'Water Temperature Prediction max': [nan, 30],
            'Water Temperature Prediction mean': [nan, 31],
            'Water Temperature Prediction std_dev': [nan, 32]
        },
        index=[datetime(2026, 1, 1, 12, 0, tzinfo=None), datetime(2026, 1, 2, 0, 0, tzinfo=None)]
        )
    ),
    # test a model name with missing lead time
    (
        # ongoing
        DataFrame({
            'Air Temperature Prediction': [50],
        },
        index=[datetime(2026, 1, 1, 12, 0, tzinfo=None)]
        ),
        # response
        {
            "model_with_no_lead_time": {
                "modelName": "ModelWithNoLeadTime",
                "timeGenerated": "2026-01-01T12:00:00",
                "p1": 1,
                "p5": 2,
                "p10": 3,
                "p25": 4,
                "p50": 5,
                "p75": 6,
                "p90": 7,
                "p95": 8,
                "p99": 9,
                "min": 10,
                "max": 11,
                "mean": 12,
                "std_dev": 13
            }
        },
        # expected df - should be unchanged
        DataFrame({
            'Air Temperature Prediction': [50],
        },
        index=[datetime(2026, 1, 1, 12, 0, tzinfo=None)]
        )
    )],
    ids=[
        "add_to_empty",
        "add_to_non_empty",
        "missing_lead_time"
    ]
)
def test_add_data(ongoing_df, response, expected_df):
    """
    tests the __add_data function of the SemaphoreOutputStatistics class to ensure
    the data is added to the dataframe properly

    :param ongoing_df: dataframe - the ongoing dataframe to add the data to
    :param response: dict[str, dict] - the validated response from the API request that needs to be added to the dataframe
    :param expected_df: dataframe - the expected dataframe after adding the data
    """

    sos = SemaphoreOutputStatistics()
    result_df = sos._SemaphoreOutputStatistics__add_data(ongoing_df, response)
    assert result_df.equals(expected_df)