import plotly.graph_objects as go
import pandas as pd
from unidecode import unidecode
import json
import numpy as np

# Noms des circonscriptions considérées appartenant à chaque ville
circo_subsets = {
    'Montréal': [
        'Acadie',
        'Anjou-Louis-Riel',
        'Bourassa-Sauve',
        'Camille-Laurin',
        'D\'Arcy-McGee',
        'Gouin',
        'Hochelaga-Maisonneuve',
        'Jacques-Cartier',
        'Jeanne-Mance-Viger',
        'LaFontaine',
        'Laurier-Dorion',
        'Marguerite-Bourgeoys',
        'Marquette',
        'Maurice-Richard',
        'Mercier',
        'Mont-Royal-Outremont',
        'Nelligan',
        'Notre-Dame-de-Grace',
        'Pointe-aux-Trembles',
        'Robert-Baldwin',
        'Rosemont',
        'Saint-Henri-Sainte-Anne',
        'Saint-Laurent',
        'Sainte-Marie-Saint-Jacques',
        'Verdun',
        'Viau',
        'Westmount-Saint-Louis'],
    'Québec': [
        'Charlesbourg',
        'Charlevoix-Cote-de-Beaupre',
        'Chauveau',
        'Jean-Lesage',
        'Jean-Talon',
        'La Peltrie',
        'Louis-Hebert',
        'Montmorency',
        'Portneuf',
        'Taschereau',
        'Vanier-Les Rivieres'], 
}

def get_map(
    map_data: dict, 
    color: list=None,
    zoom: str='auto',
    **kwargs):
    """
    Returns a choropleth map of Quebec or Montreal with the specified demographic variable.
    
    Args:
        map_data (dict): GeoJSON data for Quebec or Montreal.
        color (list): List of values to color the map.
        opacity (float): Opacity of the map markers (0 to 1).
        contour_width (int): Width of the contour lines.
        zoom (str): 'world' or 'quebec' or 'montreal'.
        
    Returns:
        go.Figure: Choropleth map to plot.
    """
    
    # Default to all zeros because otherwise the choropleth tiles are not displayed
    if color is None:
        color = [0]*len(map_data['features'])
    
    # Plot the choropleth
    fig = go.Figure(
        go.Choroplethmap(
            geojson=map_data,
            featureidkey='properties.ID',
            locations=[f['properties']['ID'] for f in map_data['features']],
            z=color,
            #colorscale='Reds',
            #**kwargs
            ))
    
    # # Set the zoom level
    # zoom = unidecode(zoom).lower()
    # if zoom == 'world':
    #     pass # Default zoom, maybe change it laters
    # elif zoom == 'quebec':
    #     fig.update_layout(
    #         map=dict(center=dict(lat=54, lon=-68.5), zoom=3.65),
    #         width=600, height=800)
    # elif zoom == 'montreal':
    #     fig.update_layout(
    #         map=dict(center=dict(lat=45.53, lon=-73.67), zoom=9.5),
    #         width=600, height=800)
    # elif zoom == 'auto':
    #     pass
    # else:
    #     raise ValueError('Invalid zoom value. Use "auto", "quebec" or "montreal".')  
    
    # # Make sure the coordinates of the GeoJSON and plotly chrolopleth correspond
    # fig.update_geos(
    #     fitbounds="locations",
    #     projection=dict(
    #         type="conic conformal",
    #         parallels=[50, 46]))
      
    return fig

def get_districts_mapdata(path:str='assets/maps/districts_QC.geojson'):
    """
    Map data for the electoral districts.
    Load the map data from the GeoJSON file and clean it.
    """
    
    with open(path, 'r', encoding='utf-8-sig') as f:
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

def get_countries_mapdata(path:str='assets/maps/countries.geojson'):
    """
    Load the countries data from the GeoJSON
    """
    
    with open(path, 'r', encoding='utf-8-sig') as f:
        countries_map_data = json.load(f)
        
    # Clean the names
    for i in range(len(countries_map_data['features'])):
        countries_map_data['features'][i]['properties']['name'] = unidecode(countries_map_data['features'][i]['properties']['name'])
        
    # Add unique IDs to use as primary key (and also row order)
    for i in range(len(countries_map_data['features'])):
        countries_map_data['features'][i]['properties']['ID'] = i
    
    return countries_map_data

