import plotly.graph_objects as go
import pandas as pd

# Noms des circonscriptions considérées appartenant à chaque ville
circo_groups = {
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
    demographics: pd.DataFrame, 
    variable: str, 
    opacity: float=0.5, 
    zoom: str='quebec'):
    """
    Returns a choropleth map of Quebec or Montreal with the specified demographic variable.
    
    Args:
        map_data (dict): GeoJSON data for Quebec or Montreal.
        demographics (DataFrame): Dataframe containing the variable for the color.
        variable (str): Name of the variable to display.
        opacity (float): Opacity of the map markers (0 to 1).
        zoom (str): 'quebec' or 'montreal'.
        
    Returns:
        go.Figure: Choropleth map to plot.
    """
    z = demographics[variable].values
    if demographics[variable].dtype == 'object':
        z = [float(s[:-1].replace(',', '.')) for s in z]
    
    fig = go.Figure(go.Choroplethmap(
        geojson=map_data,
        featureidkey='properties.ID',
        locations=[f['properties']['ID'] for f in map_data['features']],
        z=z,
        hovertext=[f['properties']['NM_CEP'] for f in map_data['features']],
        marker_opacity=opacity, marker_line_width=0))
    fig.update_geos(
        projection=dict(
            type="conic conformal",
            parallels=[50, 46]))
    
    if zoom == 'quebec':
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