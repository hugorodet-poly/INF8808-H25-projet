import os
import os.path as osp
import numpy as np
import pandas as pd

SRC_DIRPATH = 'assets/data/immigration_extracted_csvs'
DST_FPATH = 'assets/data/arrondissements.csv'

# Translate the names from those of the immigration/neighborhoods CSV to those of the GeoJSON
CLEAN_NAMES = {
    'Agglomération de Montréal': 'Agglomération de Montréal',
    'Ville de Montréal': 'Ville de Montréal',
    
    'Ahuntsic-Cartierville': 'Ahuntsic-Cartierville',
    'Anjou': 'Anjou',
    'Cte-des-NeigesNotre-Dame-de-Grce':'Côte-des-Neiges, Notre-Dame-de-Grâce',
    'L\'le-BizardSainte-Genevive': 'L\'Île-Bizard, Sainte-Geneviève',
    'LaSalle': 'LaSalle',
    'Lachine': 'Lachine',
    'MercierHochelaga-Maisonneuve': 'Mercier, Hochelaga-Maisonneuve', 
    'Montral-Nord':'Montréal-Nord',
    'Outremont': 'Outremont',
    'Pierrefonds-Roxboro': 'Pierrefonds-Roxboro',
    'Rivire-des-PrairiesPointe-aux-Trembles': 'Rivière-des-Prairies, Pointe-aux-Trembles',
    'RosemontLa': 'Rosemont, La Petite-Patrie',
    'Saint-Laurent': 'Saint-Laurent',
    'Saint-Lonard': 'Saint-Léonard',
    'Verdun': 'Verdun',
    'Ville-Marie': 'Ville-Marie',
    'VilleraySaint-MichelParc-Extension': 'Villeray, Saint-Michel, Parc-Extension',
    'Le_Plateau-Mont-Royal': 'Le Plateau-Mont-Royal',
    'Le_Sud-Ouest': 'Le Sud-Ouest'}

csv_fnames = os.listdir(SRC_DIRPATH)
arrond_names = np.unique([s.split('_')[0] for s in csv_fnames]).tolist()
arrond_names.pop(arrond_names.index('Le'))
arrond_names.append('Le_Plateau-Mont-Royal')
arrond_names.append('Le_Sud-Ouest')

# Name are all bugged, clean them
def clean(s):
    s = s.replace('â', '\'').replace('É¯', 'ï').replace('names_to_append', 'ï')
    s = s.strip().replace('Ã©', 'é').replace('Ã´', 'ô').replace('Ã\xa0', 'à')
    s = s.replace('Ã§', 'ç').replace('Ã¢', 'â').replace('Ã¨', 'è')
    s = s.replace('&nbsp', '').replace('Ã\x89', 'É').replace('\x80\x99', '')
    return s

# Some have more columns bc they include percentage and number. We juste care about the number, we can compute the % ourselves
def unify(s):
    return s.replace('Nombre_', '')
def get_csv_number(fname):
    return int(fname.split('_')[-1].split('.')[0])

# Read and clean
def get_csv(fname):
    df = pd.read_csv(osp.join(SRC_DIRPATH, fname), sep=',')
    df.columns = [unify(clean(s)) for s in df.columns]
    df['Catégorie'] = df['Catégorie'].map(clean)
    return df

# Get columns names and values for Montréal globally
col_names = ['Arrondissement']
values_agglo = ['Agglomération de Montréal']
values_ville = ['Ville de Montréal']
candidates = [s for s in csv_fnames if s.startswith(arrond_names[0])]
candidates.sort(key=lambda s: get_csv_number(s))
for csv_fname in candidates:
    df = get_csv(csv_fname)
    
    # Half-manual modification to the names because it's not displayed inside the CSVs
    names_to_append = df['Catégorie'].values.tolist() 
    if get_csv_number(csv_fname)//3 == 3:
        names_to_append = ["Non permamente, " + name for name in names_to_append]
    elif get_csv_number(csv_fname)//3 == 4:
        names_to_append = ["Âge à l'immigration, " + name for name in names_to_append]
    elif get_csv_number(csv_fname)//3 == 6:
        names_to_append = ["Imigration récente (entre 2016 et 2021), " + name for name in names_to_append]    
    elif get_csv_number(csv_fname)//3 == 11: 
        names_to_append = ["Non permanente, " + name for name in names_to_append]   
        
    if get_csv_number(csv_fname)%3 == 1:
        col_names += [name + ' - Hommes' for name in names_to_append]
    elif get_csv_number(csv_fname)%3 == 2:
        col_names += [name + ' - Femmes' for name in names_to_append]
    else:
        col_names += names_to_append
        
    values_agglo += df['Agglomération de Montréal'].values.tolist()
    values_ville += df['Ville de Montréal'].values.tolist()

# Create the dataframe with the data from mtl
main_df =  pd.DataFrame(
    data = np.array([values_agglo, values_ville]),
    columns=col_names)

# Get values for each arrondissement
for arrond_name in arrond_names:
    values = [arrond_name]

    candidates = [s for s in csv_fnames if s.startswith(arrond_name)]
    candidates.sort(key=lambda s: get_csv_number(s))
    for csv_fname in candidates:
        df_arrond = get_csv(csv_fname)
        
        arrond_col_name = df_arrond.columns[-2] if len(df_arrond.columns) == 7 else df_arrond.columns[-1]
        values += df_arrond[arrond_col_name].values.tolist()
    df = pd.DataFrame(
        data = np.array([values]),
        columns=col_names)
    main_df = pd.concat([main_df, df])

# Clean up the names
main_df['Arrondissement'] = main_df['Arrondissement'].map(lambda s: CLEAN_NAMES[s])

main_df.to_csv(DST_FPATH, index=False)