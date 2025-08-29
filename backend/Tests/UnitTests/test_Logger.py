# -*- coding: utf-8 -*-
#test_Logger.py
#-------------------------------
# Created By: Anointiyae Beasley
#----------------------------------
"""This file tests the log functions in utility
 """ 
#----------------------------------
# 
#
import sys
sys.path.append('/app/backend')
import io
import pytest
import re
from DataClasses import Logger



def test_log_info_outputs_chart_name_and_message(capsys):
    logger = Logger(chart_name="TestChart")
    logger.log_info("This is an info message")

    # Capture output
    captured = capsys.readouterr()

    # Assert it went to stdout
    assert "This is an info message" in captured.out
    assert "TestChart" in captured.out
    assert captured.err == ""  # should not print to stderr


def test_log_error_outputs_chart_name_and_message(capsys):
    logger = Logger(chart_name="ErrorChart")
    logger.log_error("This is an error message", error_type="ValueError")

    captured = capsys.readouterr()

    # Assert it went to stderr
    assert "This is an error message" in captured.err
    assert "ErrorChart" in captured.err
    assert "ValueError" in captured.err
    assert "=" * 80 in captured.err  # separator
    assert captured.out == ""  # nothing in stdout


def test_log_error_with_traceback(capsys):
    logger = Logger(chart_name="TracebackChart")

    try:
        raise ValueError("Bad value")
    except Exception:
        logger.log_error("Caught an exception", error_type="ValueError", include_traceback=True)

    captured = capsys.readouterr()

    # Ensure traceback is included
    assert "Traceback" in captured.err
    assert "ValueError" in captured.err
    assert "Caught an exception" in captured.err
    # Ensure location and chart name are in log
    assert "TracebackChart" in captured.err


def test_log_error_includes_location(capsys):
    logger = Logger("LocationChart")

    def inner_func():
        logger.log_error("Error inside inner function")

    inner_func()
    captured = capsys.readouterr()

    # Assert the function name shows up in location
    assert "inner_func" in captured.err
    assert "LocationChart" in captured.err
