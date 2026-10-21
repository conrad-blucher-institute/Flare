# -*- coding: utf-8 -*-
# Hohonu.py
# Created By: CJ Quintero
# Created On: 10/10/2026
"""
This ingestion class is for querying data from the Hohonu API.

Useful References:
    Hohonu API documentation - https://docs.hohonu.io/getting-started-with-hohonu-data

    Magnolia Beach Station - https://dashboard.hohonu.io/map-page/a8076910-b55a-4522-a66b-519828259213/MagnoliaBeach,TX

    Datums info - https://docs.hohonu.io/datums

    Water level request info - https://hohonu.readme.io/reference/viewwaterlevel

NOTE: reads HOHONU_API_AUTH from the env file.
"""
from os import getenv
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

from Ingestion.I_Ingestion import IDataIngestion
from runtimeContext import thread_storage
from Ingestion.Ingestion_Utility import add_empty_column, api_request

from pandas import DataFrame, Series, to_datetime


class Hohonu(IDataIngestion):
    """
    Hohonu ingestion class for querying data from the Hohonu API.

    cspec data request call
    {
        "key": "Hohonu",
        "args": {
            "column_name": "Hohonu-Water-Level-Measurements",
            "station_id": "hohonu-185",
            "datum": "D2W",
            "units": "english",
            "range": [-120, 0],
            "qc_level": 1,              // optional
            "flags": false,             // optional
            "predictions": false,       // optional
            "observations": "6min"      // optional
        }
    }
    """

    def __init__(self):
        self.logger = thread_storage.logger
    
    def ingest_data(
            self,
            df: DataFrame,
            reference_time: datetime,
            column_name: str,
            station_id: str,
            datum: str,
            units: str,
            range: list[int],
            qc_level: int = 1,
            flags: bool = False,
            predictions: bool = False,
            observations: str = "6min"
        ) -> DataFrame:
        """
        Ingests data from the Hohonu API

        Args:
            df (DataFrame) - the ongoing dataframe to add the new data column to

            reference_time (datetime) - the reference time for this run. Ex, if a cspec
                is ran at 12:20, then the reference_time would be 12:20.
            
            column_name (str) - the name of the new data column to add to ongoing dataframe

            station_id (str) - the ID of the station to query data from

            datum (str) - the datum of the data to query. Ex, D2W, MLLW, NAVD88

            units (str) - the units of the data. Ex, 'english' for feet, 'metric' for meters

            range (list[int]) - the times to query data for based on the reference time, in hours. The first
                value is the start of the range, and the second value is the end of the range.
                Ex, [-120, 0] will query data from 5 days ago to now.
            
            qc_level (int) - the quality control level for the data. Defaults to 1.
                0 - no quality control
                1 - basic quality control
                2 - advanced quality control 
            
            flags (bool) - whether to show QC flags for each data point in the response. If true,
                the response will include a flag for each data point indicating its QC status.
            
            predictions (bool) - whether to include tide prediction values.

            observations (str) - the frequency of observations to query.
                Can be one of:
                    "true" - all observations from the station, written as a string in the cspec call
                        When querying all observations, measurements are about every 6 seconds.
                    "false" - no measurements from the station, written as a string in the cspec call
                    "6min" - measurements every 6 minutes, written as a string in the cspec call
                        This is the default value if not specified and can also be written as
                        "six_min"

        Returns:
            DataFrame - the updated dataframe with the new data column added
        """

        headers = self._get_headers()
        if headers is None:
            self.logger.log_error("HOHONU_API_AUTH environment variable is not set")
            return add_empty_column(df, column_name)

        url = self._get_url(
            station_id = station_id,
            reference_time = reference_time,
            datum = datum,
            range = range,
            units = units,
            qc_level = qc_level,
            flags = flags,
            predictions = predictions,
            observations = observations
        )

        # the api_request function will already log HTTPError and all other exceptions
        response_data = api_request(url, headers=headers)
        if response_data is None:
            return add_empty_column(df, column_name)

        try:
            series = self._build_series(column_name, response_data)
            return df.join(series, how='outer')
        except Exception as e:
            # catch all exceptions to add an empty column instead of
            # stopping the exec when building the series fails
            self.logger.log_error(f"Error adding Hohonu data to dataframe. Exception: {e}")
            return add_empty_column(df, column_name)


    def _get_headers(self) -> dict | None:
        """
        Returns the headers for the Hohonu API request

        NOTE: Hohonu rejects urllib's default User-Agent ("Python-urllib/x.y") with a
        403 "banned browser signature". This user agent here identifies us as an automated
        client using the standard "Mozilla/5.0 (compatible; Name/Version)" convention.

        Returns:
            dict | None - the headers for the Hohonu API request or None
                if the HOHONU_API_AUTH environment variable is not set
        """

        api_auth = getenv("HOHONU_API_AUTH", None)
        if api_auth is None:
            return None

        headers = {
            "Authorization": api_auth.strip(),
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; Flare/1.0)",
        }

        return headers


    def _get_url(
            self,
            station_id: str,
            reference_time: datetime,
            datum: str,
            range: list[int],
            units: str = "english",
            qc_level: int = 1,
            flags: bool = False,
            predictions: bool = False,
            observations: str = "6min"
        ) -> str:
        """
        Builds the URL for querying data

        Args:
            station_id (str) - the ID of the station to query data from
            
            reference_time (datetime) - the reference time for this run. Ex, if a cspec
                is ran at 12:20, then the reference_time would be 12:20.

            datum (str) - the datum of the data to query. Ex, D2W, MLLW, NAVD88

            range (list[int]) - the times to query data for based on the reference time, in hours. The first
                value is the start of the range, and the second value is the end of the range.
                Ex, [-120, 0] will query data from 5 days ago to now.
            
            units (str) - the units of the data. Ex, 'english' for feet, 'metric' for meters.
                Defaults to 'english' for feet.
            
            qc_level (int) - the quality control level for the data. Defaults to 1.
                0 - no quality control
                1 - basic quality control
                2 - advanced quality control 
            
            flags (bool) - whether to show QC flags for each data point in the response. If true,
                the response will include a flag for each data point indicating its QC status.
            
            predictions (bool) - whether to include tide prediction values.

            observations (str) - the frequency of observations to query.
                Can be one of:
                    "true" - all observations from the station, written as a string in the cspec call
                        When querying all observations, measurements are about every 6 seconds.
                    "false" - no measurements from the station, written as a string in the cspec call
                    "6min" - measurements every 6 minutes, written as a string in the cspec call
                        This is the default value if not specified and can also be written as
                        "six_min"
        
        Returns:
            str - the URL for querying data from the Hohonu API
            
        NOTE: See https://hohonu.readme.io/reference/viewwaterlevel for more info
            on the water level request and parameter details.
        
        NOTE: Hohonu timestamps are returned in UTC as "t": "2025-02-15T00:00:00Z", where the
            Z means UTC. In this code, the requested from and to times are converted
            to UTC before making the query
        """

        # ensure the reference time is in UTC
        reference_time = reference_time.astimezone(timezone.utc)
        
        # calculate the start and end times for the request
        from_time = reference_time + timedelta(hours=range[0])
        to_time = reference_time + timedelta(hours=range[1])

        # format the start and end times
        from_time = from_time.strftime("%Y-%m-%d %H:%M")
        to_time = to_time.strftime("%Y-%m-%d %H:%M")
        
        params = {
            "from": from_time,
            "to": to_time,
            "units": units,
            "datum": datum,
            "qc_level": qc_level,
            "flags": str(flags).lower(),            # Hohonu expects bools to be lowercase strings
            "predictions": str(predictions).lower(),
            "observations": str(observations).lower()
        }

        url = f"https://dashboard.hohonu.io/api/v1/stations/{station_id}/waterlevel?{urlencode(params)}"

        return url


    def _build_series(self, column_name: str, response_data: dict) -> Series:
        """
        Extracts the data points from the response, builds a series, and returns it to be
        added to the ongoing dataframe.

        Args:
            column_name (str) - the name of the new data column

            response_data (dict) - the response data

        Returns:
            Series - the new data column
        """
        data_points = response_data["data"]["waterlevel"]

        # extract timestamps and values into separate lists
        data_timestamps = [p["t"] for p in data_points]
        data_values     = [p["o"] for p in data_points]
        
        # create a Series of the data points indexed by their timestamps
        # the timestamps are converted to datetime objects in UTC then remove the timezone information
        index = to_datetime(data_timestamps, utc=True).tz_localize(None)
        series = Series(
            data=data_values,
            index=index,
            name=column_name
        )

        return series
