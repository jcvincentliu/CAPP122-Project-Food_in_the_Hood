"""
Functions for getting data from Chicago Health Atlas

Takayuki Nitta, Ryoya Hashimoto
"""

import requests
import pandas as pd


def get_atlas_population():
    """
    This function gets the population data from Chicago Data Atlas.

    Input:
        Nothing

    Output:
        Nothing
    """
    period_dic = {"POP2019":"2015-2019",
                  "POP2018":"2014-2018"}

    for key, period in period_dic.items():
        params = {"topic":"POP", "population":"", "period":period, "layer":"neighborhood"}
        url = "https://chicagohealthatlas.org/api/v1/data"
        data = requests.get(url, params=params)
        results = data.json()["results"]
        df = append_results(results)
        df.to_csv(f'{key}.csv', index=False)

    df = pd.read_csv('POP2019.csv')
    for key in period_dic:
        if key != 'POP2019':
            next_df = pd.read_csv(f'{key}.csv')
            df = pd.concat([df,next_df],axis=0)

    #Extracting specific rows and cleaning data
    df = df.loc[:,['geo_id_label','period','data_value']]
    df['geo_id_label'] = df['geo_id_label'].str.replace('1714000-','')
    df.to_csv('total_population.csv', index=False)


def get_atlas_food():
    """
    This function get the data related to food insecurity from Chicago Health Atlas.

    Input:
        Nothing

    Output:
        Nothing
    """
    period_dic = {"HCSFVP":"2016-2018",
                  "HCSSP":"2016-2018",
                  "LFA":"2019",
                  "POV":"2015-2019"}

    for key, period in period_dic.items():
        params = {"topic":key, "population":"", "period":period, "layer":"neighborhood"}
        url = "https://chicagohealthatlas.org/api/v1/data"
        data = requests.get(url, params=params)
        results = data.json()["results"]
        df = append_results(results)

        df = df.loc[:,['geo_id_label','data_value']]
        if key == 'HCSFVP':
            df = df.rename(columns={'data_value': 'adult_fruit_and_vegetable_servings_rate'})
        elif key == 'HCSSP':
            df = df.rename(columns={'data_value': 'adult_soda_consumption_rate'})
        elif key == 'LFA':
            df = df.rename(columns={'data_value': 'low_food_access'})
        elif key == 'POV':
            df = df.rename(columns={'data_value': 'poverty_rate'})

        df['geo_id_label'] = df['geo_id_label'].str.replace('1714000-','')
        df = df.rename(columns={'geo_id_label': 'community_area'})
        df.to_csv(f'{key}.csv', index=False)

    df = pd.read_csv('HCSFVP.csv')
    for key in period_dic:
        if key != 'HCSFVP':
            df_next = pd.read_csv(f'{key}.csv')
            df = pd.merge(df, df_next ,on=['community_area'], how='left')

    #Merge crime rate
    df_crime = pd.read_csv('crime_rate.csv')
    df_crime = df_crime[df_crime['year'] == '2015-2019']
    df_crime = df_crime.loc[:,['community_area','crime_rate', 'population']]
    df = pd.merge(df, df_crime ,on=['community_area'], how='left')

    #Assign neighborhood name to neighborhood id
    df_name = pd.read_csv('poverty_and_crime.csv')
    df_name = df_name.loc[:,['community_area','community_area_name']]
    df = pd.merge(df, df_name ,on=['community_area'], how='left')

    df.to_csv('food_data.csv', index=False)


def concatenating_datasets():
    """
    This function merges two dataframes (rolling_total_crime.csv and total_population.csv)
    and create a new variable (crime_rate) as the number of all crimes per 10,000 people
    over the time period. A csv file is created as the result.

    Input:
        Nothing

    Output:
        Nothing
    """
    #Load data
    df_crime = pd.read_csv('crime/rolling_total_crime.csv')
    df_pop = pd.read_csv('total_population.csv')

    #Change column names
    df_pop = df_pop.rename(columns={'period':'year'})
    df_pop = df_pop.rename(columns={'geo_id_label':'community_area'})
    df_pop = df_pop.rename(columns={'data_value':'population'})

    #Merge two dataframes
    df_merge = pd.merge(df_crime,df_pop,on=['community_area','year'])

    #Calculating the crime rate: divide the number of crimes by the population
    #of the neighborhood, and then multiply 10,000.
    df_merge['crime_rate'] = (df_merge['crime_num']/df_merge['population'])*10000

    df_merge.to_csv("crime_rate.csv", index=False)


def append_results(results):
    """
    This function appends the result of a request for Chicago Health Atlas.

    Input:
        results: (list) List of requested results

    Output:
        df: (DataFrame) Value, period, ..etc corresponding the key (e.g. "POP")
            representing an indicator
    """
    #Create a dataframe and set columns
    cols = ['key', 'period', 'data_value', 'geo_layer', 'geo_id_label', 'population', 'std_error']
    df = pd.DataFrame(columns = cols)

    #Append a result of scraping
    for result in results:
        key = result['a']
        period = result['d']
        data_value = result['v']
        geo_layer = result['l']
        geo_id_label = result['g']
        population = result['p']
        std_error = result['se']

        df = df.append({'key': key, 'period': period, 'data_value': data_value,
            'geo_layer': geo_layer, 'geo_id_label': geo_id_label, 'population': population,
            'std_error': std_error}, ignore_index=True)

    return df


### Programs only for getting keys  ###
def get_atlas_keys():
    """
    This function creates the csv file "atlas_key_list.csv" which includes the name,
    key and description about an indicator.

    Input:
        Nothing

    Output:
        Nothing
    """
    base_url = "https://chicagohealthatlas.org/api/v1/topics/?offset="
    df_topic = get_df_topic(base_url)

    df_topic.to_csv("atlas_key_list.csv")


def get_df_topic(base_url):
    """
    This function creates a dataframe which includes the name, key and
    description about an indicator.

    Input:
        base_url: (str) Base url for scraping

    Output:
        df_topic: (DataFrame) a dataframe which includes the name,
        key and description about an indicator
    """
    #Create a dataframe and set columns
    cols = ['name', 'key', 'description', 'units', 'format']
    df_topic = pd.DataFrame(columns = cols)

    #Scrape by every 20 indicators
    for num in range(0,261,20):
        url = base_url + str(num)
        data = requests.get(url)
        results = data.json()["results"]

    #Append a result of scraping
        for result in results:
            name = result['name']
            key = result['key']
            desc = result['description']
            units = result['units']
            r_format = result['format']
            series = pd.Series([name, key, desc, units, r_format], index=df_topic.columns)
            df_topic = df_topic.append(series, ignore_index=True)

    return df_topic
