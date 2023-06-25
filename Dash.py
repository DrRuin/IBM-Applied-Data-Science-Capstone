# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("D:\\Users\\Chait\\Downloads\\IBM\\SpaceX\\spacex_launch_dash.csv")
payload_range = [spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
sites = ['All Sites', *spacex_df['Launch Site'].unique().tolist()]
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site-dropdown', options=[{'label': i, 'value': i} for i in sites], placeholder="Select a Launch Site here", value='All Sites', searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, value=payload_range, marks={0: '0 kg', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(Output('success-pie-chart', 'figure'), Input('site-dropdown', 'value'))
def get_pie(value):
    df = spacex_df if value == 'All Sites' else spacex_df[spacex_df['Launch Site'] == value].groupby(['Launch Site', 'class']).size().reset_index(name='class count')
    return px.pie(df, values=('class' if value == 'All Sites' else 'class count'), names=('Launch Site' if value == 'All Sites' else 'class'), title=f"Total Success Launches for site {(value if value != 'All Sites' else '')}")

@app.callback(Output('success-payload-scatter-chart', 'figure'), [Input('site-dropdown', 'value'), Input('payload-slider', 'value')])
def get_scatter(value1,value2):
    df = spacex_df[(spacex_df['Payload Mass (kg)'] > value2[0]) & (spacex_df['Payload Mass (kg)'] < value2[1])]
    df = df if value1=='All Sites' else df[df['Launch Site']==value1]
    return px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title=f"Correlation between Payload and Success for site {value1}")

if __name__ == '__main__':
    app.run_server()
