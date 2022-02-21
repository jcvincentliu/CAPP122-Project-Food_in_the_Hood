import requests
import pandas as pd

"""
Chicago Health Atlas API
{
    "Atlas": "https://chicagohealthatlas.org/api/v1/atlas/",
    "Topics": "https://chicagohealthatlas.org/api/v1/topics/",
    "Categories": "https://chicagohealthatlas.org/api/v1/categories/",
    "Data sources": "https://chicagohealthatlas.org/api/v1/sources/",
    "Stratifications": "https://chicagohealthatlas.org/api/v1/populations/",
    "Periods": "https://chicagohealthatlas.org/api/v1/periods/",
    "Geographic layers": "https://chicagohealthatlas.org/api/v1/layers/",
    "Geographies": "https://chicagohealthatlas.org/api/v1/geographies/",
    "Regions": "https://chicagohealthatlas.org/api/v1/regions/",
    "Data Coverage": "https://chicagohealthatlas.org/api/v1/coverage/",
    "Data": "https://chicagohealthatlas.org/api/v1/data/",
    "Colors": "https://chicagohealthatlas.org/api/v1/colors/",
    "Terms": "https://chicagohealthatlas.org/api/v1/terms/"
}

***sample queries***
#Retrieve the 2014-2018 Hispanic population for a full geographic layer
data = requests.get("https://chicagohealthatlas.org/api/v1/data/?topic=POP&population=H&period=2014-2018&layer=zip")
data.text

"""



def get_atlas(url):
    data = requests.get(url)
    data_lsts = data.json()
    headers = data_lsts.pop(0)
    data_df = pd.DataFrame(data_lsts, columns=headers)

    return data_df


def get_atlas_ver2():
    params = {"topic":"LFA", "population":"", "period":"2019", "layer":"zip"}
    url = "https://chicagohealthatlas.org/api/v1/data"
    data = requests.get(url, params=params)
    results = data.json()["results"]
    df = append_results(results)

    df.to_csv("atlas_result.csv")


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






