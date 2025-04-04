import plotly.graph_objects as go
from src.preprocess import get_boroughs_data
from src.maps import get_countries_mapdata, get_countries_of_origin

def get_countries_of_origin_map(borough_name='Ville de Montréal'):
    """
    Generate a world map showing the countries of origin for immigrants from a specific borough.
    """
    # Load data
    borough_df = get_boroughs_data()
    world_mapdata = get_countries_mapdata()

    # Get the color data for the map
    color = get_countries_of_origin(borough_name, borough_df, world_mapdata)

    # Create the map
    fig = go.Figure(go.Choroplethmap(
        geojson=world_mapdata,
        featureidkey='properties.name',
        locations=[f['properties']['name'] for f in world_mapdata['features']],
        z=color,
        hovertext=[f['properties']['name'] for f in world_mapdata['features']],
        colorscale="Viridis",
        marker_opacity=0.8,
        marker_line_width=0.5
    ))

    # Update layout
    fig.update_geos(
        projection=dict(type="natural earth"),
        showcoastlines=True,
        coastlinecolor="LightGray",
        showland=True,
        landcolor="WhiteSmoke",
        showocean=True,
        oceancolor="LightBlue"
    )
    fig.update_layout(
        title=f"Countries of Origin for Immigrants in {borough_name}",
        title_x=0.5,
        margin=dict(l=0, r=0, t=50, b=0),
        height=600,
        width=900
    )
    return fig