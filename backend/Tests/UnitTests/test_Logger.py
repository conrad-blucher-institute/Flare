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
import traceback
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
    
def _extract_logged_traceback(err_text: str) -> str | None:
    """
    Return the traceback block after 'Traceback   :' up to the next '====' or end.
    Matches your logger's formatting.
    """
    m = re.search(r"^Traceback\s*:\s*\n(?P<tb>.*?)(?:\n=+\n|\Z)", err_text, flags=re.S | re.M)
    return m.group("tb") if m else None


def _extract_location_line(err_text: str) -> str | None:
    """
    Extract the single 'Location    : <module>::<func>()' line's payload.
    """
    m = re.search(r"^Location\s*:\s*(?P<loc>.+)$", err_text, flags=re.M)
    return m.group("loc").strip() if m else None


def test_log_error_includes_correct_traceback_and_location(capsys):
    """
    - Cause a nested exception to ensure a multi-frame traceback.
    - Call logger.log_error(...) inside the except block.
    - Assert:
        * Logged traceback == traceback.format_exc() (exact match, trimmed)
        * Location line equals the caller function of log_error (outer_handler)
        * Traceback includes the true error site function (deep_boom)
    """
    logger = Logger(chart_name="TracebackChart")

    def deep_boom():
        return 1 / 0

    def mid():
        return deep_boom()

    def outer_handler():
        try:
            mid()
        except Exception:
            # Expected traceback for this exact exception stack:
            expected_tb = traceback.format_exc()
            logger.log_error("Caught an exception", error_type="ZeroDivisionError")
            return expected_tb  # return so test can compare outside

    expected_tb = outer_handler()
    err_text = capsys.readouterr().err

    # Sanity headers/fields are present
    assert "Caught an exception" in err_text
    assert "ZeroDivisionError" in err_text
    assert "Traceback" in err_text

    # ----- Traceback exactness -----
    logged_tb = _extract_logged_traceback(err_text)
    assert logged_tb is not None, "Traceback block not found in stderr output."
    assert logged_tb.strip() == expected_tb.strip(), (
        "Logged traceback does not match Python's traceback.format_exc().\n"
        "---- Logged ----\n"
        f"{logged_tb}\n"
        "---- Expected ----\n"
        f"{expected_tb}"
    )

    # Traceback should include the true error site (deep_boom) and mid()
    assert "deep_boom" in logged_tb
    assert "mid" in logged_tb

    # ----- Location correctness -----
    loc = _extract_location_line(err_text)
    assert loc is not None, "Location line not found."

    assert loc.endswith("::outer_handler()"), f"Unexpected location: {loc}"


    
