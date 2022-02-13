"""
Functions for retrieving data from Chicago data portal

Ryoya Hashimoto
"""

# make sure to install these packages before running:
# pip install sodapy

import os
import requests
import json
import pandas as pd
from sodapy import Socrata


#Chicago poverty and crime: ID = "fwns-pcmk"
#Chicago Population Counts: ID = "85cm-7uqa"


def read_json_to_dict(file_path):
    with open(file_path) as f:
        data_dict = json.load(f)
    return data_dict


def get_app_token():
    path_to_keys = os.path.join('config', 'socrata_chicago_keys.json')
    keys = read_json_to_dict(path_to_keys)
    return keys["app_token"]


def get_chicago_data_from_api(ID):
    token = "HkPf9JPzH4xwuY73nVnC5K3AQ"
    client = Socrata(ID, token)

    results = client.get("fwns-pcmk", limit=2000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    
    return results_df

    """
    data = requests.get(url)
    data_lst = data.json()
    headers = data_lst.pop(0)
    data_df = pd.DataFrame(data_lst, columns=headers)

    data_df = data_transformations.convert_df_dtypes(data_df)

    # rename columns
    data_df = data_df.rename(columns=var_to_colname_dict)
    """
