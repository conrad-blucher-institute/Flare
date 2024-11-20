import pandas as pd
from pandas import date_range
import numpy as np
from pandas import DataFrame
from datetime import datetime, timedelta
from io import StringIO


def post_process(df: DataFrame, col_name: str, interpolation_interval: int, limit: int) -> bool:
     """The post processing in this file preforms an linear interpolation of a column.

     Args:
          df DataFrame: The DataFrame containing this collation of the data that has been collected.
          col_name: str - The column in the DataFrame to interpolate.
          interpolation_interval: int - The interval to interpolate data on, in seconds.
          limit: int - The amount of Nan's in a row it will interpolate.

     Returns:
          bool : A boolean value based on the operations success.

     NOTE::It is expected the data will not need to be reindexed by this function.
     NOTE::This function actually uses time based interpolation which is the same as linear interpolation.


     JSON Call:
     {
          "call": "LinearInterpolation",
          "args": {
               "col_name": "",
               "interpolation_interval": -1,
               "limit: -1
          }
     },
     """
     
     # Isolate the data we are going to interpolate
     data = df[col_name]

     # The index of the data frame isn't necessarily the correct for the values we want to interpolate for this series. Thus we reindex
     # the data to the specific interval we want to interpolate on.
     data = data.reindex(date_range(start=data.index[0], end=data.index[-1], freq=timedelta(seconds=interpolation_interval)))

     # We want to not interpolate if there are too many Nans in a row. However the pandas limit parameter only stops interpolation once its
     # counted a cumulative sum of Nans higher than limit. Thus it keeps the Nans in that group where the cumulative sum was still < limit.
     # The forwards cumulative mask looks for where this mistake will happen thus used to overwrite the interpolated values with Nan.
     nan_mask = data.isna()
     cumulative_nan_streaks = nan_mask.groupby(~nan_mask).cumsum()
     forward_cumulative_nan_mask = cumulative_nan_streaks.gt(limit)

     # We do the interpolation backwards because a forwards cumulative mask was easier to write than a backwards one.
     backwards_interpolation = data.interpolate(method= 'time', limit= limit, limit_area= 'inside', limit_direction= 'backward')
     
     # Here we repair the mistake by looking at the forward cumulative mask and inserting Nan.
     backwards_interpolation[forward_cumulative_nan_mask] = np.nan

     # We have to reindex the data back in, hopefully this reindex does nothing and Nans were in-placed correctly before this call.
     #df = df.join(index=data.index, copy=False, fill_value=np.nan)
     #df.loc[:, col_name] = backwards_interpolation
     df.drop(columns=[col_name], inplace=True)
     df = df.join(backwards_interpolation, how='outer')
     
     return df



series1 = {'data6Min': [val for val in range(101)]} # 10 hours of 5min data
index = date_range(datetime(2024, 1, 1, 0, 0, 0), periods=len(series1['data6Min']), freq='6min')
df_6min = pd.DataFrame(series1, index=index)

series2 = {'data5hr': [val for val in range(3)]} # 10 hours of 5min data
index2 = date_range(datetime(2024, 1, 1, 0, 0, 0), periods=len(series2['data5hr']), freq='5h')
df_5hr = pd.DataFrame(series2, index=index2)

series3 = {'data1hr': [val for val in range(11)]} # 10 hours of 5min data
index3 = date_range(datetime(2024, 1, 1, 0, 0, 0), periods=len(series3['data1hr']), freq='1h')
df_1hr = pd.DataFrame(series3, index=index3)

one_hour_to_six_min_interpolation = df_6min.join(df_1hr, how='outer')['data1hr'].interpolate(method='time')
five_hour_to_ten_hour_interpolation = df_1hr.join(df_5hr, how='outer')['data5hr'].interpolate(method='time')

test_df = df_6min.join(df_1hr, how='outer').join(df_5hr, how='outer')


print(test_df)
test_df = post_process(test_df, 'data5hr', 3600, 500)
print('----')
print(test_df)

 # '(, 'data5hr', 3600, 500, 101),
# result = test_df['data5hr'].tolist()
# expected = five_hour_to_ten_hour_interpolation.tolist()
# print(result)
# print(expected)

# Iterate through the resulting components checking if they were calculated correctly
# for actual, expected in zip(result, expected):
#      tolerance = 1e-5

#      print(actual, '|', expected)
     # if not isclose(actual, expected, abs_tol=tolerance):
     #      assert False
# assert True