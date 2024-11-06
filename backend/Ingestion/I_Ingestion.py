# -*- coding: utf-8 -*-
#I_Ingestion.py
#----------------------------------
# Created By: Matthew Kastl
#----------------------------------
"""Ingestion is responsible for inserting data into the software. This module provides
an interface to decouple this process from the main body of code. The factory method will 
import and execute the correct code for a given process (based on a keyword) returning the result.
New data will be inserted into the dataframe by reference
 """ 
#----------------------------------
# 
#
#Imports
from abc import ABC, abstractmethod
from importlib import import_module
from pandas import DataFrame


class IDataIngestion(ABC):

    @abstractmethod
    def ingest_data(self, data: DataFrame, **kwargs) -> bool:
        raise NotImplementedError
    

def data_ingestion_factory(data: DataFrame, key: str, **kwargs) -> bool:
    """ Initiates a call to a class of IDataIngestion returning the result. The call is determined by a passed key, and arguments through the kwargs.
        :param data: DataFrame - A pre initialized data frame to insert collected data into
        :param key: str - The string key that will be used to detect the correct module.
        :kwargs: dict - The keyword args to pas to the resulting method. Make sure this is formatted as the targeted method wants.
        :returns bool - True indicated the process succeeded while false indicated it failed for some reason. 
    """
    try:
        ingestion_class: IDataIngestion = getattr(import_module(f'.IngestionClasses.{key}', 'Ingestion'), key)()
        return ingestion_class.ingest_data(data, kwargs)
    except ModuleNotFoundError:
        raise ModuleNotFoundError(f'[Error]:: No module named {key} in IngestionClasses!')
    except TypeError:
        raise TypeError(f'[Error]:: kwargs mismatch for key: {key} and kwargs: {kwargs}')
    