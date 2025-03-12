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
        map_data = json.load(f)

    # Clean the names
    for i in range(len(map_data['features'])):
        map_data['features'][i]['properties']['NM_CEP'] = unidecode(map_data['features'][i]['properties']['NM_CEP'])
    # Roughly sort. NOT RELIABLE for 1-to-1 matching
    map_data['features'].sort(key=lambda x: x['properties']['NM_CEP'].lower())
    
    # Add unique IDs to use as primary key (and also row order)
    for i in range(len(map_data['features'])):
        map_data['features'][i]['properties']['ID'] = i
        
    return map_data

def get_elections_data(path='../assets/data/resultats.csv'):
    """
    Load the elections data from the CSV file and clean it.
    Group by district for easy plotting on a map.
    """
    
    df = pd.read_csv(path, sep=',')
    
    # Clean
    df['nomCirconscription'] = df['nomCirconscription'].map(lambda s: unidecode(s))   
    
    return df 

def nb_candidates_per_circo(df):
    """
    Count the number of candidates per district.
    """
    df_grouped = df.groupby('nomCirconscription').apply(lambda x: x.shape[0])
    return df_grouped

def vote_summary_by_circo(df):
    """
    Group the elections data by circonscription, making a summary.
    Columns starting with "nb" are summed, columns starting with "taux" are averaged.
    """
    
    def reduction_fn(x):
        out = []
        for col in x.columns:
            if col.startswith('nb'):
                out.append(x[col].sum())
            elif col.startswith('taux'):
                out.append(x[col].mean())
            else:
                raise ValueError(f'Unknown column type : {col}. Only processing columns starting with "taux" or "nb"')
        return pd.DataFrame(data=[out], columns=x.columns)

    df_dropped = df.drop(columns=['numeroCirconscription', 'numeroCandidat', 'nomCandidat', 'prenomCandidat', 'abreviationPartiPolitique', 'numeroPartiPolitique'])
    df_grouped = df_dropped.groupby('nomCirconscription').apply(reduction_fn, include_groups=False).reset_index(drop=True)

    return df_grouped