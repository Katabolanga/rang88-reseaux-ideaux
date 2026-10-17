# Contre-audit, expériences C1 et C4 (16 octobre 2026)

*Claude. Données brutes : `C1_GROUPE_TEMOIN_RESULTATS.txt`, script `C1_controle_generique.sh` ; les journaux de chaque cas sont dans `agents/rang88_ideaux/ctl1016/P<p>/`. Pour C4 : `C4_compte_U_P139_qfminim.gp` et `.log`, puis `C4b_compte_U_P139_complet.gp` et `.log` pour le palier complet. Version 3 (14 h 25) : le palier complet est recompté.*

## C1 : groupe témoin de classes génériques (poste d'Ivan, Java 11, 8 fils)

- **Protocole.**
  - Idéaux de degré 1, P = (p, ζ − r), avec p ≡ 1 mod 115 : les 16 plus petits premiers de ce type après 461.
  - Entrées préparées par `prep_java.gp`, aux mêmes paramètres que P₁₃₉, P₅₉₉ et P₄₉₆₉.
  - Rang88CertZ, côté 1, avec les paramètres publiés (1057/200, S = 12), arrêt à la première touche, au plus 5 minutes.
- **Re-détection de classes déjà rejetées par la recherche PARI** (méthode indépendante) : P₆₉₁ (touche à la tâche 257), P₁₁₅₁ (60), P₁₃₈₁ (57). **3 sur 3 retrouvées.**
- **13 classes génériques nouvelles.**
  - **11 rejetées** (vecteur de norme ≤ 6) entre la tâche 33 et la tâche 941, en 39 à 233 s : 3221, 3911, 4831, 5521, 5981, 6211, 7591, 8741, 8971, 9431, 9661.
  - **2 survivantes partielles** à 5 minutes : P₂₅₃₁ (1 441 tâches sans touche) et P₁₁₇₃₁ (1 415 tâches). P₂₅₃₁ est le cas où le filtre PARI de la note avait été interrompu sans décision.
- **Lecture.**
  - L'heuristique de Siegel–Poisson prévoit 4,4 % d'extrémaux pour une orbite de taille 88 et 21 % pour une orbite de taille 44.
  - Avec 2 survivantes sur 13, aucun signe d'une méthode qui « laisserait passer » des réseaux non extrémaux.
  - La méthode retrouve les vecteurs courts là où une autre méthode les avait trouvés.
  - Attention : certains rejets demandent jusqu'à environ 1 000 tâches (P₉₆₆₁). Un filtre court doit couvrir au moins quelques milliers de tâches.
- **Portée.** C'est une expérience statistique de cohérence. Elle n'établit pas la non-omission et ne remplace pas la preuve.

## C4 : recompte indépendant de |U| par PARI (P₁₃₉, côté 1)

`qfminim` de PARI/GP 2.15.4 sur `cote1_A.gram` (entière, échelle 139), comparé à l'histogramme imprimé par Rang88CertZ :

| Énergie courte | PARI | Rang88CertZ |
|---|---|---|
| < 3 | 162 | 162 |
| < 7/2 | 4 878 | 4 878 |
| < 4 | 92 734 | 92 734 |
| < 9/2 | 1 260 158 | 1 260 158 |
| < 5 | 12 651 642 | 12 651 642 |
| ≤ 1057/200 (palier complet) | 42 957 972 | 42 957 972 |

- **Identique sur les six paliers.** Le palier < 5 a été obtenu par le second lancement : 5 966 s, fin vers 11 h 06.
- **Le palier complet.** Il est égal au nombre |U| que l'énumérateur parcourt pour P₁₃₉ côté 1.
  - Un premier essai, limité à 2 h, avait été coupé (code 124).
  - `C4b_compte_U_P139_complet.gp` l'a recompté : lancé à 11 h 07, fin à 14 h 23, 11 260 s, code 0.
  - `qfminim(A, 734, 0)` donne 42 957 972 projections au signe près, avec B = ⌊139 · 1057/200⌋ = 734. C'est **identique** au compte de Rang88CertZ.
- **Portée.** `qfminim` n'est pas certifiant, mais c'est un énumérateur indépendant du code Java : autre programme et autres auteurs.
