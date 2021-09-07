# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
##wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'ALL', 'value':'ALL'},
                                    {'label': 'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value':'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                ],
                                placeholder='Select a Launch Site here',
                                searchable=True,
                                value='ALL'
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0,
                                max=10000,
                                step=1000,
                                value=[min_payload,max_payload],
                                marks={
                                    0:'0 KG',
                                    2500: '2500 KG',
                                    5000: '5000 KG',
                                    7500: '7500 KG',
                                    10000: '10000 KG'
                                }
                                ),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def successPieChart(launchSite):
    fig = 0
    if launchSite=='ALL':
        successLaunches = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        successLaunches.rename(columns={'class':'Number of successful launches'},inplace=True)
        fig = px.pie(successLaunches, values='Number of successful launches', names='Launch Site', title='Total Success Launches by Site')
    else:
        sitedf = spacex_df[spacex_df['Launch Site']==launchSite]
        sitedf = sitedf.groupby('class')['Launch Site'].count().reset_index()
        sitedf.rename(columns={'class':'Success', 'Launch Site':'Number of launches'},inplace=True)
        title='Total Success Launches for site '+launchSite
        fig = px.pie(sitedf, values='Number of launches', names='Success', title=title)

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def successPayloadChart(launchSite,payLoadValue):
    low,high = payLoadValue
    fig = 0
    if launchSite=='ALL':
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(spacex_df[mask], x="Payload Mass (kg)", y="class", color="Booster Version Category",
        title='Connection between Payload and Success for all Sites')
    else:
        sitedf = spacex_df[spacex_df['Launch Site']==launchSite]
        mask = (sitedf['Payload Mass (kg)'] > low) & (sitedf['Payload Mass (kg)'] < high)
        title='Connection between Payload and Success for '+launchSite
        fig = px.scatter(sitedf[mask], x="Payload Mass (kg)", y="class", color="Booster Version Category", title=title)

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
