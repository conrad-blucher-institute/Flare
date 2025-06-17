# -*- coding: utf-8 -*-
#DataClasses.py
#----------------------------------
# Created By : Matthew Kastl
#----------------------------------
""" This file contains a collection of data classes for use by Flare.
These data classes are to make function call more generic and readable
 """ 
#----------------------------------
# 
#
#Imports


class Call():
    def __init__(self, call_key: str, **kwargs) -> None:
        self.call_key = call_key
        self.kwargs = kwargs

    def __str__(self):
        return f'''[Call]--------------------------------
            call_key: {self.call_key}
            kwargs: {self.kwargs}\n---------------------------------------'''
    

class CSPEC():
    def __init__(self, chart_name: str, data_requests: list[Call], post_processing: list[Call], csv_name: str, included_columns: list[str]) -> None:
        self.chart_name = chart_name
        self.data_requests = data_requests
        self.post_processing = post_processing
        self.csv_name = csv_name 
        self.included_columns = included_columns

    def __str__(self) -> str:

        requests = ''
        for r in self.data_requests:
            requests += f'\t[request]\n\t\tcall_key:{r.call_key}\n\t\tkwargs:{r.kwargs}\n\t------\n'
        if not requests: requests = '\tNone\n'

        post_processing = ''
        for p in self.post_processing:
            post_processing += f'\t[post_process]\n\t\tcall_key:{p.call_key}\n\t\tkwargs:{p.kwargs}\n\t------\n'
        if not post_processing: post_processing = '\tNone\n'

        # I know this looks formatted weird but this prints it correctly, dont indent it!
        return  f'[CSPEC]--------------------------------\n \
    chart_name: {self.chart_name}\n\
    data_requests:\n{requests}\n\
    post_processing: \n{post_processing}\n\
    csv_name: {self.csv_name}\n\
    included_columns: {self.included_columns}\n\
---------------------------------------' 
        