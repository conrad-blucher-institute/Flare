from urllib.error import HTTPError
from urllib.request import urlopen
from numpy import nan
from pandas import DataFrame
import json
from utility import log_info,log_error, get_current_chart_name

def api_request( url: str):
    """Execute a web get request against  URL returning the response or Non.
    :param url: str 

    """
    try:
        with urlopen(url) as response:
            data = json.loads(''.join([line.decode() for line in response.readlines()])) #Download and parse
        return data
    except HTTPError as err:
        log_error(f'Fetch failed, HTTPError of code: {err.status} for: {err.reason}',chart_name=get_current_chart_name(),error_type="HTTPError")
        return None
    except Exception as ex:
        log_error(message=f'Fetch failed, unhandled exceptions: {ex}',chart_name=get_current_chart_name())
        return None
    

def add_empty_column(data: DataFrame, col_name: str):
    log_info(f'Warning:: Column {col_name} is being initialized as all Nans this is likely due to failing to get data back from the ingestion source.')
    data[col_name] = nan
    return data