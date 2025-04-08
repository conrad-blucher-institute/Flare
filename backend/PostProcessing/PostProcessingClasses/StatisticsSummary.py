# -*- coding: utf-8 -*-
# StatisticsSummary.py
#-------------------------------
# Created By : Anointiyae Beasley
#-------------------------------
"""
This file is a postprocessing class under the IPostProcessing interface.
It calculates the median, max, and mean for each column in the DataFrame.
"""
#-------------------------------

from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame

class StatisticsSummary(IPostProcessing):
    
    def post_process(self, data: DataFrame, *args, **kwargs) -> DataFrame:
        """Calculates median, max, and mean for each column in the DataFrame.

        Args:
            data (DataFrame): The DataFrame containing 100 lines of data.

        Returns:
            DataFrame: A summary DataFrame with statistics for each column.
        """
        summary = DataFrame({
            "median": data.median(),
            "max": data.max(),
            "mean": data.mean()
        })

        return summary
