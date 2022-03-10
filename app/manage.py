import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff

neighborhood_dic = {}

df = pd.read_csv('../data/food_data.csv')
vars = [var for var in df.columns if var != 'community_area']
vars_neighborhood = [var for var in df.columns if var != 'community_area']

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

sidebar = html.Div(
    [
        dbc.Row(
            [
                html.H5('Settings',
                        style={'margin-top': '12px', 'margin-left': '24px'})
                ],
            style={"height": "5vh"},
            className='bg-primary text-white font-italic'
            ),
        dbc.Row(
            [
                html.Div([
                    html.P('Variablea',
                           style={'margin-top': '8px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='my-cat-picker', multi=False, value='cat0',
                                 options=[{'label': x, 'value': x}
                                          for x in vars],
                                 style={'width': '320px'}
                                 ),
                    html.P('Neighborhood',
                           style={'margin-top': '16px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='my-cont-picker', multi=False, value='cont0',
                                 options=[{'label': x, 'value': x}
                                          for x in range(78)],
                                 style={'width': '320px'}
                                 ),
                    html.P('Variables for Correlation Matrix',
                           style={'margin-top': '16px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='my-corr-picker', multi=True,
                                 value=vars,
                                 options=[{'label': x, 'value': x}
                                          for x in vars],
                                 style={'width': '320px'}
                                 ),
                    html.Button(id='my-button', n_clicks=0, children='apply',
                                style={'margin-top': '16px'},
                                className='bg-dark text-white'),
                    html.Hr()
                    ]
                    )
                ],
            style={'height': '50vh', 'margin': '8px'}),
        dbc.Row(
            [
                html.P('Target Variables', className='font-weight-bold')
                ],
            style={"height": "45vh", 'margin': '8px'}
            )
        ]
    )

content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Distribution of Variables',
                               className='font-weight-bold'),
                        ]),
                dbc.Col(
                    [
                        html.P('Geographical Distribution',
                               className='font-weight-bold')
                    ])
            ],
            style={'height': '50vh',
                   'margin-top': '16px', 'margin-left': '8px',
                   'margin-bottom': '8px', 'margin-right': '8px'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Correlation Matrix Heatmap',
                               className='font-weight-bold')
                    ])
            ],
            style={'height': '50vh', 'margin': '8px'}
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


if __name__ == "__main__":
    app.run_server(debug=True)