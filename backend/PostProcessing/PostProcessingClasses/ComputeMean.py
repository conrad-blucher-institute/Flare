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
        "targetSeries": [
            "series-one_air-temp_25",
            "series-two_air-temp_25",
            "series-three_air-temp_25",
            "series-four_air-temp_25"
        ],
        "outKey": "combined-air-temp"
    }
}

targetSeries (list[str]) - A list of input series column names to compute the mean from.
    The order of the list does not matter.
outKey (str) - The output column name for the computed mean series. This computed column
    is appended to the dataframe.

"""
class ComputeMean(IPostProcessing):
    def __init__(self):
        self.logger = thread_storage.logger

    def post_process(self, data: DataFrame, args) -> DataFrame:
        """
        Computes the mean for each timestamp in a collection of series data and
        appends the new series to the dataframe.

        Args:
            data (DataFrame): The dataframe containing the collection of series data
            args (dict): A dictionary containing the target series and output key.
                {
                    "targetSeries": [
                        "series-one_air-temp_25",
                        "series-two_air-temp_25",
                        "series-three_air-temp_25",
                        "series-four_air-temp_25"
                    ],
                    "outKey": "combined-air-temp"
                }
        
        Returns:
            DataFrame: The dataframe with the new computed mean series appended.
        """

        # validate cspec args
        # on bad arguments, log the error message and return the original dataframe
        is_valid_args = self._validate_args(data, args)
        if not is_valid_args:
            return data

        targetSeries = args["targetSeries"]
        outKey = args["outKey"]

        # compute the mean for each timestamp across the target series and append to the dataframe
        # values that fail to be casted to numeric are coerced to NaN and ignored in the mean calculation
        # and does not cause any side effects to the input columns
        data[outKey] = data[targetSeries].apply(to_numeric, errors='coerce').mean(axis=1)

        return data


    def _validate_args(self, df: DataFrame, args: dict) -> bool:
        """
        Validates the arguments passed to the post process method by checking
        for cspec errors.

        Args:
            df (DataFrame): The dataframe containing the collection of series data
            args (dict): A dictionary containing the target series and output key.
                {
                    "targetSeries": [
                        "series-one_air-temp_25",
                        "series-two_air-temp_25",
                        "series-three_air-temp_25",
                        "series-four_air-temp_25"
                    ],
                    "outKey": "combined-air-temp"
                }
        
        Returns:
            bool - True if the arguments are valid, False otherwise. If invalid, logs a warning message and returns False.
        """
        targetSeries = args.get("targetSeries", None)
        outKey = args.get("outKey", None)

        if targetSeries is None or len(targetSeries) == 0:
            msg = "ComputeMean Warning: 'targetSeries' key is missing or empty in cspec args. No mean will be computed."
            self.logger.log_info(msg)
            return False

        if outKey is None or outKey.strip() == "":
            msg = "ComputeMean Warning: 'outKey' key is missing or empty in cspec args. No mean will be computed."
            self.logger.log_info(msg)
            return False

        for key in targetSeries:
            if key not in df.columns:
                msg = f"ComputeMean Warning: Target series '{key}' not found in dataframe columns. No mean will be computed."
                self.logger.log_info(msg)
                return False

        return True
