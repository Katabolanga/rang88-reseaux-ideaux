# Témoins de norme 6 de l'addendum (version 1.2)

Ce dossier publie les vecteurs de norme 6 dont dépendent deux énoncés de l'addendum, avec deux vérificateurs autonomes et le bilan des filtres.

- **§ 4.5, tableau 4.** Les quatre rejets des filtres de la nuit du 16 au 17 octobre 2026 : P₂₅₃₁σ₂₄(P₂₅₃₁), P₅₉₈₁σ₂₄(P₅₉₈₁), P₁₈₄₀₁σ₂₄(P₁₈₄₀₁) et P₃₉₂₃₉.
- **Proposition 4.6.** Le réseau X_I, avec I = P₆₉₁σ₂₄(P₆₉₁) et P₆₉₁ = (691, ζ − 4), contient un vecteur de norme 6. C'est le jumeau de X₄₉₆₉ ; le théorème B en dépend.

Ce témoin de la prop. 4.6 n'était pas dans la version 1.1. Le témoin de `data/rejets/temoin_P691r4.gp` porte sur l'idéal premier P₆₉₁ lui-même, de norme 691, et non sur I.

| Fichier | Idéal I = (p, GEN(ζ)) | Énoncé | Côté de la touche | Énergies (courte + fibre = 12) |
|---|---|---|---|---|
| `temoin_P2531s24.gp` | (2531, ζ² + 2036ζ + 734) = P σ₂₄(P), P = (2531, ζ − 12) | tableau 4, heure 12, anneau int. | 2 | 11913/2531 + 186878916/5062² |
| `temoin_P5981s24.gp` | (5981, ζ² + 873ζ + 3719) = P σ₂₄(P), P = (5981, ζ − 16) | tableau 4, heure 11, int. | 1 | 28185/5981 + 1042775388/11962² |
| `temoin_P18401s24.gp` | (18401, ζ² + 9938ζ + 1692) = P σ₂₄(P), P = (18401, ζ − 22) | tableau 4, heure 1, int. | 1 | 85506/18401 + 9959062824/36802² |
| `temoin_P39239.gp` | (39239, ζ² + 1632ζ + 23778), premier de degré 2 | tableau 4, heure 12, ext. | 2 | 164472/39239 + 48090690576/78478² |
| `temoin_P691s24.gp` | (691, ζ² + 91ζ + 311) = P₆₉₁ σ₂₄(P₆₉₁) | prop. 4.6 (deux touches) | 1 et 2 | 3542/691 + 13129000/1382² ; 2406/691 + 16268904/1382² |

## Vérifier

Les trois commandes se lancent depuis la racine du dépôt.

| Commande | Résultat attendu |
|---|---|
| `gp -q -D parisize=400000000 addendum/temoins_norme6/verifier_temoins_norme6.gp < /dev/null` | `BILAN : 69 controles (attendus 69), 0 echecs ; 5 temoins valides sur 5 fichiers`, `TEMOINS_NORME6_ADDENDUM_OK`, code de sortie 0 (environ 30 s) |
| `python3 -I addendum/temoins_norme6/verifier_temoins_norme6.py` | `BILAN : 75 controles (attendus 75), 0 echecs ; 5 temoins valides sur 5 fichiers`, `TEMOINS_NORME6_VERIFIES_SANS_PARI`, code de sortie 0 (environ 15 s) |
| `python3 -I addendum/temoins_norme6/filtres_nuit_20261017/verifier_bilan_filtres.py` | `BILAN : 6 controles (attendus 6), 0 echecs`, `BILAN_FILTRES_CONFORME`, code de sortie 0 |

Les sorties de ces exécutions sont dans `verifier_temoins_norme6_gp.log`, `verifier_temoins_norme6_py.log` et `filtres_nuit_20261017/verifier_bilan_filtres.log`. Elles ont été obtenues avec PARI/GP 2.17.2 et Python 3.12, sous Linux (WSL). Le script GP donne le même bilan avec PARI/GP 2.15.4 sous Windows.

## Ce que contrôlent les deux vérificateurs de témoins

Le script GP et le script Python font les mêmes contrôles, numérotés de la même façon. Le second n'utilise que la bibliothèque standard de Python, en entiers et en rationnels exacts ; il lit les fichiers `.gp` comme du texte, par une grammaire limitée, sans rien évaluer. Les deux partent d'une **liste figée des cibles** : les idéaux, les côtés et les énergies imprimés dans l'addendum.

