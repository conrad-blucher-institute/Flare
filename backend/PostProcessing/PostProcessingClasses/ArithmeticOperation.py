# -*- coding: utf-8 -*-
#ArithmeticOperation.py
#-------------------------------
# Created By : Matthew Kastl
#-------------------------------
""" This file is a postprocessing class under the IPostProcessing interface.
The post processing in this file preforms a set-wise arithmetic operation columns in a data frame.
By the index of the data frame!
 """ 
#-------------------------------
# 
#
#Imports
from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame


class ArithmeticOperation(IPostProcessing):

    def post_process(self, data: DataFrame, op: str, left_col_key: str, right_col_key: str, out_col_key: str) -> DataFrame:
        """The post processing in this file preforms a set-wise arithmetic operation columns in a data frame.
        By the index of the data frame!

        Args:
            data DataFrame: The DataFrame containing this collation of the data that has been collected.
            op - the operation to preform (ex. addition)
            left_col_key - The key the column that will be on the left side of the operation.
            right_col_key - The key for the column on the right side of the operation.
            out_col_key - The key to save the column under.

        Returns:
            DataFrame : A new dataframe obj might have to be created, this will always be a reference to the most updated version.

        NOTE::  
        The operation available are:
            addition (out = Left + Right)
            subtraction (out = Left - Right) <-- ORDER MATTERS!
            multiplication (out = Left * Right) 
            division (out = Left / Right) <-- ORDER MATTERS!
            modulo (out = Left % Right) <-- ORDER MATTERS!

        JSON Call :
            {
                "key": "ArithmeticOperation",
                "args": {
                    "op": "",
                    "left_col_key": "",
                    "right_col_key": "",
                    "out_col_key": ""   
                }
            },
        """
        # Preform the requested operation on the data
        match op:
            case 'addition':
                data[out_col_key] = data[left_col_key] + data[right_col_key]
            case 'subtraction':
                data[out_col_key] = data[left_col_key] - data[right_col_key]
            case 'multiplication':
                data[out_col_key] = data[left_col_key] * data[right_col_key]
            case 'division':
                data[out_col_key] = data[left_col_key] / data[right_col_key]
            case 'modulo':
                data[out_col_key] = data[left_col_key] % data[right_col_key]
            case _:
                raise NotImplementedError(f'ERROR:: {op} not found in ArithmeticOperation class')

        return data