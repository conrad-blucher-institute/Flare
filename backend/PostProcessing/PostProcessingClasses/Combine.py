# -*- coding: utf-8 -*-
#Combine.py
#-------------------------------
# Created By : Matthew Kastl
#-------------------------------
""" The post processing in this file preforms combines two columns together. If there are non Nan values
on the same index it will always prefer the left value.
 """ 
#-------------------------------
# 
#
#Imports
from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame, isna


class Combine(IPostProcessing):

    def post_process(self, data: DataFrame, left_col_key: str, right_col_key: str) -> DataFrame:
        """The post processing in this file preforms combines two columns together. If there are non Nan values
        on the same index it will always prefer the left value.

        Args:
            data DataFrame: The DataFrame containing this collation of the data that has been collected.
            left_col_key - The key the column that will be on the left side of the operation.
            right_col_key - The key for the column on the right side of the operation.

        Returns:
            DataFrame : A new dataframe obj might have to be created, this will always be a reference to the most updated version.

        NOTE:: Combines right -> left preferring left!!

        JSON Call :
            {
                "key": "Combine",
                "args": {
                    "left_col_key": "",
                    "right_col_key": "",
                }
            },
        """
        # Isolate the series
        s_left = data[left_col_key]
        s_right = data[right_col_key]

        # A method that will prefer the left value, unless its nan, then it will take the right
        prefer_left = lambda left, right: (right if isna(left) else left)

        # Combine the data with the above rule and write it to the left column name
        data[left_col_key] = s_left.combine(s_right, prefer_left)
        return data