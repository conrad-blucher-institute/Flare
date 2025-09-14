# -*- coding: utf-8 -*-
# test_RowStatistics.py
# -------------------------------
# Created By: Anointiyae Beasley
# -------------------------------
"""This file tests the RowStatistics post-processing class for list-in-cell values."""
# -------------------------------


import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from PostProcessing.IPostProcessing import post_process_factory
from io import StringIO
from datetime import datetime

# ---------- Mock array of values----------
test_data = [
    [ [11.9, 13.2, 14.2], ],
    [ [13.5, 14.1, 15.3], ],
    [ [14.7, 15.3, 16.4], ],
    [ [15.8, 16.1, 17.3], ],
    [ [16.8, 17.3, 18.1], ],
    [ [18.0, 18.3, 19.2], ],
    [ [19.1, 20.3, 19.4], ],
    [ [20.0, 21.2, 20.6], ],
    [ [21.0, 22.3, 21.4], ],
    [ [21.9, 23.4, 22.5], ],
]

test_df = pd.DataFrame(test_data, columns=["Water Temperature Prediction"])
base_df = test_df.copy()

# Expected statistics
expected_median = [13.2, 14.10, 15.3, 16.1, 17.3, 18.3, 19.4, 20.6, 21.4, 22.5]
expected_max    = [14.20, 15.30, 16.40, 17.30, 18.10, 19.20, 20.30, 21.20, 22.30, 23.40]
expected_min    = [11.90, 13.50, 14.70, 15.80, 16.80, 18.00, 19.10, 20.00, 21.00, 21.90]
reference_time = datetime.now()
# ---------- ALL METRICS ----------
def test_row_statistics_all_metrics():
    call = "RowStatistics"
    kwargs = {
        "metrics": "all",
        "col_name": "Water Temperature Prediction"
    }
    

    result_df = post_process_factory(test_df.copy(), call, kwargs)

    expected_stats = pd.DataFrame({
        "Water Temperature Prediction Median": expected_median,
        "Water Temperature Prediction Max": expected_max,
        "Water Temperature Prediction Min": expected_min
    })

    expected_df = pd.concat([test_df.reset_index(drop=True), expected_stats], axis=1)
    assert_frame_equal(result_df.reset_index(drop=True), expected_df, atol=1e-5)

# ---------- MEDIAN ONLY ----------
def test_row_statistics_median_only():
    call = "RowStatistics"
    kwargs = {
        "metrics": "median",
        "col_name": "Water Temperature Prediction"
    }

    result_df = post_process_factory(base_df.copy(),call, kwargs)

    expected_df = base_df.copy()
    expected_df["Water Temperature Prediction Median"] = expected_median

    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True), atol=1e-5)

# ---------- MAX ONLY ----------
def test_row_statistics_max_only():
    call = "RowStatistics"
    kwargs = {
        "metrics": "max",
        "col_name": "Water Temperature Prediction"
    }

    result_df = post_process_factory(base_df.copy(),call, kwargs)

    expected_df = base_df.copy()
    expected_df["Water Temperature Prediction Max"] = expected_max

    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True), atol=1e-5)

# ---------- MIN ONLY ----------
def test_row_statistics_min_only():
    call = "RowStatistics"
    kwargs = {
        "metrics": "min",
        "col_name": "Water Temperature Prediction"
    }

    result_df = post_process_factory(base_df.copy(),call, kwargs)

    expected_df = base_df.copy()
    expected_df["Water Temperature Prediction Min"] = expected_min

    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True), atol=1e-5)

# ---------- MULTIPLES ----------
def test_row_statistics_min_and_max_only():
    call = "RowStatistics"
    kwargs = {
        "metrics": ["min", "max"],
        "col_name": "Water Temperature Prediction"
    }

    result_df = post_process_factory(base_df.copy(),call, kwargs)

    expected_df = base_df.copy()
    expected_df["Water Temperature Prediction Min"] = expected_min
    expected_df["Water Temperature Prediction Max"] = expected_max

    assert_frame_equal(result_df.sort_index(axis=1).reset_index(drop=True),
                       expected_df.sort_index(axis=1).reset_index(drop=True), atol=1e-5)
