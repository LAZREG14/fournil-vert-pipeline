# Journal d'utilisation de l'IA

Chaque ligne garde la trace d'un échange utile avec une IA générative (ChatGPT ou Claude) : ce que j'ai gardé, et surtout ce que j'ai refusé.

| Date | Prompt utilisé | Ce que j'ai gardé | Ce que j'ai refusé, et pourquoi |
| --- | --- | --- | --- |
| 2026-10-19 | P2 — problématique | La forme « Comment ajuster la production… pour réduire les invendus sans ruptures ? » | « Analyser l'impact de la météo sur les ventes » : pas de décision ni d'utilisateur |
| 2026-10-19 | P3 — sources | L'API Open-Meteo, gratuite et sans clé (documentation ouverte et testée dans le navigateur) | Une API météo payante, et un « fichier INSEE des ventes de boulangerie » qui n'existe pas |
| 2026-10-19 | P4 — architecture | Le découpage en 7 étapes, la table `meteo_jour` | Airflow pour planifier la collecte : trop complexe, un script lancé chaque matin suffit |
| 2026-10-19 | P5 — critique | La remarque sur le grain du dataset final, que j'ai précisé : 1 ligne = 1 boutique × 1 jour | — |
| 2026-10-20 | P7 — README | La structure et la rédaction de la partie Contexte | Deux phrases creuses (« solution innovante et scalable ») ; ajout du KPI taux d'invendus oublié |
