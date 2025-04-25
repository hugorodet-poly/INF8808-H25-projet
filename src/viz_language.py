import pandas as pd
import plotly.graph_objects as go

def get_district_names(df, num, criteria):
    """
    Get the district names that are in the top num of the criteria
    :param df: the dataframe
    :param num: the number of neighbourhoods to get
    :param criteria: the criteria to use
    :return: the neighbourhoods names
    """
    df = df.sort_values(criteria, ascending=False)
    neighbourhoods = df['Circonscription'][:num].tolist()
    return neighbourhoods

def get_average_votes(df):
    """
    Get the average votes for each party in the dataframe
    :param df: the dataframe
    :return: the average votes for each party
    """
    df = df.groupby(['abreviationPartiPolitique'])['tauxVote'].mean().reset_index()
    return df

def create_pivot_data(df):
    """
    Create a pivot table from the input dataframe
    """
    return df.pivot(index='Parti politique', 
                   columns='Langue', 
                   values='Taux de vote')

def generate_districts_annotation(districts_dict, lang1, lang2):
    text = "<b>Circonscriptions principalement...</b><br><br>"
    text += f"<b><span style='color:blue'>{lang1}:</span></b><br>"
    for d in districts_dict[lang1]:
        text += f"<span style='color:blue'>• {d}</span><br>"
    text += "<br>"
    text += f"<b><span style='color:red'>{lang2}:</span></b><br>"
    for d in districts_dict[lang2]:
        text += f"<span style='color:red'>• {d}</span><br>"
    return text


def prepare_dataframes(df_demo, df_elec):
    # Get distict names with most francophones, anglophones, bilinguals and neither
    NUM_DISTRICTS = 4
    districts_fr = get_district_names(df_demo, NUM_DISTRICTS, "Francais")
    districts_en = get_district_names(df_demo, NUM_DISTRICTS, "Anglais")
    districts_both = get_district_names(df_demo, NUM_DISTRICTS, "Francais et anglais (pourcentage)")
    districts_neither = get_district_names(df_demo, NUM_DISTRICTS, "Ni l'anglais ni le francais (pourcentage)")

    # Create districts dictionary
    districts_dict = {
        'Francophones': districts_fr,
        'Anglophones': districts_en,
        'Allophones': districts_both,
        'Ni francophones ni anglophones': districts_neither
    }

    # Rename parties ('C.A.Q.-E.F.L.' to 'C.A.Q.', 'P.C.Q-E.E.D.' to 'P.C.Q.', 'P.L.Q./Q.L.P.' to 'P.L.Q.')
    rename_dict = {'C.A.Q.-E.F.L.': 'C.A.Q.', 'P.C.Q-E.E.D.': 'P.C.Q.', 'P.L.Q./Q.L.P.': 'P.L.Q.'}
    df_elec['abreviationPartiPolitique'] = df_elec['abreviationPartiPolitique'].replace(rename_dict)

    # Filter and sort the elections data for the selected districts and parties
    parties = ['C.A.Q.', 'P.C.Q.', 'P.L.Q.', 'P.Q.', 'Q.S.']
    df_elec_fr = df_elec[(df_elec['nomCirconscription'].isin(districts_fr)) & (df_elec['abreviationPartiPolitique'].isin(parties))]
    df_elec_fr = df_elec_fr.sort_values(['nomCirconscription', 'numeroPartiPolitique'])
    df_elec_en = df_elec[(df_elec['nomCirconscription'].isin(districts_en)) & (df_elec['abreviationPartiPolitique'].isin(parties))]
    df_elec_en = df_elec_en.sort_values(['nomCirconscription', 'numeroPartiPolitique'])
    df_elec_both = df_elec[(df_elec['nomCirconscription'].isin(districts_both)) & (df_elec['abreviationPartiPolitique'].isin(parties))]
    df_elec_both = df_elec_both.sort_values(['nomCirconscription', 'numeroPartiPolitique'])
    df_elec_neither = df_elec[(df_elec['nomCirconscription'].isin(districts_neither)) & (df_elec['abreviationPartiPolitique'].isin(parties))]
    df_elec_neither = df_elec_neither.sort_values(['nomCirconscription', 'numeroPartiPolitique'])

    # Get the average votes for each party
    df_elec_fr = get_average_votes(df_elec_fr)
    df_elec_en = get_average_votes(df_elec_en)
    df_elec_both = get_average_votes(df_elec_both)
    df_elec_neither = get_average_votes(df_elec_neither)

    # Add the language column to each dataframe
    df_elec_fr['Langue'] = 'Francophones'
    df_elec_en['Langue'] = 'Anglophones'
    df_elec_both['Langue'] = 'Allophones'
    df_elec_neither['Langue'] = 'Ni francophones ni anglophones'
    df_elec = pd.concat([df_elec_fr, df_elec_en, df_elec_both, df_elec_neither], ignore_index=True)
    df_elec = df_elec.rename(columns={'abreviationPartiPolitique': 'Parti politique', 'tauxVote': 'Taux de vote'})
    df_elec = df_elec[['Langue', 'Parti politique', 'Taux de vote']]

    return districts_dict, df_elec

