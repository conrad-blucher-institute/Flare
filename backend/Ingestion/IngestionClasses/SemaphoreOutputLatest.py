# -*- coding: utf-8 -*-
#SemaphoreOutputLatest.py
#----------------------------------
# Created By: Matthew Kastl
#----------------------------------
"""This class ingests data from the Semaphore API. This specifically targets the latest output.
NOTE:: reads the env "SEMAPHORE_API_URL" for the base url to hit.
 """ 
#----------------------------------
# 
#
#Imports
from Ingestion.I_Ingestion import IDataIngestion
from datetime import datetime, timedelta
from Ingestion.Ingestion_Utility import api_request, add_empty_column
from utility import log_info
from pandas import DataFrame
from numpy import nan
from os import getenv


class SemaphoreOutputLatest(IDataIngestion):

    def ingest_data(self, data: DataFrame, ref_time: datetime, column_name: str, model_names: list[str]):
        '''Ingests data from the Semaphore Inputs API.'''

        url = self.__prepare_url(model_names)

        response = api_request(url)
        if not self.__validate_response(response, model_names):
            return add_empty_column(data, column_name)

        return self.__add_data(df= data, response=response, model_names=model_names, col_name= column_name)


    def __prepare_url(self, model_names: list[str]) -> str:
        '''Builds the URL for the Semaphore API given the request parameters.'''

        url = f'{getenv("SEMAPHORE_API_URL")}output_latest/?'
        for model_name in model_names: url += f'modelNames={model_name}&'
        return url[:-1]
    

    def __validate_response(self, response: dict[any], model_names: list[str]) -> bool:
        '''Checks for things like no data, empty response or non complete warnings.'''
        
        if response is None: return False
        for name in model_names:
            model_response = response.get(name)
            if model_response is None: 
                log_info(f'Warning:: Model {name} missing in returned data!')
                continue

            if not model_response['isComplete']: print(f'Warning:: Api response warns its not complete -> {model_response["nonCompleteReason"]}')
            if len(model_response['_Series__data']) <= 0: log_info(f'Warning:: Model {name} returned no data!')
        return True
    
    
    def __add_data(self, df: DataFrame, response: dict[any], model_names: list[str], col_name: str) -> DataFrame:
        '''Takes the data returned by the semaphore API, parses it into a pandas series, and adds it to the
        dataframe with all the other data.'''
        index = []
        data = []
        for name in model_names:
            model_response  = response[name]

            data_point = model_response['_Series__data'][0]

            timeGenerated = datetime.strptime(data_point['timeGenerated'], '%Y-%m-%dT%H:%M:%S')
            verifiedTime = timeGenerated + timedelta(seconds=data_point['leadTime'])
            index.append(verifiedTime)

            value = data_point['dataValue']
            if value == 'None': value = nan
            
            elif isinstance(value, list):
                # Convert all elements to float
                value = [float(v) for v in value]
            
            else: value = float(value)
            data.append(value)

        # Add this to the collation df with an outerjoin to ensure all data is preserved
        return df.join(DataFrame({col_name: data}, index=index), how='outer')