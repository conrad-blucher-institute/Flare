# -*- coding: utf-8 -*-
#LinearInterpolation.py
#-------------------------------
# Created By : Matthew Kastl
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
        data = df[col_name]

        # The index of the data frame isn't necessarily the correct for the values we want to interpolate for this series. Thus we reindex
        # the data to the specific interval we want to interpolate on.
        data = data.reindex(date_range(start=data.index[0], end=data.index[-1], freq=timedelta(seconds=interpolation_interval)))

        # We want to not interpolate if there are too many Nans in a row. However the pandas limit parameter only stops interpolation once its
        # counted a cumulative sum of Nans higher than limit. Thus it keeps the Nans in that group where the cumulative sum was still < limit.
        # The forwards cumulative mask looks for where this mistake will happen thus used to overwrite the interpolated values with Nan.
        nan_mask = data.isna()
        cumulative_nan_streaks = nan_mask.groupby(~nan_mask).cumsum()
        forward_cumulative_nan_mask = cumulative_nan_streaks.gt(limit)

        # We do the interpolation backwards because a forwards cumulative mask was easier to write than a backwards one.
        backwards_interpolation = data.interpolate(method= 'time', limit= limit, limit_area= 'inside', limit_direction= 'backward')
        
        # Here we repair the mistake by looking at the forward cumulative mask and inserting Nan.
        backwards_interpolation[forward_cumulative_nan_mask] = np.nan
   
        # Outer join to preserve all data in the dataframe.
        df.drop(columns=[col_name], inplace=True)
        df = df.join(backwards_interpolation, how='outer')
        return df


