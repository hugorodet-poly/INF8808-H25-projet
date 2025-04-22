# INF8808-H25-projet: Tableau de Bord Démographique et Électoral de Montréal

## Présentation

Cette application web interactive analyse la relation entre les modèles d'immigration, la diversité linguistique et le comportement électoral à Montréal et au Québec. Le tableau de bord visualise les données démographiques et les tendances de vote pour explorer comment la diversité culturelle influence la représentation politique.

## Architecture Technique

- **Framework**: Construit avec Dash (framework d'application web Python)
- **Traitement des données**: Pipeline de traitement en Python avec pandas, geopandas
- **Visualisations**: Plotly, Mapbox pour les cartes interactives

## Installation des dépendances

Avant d'exécuter les scripts, assurez-vous d'installer les dépendances nécessaires. Nous utilisons *Python 3.10.16*. Exécutez la commande suivante pour installer toutes les bibliothèques listées dans le fichier `requirements.txt` :
```bash
pip install -r requirements.txt
```

Pour lancer l'application :
```bash
python app.py
```
Puis ouvrez votre navigateur à l'adresse http://127.0.0.1:8050/

## Structure et Fonctionnalités du Tableau de Bord

### 1. Immigration à Montréal
- **Carte interactive**: Affiche la répartition des immigrants par circonscription électorale
- **Pays d'origine**: Visualisation interactive montrant les liens entre les arrondissements de Montréal et les pays d'origine des immigrants
  - **Interaction**: Cliquez sur n'importe quel arrondissement pour voir les principaux pays d'origine

### 2. Répartition des langues
- **Carte linguistique**: Montre la distribution des personnes ne parlant ni français ni anglais à la maison
- **Graphique à points connectés**: Compare les tendances de vote entre les groupes linguistiques
  - **Interaction**: Utilisez le menu déroulant pour sélectionner différentes variables linguistiques

### 3. Analyse de la représentation électorale
- **Graphiques en gaufre**: Représentation visuelle de la distribution des sièges à l'Assemblée nationale
  - Représentation à l'échelle du Québec
  - Représentation spécifique à Montréal
  - Visualisation d'un scénario hypothétique
- **Immigration et participation électorale**: Analyse des tendances de vote dans les zones à différents niveaux d'immigration
- **Relation revenu-vote**:
  - **Interaction**: Sélectionnez différents partis politiques pour voir la corrélation avec les niveaux de revenu

### 4. Comportements de vote selon le taux d'immigration
- **Graphiques à barres empilées**: Comparent les préférences électorales dans les circonscriptions à fort vs faible taux d'immigration

## Cartes

Cartes stockées dans `assets/maps` et disponibles à [ce lien](https://drive.google.com/drive/folders/1MC0MJos7DbcWdHZJY9pthtZptjLbz-QT?usp=sharing).
- `districts_QC.geojson` : Les districts électoraux pour tout le québec.
- `districts_montreal.geojson` : Les districts électoraux uniquement de la Ville de Montréal (donc il y a des trous). Techniquement un sous-ensemble du précédent, mais a été utile à un moment. Ne sera pas nécessaire dans la version finale.
- `arrondissements_montreal.geojson` : les frontières des arrondissements, différentes de celles des districts électoraux.
- `countries.geojson` : les frontières des pays. Utile pour visualiser d'où viennent les gens à Montréal.

## Datasets

Datasets stockés dans `assets/data` et disponibles au téléchargement via script (cf. section suivante).

- `donneesSocio2021.csv` : Données démographiques des circonscriptions
- `arrondissements.csv` : Les données sur les arrondissements, dans un seul tableau.
- `resultats-bureau-vote` : Le vote par circonscription, données prises ici : https://www.electionsquebec.qc.ca/resultats-et-statistiques/resultats-generales/2022-10-03/338/
- `immigration_extracted_csvs` : Répertoire des tableaux démographiques par arrondissement. Plus utilisé.
- [à ignorer pour le moment] `langues.csv` et `langues_metadata.csv` : _Langues utilisées au travail selon les statistiques du revenu d’emploi, le statut d’immigrant et le plus haut certificat, diplôme ou grade : Canada, provinces et territoires, régions métropolitaines de recensement et agglomérations de recensement y compris les parties._ Les fichiers ont été renommés. Disponible ici : https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=9810053001

## Exécution des Scripts

### Téléchargement des données socio-économiques

- Script : `src/dataFetcher/data-fetcher-elections.py`
- Exécution : Simplement exécuter le script pour télécharger les données socio-économiques.

### Téléchargement et Extraction des Données sur l'Immigration

Ordre d'exécution des scripts :

1. `src/dataFetcher/data-fetcher-donnees-quebec.py` - Télécharge les rapports HTML de chaque arrondissement.
2. `src/dataFetcher/extract-data-donnees-quebec.py` - Extrait les tableaux CSV des fichiers HTML téléchargés.
3. `src/dataFetcher/aggregate-neighborhood-data.py` - Agrège les données des tableux CSV en un seul.

### Téléchargement des donnés démographiques par circonscription :

`src/dataFetcher/data-fetcher-donneesSocio.py` - Extrait les données démographiques par circonscription électorale.
