# -*- coding: utf-8 -*-
# LinearInterpolation.py
#-------------------------------
# Created By: Christian Quintero
# Last Updated: 09/12/2025
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
import logging

class LinearInterpolation(IPostProcessing):

    # Dummy values used to mark to large time gaps that should not be interpolated
    DUMMY_VALUE = -9999


    def post_process(self, df: DataFrame, col_name: str, interpolation_interval: int, limit: int) -> DataFrame:
        """The post processing in this file performs a linear interpolation of a column.

        Args:
            df: DataFrame: The DataFrame containing the data we want to interpolate.
            col_name: str - The column in the DataFrame to interpolate.
            interpolation_interval: int - The interval to interpolate data on, in seconds.
            limit: int - The amount of time between 2 real values that will be interpolated, in seconds.

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

        # If the limit is zero, do nothing and return the data frame
        if limit == 0:
            return df

        # make a copy of the original data frame to avoid modifying it directly
        df = df.copy()

        # Isolate the data series we are going to interpolate
        data_series = df[col_name]

        # Count the number of non-NaN values in the original data series for logging purposes 
        original_data_count = data_series.dropna().shape[0]

        # the data series isn't guaranteed to be indexed at the specified interval
        # so we reindex the series to the specified interval
        reindexed_data_series = data_series.reindex(date_range(start=data_series.index[0], end=data_series.index[-1], freq=timedelta(seconds=interpolation_interval)))

        # find gaps whose timestamps difference is larger than the limit
        # time gaps larger than the limit will be replaced with a dummy value (-9999)
        # time gaps smaller than the limit will be left as NaN
        masked_data_series = self.fill_large_gaps(reindexed_data_series, limit)
        
        # interpolate the entire series using time based interpolation and only fill NaNs between real values
        # this will fill all the small NaN gaps and leave the dummy values in the large time gaps
        interpolated_data_series = masked_data_series.interpolate(limit_area='inside', method='time')

        # find all dummy values and replace them with NaN
        interpolated_data_series.loc[interpolated_data_series == self.DUMMY_VALUE] = np.nan

        # Log if data was lost during reindexing
        interpolted_data_series_count = interpolated_data_series.dropna().shape[0]

        if interpolted_data_series_count < original_data_count:
            logging.warning(f"[WARNING]: Data loss during reindexing: {original_data_count - interpolted_data_series_count} values lost in column '{col_name}'")
       
        # drop original column and replace with the combined series
        df.drop(columns=[col_name], inplace=True)
        df = df.join(interpolated_data_series, how='outer')

        # return the modified data frame
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


    def fill_large_gaps(self, data_series: pd.Series, limit: int) -> pd.Series:
        """ 
        This method is used to find the time gaps whose difference is larger than the limit.
        That is, if the time difference (in seconds) is > limit, the time betwee 2 real values is too long
        and we will not interpolate the values in between. Instead, we will replace the NaN values in large
        time gaps with a dummy value (-9999) to mark them as invalid for interpolation.
        This will leave time gaps <= limit as NaN, and time gaps > limit will be replaced with the dummy value.
        
        Args:
            data_series: pd.Series - The series of data to find gaps in.
            limit: int - The maximum number of seconds between 2 real values that will be interpolated.

        Returns:
            pd.Series : A new series with dummy values in place of long time gaps and with NaNs left in place for small time gaps.
        
        """

        # Create a copy to avoid modifying the input parameter
        data_series = data_series.copy()

        # initialize variables 
        nan_gap_start_index = None                     # holds the index of the first nan in a gap
        next_real_value_index = None                   # holds the index of the next real value after a gap
        i = 0                                          # iterator

        # iterate over the data series
        while i < len(data_series):
            
            # when a NaN is found, mark the start of a NaN gap
            if pd.isna(data_series.iloc[i]):
                
                # holds the position of the first nan in a gap
                nan_gap_start_index = i

                # from the first NaN, continue to iterate until a real value is found
                while i < len(data_series) and pd.isna(data_series.iloc[i]):
                    i = i + 1
                
                # mark the end of a NaN gap (holds a real value)
                next_real_value_index = i

                # this handles the case where the series ends with NaNs
                # and also prevents index out of range errors
                if next_real_value_index >= len(data_series):
                    # Mark all trailing NaNs as dummy values since there's no next real value
                    data_series.iloc[nan_gap_start_index:] = self.DUMMY_VALUE
                    break

                # calculate how many seconds are between the first nan in the gap, and the next real value
                # Ex) a time difference of 18000 seconds, means there are 5 hours of nans in between 2 real values
                time_difference = data_series.index[next_real_value_index] - data_series.index[nan_gap_start_index]
                time_difference_seconds = time_difference.total_seconds()

                # if the time difference is larger than the limit, replace the NaNs in between with the dummy value
                if time_difference_seconds > limit:
                    data_series.iloc[nan_gap_start_index:next_real_value_index] = self.DUMMY_VALUE
                
            else:
                i = i + 1
        # end while loop
        
        # return the modified copy with dummy values in place of large NaN gaps
        return data_series