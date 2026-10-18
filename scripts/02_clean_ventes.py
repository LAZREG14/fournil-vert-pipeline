"""Étape 3 du pipeline (nettoyage / transformation) : réunit les deux exports de caisse.

Entrée : data/raw/caisse_boutique_A.csv et data/raw/caisse_boutique_B.csv
Sortie : data/processed/ventes_propres.csv (une ligne = un article vendu, un seul format)

Lancement, depuis le dossier racine du projet :
    python scripts/02_clean_ventes.py

Ce script sert de démonstration en séquence 1 (vidéo V11 : notebook ou script ?).
Chaque ligne de code sera expliquée en séquence 4.
"""
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
RAW = RACINE / "data" / "raw"
PROCESSED = RACINE / "data" / "processed"

COLONNES = ["ticket_id", "date_vente", "heure", "code_boutique",
            "produit", "famille", "quantite", "montant_ttc"]

# --- Caisse A : euros avec virgule décimale, dates AAAA-MM-JJ, samedi 14 en double
caisse_a = pd.read_csv(RAW / "caisse_boutique_A.csv", sep=";", encoding="utf-8-sig",
                       decimal=",", dtype={"code_boutique": str})
avant = len(caisse_a)
caisse_a = caisse_a.drop_duplicates()
print(f"Caisse A : {avant - len(caisse_a)} lignes en double supprimées")
caisse_a["date_vente"] = pd.to_datetime(caisse_a["date_vente"], format="%Y-%m-%d")

# --- Caisse B : autres noms de colonnes, centimes, dates JJ/MM/AAAA, rayons en majuscules
caisse_b = pd.read_csv(RAW / "caisse_boutique_B.csv", sep=";", encoding="utf-8-sig",
                       dtype={"Magasin": str})
caisse_b = caisse_b.rename(columns={
    "Date": "date_vente", "Heure": "heure", "N° ticket": "ticket_id",
    "Magasin": "code_boutique", "Article": "produit", "Rayon": "famille",
    "Qté": "quantite", "Total TTC": "montant_ttc",
})
caisse_b["date_vente"] = pd.to_datetime(caisse_b["date_vente"], format="%d/%m/%Y")
caisse_b["montant_ttc"] = caisse_b["montant_ttc"] / 100  # centimes -> euros
caisse_b["famille"] = caisse_b["famille"].map({
    "PAIN": "Pains", "VIENNOISERIE": "Viennoiseries",
    "SNACKING": "Snacking", "PATISSERIE": "Pâtisseries",
})
caisse_b["ticket_id"] = "B" + caisse_b["ticket_id"].astype(str)

# --- Empilement des deux caisses dans un format unique
ventes = pd.concat([caisse_a[COLONNES], caisse_b[COLONNES]], ignore_index=True)

PROCESSED.mkdir(parents=True, exist_ok=True)
ventes.to_csv(PROCESSED / "ventes_propres.csv", sep=";", index=False)

print(f"{len(ventes)} lignes enregistrées dans data/processed/ventes_propres.csv")
print("\nCA de la semaine par boutique (€) :")
print(ventes.groupby("code_boutique")["montant_ttc"].sum().round(2).to_string())
