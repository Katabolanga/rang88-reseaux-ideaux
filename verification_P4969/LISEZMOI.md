# Vérification exacte de X4969 (addendum, théorème A, prop. 2.1 et 2.3)

Les commandes se lancent depuis la racine de ce dossier, avec Python ≥ 3.9 et sa seule bibliothèque standard.

| Contrôle | Commande | Résultat attendu (journal joint) |
|---|---|---|
| Raccord exact | `python3 -I code/verification/verifier_raccord.py P4969` | `BILAN : 37 controles, 0 echecs` puis `FIN_OK` (`verifier_raccord_P4969.log`) |
| Non-isométrie, démontrée sans GRH | `python3 -I code/verification/verifier_non_isometrie_P4969_v2.py` | code de sortie 0 (`verifier_non_isometrie_P4969_v2.log`) |

Le raccord exact vérifie, en entiers et en rationnels, sans PARI :
- la base engendre P4969 ;
- la Gram, recalculée depuis α, est entière, paire, de déterminant 1 et définie positive ;
- les fichiers d'entrée des deux côtés décrivent exactement ce réseau ;
- `data/P4969/norme8.txt` est un vecteur de norme 8.

La non-isométrie montre que les classes ne sont pas conjuguées par Galois, sans GRH, à l'aide du certificat `data/P4969/certificat_K22.txt`.

## Contenu

- `data/P4969/entrees/` : les entrées du programme certifiant (`cote1_*`, `cote2_*`, `I_data.gp`).
- `data/P4969/premiere_execution/` : journaux des premières exécutions complètes. Les exécutions certifiées et leurs réplications sont dans `../calcul_externe_resultats_20261015/`.
- `data/P139/`, `data/corps/` : données de référence de la note, utilisées pour les comparaisons.
- `recherche_classe/` : certificat de classe dans K₂₂.
- `recherche_norme8/` : la recherche du vecteur de norme 8, par une exécution courte, arrêtée à la première touche.

Le minimum 8 lui-même est assisté par calcul : voir l'addendum, théorème A, et `../calcul_externe_resultats_20261015/LISEZMOI.md`.
