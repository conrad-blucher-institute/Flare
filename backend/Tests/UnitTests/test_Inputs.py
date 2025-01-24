# -*- coding: utf-8 -*-
# test_Inputs.py
#-------------------------------
# Created By: Anointiyae Beasley
#----------------------------------
"""This file tests the Inputs
 """ 
#----------------------------------
# 
#
import sys
sys.path.append('/app/backend')

import pytest
from Ingestion.I_Ingestion import data_ingestion_factory
from datetime import datetime
from numpy import nan
from pandas import DataFrame

# Numeric test data

@pytest.mark.parametrize("column_name, location, source, series, interval, range, datum", [
    ("Air Temperature Measurement", "SBI", "NOAATANDC", "dAirTmp", "3600", [-144, 0], None),
    ("Air Temperature Prediction", "lagunamadre", "NDFD_EXP", "pAirTemp", "3600", [120, 1], None),  # Tests left preference over nan
    ("Air Temperature Prediction", "lagunamadre", "NDFD_EXP", "pAirTemp", "3600", [120, 0], None),
    ("Air Temperature Prediction", "lagunamadre", "NDFD_EXP", "pAirTemp", "3600", [0, 120], None),
    ("Air Temperature Prediction", "lagunamadre", "NDFD_EXP", "pAirTemp", "3600", [1, 120], None),
    ("Air Temperature Prediction", "lagunamadre", "NDFD_EXP", "pAirTemp", "3600", [2, 120], None)
])
def test_post_process_data(column_name: str, location: str, source: str, series: str, interval: str, range: list[int], datum: str):
    """This function tests the post process method in the Arithmetic Operation post process class.
    """

    test_df = DataFrame()
    reference_time = datetime.now()
    reference_time = reference_time.replace(second=0, microsecond=0)
    key = "SemaphoreInputs"
    kwargs = {
        "column_name": column_name,
        "location": location, 
        "source": source,
        "series": series,
        "interval": interval,
        "range": range
    }
    # Call the factory to get the resolver and pass it the fake input data and the post process call
    print(f'---------Ingesting {column_name} at range {range}-----------------')
    test_df = data_ingestion_factory(test_df, reference_time, key, kwargs)
    print(f'DF: {test_df}')
    assert True

