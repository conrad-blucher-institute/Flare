# -*- coding: utf-8 -*-
# test_hohonu.py
#-------------------------------
# Created By: CJ Quintero
# 10/20/2026
#----------------------------------
"""
This file tests the hohonu data ingestion class.

docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_hohonu.py -v
""" 
from numpy import nan
from datetime import datetime
from pandas import DataFrame, Series
from pandas.testing import assert_frame_equal
from unittest.mock import MagicMock, patch
from flareRunner import thread_storage
from Ingestion.IngestionClasses.Hohonu import Hohonu

response = {
  "meta": {
    "location": "Magnolia Beach, TX",
    "station_id": "hohonu-185",
    "data_source": "Hohonu",
    "measurement_type": "tidal",
    "datum": {
      "label": "Sensor Datum",
      "unit": "ft"
    }
  },
  "data": {
    "waterlevel": [
        {"t": "2026-10-21T01:00:00Z", "o": 6.49},
        {"t": "2026-10-21T01:06:00Z", "o": 6.5},
        {"t": "2026-10-21T01:12:00Z", "o": 6.5},
        {"t": "2026-10-21T01:18:00Z", "o": 6.5},
        {"t": "2026-10-21T01:24:00Z", "o": 6.5},
        {"t": "2026-10-21T01:30:00Z", "o": 6.5},
        {"t": "2026-10-21T01:36:00Z", "o": 6.5},
        {"t": "2026-10-21T01:42:00Z", "o": 6.49}
    ]
  }
}

