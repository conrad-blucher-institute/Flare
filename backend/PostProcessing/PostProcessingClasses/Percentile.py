# -*- coding: utf-8 -*-
# Percentile.py
# -------------------------------
# Created By : Christian Quintero, Jeremiah Sosa
# Last Updated : 06/05/2025
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

        The tag is considered BELOW if the value is less than or equal to the computed percentile value,
        and ABOVE otherwise.

        This assumes that 'df[col_key]' is a column of lists such as a list of floats or ints


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

        # calculate the percentile value for each list in the column
        #
        # 'values' is a list of numbers from each row in the specified column
        def calc_percentile(values):
            return np.percentile(values, percentile)

        # add the percentile value column using .apply on each list of values
        df[f"{output_col_key} Value"] = df[col_key].apply(calc_percentile)

        # for each row, compare each value in the list to the calculated percentile value
        # and tag it as "Below" if it's <= the percentile value, "Above" otherwise
        def tag_values(row):
            return ["Below" if val <= row[f"{output_col_key} Value"] else "Above" for val in row[col_key]]

        # add the percentile tag column using .apply across rows
        df[f"{output_col_key} Tag"] = df.apply(tag_values, axis=1)

        # return the data frame with the added columns
        return df
    
