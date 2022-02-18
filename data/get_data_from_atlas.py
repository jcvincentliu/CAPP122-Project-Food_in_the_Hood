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


