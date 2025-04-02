import os
import os.path as osp
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input

from maps import *
from preprocess import *

# Immigration data per borough in Montreal
borough_df = get_boroughs_data()

# Montreal boroughs choropleth for immigration data
montreal_boroughs_mapdata = get_boroughs_mapdata()

# World map choropleth
world_mapdata = get_countries_mapdata()

# get the map of montreal
def get_montreal_boroughs_map():
    mtl_map_color = [borough_df.loc[borough_df['Arrondissement']==f['properties']['nom_arr'], 'Immigrante'].values[0] if f['properties']['nom_arr'] is not None else None for f in montreal_boroughs_mapdata['features']]
    montreal_map = get_map(montreal_boroughs_mapdata, mtl_map_color, zoom='montreal', marker_line_width=1)
    mtl_hovertemplate = "<b>Neighborhood :</b> %{customdata[0]}<br><b>Borough :</b> %{customdata[1]}<br><b>Immigrants :</b> %{z}<extra></extra>"
    montreal_map.update_traces(
        showscale=False,
        hovertemplate=mtl_hovertemplate,
        customdata=[
            (
                f['properties']['nom_qr'],
                f['properties']['nom_arr'] if f['properties']['nom_arr'] is not None else '<i>No associated borough</i>',
            ) for f in montreal_boroughs_mapdata['features']])
    montreal_map.update_layout(
        map_style='white-bg',
        margin=dict(l=0, r=0, t=0, b=0),
        map=dict(center=dict(lat=45.5517, lon=-73.7073), zoom=9),
        width=400, height=600)
    return montreal_map

# Plot the mesh corresponding to the histogram, via sampling if needed
@callback(
    Output(component_id='world-map', component_property='figure'),
    Input(component_id='montreal-map', component_property='clickData'))
def update_world_map(clickdata):
    if clickdata is None:
        color = get_countries_of_origin('Ville de Montréal', borough_df, world_mapdata)
        world_map = get_map(world_mapdata, color=color)
        world_map.update_layout(title='Countries of origin across Montreal boroughs')
    else:
        idx = clickdata['points'][0]['pointNumber']
        borough_name = montreal_boroughs_mapdata['features'][idx]['properties']['nom_arr']

        # Some choropleth polygons actually have no associated borough
        if borough_name is None:
            world_map = get_map(world_mapdata, color=[None]*len(world_mapdata['features']))
        else:
            color = get_countries_of_origin(borough_name, borough_df, world_mapdata)
            world_map = get_map(world_mapdata, color)
            world_map.update_layout(title=f'Countries of origin for {borough_name}')
 
    world_map.update_layout(
        margin=dict(l=0, r=100, t=50, b=0),
        map=dict(center=dict(lat=50, lon=0), zoom=0.5),
        width=800, height=600)
    return world_map