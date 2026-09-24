# -*- coding: utf-8 -*-
# ComputeMean.py
#-------------------------------
# Created By: CJ Quintero
# Created On: 09/17/2026
#-------------------------------
"""
This post processing class computes the mean for
each timestamp in a collection of series data.
"""
#-------------------------------
from PostProcessing.IPostProcessing import IPostProcessing
from runtimeContext import thread_storage

from pandas import DataFrame, to_numeric

"""
cspec format:
{
    "_comment": "optional comment about this post processing call",
    "key": "ComputeMean",
    "args": {
        "dropOutlierValues": true,
        "thresholdDeviationFromMedian": 3.5,
        "targetSeries": [
            "series-one_air-temp_25",
            "series-two_air-temp_25",
            "series-three_air-temp_25",
            "series-four_air-temp_25"
        ],
        "outKey": "combined-air-temp"
    }
}
"""
class ComputeMean(IPostProcessing):
    def __init__(self):
        self.logger = thread_storage.logger

    def post_process(
            self, 
            data: DataFrame,
            targetSeries: list[str],
            outKey: str,
            dropOutlierValues: bool = False,
            thresholdDeviationFromMedian: float = None
        ) -> DataFrame:
        """
        Computes the mean for each timestamp in a collection of series data and
        appends the new series to the dataframe.

        Args:
            data (DataFrame): The dataframe containing the collection of series data
            targetSeries (list[str]): A list of input series column names to compute the mean from
            outKey (str): The output column name for the computed mean series
            dropOutlierValues (bool): Optional. If true, outlier values will be dropped from the target series before computing the mean.
            thresholdDeviationFromMedian (float): Optional, required if dropOutlierValues is true. 
                Values that are >= threshold from the median are considered outliers and will be dropped from the mean calculation.
        
        Returns:
            DataFrame: The dataframe with the new computed mean series appended
        """

        # validate cspec args
        # on bad arguments, log the error message and return the df with an empty post processing column
        is_valid_args = self._validate_args(data, targetSeries, outKey, dropOutlierValues, thresholdDeviationFromMedian)
        if not is_valid_args:
            data[outKey] = None
            return data

        # extract the target series from the df and convert to numeric
        available_series = [key for key in targetSeries if key in data.columns]
        values_df = data[available_series].apply(to_numeric, errors='coerce')

        # add the new mean series to the dataframe
        data[outKey] = values_df.apply(
            self._compute_mean,
            axis=1,
            dropOutlierValues=dropOutlierValues,
            threshold=thresholdDeviationFromMedian
        )

        return data


    def _validate_args(
            self,
            df: DataFrame,
            targetSeries: list[str],
            outKey: str,
            dropOutlierValues: bool = False,
            thresholdDeviationFromMedian: float = None
        ) -> bool:
        """
        Validates the arguments passed to the post process method by checking
        for cspec errors and missing data in the dataframe that is required for computing the mean.

        Args:
            df (DataFrame): The dataframe containing the collection of series data
            targetSeries (list[str]): A list of input series column names to compute the mean from
            outKey (str): The output column name for the computed mean series
            dropOutlierValues (bool): Optional. If true, outlier values will be dropped from the target series before computing the mean.
            thresholdDeviationFromMedian (float): Optional, required if dropOutlierValues is true. 
                Values that are >= threshold from the median are considered outliers and will be dropped from the mean calculation.
        
        Returns:
            bool - True if the arguments are valid, False otherwise. If invalid, logs a warning message and returns False.
        """

        # this is a special case since on bad arguments, we would return the df
        # with the new column set to all None, but without the outKey we cannot do that
        if outKey is None or outKey.strip() == "":
            msg = "ComputeMean Error: 'outKey' key is missing or empty in cspec args."
            raise KeyError(msg)

        if targetSeries is None or len(targetSeries) == 0:
            msg = "ComputeMean Warning: 'targetSeries' key is missing or empty in cspec args. No mean will be computed."
            self.logger.log_info(msg)
            return False

        # if a key is missing from the columns, we can still try to compute the mean for the available series.
        for key in targetSeries:
            if key not in df.columns:
                msg = f"ComputeMean Warning: Target series '{key}' not found in dataframe columns."
                self.logger.log_info(msg)

        # if all keys are missing from the df, no mean can be computed
        found_keys = [key for key in targetSeries if key in df.columns]
        if len(found_keys) == 0:
            msg = "ComputeMean Warning: No valid target series found in dataframe columns. No mean will be computed."
            self.logger.log_info(msg)
            return False

        if dropOutlierValues and thresholdDeviationFromMedian is None:
            msg = "ComputeMean Warning: 'thresholdDeviationFromMedian' key is missing in cspec args. No mean will be computed."
            self.logger.log_info(msg)
            return False

        if dropOutlierValues and thresholdDeviationFromMedian <= 0:
            msg = "ComputeMean Warning: 'thresholdDeviationFromMedian' key must be greater than 0 in cspec args. No mean will be computed."
            self.logger.log_info(msg)
            return False

        return True


    def _compute_mean(self, row, dropOutlierValues: bool = False, threshold: float = None) -> float | None:
        """
        computes the mean for a given row of data for the target series.
        If dropOutlierValues is true, outlier values will be dropped from the target series before computing the mean.

        Args:
            row (Series): A row of data from the dataframe with the target series values for a specific timestamp
            dropOutlierValues (bool): Optional. If true, outlier values will be dropped from the target series before computing the mean.
            threshold (float): Optional, required if dropOutlierValues is true. 
                Values that are >= threshold from the median are considered outliers and will be dropped from the mean calculation.
        
        Returns:
            float | None: The computed mean value for the row, or None if there are no valid values to compute the mean from.
        """
        valid_values = row.dropna()

        if valid_values.empty:
            return None

        if dropOutlierValues:
            median_value = valid_values.median()
            deviation_from_median = (valid_values - median_value).abs()
 
            # keep only values within the threshold; values at or above it are outliers
            valid_values = valid_values[deviation_from_median < threshold]
 
            if valid_values.empty:
                return None
 
        return valid_values.mean()
