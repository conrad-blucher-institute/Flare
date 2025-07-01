# -*- coding: utf-8 -*-
#test_Logging.py
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

import pytest
from utility import log_error, set_current_chart_name, get_current_chart_name



def test_chart_name_tracking():
    set_current_chart_name("test_chart")
    assert get_current_chart_name() == "test_chart"

    set_current_chart_name(None)
    assert get_current_chart_name() == "unknown_chart"

    set_current_chart_name("  my_chart  ")
    assert get_current_chart_name() == "my_chart"

def test_log_error_output(capfd):
    set_current_chart_name("TestChart")
    log_error("This is a test error", chart_name=get_current_chart_name(), error_type="TestError")

    out, err = capfd.readouterr()

    assert "TestError" in err
    assert "ChartName   : TestChart" in err
    assert "This is a test error" in err
    assert "Location    :" in err
    assert "=" * 80 in err
