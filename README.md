# INF8808-H25-projet

## Installation des dépendances

Avant d'exécuter les scripts, assurez-vous d'installer les dépendances nécessaires. Exécutez la commande suivante pour installer toutes les bibliothèques listées dans le fichier requirements.txt :
```
pip install -r requirements.txt
```

## Datasets

Datasets stockés dans `assets/data`

- `donneesSocio2021.csv` : Données démographiques des circonscriptions
- `immigration_extracted_csvs` : Répertoire des tableaux démographiques par arrondissement
- [à ignorer pour le moment] `langues.csv` et `langues_metadata.csv` : _Langues utilisées au travail selon les statistiques du revenu d’emploi, le statut d’immigrant et le plus haut certificat, diplôme ou grade : Canada, provinces et territoires, régions métropolitaines de recensement et agglomérations de recensement y compris les parties._ Les fichiers ont été renommés. Disponible ici : https://www150.statcan.gc.ca/t1/tbl1/fr/tv.action?pid=9810053001

## Cartes

Cartes stockées dans `assets/maps`
- `districts_montreal.geojson` : Les districts électoraux uniquement de la Ville de Montréal (donc il y a des trous)
- `districts_QC.geojson` : Les districts électoraux pour tout le québec
- `arrondissements_montreal.geojson` : les frontières des arrondissements, différentes de celles des districts électoraux.

## Exécution des Scripts

### Téléchargement des données socio-économiques

- Script : src\dataFetcher\data-fetcher-elections.py
- Exécution : Simplement exécuter le script pour télécharger les données socio-économiques.

### Téléchargement et Extraction des Données sur l'Immigration

#### Ordre d'exécution des scripts :

1. src\dataFetcher\data-fetcher-donnees-quebec.py - Télécharge les rapports HTML de chaque arrondissement.
2. src\dataFetcher\extract-data-donnees-quebec.py - Extrait les tableaux CSV des fichiers HTML téléchargés.
