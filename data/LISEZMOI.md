# Données : contenu et formats

Tous les fichiers de `data/` sont des fichiers texte ASCII (fins de ligne LF, sauf les journaux du premier ordinateur, en CRLF). Les fichiers `.gp` ne contiennent que des affectations de constantes (polynômes, matrices, vecteurs) ; les vérificateurs Python les lisent par une grammaire limitée, sans rien évaluer.

## `corps/`

- `rang88_m115c0_data.txt` : un vecteur PARI/GP `[Pm, beta0, …]`. `Pm` (variable `x`) est le polynôme minimal de c = ζ + ζ⁻¹, ζ = ζ₁₁₅ ; `beta0` est l'élément β₀ de L⁺ = Q(c) de la note (totalement positif, β₀𝔇 = O⁺), écrit dans la base (cᵏ). Les trois composantes suivantes sont des objets auxiliaires de la préparation ; aucun vérificateur ne les utilise. Contrôle : `code/verification/verifier_corps.py`.

## `P139/` et `P599/`

| Fichier | Contenu |
|---|---|
| `entrees/I_data.gp` | `PREMIERS`, `Q` (norme absolue), `NU` (ν ≫ 0, générateur de N_{L/L⁺}(P)), `ALPHA` (= β₀/ν), `BASE` (Z-base de l'idéal P, matrice 88 × 88 dans la base ζ⁰..ζ⁸⁷, vecteurs colonnes), `GRAM` (matrice de Gram de X_p dans cette base), `AB` (coordonnées (b ; a) du recollement, prop. 4.1) |
| `entrees/cote{1,2}_A.gram`, `_B.gram`, `_T.mat` | entrées du programme certifiant : « r c » puis r·c entiers ; A = D_A·(Gram de la projection courte), B = D_B·(Gram de la fibre 2νO⁺), Tn (relèvements) |
| `entrees/cote{1,2}_meta.txt` | « D_A D_B d » |
| `entrees/cote{1,2}_bases.gp` | `Hc`, `Hl`, `Hf` : bases qui relient (u, y) au réseau (voir `verifier_raccord.py`, G6) |
| `cote{1,2}.taches` | catalogue des tâches de chaque côté (identique pour toutes les exécutions ; régénérable en quelques secondes, `REPRODUIRE.md`) |
| `norme8.txt` | un couple (côté, u, y) qui donne un vecteur de norme 8 |
| `certificat_K22.txt` | certificat de classe dans K₂₂ (candidats ; tout est recontrôlé par `verifier_classe_P*.py`) |
| `replication/` | **exécutions de référence**, sur le second ordinateur (Linux, OpenJDK 21), sans reprise : reçus `cote{1,2}.ckpt`, journal `cote{1,2}.stdout.log`, `cote{1,2}.stderr.log`, code de sortie `cote{1,2}.java.exit`, et `INVENTAIRE_SORTIE.txt` (inventaire complet du répertoire de sortie) |
| `premiere_execution/` | première exécution, sur le premier ordinateur (Windows, OpenJDK 11.0.16.1) : reçus, journaux, stderr (vides). Pour P₅₉₉ côté 1 : deux lancements (`cote1_lancement1.log`, arrêt forcé ; `cote1_lancement2.log`, reprise) et l'état du fichier de reçus juste avant la reprise (`cote1_avant_reprise.ckpt`) |
| `rejeu_reprises/` (P₅₉₉ seulement) | rejeu complet, sur le premier ordinateur, des 21 459 tâches reprises : `liste_taches_reprises.txt` (indices) et `rejeu_cote1.ckpt` (reçus) |

**Format d'un reçu** (une ligne par tâche terminée, après une ligne d'en-tête `R88Z_CKPT_V1|paramètres|total=…|catalogue=<SHA-256>|entrees=<SHA-256>|classes=<SHA-256>`) :
`T|<indice>|U=<…>|CVP=<…>|NA=<…>|NB=<…>|TOUCHES=<…>|HIST=<…>|FIN`. Les reçus sont déterministes ; leur ordre dans le fichier dépend de l'ordonnancement des fils. **Empreinte canonique** : lignes de reçu triées par indice numérique, chacune suivie de LF, puis SHA-256 (`code/verification/empreinte_canonique.py`).

Les journaux sont copiés tels quels. Ils contiennent les dates et heures d'exécution imprimées par le programme, le nom du système, le nombre de processeurs et le numéro de processus de la machine virtuelle. Ceux du premier ordinateur impriment des chemins relatifs au répertoire d'exécution ; ceux du second impriment le chemin `/out/science/` du répertoire de sortie à l'intérieur de l'environnement isolé d'exécution, et `cote*.stderr.log` y contient une seule ligne d'information de la machine virtuelle (`NOTE: Picked up JDK_JAVA_OPTIONS: …`).

## `rejets/`

Huit témoins de norme 6 (note, tableau 2). Chaque fichier contient `PREMIERS`, `NORME_ABS_I`, `PM`, `BETA0`, `NU`, `ALPHA`, `BASE`, `GRAM`, `X` (coordonnées du vecteur dans `BASE`), `NORME` (= 6) et `Z` (le vecteur dans la base ζ⁰..ζ⁸⁷). Les sept fichiers dont la note cite l'empreinte abrégée sont copiés tels quels (leur première ligne est un commentaire d'origine). `temoin_P1471d2.gp` est le témoin de P₁₄₇₁ = (1471, ζ² + 879ζ + 948), copié tel quel (SHA-256 `11b4d4cb…2e31`) ; il contient en plus `Q`, `AB` et `FACTEUR_INTRINSEQUE`. Contrôles : `verifier_temoins.gp` (PARI/GP) et `verifier_temoins.py` (Python, indépendant).

## `L0/`

- `certificat_H_L0.txt` : la matrice entière P (88 × 88), β (= β₀) et l'exposant a du certificat H ≅ L₀ (note, § 2.5).
- `certificat_conformite.txt` : la matrice entière X (22 × 22) de la seconde identité Q G_art Qᵀ = G.

Ces deux fichiers ne contiennent aucune donnée de R. Sakamoto. Les vérifications lisent sa matrice de Gram dans `externe/integer_input.txt`, que l'utilisateur télécharge lui-même (`externe/LISEZMOI.md`).

## `validation/`

Entrées du programme pour deux cas de réponse connue (note, § 5.2, « Validation ») : `L0/` (I = O_L, réseau H ≅ L₀) et `P461/` (idéal rejeté). Mêmes formats que `entrees/`.
