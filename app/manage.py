import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash.dependencies import Input, Output, State


df = pd.read_csv('../data/food_data.csv')
vars = [var for var in df.columns if var != 'community_area']
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

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


sidebar = html.Div(
    [
        dbc.Row(
            [
                html.H5('Food insecurity',
                        style={'margin-top': '12px', 'margin-left': '24px'})
                ],
            style={"height": "5vh"},
            className='bg-primary text-white font-italic'
            ),
        dbc.Row(
            [
                html.Div([
                    html.P('Variables',
                           style={'margin-top': '8px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='my-cat-picker', multi=False, value='adult_fruit_and_vegetable_servings_rate',
                                 options=[{'label': x, 'value':x}
                                          for x in vars],
                                 style={'width': '220px'}
                                 ),
                    html.Button(id='my-button', n_clicks=0, children='apply',
                                style={'margin-top': '16px'},
                                className='bg-dark text-white'),
                    html.Hr()
                    ]
                    )
                ],
            style={'height': '50vh', 'margin': '8px'})
        ]
    )

content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(id='bar-title',
                                #children='Distribution of Variables',
                                className='font-weight-bold'),
                        dcc.Graph(id="bar-chart",
                                #figure=fig_bar,
                                className='bg-light')])
            ],
            style={'height': '50vh',
                   'margin-top': '16px', 'margin-left': '8px',
                   'margin-bottom': '8px', 'margin-right': '8px'}),
        dbc.Row(
            [
                dbc.Col([
                    html.P('Correlation Matrix Heatmap',
                        className='font-weight-bold'),
                    dcc.Graph(id='corr_chart',
                        figure=fig_corr,
                        className='bg-light')])
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


# Bar Chart
@app.callback(Output('bar-chart', 'figure'),
              Output('bar-title', 'children'),
              Input('my-button', 'n_clicks'),
              State('my-cat-picker', 'value'))

def update_bar(n_clicks, cat_pick):
    df_bar = df[cat_pick]
    fig_bar = go.Figure(data=[
        go.Bar(name=cat_pick,
            x=df['community_area_name'],
            y=df_bar.values,
            marker=dict(color='#bad6eb'))])

    fig_bar.update_layout(
        width=1500,
        height=250,
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
    title_bar = 'Distribution of Categorical Variable: ' + cat_pick

    return fig_bar, title_bar


if __name__ == "__main__":
    app.run_server(host='127.0.0.1',port=8700)