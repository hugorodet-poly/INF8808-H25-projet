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
    opacity: float=0.5,
    contour_width: int=0,
    zoom: str='world'):
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
    fig = go.Figure(go.Choroplethmap(
        geojson=map_data,
        featureidkey='properties.ID',
        locations=[f['properties']['ID'] for f in map_data['features']],
        z=color,
        colorscale='Viridis',
        marker_opacity=opacity, marker_line_width=contour_width))
    
    # Male sure the coordinates of the GeoJSON and plotly chrolopleth correspond
    fig.update_geos(
        projection=dict(
            type="conic conformal",
            parallels=[50, 46]))
    
    # Set the zoom level
    zoom = unidecode(zoom).lower()
    if zoom == 'world':
        pass # Default zoom, maybe change it laters
    elif zoom == 'quebec':
        fig.update_layout(
            map=dict(center=dict(lat=54, lon=-68.5), zoom=3.65),
            width=600, height=800)
    elif zoom == 'montreal':
        fig.update_layout(
            map=dict(center=dict(lat=45.53, lon=-73.67), zoom=9.5),
            width=600, height=800)
    else:
        raise ValueError('Invalid zoom value. Use "quebec" or "montreal".')    
    return fig

def get_districts_mapdata(path:str='../assets/maps/districts_QC.geojson'):
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

def get_countries_mapdata(path:str='../assets/maps/countries.geojson'):
    """
    Load the countries data from the GeoJSON
    """
    
    with open(path) as f:
        countries_map_data = json.load(f)
        
    # Clean the names
    for i in range(len(countries_map_data['features'])):
        countries_map_data['features'][i]['properties']['name'] = unidecode(countries_map_data['features'][i]['properties']['name'])
        
    # Add unique IDs to use as primary key (and also row order)
    for i in range(len(countries_map_data['features'])):
        countries_map_data['features'][i]['properties']['ID'] = i
    
    return countries_map_data

def get_neighborhoods_mapdata(path:str='../assets/maps/arrondissements_montreal.geojson'):
    """
    Load the neighborhood data from the GeoJSON
    """
    
    with open(path) as f:
        countries_map_data = json.load(f)
        
    # Clean the names
    for i in range(len(countries_map_data['features'])):
        countries_map_data['features'][i]['properties']['nom_qr'] = unidecode(countries_map_data['features'][i]['properties']['nom_qr'])
        
    # Add unique IDs to use as primary key (and also row order)
    for i in range(len(countries_map_data['features'])):
        countries_map_data['features'][i]['properties']['ID'] = i
    
    return countries_map_data

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
        