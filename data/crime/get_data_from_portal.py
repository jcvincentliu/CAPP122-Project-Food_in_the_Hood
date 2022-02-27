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

"""
Chicago poverty and crime: "fwns-pcmk"
https://data.cityofchicago.org/Health-Human-Services/Chicago-poverty-and-crime/fwns-pcmk

Chicago Population Counts: "85cm-7uqa"
https://data.cityofchicago.org/Health-Human-Services/Chicago-Population-Counts/85cm-7uqa

Crimes - 2001 to present -
https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present-Dashboard/5cd6-ry5g


"""

crime_dic = {"crime_2019":"w98m-zvie",
            "crime_2018":"3i3m-jwuy",
            "crime_2017":"d62x-nvdr",
            "crime_2016":"kf95-mnd6",
            "crime_2015":"vwwp-7yr9",
            "crime_2014":"qnmj-8ku6"}

test_dic = {"crime_2020":"qzdf-xmn8",
            "crime_2019":"w98m-zvie"}


def get_chicago_data_portal():
    """
    
    """
    token = "HkPf9JPzH4xwuY73nVnC5K3AQ"
    client = Socrata("data.cityofchicago.org", token)

    results = client.get("85cm-7uqa")
    results_df = pd.DataFrame.from_records(results)

    results_df.to_csv('chicago_population.csv', index=False)


def get_crime_data():
    token = "HkPf9JPzH4xwuY73nVnC5K3AQ"
    client = Socrata("data.cityofchicago.org", token)

    for year, id in crime_dic.items():
        results = client.get(id, limit=1000000)
        df = pd.DataFrame.from_records(results)
        df_col = df[['id','community_area','year']]
        num_crime = df_col.groupby(['community_area','year']).size().reset_index()
        num_crime.to_csv(f'{year}.csv', index=False)
    
    df = concatenate_csv()
    df.to_csv('total_crime.csv', index=False)


def concatenate_csv():
    df = pd.read_csv('crime_2019.csv')
    for year, id in crime_dic.items():
        if year != 'crime_2019':
            next_df = pd.read_csv(f'{year}.csv')
            df = pd.concat([df,next_df],axis=0)
    return df







