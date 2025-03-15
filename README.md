# INF8808-H25-projet

## Installation des dépendances

Avant d'exécuter les scripts, assurez-vous d'installer les dépendances nécessaires. Exécutez la commande suivante pour installer toutes les bibliothèques listées dans le fichier requirements.txt :
```
pip install -r requirements.txt
```

## Cartes

Cartes stockées dans `assets/maps` et disponibles à [ce lien](https://drive.google.com/drive/folders/1MC0MJos7DbcWdHZJY9pthtZptjLbz-QT?usp=sharing).
- `districts_QC.geojson` : Les districts électoraux pour tout le québec.
- `districts_montreal.geojson` : Les districts électoraux uniquement de la Ville de Montréal (donc il y a des trous). Techniquement un sous-ensemble du précédent, mais a été utile à un moment. Ne sera pas nécessaire dans la version finale.
- `arrondissements_montreal.geojson` : les frontières des arrondissements, différentes de celles des districts électoraux./

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
   