1. **L'idéal (A1–A3).**
   - Pour P σ₂₄(P) : p est premier, r₁ et r₂ sont deux racines distinctes de Φ₁₁₅ modulo p, avec r₂ = r₁²⁴ ; donc (p, ζ − r₂) = σ₂₄(p, ζ − r₁), car 24² ≡ 1 (mod 115). GEN est (y − r₁)(y − r₂) réduit modulo p.
   - Pour P₃₉₂₃₉ : 39239 est d'ordre 2 modulo 115, et GEN est un facteur irréductible de degré 2 de Φ₁₁₅ modulo 39239. Tous les premiers de degré 2 au-dessus de 39239 sont conjugués sous Gal(L/Q) : l'orbite ne dépend pas du facteur choisi.
   - Une base C de I est construite par le vérificateur lui-même, **sans la base du préparateur** : p, pζ et GEN(ζ)ζʲ pour 0 ≤ j ≤ 85. Le module qu'elle engendre est stable par ζ, contient p et GEN(ζ) et est contenu dans (p, GEN(ζ)) ; il est donc égal à I, d'indice p².
2. **Le réseau (B1–B4).** α est lu dans le fichier ; le vérificateur contrôle α·ν = β₀ avec le β₀ de `data/corps/`. La matrice de Gram G = Cᵀ H C, avec H[i, j] = Tr(α ζ^(i−j)), est recalculée depuis α seul. Elle est entière, paire, de déterminant 1 et définie positive. Donc (I, α) est un réseau pair unimodulaire de rang 88. Par la prop. 2.3 (b) de la note, c'est l'élément de S de classe [I].
3. **Les témoins (C1–C3).**
   - Chaque vecteur z est entier, non nul et appartient à I ; ses coordonnées w dans C sont entières, et wᵀ G w = 6.
   - Tr(α z z̄) = 6 est recalculé directement dans Q(ζ), sans base.
   - Les énergies imprimées dans l'addendum sont retrouvées exactement. Avec f = Tr(α z²), on a Λ(a) = 6 + f et Λ′(b) = 6 − f (note, lemme 4.2). La projection courte porte sur a au côté 1 et sur b au côté 2 (note, prop. 4.1 (c)).
4. **La provenance (D1–D3, et E1 en Python).** `BASE` est la base des fichiers d'entrée du programme. Elle engendre I. `GRAM` = BASEᵀ H BASE, Z = BASE·X et Xᵀ GRAM X = 6. En Python, chaque colonne de X est aussi comparée, entier pour entier, à la ligne `x = […]` du journal d'audit du 17 octobre.

Conclusion, **démontrée sans GRH** : les cinq réseaux X_I contiennent un vecteur de norme 6, donc ne sont pas extrémaux. Aucun `bnfinit`, aucun programme Java, aucune sortie de session n'interviennent dans les contrôles A à C. Les contrôles D et E ne servent qu'à relier ces vecteurs aux exécutions du 17 octobre.

**Essais négatifs.** Quatre copies altérées ont été soumises aux deux vérificateurs : un coefficient d'un témoin, le générateur d'un idéal, un coefficient de α, l'ordre des deux premiers dans la liste. Les deux vérificateurs les rejettent toutes, avec le code de sortie 1. Ces copies ne sont pas publiées.

## Format des fichiers `temoin_*.gp`

Ce sont des affectations de constantes, précédées d'un commentaire.

- `NOM`, `PREMIERS` (conventions de la note : [p, r] pour (p, ζ − r), [p, 2, k] pour un premier de degré 2) et `NORME_ABS_I` = p².
- `GEN` : I = (p, GEN(ζ)).
- `NU` et `ALPHA` = β₀/ν : polynômes en x = ζ + ζ⁻¹.
- `BASE` et `GRAM` : base des fichiers d'entrée du programme, vecteurs colonnes dans la base ζ⁰…ζ⁸⁷, et matrice de Gram dans cette base.
- `COTES`, `TOUCHES` : le côté et la ligne brute de chaque touche du programme.
- `X` et `Z` : une colonne par témoin. X donne les coordonnées dans `BASE`, et Z = BASE·X les coefficients en ζ⁰…ζ⁸⁷.
- `NORME` = 6.

Ces fichiers ont été extraits le 18 octobre 2026 des fichiers d'entrée et des fichiers de touches des filtres. Pour chaque touche (u, y), x = AB⁻¹(b ; a) a été recalculé exactement, comme dans `temoin_filtre.gp`. Les fichiers d'entrée complets (environ 400 Ko par idéal) ne sont pas publiés : les vérificateurs n'en ont pas besoin.

## `filtres_nuit_20261017/` : le bilan des 21 filtres

