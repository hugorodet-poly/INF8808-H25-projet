import dash
from dash import html, dcc, callback, Input, Output
from dash.dependencies import State
import plotly.graph_objects as go
import pandas as pd
import os

# Add import for callback_context
from dash import callback_context

from src.maps import get_map, get_districts_mapdata, get_boroughs_mapdata, get_countries_mapdata, circo_subsets, get_countries_of_origin
from src.preprocess import get_demographics_data, get_elections_data, get_boroughs_data
from src.viz_guillaume import stacked_bar_chart_most, stacked_bar_chart_least, immigrants_map, linguistic_map
from src.viz_hugo import get_montreal_boroughs_map
# Import Sidney's visualizations
from src.viz_sid import get_quebec_waffle_chart, get_montreal_waffle_chart, get_hypothetical_waffle_chart
from src.viz_sid import get_immigrant_voting_scatter, get_party_income_relation

from src.viz_countries import get_countries_of_origin_map

# Load the data
demographics_data = get_demographics_data()
borough_df = get_boroughs_data()
districts_mapdata = get_districts_mapdata()
montreal_boroughs_mapdata = get_boroughs_mapdata()
world_mapdata = get_countries_mapdata()

# Initialize the Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    assets_folder='assets',
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
app.title = 'Electoral Demographics Analysis'

# Define the app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Electoral Demographics Analysis Dashboard'),
        html.P('Interactive visualization of demographics and electoral patterns in Montreal and Quebec')
    ], className='dashboard-header'),
    
    # Main container
    html.Div([
        # Tab navigation
        dcc.Tabs(
            id='tabs', 
            value='tab-1', 
            children=[
                dcc.Tab(label='Immigration Map', value='tab-1', className='tab', selected_className='tab--selected'),
                dcc.Tab(label='Language Distribution', value='tab-2', className='tab', selected_className='tab--selected'),
                dcc.Tab(label='Electoral Representation', value='tab-3', className='tab', selected_className='tab--selected'),
                dcc.Tab(label='World Immigration Origins', value='tab-4', className='tab', selected_className='tab--selected'),
                dcc.Tab(label='Voting Patterns', value='tab-5', className='tab', selected_className='tab--selected'),
            ],
            className='custom-tabs'
        ),
        
        # Loading component for tab content
        dcc.Loading(
            id="loading-tabs",
            type="circle",
            children=[html.Div(id='tabs-content')],
            className='loading-container'
        )
    ], className='dashboard-container')
], style={'fontFamily': 'Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif'})

# Define callback to update tab content
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def update_tab(selected_tab):
    if selected_tab == 'tab-1':
        # Immigration Map - Montreal
        fig = immigrants_map()
        return html.Div([
            html.Div([
                html.H3('Immigration Distribution in Montreal'),
                html.P('This map shows the percentage of immigrants across different electoral districts in Montreal.')
            ], className='card'),
            html.Div([
                dcc.Graph(figure=fig, className='graph')
            ], className='graph-container card')
        ])
    
    elif selected_tab == 'tab-2':
        # Linguistic Map - Montreal
        fig = linguistic_map()
        return html.Div([
            html.Div([
                html.H3('Language Distribution in Montreal'),
                html.P('This map shows the percentage of people who speak neither English nor French across Montreal electoral districts.')
            ], className='card'),
            html.Div([
                dcc.Graph(figure=fig, className='graph')
            ], className='graph-container card')
        ])
    
    elif selected_tab == 'tab-3':
        # Electoral Representation - Sidney's Visualizations
        fig_quebec = get_quebec_waffle_chart()
        fig_montreal = get_montreal_waffle_chart()
        fig_hypothetical = get_hypothetical_waffle_chart()
        fig_immigrant_voting = get_immigrant_voting_scatter()
        fig_party_income = get_party_income_relation('Q.S.')
        
        return html.Div([
            html.Div([
                html.H3('Electoral Representation Analysis'),
                html.P('These visualizations analyze electoral representation in Quebec and Montreal, showing the relationship between demographics and voting patterns.')
            ], className='card'),
            html.Div([
                html.Div([
                    html.H4('Quebec Electoral Representation'),
                    html.P('Distribution of seats in the Quebec National Assembly (2022 election).')
                ], className='card'),
                html.Div([
                    dcc.Graph(figure=fig_quebec, className='graph')
                ], className='graph-container card')
            ]),
            html.Div([
                html.Div([
                    html.H4('Montreal Electoral Representation'),
                    html.P('Distribution of seats in Montreal electoral districts (2022 election).')
                ], className='card'),
                html.Div([
                    dcc.Graph(figure=fig_montreal, className='graph')
                ], className='graph-container card')
            ]),
            html.Div([
                html.Div([
                    html.H4('Hypothetical Electoral Scenario'),
                    html.P('What if Montreal voting patterns applied to all of Quebec?')
                ], className='card'),
                html.Div([
                    dcc.Graph(figure=fig_hypothetical, className='graph')
                ], className='graph-container card')
            ]),
            html.Div([
                html.Div([
                    html.H4('Immigration and Voter Participation'),
                    html.P('Correlation between immigration rates and voter turnout.')
                ], className='card'),
                html.Div([
                    dcc.Graph(figure=fig_immigrant_voting, className='graph')
                ], className='graph-container card')
            ]),
            html.Div([
                html.Div([
                    html.H4('Party Support by Income Level'),
                    html.P('Relationship between median household income and voting patterns.')
                ], className='card'),
                html.Div([
                    html.H5('Select Political Party:'),
                    dcc.Dropdown(
                        id='party-dropdown',
                        options=[
                            {'label': 'Québec Solidaire', 'value': 'Q.S.'},
                            {'label': 'Parti Libéral du Québec', 'value': 'P.L.Q./Q.L.P.'},
                            {'label': 'Coalition Avenir Québec', 'value': 'C.A.Q.-E.F.L.'},
                            {'label': 'Parti Québécois', 'value': 'P.Q.'}
                        ],
                        value='Q.S.',
                        className='custom-dropdown'
                    )
                ], className='card'),
                html.Div(id='income-chart-container', className='graph-container card')
            ])
        ])
    
    elif selected_tab == 'tab-4':
        # World Immigration Origins Map
        fig = get_countries_of_origin_map('Ville de Montréal')  # Default to "Ville de Montréal"
        return html.Div([
            html.Div([
                html.H3('Countries of Origin'),
                html.P('This map shows the countries of origin for immigrants in Montreal boroughs. Select a borough from the dropdown menu or click on a borough in the "Montreal Boroughs" tab.')
            ], className='card'),
            html.Div([
                dcc.Dropdown(
                    id='borough-dropdown',
                    options=[{'label': borough, 'value': borough} for borough in borough_df['Arrondissement'].unique() if borough is not None],
                    value='Ville de Montréal',
                    className='custom-dropdown'
                )
            ], className='card'),
            html.Div([
                dcc.Graph(id='world-map', figure=fig, className='graph')
            ], className='graph-container card')
        ])
    
    elif selected_tab == 'tab-5':
        # Voting Patterns - Stacked Bar Charts (automatically generated)
        fig_most = stacked_bar_chart_most()
        fig_least = stacked_bar_chart_least()
        
        return html.Div([
            html.Div([
                html.H3('Voting Patterns by Immigration Level'),
                html.P('These charts show voting patterns in electoral districts with highest and lowest immigration levels.')
            ], className='card'),
            html.Div([
                html.Div([
                    html.H4('Districts with Highest Immigration Levels'),
                ], className='card'),
                html.Div([
                    dcc.Graph(figure=fig_most, className='graph')
                ], className='graph-container card')
            ]),
            html.Div([
                html.Div([
                    html.H4('Districts with Lowest Immigration Levels'),
                ], className='card'),
                html.Div([
                    dcc.Graph(figure=fig_least, className='graph')
                ], className='graph-container card')
            ])
        ])

