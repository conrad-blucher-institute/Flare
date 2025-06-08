# -*- coding: utf-8 -*-
# Percentile.py
# -------------------------------
# Created By : Christian Quintero, Jeremiah Sosa
# Last Updated : 06/08/2025
# -------------------------------
"""
This file is a postprocessing class under the IPostProcessing interface.

This class calculates a specified percentile for a column where each cell contains a list of values.
It then creates two new columns: one showing the computed percentile value per row,
and another tagging each value in the original list as "Above" or "Below" the computed percentile.
"""
# -------------------------------

# imports
from PostProcessing.IPostProcessing import IPostProcessing  # for post processing interface
from pandas import DataFrame                                # for DataFrame object
import numpy as np                                          # for percentile() method


class Percentile(IPostProcessing):

    def post_process(self, df: DataFrame, col_key: str, percentile: int, output_col_key: str) -> DataFrame:
        """
        This method creates 2 new columns: One for the VALUE at the given percentile, 
        and one for a TAG that says if the input value is above or below the computed percentile value.
        
        The computed percentile value is NaN if the input list is empty or not a list.

        The tag is considered Below if the value is less than or equal to the computed percentile value,
        and Above if the value is greater than the computed percentile value.
        The tag is None if the computed percentile value is NaN.


        Args:
            df (DataFrame): The DataFrame containing the collected data.
            col_key (str): The column name to calculate the percentiles from.
            percentile (int): The requested percentile to calculate. 
                The percentile is in percentage form, so the value must be an integer between 0-100.
            output_col_key (str): The base name for the output columns.

        Returns:
            DataFrame : The dataframe with the added percentile value and percentile tag columns.

        JSON Call:
        {
            "key": "Percentile",
            "args": {
                "col_key": "",           # name of the column 
                "percentile": 5,         # the percentile to compute
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
        try:
            percentile = int(percentile)
        except (ValueError, TypeError):
            raise ValueError(f"Percentile '{percentile}' must be an integer between 0 and 100.")

        # validate the range 
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

        def tag_values(row):
            """
            tag_values method

            gives a tag for each value in the list based on the computed percentile value
            if the value is less than or equal to the percentile value, it is tagged as "Below"
            if the value is greater than the percentile value, it is tagged as "Above"
            if the value is NaN, it is tagged as None

            this method runs for each row in the data frame

            Args:
                row (Series): A row of the DataFrame containing the percentile value (computed above) and the list of values (ensemble data).

             Returns:
                List[str]: A list of tags ("Below", "Above", or None) corresponding to each value in the list.
            """

            # get the percentile value and the list of values from the row
            percentile_value = row[f"{output_col_key} Value"]
            vals = row[col_key]

            # ensure vals is a list or array-like structure
            if not isinstance(vals, (list, tuple, np.ndarray)):
                # if vals is not a list, return an empty list
                vals = []

            # if the percentile value is NaN, give a None tag for each val
            if np.isnan(percentile_value):
                return [None] * len(vals)
            
            # compare the values to the percentile value and tag them accordingly
            return ["Below" if v <= percentile_value else "Above" for v in vals]

        # add the percentile tag column using .apply across rows
        df[f"{output_col_key} Tag"] = df.apply(tag_values, axis=1)

        # return the data frame with the added columns
        return df
    
