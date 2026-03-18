# -*- coding: utf-8 -*-
# test_Combine.py
#-------------------------------
# Created By: Christian Quintero
#----------------------------------
"""
This file tests the SemaphoreOutputLatest data ingestion class.

NOTE:: these tests don't actually call the SemaphoreOutputLatest class
but instead use the same logic to test the parsing and validation of the API response

docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_SemaphoreOutputLatest.py -v
""" 
#----------------------------------
# 
#
import pytest
import numpy as np
from pandas import DataFrame
from datetime import datetime, timedelta



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
sinlge_list_value = {
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
        )
    ],
    ids = [
        "Legacy Model Response",
        "MRE Model Response"
    ]
)
def test_add_data(response, name, expected_data):
    """
    tests the __add_data function for the new parsing logic from the semaphore CRPS refactor

    NOTE:: This test doesn't actually call the __add_data function, but uses the same logic

    docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_SemaphoreOutputLatest.py::test_add_data -v
    """
    index = []
    data = []
    expected_shapes = [(1, 100, 1), (1, 1, 1)]

    model_response  = response[name]
    data_point = model_response['_Series__data'][0]

    timeGenerated = datetime.strptime(data_point['timeGenerated'], '%Y-%m-%dT%H:%M:%S')
    verifiedTime = timeGenerated + timedelta(seconds=data_point['leadTime'])
    index.append(verifiedTime)
    value = data_point['dataValue']

    # assert regular responses pass the expected shape check
    assert np.array(value).shape in expected_shapes

    # test the flattening
    # the array should have the shape of [1.0, 2.0, ..., 100.0]
    if 'MRE' in name:
        flat_array = np.asarray(value[0], dtype=float).flatten().tolist()
        data.append(flat_array)
    
    # test the single value parsing
    # the data appended should be a scalar such as 1.0, not an array
    else:
        single_value = float(value[0][0][0])
        data.append(single_value)
    
    assert data[0] == expected_data

@pytest.mark.parametrize(
    "response, name",
    [
        (missing_data_value, "Bird-Island_Water-Temperature_120hr"),
        (sinlge_list_value, "Bird-Island_Water-Temperature_120hr"),
        (two_one_one, "Bird-Island_Water-Temperature_120hr")
    ],
    ids = [
        "Missing Data Value",
        "Bad Shape",
        "2x1x1 Shape"
    ]
)
def test_add_data_nan_cases(response, name):
    """
    test the nan cases for __add_data, such as missing data values and bad shapes

    NOTE:: this test doesn't actually call the __add_data function, but uses the same logic

    docker exec flare-backend python3 -m pytest /app/backend/Tests/UnitTests/test_SemaphoreOutputLatest.py::test_add_data_nan_cases -v
    """
    index = []
    data = []
    expected_shapes = [(1, 100, 1), (1, 1, 1)]
    bad_shapes = [sinlge_list_value, two_one_one]

    model_response  = response[name]
    data_point = model_response['_Series__data'][0]

    timeGenerated = datetime.strptime(data_point['timeGenerated'], '%Y-%m-%dT%H:%M:%S')
    verifiedTime = timeGenerated + timedelta(seconds=data_point['leadTime'])
    index.append(verifiedTime)
    value = data_point['dataValue']

    
    if response == missing_data_value:
        # test that when dataValue is missing, nan is appended
        assert value in (None, 'None', [])
        data.append(np.nan)
    else:
        # test that the bad shape cases are caught and nan is appended
        assert np.array(value).shape not in expected_shapes
        data.append(np.nan)

    # assert that the data looks like [nan]
    assert np.isnan(data[0])

        

