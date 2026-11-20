# -*- coding: utf-8 -*-
# test_SemaphoreOutputTimeSpan.py
#-------------------------------
# Created By: CJ Quintero
# 11/19/2026
#----------------------------------
"""
This file tests the Semaphore output time span data ingestion class.

docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_SemaphoreOutputTimeSpan.py -v
"""
import pytest
from unittest.mock import MagicMock, patch

from flareRunner import thread_storage
from Ingestion.IngestionClasses.SemaphoreOutputTimeSpan import SemaphoreOutputTimeSpan

from numpy import nan
from datetime import datetime
from pandas import DataFrame, Series, to_datetime
from pandas.testing import assert_frame_equal, assert_series_equal

@pytest.fixture(autouse=True)
def mock_logger():
    thread_storage.logger = MagicMock()
    yield thread_storage.logger


def make_point(value, verified, generated, lead_time):
    return {
        "dataValue": [[[value]]],
        "dataUnit": "meter",
        "timeVerified": verified,
        "timeGenerated": generated,
        "leadTime": lead_time
    }


response_1 = {
    "model_1": {
        "_Series__data": [
            make_point(1, '2026-11-20T01:00:00', '2026-11-20T01:00:00', 100),
            make_point(2, '2026-11-20T02:00:00', '2026-11-20T02:00:00', 100),
            make_point(3, '2026-11-20T03:00:00', '2026-11-20T03:00:00', 100),
        ]
    },
    "model_2": {
        # overlaps the first 3 points of model 1, but has 3 additional points
        "_Series__data": [
            make_point(10, '2026-11-20T01:00:00', '2026-11-20T01:00:00', 200),
            make_point(20, '2026-11-20T02:00:00', '2026-11-20T02:00:00', 200),
            make_point(30, '2026-11-20T03:00:00', '2026-11-20T03:00:00', 200),
            make_point(40, '2026-11-20T04:00:00', '2026-11-20T04:00:00', 200),
            make_point(50, '2026-11-20T05:00:00', '2026-11-20T05:00:00', 200),
            make_point(60, '2026-11-20T06:00:00', '2026-11-20T06:00:00', 200),
        ]
    },
    "model_3": {
        # overlaps the first 3 points with model 1 and 2, and points 4-6 with model 2
        # and has 3 additional points
        "_Series__data": [
            make_point(100, '2026-11-20T01:00:00', '2026-11-20T01:00:00', 300),
            make_point(200, '2026-11-20T02:00:00', '2026-11-20T02:00:00', 300),
            make_point(300, '2026-11-20T03:00:00', '2026-11-20T03:00:00', 300),
            make_point(400, '2026-11-20T04:00:00', '2026-11-20T04:00:00', 300),
            make_point(500, '2026-11-20T05:00:00', '2026-11-20T05:00:00', 300),
            make_point(600, '2026-11-20T06:00:00', '2026-11-20T06:00:00', 300),
            make_point(700, '2026-11-20T07:00:00', '2026-11-20T07:00:00', 300),
            make_point(800, '2026-11-20T08:00:00', '2026-11-20T08:00:00', 300),
            make_point(900, '2026-11-20T09:00:00', '2026-11-20T09:00:00', 300),
        ]
    }
}

response_2 = {
    "model_1": {
        "_Series__data": [
            make_point(1, '2026-11-20T01:00:00', '2026-11-20T01:00:00', 1),
            make_point(2, '2026-11-20T02:00:00', '2026-11-20T02:00:00', 1),
            make_point(nan, '2026-11-20T03:00:00', '2026-11-20T03:00:00', 1),
            make_point(nan, '2026-11-20T04:00:00', '2026-11-20T04:00:00', 1),
            make_point(nan, '2026-11-20T05:00:00', '2026-11-20T05:00:00', 1),
            make_point(nan, '2026-11-20T06:00:00', '2026-11-20T06:00:00', 1),
        ]
    },
    "model_2": {
        "_Series__data": [
            make_point(10, '2026-11-20T01:00:00', '2026-11-20T01:00:00', 2),
            make_point(20, '2026-11-20T02:00:00', '2026-11-20T02:00:00', 2),
            make_point(30, '2026-11-20T03:00:00', '2026-11-20T03:00:00', 2),
            make_point(40, '2026-11-20T04:00:00', '2026-11-20T04:00:00', 2),
            make_point(nan, '2026-11-20T05:00:00', '2026-11-20T05:00:00', 2),
            make_point(nan, '2026-11-20T06:00:00', '2026-11-20T06:00:00', 2)
        ]
    },
    "model_3": {
        "_Series__data": [
            make_point(100, '2026-11-20T01:00:00', '2026-11-20T01:00:00', 3),
            make_point(200, '2026-11-20T02:00:00', '2026-11-20T02:00:00', 3),
            make_point(300, '2026-11-20T03:00:00', '2026-11-20T03:00:00', 3),
            make_point(400, '2026-11-20T04:00:00', '2026-11-20T04:00:00', 3),
            make_point(500, '2026-11-20T05:00:00', '2026-11-20T05:00:00', 3),
            make_point(600, '2026-11-20T06:00:00', '2026-11-20T06:00:00', 3),
        ]
    }
}

