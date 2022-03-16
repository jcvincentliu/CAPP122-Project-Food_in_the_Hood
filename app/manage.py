"""
Application for Dash Visualization

Ryoya Hashimoto, Takayuki Nitta
"""
import json
import dash
from matplotlib.pyplot import figure
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
import geopandas as gpd
from dash.dependencies import Input, Output, State


df = pd.read_csv('../data/food_data.csv')
vars = [var for var in df.columns if not var in ['community_area','community_area_name']]
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

name_dic = {'adult_fruit_and_vegetable_servings_rate':'Adult fruit and vegetable servings rate (%)',
        'adult_soda_consumption_rate':'Adult soda consumption rate (%)',
        'low_food_access':'Low food access (%)',
        'poverty_rate':'Poverty rate (%)',
        'crime_rate':'Crime rate',
        'population':'Population'}

dic = {'adult_fruit_and_vegetable_servings_rate':'Percent of adults who reported \
            eating five or more servings of fruits and vegetables (combined) daily.',
        'adult_soda_consumption_rate':'Percent of adults who drank soda or pop or other \
            sweetened drinks like sweetened iced tea, sports drinks, fruit punch or other \
            fruit-flavored drinks at least once per day in the past month.',
        'low_food_access':'Percent of residents who have low access to food, defined solely \
            by distance: further than 1/2 mile from the nearest supermarket in an urban area, \
            or further than 10 miles in a rural area.',
        'poverty_rate':'Percent of residents in families that are in poverty \
            (below the Federal Poverty Level).',
        'crime_rate':'The number of all crimes per 10,000 people over the time period',
        'population':'Average population over the time period.'}

# Heatmap
corr_pick = vars
df_corr = df[corr_pick].corr()
x = list(df_corr.columns)
y = list(df_corr.index)
z = df_corr.values

fig_corr = ff.create_annotated_heatmap(
    z,
    x=x,
    y=y,
    annotation_text=np.around(z, decimals=2),
    hoverinfo='z',
    colorscale='Blues'
)
fig_corr.update_layout(width=1040,
                       height=300,
                       margin=dict(l=40, r=20, t=20, b=20),
                       paper_bgcolor='rgba(0,0,0,0)'
                       )

#Create left sidebar 
sidebar = html.Div(
    [
        dbc.Row(
            [
                html.H5('All food in the Neighborhood',
                        style={'margin-top': '12px', 'margin-left': '24px'})
                ],
            style={"height": "10vh"},
            className='bg-primary text-white font-italic'
            ),
        dbc.Row(
            [
                html.Div([
                    html.P('Variables',
                           style={'margin-top': '8px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='catpick', multi=False,
                                 value='adult_fruit_and_vegetable_servings_rate',
                                 options=[{'label': x, 'value':x}
                                          for x in vars],
                                 style={'width': '200px'}
                                 ),
                    html.Button(id='my-button', n_clicks=0, children='apply',
                                style={'margin-top': '16px'},
                                className='bg-dark text-white'),
                    html.Hr()
                    ]
                    )
                ],
            style={'height': '30vh', 'margin': '8px'}),
        dbc.Row(
            [
                html.P('What is the variable?'),
                html.P(id='explanation',
                        className='font-weight-bold')
                ],
            style={"height": "40vh"}
            )
        ]
    )

#Create content (right side of dashboard)
content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(id='bar-title',
                                className='font-weight-bold'),
                        dcc.Graph(id="bar-chart",
                                className='bg-light')])
            ],
            style={'height': '50vh'}),
        dbc.Row(
            [
                dbc.Col([
                    html.P('Choropleth Map',
                        className='font-weight-bold'),
                        dcc.Graph(id="choropleth",
                                className='bg-light')])
            ],
            style={'height': '80vh', 'margin': '8px'}),
        dbc.Row(
            [
                dbc.Col([
                    html.P('Correlation Matrix Heatmap',
                        className='font-weight-bold'),
                    dcc.Graph(id='corr_chart',
                        figure=fig_corr,
                        className='bg-light')])
            ],
            style={'height': '50vh'}
            )
        ]
    )

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9)
                ]
            ),
        ],
    fluid=True
    )

