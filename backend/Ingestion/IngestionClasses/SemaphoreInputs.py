# -*- coding: utf-8 -*-
#SemaphoreInputs.py
#----------------------------------
# Created By: Matthew Kastl
#----------------------------------
"""This class ingests data from the Semaphore API. This specifically targets the input endpoint.
NOTE:: reads the env "SEMAPHORE_API_URL" for the base url to hit.
 """ 
#----------------------------------
# 
#
#Imports
from Ingestion.I_Ingestion import IDataIngestion
from datetime import datetime, timedelta
from Ingestion.Ingestion_Utility import api_request, add_empty_column
from pandas import DataFrame
from numpy import nan
from os import getenv


class SemaphoreInputs(IDataIngestion):

    def ingest_data(self, data: DataFrame, ref_time: datetime, column_name: str, range: list[int], source: str, series: str, location: str, interval: str, datum: str = None):
        '''Ingests data from the Semaphore Inputs API.'''

        url = self.__prepare_url(ref_time, range, source, series, location, interval, datum)

        response = api_request(url)
        if not self.__validate_response(response):
            return add_empty_column(data, column_name)
        
        return self.__add_data(df= data, data_points= response['_Series__data'], col_name= column_name)


    def __prepare_url(self, ref_time: datetime, range: list[int], source: str, series: str, location: str, interval: str, datum: str = None) -> str:
        '''Builds the URL for the Semaphore API given the request parameters.'''
        # Computer time range using range and interval
        fromTimeOffset = timedelta(seconds=float(interval) * range[0]) 
        toTimeOffset = timedelta(seconds=float(interval) * range[1]) 

        fromDateTime = ref_time + fromTimeOffset
        toDateTime = ref_time + toTimeOffset

        # Convert to urlsafe datetime
        fromDateTime = datetime.strftime(fromDateTime, '%Y%m%d%H')
        toDateTime = datetime.strftime(toDateTime, '%Y%m%d%H')

        url = f'{getenv("SEMAPHORE_API_URL")}input/source={source}/series={series}/location={location}/fromDateTime={fromDateTime}/toDateTime={toDateTime}'
        if datum != None: url += f'?datum={datum}'
        return url
    

    def __validate_response(self, response: dict[any]) -> bool:
        '''Checks for things like no data, empty response or non complete warnings.'''
        
        if response is None: return False
        if not response['isComplete']: print(f'Warning:: Api response warns its not complete -> {response["nonCompleteReason"]}')
        if len(response['_Series__data']) <= 0: return False
        return True
    
    
    def __add_data(self, df: DataFrame, data_points: list[dict[any]], col_name: str) -> DataFrame:
        '''Takes the data returned by the semaphore API, parses it into a pandas series, and adds it to the
        dataframe with all the other data.'''
        index = []
        data = []
        for datapoint in data_points:

            # Convert the string datetime into a proper datetime
            index.append(datetime.strptime(datapoint['timeVerified'], '%Y-%m-%dT%H:%M:%S'))

            # Check its not a null datapoint
            value = datapoint['dataValue']
            if (value == 'None') or (value is None): value = nan
            else: 
                value = float(value)
            data.append(value)

        # Add this to the collation df with an outer join to ensure all data is preserved
        return df.join(DataFrame({col_name: data}, index=index), how='outer')