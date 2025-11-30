# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# ----------------------------
# APP LAYOUT
# ----------------------------
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),

    # ----------------------------
    # TASK 1: Launch Site Dropdown
    # ----------------------------
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # ----------------------------
    # TASK 2: Pie Chart
    # ----------------------------
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # ----------------------------
    # TASK 3: Payload RangeSlider
    # ----------------------------
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000',
               5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # ----------------------------
    # TASK 4: Scatter Plot
    # ----------------------------
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# ----------------------------
# TASK 2: Pie Chart Callback
# ----------------------------
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Show total success launches for all sites
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Success Launches by Site'
        )
    else:
        # Show success vs failure for selected site
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        counts = site_df['class'].value_counts().reset_index()
        counts.columns = ['class', 'count']
        fig = px.pie(
            counts,
            names='class',
            values='count',
            title=f'Success vs Failure for site {entered_site}'
        )
    return fig


# ----------------------------
# TASK 4: Scatter Plot Callback
# ----------------------------
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_plot(entered_site, payload_range):
    low, high = payload_range
    # Filter by payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                            (spacex_df['Payload Mass (kg)'] <= high)]

    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Outcome for All Sites',
            hover_data=['Launch Site']
        )
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Outcome for site {entered_site}',
            hover_data=['Launch Site']
        )
    return fig


# ----------------------------
# Run the app
# ----------------------------
if __name__ == '__main__':
    app.run()

