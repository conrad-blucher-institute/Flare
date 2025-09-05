# -*- coding: utf-8 -*-
# RowStatistics.py
# -------------------------------
# Created By : Anointiyae Beasley
# -------------------------------
"""
This file is a postprocessing class under the IPostProcessing interface.
It calculates the min, max, and/or median for each row in the DataFrame containing a list of values.

JSON Call:
    {
        "key": "RowStatistics",
        "args": {
            "metrics": "all"                # OR "median" OR ["min", "max"]
            "col_name": "Name of the column"
        }
    }
"""
# -------------------------------

from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame
from statistics import median  

class RowStatistics(IPostProcessing):

    def post_process(self, data: DataFrame, metrics: str, col_name: str, **kwargs) -> DataFrame:
        """
        Calculates statistics for each model and appends ot the dataframe.

        Args:
            data (DataFrame): The DataFrame with input data. Should include a 'timestamp' column.
            metrics (str or list): One or more of ["min", "max", "median"], or "all".

        Returns:
            DataFrame: Original DataFrame with new columns based on selected statistics.
        """

        
        df = data.copy()
        
        if col_name not in df.columns:
            raise KeyError(f"Column '{col_name}' not found. Available columns: {df.columns.tolist()}")

        # Normalize input
        if isinstance(metrics, str):
            if metrics.lower() == "all":
                metrics = ["min", "max", "median"]
            else:
                metrics = [metrics.lower()]

        # Validate input
        allowed_metrics = {"min", "max", "median"}
        invalid = set(metrics) - allowed_metrics
        if invalid:
            raise ValueError(f"Invalid metric(s): {invalid}. Allowed: {allowed_metrics}")
        
        def is_valid_list(val):
            return isinstance(val, list) and len(val) > 0


        # Add requested statistics
        if "median" in metrics:
            df[f"{col_name} Median"] = df[col_name].apply(lambda x: median(x) if is_valid_list(x) else None)
        if "max" in metrics:
            df[f"{col_name} Max"] = df[col_name].apply(lambda x: max(x) if is_valid_list(x) else None)
        if "min" in metrics:
            df[f"{col_name} Min"] = df[col_name].apply(lambda x: min(x) if is_valid_list(x) else None)

        return df
    
  