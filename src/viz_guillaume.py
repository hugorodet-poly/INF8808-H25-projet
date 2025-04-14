import pandas as pd
import plotly.graph_objects as go

from src.maps import get_map, circo_subsets


def stacked_bar_chart_most(df1, df):
    """df1 = demographics data
    df = elections data"""

    df1['Immigrants'] = pd.to_numeric(df1['Immigrants'])

    y_data = df1.nlargest(10, 'Immigrants').set_index('Circonscription')['Immigrants'].keys().tolist()
    y_data.reverse()

    top_labels = df['abreviationPartiPolitique'].value_counts().nlargest(5).keys().tolist()
    top_labels.append('Others')

    x_data = []
    for circ in y_data:
        circ_data = []
        for party in top_labels:
            if party != 'Others':
                try:
                    vote_percentage = df.loc[
                        (df['abreviationPartiPolitique'] == party) & (
                                df['nomCirconscription'] == circ), 'tauxVote'].values[
                        0]
                    circ_data.append(round(float(vote_percentage), 1))
                except IndexError:
                    circ_data.append(0.0)  # Default value if party not found
            else:  # Handle the 'Others' category
                other_parties_votes = df.loc[
                    (df['nomCirconscription'] == circ) & (
                        ~df['abreviationPartiPolitique'].isin(top_labels[:-1])), 'tauxVote'].sum()
                circ_data.append(round(float(other_parties_votes), 1))
        x_data.append(circ_data)

    colors = ['rgba(0, 169, 230, 0.8)', 'rgba(35, 41, 100, 0.8)',
              'rgba(20, 41, 80, 0.8)', 'rgba(236, 25, 44, 0.8)',
              'rgba(255, 85, 4, 0.8)', 'rgba(127, 127, 127, 0.8)']

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                ),
                hovertemplate='%{x}%',
                name=''
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=120, r=10, t=140, b=80),
        showlegend=False,
    )

    annotations = []
    shift = 100 / 7

    for yd, xd in zip(y_data, x_data):
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        if xd[0] >= 5:
            annotations.append(dict(xref='x', yref='y',
                                    x=xd[0] / 2, y=yd,
                                    text=str(xd[0]) + '%',
                                    font=dict(family='Arial', size=14,
                                              color='rgb(248, 248, 255)'),
                                    showarrow=False))
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=shift, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='Arial', size=21, weight='bold',
                                              color=colors[0]),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
            if xd[i] >= 5:
                annotations.append(dict(xref='x', yref='y',
                                        x=space + (xd[i] / 2), y=yd,
                                        text=str(xd[i]) + '%',
                                        font=dict(family='Arial', size=14,
                                                  color='rgb(248, 248, 255)'),
                                        showarrow=False))
            if yd == y_data[-1]:
                annotations.append(dict(xref='x', yref='paper',
                                        x=shift * (i + 1), y=1.1,
                                        text=top_labels[i],
                                        font=dict(family='Arial', size=21, weight='bold',
                                                  color=colors[i]),
                                        showarrow=False))
            space += xd[i]

    fig.update_layout(annotations=annotations,
                      margin=dict(t=200),
                      title_text="Répartition des votes dans les circonscriptions avec le plus d'immigrants",
                      title_x=0.5,
                      title_y=0.95,
                      title_yanchor='top',
                      title_font=dict(size=32, weight='bold'),
                      )
    return fig


