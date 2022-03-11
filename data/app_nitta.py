from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import geopandas as gpd
import pandas as pd
import json

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Choropleth by neighborhood'),
    html.P("Select an indicator:"),
    dcc.RadioItems(
        id='indicator', 
        options=["assault_homicide", "below_poverty_level", "unemployment"],
        value="unemployment",
        inline=True
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("indicator", "value"))

def display_choropleth(indicator):
    CENTER = {'lat': 41.8781, 'lon': -87.6298}
    chi2 = preprocess_choro('chicago_community_areas.geojson', 'poverty_and_crime.csv')
    fig = px.choropleth_mapbox(chi2, geojson=json.loads(chi2['geometry'].to_json()), 
        locations='community_area_ID', color=indicator,
        #title = 'unemployment rate',
        hover_name = 'community_area_name_x',
        color_continuous_scale="OrRd", 
        mapbox_style='white-bg',
        zoom=9, 
        center=CENTER,
        opacity=0.5,
        #labels={'unemployment':'unemp_rate'}
        )
    fig.update_geos(fitbounds="locations", visible=False)
    #fig.update_layout(margin={'r':20,'t':40,'l':20,'b':10,'pad':5})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def preprocess_choro(path_to_geojson, path_to_csv):
    chi = gpd.read_file(path_to_geojson)
    chi = chi.rename(columns={'area_num_1': 'community_area_ID', 'community' : 'community_area_name'})
    df = pd.read_csv(path_to_csv)
    df['community_area'] = df['community_area'].astype(str)
    df = df.rename(columns={'community_area': 'community_area_ID'})
    df['community_area_name'] = df['community_area_name'].str.upper()
    chi2 = pd.merge(chi, df, on=['community_area_ID'])
    chi2.set_index('community_area_ID', drop=False, inplace=True)
    
    return chi2

app.run_server(debug=True)