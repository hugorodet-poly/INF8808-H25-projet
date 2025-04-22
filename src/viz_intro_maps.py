import os
import os.path as osp
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

from src.maps import get_map, get_countries_of_origin

# get the map of montreal
def get_montreal_boroughs_map(montreal_boroughs_mapdata, borough_df):
    """
    Create a map of Montreal boroughs
    """
    # Get the values used later for the color scale
    mtl_map_color = []
    unique_edges = []
    for f in montreal_boroughs_mapdata['features']:
        if f['properties']['nom_arr'] is not None: # Some names are missing
            edge = borough_df.loc[borough_df['Arrondissement']==f['properties']['nom_arr'], 'Immigrante'].values[0]
            mtl_map_color.append(edge)
            if edge not in unique_edges:
                unique_edges.append(edge)
        else:
            mtl_map_color.append(None)
  
    # Setup the "discrete" color scale (they are not possible with choropleths by default, so we cheat)
    unique_edges = np.sort(np.array(unique_edges, dtype=float))
    unique_edges -= unique_edges.min()
    unique_edges /= unique_edges.max()
    colors = px.colors.qualitative.Pastel1
    custom_scale = [(e, colors[i%len(colors)]) for i,e in enumerate(np.repeat(unique_edges,2))]
  
    # Create the map    
    montreal_map = get_map(montreal_boroughs_mapdata, mtl_map_color, zoom='montreal', marker_line_width=1)
    mtl_hovertemplate = "<b>Neighborhood :<br></b> %{customdata[0]}<br><b>Borough :<br></b> %{customdata[1]}<br><b>Immigrants :<br></b>  %{z}<extra></extra>"
    
    montreal_map.update_traces(
        colorscale=custom_scale,
        showscale=False,
        hovertemplate=mtl_hovertemplate,
        hoverlabel=dict(align='left'),
        customdata=[
            (
                f['properties']['nom_qr'],
                f['properties']['nom_arr'].replace(',', ',<br>') if f['properties']['nom_arr'] is not None else '<i>No associated borough</i>',
            ) for f in montreal_boroughs_mapdata['features']])
    
    montreal_map.update_layout(
        hovermode='x',
        map_style='white-bg',
        margin=dict(l=0, r=0, t=0, b=0),
        map=dict(center=dict(lat=45.5517, lon=-73.7073), zoom=9),
        width=400, height=400)
    
    return montreal_map

def express_choropleth(map_data, color):
    """
    Create a map of the world
    """
    fig = px.choropleth(
        geojson=map_data,
        color=color,
        featureidkey='properties.ID',
        locations=[f['properties']['ID'] for f in map_data['features']],
        color_continuous_scale=px.colors.sequential.Reds,
        projection='equal earth',
    )
    fig.update_mapboxes(style="white-bg")

    return fig

def get_world_immigrants_map(
    montreal_boroughs_mapdata,
    world_mapdata,
    borough_df,
    clickdata=None):
    # Case when no borough is selected, showing for the whole of Montréal by default
    if clickdata is None:
        color, country_names = get_countries_of_origin('Ville de Montréal', borough_df, world_mapdata)
        world_map = express_choropleth(world_mapdata, color=color)
        borough_name = 'Ville de Montréal'
    # Case when a borough is selected
    else:
        idx = clickdata['points'][0]['pointNumber']
        borough_name = montreal_boroughs_mapdata['features'][idx]['properties']['nom_arr']

        # Some choropleth polygons actually have no associated borough
        if borough_name is None:
            world_map = express_choropleth(world_mapdata, color=[None]*len(world_mapdata['features']))
            
        else:
            color, country_names = get_countries_of_origin(borough_name, borough_df, world_mapdata)
            world_map = express_choropleth(world_mapdata, color)
 
    hovertemplate = "<b>%{customdata[0]} :</b> %{z}<extra></extra>"
    
    # Capitalize first letters
    country_names = ['-'.join([word.capitalize() for word in name.split('-')]) for name in country_names]
    country_names = [' '.join([word.capitalize() for word in name.split(' ')]) for name in country_names]
    country_names = ['\''.join([word.capitalize() for word in name.split('\'')]) for name in country_names]
    
    
    world_map.update_traces(
        marker_line_width=0.1,
        marker_line_color='gray',
        hovertemplate=hovertemplate,
        customdata=[[name] for name in country_names])
    
    world_map.update_layout(
        title=None,
        margin=dict(l=0, r=0, t=0, b=0),
        width=900, height=400)
    
    world_map.update_coloraxes(colorbar_title='Immigrants')
    
    return world_map, f'Pays d\'origine : {borough_name}'