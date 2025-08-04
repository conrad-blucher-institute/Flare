# -*- coding: utf-8 -*-
# LinearInterpolation.py
#-------------------------------
# Created By: Christian Quintero
# Last Updated: 08/04/2025
#-------------------------------
""" The post processing in this file performs a linear interpolation of a column.
 """ 
#-------------------------------
# 
#
#Imports
from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame, date_range
import numpy as np
from datetime import timedelta

class LinearInterpolation(IPostProcessing):


    def post_process(self, df: DataFrame, col_name: str, interpolation_interval: int, limit: int) -> DataFrame:
        """The post processing in this file preforms an linear interpolation of a column.

        Args:
            df DataFrame: The DataFrame containing this collation of the data that has been collected.
            col_name: str - The column in the DataFrame to interpolate.
            interpolation_interval: int - The interval to interpolate data on, in seconds.
            limit: int - The amount of Nan's consecutive NaNs in a row to interpolate.

        Returns:
            DataFrame : A new dataframe obj might have to be created, this will always be a reference to the most updated version.

        NOTE::This function actually uses time based interpolation which is the same as linear interpolation.

        JSON Call:
        {
            "key": "LinearInterpolation",
            "args": {
                "col_name": "",
                "interpolation_interval": -1,
                "limit: -1
            }
        },
        """

        # Isolate the data we are going to interpolate
        data = df[col_name]

        # The index of the data frame isn't necessarily the correct for the values we want to interpolate for this series. Thus we reindex
        # the data to the specific interval we want to interpolate on.
        data = data.reindex(date_range(start=data.index[0], end=data.index[-1], freq=timedelta(seconds=interpolation_interval)))

        # We want to 'mask' the data so that each value gets assigned TRUE if NaN and FALSE if it is a real value.
        nan_mask = data.isna()

        # Create unique group IDs for consecutive NaN streaks.
        group_ids = (~nan_mask).cumsum()

        # Count the length of each NaN streak
        # For each group ID, count how many NaN values (True values in nan_mask) are in that group
        streak_lengths = nan_mask.groupby(group_ids).transform('sum')   

        # Create a mask for NaN streaks longer than the limit
        # We only want to mark actual NaN positions that are in long streaks
        long_streak_mask = (streak_lengths > limit) & nan_mask

        # Interpolate all NaN values using time-based interpolation, which is the same as linear interpolation
        interpolated_data = data.interpolate(method='time', limit_area='inside')

        # Put NaNs back where streaks were too long
        # aka where the NaN streaks > limit
        interpolated_data[long_streak_mask] = np.nan

        # Replace the original column with our processed data
        df.drop(columns=[col_name], inplace=True)
        df = df.join(interpolated_data, how='outer')
        return df

