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


#Chicago poverty and crime: "fwns-pcmk"
#https://data.cityofchicago.org/Health-Human-Services/Chicago-poverty-and-crime/fwns-pcmk
#
#Chicago Population Counts: "85cm-7uqa"
#https://data.cityofchicago.org/Health-Human-Services/Chicago-Population-Counts/85cm-7uqa
#
#Crimes - 2001 to present -
#https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present-Dashboard/5cd6-ry5g


def get_chicago_data_from_api():
    """
    
    """
    token = "HkPf9JPzH4xwuY73nVnC5K3AQ"
    client = Socrata("data.cityofchicago.org", token)

    results = client.get("85cm-7uqa", limit=2000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    results_df.to_csv('chicago_population.csv', index=False)

"""
###### sandobox #######
data = requests.get(url)
data_lst = data.json()
headers = data_lst.pop(0)
data_df = pd.DataFrame(data_lst, columns=headers)

data_df = data_transformations.convert_df_dtypes(data_df)

# rename columns
data_df = data_df.rename(columns=var_to_colname_dict)

def read_json_to_dict(file_path):
    with open(file_path) as f:
        data_dict = json.load(f)
    return data_dict

def get_app_token():
    path_to_keys = os.path.join('config', 'socrata_chicago_keys.json')
    keys = read_json_to_dict(path_to_keys)
    return keys["app_token"]
"""
