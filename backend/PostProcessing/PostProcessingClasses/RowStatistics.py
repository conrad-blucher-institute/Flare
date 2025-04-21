# -*- coding: utf-8 -*-
# RowStatistics.py
# -------------------------------
# Created By : Anointiyae Beasley
# -------------------------------
"""
This file is a postprocessing class under the IPostProcessing interface.
It calculates the min, max, and/or median for each row in the DataFrame depending on user input.

JSON Call:
    {
        "key": "RowStatistics",
        "args": {
            "metrics": "all"                # OR "median" OR ["min", "max"]
        }
    }
"""
# -------------------------------

from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame

class RowStatistics(IPostProcessing):

    def post_process(self, data: DataFrame, metrics: str, **kwargs) -> DataFrame:
        """
        Calculates row-wise statistics (min, max, median) and appends them to the DataFrame.

        Args:
            data (DataFrame): The DataFrame with input data. Should include a 'timestamp' column.
            metrics (str or list): One or more of ["min", "max", "median"], or "all".

        Returns:
            DataFrame: Original DataFrame with new columns based on selected statistics.
        """
        # Drop non-numeric columns like timestamp
        numeric_df = data.drop(columns=['Date'])

        # Normalize input
        if isinstance(metrics, str):
            if metrics.lower() == "all":
                metrics = ["min", "max", "median"]
            else:
                metrics = [metrics]

        # Validate input
        allowed_metrics = {"min", "max", "median"}
        invalid = set(metrics) - allowed_metrics
        if invalid:
            raise ValueError(f"Invalid metric(s): {invalid}. Allowed: {allowed_metrics}")

        # Add requested statistics
        if "median" in metrics:
            data["median"] = numeric_df.median(axis=1)
        if "max" in metrics:
            data["max"] = numeric_df.max(axis=1)
        if "min" in metrics:
            data["min"] = numeric_df.min(axis=1)

        return data
