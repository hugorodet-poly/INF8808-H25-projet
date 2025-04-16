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
            html.H2('Immigration à Montreal', className='section-title'),
            
            html.H3('Répartition des immigrants en ville', className='section-title'),
            html.P(
                """Le Québec compte environ 1,1 million de personnes immigrantes, dont plus de 500 000 vivent sur l’île de Montréal. 
                Cela signifie que près de la moitié de la population immigrante de la province est concentrée 
                sur un territoire représentant moins de 5% de sa superficie. 
                Cette forte densité souligne le rôle central de Montréal comme pôle d’accueil au Québec."""),
            html.P(
                """Plusieurs facteurs expliquent cette répartition : la présence de quartiers multiculturels historiques, 
                une offre de logement relativement accessible, des services d’intégration développés et des réseaux 
                communautaires bien établis."""),
            html.P(
                "Source : Statistique Canada, Recensement de 2021 — Profil de la population immigrante (tableau 98-10-0439-01).", 
                style={"fontSize": "0.8em", "color": "#6c757d", "marginTop": "10px"}),
            html.P(
                """La carte ci-dessous montre la répartition des immigrants selon les circonscriptions électorales de 
                l’île de Montréal, avec des zones de forte concentration comme Côte-des-Neiges, Saint-Laurent ou Parc-Extension.
                Elle permet de visualiser les contrastes territoriaux et de mieux comprendre la géographie sociale de l’immigration sur l’île."""),
            html.Iframe(src="/assets/immigration_map.html", width="100%", height="600", className='iframe'),
            
            html.Hr(className='section-divider'),
            
            html.H3('Pays d\'origine', className='section-title'),
            html.P(
                """Cette visualisation met en relation les arrondissements de Montréal avec les principaux pays d’origine de 
                leur population immigrante. Elle permet d’explorer la diversité géographique des communautés présentes dans 
                chaque secteur de la ville, en offrant une lecture croisée entre territoire local et provenance mondiale."""),
            html.H4('Cliquez sur un arrondissement !'),
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
            html.H2('Répartition des langues à Montréal', className='section-title'),
            html.P(
                """Cette carte montre la répartition des personnes vivant sur l’île de Montréal qui ne parlent ni le français 
                ni l’anglais à la maison. Bien que leur proportion demeure faible dans l’ensemble, certaines circonscriptions 
                dépassent les 5 %, notamment dans des secteurs marqués par une forte diversité linguistique."""),
            html.P(
                """Cette situation révèle une réalité importante : pour une partie des résidents, les langues officielles 
                ne sont ni maîtrisées ni utilisées au quotidien, ce qui peut limiter l’accès à l’information, aux soins, 
                à l’éducation, ainsi qu’à la participation à la vie citoyenne et politique."""),
            html.P(
                "Source : Statistique Canada, Recensement de 2021 – Langue parlée à la maison (tableau 98-10-0235-01).",
                style={"fontSize": "0.8em", "color": "#6c757d", "marginTop": "10px"}),
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
            html.H2('Analyse de la représentaion électorale', className='section-title'),
            html.P(
                """Cette section présente plusieurs visualisations en forme de waffle charts, illustrant la 
                répartition des 125 sièges de l’Assemblée nationale du Québec. Chaque case représente un siège 
                et est colorée selon le parti politique auquel il appartient. Ces représentations permettent 
                d’analyser différentes configurations électorales et d’explorer les effets du système majoritaire, 
                tout en mettant en lumière les liens possibles entre la structure démographique des territoires 
                et les tendances de vote observées."""),
            # Example of a flex row with two columns
            html.Div([
                # Quebec Waffle
                html.Div([
                    html.H3('Représentation électorale qu Québec'),
                    html.P(
                        """Le résultat électoral à l’échelle provinciale révèle une nette domination de la 
                        Coalition Avenir Québec (CAQ), qui occupe une large majorité des sièges à l’Assemblée 
                        nationale. Cette surreprésentation reflète les effets du système électoral majoritaire 
                        uninominal à un tour, qui favorise fortement le parti en tête, même lorsque le vote 
                        populaire est plus partagé entre plusieurs formations politiques (élections 2022)."""),
                    dcc.Graph(figure=fig_quebec, className='graph')
                ], className='card flex-child'),

                # Montreal Waffle
                html.Div([
                    html.H3('Représentation électorale à Montréal'),
                    html.P(
                        """Sur l’île de Montréal, la répartition des sièges reflète une plus grande diversité 
                        politique, dominée par le Parti libéral du Québec (PLQ) et Québec solidaire (QS), avec 
                        une faible présence de la CAQ. Cette tendance s’explique en partie par un électorat urbain 
                        plus progressiste, jeune et fortement marqué par l’immigration et la diversité culturelle, 
                        des facteurs qui influencent significativement les choix électoraux (élections 2022)."""),
                    dcc.Graph(figure=fig_montreal, className='graph')
                ], className='card flex-child'),

            ], className='flex-row'),

            # Another row for the next two
            # Hypothetical Electoral Scenario
            html.Div([
                html.H3('Scénario hypothétique d\'élections'),
                html.P(
                    """En imaginant que l’ensemble du Québec adopte les tendances de vote observées à Montréal, 
                    la composition de l’Assemblée nationale serait transformée, avec une présence renforcée 
                    des partis progressistes. Ce scénario révèle un décalage important entre les milieux urbains 
                    et les régions rurales, en partie lié à la diversité culturelle, à l’immigration et aux 
                    réalités sociales propres aux centres urbains. Il met aussi en évidence les limites d’un 
                    système électoral qui peine à refléter la pluralité des voix à l’échelle provinciale."""),
                dcc.Graph(figure=fig_hypothetical, className='graph')
            ], className='card'),

            # Upper median immigration districts
            html.Div([
                html.H3('Circonscriptions à immigration supérieure à la médiane'),
                dcc.Graph(figure=fig_upper_median_immigration, className='graph')
            ], className='card'),

            # Lower median immigration districts
            html.Div([
                html.H3('Circonscriptions à immigration inférieure à la médiane'),
                dcc.Graph(figure=fig_lower_median_immigration, className='graph')
            ], className='card'),

            # Immigration and Voter Participation
            html.Div([
                html.H3('Immigration et taux de participation électorale'),
                html.P(
                    """Le taux de participation électorale tend à diminuer légèrement dans les circonscriptions 
                    où la proportion d’immigrants est plus élevée. Cette tendance, bien que non systématique, 
                    reflète des dynamiques sociales complexes liées à l’intégration et à la représentation politique."""),
                dcc.Graph(figure=fig_immigrant_voting, className='graph')
            ], className='card'),


            # 4.5 Party Support by Income
            html.Div([
                html.H3('Soutien électoral par niveau de revenu'),
                html.P(
                    """Cette visualisation interactive permet d’explorer la relation entre le revenu médian 
                    des ménages et le soutien électoral selon le parti sélectionné. Elle met en évidence certaines 
                    tendances, notamment le lien entre le niveau de revenu d’une circonscription et l’adhésion 
                    à un parti, offrant un aperçu des profils socio-économiques associés aux préférences politiques."""),
                html.Div([
                    html.H4('Sélectionnez un parti politique :'),
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
            html.H2('Comportements de vote en fonction du taux d\'immigration', className='section-title'),
            html.P(
                """Le contraste entre les circonscriptions à faible et forte immigration révèle une polarisation des 
                préférences électorales. La CAQ domine dans les zones moins diversifiées, tandis que le vote est plus 
                fragmenté dans les secteurs à forte immigration, avec une présence marquée du PLQ et de Québec solidaire. 
                Ces résultats montrent que la composition démographique influence directement les dynamiques politiques 
                locales : la diversité culturelle, linguistique et socio-économique façonne les priorités électorales 
                et les comportements politiques à l’échelle des territoires."""),
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
    app.run(debug=True)
