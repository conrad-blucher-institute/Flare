# -*- coding: utf-8 -*-
# Hohonu.py
# Created By: CJ Quintero
# Created On: 10/15/2026
"""
This ingestion class is for querying the output time span endpoint from Semaphore.
"""
from os import getenv
from datetime import timedelta, datetime

from Ingestion.I_Ingestion import IDataIngestion
from runtimeContext import thread_storage
from Ingestion.Ingestion_Utility import api_request, add_empty_column
from pandas import DataFrame, to_datetime


class SemaphoreOutputTimeSpan(IDataIngestion):

    def __init__(self):
        self.logger = thread_storage.logger

    
    def ingest_data(self, df: DataFrame, reference_time: str, column_name: str, range: list[int], models: list[str]) -> DataFrame:
        """
        Ingests data from the Semaphore output time span endpoint

        Args:
            df (DataFrame) - the ongoing dataframe to add the new data column to

            reference_time (str) - the reference time for this run. Ex, if a cspec
                is ran at 12:20, then the reference_time would be 12:20.
            
            column_name (str) - the name of the new data column to add to the ongoing dataframe

            range (list[int]) - the range of hours to query data for relative to the reference time.
                Ex, [0, 48] would query for predictions that have verified times between now and 48 hours in the future.
            
            models (list[str]) - the list of models to query data for
        
        Returns:
            DataFrame - the ongoing dataframe with the new data column added
        """

        url = self._build_url(reference_time, range, models)

        resp = api_request(url)
        if not self._validate_response(resp):
            return add_empty_column(df, column_name)

        try:
            return self._add_data(df, resp, column_name)
        except Exception as e:
            self.logger.log_error(f"Error adding Semaphore output time span data. Exception: {e}")
            return add_empty_column(df, column_name)


    def _build_url(self, reference_time: str, range: list[int], models: list[str]) -> str:
        """
        Builds the URL for the Semaphore output time span endpoint

        Args:
            reference_time (str) - the reference time for this run. Ex, if a cspec
                is ran at 12:20, then the reference_time would be 12:20.
            
            range (list[int]) - the range of hours to query data for relative to the reference time.
                Ex, [0, 48] would query for predictions that have verified times between now and 48 hours in the future.
            
            models (list[str]) - the list of models to query data for
        
        Returns:
            str - the URL for the Semaphore output time span endpoint
        """
        # calculate from and to times based on the reference time and range
        fromDateTime = reference_time + timedelta(hours=range[0])
        toDateTime = reference_time + timedelta(hours=range[1])

        # convert to url safe datetime
        fromDateTime = datetime.strftime(fromDateTime, '%Y%m%d%H')
        toDateTime = datetime.strftime(toDateTime, '%Y%m%d%H')

        url =f'{getenv("SEMAPHORE_API_URL")}output_time_span/?fromDateTime={fromDateTime}&toDateTime={toDateTime}'

        for model in models:
            url += f'&modelNames={model}'

        return url


    def _validate_response(self, response: dict) -> bool:
        """
        Validates the response from the Semaphore output time span endpoint

        Args:
            response (dict) - the response from the Semaphore output time span endpoint
        
        Returns:
            bool - True if the response is valid, False otherwise
        """
        # check for None response
        if response is None:
            self.logger.log_error("Semaphore output time span response is None")
            return False

        # the response is keyed by model name, so validate each model's series
        for model_name, series in response.items():
            # check for incomplete response
            if not series['isComplete']:
                self.logger.log_info(f"Semaphore output time span response for {model_name} is incomplete. Reason: {series.get('nonCompleteReason')}")
                return False

            # check for no data in the response
            if len(series['_Series__data']) <= 0:
                self.logger.log_info(f"Semaphore output time span response for {model_name} has no data")
                return False

        return True


    def _add_data(self, df: DataFrame, resp: dict, column_name: str) -> DataFrame:
        """
        Adds the data points from the Semaphore output time span endpoint to the ongoing dataframe

        Args:
            df (DataFrame) - the ongoing dataframe to add the new data column to
            
            resp (dict) - the response from the Semaphore output time span endpoint
            
            column_name (str) - the name of the new data column to add to the ongoing dataframe
        
        Returns:
            DataFrame - the ongoing dataframe with the new data column added
        """

        # flatten every data point from every model into one list of rows
        rows = []
        for series in resp.values():
            for point in series['_Series__data']:
                rows.append({
                    'time': point['timeVerified'],
                    column_name: point['dataValue'][0][0][0],
                    'lead_time': point['leadTime'],
                })

        # create a temp df for the rows and convert the time column to datetime objects
        points = DataFrame(rows)
        points['time'] = to_datetime(points['time'])

        # when multiple models predict the same time, keep the point with the lowest lead time
        points = (
            points.sort_values('lead_time')
                  .drop_duplicates(subset='time', keep='first')
                  .set_index('time')
                  .sort_index()
        )

        new_df = points[[column_name]]
        return df.join(new_df, how='outer')
