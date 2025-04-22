import numpy as np
import pandas as pd
import json
import os
from unidecode import unidecode

# Constants

political_parties = {
    1: "Coalition avenir Québec",
    2: "Parti libéral du Québec",
    3: "Québec solidaire",
    4: "Parti québécois"
    }

def get_demographics_data(path:str='assets/data/donneesSocio2021.csv'):
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
    
    # Convert the percentages from str to float
    for i in range(len(df_dem.columns)):
        if df_dem.dtypes.iloc[i] == 'object' and df_dem.columns[i] not in ['Circonscription']:
            df_dem.iloc[:,i] = df_dem.iloc[:,i].str[:-1].map(lambda s: float(s.replace(',', '.').replace(' ', '')) if s else 0)
    
    return df_dem
    
def get_boroughs_data(path:str='assets/data/arrondissements.csv'):
    """
    Load the immigration data PER borough (not the same as electoral disctricts)
    """
    df_imm = pd.read_csv(path, sep=',')
    
    return df_imm    

def get_elections_data(path:str='assets/data/resultats.csv'):
    """
    Load the elections data from the CSV file and clean it.
    Group by district for easy plotting on a map.
    """
    
    df = pd.read_csv(path, sep=',')
    
    # Clean
    df['nomCirconscription'] = df['nomCirconscription'].map(lambda s: unidecode(s))   
    
    return df 

def nb_candidates_per_circo(df:pd.DataFrame):
    """
    Count the number of candidates per district.
    """
    df_grouped = df.groupby('nomCirconscription').apply(lambda x: x.shape[0])
    return df_grouped

def vote_summary_by_circo(df:pd.DataFrame):
    """
    Group the elections data by circonscription, making a summary.
    Columns starting with "nb" are summed, columns starting with "taux" are averaged.
    If you want info for a specific party only, you can just pass as argument the sub-dataframe 
    contaiing only the data from that party, e.g. df[df['abreviationPartiPolitique']=='P.L.Q/L.P.Q']
    """
    
    def reduction_fn(x):
        out = []
        for col in x.columns:
            if col.startswith('taux') or col in ['nbBureauTotal', 'nbVoteValide', 'nbVoteRejete', 'nbVoteExerce', 'nbElecteurInscrit' ]:
                out.append(x[col].mean())
            elif col in ['nbVoteTotal', 'nbVoteAvance']:
                out.append(x[col].sum())
            else:
                raise ValueError(f'Unknown column type : {col}. Only processing columns starting with "taux" or "nb"')
        return pd.DataFrame(data=[out], columns=x.columns)

    df_dropped = df.drop(columns=[
        'numeroCirconscription', 
        'numeroCandidat', 
        'nomCandidat', 
        'prenomCandidat', 
        'abreviationPartiPolitique', 
        'numeroPartiPolitique', 
        'nbBureauComplete'])
    df_grouped = df_dropped.groupby('nomCirconscription').apply(reduction_fn, include_groups=False).reset_index()
    df_grouped = df_grouped.sort_values(by='nomCirconscription', key=lambda x: x.str.lower()).reset_index(drop=True)

    return df_grouped


def group_elections_data_as_party(df, circonscription=None, party='Q.S.'):
    """
    return the vote rate of a specific party in a specific circonscription
    """
    
    df_filtered = df[df['abreviationPartiPolitique'] == party]
    
    df_grouped = df_filtered.groupby('nomCirconscription', as_index=False)['tauxVote'].sum()

    if circonscription:
        df_grouped = df_grouped[df_grouped['nomCirconscription'] == circonscription]

    return df_grouped

def get_participation_per_district(df):
    """
    Group the elections data by circonscription to get the participation rate.
    """
    
    df_grouped = df.groupby('nomCirconscription').agg({'tauxParticipation': 'first'}).reset_index()
    
    return df_grouped

def get_taux_vote_per_district(df):
    """
    Group the elections data by circonscription to get the participation rate.
    """
    
    df_grouped = df.groupby('nomCirconscription').agg({'tauxVote': 'first'}).reset_index()
    
    return df_grouped

def get_elections_data_by_winning_party(df):
    """
    Group the elections data by winning party.
    """
    
    df_grouped =  df.groupby('nomCirconscription').agg({'abreviationPartiPolitique': 'first', 'nbVoteAvance': 'first'}).reset_index()
    # only keep the winning party
    df_grouped['nbVoteAvance'] == df_grouped.groupby('nomCirconscription')['nbVoteAvance'].transform("max")
    
    return df_grouped

def map_abreviation_to_party_name():
    """
    Map the party abbreviation to the party name.
    """
    
    political_parties = {
        1: "Coalition avenir Québec",
        2: "Parti libéral du Québec",
        3: "Québec solidaire",
        4: "Parti québécois"
        }
    
    abreviation = {
        1: "C.A.Q.-E.F.L.",
        2: "P.L.Q./Q.L.P.",
        3: "Q.S.",
        4: "P.Q."
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(political_parties.items(), columns=['id', 'nomPartiPolitique'])
    # add abreviation
    df['abreviationPartiPolitique'] = df['id'].map(abreviation)
    
    # Clean the names
    df.rename(columns={s:unidecode(s) for s in df.columns}, inplace=True)
    
    return df[['abreviationPartiPolitique', 'nomPartiPolitique']]

def get_circonscriptions_with_full_party_name():

    df = get_elections_data_by_winning_party(get_elections_data())
    df_map = map_abreviation_to_party_name()

    df = df.merge(right=df_map, how='inner', left_on='abreviationPartiPolitique', right_on='abreviationPartiPolitique')
    df.sort_values(by=("abreviationPartiPolitique"), inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def get_lists_of_circonscription_according_to_winning_party():
    """
    Get the lists of circonscriptions according to the winning party.
    """
    
    df_grouped = get_circonscriptions_with_full_party_name().groupby('nomPartiPolitique')['nomCirconscription'].apply(list).reset_index()
    
    return df_grouped
