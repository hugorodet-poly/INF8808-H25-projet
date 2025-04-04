import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px
from src.preprocess import get_demographics_data, get_elections_data, get_elections_data_by_winning_party
from src.preprocess import get_participation_per_district, group_elections_data_as_party

# Define political party colors and names
political_parties = {
    1: "Coalition avenir Québec",
    2: "Parti libéral du Québec",
    3: "Québec solidaire",
    4: "Parti québécois"
}

def set_customdata(z, customdata, m, n, political_parties):
    """Set custom hover data for waffle charts"""
    for i in range(m):
        for j in range(n):
            customdata[i, j] = political_parties[z[i, j]]
    return customdata

def set_customdata_montreal(z, customdata, m, n, political_parties):
    """Set custom hover data specifically for Montreal waffle chart"""
    for i in range(m):
        for j in range(n):
            customdata[i, j] = political_parties[z[i, j]]
    return customdata

def get_quebec_waffle_chart():
    """Create a waffle chart for all of Quebec's National Assembly seats"""
    m = 5  # Rows
    n = 25  # Columns
    z = np.ones((m, n))

    # Set party values (1=CAQ, 2=PLQ, 3=QS, 4=PQ)
    z[0:5, 0:4] = 2
    z[0, 4] = 2
    z[4, 4] = 3
    z[0:5, 5:7] = 3
    z[1:4, 4] = 4

    # Create custom data for hover info
    M = max([len(s) for s in political_parties.values()])
    customdata = np.empty((m, n), dtype=f'<U{M}')
    customdata = set_customdata(z, customdata, m, n, political_parties)

    # Define color scale
    colorscale = [
        [0, "#1E90FF"],      # CAQ - Blue 
        [0.33, "#00cc96"],   # PLQ - Green
        [0.33, "#b52121"],   # QS - Red
        [0.66, "#FF8040"],   # PQ - Orange
        [0.66, "#FF8040"],
        [1, "#004A9A"]
    ]

    # Create figure
    fig = go.Figure(go.Heatmap(
        z=z,
        customdata=customdata, 
        xgap=3, 
        ygap=3,
        colorscale=colorscale, 
        showscale=False,
        hovertemplate="%{customdata}<extra></extra>"
    ))

    fig.update_layout(
        width=800,
        height=400, 
        yaxis_autorange='reversed',
        title="Sièges par parti politique à l'Assemblée nationale du Québec aux élections 2022",
        title_x=0.5,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    
    return fig

def get_montreal_waffle_chart():
    """Create a waffle chart for Montreal's National Assembly seats"""
    m = 3  # Rows
    n = 9  # Columns
    z = np.ones((m, n))

    # Set party values (1=CAQ, 2=PLQ, 3=QS, 4=PQ)
    z[0:, 0:5] = 2
    z[0, 5] = 2
    z[1, 5] = 4
    z[2, 5] = 3
    z[0:, 6:8] = 3
    z[0, 8] = 3

    # Create custom data for hover info
    M = max([len(s) for s in political_parties.values()])
    customdata = np.empty((m, n), dtype=f'<U{M}')
    customdata = set_customdata_montreal(z, customdata, m, n, political_parties)

    # Define color scale
    colorscale = [
        [0, "#1E90FF"],      # CAQ - Blue
        [0.33, "#00cc96"],   # PLQ - Green
        [0.33, "#b52121"],   # QS - Red
        [0.66, "#FF8040"],   # PQ - Orange
        [0.66, "#FF8040"],
        [1, "#004A9A"]
    ]

    # Create figure
    fig = go.Figure(go.Heatmap(
        z=z,
        customdata=customdata, 
        xgap=3, 
        ygap=3,
        colorscale=colorscale, 
        showscale=False,
        hovertemplate="%{customdata}<extra></extra>"
    ))

    fig.update_layout(
        width=800,
        height=400, 
        yaxis_autorange='reversed',
        title="Sièges par parti politique selon les circonscriptions de Montréal aux élections 2022",
        title_x=0.5,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    
    return fig

def get_hypothetical_waffle_chart():
    """Create a waffle chart showing what Quebec's National Assembly would look like 
    if Montreal's voting patterns were applied to the entire province"""
    m = 5  # Rows
    n = 25  # Columns
    z = np.ones((m, n))

    # Set party values (1=CAQ, 2=PLQ, 3=QS, 4=PQ)
    z[0:5, 0:15] = 2
    z[4, 14] = 4
    z[0:4, 15] = 4
    z[4, 15] = 3
    z[0:5, 16:23] = 3
    z[0, 23] = 3

    # Create custom data for hover info
    M = max([len(s) for s in political_parties.values()])
    customdata = np.empty((m, n), dtype=f'<U{M}')
    customdata = set_customdata(z, customdata, m, n, political_parties)

    # Define color scale
    colorscale = [
        [0, "#1E90FF"],      # CAQ - Blue
        [0.33, "#00cc96"],   # PLQ - Green
        [0.33, "#b52121"],   # QS - Red
        [0.66, "#FF8040"],   # PQ - Orange
        [0.66, "#FF8040"],
        [1, "#004A9A"]
    ]

    # Create figure
    fig = go.Figure(go.Heatmap(
        z=z,
        customdata=customdata, 
        xgap=3, 
        ygap=3,
        colorscale=colorscale, 
        showscale=False,
        hovertemplate="%{customdata}<extra></extra>"
    ))

    fig.update_layout(
        width=800,
        height=400, 
        yaxis_autorange='reversed',
        title="Sièges par parti politique à l'Assemblée nationale du Québec aux élections 2022 <br> si Montréal était tout le Québec",
        title_x=0.5,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    
    return fig

def get_immigrant_voting_scatter():
    """Create a scatter plot showing relationship between immigration percentage and voter participation"""
    df_demographics = get_demographics_data()
    immigration_rate = df_demographics[['Circonscription', 'Immigrants']]
    
    df_election = get_elections_data()
    df_election = get_participation_per_district(df_election)
    
    df_election.rename(columns={'nomCirconscription': 'Circonscription'}, inplace=True)
    df_election = df_election.merge(right=immigration_rate, how='inner', on='Circonscription')
    
    fig = px.scatter(
        df_election, 
        x="Immigrants", 
        y="tauxParticipation", 
        hover_data=['Circonscription'],
        labels={
            "Immigrants": "Pourcentage d'Immigrants", 
            "tauxParticipation": "Taux de participation"
        },
    )
    
    fig.update_layout(
        title="Taux de participation en fonction du taux d'immigration",
        title_x=0.5,
        height=600,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def get_party_income_relation(party='Q.S.'):
    """Create a scatter plot showing relationship between median household income and votes for a specific party"""
    df_demographics = get_demographics_data()
    income_data = df_demographics[['Circonscription', "Revenu median des menages $"]]
    
    df_election = get_elections_data()
    df_election_filtered = group_elections_data_as_party(df_election, None, party)
    
    df_election_filtered.rename(columns={'nomCirconscription': 'Circonscription'}, inplace=True)
    df_election_filtered = df_election_filtered.merge(right=income_data, how='inner', on='Circonscription')
    df_election_filtered = df_election_filtered.sort_values("Revenu median des menages $")
    
    fig = px.scatter(
        df_election_filtered, 
        x="Revenu median des menages $", 
        y="tauxVote", 
        hover_data=['Circonscription'],
        labels={
            "Revenu median des menages $": "Revenu médian des ménages $",
            "tauxVote": f"Taux de vote pour {party}"
        }
    )
    
    fig.update_layout(
        title=f"Taux de vote pour {party} en fonction du revenu médian des ménages",
        title_x=0.5,
        height=600,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig