from CSPEC_Parser import CSPEC_Parser
from DataClasses import Call
from datetime import datetime
from pandas import DataFrame
import argparse

from Ingestion.I_Ingestion import data_ingestion_factory
from PostProcessing.IPostProcessing import post_process_factory


def generate_csv(cspec_file_path: str, verbose: bool = False) -> None:
    
    # Parse CSPEC
    CSPEC = CSPEC_Parser(cspec_file_path).parse_CSPEC()

    # Initialize reference data and data structures
    reference_time = datetime.now()
    reference_time = reference_time.replace(second=0, microsecond=0)

    df = DataFrame()

    # Run Ingestion
    print('Init Ingestion Calls...')
    for ingestion_call in CSPEC.data_requests:
        print(f'\tIngestion Call: {ingestion_call.call_key}')
        print(f'\t\tkwargs: {ingestion_call.kwargs}')
        df = data_ingestion_factory(data=df, ref_time=reference_time, key=ingestion_call.call_key, **ingestion_call.kwargs)
        if verbose: print(df)
    

    # Run PostProcessing
    print('Init Post Process Calls...')
    for post_processing_call in CSPEC.post_processing:
        print(f'\tPost Processing Call: {post_processing_call.call_key}')
        print(f'\t\tkwargs: {post_processing_call.kwargs}')
        df = post_process_factory(data=df, key=post_processing_call.call_key, **post_processing_call.kwargs)
        if verbose: print(df)

    # Export CSV
    print('Init csv export...')
    export_path = f'./data/csv/{CSPEC.csv_name}'
    print(f'Exporting to {export_path}...')

    for col in CSPEC.included_columns:
        print('\t' + col) 
    df[CSPEC.included_columns].to_csv(export_path)


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