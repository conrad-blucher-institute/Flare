# -*- coding: utf-8 -*-
# flareRunner.py
#----------------------------------
# Created By : Matthew Kastl
#----------------------------------
""" This is the main runner script for Flare
 """ 
#----------------------------------
# 
#
#Imports
from CSPEC_Parser import CSPEC_Parser
from DataClasses import Logger
from datetime import datetime
from pandas import DataFrame
from runtimeContext import thread_storage
import os
import argparse
from Ingestion.I_Ingestion import data_ingestion_factory
from PostProcessing.IPostProcessing import post_process_factory

def generate_csv(cspec_file_path: str, verbose: bool = False) -> None:
    
    # Parse CSPEC
    try:
        CSPEC = CSPEC_Parser(cspec_file_path).parse_CSPEC()
    except Exception as e:
        raise RuntimeError(f"Failed to parse CSPEC: {cspec_file_path}") from e
        
    logger = thread_storage.logger

    # Initialize reference data and data structures
    reference_time = datetime.now()
    reference_time = reference_time.replace(second=0, microsecond=0)

    df = DataFrame()

    # Run Ingestion
    
    logger.log_info(f'------------Init Ingestion Calls-------------')
    for ingestion_call in CSPEC.data_requests:
        logger.log_info(f'\tIngestion Call: {ingestion_call.call_key}')
        logger.log_info(f'\t\tkwargs: {ingestion_call.kwargs}')
        try:
            df = data_ingestion_factory(data=df, ref_time=reference_time, key=ingestion_call.call_key, **ingestion_call.kwargs)
        except Exception as e:
            raise RuntimeError(f"Ingestion failed for call={ingestion_call.call_key}") from e
        
        if verbose: logger.log_info(f'\n{df}')
        
    logger.log_info(f'Ingestion data columns:\n {df.columns}')

    if df.empty:
        raise RuntimeError("EmptyDataFrameAfterIngestion")
    
    logger.log_info('Init Post Process Calls...')
  
    # Run PostProcessing
    for post_processing_call in CSPEC.post_processing:
        logger.log_info(f'\tPost Processing Call: {post_processing_call.call_key}')
        logger.log_info(f'\t\tkwargs: {post_processing_call.kwargs}')
        try:
            df = post_process_factory(data=df, key=post_processing_call.call_key, **post_processing_call.kwargs)
        except IndexError as e:
            raise IndexError(f"IndexError during post processing ({post_processing_call.call_key}). A required DataFrame column may be empty.") from e
        except ValueError as e:
            raise ValueError(f"ValueError during post processing ({post_processing_call.call_key})") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error during post processing ({post_processing_call.call_key})") from e
        
        if verbose: logger.log_info(f'\n{df}')
        
    logger.log_info(f'IPost Processing data columns:\n {df.columns}')
    
    if df.empty:
        raise RuntimeError("EmptyDataFrameAfterPostProcessing")
    
    # Rename the index to "Date"
    df.index.name = "Date" 
    # Export CSV
    logger.log_info('Init csv export...')
    export_path = f'./data/csv/{CSPEC.csv_name}'
    logger.log_info(f'Exporting to {export_path}...')

    for col in CSPEC.included_columns:
        logger.log_info('\t' + col) 
    
    
    try:
        df[CSPEC.included_columns].to_csv(export_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"CSV export failed for path={export_path}") from e
    logger.log_info(f"CSV successfully generated at {export_path}")
    logger.log_info("============ CSV Export Complete ===================")
       
    


def main():

    parser = argparse.ArgumentParser(
        prog='Flare-Backend',
        description='Generate a data CSV for use by Flare-Frontend',
        epilog='End Help'
    )
    parser.add_argument('-c', '--cspec', nargs='+', type=str, required=True,
                        help= 'The path of the CSPEC file of the model you want to generate the CSPEC for.')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help= 'Exports the DataFrame after each step.')

    args = parser.parse_args()
    
    for cspec_path in args.cspec:
        cspec_name = os.path.splitext(os.path.basename(cspec_path))[0] 
        thread_storage.logger = Logger(cspec_name)
        logger = thread_storage.logger
        logger.log_info('')
        logger.log_info("============ Running Flare ============")
        logger.log_info(f"---- Attempting CSPEC: {cspec_name} ----")
        try:
            generate_csv(cspec_path, args.verbose)
        except Exception as e:
            
            logger = thread_storage.logger
            logger.log_error(message=f"Pipeline failed:\n {e}", error_type="PipelineError")
            
            continue #So that the loop will continue despite one cspec failing
    
            



if __name__ == '__main__':
    main()