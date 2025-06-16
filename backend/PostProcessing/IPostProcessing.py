# -*- coding: utf-8 -*-
#IPostProcessing.py
#----------------------------------
# Created By: Matthew Kastl
#----------------------------------
"""Post processing is responsible for preforming operation on data within the collection of data. 
An example of this could be preforming an arithmetic operation on a column of data or cleaning missing values.)
This module provides an interface to decouple this process from the main body of code. The factory method will 
import and execute the correct code for a given process (based on a keyword) returning the result.
New data will be inserted into the DataFrame by reference
 """ 
#----------------------------------
# 
#
#Imports
from abc import ABC, abstractmethod
from importlib import import_module
from pandas import DataFrame
from utility import log_error,get_current_chart_name


class IPostProcessing(ABC):

    @abstractmethod
    def post_process(self, data: DataFrame, **kwargs) -> DataFrame:
        raise NotImplementedError
    

def post_process_factory(data: DataFrame, key: str, kwargs) -> DataFrame:
    """ Initiates a call to a class of IDataIngestion returning the result. The call is determined by a passed key, and arguments through the kwargs.
        :param data: DataFrame - A pre initialized data frame to insert collected data into
        :param key: str - The string key that will be used to detect the correct module.
        :kwargs: dict - The keyword args to pas to the resulting method. Make sure this is formatted as the targeted method wants.
        :returns bool - True indicated the process succeeded while false indicated it failed for some reason. 
    """
    try:
        post_processing_class: IPostProcessing = getattr(import_module(f'.PostProcessingClasses.{key}', 'PostProcessing'), key)()
        return post_processing_class.post_process(data, **kwargs)
    except ModuleNotFoundError:
        log_error(message=f'No module named {key} in PostProcessingClasses!',chart_name=get_current_chart_name(),error_type='ModuleNotFoundError')
        raise ModuleNotFoundError(f'[Error]:: No module named {key} in PostProcessingClasses!')
    except TypeError as e:
        log_error(message=f'{e}.kwargs mismatch for key: {key} and kwargs: {kwargs}',chart_name=get_current_chart_name(),error_type='TypeError')
        raise TypeError(f'[Error]:: kwargs mismatch for key: {key} and kwargs: {kwargs}')
    