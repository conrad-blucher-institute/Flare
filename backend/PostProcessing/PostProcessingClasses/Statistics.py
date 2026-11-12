"""
Statistics.py

This post processing class calculates statistics for each row of a column,
where every row holds a list of values, and appends them to the ongoing dataframe.

NOTE: NaNs in the row's list are ignored when calculating statistics.

Created by: CJ Quintero
Created on: 11/09/2026
"""
import numpy as np
from PostProcessing.IPostProcessing import IPostProcessing
from runtimeContext import thread_storage
from pandas import DataFrame, Series, to_numeric

"""
Post Processing call:
{
    "key": "Statistics",
    "args": {
        "column_name": "Air Temperature Predictions",
        "percentiles": [0, 5, 25, 50, 75, 95, 100],
        "statistics": ["min", "max", "mean", "median"]
    }
}
"""

class Statistics(IPostProcessing):
    """
    Statistics Post Processing Class:
    computes statistics for a specific column across each row
    """

    def __init__(self):
        self.logger = thread_storage.logger

    def post_process(
            self, 
            df: DataFrame,
            column_name: str,
            statistics: list[str] | None = None,
            percentiles: list[int] | None = None
        ) -> DataFrame:
        """
        performs the post process on the specified column of the dataframe

        Args:
            df (DataFrame) - the dataframe to post process

            column_name (str) - the name of the column to calculate statistics for.
                Each row must hold a list of numbers; statistics are computed
                across each row's list, giving one value per row.
            
            statistics (list[str] | None) - the statistics to calculate.
                Can be any of the following as a list of strings,
                or defaults to None if not requested/provided:
                ["min", "max", "mean", "median", "std", "var"]

            percentiles (list[int]) - the percentiles to calculate
                as a list of integers, or defaults to the None if not provided.
                percentiles must be between 0 <= p <= 100.
        
        Returns:
            DataFrame - the dataframe with the calculated statistics appended
        """
        if column_name not in df.columns:
            self.logger.log_error(f"Column '{column_name}' not found in dataframe")
            return df

        if percentiles is None and statistics is None:
            self.logger.log_error('No statistics or percentiles requested')
            return df

        # ensure every row in the column is numeric and coerce invalid values to NaN
        column = df[column_name].apply(to_numeric, errors='coerce')

        result_df = DataFrame(index=column.index)
        if percentiles:
            result_df = result_df.join(self._compute_percentiles(column, percentiles), how='outer')
        if statistics:
            result_df = result_df.join(self._compute_statistics(column, statistics), how='outer')

        return df.join(result_df, how='outer')


    def _compute_statistics(self, column: Series, statistics: list[str]) -> DataFrame:
        """
        computes the requested statistics for each row in the specified column

        Args:
            column (Series) - the column to calculate statistics for
            statistics (list[str]) - the statistics to calculate

        Returns:
            DataFrame - a dataframe containing the requested statistics

        NOTE: The np functions ignore NaNs in their computations and
        some functions will raise errors if an empty list [] is provided.
        To guard against this, if the row is all NaNs or an empty list,
        the result is set to a single NaN.
        """
        result = {}
        for stat in statistics:
            match stat:
                case "min":
                    result[f'{column.name} min'] = column.apply(
                        lambda row: np.nan if np.isnan(row).all() else np.nanmin(row)
                    )
                case "max":
                    result[f'{column.name} max'] = column.apply(
                        lambda row: np.nan if np.isnan(row).all() else np.nanmax(row)
                    )
                case "mean":
                    result[f'{column.name} mean'] = column.apply(
                        lambda row: np.nan if np.isnan(row).all() else np.nanmean(row)
                    )
                case "median":
                    result[f'{column.name} median'] = column.apply(
                        lambda row: np.nan if np.isnan(row).all() else np.nanmedian(row)
                    )
                case "std":
                    # standard deviation
                    result[f'{column.name} std'] = column.apply(
                        lambda row: np.nan if np.isnan(row).all() else np.nanstd(row)
                    )
                case "var":
                    # variance
                    result[f'{column.name} var'] = column.apply(
                        lambda row: np.nan if np.isnan(row).all() else np.nanvar(row)
                    )
                case _:
                    self.logger.log_error(f'Invalid statistic: {stat}')
        
        # the index from the column is the same as the ongoing df's index
        return DataFrame(result, index=column.index)


    def _compute_percentiles(self, column: Series, percentiles: list[int]) -> DataFrame:
        """
        computes the requested percentiles for each row in the specified column

        Args:
            column (Series) - the column to calculate percentiles for
            percentiles (list[int]) - the percentiles to calculate

        Returns:
            DataFrame - a dataframe containing the requested percentiles
        
        NOTE: This formats the computed percentiles as '<column name> p<percentile>',
        such as 'air temp p50'

        NOTE: The np functions ignore NaNs in their computations and
        some functions will raise errors if an empty list [] is provided.
        To guard against this, if the row is all NaNs or an empty list,
        the result is set to a single NaN.
        """

        valid_percentiles = []
        for p in percentiles:
            if 0 <= p <= 100:
                valid_percentiles.append(p)
            else:
                self.logger.log_error(f'Invalid percentile: {p}')

        result = {}
        for percentile in valid_percentiles:
            result[f'{column.name} p{percentile}'] = column.apply(
                lambda row: np.nan if np.isnan(row).all() else np.nanpercentile(row, percentile)
            )

        return DataFrame(result, index=column.index)
