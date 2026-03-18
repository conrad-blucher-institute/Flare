# -*- coding: utf-8 -*-
# test_SemaphoreOutputLatest.py
#-------------------------------
# Created By: Christian Quintero
# 03/18/2026
#----------------------------------
"""
This file tests the SemaphoreOutputLatest data ingestion class.

docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_SemaphoreOutputLatest.py -v
""" 
#----------------------------------
# 
#
import pytest
import numpy as np
from pandas import DataFrame
from unittest.mock import MagicMock
from flareRunner import thread_storage
from Ingestion.IngestionClasses.SemaphoreOutputLatest import SemaphoreOutputLatest

# NOTE:: nulls were replaced with None, true was changed to True,
# and the data value was changed to 1.0 for simplicity
# to test legacy models work as expected
response = {
  "Bird-Island_Water-Temperature_120hr": {
    "description": {
      "modelName": "Bird-Island_Water-Temperature_120hr",
      "modelVersion": "1.0.0",
      "dataSeries": "pWaterTmp",
      "dataLocation": "SouthBirdIsland",
      "dataDatum": None
    },
    "timeDescription": None,
    "isComplete": True,
    "_Series__data": [
      {
        "dataValue": [
          [
            [
              1.0
            ]
          ]
        ],
        "dataUnit": "celsius",
        "timeGenerated": "2026-03-18T15:00:00",
        "leadTime": 432000
      }
    ]
  }
}

# NOTE:: nulls were replaced with None, true was changed to True,
# and the data values were changed for simplicity
# to test normal MRE data works as expected
mre_response = {
  "MRE_Bird-Island_Water-Temperature_120hr": {
    "description": {
      "modelName": "MRE_Bird-Island_Water-Temperature_120hr",
      "modelVersion": "1.0.0",
      "dataSeries": "pWaterTmp",
      "dataLocation": "SouthBirdIsland",
      "dataDatum": None
    },
    "timeDescription": None,
    "isComplete": True,
    "_Series__data": [
      {
        "dataValue": [
          [
            [1.0],  [2.0],  [3.0],  [4.0],  [5.0],  [6.0],  [7.0],  [8.0],  [9.0],  [10.0],
            [11.0], [12.0], [13.0], [14.0], [15.0], [16.0], [17.0], [18.0], [19.0], [20.0],
            [21.0], [22.0], [23.0], [24.0], [25.0], [26.0], [27.0], [28.0], [29.0], [30.0],
            [31.0], [32.0], [33.0], [34.0], [35.0], [36.0], [37.0], [38.0], [39.0], [40.0],
            [41.0], [42.0], [43.0], [44.0], [45.0], [46.0], [47.0], [48.0], [49.0], [50.0],
            [51.0], [52.0], [53.0], [54.0], [55.0], [56.0], [57.0], [58.0], [59.0], [60.0],
            [61.0], [62.0], [63.0], [64.0], [65.0], [66.0], [67.0], [68.0], [69.0], [70.0],
            [71.0], [72.0], [73.0], [74.0], [75.0], [76.0], [77.0], [78.0], [79.0], [80.0],
            [81.0], [82.0], [83.0], [84.0], [85.0], [86.0], [87.0], [88.0], [89.0], [90.0],
            [91.0], [92.0], [93.0], [94.0], [95.0], [96.0], [97.0], [98.0], [99.0], [100.00]
          ]
        ],
        "dataUnit": "celsius",
        "timeGenerated": "2026-03-18T15:00:00",
        "leadTime": 432000
      }
    ]
  }
}

# to test that when dataValue is missing, nan is appended
missing_data_value = {
  "Bird-Island_Water-Temperature_120hr": {
    "description": {
      "modelName": "Bird-Island_Water-Temperature_120hr",
      "modelVersion": "1.0.0",
      "dataSeries": "pWaterTmp",
      "dataLocation": "SouthBirdIsland",
      "dataDatum": None
    },
    "timeDescription": None,
    "isComplete": True,
    "_Series__data": [
      {
        "dataValue": [],
        "dataUnit": "celsius",
        "timeGenerated": "2026-03-18T15:00:00",
        "leadTime": 432000
      }
    ]
  }
}

# to test that bad shapes are caught and nan is appended
# this case uses has a shape of (1)
single_list_value = {
  "Bird-Island_Water-Temperature_120hr": {
    "description": {
      "modelName": "Bird-Island_Water-Temperature_120hr",
      "modelVersion": "1.0.0",
      "dataSeries": "pWaterTmp",
      "dataLocation": "SouthBirdIsland",
      "dataDatum": None
    },
    "timeDescription": None,
    "isComplete": True,
    "_Series__data": [
      {
        "dataValue": [1.0],
        "dataUnit": "celsius",
        "timeGenerated": "2026-03-18T15:00:00",
        "leadTime": 432000
      }
    ]
  }
}

# to test that bad shapes are caught and nan is appended
# this case uses (2, 1, 1)
two_one_one = {
    "Bird-Island_Water-Temperature_120hr": {
    "description": {
      "modelName": "Bird-Island_Water-Temperature_120hr",
      "modelVersion": "1.0.0",
      "dataSeries": "pWaterTmp",
      "dataLocation": "SouthBirdIsland",
      "dataDatum": None
    },
    "timeDescription": None,
    "isComplete": True,
    "_Series__data": [
      {
        "dataValue": [
            [
                [1.0]
            ],
            [
                [2.0]
            ]
        ],
        "dataUnit": "celsius",
        "timeGenerated": "2026-03-18T15:00:00",
        "leadTime": 432000
      }
    ]
  }
}

@pytest.mark.parametrize(
    "response, name, expected_data",
    [
        (response, "Bird-Island_Water-Temperature_120hr", 1.0),
        (mre_response, "MRE_Bird-Island_Water-Temperature_120hr",
            [
                1.0,  2.0,  3.0,  4.0,  5.0,  6.0,  7.0,  8.0,  9.0,  10.0,
                11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0,
                21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0,
                31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0,
                41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.00,
                51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0,
                61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0,
                71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0,
                81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0,
                91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.00
            ]
        ),
        (missing_data_value, "Bird-Island_Water-Temperature_120hr", np.nan),
        (single_list_value, "Bird-Island_Water-Temperature_120hr", np.nan),
        (two_one_one, "Bird-Island_Water-Temperature_120hr", np.nan)
    ],
    ids = [
        "Legacy Model Response",
        "MRE Model Response",
        "Missing dataValue",
        "Bad Shape: Single List",
        "Bad Shape: (2, 1, 1)"
    ]
)
def test_add_data(response, name, expected_data):
    """
    tests the __add_data function for the new parsing logic from the semaphore CRPS refactor

    docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_SemaphoreOutputLatest.py::test_add_data -v
    """
    nan_tests = [missing_data_value, single_list_value, two_one_one]
    ingestor = SemaphoreOutputLatest()
    thread_storage.logger = MagicMock()

    result_df = ingestor._SemaphoreOutputLatest__add_data(
        df = DataFrame(),
        response = response,
        model_names = [name],
        col_name = 'test_col'
    )

    result_col = result_df['test_col']

    if response in nan_tests:
        assert np.isnan(result_col.iloc[0])
    else:
        assert result_col.iloc[0] == expected_data
    
    print(f'\n\n\nResult DF: {result_df}\n result col: {result_col}\n\n\n')


