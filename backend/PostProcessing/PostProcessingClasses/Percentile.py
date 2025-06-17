# -*- coding: utf-8 -*-
# Percentile.py
# -------------------------------
# Created By : Christian Quintero, Jeremiah Sosa
# Last Updated : 06/08/2025
# -------------------------------
"""
This file is a postprocessing class under the IPostProcessing interface.

This class calculates a specified percentile for a column where each cell contains a list of values.
It then creates a new column showing the computed percentile value per row.
"""
# -------------------------------

# imports
from PostProcessing.IPostProcessing import IPostProcessing  
from pandas import DataFrame                               
import numpy as np                                          


class Percentile(IPostProcessing):

    def post_process(self, df: DataFrame, col_key: str, percentile: int, output_col_key: str) -> DataFrame:
        """
        This method creates a new column for the percentile value of a specified column in the DataFrame.
        
        The computed percentile value is NaN if the input list is empty or not a list.

        Args:
            df (DataFrame): The DataFrame containing the collected data.
            col_key (str): The column name to calculate the percentiles from.
            percentile (int): The requested percentile to calculate. 
                The percentile is in percentage form, so the value must be an integer between 0-100.
            output_col_key (str): The base name for the output column.

        Returns:
            DataFrame : The dataframe with the added percentile value column.

        JSON Call:
        {
            "key": "Percentile",
            "args": {
                "col_key": "",           # name of the column 
                "percentile": 5,         # the percentile to compute, for example 5 for the 5th percentile
                "output_col_key": ""     # the base name for the output columns
            }
        },  
        """

        # make a copy of the data to prevent changing the original data frame 
        df = df.copy()

        # validate the input column 
        if col_key not in df.columns:
            raise KeyError(f"Column '{col_key}' not found. Available columns: {df.columns.tolist()}")
        
        # try to cast the input into an integer
        # this will raise a ValueError if the input is not an integer
        try:
            percentile = int(percentile)
        except (ValueError, TypeError):
            raise ValueError(f"Percentile '{percentile}' must be an integer.")

        # now validate the integers range
        if not 0 <= percentile <= 100:
            raise ValueError(f"Percentile '{percentile}' is not in a valid range. Must be between 0 and 100.")

        
        def calc_percentile(values):
            """
            calc_percentile method

            calculates the percentile value for a list of values in a row

            runs for each row in the data frame
            
            Args:
                values (list): A list of numerical values from the specified column.

            Returns:
                float: The computed percentile value for the list of values.
                NaN: if the list is empty or not a list.
            """

            # if 'values' is an empty list or not a list, return NaN
            if not isinstance(values, (list, tuple, np.ndarray)) or len(values) == 0:
                return np.nan

            # cast to a float array
            arr = np.array(values, dtype=float)

            # nanpercentile will ignore NaNs in the values array
            return np.nanpercentile(arr, percentile)
            
           
        # add the percentile value column using .apply on each list of values
        df[f"{output_col_key} Value"] = df[col_key].apply(calc_percentile)

        # return the data frame with the added column
        return df
    
