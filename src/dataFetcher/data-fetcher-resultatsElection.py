import requests
import json
import csv

json_url = "https://donnees.electionsquebec.qc.ca/production/provincial/resultats/archives/gen2022-10-03/resultats.json"
csv_output_file = "resultats.csv"

response = requests.get(json_url)

if response.status_code == 200:
    data = response.json()  # data is a dict with keys "statistiques" and "circonscriptions"
    
    # Extract the list of circonscriptions
    circonscriptions = data["circonscriptions"]
    
    fieldnames = [
        "numeroCirconscription", 
        "nomCirconscription", 
        "nbBureauComplete", 
        "nbBureauTotal",
        "nbVoteValide", 
        "nbVoteRejete",
        "nbVoteExerce",
        "nbElecteurInscrit",
        "tauxVoteValide",
        "tauxVoteRejete",
        "tauxParticipation",
        "numeroCandidat",
        "nomCandidat",
        "prenomCandidat",
        "numeroPartiPolitique",
        "abreviationPartiPolitique",
        "nbVoteTotal",
        "tauxVote",
        "nbVoteAvance"
    ]
    
    with open(csv_output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Now iterate over each circonscription in the list
        for circonscription in circonscriptions:
            
            # Top-level fields
            cir_num = circonscription.get("numeroCirconscription", "")
            cir_nom = circonscription.get("nomCirconscription", "")
            nb_bureau_complete = circonscription.get("nbBureauComplete", "")
            nb_bureau_total = circonscription.get("nbBureauTotal", "")
            nb_vote_valide = circonscription.get("nbVoteValide", "")
            nb_vote_rejete = circonscription.get("nbVoteRejete", "")
            nb_vote_exerce = circonscription.get("nbVoteExerce", "")
            nb_electeur_inscrit = circonscription.get("nbElecteurInscrit", "")
            taux_vote_valide = circonscription.get("tauxVoteValide", "")
            taux_vote_rejete = circonscription.get("tauxVoteRejete", "")
            taux_participation = circonscription.get("tauxParticipation", "")
            
            candidats = circonscription.get("candidats", [])
            for candidat in candidats:
                row = {
                    "numeroCirconscription": cir_num,
                    "nomCirconscription": cir_nom,
                    "nbBureauComplete": nb_bureau_complete,
                    "nbBureauTotal": nb_bureau_total,
                    "nbVoteValide": nb_vote_valide,
                    "nbVoteRejete": nb_vote_rejete,
                    "nbVoteExerce": nb_vote_exerce,
                    "nbElecteurInscrit": nb_electeur_inscrit,
                    "tauxVoteValide": taux_vote_valide,
                    "tauxVoteRejete": taux_vote_rejete,
                    "tauxParticipation": taux_participation,
                    "numeroCandidat": candidat.get("numeroCandidat", ""),
                    "nomCandidat": candidat.get("nom", ""),
                    "prenomCandidat": candidat.get("prenom", ""),
                    "numeroPartiPolitique": candidat.get("numeroPartiPolitique", ""),
                    "abreviationPartiPolitique": candidat.get("abreviationPartiPolitique", ""),
                    "nbVoteTotal": candidat.get("nbVoteTotal", ""),
                    "tauxVote": candidat.get("tauxVote", ""),
                    "nbVoteAvance": candidat.get("nbVoteAvance", "")
                }
                writer.writerow(row)
    
    print(f"CSV data flattened and saved to {csv_output_file}")

else:
    print(f"Failed to download JSON data. Status code: {response.status_code}")