def get_boroughs_mapdata(path:str='assets/maps/arrondissements_montreal.geojson'):
    """
    Load the borough data from the GeoJSON
    """
    
    with open(path, 'r', encoding='utf-8-sig') as f:
        boroughs_map_data = json.load(f)
        
    # Clean the names
    for i in range(len(boroughs_map_data['features'])):
        boroughs_map_data['features'][i]['properties']['nom_qr'] = unidecode(boroughs_map_data['features'][i]['properties']['nom_qr'])
        
        s = boroughs_map_data['features'][i]['properties']['nom_arr']
        s = s.replace('–', ', ') if s is not None else None
        boroughs_map_data['features'][i]['properties']['nom_arr'] = s
        
    # Add unique IDs to use as primary key (and also row order)
    for i in range(len(boroughs_map_data['features'])):
        boroughs_map_data['features'][i]['properties']['ID'] = i
    
    return boroughs_map_data

def get_subset_mask(set: list, subset:list):
    """
    Return a boolean mask indicating the elements of the set that are in the subset.
    
    Args:
        set (list): List of circo names
        subset (list): List of circo names, c.f. maps.py
    
    Returns:
        np.array: Boolean mask to subset the dataframe.
    
    example usage:
        mask = subset_mask(df_demographics, circo_subsets['Montréal'])
        df_subset = df[mask]
    """
    return np.array([s in subset for s in set])
        
def get_countries_of_origin(
    borough: str, 
    df: pd.DataFrame, 
    mapdata: dict):
    """
    Find where people come from in a given borough.
    This is meant return the "color" variable to use with get_map,
    to plot on a choropleth map the accurate number of people coming from each country.
    
    Args:
        borough (str): Name of the borough.
        df (pd.DataFrame): Dataframe with the boroughs data (also called "immigration data" in the project).
        mapdata (dict): GeoJSON data for the boroughs.
        
    Returns:
        str: Name of the country of origin.
    """

    # Those are the indices of the columns containing "country of origin" info in the dataframe
    indices = {
        'all': np.arange(134, 193),
        'Americas': {
            'main': np.arange(135, 145),
            'other': 145
        },
        'Europe': {
            'main': np.arange(147, 162),
            'other': 162
        },
        'Africa': {
            'main': np.arange(164, 173),
            'other': 173
        },
        'Asia': {
            'main': np.arange(175, 191),
            'other': 191
        },
        'Oceania': {
            'other': 192
        }
    }

    # Some names are different in the mapdata geoJSON and in the dataframe
    to_change = {
        'salvador': 'el salvador',
        'pays-bas': 'pays bas',
        'republique democratique du congo': 'congo rdc',
        'coree du sud': 'coree sud',
        'republique populaire de chine': 'chine',   
        'irak': 'iraq'
    }

    # Already get the subdataframe 
    df = df[df['Arrondissement']==borough]

    # Prepare some lists for optimization purposes
    countries = df.columns[
        np.concatenate((indices['Americas']['main'], indices['Europe']['main'], indices['Africa']['main'], indices['Asia']['main']), axis=0)
        ].map(lambda s: unidecode(s).lower()).values

    # Always have to format everything......
    formatted_columns = df.columns.map(lambda s: unidecode(s).lower()).to_list()

    # Iteratively fill this list of values
    color = []
    country_names = []
    for feature in mapdata['features']:
        
        # Format the country name
        country_name = unidecode(feature['properties']['name_fr']).lower()
        if country_name in to_change.keys():
            country_name = to_change[country_name]
            
        # If country name is in the dataframe, use the listed value
        if country_name in countries:
            idx = formatted_columns.index(country_name)
            color.append(df.iloc[0, idx])
            country_names.append(country_name)
            
        # Elif the continent is in the dataframe, use the listed value for "Autres lieux de naissance..."
        # There are issue with how we SHOULD represent this data, so for now it's not used
        # elif feature['properties']['continent'] in ['South America', 'North America']:
        #     color.append(df.iloc[0, indices['Americas']['other']])
        # elif feature['properties']['continent'] in ['Europe']:
        #     color.append(df.iloc[0, indices['Europe']['other']])
        # elif feature['properties']['continent'] in ['Africa']:
        #     color.append(df.iloc[0, indices['Africa']['other']])
        # elif feature['properties']['continent'] in ['Asia']:
        #     color.append(df.iloc[0, indices['Asia']['other']])
        # elif feature['properties']['continent'] in ['Oceania']:
        #     color.append(df.iloc[0, indices['Oceania']['other']])

        # Else we don't plot the country (e.g. for Antarctica)
        else:
            color.append(0)
            country_names.append(country_name)

    return color, country_names
