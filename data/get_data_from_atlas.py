import requests
import pandas as pd

"""

***sample queries***
#Retrieve the 2014-2018 Hispanic population for a full geographic layer
import requests
data = requests.get("https://chicagohealthatlas.org/api/v1/data/?topic=POP&population=H&period=2014-2018&layer=zip")
data.text

import get_data_from_atlas
url = "https://chicagohealthatlas.org/api/v1/data/?topic=POP&population=H&period=2014-2018&layer=zip"
data = get_data_from_atlas.get_atlas(url)
data
"""


def get_atlas_ver2():
    params = {"topic":"POP", "population":"", "period":"2014-2018", "layer":"neighborhood"}
    url = "https://chicagohealthatlas.org/api/v1/data"
    data = requests.get(url, params=params)
    results = data.json()["results"]
    df = append_results(results)

    df.to_csv("atlas_result.csv")


def get_atlas_population():
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
    for key in period_dic.keys():
        if key != 'POP2019':
            next_df = pd.read_csv(f'{key}.csv')
            df = pd.concat([df,next_df],axis=0)
    
    #Extracting specific rows and cleaning data
    df = df.loc[:,['geo_id_label','period','data_value']]
    df['geo_id_label'] = df['geo_id_label'].str.replace('1714000-','')
    df.to_csv('total_population.csv', index=False)


def append_results(results):
    cols = ['key', 'period', 'data_value', 'geo_layer', 'geo_id_label', 'population', 'std_error']
    df = pd.DataFrame(columns = cols)
    for result in results:
        key = result['a']
        period = result['d']
        data_value = result['v']
        geo_layer = result['l']
        geo_id_label = result['g']
        population = result['p']
        std_error = result['se']

        df = df.append({'key': key, 'period': period, 'data_value': data_value, 'geo_layer': geo_layer,
        'geo_id_label': geo_id_label, 'population': population, 'std_error': std_error}, ignore_index=True)
    
    return df

        
### Programs for getting keys  ###

def get_atlas_keys():
    base_url = "https://chicagohealthatlas.org/api/v1/topics/?offset="
    df_topic = get_df_topic(base_url)

    df_topic.to_csv("atlas_key_list.csv")


def get_df_topic(base_url):
    cols = ['name', 'key', 'description', 'units', 'format']
    df_topic = pd.DataFrame(columns = cols)

    for num in range(0,261,20):
        url = base_url + str(num)
        data = requests.get(url)
        results = data.json()["results"]

        for result in results:
            name = result['name']
            key = result['key']
            desc = result['description']
            units = result['units']
            r_format = result['format']
            series = pd.Series([name, key, desc, units, r_format], index=df_topic.columns)
            df_topic = df_topic.append(series, ignore_index=True)

    return df_topic


def concatenating_datasets():
    df_crime = pd.read_csv('crime/rolling_total_crime.csv')
    
    df_pop = pd.read_csv('total_population.csv')
    df_pop = df_pop.rename(columns={'period':'year'})
    df_pop = df_pop.rename(columns={'geo_id_label':'community_area'})
    df_pop = df_pop.rename(columns={'data_value':'population'})

    df_merge = pd.merge(df_crime,df_pop,on=['community_area','year'])

    df_merge['crime_rate'] = (df_merge['crime_num']/df_merge['population'])*10000

    df_merge.to_csv("food_and_hood_data.csv")
