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
from requests import get

from Ingestion.I_Ingestion import IDataIngestion
from runtimeContext import thread_storage
from Ingestion.Ingestion_Utility import add_empty_column

from pandas import DataFrame, to_datetime


class Hohonu(IDataIngestion):

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
            predictions: bool = False
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
            
        
        Returns:
            DataFrame - the updated dataframe with the new data column added
        """

        response_data = self._get_response(
            station_id = station_id,
            reference_time = reference_time,
            datum = datum,
            range = range,
            units = units,
            qc_level = qc_level,
            flags = flags,
            predictions = predictions
        )
        if response_data is None:
            return add_empty_column(df, column_name)

        try:
            return self._add_data(df, column_name, response_data)
        except Exception as e:
            # catch all exceptions to add an empty column instead of stopping the exec
            self.logger.log_error(f"Error adding Hohonu data to dataframe. Exception: {e}")
            return add_empty_column(df, column_name)


    def _get_response(
            self,
            station_id: str,
            reference_time: datetime,
            datum: str,
            range: list[int],
            units: str = "english",
            qc_level: int = 1,
            flags: bool = False,
            predictions: bool = False, 
        ) -> dict | None:
        """
        Builds the URL for querying data and fetches the response

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
        
        Returns:
            dict - the JSON response data from the request
            None - if the request fails or an exception occurs
            
        NOTE: See https://hohonu.readme.io/reference/viewwaterlevel for more info
            on the water level request and parameter details.
        
        NOTE: Hohonu timestamps are returned in UTC as "t": "2025-02-15T00:00:00Z", where the
            Z means UTC. In this code, the requested from and to times are converted
            to UTC before making the query
        """

        api_auth = getenv("HOHONU_API_AUTH", None)
        if api_auth is None:
            raise ValueError("HOHONU_API_AUTH environment variable is not set")

        # ensure the reference time is in UTC
        reference_time = reference_time.astimezone(timezone.utc)
        
        # calculate the start and end times for the request
        from_time = reference_time + timedelta(hours=range[0])
        to_time = reference_time + timedelta(hours=range[1])

        # format the start and end times
        from_time = from_time.strftime("%Y-%m-%d %H:%M")
        to_time = to_time.strftime("%Y-%m-%d %H:%M")

        url = f"https://dashboard.hohonu.io/api/v1/stations/{station_id}/waterlevel"
        params = {
            "from": from_time,
            "to": to_time,
            "units": units,
            "datum": datum,
            "qc_level": qc_level,
            "flags": str(flags).lower(),    # Hohonu expects bools to be lowercase
            "predictions": str(predictions).lower()
        }
        headers = {
            "Authorization": api_auth,
            "Accept": "application/json",
        }

        try:
            resp = get(url, params=params, headers=headers, timeout=30)
            if not resp.ok:
                self.logger.log_error(f"Error querying Hohonu API: {resp.status_code} - {resp.text}")
                return None

            data = resp.json()
            return data
        
        except Exception as e:
            # catch all exceptions to add an empty column instead of stopping the exec
            self.logger.log_error(f"Error fetching response from Hohonu API URL: {url}. Exception: {e}")
            return None


    def _add_data(self, df: DataFrame, column_name: str, response_data: dict) -> DataFrame:
        """
        Adds the new data column to the ongoing dataframe using the response data

        Args:
            df (DataFrame) - the ongoing dataframe to add the new data column to

            column_name (str) - the name of the new data column

            response_data (dict) - the response data

        Returns:
            DataFrame - the updated dataframe with the new data column added
        """
        data_points = response_data["data"]["waterlevel"]

        # extract timestamps and values into separate lists
        data_timestamps = [p["t"] for p in data_points]
        data_values     = [p["o"] for p in data_points]
        
        # create a new df where the data points are indexed by their timestamps
        # the timestamps are converted to datetime objects in UTC then remove the timezone information
        index = to_datetime(data_timestamps, utc=True).tz_localize(None)
        new_df = DataFrame({column_name: data_values}, index=index)

        # remove any duplicate timestamps
        new_df = new_df[~new_df.index.duplicated()]

        # outer join to preserve all timestamps from both dataframes
        return df.join(new_df, how='outer')
