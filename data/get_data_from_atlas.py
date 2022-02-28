import requests
import pandas as pd


topics_dic = {"Low food access":"LFA",
"Neighborhood safety rate":"HCSNSP",
"Per capita income":"PCI"}


period_dic = {"2014-2018":"2014-2018",
              "2015":"2015",
              "2015-2017":"2015-2017",
              "2015-2019":"2015-2019",
              "2016-2018":"2016-2018",
              "2019":"2019"}


def get_atlas_ver2(topics_dic, period_dic):
    cols = ['key', 'period', 'data_value', 'geo_layer', 'geo_id_label', 'population', 'std_error']
    df = pd.DataFrame(columns = cols)
    for _, topic in topics_dic.items():
        for _, period in period_dic.items():
            params = {"topic":topic, "population":"", "period": period, "layer":"neighborhood"}
            url = "https://chicagohealthatlas.org/api/v1/data"
            data = requests.get(url, params=params)
            results = data.json()["results"]
            df_results = append_results(results)
            df = pd.concat([df, df_results], axis=0)
    df = post_processing(df)
    df.to_csv("atlas_result.csv")


def post_processing(df):
    key_name_dic =  create_key_name_dic()
    for _, row in df.iterrows():
        row_key = row['key']
        row['key'] = key_name_dic[row_key]

    df['geo_id_label'] = df['geo_id_label'].str.replace('1714000-','')
    df = df.loc[:, ['key','geo_id_label','period','data_value']]
    df_result = key_to_row(df)

    return df_result


def key_to_row(df):
    name_list = []
    for _, row in df.iterrows():
        name_list.append(row['key'])
    name_list = list(set(name_list))

    df_result = (
        df.groupby(['geo_id_label', 'period'])
        .apply(lambda x: x.set_index('key').reindex(name_list)['data_value'])
        .reset_index()
        .rename_axis(None, axis=1))
    
    return df_result


def create_key_name_dic():
    dic = {}
    key_name_list = pd.read_csv("atlas_key_list.csv")
    for _, row in key_name_list.iterrows():
        dic[row['key']] = row['name']
    return dic


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

    df_atlas = pd.read_csv('atlas_result.csv')
    df_atlas = df_atlas.rename(columns={'period':'year'})
    df_atlas = df_atlas.rename(columns={'geo_id_label':'community_area'})
    df_atlas = df_atlas.rename(columns={'data_value':'population'})

    df_concatenate = pd.merge(df_atlas, df_merge ,on=['community_area','year'], how='left')
    df_concatenate = df_concatenate.sort_values(['community_area', 'year'], ignore_index=True)

    df_concatenate.to_csv("food_and_hood_data.csv", index=False)
