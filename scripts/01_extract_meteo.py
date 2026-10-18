"""Étape 2 du pipeline (collecte) : récupère la météo du jour pour chaque boutique.

Source : API publique Open-Meteo (gratuite, sans clé d'API).
Sortie : une copie brute dans data/raw/meteo_AAAA-MM-JJ.json

Lancement, depuis le dossier racine du projet :
    python scripts/01_extract_meteo.py

Ce script est montré en séquence 1 (vidéo V04) pour illustrer la collecte automatisée.
On apprend à écrire ce type de script en séquence 2.
"""
import json
from datetime import date
from pathlib import Path

import requests

URL_API = "https://api.open-meteo.com/v1/forecast"

# code boutique : (ville, latitude, longitude)
BOUTIQUES = {
    "001": ("Puteaux", 48.884, 2.238),
    "002": ("Courbevoie", 48.897, 2.253),
    "003": ("Nanterre", 48.892, 2.207),
    "004": ("Suresnes", 48.871, 2.225),
    "005": ("Rueil-Malmaison", 48.877, 2.190),
    "006": ("Levallois-Perret", 48.893, 2.288),
}

DOSSIER_RAW = Path(__file__).resolve().parents[1] / "data" / "raw"


def meteo_du_jour(latitude, longitude):
    """Interroge l'API pour un point GPS et renvoie sa réponse (un dictionnaire)."""
    parametres = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,precipitation_sum",
        "timezone": "Europe/Paris",
        "forecast_days": 1,
    }
    reponse = requests.get(URL_API, params=parametres, timeout=10)
    reponse.raise_for_status()  # stoppe le script si l'API renvoie une erreur
    return reponse.json()


def main():
    resultats = []
    for code, (ville, lat, lon) in BOUTIQUES.items():
        donnees = meteo_du_jour(lat, lon)
        donnees["ville"] = ville
        donnees["code_boutique"] = code
        resultats.append(donnees)
        print(f"{ville:<17} {donnees['daily']['temperature_2m_max'][0]:>5} °C   "
              f"{donnees['daily']['precipitation_sum'][0]:>4} mm")

    DOSSIER_RAW.mkdir(parents=True, exist_ok=True)
    fichier = DOSSIER_RAW / f"meteo_{date.today().isoformat()}.json"
    fichier.write_text(json.dumps(resultats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nMétéo de {len(resultats)} villes enregistrée dans {fichier}")


if __name__ == "__main__":
    main()
