# -*- coding: utf-8 -*-
#test_Percentile.py
#-------------------------------
# Created By: Christian Quintero, Jeremiah Sosa
# Last Updated: 06/05/2025
#----------------------------------
"""
This file tests the Percentile PPC by comparing the 5th and 95th
percentile values and tags to the expected values and tags. 
"""
#----------------------------------

import sys
sys.path.append('/app/backend')

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from PostProcessing.IPostProcessing import post_process_factory

# ---------- Mock array of values----------
test_data = [
    [ [11.9, 13.2, 14.2, 15.6, 16.8], ],
    [ [13.5, 14.1, 15.3, 17.7, 18.2], ],
    [ [14.7, 15.3, 16.4, 17.3, 17.7], ],
    [ [15.8, 16.1, 17.3, 17.7, 18.4], ],
    [ [16.8, 17.3, 18.1, 18.3, 19.5], ],
    [ [18.0, 18.3, 19.2, 19.5, 20.4], ],
    [ [19.1, 19.3, 19.4, 20.4, 20.9], ],
    [ [20.0, 21.2, 20.6, 20.9, 21.4], ],
    [ [21.0, 22.3, 22.4, 23.4, 23.5], ],
    [ [21.9, 22.4, 22.5, 23.7, 23.9], ],
]

test_df = pd.DataFrame(test_data, columns=["Temperature Prediction"])
base_df = test_df.copy()

# the 5th percentile for each array in test_data
expected_5th_percentile = [12.16, 13.62, 14.82, 15.86, 16.90, 18.06, 19.14, 20.12, 21.26, 22.00]

# as expected, only the first array value is below the 5th percentile, and 
# all other values are above the 5th percentile.
expected_5th_percentile_tag = [
    ["Below", "Above", "Above", "Above", "Above"],
    ["Below", "Above", "Above", "Above", "Above"],
    ["Below", "Above", "Above", "Above", "Above"],
    ["Below", "Above", "Above", "Above", "Above"],  
    ["Below", "Above", "Above", "Above", "Above"],
    ["Below", "Above", "Above", "Above", "Above"],
    ["Below", "Above", "Above", "Above", "Above"],
    ["Below", "Above", "Above", "Above", "Above"],
    ["Below", "Above", "Above", "Above", "Above"],
    ["Below", "Above", "Above", "Above", "Above"],     
]

# the 95th percentile for each array in test_data
expected_95th_percentile = [16.56, 18.10, 17.62, 18.26, 19.26, 20.22, 20.80, 21.36, 23.48, 23.86]

# as expected, only the largest value in the set is above the 95th percentile
# and all other values are below the 95th percentile
expected_95th_percentile_tag = [
    ["Below", "Below", "Below", "Below", "Above"],
    ["Below", "Below", "Below", "Below", "Above"],
    ["Below", "Below", "Below", "Below", "Above"],
    ["Below", "Below", "Below", "Below", "Above"],
    ["Below", "Below", "Below", "Below", "Above"],
    ["Below", "Below", "Below", "Below", "Above"],
    ["Below", "Below", "Below", "Below", "Above"],
    ["Below", "Below", "Below", "Below", "Above"],
    ["Below", "Below", "Below", "Below", "Above"],
    ["Below", "Below", "Below", "Below", "Above"]
]

# this runs test_percentile_values_and_tags for each list of parameters here.
# in this case, it runs the method to compute the 5th and 95th percentiles and tags
# instead of having to write many methods that do very similar things 
@pytest.mark.parametrize("percentile, expected_values, expected_tags, output_key", [
    (5, expected_5th_percentile, expected_5th_percentile_tag, "5th percentile"),
    (95, expected_95th_percentile, expected_95th_percentile_tag, "95th percentile")
])

# compare the expected to the results
def test_percentile_values_and_tags(percentile, expected_values, expected_tags, output_key):
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
    expected_df[f"{output_key} Value"] = expected_values
    expected_df[f"{output_key} Tag"] = expected_tags

    # ensure that the 2 new columns were made correctly 
    assert f"{output_key} Value" in result_df.columns
    assert f"{output_key} Tag" in result_df.columns

    # compare the result to the expected values
    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True), atol=1e-5)



