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
    """
        The post processing in this file preforms an arithmetic operation on columns in a data frame by a constant.
        By the index of the data frame!
        The operation available are:
            addition (out = Left + value)
            subtraction (out = Left - value) <-- ORDER MATTERS!
            multiplication (out = Left * value) 
            division (out = Left / value) <-- ORDER MATTERS!
            modulo (out = Left % value) <-- ORDER MATTERS!

        args: 
                op - the operation to preform (ex. addition)
                left_col_key - The key the column that will be on the left side of the operation.
                value - The constant value for the operation as a string float.
                out_col_key - The key to save the column under.

        json_copy:
        {
            "call": "ArithmeticOperation",
            "args": {
                "op": "",
                "left_col_key": "",
                "value": "",
                "out_col_key": ""   
            }
        },

    """
    def post_process(self, data: DataFrame, **kwargs) -> bool:
        """Method to define the post-processing operation.

        Args:
            data DataFrame: The DataFrame containing this collation of the data that has been collected.
            kwargs Dict: A kwargs dictionary containing the information from the CSPEC.

        Returns:
            bool : A boolean value based on the operations success.
        """

        # Unpack arguments from kwargs object
        OPERATION = kwargs['op']
        LEFT_KEY = kwargs['left_col_key']
        VALUE = float(kwargs['right_col_key'])
        OUT_KEY = kwargs['out_col_key']

        # Preform the requested operation on the data
        match OPERATION:
            case 'addition':
                data[OUT_KEY] = data[LEFT_KEY] + VALUE
            case 'subtraction':
                data[OUT_KEY] = data[LEFT_KEY] - VALUE
            case 'multiplication':
                data[OUT_KEY] = data[LEFT_KEY] * VALUE
            case 'division':
                data[OUT_KEY] = data[LEFT_KEY] / VALUE
            case 'modulo':
                data[OUT_KEY] = data[LEFT_KEY] % VALUE
            case _:
                raise NotImplementedError(f'ERROR:: {OPERATION} not found in ArithmeticOperation class')

        return True