from urllib.error import HTTPError
from urllib.request import urlopen
from numpy import nan
from pandas import DataFrame
import json
from runtimeContext import thread_storage


def api_request( url: str):

    """Execute a web get request against  URL returning the response or Non.
    :param url: str 

    """
    logger = thread_storage.logger
    try:
        with urlopen(url) as response:
            data = json.loads(''.join([line.decode() for line in response.readlines()])) #Download and parse
        return data
    except HTTPError as err:
        logger.log_error(f'[URL:{url}] Fetch failed, HTTPError of code: {err.status} for: {err.reason}',error_type="HTTPError")
        return None
    except Exception as ex:
        logger.log_error(message=f'[URL:{url}] Fetch failed, unhandled exceptions: {ex}')
        return None
    

def add_empty_column(data: DataFrame, col_name: str):
    logger = thread_storage.logger
    logger.log_info(f'Warning:: Column {col_name} is being initialized as all Nans this is likely due to failing to get data back from the ingestion source.')
    data[col_name] = nan
    return data