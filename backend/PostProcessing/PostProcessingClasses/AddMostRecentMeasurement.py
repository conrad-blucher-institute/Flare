# -*- coding: utf-8 -*-
# AddMostRecentMeasurement.py
# -------------------------------
# Created By : Anointiyae Beasley
# -------------------------------
""" 
The post-processing in this file adds the most recent measurement to the prediction column for the same date.
"""
# -------------------------------
#
#
# Imports
from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame, isna
from datetime import datetime

class AddMostRecentMeasurement(IPostProcessing):
    
    def post_process(self, data: DataFrame, measurement_col_key: str, prediction_col_key: str) -> DataFrame:
        """
        Replaces the prediction value with the most recent measurement for the same date, 
        ensuring only one update is made.

        Args:
            data (DataFrame): The DataFrame containing the measurement, prediction, and date columns.
            measurement_col_key (str): The key for the measurement column.
            prediction_col_key (str): The key for the prediction column.
            date_col_key (str): The key for the date column.

        Returns:
            DataFrame: A DataFrame with the prediction updated for the closest measurement to now.
        """
        
        # Isolate the relevant series
        s_measurement = data[measurement_col_key]
        s_prediction = data[prediction_col_key]
        s_date = data["Date"]
        # Get the current date
        now = datetime.now()

        # Find the row with the closest date to now and a non-NaN measurement
        closest_index = None
        closest_time_diff = None
        for i in range(len(data)):
            if not isna(s_measurement.iloc[i]):  # Only consider rows with valid measurements
                row_date = datetime.strptime(s_date.iloc[i], '%Y-%m-%d')  # Convert date string to datetime
                time_diff = abs((row_date - now).total_seconds())  # Calculate time difference in seconds
                
                if closest_time_diff is None or time_diff < closest_time_diff:
                    closest_time_diff = time_diff
                    closest_index = i

        # Update the prediction for the closest row
        if closest_index is not None:
            s_prediction.iloc[closest_index] = s_measurement.iloc[closest_index]

        # Update the DataFrame with the modified prediction column
        data[prediction_col_key] = s_prediction

        return data
