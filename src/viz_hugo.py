import os
import os.path as osp
import numpy as np
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

from src.maps import get_map, get_countries_mapdata, get_boroughs_mapdata, get_countries_of_origin
from src.preprocess import get_boroughs_data

# Immigration data per borough in Montreal
borough_df = get_boroughs_data()

# Montreal boroughs choropleth for immigration data
montreal_boroughs_mapdata = get_boroughs_mapdata()

# World map choropleth
world_mapdata = get_countries_mapdata()

# get the map of montreal
def get_montreal_boroughs_map():
    """
    Create a map of Montreal boroughs
    """
    # Prepare the map data
    montreal_map = px.choropleth_mapbox(
        geojson=montreal_boroughs_mapdata,
        locations=range(len(montreal_boroughs_mapdata['features'])),
        color=[f['properties']['nom_arr'] for f in montreal_boroughs_mapdata['features']],
        featureidkey="id",
        mapbox_style="carto-positron",
        zoom=9.5,
        center={"lat": 45.55, "lon": -73.72},
        opacity=0.8,
        labels={'color':'Borough'}
    )
    
    montreal_map.update_layout(
        title='Montreal Boroughs',
        autosize=True,
        height=600,
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False
    )
    
    return montreal_map