# -*- coding: utf-8 -*-
#ImmediateArithmeticOperation.py
#-------------------------------
# Created By : Matthew Kastl
#-------------------------------
""" This file is a postprocessing class under the IPostProcessing interface.
The post processing in this file preforms an arithmetic operation on columns in a data frame by a constant.
By the index of the data frame!
 """ 
#-------------------------------
# 
#
#Imports
from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame



class ImmediateArithmeticOperation(IPostProcessing):

    def post_process(self, data: DataFrame, op: str, left_col_key: str, value: float, out_col_key: str) -> DataFrame:
        """The post processing in this file preforms an arithmetic operation on columns in a data frame by a constant.
        By the index of the data frame!

        Args:
            data DataFrame: The DataFrame containing this collation of the data that has been collected.
            op - the operation to preform (ex. addition)
            left_col_key - The key the column that will be on the left side of the operation.
            value - The right operands value.
            out_col_key - The key to save the column under.

        Returns:
            DataFrame : A new dataframe obj might have to be created, this will always be a reference to the most updated version.

        NOTE::The operation available are:
            addition (out = Left + value)
            subtraction (out = Left - value) <-- ORDER MATTERS!
            multiplication (out = Left * value) 
            division (out = Left / value) <-- ORDER MATTERS!
            modulo (out = Left % value) <-- ORDER MATTERS!

        JSON Call:
        {
            "key": "ImmediateArithmeticOperation",
            "args": {
                "op": "",
                "left_col_key": "",
                "value": "",
                "out_col_key": ""   
            }
        },
        """

        # Preform the requested operation on the data
        match op:
            case 'addition':
                data[out_col_key] = data[left_col_key] + value
            case 'subtraction':
                data[out_col_key] = data[left_col_key] - value
            case 'multiplication':
                data[out_col_key] = data[left_col_key] * value
            case 'division':
                data[out_col_key] = data[left_col_key] / value
            case 'modulo':
                data[out_col_key] = data[left_col_key] % value
            case _:
                raise NotImplementedError(f'ERROR:: {op} not found in ImmediateArithmeticOperation class')

        return data