# Definition of variables
@app.callback(Output("explanation", 'children'),
              Input('my-button', 'n_clicks'),
              State('catpick', 'value'))

def update_explanation(n_clicks, cat_pick):
    """
    This function updates the explanation on the side bar of our dashboard.

    Input:
        n_clicks: (int) Takes 1 if user clicks the apply button otherwise 0
        catpick: (list) List of strings where strings represent variable names,
        e.g. "low_food_access"
    
    Output:
        explanation: (str) Description of selected variable
    """
    explanation = dic[cat_pick]
    return explanation


# Bar Chart
@app.callback(Output('bar-chart', 'figure'),
              Output('bar-title', 'children'),
              Input('my-button', 'n_clicks'),
              State('catpick', 'value'))

def update_bar(n_clicks, cat_pick):
    """
    This function updates the bar chart on the dashboard

    Input:
        n_clicks: (int) Takes a value of 1 if user clicks the apply button,
        and 0 otherwise
        catpick: (list) List of strings where strings represent variable names,
        e.g. "low_food_access"
    
    Output:
        fig_bar: (figure object) Bar chart which shows the level of selected variable
        by neighborhood
        title_bar: (str) Title of the Bar chart
    """
    df_bar = df[cat_pick]
    fig_bar = go.Figure(data=[
        go.Bar(name=cat_pick,
            x=df['community_area_name'],
            y=df_bar.values,
            marker=dict(color='#bad6eb'))])

    fig_bar.update_layout(
        width=1500,
        height=250,
        xaxis={'categoryorder':'total descending'},
        xaxis_tickangle=-45,
        margin=dict(l=40, r=20, t=20, b=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    title_bar = 'Bar chart: ' + name_dic[cat_pick]

    return fig_bar, title_bar

# Choropleth Map
@app.callback(Output("choropleth", 'figure'),
              Input('my-button', 'n_clicks'),
              State('catpick', 'value'))


def display_choropleth(n_clicks, catpick):
    """
    This function creates a choropleth map of Chicago.

    Input:
        n_clicks: (int) Takes a value of 1 if user clicks the apply button,
        and 0 otherwise
        catpick: (list) List of strings where strings represent variable names,
        e.g. "low_food_access"

    Output:
        fig: (figure object) Choropleth map of Chicago
    """
    #Set center latitude and longitude of the map
    CENTER = {'lat': 41.8781, 'lon': -87.6298}

    #Combine the main data and Chicago geographic data
    chi2 = preprocess_choro('../data/chicago_community_areas.geojson', '../data/food_data.csv')

    #Create a choropleth map
    fig = px.choropleth_mapbox(chi2, geojson=json.loads(chi2['geometry'].to_json()),
        locations='community_area_ID', color= catpick,
        labels = name_dic,
        hover_name = 'community_area_name_x',
        color_continuous_scale="OrRd",
        mapbox_style='white-bg',
        zoom=9,
        center=CENTER,
        opacity=0.5,
        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def preprocess_choro(path_to_geojson, path_to_csv):
    """
    This function combines the main data and Chicago geographic data.

    Input:
        path_to_geojson: (str) File path to Chicago geojson file
        path_to_csv: (str) File path to food_data.csv file

    Output:
        chi2: (dataframe) Dataframe which contains the main data and Chicago geographic data
    """
    #Read Chicago geojson file
    chi = gpd.read_file(path_to_geojson)

    #Preprocess the geojson file for merge
    chi = chi.rename(columns={'area_num_1': 'community_area_ID', \
        'community' : 'community_area_name'})

    #Read food_data.csv
    df = pd.read_csv(path_to_csv)
    df['community_area'] = df['community_area'].astype(str)

    #Preprocess the dataframe for merge
    df = df.rename(columns={'community_area': 'community_area_ID'})
    df['community_area_name'] = df['community_area_name'].str.upper()

    #Merge geojson and food_data.csv
    chi2 = pd.merge(chi, df, on=['community_area_ID'])

    #Set index in order to match community area ID
    chi2.set_index('community_area_ID', drop=False, inplace=True)

    return chi2


if __name__ == "__main__":
    app.run_server(host='127.0.0.1',port=8500)
