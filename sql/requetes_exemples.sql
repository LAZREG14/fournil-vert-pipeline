-- Trois requêtes simples pour la démonstration de la vidéo V06.
USE fournil_vert;

-- 1. Les ventes de la semaine, boutique par boutique
SELECT * FROM ventes_jour ORDER BY boutique_id, date_vente;

-- 2. Le CA de la semaine par boutique
SELECT b.ville, SUM(v.ca_ttc_eur) AS ca_semaine_eur
FROM ventes_jour v
JOIN boutiques b ON b.boutique_id = v.boutique_id
GROUP BY b.ville;

-- 3. Le dataset final, prêt pour Power BI : ventes, invendus et météo réunis
SELECT * FROM v_dataset_final ORDER BY boutique_id, date_vente;
