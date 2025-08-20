# -*- coding: utf-8 -*-
# test_AddMostRecentMeasurement.py
# -------------------------------
# Created By : Anointiyae Beasley
# -------------------------------
""" 
Unit tests for the AddMostRecentMeasurement class using pytest.
"""

import pytest
from pandas import DataFrame, to_datetime
from PostProcessing.IPostProcessing import post_process_factory
from datetime import datetime, timedelta
from numpy import nan
#I need to pass botht he measurement and prediction column key and then add the measurment closest to now time to the beginning of the prediction column so that the lines meet.
# Generate a list of dates starting two days before today
# Get today's date
today = datetime.now()

# Calculate the starting date (2 days before today)
start_date = today - timedelta(days=2)

# Generate a list of 4 dates
dates = []
for i in range(5):
    dates.append((start_date + timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S'))
    
# Define the test DataFrame
test_df = DataFrame({
    'measurement': [1.0, 2.0, 2.5, nan, nan],
    'prediction': [nan, nan, nan, 2.2, 2.6],
    'Date': dates
}).set_index('Date')  # Set Date as the index


@pytest.mark.parametrize("test_df, measurement_key, prediction_key, expected_results", [
    (
        test_df.copy(),
        'measurement',
        'prediction',
        DataFrame({
            'measurement': [1.0, 2.0, 2.5, nan, nan],
            'prediction': [nan, nan, 2.5, 2.2, 2.6],
            'Date': dates 
        }).set_index('Date')  # Set Date as the index
    )
])
def test_post_process(test_df: DataFrame, measurement_key: str, prediction_key: str, expected_results: DataFrame):
    """Tests the post_process method in AddMostRecentMeasurement class."""
    
    
    kwargs = {
    'measurement_col_key': measurement_key,
    'prediction_col_key': prediction_key
}
    
    
    result = post_process_factory(test_df,'AddMostRecentMeasurement', kwargs)
    

    # Display the updated DataFrame
    print(f'Data: {result}')
    
    # Reset index for comparison
    result.reset_index(drop=True, inplace=True)
    expected_results.reset_index(drop=True, inplace=True)

    # Assert that the result matches the expected DataFrame
    assert result.equals(expected_results), "The post_process method did not produce the expected result."