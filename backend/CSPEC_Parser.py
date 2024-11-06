# -*- coding: utf-8 -*-
#CSPEC_Parser.py
#----------------------------------
# Created By : Matthew Kastl
#----------------------------------
""" The CSPEC or chart specification file is a file containing all instruction and information
for Flare to run a generate a data CSV. This file contains a parent parser that will execute sub parsers
for any version of CSPEC.
 """ 
#----------------------------------
# 
#
#Imports
from os.path import exists
from json import load
from DataClasses import *

class CSPEC_Parser:
    def __init__(self, file_path: str) -> None:

        if not exists(file_path):
            print(f'{file_path} not found!')
            raise FileNotFoundError
        with open(file_path) as CSPEC_file:
            
            # Read CSPEC from file and grab version
            self.__CSPEC_json: dict = load(CSPEC_file)
            self.__CSPEC_version: str = self.__CSPEC_json.get('CSPEC_version')


    def parse_CSPEC(self) -> CSPEC:
        
        match self.__CSPEC_version:
            case '1.0.0':
                sub_parser = CSPEC_sub_Parser_1_0_0(self.__CSPEC_json)
            case _:
                raise NotImplementedError(f'No parser for CSPEC version {self.__CSPEC_json} found!')
            
        return sub_parser.parse_CSPEC() 


class CSPEC_sub_Parser_1_0_0:

    def __init__(self, json: dict) -> None:
        self.__CSPEC_json = json


    def parse_CSPEC(self) -> CSPEC:
        """ Parses a CSPEC json dictionary into an actual CSPEC obj.
            :return CSPEC
        """
        chart_name = self.__CSPEC_json["chart_name"]
        data_requests = self.__parse_call_group("data_requests")
        post_processing = self.__parse_call_group("post_processing")
        csv_name, included_columns = self.__parse_csv_config(self.__CSPEC_json["csv_config"])
        return CSPEC(
            chart_name=chart_name,
            data_requests=data_requests,
            post_processing=post_processing,
            csv_name=csv_name,
            included_columns=included_columns
        )


    def __parse_call_group(self, target: str) -> list[Call]:
        """ Parses a collection of call objects from a dictionary.
            :param target: str - The target keyword to query the collection from the dictionary.
            :return list[Call] - A list of the parsed calls.
        """
        call_group = self.__CSPEC_json[target]
        return [self.__parse_call(call) for call in call_group]


    def __parse_call(self, call_json: dict) -> Call:
        """ Parses a call objects from a dictionary.
            :param call_json: dict - The dictionary from the json, to be parsed.
            :return Call - The parsed call.
        """
        return Call(
            call_key = call_json.get("key"),  
            kwargs = call_json.get("args", {})
        )
    

    def __parse_csv_config(self, csv_config_json: dict) -> tuple[str, list[str]]:
        """ Parses a the csv_config from the CSPEC.
            :param csv_config_json: dict - The dictionary from the json, to be parsed.
            :return str - The csv name.
            :return list[str] - The included columns in the csv.
        """
        csv_name = csv_config_json["csv_name"]
        included_columns = csv_config_json["included_columns"]
        return csv_name, included_columns