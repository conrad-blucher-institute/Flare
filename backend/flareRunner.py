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
from DataClasses import Call
from datetime import datetime
from pandas import DataFrame
import argparse

from Ingestion.I_Ingestion import data_ingestion_factory
from PostProcessing.IPostProcessing import post_process_factory
from utility import log_info,log_error,get_current_chart_name


def generate_csv(cspec_file_path: str, verbose: bool = False) -> None:
    
    # Parse CSPEC
    CSPEC = CSPEC_Parser(cspec_file_path).parse_CSPEC()


    # Initialize reference data and data structures
    reference_time = datetime.now()
    reference_time = reference_time.replace(second=0, microsecond=0)

    df = DataFrame()

    # Run Ingestion
    log_info('')
    log_info("============ Running Flare ============")
    log_info(f'------------{reference_time} : Init Ingestion Calls-------------')
    for ingestion_call in CSPEC.data_requests:
        log_info(f'\tIngestion Call: {ingestion_call.call_key}')
        log_info(f'\t\tkwargs: {ingestion_call.kwargs}')
        df = data_ingestion_factory(data=df, ref_time=reference_time, key=ingestion_call.call_key, **ingestion_call.kwargs)
        if verbose: log_info(df)
    log_info(f'Ingestion data columns: {df.columns}')

    if df.empty:
        log_error(message="DF is empty. Exiting....",chart_name=CSPEC.chart_name)
        return
    
    try:
        # Run PostProcessing
        log_info('Init Post Process Calls...')
        for post_processing_call in CSPEC.post_processing:
            log_info(f'\tPost Processing Call: {post_processing_call.call_key}')
            log_info(f'\t\tkwargs: {post_processing_call.kwargs}')
            df = post_process_factory(data=df, key=post_processing_call.call_key, **post_processing_call.kwargs)
            if verbose: log_info(f'\n{df}')
        log_info(f'IPost Processing data columns: {df.columns}')

        # Rename the index to "Date"
        df.index.name = "Date" 
        # Export CSV
        log_info('Init csv export...')
        export_path = f'./data/csv/{CSPEC.csv_name}'
        log_info(f'Exporting to {export_path}...')

        for col in CSPEC.included_columns:
            log_info('\t' + col) 
        
        if df.empty:
            log_error(message="DF is empty after PostProcessing. Exiting....",chart_name=CSPEC.chart_name)
            return
        
        df[CSPEC.included_columns].to_csv(export_path)
        log_info(f"CSV successfully generated at {export_path}")
        log_info("============ CSV Export Complete ===================")
       
            
    except IndexError as e:
        log_error(message=f"IndexError during post processing: {e}. DataFrame column may be empty.",chart_name=get_current_chart_name(),error_type="IndexError",include_traceback=True)
    except ValueError as e:
        log_error(message=f"ValueError: {e}.",chart_name=get_current_chart_name(),error_type="ValueError",include_traceback=True)
    except FileNotFoundError as e:
         log_error(message=f"CSV export failed: {e}",chart_name=get_current_chart_name(),error_type="FileNotFoundError", include_traceback=True)
    except Exception as e:
        log_error(message=f"An unexpected error occurred: {e}",chart_name=get_current_chart_name(),error_type="Exception",include_traceback=True)
    


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
        generate_csv(cspec_path, args.verbose)



if __name__ == '__main__':
    main()