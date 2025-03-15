import numpy as np
import pandas as pd
import json
import os
from unidecode import unidecode

def get_demographics_data(path='../assets/data/donneesSocio2021.csv'):
    """
    Load the demographics data from the CSV file and clean it.
    """

    df_dem = pd.read_csv(path, sep=';')
    
    # Clean the names
    df_dem.rename(columns={s:unidecode(s) for s in df_dem.columns}, inplace=True)
    df_dem.rename(columns={'Circonscription/ DSE 2021':'Circonscription'}, inplace=True)
    df_dem.rename(columns={s: s.strip() for s in df_dem.columns}, inplace=True)

    # The first row is a recap for the entire province, we drop it and clean
    df_dem = df_dem.drop(df_dem[df_dem['Circonscription']=='Province'].index).reset_index(drop=True)
    df_dem['Circonscription'] = df_dem['Circonscription'].map(lambda s: unidecode(s))
    df_dem['Circonscription'] = df_dem['Circonscription'].map(lambda s: s.strip())

    # Sort by name
    df_dem.sort_values(by='Circonscription', inplace=True, key=lambda x: x.str.lower())
    df_dem = df_dem.reset_index(drop=True)  
    
    return df_dem
    
def get_map_data(path='../assets/maps/districts_QC.geojson'):
    """
    Load the map data from the GeoJSON file and clean it.
    """
    
    with open(path) as f:
        districts = json.load(f)

    # Clean the names
    for i in range(len(districts['features'])):
        districts['features'][i]['properties']['NM_CEP'] = unidecode(districts['features'][i]['properties']['NM_CEP'])
    # Roughly sort. NOT RELIABLE for 1-to-1 matching
    districts['features'].sort(key=lambda x: x['properties']['NM_CEP'].lower())
    
    # Add unique IDs to use as primary key (and also row order)
    for i in range(len(districts['features'])):
        districts['features'][i]['properties']['ID'] = i
        
    return districts

def get_elections_data(path='../assets/data/resultats.csv'):
    """
    Load the elections data from the CSV file and clean it.
    Group by district for easy plotting on a map.
    """
    
    df = pd.read_csv(path, sep=',')
    
    # Clean
    df['nomCirconscription'] = df['nomCirconscription'].map(lambda s: unidecode(s))   
    
    return df 

def group_elections_data(df, by='circo'):
    """
    Group the elections data by circonscription or by party.
    """
    
    df_grouped = df.groupby('nomCirconscription').agg({'nomParti': 'first', 'pourcentageVotes': 'first'}).reset_index()
    
    return df_grouped

# def group_elections_data_sid(df, specific_party='first'):
#     """
#     Group the elections data by circonscription or by party.
#     """
#     df_grouped = df.groupby('nomCirconscription').agg({'abreviationPartiPolitique': specific_party, 'tauxVote': 'first'}).reset_index()

#     return df_grouped

def group_elections_data_as_party(df, circonscription=None, party='Q.S.'):
    """
    return the vote rate of a specific party in a specific circonscription
    """
    
    # Filtrer le DataFrame pour ne garder que les votes du parti choisi
    df_filtered = df[df['abreviationPartiPolitique'] == party]
    
    # Grouper par circonscription et récupérer le taux de vote
    df_grouped = df_filtered.groupby('nomCirconscription', as_index=False)['tauxVote'].sum()

    # Si une circonscription spécifique est demandée, on la filtre
    if circonscription:
        df_grouped = df_grouped[df_grouped['nomCirconscription'] == circonscription]

    return df_grouped

def get_participation_per_district(df):
    """
    Group the elections data by circonscription to get the participation rate.
    """
    
    df_grouped = df.groupby('nomCirconscription').agg({'tauxParticipation': 'first'}).reset_index()
    
    return df_grouped