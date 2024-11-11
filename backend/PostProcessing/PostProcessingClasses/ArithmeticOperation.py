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
import numpy as np
from pandas import DataFrame


class ArithmeticOperation(IPostProcessing):
    """
        The post processing in this file preforms a set-wise arithmetic operation columns in a data frame.
        By the index of the data frame!
        The operation available are:
            addition (out = Left + Right)
            subtraction (out = Left - Right) <-- ORDER MATTERS!
            multiplication (out = Left * Right) 
            division (out = Left / Right) <-- ORDER MATTERS!
            modulo (out = Left % Right) <-- ORDER MATTERS!
        

        args: 
                op - the operation to preform (ex. addition)
                left_col_key - The key the column that will be on the left side of the operation.
                right_col_key - The key for the column on the right side of the operation.
                out_col_key - The key to save the column under.

        json_copy:
        {
            "call": "ArithmeticOperation",
            "args": {
                "op": "",
                "left_col_key": "",
                "right_col_key": "",
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
        RIGHT_KEY = kwargs['right_col_key']
        OUT_KEY = kwargs['out_col_key']

        # Preform the requested operation on the data
        match OPERATION:
            case 'addition':
                data[OUT_KEY] = data[LEFT_KEY] + data[RIGHT_KEY]
            case 'subtraction':
                data[OUT_KEY] = data[LEFT_KEY] - data[RIGHT_KEY]
            case 'multiplication':
                data[OUT_KEY] = data[LEFT_KEY] * data[RIGHT_KEY]
            case 'division':
                data[OUT_KEY] = data[LEFT_KEY] / data[RIGHT_KEY]
            case 'modulo':
                data[OUT_KEY] = data[LEFT_KEY] % data[RIGHT_KEY]
            case _:
                raise NotImplementedError(f'ERROR:: {OPERATION} not found in ArithmeticOperation class')

        return True