import pandas as pd
from pandas import date_range
import numpy as np
from pandas import DataFrame
from datetime import datetime, timedelta
from io import StringIO

from Ingestion.I_Ingestion import data_ingestion_factory


df = DataFrame()
ref = datetime(2024, 11, 14, 22, 0, 0)
key = 'SemaphoreInputs'
kargs =  {
          "column_name": "test",
          "source": "NDFD_EXP", 
          "series": "pWnSpd", 
          "location": "VirginiaKey",       
          "interval": 3600,
          "range": [-11, 0]
        }
df= data_ingestion_factory(df, ref, key, kargs)
print(df)

kargs =  {
          "column_name": "test2",
          "model_names": [
            "12hr_VirginiaKey_wl",
            "24hr_VirginiaKey_wl",
            "48hr_VirginiaKey_wl",
            "72hr_VirginiaKey_wl",
            "96hr_VirginiaKey_wl"           
          ] 
        }

key = 'SemaphoreOutputLatest'
print(data_ingestion_factory(df, ref, key, kargs))