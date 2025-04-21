# -*- coding: utf-8 -*-
# test_RowStatistics.py
# -------------------------------
# Created By: Anointiyae Beasley
# -------------------------------
"""This file tests the RowStatistics post-processing class.
"""
# -------------------------------

import sys
sys.path.append('/app/backend')

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from PostProcessing.IPostProcessing import post_process_factory
from io import StringIO

# Sample CSV with 'Date'
csv_data = """Date,member 1,member 2,member 3,member 4,member 5,member 6,member 7,member 8,member 9,member 10
2025-04-09 00:00,12.4,13.1,11.9,12.8,13.0,14.2,12.5,13.3,12.9,14.1
2025-04-09 01:00,14.2,13.8,14.0,13.5,14.1,15.3,14.1,14.9,13.8,15.2
2025-04-09 02:00,15.0,15.3,14.7,15.2,15.4,16.4,15.8,15.7,15.1,16.1
2025-04-09 03:00,16.1,16.0,15.8,15.9,16.3,17.2,16.5,16.8,16.2,17.3
2025-04-09 04:00,17.0,17.2,16.8,17.1,16.9,18.0,17.3,17.4,17.0,18.1
2025-04-09 05:00,18.5,18.3,18.0,18.4,18.2,19.1,18.6,18.5,18.3,19.2
2025-04-09 06:00,19.4,19.6,19.3,19.1,19.5,20.3,19.8,19.6,19.7,20.0
2025-04-09 07:00,20.0,20.2,20.1,20.3,20.4,21.0,20.6,20.8,20.9,21.2
2025-04-09 08:00,21.1,21.3,21.0,21.4,21.2,22.1,21.7,21.9,21.8,22.3
2025-04-09 09:00,22.0,22.2,21.9,22.1,22.3,23.2,22.8,22.6,22.7,23.4"""

# Load and prepare input
test_df = pd.read_csv(StringIO(csv_data))
test_df['Date'] = pd.to_datetime(test_df['Date'])
base_df = test_df.copy()

# Reference stats
expected_median = [12.95, 14.10, 15.35, 16.25, 17.15, 18.45, 19.60, 20.50, 21.55, 22.45]
expected_max    = [14.20, 15.30, 16.40, 17.30, 18.10, 19.20, 20.30, 21.20, 22.30, 23.40]
expected_min    = [11.90, 13.50, 14.70, 15.80, 16.80, 18.00, 19.10, 20.00, 21.00, 21.90]

# ---------- ALL METRICS ----------
def test_row_statistics_all_metrics():
    call = "RowStatistics"
    kwargs = { "metrics": "all" }

    result_df = post_process_factory(test_df.copy(), call, kwargs)

    expected_stats = pd.DataFrame({
        "median": expected_median,
        "max": expected_max,
        "min": expected_min
    })

    expected_df = pd.concat([test_df.reset_index(drop=True), expected_stats], axis=1)
    assert_frame_equal(result_df.reset_index(drop=True), expected_df, atol=1e-5)

# ---------- MEDIAN ONLY ----------
def test_row_statistics_median_only():
    call = "RowStatistics"
    kwargs = { "metrics": "median" }

    result_df = post_process_factory(base_df.copy(), call, kwargs)

    expected_df = base_df.copy()
    expected_df["median"] = expected_median

    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True), atol=1e-5)

# ---------- MAX ONLY ----------
def test_row_statistics_max_only():
    call = "RowStatistics"
    kwargs = { "metrics": "max" }

    result_df = post_process_factory(base_df.copy(), call, kwargs)

    expected_df = base_df.copy()
    expected_df["max"] = expected_max

    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True), atol=1e-5)

# ---------- MIN ONLY ----------
def test_row_statistics_min_only():
    call = "RowStatistics"
    kwargs = { "metrics": "min" }

    result_df = post_process_factory(base_df.copy(), call, kwargs)

    expected_df = base_df.copy()
    expected_df["min"] = expected_min

    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True), atol=1e-5)

# ---------- MULTIPLES ----------
def test_row_statistics_min_and_max_only():
    call = "RowStatistics"
    kwargs = { "metrics": ["min", "max"] }

    result_df = post_process_factory(base_df.copy(), call, kwargs)

    expected_df = base_df.copy()
    expected_df["min"] = expected_min
    expected_df["max"] = expected_max

    assert_frame_equal(result_df.sort_index(axis=1).reset_index(drop=True),expected_df.sort_index(axis=1).reset_index(drop=True),atol=1e-5)