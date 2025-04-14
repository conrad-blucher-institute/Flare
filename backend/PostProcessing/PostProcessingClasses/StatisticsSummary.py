# -*- coding: utf-8 -*-
# StatisticsSummary.py
#-------------------------------
# Created By : Anointiyae Beasley
#-------------------------------
"""
This file is a postprocessing class under the IPostProcessing interface.
It calculates the min,max, and median for each column in the DataFrame.

JSON Call :
            {
                "key": "StatisticsSummary",
                "args": {  
                }
            },
"""
#-------------------------------

from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame

class StatisticsSummary(IPostProcessing):
    
    def post_process(self, data: DataFrame) -> DataFrame:
        """Calculates min, max, and median for each row in the DataFrame and adds it to the end of the dataframe.

        Args:
            data (DataFrame): The DataFrame containing 100 lines of data.

        Returns:
            DataFrame: A summary DataFrame with statistics for each column.
        """
        
        temporary_df_numeric = data.drop(columns=['timestamp'])
        
        data["median"] = temporary_df_numeric.median(axis=1)
        data["max"] = temporary_df_numeric.max(axis=1)
        data["min"] = temporary_df_numeric.min(axis=1)
        
        return data