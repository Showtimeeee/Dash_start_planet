import dash
#import dash_core_components as dcc
from dash import dcc
#import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
import requests
import pandas as pd
import plotly.express as px

# Kepler Project API
response = requests.get('http://asterank.com/api/kepler?query={}&limit=2000')
df = pd.json_normalize(response.json())
df = df[df['PER'] > 0]

# create star size category:
bins = [0, 0.8, 1.2, 100]
names = ['small', 'similar', 'bigger']
df['StarSize'] = pd.cut(df['RSTAR'], bins, labels=names)

option = []
for k in names:
    option.append({'label': k, 'value': k})

star_size_selector = dcc.Dropdown(
    id='star-selector',
    options=option,
    value=['small', 'similar'],
    multi=True
)

# RPLANET Radius planet
rplanet_selector = dcc.RangeSlider(
    id='range-slider',
    min=min(df['RPLANET']),
    max=max(df['RPLANET']),
    marks={5: '5', 10: '10', 20: '20'},
    step=1,
    value=[5, 50]
)


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('DashGraph'),
    html.Div('Select planet main semi-axis range'),
    html.Div(rplanet_selector,
             style={'width': '400px',
                    'margin-bottom': '40px'}),
    html.Div('Star Size'),
    html.Div(star_size_selector,
             style={'width': '400px',
                    'margin-bottom': '40px'}),
    html.Div('Planet Temperature ~ Distance from the Star'),
    dcc.Graph(id='dist-temp-chart')
],
    style={'margin-left': '80px',
           'margin-right': '80px'})


@app.callback(
    Output(component_id='dist-temp-chart', component_property='figure'),
    [Input(component_id='range-slider', component_property='value'),
     Input(component_id='star-selector', component_property='value')]
)
def update_dist_temp_chart(radius_range, star_size):
    chart_data = df[(df['RPLANET'] > radius_range[0]) &
                    (df['RPLANET'] < radius_range[1]) &
                    (df['StarSize'].isin(star_size))]
    fig = px.scatter(chart_data, x='TPLANET', y='A', color='ROW')

    return fig

# @app.callback(
#     Output(component_id='dist-temp', component_property='figure'),
#     Input(component_id='range', component_property='value'),)
# def update_dist_temp(radius):
#     chart_data = df[(df['RPLANET'] > radius) &
#                     (df['RPLANET'] < radius)]
#     fig = px.scatter(chart_data)
#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)




