# -*- coding: utf-8 -*-
#test_Percentile.py
#-------------------------------
# Created By: Christian Quintero, Jeremiah Sosa
# Last Updated: 06/08/2025
#----------------------------------
"""
This file tests the Percentile PPC by comparing computed
percentile values to the expected values.
"""
#----------------------------------

import sys
sys.path.append('/app/backend')

import pytest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
from PostProcessing.IPostProcessing import post_process_factory

# ---------- Mock array of values----------
# 3 normal rows
# ------------------------------------------
test_data = [
    [ [11.9, 13.2, 14.2, 15.6, 16.8], ],
    [ [13.5, 14.1, 15.3, 17.7, 18.2], ],
    [ [14.7, 15.3, 16.4, 17.3, 17.7], ]
]

test_df = pd.DataFrame(test_data, columns=["Temperature Prediction"])
base_df = test_df.copy()

# the 0th percentile value for each array in test_data
# which is the MINIMUM value in each array
expected_0th_percentiles = [11.9, 13.5, 14.7]

# the 5th percentile value for each array in test_data
# this value is interpolated from the data
expected_5th_percentiles = [12.16, 13.62, 14.82]

# the 25th percentile value for each array in test_data
# this is the median of the lower half of the data
expected_25th_percentiles = [13.2, 14.1, 15.3]

# the 50th percentile value for each array in test_data
# which is the MEDIAN value in each array
expected_50th_percentiles = [14.2, 15.3, 16.4]

# the 75th percentile value for each array in test_data
# this is the median of the upper half of the data
expected_75th_percentiles = [15.6, 17.7, 17.3]

# the 95th percentile value for each array in test_data
# this value is interpolated from the data
expected_95th_percentiles = [16.56, 18.10, 17.62]

# the 100th percentile value for each array in test_data
# which is the MAXIMUM value in each array
expected_100th_percentiles = [16.8, 18.2, 17.7]

# this runs test_percentile_values for each list of parameters here
@pytest.mark.parametrize("percentile, expected_percentile_values, output_key", [
    (0, expected_0th_percentiles, "0th percentile"),
    (5, expected_5th_percentiles,"5th percentile"),
    (25, expected_25th_percentiles, "25th percentile"),
    (50, expected_50th_percentiles, "50th percentile"),
    (75, expected_75th_percentiles, "75th percentile"),
    (95, expected_95th_percentiles, "95th percentile"),
    (100, expected_100th_percentiles, "100th percentile")
])

# compare the expected to the results
def test_percentile_values(percentile, expected_percentile_values, output_key):
    """
    This function tests normal percentile values within the range of 0-100.
    It checks that the computed percentile values match the expected values
    """

    # assigns the call type and the arguments for the Percentile PPC
    # this is the call that will be made to the post_process_factory
    call = "Percentile"
    kwargs = {
        "col_key": "Temperature Prediction",
        "percentile": percentile,
        "output_col_key": output_key 
    }

    # call the Percentile PPC method using the factory
    result_df = post_process_factory(test_df.copy(), call, kwargs)

    # assign the expected values to the expected data frame
    expected_df = base_df.copy()
    expected_df[f"{output_key} Value"] = expected_percentile_values

    # ensure that the new column was made correctly 
    assert f"{output_key} Value" in result_df.columns

    # compare the result to the expected value
    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True), atol=1e-5)


# ------------------------------------------
# this runs test_invalid_percentile_bounds to check the bounds 
# of the percentile values
# ------------------------------------------
@pytest.mark.parametrize("percentile", [-1, 101])

def test_invalid_percentile_bounds(percentile):
    """
    This function tests invalid percentile values outside the range of 0-100.
    It checks that a ValueError is raised for invalid percentiles.
    """
    call = "Percentile"
    kwargs = {
        "col_key": "Temperature Prediction",
        "percentile": percentile,
        "output_col_key": "Invalid Percentile Bounds"
    }

    with pytest.raises(ValueError, match=f"Percentile '{percentile}' is not in a valid range. Must be between 0 and 100."):
        post_process_factory(test_df.copy(), call, kwargs)


# ------------------------------------------
# this runs test_invalid_percentile_type to check the type of the percentile value
# ------------------------------------------
@pytest.mark.parametrize("percentile", ["Hello World", None, np.nan])

def test_invalid_percentile_type(percentile):
    """
    This function tests invalid percentile types that are not integers.
    It checks that a ValueError is raised for invalid percentile types.
    """
    call = "Percentile"
    kwargs = {
        "col_key": "Temperature Prediction",
        "percentile": percentile,
        "output_col_key": "Invalid Percentile Type"
    }

    with pytest.raises(ValueError, match=f"Percentile '{percentile}' must be an integer."):
        post_process_factory(test_df.copy(), call, kwargs)