class TestSemaphoreOutputTimeSpan:
    """testing suite for the SemaphoreOutputTimeSpan ingestion class"""

    @pytest.mark.parametrize("response, expected", [
        (
            # tests that the lowest lead time is used when multiple models predict the same time
            # the first 3 points are from model 1, the next 3 points are from model 2, and the last 3 points are from model 3
            response_1,
            DataFrame({
                'test-column': Series(
                    [1, 2, 3, 40, 50, 60, 700, 800, 900],
                    index=to_datetime([
                        '2026-11-20T01:00:00',
                        '2026-11-20T02:00:00',
                        '2026-11-20T03:00:00',
                        '2026-11-20T04:00:00',
                        '2026-11-20T05:00:00',
                        '2026-11-20T06:00:00',
                        '2026-11-20T07:00:00',
                        '2026-11-20T08:00:00',
                        '2026-11-20T09:00:00'
                    ]).rename("timeVerified")
                )
            })
        ),
        (
            # tests that nans are dropped and a valid point with a higher lead time is used instead
            # of a point that is nan with a lower lead time. The first 2 points are from model 1,
            # then points 3-4 are from model 2, and points 5-6 are from model 3.
            # casting to float is needed since nans are floats, and the column will be float if any nans are dropped
            response_2,
            DataFrame({
                'test-column': Series(
                    [1, 2, 30, 40, 500, 600],
                    index=to_datetime([
                        '2026-11-20T01:00:00',
                        '2026-11-20T02:00:00',
                        '2026-11-20T03:00:00',
                        '2026-11-20T04:00:00',
                        '2026-11-20T05:00:00',
                        '2026-11-20T06:00:00'
                    ]).rename("timeVerified"),
                    dtype='float'
                )
            })
        )
    ],
    ids=[
        "all-data",
        "nan-values"
    ])
    def test_ingest_data(self, response, expected):
        """tests basic functionality of the whole module"""

        with patch("Ingestion.IngestionClasses.SemaphoreOutputTimeSpan.api_request", return_value=response):
            sem = SemaphoreOutputTimeSpan()
            df = sem.ingest_data(
                df=DataFrame(),
                reference_time=datetime(2026, 11, 20, 0),
                column_name="test-column",
                time_range=[0, 12],
                models=["model_1", "model_2", "model_3"],
            )

        assert_frame_equal(df, expected)


    @pytest.mark.parametrize("response", [response_1, response_2])
    def test_validate_response(self, response):
        """tests that models with no data are removed and models with data are kept"""

        sem = SemaphoreOutputTimeSpan()

        # a failed request should return None
        assert sem._validate_response(None) is None

        # model_1 has data, model_2 has no data points, and model_3 doesn't exist
        mixed_response = {
            "model_1": response["model_1"],
            "model_2": {"_Series__data": []},
            "model_3": None,
        }
        validated = sem._validate_response(mixed_response)

        # only model_1 should be kept, unchanged
        assert list(validated.keys()) == ["model_1"]
        assert validated["model_1"] == response["model_1"]

        # if every model has no data, None should be returned
        empty_response = {
            "model_2": {"_Series__data": []},
            "model_3": None,
        }
        assert sem._validate_response(empty_response) is None

        # a response where every model has data should be returned unchanged
        assert sem._validate_response(response) == response


    @pytest.mark.parametrize("response, expected", [
        (
            # tests that a single model is returned as is, with nothing to de-duplicate
            {"model_1": response_1["model_1"]},
            Series(
                [1, 2, 3],
                name='test-column',
                index=to_datetime([
                    '2026-11-20T01:00:00',
                    '2026-11-20T02:00:00',
                    '2026-11-20T03:00:00'
                ]).rename("timeVerified")
            )
        ),
        (
            # tests that points returned out of order are sorted by time
            {
                "model_1": {
                    "_Series__data": [
                        make_point(3, '2026-11-20T03:00:00', '2026-11-20T03:00:00', 100),
                        make_point(1, '2026-11-20T01:00:00', '2026-11-20T01:00:00', 100),
                        make_point(2, '2026-11-20T02:00:00', '2026-11-20T02:00:00', 100),
                    ]
                }
            },
            Series(
                [1, 2, 3],
                name='test-column',
                index=to_datetime([
                    '2026-11-20T01:00:00',
                    '2026-11-20T02:00:00',
                    '2026-11-20T03:00:00'
                ]).rename("timeVerified")
            )
        )
    ],
    ids=[
        "single-model",
        "unsorted-points"
    ])
    def test_build_series(self, response, expected):
        """tests that the series is built correctly from the response"""

        sem = SemaphoreOutputTimeSpan()
        series = sem._build_series(response, "test-column")

        assert_series_equal(series, expected)