def get_language_dropdown_options():
    options = [
        'Anglophones VS. Francophones',
        'Allophones VS. Francophones',
        'Allophones VS. Anglophones',
        'Francophones VS. Ni francophones ni anglophones',
        'Anglophones VS. Ni francophones ni anglophones',
        'Allophones VS. Ni francophones ni anglophones',
    ]
    return options

# Create vizualization
def create_interactive_connected_dot_plot(df_demo, df_elec, lang_option):
    
    districts_dict, df = prepare_dataframes(df_demo, df_elec)
    
    # Create a figure
    fig = go.Figure()
    
    lang1, lang2 = lang_option.split(" VS. ")
 
    # Create pivot table
    df_pivot = create_pivot_data(df)
        
    # Add connecting lines
    for parti in df_pivot.index:
        fig.add_trace(go.Scatter(
            x=[df_pivot.loc[parti, lang1], df_pivot.loc[parti, lang2]],
            y=[parti, parti],
            mode='lines',
            line=dict(color='black', width=3),
            showlegend=False,
        ))
        # Add invisible point for gap hover
        ecart = abs(df_pivot.loc[parti, lang1] - df_pivot.loc[parti, lang2])
        fig.add_trace(go.Scatter(
            x=[(df_pivot.loc[parti, lang1] + df_pivot.loc[parti, lang2]) / 2],
            y=[parti],
            mode='markers',
            marker=dict(size=15, color='rgba(0,0,0,0)'),
            text=f"Ecart : {ecart:.2f}%",
            hoverinfo="text",
            showlegend=False,
        ))
    # Add points for first language
    fig.add_trace(go.Scatter(
        x=df_pivot[lang1],
        y=df_pivot.index,
        name=f'Circonscriptions principalement {lang1.lower()}',
        mode='markers',
        marker=dict(color='blue', size=12, line=dict(color='black', width=1)),
        text=[f"{lang1} | Votes : {v:.2f}%" for v in df_pivot[lang1]],
        hoverinfo="text",
    ))
    # Add points for second language
    fig.add_trace(go.Scatter(
        x=df_pivot[lang2],
        y=df_pivot.index,
        name=f'Circonscriptions principalement {lang2.lower()}',
        mode='markers',
        marker=dict(color='red', size=12, line=dict(color='black', width=1)),
        text=[f"{lang2} | Votes : {v:.2f}%" for v in df_pivot[lang2]],
        hoverinfo="text",
    ))
        
    fig.update_layout(
        xaxis=dict(
            title='Pourcentage des suffrages exprimés',
            showgrid=True,
            showline=True,
            linecolor='black',
            tickfont_color='black',
            showticklabels=True,
            dtick=10,
            ticks='outside',
            tickcolor='black',
            autorange=False,  # Set autorange to False to define a fixed range
            range=[0, 60]
        ),
        yaxis=dict(
            title='Principaux partis politiques québécois',
            showgrid=False,
            linecolor='black',
            tickfont_color='black',
            showticklabels=True,
            ticks='outside',
            tickcolor='black',
            autorange="reversed"
        ),
        margin=dict(l=150, r=250, b=50, t=20),
        legend=dict(font_size=10, yanchor='top', xanchor='left'),
        width=1300,
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='rgba(192, 203, 238, 0.5)',
        hovermode='closest'
    )
    # Add Districts annotation
    annotation = generate_districts_annotation(districts_dict, lang1, lang2)
    fig.update_layout(
        annotations=[
            dict(
                text=annotation,
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.02,
                y=0.5,
                xanchor='left',
                yanchor='middle',
                font=dict(size=12),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='black',
                borderwidth=1
            )
        ]
    )
    fig.update_layout(
        title='Comparaison des votes par groupe linguistique aux élections québécoises de 2022',
        title_x=0.5,
        margin=dict(t=100)
    )
    return fig