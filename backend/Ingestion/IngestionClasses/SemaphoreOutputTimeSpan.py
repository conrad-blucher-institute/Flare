"""
SemaphoreOutputTimeSpan.py

This ingestion class is for querying the output time span endpoint from Semaphore.

Created by: CJ Quintero
Created on: 11/19/2026
"""
from os import getenv
from datetime import timedelta, datetime

from Ingestion.I_Ingestion import IDataIngestion
from runtimeContext import thread_storage
from Ingestion.Ingestion_Utility import api_request, add_empty_column
from pandas import DataFrame, Series, to_datetime


class SemaphoreOutputTimeSpan(IDataIngestion):
    """
    ingestion class for querying the output time span endpoint from Semaphore.

    cspec data request call
    {
        "key": "SemaphoreOutputTimeSpan",
        "args": {
            "column_name": "Magnolia",
            "time_range": [0, 48],
            "models": ["magnolia_12", "magnolia_24", "magnolia_48"]
        }
    }
    """

    def __init__(self):
        self.logger = thread_storage.logger

    
    def ingest_data(self, df: DataFrame, reference_time: datetime, column_name: str, time_range: list[int], models: list[str]) -> DataFrame:
        """
        Ingests data from the Semaphore output time span endpoint

        Args:
            df (DataFrame) - the ongoing dataframe to add the new data column to

            reference_time (datetime) - the reference time for this run. Ex, if a cspec
                is ran at 12:20, then the reference_time would be 12:20.
            
            column_name (str) - the name of the new data column to add to the ongoing dataframe

            time_range (list[int]) - the range of hours to query data for relative to the reference time.
                Ex, [0, 48] would query for predictions that have verified times between now and 48 hours in the future.
            
            models (list[str]) - the list of models to query data for
        
        Returns:
            DataFrame - the ongoing dataframe with the new data column added
        """

        url = self._build_url(reference_time, time_range, models)
        if url is None:
            return add_empty_column(df, column_name)

        resp = api_request(url)
        valid_resp = self._validate_response(resp)
        if valid_resp is None:
            return add_empty_column(df, column_name)

        try:
            series = self._build_series(valid_resp, column_name)
            return df.join(series, how='outer')
        except Exception as e:
            # catch all exceptions to add an empty column instead of
            # stopping the exec when building the series fails
            self.logger.log_error(f"Error adding Semaphore output time span data. Exception: {e}")
            return add_empty_column(df, column_name)


    def _build_url(self, reference_time: datetime, time_range: list[int], models: list[str]) -> str | None:
        """
        Builds the URL for the Semaphore output time span endpoint

        Args:
            reference_time (datetime) - the reference time for this run. Ex, if a cspec
                is ran at 12:20, then the reference_time would be 12:20.
            
            time_range (list[int]) - the range of hours to query data for relative to the reference time.
                Ex, [0, 48] would query for predictions that have verified times between now and 48 hours in the future.
            
            models (list[str]) - the list of models to query data for
        
        Returns:
            str | None - the URL for the Semaphore output time span endpoint
                or None if the SEMAPHORE_API_URL environment variable is not set
        """
        # calculate from and to times based on the reference time and range
        fromDateTime = reference_time + timedelta(hours=time_range[0])
        toDateTime = reference_time + timedelta(hours=time_range[1])

        # convert to url safe datetime
        fromDateTime = datetime.strftime(fromDateTime, '%Y%m%d%H')
        toDateTime = datetime.strftime(toDateTime, '%Y%m%d%H')

        base_path = getenv("SEMAPHORE_API_URL", None)
        if base_path is None:
            self.logger.log_error("SEMAPHORE_API_URL environment variable is not set")
            return None

        if not base_path.endswith('/'):
            base_path += '/'
        
        url = f'{base_path}output_time_span/?fromDateTime={fromDateTime}&toDateTime={toDateTime}'

        for model in models:
            url += f'&modelNames={model}'

        return url


    def _validate_response(self, response: dict | None) -> dict | None:
        """
        Validates the response from the Semaphore output time span endpoint and
        filters out any models that returned no data

        Args:
            response (dict | None) - the response from the Semaphore output time span endpoint
                or None if the request failed

        Returns:
            dict | None - the response with only the models that have data,
                or None if the request failed or no model has data
        """

        # response reason for being None is logged in the api_request function
        if response is None:
            return None

        valid_models = {}
        for model_name, model_series in response.items():
            # skip models that don't exist or returned no data points
            if not model_series or len(model_series['_Series__data']) == 0:
                self.logger.log_info(f"Semaphore output time span response for {model_name} has no data")
                continue

            valid_models[model_name] = model_series

        # every model was empty, so there is nothing to add
        if not valid_models:
            return None

        return valid_models


    def _build_series(self, resp: dict, column_name: str) -> Series:
        """
        Returns the data points for the new data column to add to the ongoing dataframe

        Args:
            resp (dict) - the response from the Semaphore output time span endpoint
            
            column_name (str) - the name of the new data column to add to the ongoing dataframe
        
        Returns:
            Series - a series of data points for the new data column to add to the ongoing dataframe
        """

        # flatten every data point from every model into one list of rows
        rows = []
        for series in resp.values():
            for point in series['_Series__data']:
                rows.append({
                    'timeVerified': point['timeVerified'],
                    'leadTime': point['leadTime'],
                    column_name: point['dataValue'][0][0][0]
                })
        
        # create a temp df so the rows can be sorted and de-duplicated
        points = DataFrame(rows)
        points['timeVerified'] = to_datetime(points['timeVerified'])

        # when multiple models predict the same time, keep the point with the lowest lead time
        points = (
            points.sort_values('leadTime')
                  .drop_duplicates(subset='timeVerified', keep='first')
                  .set_index('timeVerified')
                  .sort_index()
        )

        # only return a single combined series of data points for the column name
        return points[column_name]
