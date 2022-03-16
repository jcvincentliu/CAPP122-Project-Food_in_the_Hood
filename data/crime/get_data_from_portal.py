"""
Functions for getting data from Chicago Data Portal

Ryoya Hashimoto
"""

import os
import requests
import json
import pandas as pd
from sodapy import Socrata

"""
This module gets the number of crimes by Chicago neighborhood from Chicago Data Portal.

Crimes - 2001 to present -
https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-present-Dashboard/5cd6-ry5g

A example of use:
import get_data_from_portal
get_data_from_portal.get_crime_data()
get_data_from_portal.getting_rolling_data()
"""


crime_dic = {"crime_2019":"w98m-zvie",
            "crime_2018":"3i3m-jwuy",
            "crime_2017":"d62x-nvdr",
            "crime_2016":"kf95-mnd6",
            "crime_2015":"vwwp-7yr9",
            "crime_2014":"qnmj-8ku6"}


def get_crime_data():
    """
    This function gets the number of crimes by neighborhood from Chicago Data Portal as csv file
    If you want data prior to 2014, you need to add the year and id in the 'crime_dic' dictionary.
    Be careful that the amount of data is really huge. 

    Input:
        Nothing
    
    Output:
        Nothing
    """
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
    """
    This is a helper function for get_crime_data function.
    This merges data coming from different years.

    Input:
        Nothing

    Outout:
        df (pandas dataframe): merged dataframe
    """
    df = pd.read_csv('crime_2019.csv')
    for year in crime_dic.keys():
        if year != 'crime_2019':
            next_df = pd.read_csv(f'{year}.csv')
            df = pd.concat([df,next_df],axis=0)
    return df


def getting_rolling_data():
    """
    To compare data from Chicago Data Atlas, this function creates average number of crimes 
    over 5 years as csv file.
    
    Input:
        Nothing
    
    Output:
        Nothing
    """
    df = pd.read_csv('total_crime.csv')
    df = df.rename(columns={'0':'crime_num'})

    #2015-2019
    df_2019 = df[df['year'] != 2019]
    df_2019 = df_2019.groupby(['community_area']).mean().reset_index()
    df_2019.loc[:,'year'] = '2015-2019'

    #2014-2018
    df_2018 = df[df['year'] != 2018]
    df_2018 = df_2019.groupby(['community_area']).mean().reset_index()
    df_2018.loc[:,'year'] = '2014-2018'

    #Concatenate two dataframes
    df_total = pd.concat([df_2019,df_2018],axis=0)
    df_total.to_csv('rolling_total_crime.csv', index=False)
