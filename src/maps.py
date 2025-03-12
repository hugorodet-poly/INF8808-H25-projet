import plotly.graph_objects as go

def get_map(districts, demographics, variable, opacity=0.5, zoom='quebec'):
    z = demographics[variable].values
    if demographics[variable].dtype == 'object':
        z = [float(s[:-1].replace(',', '.')) for s in z]
    
    fig = go.Figure(go.Choroplethmap(
        geojson=districts,
        featureidkey='properties.ID',
        locations=[f['properties']['ID'] for f in districts['features']],
        z=z,
        hovertext=[f['properties']['NM_CEP'] for f in districts['features']],
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
            map=dict(center=dict(lat=45.5, lon=-73.6), zoom=9.5),
            width=600, height=800)
    else:
        raise ValueError('Invalid zoom value. Use "quebec" or "montreal".')    
    return fig