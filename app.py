import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Import your custom modules
from src.maps import get_districts_mapdata, get_boroughs_mapdata, get_countries_mapdata
from src.preprocess import get_demographics_data, get_elections_data, get_boroughs_data
from src.viz_guillaume import stacked_bar_chart_most, stacked_bar_chart_least, immigrants_map, linguistic_map
from src.viz_hugo import get_montreal_boroughs_map, get_world_immigrants_map
from src.viz_nathan import create_interactive_connected_dot_plot, get_language_dropdown_options

# Import Sidney's visualizations
from src.viz_sid import get_quebec_waffle_chart, get_montreal_waffle_chart, get_hypothetical_waffle_chart, get_upper_median_immigration_waffle, get_lower_median_immigration_waffle
from src.viz_sid import get_immigrant_voting_scatter, get_party_income_relation

# ---------- Data Loading -------------
demographics_data = get_demographics_data()
borough_df = get_boroughs_data()
districts_mapdata = get_districts_mapdata()
montreal_boroughs_mapdata = get_boroughs_mapdata()
world_mapdata = get_countries_mapdata()
election_data = get_elections_data()

# ---------- Pre-generate Figures -----
immigrants_map_fig = immigrants_map(demographics_data, districts_mapdata)
linguistic_map_fig = linguistic_map(demographics_data, districts_mapdata)
fig_quebec = get_quebec_waffle_chart()
fig_montreal = get_montreal_waffle_chart()
fig_hypothetical = get_hypothetical_waffle_chart()
fig_upper_median_immigration = get_upper_median_immigration_waffle()
fig_lower_median_immigration = get_lower_median_immigration_waffle()
fig_immigrant_voting = get_immigrant_voting_scatter(demographics_data, election_data)
fig_most = stacked_bar_chart_most(demographics_data, election_data)
fig_least = stacked_bar_chart_least(demographics_data, election_data)
montreal_boroughs_map = get_montreal_boroughs_map(montreal_boroughs_mapdata, borough_df)
language_dropdown_options = get_language_dropdown_options()

# ---------- Dash App Setup -----------
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=False,
    assets_folder='assets',
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
server = app.server
app.title = 'Electoral Demographics Analysis'
immigrants_map_fig.write_html("assets/immigration_map.html", include_plotlyjs='cdn')
linguistic_map_fig.write_html("assets/linguistic_map.html", include_plotlyjs='cdn')

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

        # 1. World Immigration Origins
        html.Div([
            html.H2('Immigration in Montreal', className='section-title'),
            
            html.H3('Distribution of the immigrants', className='section-title'),
            html.P('This map shows the percentage of immigrants across different electoral districts in Montreal.'),
            html.Iframe(src="/assets/immigration_map.html", width="100%", height="600", className='iframe'),
            
            html.Hr(className='section-divider'),
            
            html.H3('Countries of Origin', className='section-title'),
            html.P('This map shows the countries of origin for immigrants in Montreal boroughs. <b>Click on a borough !</b>'),
            html.P(id='current-borough', children='Ville de Montréal'),
            
            html.Div(className='flex-row', children=[
                html.Div(className='four columns', children=[ # Montreal Map
                    dcc.Graph(id='montreal-immigrants-map', figure=montreal_boroughs_map, style={'justify': 'center'})]),
                html.Div(className='eight columns', children=[ # World map
                    dcc.Graph(id='world-immigrants-map', style={'justify': 'center'})])]),
        ], className='card'),

        html.Hr(className='section-divider'),

        # 3. Language Distribution (Montreal)
        html.Div([
            html.H2('Language Distribution in Montreal', className='section-title'),
            html.P('This map shows the percentage of people who speak neither English nor French across Montreal electoral districts.'),
            html.Iframe(src="/assets/linguistic_map.html", width="100%", height="600", className='iframe'),
            html.Hr(className='section-divider'),
            html.P('Comparaison des votes par groupe linguistique aux élections québécoises de 2022'),
            dcc.Dropdown(
                id='language-dropdown',
                options=language_dropdown_options,
                value=language_dropdown_options[0],
                className='custom-dropdown'),
            dcc.Graph(id='connected-dot-plot', className='graph'),
        ], className='card'),
        

        # 4. Electoral Representation
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
            # Hypothetical Electoral Scenario
            html.Div([
                html.H3('Hypothetical Electoral Scenario'),
                html.P('What if Montreal voting patterns applied to all of Quebec?'),
                dcc.Graph(figure=fig_hypothetical, className='graph')
            ], className='card'),

            # Upper median immigration districts
            html.Div([
                html.H3('Upper Median Immigration Districts'),
                dcc.Graph(figure=fig_upper_median_immigration, className='graph')
            ], className='card'),

            # Lower median immigration districts
            html.Div([
                html.H3('Lower Median Immigration Districts'),
                dcc.Graph(figure=fig_lower_median_immigration, className='graph')
            ], className='card'),

            # Immigration and Voter Participation
            html.Div([
                html.H3('Immigration and Voter Participation'),
                html.P('Correlation between immigration rates and voter turnout.'),
                dcc.Graph(figure=fig_immigrant_voting, className='graph')
            ], className='card'),


            # 4.5 Party Support by Income
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
                ], className='row'),

                html.Div(
                    id='income-chart-container',
                    className='graph-container row'
                )
            ], className='card'),
        ], className='card'),

        html.Hr(className='section-divider'),

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
    Output('income-chart-container', 'children'),
    Input('party-dropdown', 'value')
)
def update_party_income_chart(party):
    fig = get_party_income_relation(demographics_data, election_data, party)
    return dcc.Graph(figure=fig, className='graph')

@app.callback(
    Output(component_id='world-immigrants-map', component_property='figure'),
    Output(component_id='current-borough', component_property='children'),
    Input(component_id='montreal-immigrants-map', component_property='clickData'))
def update_world_immigrants_map(clickdata):
    fig, borough = get_world_immigrants_map(montreal_boroughs_mapdata, world_mapdata, borough_df, clickdata)
    return fig, borough

@app.callback(
    Output(component_id='connected-dot-plot', component_property='figure'),
    Input(component_id='language-dropdown', component_property='value'))
def update_language_dot_plot(lang_option):
    fig = create_interactive_connected_dot_plot(demographics_data, election_data, lang_option)
    return fig
    

if __name__ == '__main__':
    app.run(debug=False)
