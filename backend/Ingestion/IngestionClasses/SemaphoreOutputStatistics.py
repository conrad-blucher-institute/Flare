# -*- coding: utf-8 -*-
# SemaphoreOutputStatistics.py
# Created By: Christian Quintero
# Created On: 05/13/2026
"""
This class ingests data from the output_statistics endpoint of the Semaphore API.
NOTE:: reads the env "SEMAPHORE_API_URL" for the base url to hit.
"""
from Ingestion.I_Ingestion import IDataIngestion
from datetime import datetime, timedelta
from Ingestion.Ingestion_Utility import api_request, add_empty_column
from flareRunner import thread_storage 
from pandas import DataFrame
from os import getenv
import numpy as np
import re


class SemaphoreOutputStatistics(IDataIngestion):
    STATISTICS = ['p1', 'p5', 'p10', 'p25', 'p50', 'p75', 'p90', 'p95', 'p99', 'min', 'max', 'mean', 'std_dev']

    def ingest_data(self, data: DataFrame, ref_time: datetime, model_names: list[str]):
        '''
        Ingests data from a Semaphore API endpoint

        :param data: dataframe - the dataframe object to fill with data
        :param ref_time: datetime - the reference time for the data request, this is unused for this ingestion class
        :param model_names: list[str] - the names of the models to request data for

        :returns: dataframe - a new dataframe with the ingested data added
        '''

        url = self.__prepare_url(model_names)
        response = api_request(url)
        validated_response = self.__validate_response(response)
        return self.__add_data(df= data, response=validated_response)


    def __prepare_url(self, model_names: list[str]) -> str:
        '''
        This function builds the URl for the API request based on the model names provided

        :params model_names: list[str] - the names of the models to request data for

        :returns: str - the URL to hit for the API request
        '''

        # the base url for the semaphore api, already ending with a slash
        base_url = getenv("SEMAPHORE_API_URL")
        url = f'{base_url}output_statistics/?'

        # append each model name as a query parameter
        # the resulting url will look like
        # https://sherlock-prod.tamucc.edu/semaphore-api/output_statistics/?modelNames=CRPS_6hr&modelNames=MRE_Bird-Island_Water-Temperature_120hr&
        for model_name in model_names: url += f'modelNames={model_name}&'
        return url[:-1]  # remove the trailing '&'
    

    def __validate_response(self, response: dict) -> dict[str, dict] | None:
        '''
        This function validates the response from the semaphore API by checking for
        empty responses and missing data then retuns a dictionary containing only valid data
        that has statistics or None if no valid data is present

        :params response: dict - the response from the API request
            the response will look like 
            {
                "CRPS_6hr": {
                    "modelName": "CRPS_6hr",
                    "timeGenerated": "2026-05-12T12:00:00",
                    "p1": 25.20813787460327,
                    "p5": 25.744343280792236,
                    "p10": 25.94855365753174,
                    "p25": 26.22447681427002,
                    "p50": 26.485905647277832,
                    "p75": 26.73847484588623,
                    "p90": 27.00280132293701,
                    "p95": 27.201376342773436,
                    "p99": 27.95702182769775,
                    "min": 22.700056076049805,
                    "max": 29.92579460144043,
                    "mean": 26.486501573524475,
                    "std_dev": 0.48822468208073955
                },
                "model_that_doesn't_exit": null,
                ...
            }

        :returns dict[str, dict] | None - a dictionary containing only valid data that has statistics or None if no valid data is present
        '''
        logger = thread_storage.logger
        validated_response = {}

        if response is None:
            logger.log_info('Warning:: Failed to ingest statistics response from the Semaphore API!')
            return None
        
        # filter out nulls in the response to only include models that compute statistics
        for key, value in response.items():
            if value is None:
                logger.log_info(f'Warning:: Model statistics for key: {key} missing in returned data!')
                continue
            else:
                validated_response[key] = value

        # catch cases where all models are missing or have no data
        if validated_response == {}:
            return None
        else:
            return validated_response
    
    
    def __add_data(self, df: DataFrame, response: dict[str, dict]) -> DataFrame:
        '''
        Takes the validated response dict and adds it into the dataframe

        :param df: dataframe - the dataframe to add the data to
        :param response: dict[str, dict] | None - the validated response from the API request or None if the response was invalid
            the response will look like 
            {
                "CRPS_6hr": {
                    "modelName": "CRPS_6hr",
                    "timeGenerated": "2026-05-12T12:00:00",
                    "p1": 25.20813787460327,
                    "p5": 25.744343280792236,
                    "p10": 25.94855365753174,
                    "p25": 26.22447681427002,
                    "p50": 26.485905647277832,
                    "p75": 26.73847484588623,
                    "p90": 27.00280132293701,
                    "p95": 27.201376342773436,
                    "p99": 27.95702182769775,
                    "min": 22.700056076049805,
                    "max": 29.92579460144043,
                    "mean": 26.486501573524475,
                    "std_dev": 0.48822468208073955
                },
                ...
            }

        :returns: dataframe - the ongoing dataframe with the new data joined to it
        '''
        logger = thread_storage.logger

        # if there is no valid data to add, then add empty columns into the dataframe and return it
        if response is None:
            df[[f"Water Temperature Prediction {stat}" for stat in self.STATISTICS]] = np.nan
            return df

        rows = []
        for _, value in response.items():
            '''
            since the lead time isn't explicitly given in the response, we have to
            extract it since the lead times are tied to the model name
            
            Ex) CRPS_6hr has a lead time of 6 hours, so the 6 is extracted and 6 hours are added
                to the time generated to get the verified time which is used as the index for the data

            TODO  Remove this once the API returns the lead time
            '''
            model_name = value['modelName']
            match = re.search(r'(\d+)hr', model_name)
            if match:
                lead_time = int(match.group(1))
            else:
                logger.log_info(f'Warning:: Could not extract lead time from model name {model_name}')
                continue
            
            timeGenerated = datetime.strptime(value['timeGenerated'], '%Y-%m-%dT%H:%M:%S')
            verifiedTime = timeGenerated + timedelta(hours=lead_time)

            row = {'verifiedTime': verifiedTime}
            for stat in self.STATISTICS:
                row[f'Water Temperature Prediction {stat}'] = value.get(stat, np.nan)
            rows.append(row)
        
        df_stats = DataFrame(rows)

        # catch cases where models do give a valid response but all regex extractions fail
        if df_stats.empty:
            df[[f"Water Temperature Prediction {stat}" for stat in self.STATISTICS]] = np.nan
            return df

        df_stats = DataFrame(rows).set_index('verifiedTime')

        # join the data frames with an outer join to ensure all data is preserved
        return df.join(df_stats, how='outer')