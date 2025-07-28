# -*- coding: utf-8 -*-
#ImmediateArithmeticOperation.py
#-------------------------------
# Created By : Matthew Kastl, Christian Quintero
#
# Last Updated: 07/27/2025
#-------------------------------
""" The post processing in this file preforms an linear interpolation of a column.
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
            limit: int - The amount of Nan's in a row it will interpolate.

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
        data = df[col_name].copy()

        # Reindex the data to the specific interval we want to interpolate on
        data = data.reindex(date_range(start=data.index[0], end=data.index[-1], freq=timedelta(seconds=interpolation_interval)))

        # Find consecutive NaN streaks and mark those longer than limit
        nan_mask = data.isna()
        
        # Create group labels that change each time we switch between NaN/non-NaN
        group_labels = (nan_mask != nan_mask.shift(1)).cumsum()
        
        # Count consecutive NaNs in each group
        consecutive_nan_counts = nan_mask.groupby(group_labels).transform('sum')
        
        # Identify NaN positions that are part of streaks longer than limit
        long_nan_streak_mask = nan_mask & (consecutive_nan_counts > limit)

        # Perform time-based interpolation on all NaNs
        interpolated_data = data.interpolate(method='time', limit_area='inside')
        
        # Restore NaNs for consecutive streaks that were too long
        interpolated_data.loc[long_nan_streak_mask] = np.nan
   
        # Update the original dataframe
        df = df.drop(columns=[col_name])
        df = df.join(interpolated_data, how='outer')
        
        return df


