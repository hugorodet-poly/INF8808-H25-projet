import pandas as pd
import plotly.graph_objects as go
from preprocess import get_elections_data, get_demographics_data

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


# Get demographics and elections data
df_demo = get_demographics_data()
df_elec = get_elections_data()

# Get distict names with most francophones, anglophones, bilinguals and neither
districts_fr = get_district_names(df_demo, 5, "Francais")
districts_en = get_district_names(df_demo, 5, "Anglais")
districts_both = get_district_names(df_demo, 5, "Francais et anglais (pourcentage)")
districts_neither = get_district_names(df_demo, 5, "Ni l'anglais ni le francais (pourcentage)")

# Filter and sort the elections data for the selected districts and parties
parties = ['C.A.Q.-E.F.L.', 'P.C.Q-E.E.D.', 'P.L.Q./Q.L.P.', 'P.Q.', 'Q.S.']
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


# Create vizualization
def create_interactive_connected_dot_plot(df):
    # Get unique language values
    languages = df['Langue'].unique()
    
    fig = go.Figure()
    
    # Create traces for each possible combination, avoiding duplicates
    visible_traces = {}
    combinations = []
    
    # Create unique combinations without duplicates
    processed_pairs = set()
    for lang1 in languages:
        for lang2 in languages:
            if lang1 != lang2:
                # Sort languages to ensure consistent ordering
                sorted_langs = tuple(sorted([lang1, lang2]))
                if sorted_langs not in processed_pairs:
                    processed_pairs.add(sorted_langs)
                    # Put Anglais vs Français first
                    if set(sorted_langs) == {'Anglophones', 'Francophones'}:
                        combinations.insert(0, sorted_langs)
                    else:
                        combinations.append(sorted_langs)
    
    # Create pivot table
    df_pivot = create_pivot_data(df)
    
    # Create traces for all combinations
    for lang1, lang2 in combinations:
        key = f"{lang1}_vs_{lang2}"
        traces = []
        
        # Add connecting lines
        for parti in df_pivot.index:
            traces.append(go.Scatter(
                x=[df_pivot.loc[parti, lang1], df_pivot.loc[parti, lang2]],
                y=[parti, parti],
                mode='lines',
                line=dict(color='black', width=3),
                showlegend=False,
                visible=(set([lang1, lang2]) == {'Anglophones', 'Francophones'})
            ))
            
            # Add invisible point for gap hover
            ecart = abs(df_pivot.loc[parti, lang1] - df_pivot.loc[parti, lang2])
            traces.append(go.Scatter(
                x=[(df_pivot.loc[parti, lang1] + df_pivot.loc[parti, lang2]) / 2],
                y=[parti],
                mode='markers',
                marker=dict(size=15, color='rgba(0,0,0,0)'),
                text=f"Ecart : {ecart:.2f}%",
                hoverinfo="text",
                showlegend=False,
                visible=(set([lang1, lang2]) == {'Anglophones', 'Francophones'})
            ))
        
        # Add points for first language
        traces.append(go.Scatter(
            x=df_pivot[lang1],
            y=df_pivot.index,
            name=f'Quartiers principalement {lang1.lower()}',
            mode='markers',
            marker=dict(color='blue', size=12, line=dict(color='black', width=1)),
            text=[f"{lang1} | Votes : {v:.2f}%" for v in df_pivot[lang1]],
            hoverinfo="text",
            visible=(set([lang1, lang2]) == {'Anglophones', 'Francophones'})
        ))
        
        # Add points for second language
        traces.append(go.Scatter(
            x=df_pivot[lang2],
            y=df_pivot.index,
            name=f'Quartiers principalement {lang2.lower()}',
            mode='markers',
            marker=dict(color='red', size=12, line=dict(color='black', width=1)),
            text=[f"{lang2} | Votes : {v:.2f}%" for v in df_pivot[lang2]],
            hoverinfo="text",
            visible=(set([lang1, lang2]) == {'Anglophones', 'Francophones'})
        ))
        
        visible_traces[key] = traces
        for trace in traces:
            fig.add_trace(trace)
    
    # Create dropdown menu
    dropdown_buttons = []
    for key in visible_traces.keys():
        lang1, lang2 = key.split("_vs_")
        visibility = [False] * len(fig.data)
        
        start_idx = list(visible_traces.keys()).index(key) * len(visible_traces[key])
        for i in range(len(visible_traces[key])):
            visibility[start_idx + i] = True
            
        dropdown_buttons.append(dict(
            args=[{"visible": visibility}],
            label=f"{lang1} vs {lang2}",
            method="update"
        ))
    
    # Rest of the layout remains the same as before
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=dropdown_buttons,
                direction="down",
                showactive=True,
                x=0.1,
                y=1.15,
                xanchor="left",
                yanchor="top"
            )
        ],
        title=dict(
            text="Comparaison des votes par groupe linguistique aux élections québécoises de 2022",
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            title='Pourcentage des suffrages exprimés',
            showgrid=True,
            showline=True,
            linecolor='black',
            tickfont_color='black',
            showticklabels=True,
            dtick=10,
            ticks='outside',
            tickcolor='black'
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
        margin=dict(l=150, r=40, b=50, t=120),
        legend=dict(font_size=10, yanchor='bottom', xanchor='right'),
        width=1000,
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='rgba(192, 203, 238, 0.5)',
        hovermode='closest'
    )
    
    return fig

# Create and show the plot
fig = create_interactive_connected_dot_plot(df_elec)
fig.show()