# Callback for Montreal borough details
@app.callback(
    Output('borough-details', 'children'),
    Input('montreal-map', 'clickData')
)
def display_borough_details(clickdata):
    if clickdata is None:
        return html.Div([
            html.H4('Borough Information'),
            html.P('Click on a borough on the map to see detailed information.')
        ])
    
    idx = clickdata['points'][0]['pointNumber']
    borough_name = montreal_boroughs_mapdata['features'][idx]['properties']['nom_arr']
    
    if borough_name is None:
        return html.Div([
            html.H4('No Data Available'),
            html.P('No information available for the selected area.')
        ])
    
    borough_data = borough_df[borough_df['Arrondissement'] == borough_name].iloc[0]
    
    return html.Div([
        html.H4(f'{borough_name}'),
        html.Div([
            html.P(f'Total Population: {borough_data["Population totale"]:,.0f}'),
            html.P(f'Immigrants: {borough_data["Immigrante"]:,.0f} ({borough_data["Immigrante"]/borough_data["Population totale"]*100:.1f}%)'),
            html.P(f'Non-immigrants: {borough_data["Non-immigrante"]:,.0f} ({borough_data["Non-immigrante"]/borough_data["Population totale"]*100:.1f}%)')
        ])
    ])

# Callback for World Map
@app.callback(
    Output('world-map', 'figure'),
    Input('borough-dropdown', 'value')
)
def update_countries_of_origin_map(borough_name):
    return get_countries_of_origin_map(borough_name)

# Callbacks for generating stacked bar charts
@app.callback(
    Output('stacked-most-container', 'children'),
    Input('generate-most-btn', 'n_clicks')
)
def generate_most_chart(n_clicks):
    if n_clicks is None:
        return html.P('Click the button to generate the chart.', className='card')
    
    fig = stacked_bar_chart_most()
    return html.Div([
        dcc.Graph(figure=fig, className='graph')
    ], className='graph-container card')

@app.callback(
    Output('stacked-least-container', 'children'),
    Input('generate-least-btn', 'n_clicks')
)
def generate_least_chart(n_clicks):
    if n_clicks is None:
        return html.P('Click the button to generate the chart.', className='card')
    
    fig = stacked_bar_chart_least()
    return html.Div([
        dcc.Graph(figure=fig, className='graph')
    ], className='graph-container card')

# Callback for party income relation chart
@app.callback(
    Output('income-chart-container', 'children'),
    Input('party-dropdown', 'value')
)
def update_party_income_chart(party):
    fig = get_party_income_relation(party)
    return dcc.Graph(figure=fig, className='graph')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)