def stacked_bar_chart_least(df1, df):
    """df1 = demographics data
    df = elections data"""

    df1['Immigrants'] = pd.to_numeric(df1['Immigrants'])

    y_data = df1.nsmallest(10, 'Immigrants').set_index('Circonscription')['Immigrants'].keys().tolist()
    y_data.reverse()


    top_labels = df['abreviationPartiPolitique'].value_counts().nlargest(5).keys().tolist()
    top_labels.append('Others')

    x_data = []
    for circ in y_data:
        circ_data = []
        for party in top_labels:
            if party != 'Others':
                try:
                    vote_percentage = df.loc[
                        (df['abreviationPartiPolitique'] == party) & (
                                df['nomCirconscription'] == circ), 'tauxVote'].values[
                        0]
                    circ_data.append(round(float(vote_percentage), 1))
                except IndexError:
                    circ_data.append(0.0)  # Default value if party not found
            else:  # Handle the 'Others' category
                other_parties_votes = df.loc[
                    (df['nomCirconscription'] == circ) & (
                        ~df['abreviationPartiPolitique'].isin(top_labels[:-1])), 'tauxVote'].sum()
                circ_data.append(round(float(other_parties_votes), 1))
        x_data.append(circ_data)

    colors = ['rgba(0, 169, 230, 0.8)', 'rgba(35, 41, 100, 0.8)',
              'rgba(20, 41, 80, 0.8)', 'rgba(236, 25, 44, 0.8)',
              'rgba(255, 85, 4, 0.8)', 'rgba(127, 127, 127, 0.8)']

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                ),
                hovertemplate='%{x}%',
                name=''
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=120, r=10, t=140, b=80),
        showlegend=False,
    )

    annotations = []
    shift = 100 / 7

    for yd, xd in zip(y_data, x_data):
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial', size=14,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        if xd[0] >= 5:
            annotations.append(dict(xref='x', yref='y',
                                    x=xd[0] / 2, y=yd,
                                    text=str(xd[0]) + '%',
                                    font=dict(family='Arial', size=14,
                                              color='rgb(248, 248, 255)'),
                                    showarrow=False))
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=shift, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='Arial', size=21, weight='bold',
                                              color=colors[0]),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
            if xd[i] >= 5:
                annotations.append(dict(xref='x', yref='y',
                                        x=space + (xd[i] / 2), y=yd,
                                        text=str(xd[i]) + '%',
                                        font=dict(family='Arial', size=14,
                                                  color='rgb(248, 248, 255)'),
                                        showarrow=False))
            if yd == y_data[-1]:
                annotations.append(dict(xref='x', yref='paper',
                                        x=shift * (i + 1), y=1.1,
                                        text=top_labels[i],
                                        font=dict(family='Arial', size=21, weight='bold',
                                                  color=colors[i]),
                                        showarrow=False))
            space += xd[i]

    fig.update_layout(annotations=annotations,
                      margin=dict(t=200),
                      title_text="Répartition des votes dans les circonscriptions avec le moins d'immigrants",
                      title_x=0.5,
                      title_y=0.95,
                      title_yanchor='top',
                      title_font=dict(size=32, weight='bold'),
                      )
    return fig


def linguistic_map(df, map_data):
    """df = demographics data, map_data for districts"""

    # mask = get_subset_mask(df['Circonscription'], circo_subsets['Montréal'])
    # color = df['Immigrants'].values
    # color[~mask] = None

    # Code above doesn't work outside of notebook for some reason
    district_mapping = {row['Circonscription']: i for i, row in df.iterrows()}
    color = [None] * len(map_data['features'])

    for i, feature in enumerate(map_data['features']):
        district_name = feature['properties']['NM_CEP']
        district_name = district_name.replace("A(c)", "e")
        district_name = district_name.replace("AC/ce", "ace")
        if district_name in district_mapping and district_name in circo_subsets['Montréal']:
            color[i] = df.loc[district_mapping[district_name], "Ni l'anglais ni le francais (pourcentage)"]

    fig = get_map(map_data, color, zoom='montreal')
    fig.update_layout(
        title_text="Proportion de personnes parlant ni le français ni l'anglais dans les circonscriptions de Montréal",
        title_x=0.5,
        title_yanchor='top',
        title_font=dict(size=21, weight='bold'),
        height=400,
        width=600,
    )
    fig.data[0].colorbar = dict(ticksuffix="%")
    return fig


def immigrants_map(df, map_data):
    """df = demographics data, map_data for districts"""

    # mask = get_subset_mask(df['Circonscription'], circo_subsets['Montréal'])
    # color = df['Immigrants'].values
    # color[~mask] = None

    # Code above doesn't work outside of notebook for some reason
    district_mapping = {row['Circonscription']: i for i, row in df.iterrows()}
    color = [None] * len(map_data['features'])

    # for i, feature in enumerate(map_data['features']):
    #     district_name = feature['properties']['NM_CEP']
    #     district_name = district_name.replace("A(c)", "e")
    #     district_name = district_name.replace("AC/ce", "ace")
    #     if district_name in district_mapping and district_name in circo_subsets['Montréal']:
    #         color[i] = df.loc[district_mapping[district_name], "Immigrants"]

    fig = get_map(map_data, None)
    # fig.update_layout(title_text='Population immigrante des circonscriptions de Montréal',
    #                   title_x=0.5,
    #                   title_yanchor='top',
    #                   title_font=dict(size=21, weight='bold'),
    #                   height=400,
    #                   width=600,
    #                   )
    # fig.data[0].colorbar = dict(ticksuffix="%")
    return fig
