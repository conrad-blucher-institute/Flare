# -*- coding: utf-8 -*-
#ComputeMeanESB.py
#-------------------------------
# Created By : Hector Marrero-Colominas
#-------------------------------
""" This file is a postprocessing class under the IPostProcessing interface.
The post processing in this file preforms a .
By the index of the data frame!
 """ 
#-------------------------------
# 
#
#Imports
from PostProcessing.IPostProcessing import IPostProcessing
from pandas import DataFrame



class ComputeMeanESB(IPostProcessing):

    def post_process(self, data: DataFrame, op: str, left_col_key: str, right_col_key: str, out_col_key: str) -> DataFrame:

        # code logic goes here
        df = data

        print(df)

        return data