-- Base de démonstration du Fournil Vert (vidéo V06).
-- Lancer ce fichier, puis demo_data.sql, dans MySQL Workbench.
-- La modélisation complète et le RGPD sont travaillés en séquence 5.

CREATE DATABASE IF NOT EXISTS fournil_vert CHARACTER SET utf8mb4;
USE fournil_vert;

DROP VIEW IF EXISTS v_dataset_final;
DROP TABLE IF EXISTS production_jour, ventes_jour, meteo_jour, calendrier, boutiques;

-- Les 6 boutiques du réseau (référentiel, mis à jour à la main)
CREATE TABLE boutiques (
    boutique_id  CHAR(3)       PRIMARY KEY,   -- '001' à '006', toujours en texte
    nom          VARCHAR(60)   NOT NULL,
    ville        VARCHAR(60)   NOT NULL,
    latitude     DECIMAL(8,5),
    longitude    DECIMAL(8,5)
);

-- Ventes : 1 ligne = 1 boutique x 1 jour (agrégées depuis les tickets de caisse)
CREATE TABLE ventes_jour (
    date_vente   DATE          NOT NULL,
    boutique_id  CHAR(3)       NOT NULL,
    nb_tickets   INT           NOT NULL,
    qte_vendue   INT           NOT NULL,
    ca_ttc_eur   DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (date_vente, boutique_id),
    FOREIGN KEY (boutique_id) REFERENCES boutiques (boutique_id)
);

-- Production et invendus : 1 ligne = 1 boutique x 1 jour x 1 famille (saisie des gérants)
CREATE TABLE production_jour (
    date_prod    DATE          NOT NULL,
    boutique_id  CHAR(3)       NOT NULL,
    famille      VARCHAR(30)   NOT NULL,
    qte_produite INT           NOT NULL,
    qte_invendue INT           NULL,          -- NULL = non saisi par le gérant
    PRIMARY KEY (date_prod, boutique_id, famille),
    FOREIGN KEY (boutique_id) REFERENCES boutiques (boutique_id)
);

-- Météo : 1 ligne = 1 ville x 1 jour (collectée par scripts/01_extract_meteo.py)
CREATE TABLE meteo_jour (
    date_meteo   DATE          NOT NULL,
    ville        VARCHAR(60)   NOT NULL,
    temp_max_c   DECIMAL(4,1),
    pluie_mm     DECIMAL(5,1),
    PRIMARY KEY (date_meteo, ville)
);

-- Calendrier : 1 ligne = 1 jour
CREATE TABLE calendrier (
    date_jour          DATE        PRIMARY KEY,
    jour_semaine       VARCHAR(10) NOT NULL,
    jour_ferie         BOOLEAN     NOT NULL DEFAULT FALSE,
    vacances_scolaires BOOLEAN     NOT NULL DEFAULT FALSE
);

-- Dataset final : 1 ligne = 1 boutique x 1 jour, prêt pour Power BI et le Machine Learning
CREATE VIEW v_dataset_final AS
SELECT
    v.date_vente,
    c.jour_semaine,
    v.boutique_id,
    b.ville,
    v.ca_ttc_eur,
    v.nb_tickets,
    ROUND(v.ca_ttc_eur / v.nb_tickets, 2)              AS panier_moyen_eur,
    p.qte_produite,
    v.qte_vendue,
    p.qte_invendue,
    ROUND(p.qte_invendue / p.qte_produite, 3)          AS taux_invendus,
    m.temp_max_c,
    m.pluie_mm,
    c.jour_ferie,
    c.vacances_scolaires
FROM ventes_jour v
JOIN boutiques b  ON b.boutique_id = v.boutique_id
JOIN calendrier c ON c.date_jour   = v.date_vente
LEFT JOIN meteo_jour m ON m.date_meteo = v.date_vente AND m.ville = b.ville
LEFT JOIN (
    SELECT date_prod, boutique_id,
           SUM(qte_produite) AS qte_produite,
           -- si une seule famille n'est pas saisie, le total du jour est inconnu
           CASE WHEN COUNT(qte_invendue) = COUNT(*) THEN SUM(qte_invendue) END AS qte_invendue
    FROM production_jour
    GROUP BY date_prod, boutique_id
) p ON p.date_prod = v.date_vente AND p.boutique_id = v.boutique_id;