class TestHohonu:

    def test_build_series(self):
        """
        Tests that the response is converted into a Series indexed by naive UTC timestamps
        """
        thread_storage.logger = MagicMock()
        series = Hohonu()._build_series("Hohonu-Test", response)

        assert series.name == "Hohonu-Test"
        assert len(series) == 8
        assert series.index[0] == datetime(2026, 10, 21, 1, tzinfo=None)   # Z removed, still UTC
        assert series.index.tz is None
        assert series.iloc[0] == 6.49
        assert series.iloc[-1] == 6.49


    def test_ingest_data(self):
        """
        Tests that ingest_data adds the response data as a new column
        and doesn't modify existing data
        """
        thread_storage.logger = MagicMock()

        # data every 15 minutes, with a missing value at 1:00
        other_series = Series(
            name="other-series",
            data=[100, 200, 300, 400, nan, 600, 700],
            index=[
                datetime(2026, 10, 21, 1, 0),
                datetime(2026, 10, 21, 1, 15),
                datetime(2026, 10, 21, 1, 30),
                datetime(2026, 10, 21, 1, 45),
                datetime(2026, 10, 21, 2, 0),
                datetime(2026, 10, 21, 2, 15),
                datetime(2026, 10, 21, 2, 30),
            ]
        )

        # the df that the hohonu data will be added to
        test_df = DataFrame({"other-series": other_series})

        # skip the headers and use the mock response for the api_request function
        with patch.object(Hohonu, "_get_headers", return_value={}), \
            patch("Ingestion.IngestionClasses.Hohonu.api_request", return_value=response):
            
            test_df = Hohonu().ingest_data(
                df=test_df,
                reference_time=datetime(2026, 10, 21, 0),
                column_name="Hohonu-Test",
                station_id="hohonu-185",
                datum="D2W",
                units="english",
                range=[-1, 0]
            )

        expected_series = Series(
            name="Hohonu-Test",
            data=[6.49, 6.5, 6.5, 6.5, 6.5, 6.5, 6.5, 6.49],
            index=[
                datetime(2026, 10, 21, 1, 0),
                datetime(2026, 10, 21, 1, 6),
                datetime(2026, 10, 21, 1, 12),
                datetime(2026, 10, 21, 1, 18),
                datetime(2026, 10, 21, 1, 24),
                datetime(2026, 10, 21, 1, 30),
                datetime(2026, 10, 21, 1, 36),
                datetime(2026, 10, 21, 1, 42)
            ]
        )

        expected_df = DataFrame(
            {
                "other-series": [
                    100,     # 1:00
                    nan,     # 1:06 - inserted due to the outer join
                    nan,     # 1:12 - inserted due to the outer join
                    200,     # 1:15
                    nan,     # 1:18 - inserted due to the outer join
                    nan,     # 1:24 - inserted due to the outer join
                    300,     # 1:30
                    nan,     # 1:36 - inserted due to the outer join
                    nan,     # 1:42 - inserted due to the outer join
                    400,     # 1:45
                    nan,     # 2:00 - original missing value
                    600,     # 2:15
                    700,     # 2:30
                ],
                "Hohonu-Test": [
                    6.49,    # 1:00
                    6.5,     # 1:06
                    6.5,     # 1:12
                    nan,     # 1:15 - inserted due to the outer join
                    6.5,     # 1:18
                    6.5,     # 1:24
                    6.5,     # 1:30
                    6.5,     # 1:36
                    6.49,    # 1:42
                    nan,     # 1:45 - inserted due to the outer join
                    nan,     # 2:00 - inserted due to the outer join
                    nan,     # 2:15 - inserted due to the outer join
                    nan,     # 2:30 - inserted due to the outer join
                ],
            },
            index=[
                datetime(2026, 10, 21, 1, 0),   # hohonu
                datetime(2026, 10, 21, 1, 6),   # hohonu
                datetime(2026, 10, 21, 1, 12),  # hohonu
                datetime(2026, 10, 21, 1, 15),  # other
                datetime(2026, 10, 21, 1, 18),  # hohonu
                datetime(2026, 10, 21, 1, 24),  # hohonu
                datetime(2026, 10, 21, 1, 30),  # hohonu
                datetime(2026, 10, 21, 1, 36),  # hohonu
                datetime(2026, 10, 21, 1, 42),  # hohonu
                datetime(2026, 10, 21, 1, 45),  # other
                datetime(2026, 10, 21, 2, 0),   # other
                datetime(2026, 10, 21, 2, 15),  # other
                datetime(2026, 10, 21, 2, 30),  # other
            ]
        )

        assert_frame_equal(test_df, expected_df)


    def test_missing_api_key(self, monkeypatch):
        """
        Tests that a missing HOHONU_API_AUTH logs one error, skips the request,
        and adds an empty column
        """
        thread_storage.logger = MagicMock()

        # make sure the api key is not set for this test
        # this only removes the variable for the duration of this test, so it won't affect other tests
        monkeypatch.delenv("HOHONU_API_AUTH", raising=False)

        with patch("Ingestion.IngestionClasses.Hohonu.api_request") as mock_api_request:
            test_df = Hohonu().ingest_data(
                df=DataFrame(),
                reference_time=datetime(2026, 10, 21, 0),
                column_name="Hohonu-Test",
                station_id="hohonu-185",
                datum="D2W",
                units="english",
                range=[-1, 0]
            )

        thread_storage.logger.log_error.assert_called_once_with("HOHONU_API_AUTH environment variable is not set")

        # The api_request function should not be called since the API key is missing
        # and an empty column should be added to the DataFrame
        mock_api_request.assert_not_called()
        assert "Hohonu-Test" in test_df.columns
        assert test_df["Hohonu-Test"].isna().all()


    def test_api_request_failure(self):
        """
        Tests that an API request failure adds an empty column 
        """
        thread_storage.logger = MagicMock()

        # skip the headers and use a mock api request that returns None to simulate a failure
        with patch.object(Hohonu, "_get_headers", return_value={}), \
            patch("Ingestion.IngestionClasses.Hohonu.api_request", return_value=None):

            test_df = Hohonu().ingest_data(
                df=DataFrame(),
                reference_time=datetime(2026, 10, 21, 0),
                column_name="Hohonu-Test",
                station_id="hohonu-185",
                datum="D2W",
                units="english",
                range=[-1, 0]
            )

        # api_request already logs the failure, so Hohonu shouldn't log again
        thread_storage.logger.log_error.assert_not_called()
        assert "Hohonu-Test" in test_df.columns
        assert test_df["Hohonu-Test"].isna().all()
