# -*- coding: utf-8 -*-
# LinearInterpolation.py
#-------------------------------
# Created By: Christian Quintero
# Last Updated: 08/13/2025
#-------------------------------
"""
The post processing in this file performs linear interpolation of a column.
""" 
#-------------------------------
# 
#
#Imports
from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame, date_range
import numpy as np
import pandas as pd
from datetime import timedelta

class LinearInterpolation(IPostProcessing):

    # Dummy value used to replace large gaps in the data
    DUMMY_VALUE = -9999  

    def post_process(self, df: DataFrame, col_name: str, interpolation_interval: int, limit: int) -> DataFrame:
        """The post processing in this file performs a linear interpolation of a column.

        Args:
            df: DataFrame: The DataFrame containing the data we want to interpolate.
            col_name: str - The column in the DataFrame to interpolate.
            interpolation_interval: int - The interval to interpolate data on, in seconds.
            limit: int - The amount of consecutive NaNs in a row to interpolate.

        Returns:
            DataFrame : A new dataframe obj might have to be created, this will always be a reference to the most updated version.

        NOTE::This function actually uses time based interpolation which is the same as linear interpolation.

        JSON Call:
        {
            "key": "LinearInterpolation",
            "args": {
                "col_name": "",
                "interpolation_interval": -1,
                "limit": -1
            }
        },
        """

        # Validate the arguments passed to the post_process method
        self.validate_args(df, col_name, interpolation_interval, limit)

        # If the limit is zero, do nothing and return the original DataFrame.
        if limit == 0:
            return df
        
        # Isolate the data series we are going to interpolate
        data_series = df[col_name]

        # The index of the data frame isn't necessarily correct for the values we want to interpolate for this series. Thus we reindex
        # the data to the specific interval we want to interpolate on.
        data_series = data_series.reindex(date_range(start=data_series.index[0], end=data_series.index[-1], freq=timedelta(seconds=interpolation_interval)))

        # make a copy of the data and find gaps larger than the limit
        # gaps larger than the limit will be replaced with a dummy value (-9999)
        # gaps smaller than the limit will be left as NaN
        masked_data_series = self.fill_large_gaps(data_series.copy(), limit)

        # interpolate the entire series
        # this will fill all the small NaN gaps and leave the dummy values in the large gaps
        interpolated_data_series = masked_data_series.interpolate(limit_area='inside', method='time')

        # find all dummy values and replace them with NaN
        interpolated_data_series.loc[interpolated_data_series == self.DUMMY_VALUE] = np.nan

        # drop original column and replace with the interpolated one
        df.drop(columns=[col_name], inplace=True)
        df = df.join(interpolated_data_series, how='outer')

        return df
    


    def validate_args(self, df: DataFrame, col_name: str, interpolation_interval: int, limit: int):
        """
        This method validates the arguments passed to the post_process method.

        NOTE:: A limit of 0 is a special case that will not interpolate any data, but will return the original DataFrame.
        This is done in the post_process method after validation, since this method does not return anything.
        """

        # df must be a pandas DataFrame
        if not isinstance(df, DataFrame):
            raise TypeError(f"[ERROR]:: DataFrame must be a pandas DataFrame, got {type(df)} instead.")
        
        # df cannot be empty
        if df.empty:
            raise ValueError("[ERROR]:: DataFrame is empty, cannot perform interpolation.")
        
        # Check if DataFrame has a datetime index
        if not isinstance(df.index, pd.DatetimeIndex):
            raise TypeError("[ERROR]:: DataFrame must have a DatetimeIndex for time-based interpolation.")
        
        # col_name must be a string
        if not isinstance(col_name, str):
            raise TypeError(f"[ERROR]:: Column name must be a string, got {type(col_name)} instead.")
        
        # col_name must be a valid column in the DataFrame
        if col_name not in df.columns:
            raise KeyError(f"Column '{col_name}' not found. Available columns: {df.columns.tolist()}")
        
        # interpolation_interval must be a positive integer
        if not isinstance(interpolation_interval, int):
            raise TypeError(f"[ERROR]:: Interpolation interval must be an integer, got {type(interpolation_interval)} instead.")
        
        # interpolation_interval must be greater than 0
        if interpolation_interval <= 0:
            raise ValueError(f"[ERROR]:: Interpolation interval must be greater than 0, got {interpolation_interval} instead.")
        
        # limit must be an integer
        if not isinstance(limit, int):
            raise TypeError(f"[ERROR]:: Limit must be an integer, got {type(limit)} instead.")
        
        # limit must be greater than or equal to 0.
        # A limit of 0 is a special case that will not interpolate any data, but will return the original DataFrame.
        if limit < 0:
            raise ValueError(f"[ERROR]:: Limit must be greater than or equal to 0, got {limit} instead.")



    def fill_large_gaps(self, temp_data_series: pd.Series, limit: int) -> pd.Series:
        """ 
        This method is used to find the gaps in the data that are larger than the limit.
        A for loop is used to iterate over the entire series, with a nested while loop to count consecutive NaNs. 
        If a gap > limit is found, it is replaced with a dummy value (-9999).
        After all large gaps are replaced, the series is returned with dummy values in place of large NaN gaps,
        keeping the small gaps as NaNs. 
        
        Args:
            temp_data_series: pd.Series - The series of data to find gaps in.
            limit: int - The maximum number of consecutive NaN entries that will be interpolated.
                Any group of consecutive NaNs that are larger than this value will stay as NaNs.

        Returns:
            pd.Series : A new series with dummy values in place of large NaN gaps, with small gaps left as NaN.
        
        """

        # initialize variables 
        nan_gap_start = None                 # to mark the beginning of a NaN gap aka NaN streak
        nan_gap_end = None                   # to mark the end of a NaN gap aka NaN streak
        nan_gap_size = None                  # to mark the size of a NaN gap. This is the difference between nan_gap_end - nan_gap_start 
        i = 0                                # index for iterating over the data series   


        # iterate over the data series
        while i < len(temp_data_series):
            
            # when a NaN is found, mark the start of a NaN gap
            if pd.isna(temp_data_series.iloc[i]):

                nan_gap_start = i

                # from the first NaN, continue to iterate until a non-NaN value is found
                while i < len(temp_data_series) and pd.isna(temp_data_series.iloc[i]):
                    i = i + 1
                
                # mark the end of a NaN gap
                nan_gap_end = i

                # by subtracting the start from the end, we can find the size of the NaN gap
                # for example, a nan_gap_size of 2 means 2 consecutive NaNs were found
                nan_gap_size = nan_gap_end - nan_gap_start

                # if the gap size is > limit, replace with dummy values, otherwise, leave the small gaps as NaN
                if nan_gap_size > limit:

                    # replace large gaps with dummy value
                    # excludes the nan_gap_end index
                    temp_data_series.iloc[nan_gap_start:nan_gap_end] = self.DUMMY_VALUE
            else:
                i = i + 1
        # end while loop
        
        # return the series with dummy values in place of large NaN gaps
        return temp_data_series