| Pièce | Contenu |
|---|---|
| `BILAN_FILTRES.txt` | Le bilan des 21 filtres, copié tel quel : date, idéal, orbite, verdict, détails, témoin exact. La colonne « orbite » a été calculée sous GRH ; le corollaire 4.8 de l'addendum certifie ces heures sans GRH. |
| `AUDIT_REJETS_20261017_044917.txt` | L'audit de référence des rejets, copié tel quel (SHA-256 `7d3c6722…f66cf`, empreinte citée en tête de `addendum/comptes_filtres.tex`). Un rejet n'y est retenu que si sa vérification exacte réussit entièrement : code 0, sentinelle finale, nombre complet de contrôles, au moins une touche vérifiée, aucune erreur GP. |
| `temoin_filtre.gp` | Le gabarit du vérificateur de touches du 17 octobre (v3, SHA-256 `f2740a12…0c42`), copié tel quel. |
| `temoin_<NOM>.audit_20261017_044917.log` | Les quatre sorties de cet audit (PARI/GP 2.15.4, Windows), copiées telles quelles, avec leurs fins de ligne CRLF. |
| `executions/` | Pour chaque filtre et chaque côté : le journal du programme (`.log`, fins de ligne CRLF), le code de sortie (`.exit`), les reçus (`.ckpt`) et, pour les quatre rejets, le fichier de touches (`.ckpt.touches`). |
| `verifier_bilan_filtres.py`, `verifier_bilan_filtres.log` | Le contrôle, en lecture seule, du bilan, des journaux et des tableaux de l'addendum. Il recalcule les 21 lignes du tableau 4 et les macros de comptes à partir du bilan, des reçus et de l'audit, puis les compare octet pour octet à `addendum/tableau_filtres_fr.tex`, `tableau_filtres_en.tex` et `comptes_filtres.tex`. |

Précisions sur ces pièces :
- Les scripts d'audit du 17 octobre étaient formés de cinq lignes de paramètres suivies de `temoin_filtre.gp`. Ces cinq lignes comprennent deux chemins absolus du poste de l'auteur ; c'est pourquoi ces scripts ne sont pas publiés. Leurs autres paramètres sont dans la table du début (idéal, côté).
- Les lanceurs des filtres, le script d'audit `auditer_rejets.sh` et le générateur des tableaux `tableau_filtres.py` contiennent des chemins absolus, ou écrivent hors de leur dossier. Ils ne sont pas publiés. `verifier_bilan_filtres.py` refait le calcul du générateur.
- Les codes de sortie valent tous `code 1`. Chaque machine virtuelle Java a été arrêtée par le lanceur, au plafond de 12 minutes ou après une touche ; ces codes ne jouent aucun rôle dans les preuves.
- Les catalogues de tâches (`.taches`, de 8 à 25 Mo chacun) ne sont pas inclus. Ils sont régénérables (`REPRODUIRE.md`), et leur empreinte est imprimée dans chaque journal (`CATALOGUE_SHA256`).

**Statuts.** Les quatre rejets sont démontrés sans GRH, par les témoins. Les 17 survivants partiels sont constatés : un filtre arrêté ne démontre rien.

## `prop46_P691s24_execution/` : le filtre de la prop. 4.6

- Les journaux, codes de sortie (`code 0`, arrêt du programme sur sa première touche), reçus et fichiers de touches du filtre lancé le 17 octobre 2026 à 0 h 17 sur les deux côtés de I.
- `temoin_P691s24.log` : la sortie, copiée telle quelle, de la vérification exacte du 17 octobre à 0 h 24 (10 contrôles, 0 échec ; PARI/GP 2.15.4, Windows).
- Ces journaux sont des sorties Windows, aux fins de ligne CRLF.

Le script de cette vérification contenait deux chemins absolus et n'est pas publié. Son rôle est repris par les deux vérificateurs de ce dossier, qui ne dépendent d'aucun chemin local.

---

**English summary.** This folder publishes the norm-6 vectors behind two statements of the addendum: the four rejections of the overnight filters (§ 4.5, Table 4) and Proposition 4.6. Proposition 4.6 says that the twin of X₄₉₆₉, the lattice of I = P₆₉₁σ₂₄(P₆₉₁), is not extremal; Theorem B relies on it. Two independent checkers are provided. One is in PARI/GP (69 checks); the other in plain Python with exact integer and rational arithmetic, without PARI (75 checks). Both rebuild a basis of I from its two generators and recompute the Gram matrix from α alone. They check that it is even, unimodular and positive definite, and that each vector lies in I and has norm exactly 6. They also recover the printed energies. `filtres_nuit_20261017/` contains the summary of the 21 filters, the reference audit, the program logs and receipts, and a read-only script. That script recomputes Table 4 and the count macros of the addendum byte for byte.
