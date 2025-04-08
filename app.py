import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Import your custom modules
from src.maps import get_districts_mapdata, get_boroughs_mapdata, get_countries_mapdata
from src.preprocess import get_demographics_data, get_elections_data, get_boroughs_data
from src.viz_guillaume import stacked_bar_chart_most, stacked_bar_chart_least, immigrants_map, linguistic_map
from src.viz_hugo import get_montreal_boroughs_map
# Import Sidney's visualizations
from src.viz_sid import get_quebec_waffle_chart, get_montreal_waffle_chart, get_hypothetical_waffle_chart
from src.viz_sid import get_immigrant_voting_scatter, get_party_income_relation
from src.viz_countries import get_countries_of_origin_map

# ---------- Data Loading -------------
demographics_data = get_demographics_data()
borough_df = get_boroughs_data()
districts_mapdata = get_districts_mapdata()
montreal_boroughs_mapdata = get_boroughs_mapdata()
world_mapdata = get_countries_mapdata()

# ---------- Pre-generate Figures -----
immigrants_map_fig = immigrants_map()
linguistic_map_fig = linguistic_map()
fig_quebec = get_quebec_waffle_chart()
fig_montreal = get_montreal_waffle_chart()
fig_hypothetical = get_hypothetical_waffle_chart()
fig_immigrant_voting = get_immigrant_voting_scatter()
fig_most = stacked_bar_chart_most()
fig_least = stacked_bar_chart_least()
default_world_map_fig = get_countries_of_origin_map('Ville de Montréal')

# ---------- Dash App Setup -----------
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    assets_folder='assets',
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
app.title = 'Electoral Demographics Analysis'

# ---------- Layout --------------------
app.layout = html.Div([

    # Floating Navbar
    html.Nav([
        html.Div([
            # Left side: Dashboard Title / Branding
            html.Div("Demographics Dashboard", className="navbar-brand"),
            
            # Right side: Any extra nav links or placeholders
            html.Div([
                html.A("Home", href="#", className="nav-link"),
                html.A("Contact", href="#", className="nav-link")
            ], className="nav-right")
        ], className="navbar-container")
    ], className="navbar"),

    # Header
    html.Header([
        html.H1('Electoral Demographics Analysis'),
        html.P('Interactive visualization of demographics and electoral patterns in Montreal and Quebec')
    ], className='hero-header'),

    # Main container
    html.Div([
        # 1. Immigration Map (Montreal)
        html.Div([
            html.H2('Immigration Distribution in Montreal', className='section-title'),
            html.P('This map shows the percentage of immigrants across different electoral districts in Montreal.'),
            dcc.Graph(figure=immigrants_map_fig, className='graph')
        ], className='card'),

        html.Hr(className='section-divider'),

        # 2. Language Distribution (Montreal)
        html.Div([
            html.H2('Language Distribution in Montreal', className='section-title'),
            html.P('This map shows the percentage of people who speak neither English nor French across Montreal electoral districts.'),
            dcc.Graph(figure=linguistic_map_fig, className='graph')
        ], className='card'),

        html.Hr(className='section-divider'),

        # 3. Electoral Representation
        html.Div([
            html.H2('Electoral Representation Analysis', className='section-title'),
            html.P('Visualizations analyzing electoral representation in Quebec and Montreal, showing relationships between demographics and voting patterns.'),
            
            # Example of a flex row with two columns
            html.Div([
                # Quebec Waffle
                html.Div([
                    html.H3('Quebec Electoral Representation'),
                    html.P('Distribution of seats in the Quebec National Assembly (2022 election).'),
                    dcc.Graph(figure=fig_quebec, className='graph')
                ], className='card flex-child'),

                # Montreal Waffle
                html.Div([
                    html.H3('Montreal Electoral Representation'),
                    html.P('Distribution of seats in Montreal electoral districts (2022 election).'),
                    dcc.Graph(figure=fig_montreal, className='graph')
                ], className='card flex-child'),

            ], className='flex-row'),

            # Another row for the next two
            html.Div([
                # Hypothetical
                html.Div([
                    html.H3('Hypothetical Electoral Scenario'),
                    html.P('What if Montreal voting patterns applied to all of Quebec?'),
                    dcc.Graph(figure=fig_hypothetical, className='graph')
                ], className='card flex-child'),

                # Immigration & Voter Participation
                html.Div([
                    html.H3('Immigration and Voter Participation'),
                    html.P('Correlation between immigration rates and voter turnout.'),
                    dcc.Graph(figure=fig_immigrant_voting, className='graph')
                ], className='card flex-child'),
            ], className='flex-row'),

            # 3.5 Party Support by Income
            html.Div([
                html.H3('Party Support by Income Level'),
                html.P('Relationship between median household income and voting patterns.'),
                
                html.Div([
                    html.H4('Select Political Party:'),
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

                html.Div(
                    id='income-chart-container',
                    className='graph-container card'
                )
            ], className='card'),
        ], className='card'),

        html.Hr(className='section-divider'),

        # 4. World Immigration Origins
        html.Div([
            html.H2('Countries of Origin', className='section-title'),
            html.P('This map shows the countries of origin for immigrants in Montreal boroughs. Select a borough from the dropdown menu below.'),
            
            dcc.Dropdown(
                id='borough-dropdown',
                options=[{'label': b, 'value': b} for b in borough_df['Arrondissement'].unique() if b],
                value='Ville de Montréal',
                className='custom-dropdown'
            ),
            dcc.Graph(id='world-map', figure=default_world_map_fig, className='graph')
        ], className='card'),

        html.Hr(className='section-divider'),

        # 5. Voting Patterns (Stacked Bar)
        html.Div([
            html.H2('Voting Patterns by Immigration Level', className='section-title'),
            html.P('Charts showing voting patterns in electoral districts with the highest and lowest immigration levels.'),

            html.Div([
                html.H3('Districts with Highest Immigration Levels'),
                dcc.Graph(figure=fig_most, className='graph')
            ], className='card'),

            html.Div([
                html.H3('Districts with Lowest Immigration Levels'),
                dcc.Graph(figure=fig_least, className='graph')
            ], className='card')
        ], className='card'),
    ], className='dashboard-container'),

    # Footer
    html.Footer([
        html.P("© 2025 My Dashboard, Inc."),
        html.A("Privacy Policy", href="#"),
        html.A("Terms of Service", href="#")
    ], className="page-footer"),

], className='body-wrapper')  # outermost container

# ---------- Callbacks ----------
@app.callback(
    Output('world-map', 'figure'),
    Input('borough-dropdown', 'value')
)
def update_countries_of_origin_map(borough_name):
    return get_countries_of_origin_map(borough_name)

@app.callback(
    Output('income-chart-container', 'children'),
    Input('party-dropdown', 'value')
)
def update_party_income_chart(party):
    fig = get_party_income_relation(party)
    return dcc.Graph(figure=fig, className='graph')

if __name__ == '__main__':
    app.run(debug=True)
