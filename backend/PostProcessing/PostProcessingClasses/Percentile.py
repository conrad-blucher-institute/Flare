# -*- coding: utf-8 -*-
# Percentile.py
# -------------------------------
# Created By : Christian Quintero, Jeremiah Sosa
# Last Updated : 06/04/2025
# -------------------------------
"""
This file is a postprocessing class under the IPostProcessing interface.

This file calculates the value at a given percentile and creates 2 new columns: One for the VALUE at the given percentile, 
and one for a TAG that says if the input value is above or below the computed percentile value.
"""
# -------------------------------

# imports
from PostProcessing.IPostProcessing import IPostProcessing  # for post processing interface
from pandas import DataFrame                                # for DataFrame object


class Percentile(IPostProcessing):

    def post_process(self, df: DataFrame, col_key: str, percentile: int, output_col_key: str, **kwargs) -> DataFrame:
        """
        This method creates 2 new columns: One for the VALUE at the given percentile, 
        and one for a TAG that says if the input value is above or below the computed percentile value.

        The tag is considered BELOW if the value is less than or equal to the computed percentile value,
        and ABOVE otherwise.


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
                "percentile": "",        # the percentile to compute
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

        # calculate the percentile
        calculated_percentile_value = df[col_key].quantile(percentile/100)

        # store the percentile value in each row. The value here will be repeated
        # for each row in this output column.
        df[f"{output_col_key} Value"] = calculated_percentile_value

        # assign a tag to each row that says if the input value is above or below
        # the calculated value.
        df[f"{output_col_key} Tag"] = df[col_key].apply(lambda x: "Below" if x <= calculated_percentile_value else "Above")

        # return the data frame object with the added columns 
        return df

        

        


    
