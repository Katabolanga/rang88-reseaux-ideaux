# rang88-reseaux-ideaux

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23638084.svg)](https://doi.org/10.5281/zenodo.23638084)

Archive Zenodo : DOI de concept (toutes les versions) [10.5281/zenodo.23638084](https://doi.org/10.5281/zenodo.23638084) ; version 1.3 (release v1.3.1 du 25 octobre 2026) : [10.5281/zenodo.23638085](https://doi.org/10.5281/zenodo.23638085) ; version 1.4 (release v1.4 du 31 octobre 2026) : [10.5281/zenodo.23835418](https://doi.org/10.5281/zenodo.23835418) ; version 1.5 (release v1.5 du 7 novembre 2026) : [10.5281/zenodo.24044458](https://doi.org/10.5281/zenodo.24044458).

Données, programmes et vérifications qui accompagnent la note **« Réseaux idéaux pairs unimodulaires de rang 88 sur Q(ζ₁₁₅) »** d'Ivan Gauvin (15 octobre 2026, révisée le 7 novembre 2026), dont le texte source et le PDF sont dans `article/`, son addendum du 17 octobre 2026 (`addendum/`) et son addendum 3 du 7 novembre 2026 (`addendum3/`). *English summary below.*

Le dépôt est autoportant : avec PARI/GP 2.15, Python ≥ 3.9 (bibliothèque standard seulement) et, pour les essais facultatifs, Java 11 ou plus, on peut rejouer toutes les vérifications exactes de la note, sauf les deux qui lisent la matrice de Gram de L₀ publiée par R. Sakamoto : ce fichier n'est pas redistribué et doit être téléchargé à part (`externe/LISEZMOI.md`). Les balayages certifiants eux-mêmes (plusieurs heures par côté) ne sont pas relancés par les vérificateurs : leurs reçus, journaux et catalogues sont fournis et contrôlés exactement ; la commande pour les refaire est dans `REPRODUIRE.md`.

## Version 1.5 (7 novembre 2026) : X(P₃₃₅₉) et X(P₄₆₁σ₉₁), de minimum 8 assisté par calcul ; la composante 45 013 sans GRH ; corrections

> **Statuts.** Le minimum 8 de X(P₃₃₅₉) et de X(P₄₆₁σ₉₁) est **assisté par calcul** (th. 4.6 de la note, `Rang88CertZ`, M1, M2, H1–H3) : chaque côté a été balayé sans touche deux fois, sur deux machines, **avec le même programme** ; aucune implantation indépendante ne le certifie, et **aucun humain ne l'a audité**. Ces deux réseaux ne sont extrémaux que sous ces hypothèses.

L'**addendum 3** (`addendum3/addendum3_en.pdf`, 7 p., et `addendum3/addendum3_fr.pdf`, 7 p., avec leurs sources) et le dossier `v15_P3359_et_P461s91/` (son `README_v15.md`, en français puis en anglais, donne tout le détail) apportent :
- **X(P₃₃₅₉)**, I = (3359, ζ² + 2202ζ + 1829), survivant partiel de la note : les deux côtés balayés en entier, sur SpiraleG (19–21 oct.) puis sur Bertha (6–7 nov.), reçus identiques tâche par tâche, empreintes canoniques `9fc5bb74…`, `a5e5f7b9…` ;
- **X(P₄₆₁σ₉₁)**, candidat de la version 1.4 : une seconde exécution neuve (Bertha, 7 nov.) redonne les 146 603 reçus de Crapaud08 à l'octet ; il n'est plus un candidat non répliqué ;
- **un certificat sans GRH** : la composante 45 013 de la classe de X(P₄₆₁σ₉₁) est non nulle (sommes de Jacobi et théorème de Stickelberger ; vérificateur en Python, bibliothèque standard seulement) ; X(P₄₆₁σ₉₁) n'est donc isométrique ni à L₀ ni à L_S, sans GRH et sans calcul assisté de notre part ;
- **la note et l'addendum corrigés** : citation de Quebbemann (J. reine angew. Math. 326, 1981), dont le th. 3.3 de la note étend l'argument ; citation de Bayer-Fluckiger 1984 (son cor. 3.3 est une majoration) ; statut de la non-isométrie précisé. Toutes les corrections sont relevées dans `CHANGEMENTS_V15.md`.

| Énoncé | Statut | Commande (depuis la racine, sauf mention) | Résultat attendu |
|---|---|---|---|
| X(P₃₃₅₉) : pair, unimodulaire, défini positif ; raccord exact des entrées | démontré | `python3 -I code/verifier_raccord_tranche1.py P3359` (depuis `v15_P3359_et_P461s91/verification/`) | `BILAN : 37 controles, 0 echecs`, `FIN_OK` |
| Minimum 8 de X(P₃₃₅₉) : deux côtés sans touche, deux machines | assisté par calcul (M1, M2, H1–H3), même programme, non audité | `controle_execution.py`, `empreinte_canonique.py`, `compare_recus.py` (voir `README_v15.md`, § 4) | 31 et 29 contrôles, 0 échec ; empreintes égales sur les deux machines ; reçus identiques |
| Minimum 8 de X(P₄₆₁σ₉₁) : seconde exécution neuve | assisté par calcul (M1, M2, H1–H3), même programme, non audité | idem | 73 244 et 73 359 reçus identiques à l'octet à ceux de la version 1.4 |
| Composante 45 013 de [P₅σ₉₁(P₅)] non nulle ; X(P₄₆₁σ₉₁) ≇ L₀, L_S | démontré, sans GRH, modulo Stickelberger, l'indice des unités, le th. 3.3 et le minimum 8 de Sakamoto | `python3 -I verifier_certificat_45013.py certificat_45013_P461s91.json` (depuis `v15_P3359_et_P461s91/certificat_45013/`) | `462 controles, 0 echecs`, code 0 ; trois certificats altérés rejetés |
| Classes de X(P₃₃₅₉), X(P₄₆₁σ₉₁) et des sept extrémaux connus deux à deux non conjuguées | démontré, sans GRH ; non-isométrie par le th. 3.3, sous le minimum 8 assisté de l'un des deux réseaux comparés (sauf face à L₀, L_S) | `python3 -I code/verifier_non_isometrie_tranche1.py` (depuis `v14_P1151s24_et_candidat_P461s91/verification/`) et le certificat ci-dessus | `BILAN : 123 controles, 0 echecs` |
| Seconde implantation `enum88.c` sur X(P₄₆₁σ₉₁) | constaté (recoupement numérique, pas un certificat) | `python3 -I v15_P3359_et_P461s91/recoupement_enum88/comparer_enum88.py …` | 6 contrôles, 0 échec, par côté |

Sous ces hypothèses, la famille compte au moins **neuf** réseaux extrémaux de rang 88 deux à deux non isométriques : L₀, L_S (Sakamoto) et sept réseaux à minimum assisté par calcul, X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉, X(P₁₁₅₁σ₂₄), X(P₃₃₅₉), X(P₄₆₁σ₉₁).

**Textes révisés.** `article/rang88.tex` et `.pdf` (26 p.), `article/rang88_en.tex` et `.pdf` (25 p.), `addendum/addendum_fr.tex` et `.pdf` (15 p.), `addendum/addendum_en.tex` et `.pdf` (14 p.) portent la date de révision du 7 novembre 2026 ; leur numérotation est inchangée (contrôlé sur les fichiers `.aux`). Les textes de la version 1.4 restent dans l'historique du dépôt (commit `ce38bd8`) et dans l'archive Zenodo de la version 1.4.

## Version 1.4 (31 octobre 2026) : horodatage de X(P₁₁₅₁σ₂₄) et du CANDIDAT X(P₄₆₁σ₉₁)

> *Depuis la version 1.5, les deux réserves sur X(P₄₆₁σ₉₁) ci-dessous sont levées : minimum répliqué sur une seconde machine (même programme), non-isométrie à L₀ sans GRH. Cette section est conservée telle qu'elle a été publiée.*

> **X(P₄₆₁σ₉₁) est un CANDIDAT** : minimum annoncé par les auteurs, **NON répliqué** (seule la partie courte de ses reçus est recoupée, par ceux de P₄₆₁σ₂₄) ; non-isométrie à L₀ **sous GRH seulement**.

Le dossier `v14_P1151s24_et_candidat_P461s91/` date publiquement deux réseaux idéaux pairs unimodulaires de rang 88, attachés à des produits de deux premiers de degré 1 échangés par Galois. Son `README_v14.md` (français, puis anglais) donne les constructions, les statuts, les commandes et ce qui n'est pas revendiqué. La note et l'addendum sont inchangés.

| Énoncé | Statut | Dossier | Commande (depuis `v14_P1151s24_et_candidat_P461s91/verification/`, sauf mention) | Résultat attendu |
|---|---|---|---|---|
| X(P₁₁₅₁σ₂₄), I = (1151, ζ − 6)(1151, ζ − 605) : pair, unimodulaire, défini positif ; raccord exact des entrées | démontré | `verification/` | `python3 -I code/verifier_raccord_P1151s24.py P1151s24` | `BILAN : 38 controles, 0 echecs`, `FIN_OK` |
| Minimum 8 de X(P₁₁₅₁σ₂₄) : deux côtés balayés sans touche, deux fois, sur deux machines | assisté par calcul (M1, M2, H1–H3), répliqué | `balayages/P1151s24_*` | `controle_execution.py` (voir `README_v14.md`, § 5) | 27 contrôles, 0 échec par exécution ; empreintes canoniques `36c946d4…`, `32818d45…` égales deux à deux |
| X(P₁₁₅₁σ₂₄) non isométrique aux six extrémaux connus | non-conjugaison : démontrée, sans GRH ; non-isométrie : par le th. 3.3 | `verification/` | `python3 -I code/verifier_non_isometrie_P1151s24.py` | `BILAN : 85 controles, 0 echecs` |
| **Candidat** X(P₄₆₁σ₉₁), I = (461, ζ − 5)(461, ζ − 115) : pair, unimodulaire, défini positif ; raccord exact | démontré | `verification/` | `python3 -I code/verifier_raccord_tranche1.py P461s91` | `BILAN : 38 controles, 0 echecs`, `FIN_OK` |
| Minimum 8 du **candidat** X(P₄₆₁σ₉₁) : deux côtés balayés sans touche, une fois (côté 1 repris d'un lancement interrompu) | **CANDIDAT : annoncé par les auteurs, NON répliqué** (seule la partie courte des reçus est recoupée) | `balayages/CANDIDAT_P461s91_non_replique_Crapaud08_V2_20261019/` | `controle_execution.py` (voir `README_v14.md`, § 5) | côté 2 : 28 contrôles, 0 échec ; côté 1 : 4 échecs E1 de reprise, attendus |
| **Candidat** X(P₄₆₁σ₉₁) non isométrique à X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉, X(P₁₁₅₁σ₂₄), L_S ; à L₀ | sans GRH, sauf L₀ : **sous GRH seulement** | `verification/` | `python3 -I code/verifier_non_isometrie_tranche1.py` | `BILAN : 123 controles, 0 echecs` |

Avec X(P₁₁₅₁σ₂₄), la famille compte au moins sept réseaux extrémaux de rang 88, deux à deux non isométriques : L₀, L_S (Sakamoto) et cinq réseaux à minimum assisté par calcul et répliqué. X(P₄₆₁σ₉₁) est un huitième candidat, non répliqué, dont la nouveauté face à L₀ dépend de GRH.

## Version 1.3 (octobre 2026) : traduction anglaise et archivage

- **La note en anglais** : `article/rang88_en.pdf` (24 p.) et sa source `article/rang88_en.tex`. C'est une traduction ; l'original français fait foi.
- **Le texte français mis à jour** : `article/rang88.tex` et `article/rang88.pdf` (25 p.) remplacent ceux de la version 1.0. Ce sont les textes soumis à arXiv le 15 octobre 2026, soumission que la modération d'arXiv n'a pas retenue. Changements : la non-isométrie est énoncée « sans GRH » ; les normalisateurs du groupe des multiplications dans Aut(X₁₃₉) et Aut(X₅₉₉) sont d'ordres 460 et 920. Le texte de la version 1.0 reste dans l'historique du dépôt (commit f20d0bd).
- **L'archivage** : le fichier `.zenodo.json` décrit le dépôt pour l'archive Zenodo. Archive publiée le 25 octobre 2026 (release v1.3.1, même contenu que l'étiquette v1.3) : DOI de version 10.5281/zenodo.23638085, DOI de concept 10.5281/zenodo.23638084.
- Aucun nouveau calcul. Les données, programmes et vérifications des versions 1.0 à 1.2 sont inchangés.

## Version 1.2 (18 octobre 2026) : témoins de norme 6 de l'addendum

La version 1.2 publie les pièces annoncées dans la version 1.1, et une pièce qui manquait. Tout est dans `addendum/temoins_norme6/` (voir son `LISEZMOI.md`).
- **Les quatre rejets des filtres du § 4.5 de l'addendum (tableau 4).** Leurs témoins de norme 6 ; le bilan des 21 filtres, l'audit des rejets du 17 octobre et les journaux des filtres.
- **Le témoin de norme 6 de la proposition 4.6 de l'addendum.** Le réseau de I = P₆₉₁σ₂₄(P₆₉₁), jumeau de X₄₉₆₉, contient un vecteur de norme 6 ; le théorème B en dépend. Ce témoin n'était pas public dans la version 1.1, et il n'y était pas annoncé.
- **Deux vérificateurs autonomes** de ces cinq témoins, l'un en PARI/GP, l'autre en Python sans PARI. Ils reconstruisent une base de l'idéal à partir de ses deux générateurs, et la matrice de Gram à partir de α seul.
- **Une précision de statut** (ci-dessous) : la non-isométrie entre deux réseaux candidats est démontrée sans GRH, mais elle suppose le minimum 8, assisté par calcul, d'au moins un des deux réseaux comparés.

Les textes de la note et de l'addendum (`.tex`, `.pdf`) sont inchangés ; leurs corrections iront dans une version 2 sur arXiv.

## Version 1.1 (17 octobre 2026) : addendum

L'**addendum** est dans `addendum/addendum_en.pdf` (14 p.) et `addendum/addendum_fr.pdf` (15 p.), avec ses sources dans `addendum/`. Il apporte trois résultats.

- **Théorème A, six réseaux extrémaux.** Soit P₄₉₆₉ = (4969, ζ² + 3763ζ + 2809) et P₄₀₄₉ = (4049, ζ² + 105ζ + 2084). Les réseaux X₄₉₆₉ et X₄₀₄₉ sont pairs, unimodulaires, de rang 88 et de minimum 8. Avec X₁₃₉, X₅₉₉, L₀ et L_S, la famille contient donc au moins six réseaux extrémaux, deux à deux non isométriques.
  - Le minimum est assisté par calcul (M1, M2, H1–H3). Chaque côté a été balayé deux fois sur deux machines louées, avec des reçus identiques à l'octet.
  - La non-isométrie est démontrée sans GRH, sous le minimum 8 assisté par calcul de X₄₉₆₉ ou X₄₀₄₉. En effet, la non-conjugaison des classes est démontrée sans GRH, mais le théorème d'isométrie qui la transforme en non-isométrie demande le minimum 8 d'au moins un des deux réseaux comparés ; pour X₁₃₉ et X₅₉₉, ce minimum est lui aussi assisté par calcul. La non-isométrie à L₀ et à L_S ne dépend pas de ce minimum assisté : un réseau de minimum au plus 6 n'est pas isométrique à un réseau de minimum 8, et le minimum 8 de L₀ et de L_S est établi par Sakamoto.
- **Théorème B.** L'extrémalité n'est pas un invariant des paires de jumeaux de la couche σ₂₄. (X₄₀₄₉, X₅₉₉) est une paire extrémale, comme (L₀, L_S) ; en revanche, le jumeau de X₄₉₆₉ contient un vecteur de norme 6. Les relations de jumeaux et ce vecteur sont démontrés, sans GRH ; le vecteur est publié depuis la version 1.2 (`addendum/temoins_norme6/`).
- **Théorème C, le cadran de la couche σ₂₄ sans GRH.** L'orbite d'un idéal de la couche se lit sur des résidus de puissance 331-ième.

| Énoncé de l'addendum | Statut | Dossier | Commande | Résultat attendu |
|---|---|---|---|---|
| X₄₉₆₉, X₄₀₄₉ : pairs, unimodulaires, définis positifs ; raccord exact des entrées ; vecteur de norme 8 (prop. 2.1) | démontré | `verification_P4969/`, `verification_P4049/` | `python3 -I code/verification/verifier_raccord.py P4969` (depuis le dossier ; idem pour P4049) | `BILAN : 37 controles, 0 echecs`, `FIN_OK` |
| Classes non conjuguées (prop. 2.3), donc non-isométrie (th. A) | non-conjugaison : démontrée, sans GRH ; non-isométrie : démontrée sans GRH sous le minimum 8 assisté par calcul de X₄₉₆₉ ou X₄₀₄₉ (le théorème d'isométrie demande le minimum 8 d'au moins un des deux réseaux comparés) ; à L₀ et L_S : sans ce minimum assisté | idem | `python3 -I code/verification/verifier_non_isometrie_P4969_v2.py` (idem pour P4049) | code de sortie 0 |
| Minimum 8 de X₄₉₆₉ et X₄₀₄₉ : balayages complets et répliqués (§ 2.2) | assisté par calcul (M1, M2, H1–H3) | `calcul_externe_resultats_20261015/` | voir le `LISEZMOI.md` du dossier | 27 contrôles et 0 échec par exécution ; empreintes canoniques égales deux à deux |
| Fiches au format du catalogue de Nebe et Sloane (X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉) ; sous-groupes d'ordre 460 et 920 | démontré (contrôles exacts) | `catalogue/` | `python3 -I verify_std.py X139.std X599.std X4969.std X4049.std` ; `python3 verify_construction.py X139 X599 X4969 X4049` | `all checks passed` ; `all reconstructions agree with the .std files` |
| Jumeaux et même orbite (prop. 4.5) | démontré, sans GRH | `addendum/certificats_jumeaux/` | `gp -q jumeaux_K22.gp < /dev/null` ; `gp -q meme_orbite_K22.gp < /dev/null` | certificats OK, code de sortie 0 |
| Cadran sans GRH (prop. 4.7, cor. 4.8, th. C) | démontré, sans GRH | `addendum/cadran_sans_GRH/` | `gp -q cadran_sans_GRH.gp < /dev/null` ; `python3 -I verifier_cadran.py` | `CADRAN_SANS_GRH_OK` (97) ; `CADRAN_VERIFIE_SANS_PARI` (186) |
| Attaques contre la méthode (§ 3) | constaté | `contre_audit_20261016/` | voir le `LISEZMOI.md` du dossier | bilans C1–C4 |
| Quatre rejets des filtres (§ 4.5, tableau 4) ; vecteur de norme 6 du jumeau de X₄₉₆₉, réseau de P₆₉₁σ₂₄(P₆₉₁) (prop. 4.6, th. B) (version 1.2) | démontré, sans GRH | `addendum/temoins_norme6/` | `gp -q -D parisize=400000000 addendum/temoins_norme6/verifier_temoins_norme6.gp < /dev/null` ; `python3 -I addendum/temoins_norme6/verifier_temoins_norme6.py` (depuis la racine) | `TEMOINS_NORME6_ADDENDUM_OK` (69 contrôles) ; `TEMOINS_NORME6_VERIFIES_SANS_PARI` (75 contrôles) ; 5 témoins valides sur 5 ; code de sortie 0 |
| Bilan des 21 filtres de la nuit du 16 au 17 octobre (§ 4.5) : 4 rejets, 17 survivants partiels ; tableau 4 et comptes (version 1.2) | rejets : démontrés (ligne précédente) ; survivants : constaté | `addendum/temoins_norme6/filtres_nuit_20261017/` | `python3 -I addendum/temoins_norme6/filtres_nuit_20261017/verifier_bilan_filtres.py` (depuis la racine) | `BILAN_FILTRES_CONFORME` (6 contrôles) ; tableau 4 recalculé octet pour octet ; code de sortie 0 |

**Pièces à venir, dans une version ultérieure (1.3) :** les exécutions lourdes du contre-audit (mutants, rejeu prédictif). Elles font environ 264 Mo, surtout des catalogues de tâches régénérables, et doivent être allégées avant publication.

**Chemins absolus.** Quelques scripts déjà exécutés contiennent, sur une seule ligne d'affectation, un chemin absolu du poste de l'auteur. Les `LISEZMOI` de leurs dossiers les indiquent. Ces scripts sont publiés à l'identique ; avant de les relancer, remplacer ce chemin par un chemin local.

## Ce que dit la note, et comment le vérifier

Statuts de la note (§ 1.3) : **démontré** (preuve complète, ou identité exacte rejouable) ; **sous GRH** (dépend de `bnfinit`) ; **assisté par calcul** (démontré sous des hypothèses nommées sur une exécution : M1, M2, H1–H3) ; **constaté** (sortie de programme sans valeur de preuve) ; **ouvert**. Les commandes se lancent depuis la racine du dépôt ; `py` désigne `python -I`, `gp` désigne `gp -q -D parisize=400000000 … < /dev/null`. Les sorties réelles sont dans `verification/RESULTATS.md`.

| Énoncé de la note | Statut (note) | Fichiers | Commande | Résultat rejoué |
|---|---|---|---|---|
| Notations : β₀ ≫ 0, β₀𝔇 = O⁺ ; H = (O_L, β₀) pair, unimodulaire | démontré | `data/corps/` | `py code/verification/verifier_corps.py` | 5 contrôles, 0 échec |
| Prop. 2.2 : h⁻(115) = 44 697 909 = 3·331·45 013 (formule analytique, arithmétique exacte) ; h⁻(87), h⁻(65), h⁻(85) | démontré (h⁺ = 1 : Miller) | — | `gp code/verification/hmoins115.gp` ; second calcul indépendant : `py code/verification/verifier_hmoins_caracteres.py` | 44 697 909 par les deux programmes ; 1 536, 64, 6 205 |
| Prop. 2.5, tableau 1 : caractères χ₃, χ₃₃₁, χ₄₅₀₁₃, noyaux, 508 463 orbites | démontré | — | `gp code/verification/caracteres115.gp` ; `py code/verification/verifier_hmoins_caracteres.py` | 508 463 orbites (et par Burnside) ; noyaux {1,22,24,68}, {1,91} |
| § 2.5 : H ≅ L₀ (P G Pᵀ = G_H, det P = −1) et Q G_art Qᵀ = G | démontré, sans GRH ; Sakamoto a la priorité | `data/L0/`, `externe/integer_input.txt` (à télécharger) | `py code/verification/verifier_H_L0.py` ; `py code/verification/verifier_conformite_article.py` | VALIDE ; VALIDE (avec le fichier de Sakamoto de SHA-256 `68af477c…631f`) |
| Th. 3.3 (isométrie), prop. 4.1, lemmes 4.2–4.5, th. 4.6 (critère) | démontré ; le th. 3.3 étend au conducteur composé 115 un argument de Quebbemann (1981), et le lemme 4.3 reprend une idée de Parseval de la même source (note, § 1.4, depuis la version 1.5) | preuves dans la note ; contrôles exacts du recollement et du seuil dans `verifier_raccord.py` (G5, G7, G8) | — | — |
| Th. 5.1 et cor. 5.2 (non-omission de `Rang88CertZ`) | démontré sous M1–M3 ; relu dans une portée limitée | `preuve/PREUVE_NON_OMISSION.md`, `preuve/LIAISON_PREUVE_CODE.md`, `code/certifiant/` | lecture ; recompilation : `REPRODUIRE.md` § 4 | 8 classes recompilées identiques octet pour octet |
| § 5.2, « Validation » : P₄₆₁ au seuil 7/2 ; harnais ; catalogues | constaté | `data/validation/`, `code/certifiant/` | `REPRODUIRE.md` § 4 | 697 u, 2 touches de norme 6 ; harnais (300 formes) 910 contrôles, 0 échec ; 4 catalogues identiques |
| Prop. 6.1, tableau 2 : huit idéaux rejetés par un vecteur de norme 6 (dont P₁₄₇₁ = (1471, ζ² + 879ζ + 948)) | démontré, sans GRH | `data/rejets/` | `gp code/verification/verifier_temoins.gp` ; `py code/verification/verifier_temoins.py` | 8 témoins valides sur 8, par les deux programmes ; empreintes conformes au tableau 2 ; décompositions des trois touches du § 6.1 |
| Prop. 6.3 (1), (2) et 6.4 (1), (2) : X₁₃₉, X₅₉₉ pairs, unimodulaires, définis positifs, de rang 88 ; vecteur de norme 8 ; raccord exact des fichiers d'entrée au réseau | démontré | `data/P139/entrees/`, `data/P599/entrees/`, `norme8.txt` | `py code/verification/verifier_raccord.py P139` (puis `P599`) | 37 contrôles, 0 échec, pour chacun |
| Prop. 6.3 (3) et 6.4 (3) : aucun vecteur non nul de norme ≤ 6 ; th. 6.11 (B) | assisté par calcul (M1, M2, H1–H3) | `data/P*/replication/` (exécutions de référence, second ordinateur, sans reprise), `data/P*/premiere_execution/`, `data/P*/cote*.taches` | `py code/verification/verifier_recus.py P139` (puis `P599`) | 87 et 98 contrôles, 0 échec ; empreintes canoniques `c99dcf87…5122`, `8ab1f40a…daf7`, `f3cf379a…2689`, `b9c93a83…8ef6` pour les deux exécutions ; aucun fichier de touche |
| P₅₉₉, « Sur l'hypothèse H4 » et « Rejeu des tâches reprises » | contrôle exact des fichiers (H4 n'est plus nécessaire) | `data/P599/premiere_execution/`, `data/P599/rejeu_reprises/` | `py code/verification/verifier_recus.py P599` (contrôles R8) | reprise : préfixe exact, 21 459 + 37 796 indices disjoints ; 21 459 reçus rejoués identiques |
| Prop. 6.6 : P₁₃₉³ non principal ; prop. 6.7 : ordre de [P₅₉₉] divisible par 331, composante 3 nulle | démontré, sans GRH | `data/P*/certificat_K22.txt` | `py code/verification/verifier_classe_P139.py` ; `py code/verification/verifier_classe_P599.py` | 24 et 37 contrôles, 0 échec |
| Rem. 6.10, prop. 6.9 : non-isométrie | démontré, sans GRH, modulo [Sak26] et le th. 3.3 | preuve dans la note ; 4·139 ≠ a² + 23b² et 599 = 24² + 23 contrôlés dans `verifier_classe_P599.py` (F) | — | — |
| Colonne « orbite » des tableaux 2 et 3 ; « neuf orbites distinctes » ; étiquettes d'orbite de P₁₃₉, P₅₉₉ | composante 3 : sans GRH ; 331 et 45 013 : sous GRH | `code/sous_grh/` | `gp -q -D parisize=800000000 code/sous_grh/localiser_classes.gp < /dev/null` | classes de N(P) dans Cl(F), Cl(K₂₂) ≅ Z/662, Cl(K₄₄) ≅ Z/45 013 |
| Préparation des entrées (§ 5.1 : A, B, Tₙ, d, bases ; BKZ-20) | outil (le raccord est contrôlé à part) | `code/preparation/` | `GP=gp sh code/preparation/preparer.sh` | les 22 fichiers d'entrée de P₁₃₉ et P₅₉₉ régénérés identiques octet pour octet |
| Tableau 3 (survivants partiels), Q1–Q7 | constaté ; ouvert | non inclus (voir plus bas) | — | — |

**Le théorème 6.11** (X₁₃₉ et X₅₉₉ sont extrémaux ; ni isométriques entre eux, ni à L₀, ni à L_S) est une **démonstration assistée par ordinateur** : il compose (A) le raccord géométrique, (B) le lien entre la preuve de non-omission et le code, appliqué aux quatre exécutions neuves du second ordinateur, et (C) le critère du th. 4.6. Il repose sur le modèle d'exécution M1, M2, H1–H3 (note, § 5.4), que les réplications étayent sans le démontrer. Il n'utilise ni H4, ni l'exactitude des compteurs, ni GRH. Aucune implantation indépendante du balayage n'a été exécutée.

## Structure

```
README.md, REPRODUIRE.md, CITATION.cff, LICENSE (MIT, code), LICENSE-CC-BY-4.0.md (textes et données), SHA256SUMS.txt, .gitignore
article/            rang88.tex, rang88.pdf (pdfLaTeX, trois passes)
code/certifiant/    Rang88CertZ.java, TestCertZ.java, classes/ (8 classes compilées, OpenJDK 11.0.16.1), rejouer_cote.sh
code/verification/  vérificateurs (Python, PARI/GP), tout_verifier.sh, empreinte_canonique.py, verifier_sha256.py
code/preparation/   scripts PARI/GP qui produisent les entrées (bnfinit sous GRH, BKZ), preparer.sh
code/sous_grh/      localisation des classes dans Cl(K₂₂), Cl(K₄₄) (sous GRH)
data/               corps/, P139/, P599/, rejets/, L0/, validation/ ; formats : data/LISEZMOI.md
externe/            LISEZMOI.md : où placer le fichier de R. Sakamoto (non redistribué)
preuve/             PREUVE_NON_OMISSION.md, LIAISON_PREUVE_CODE.md
verification/       RESULTATS.md : sorties réelles des vérifications rejouées depuis ce dépôt
addendum/           addendum (anglais, français ; sources, PDF), certificats de jumelage et du cadran sans GRH (version 1.1)
addendum/temoins_norme6/   témoins de norme 6 du tableau 4 et de la prop. 4.6, vérificateurs GP et Python, bilan et journaux des 21 filtres (version 1.2)
catalogue/          fiches .std au format du catalogue de Nebe et Sloane, constructions, vérificateurs (version 1.1)
verification_P4969/, verification_P4049/   raccord exact et non-isométrie de X₄₉₆₉ et X₄₀₄₉ (version 1.1)
calcul_externe_resultats_20261015/        balayages certifiés de X₄₉₆₉, X₄₀₄₉ et leurs réplications (version 1.1)
contre_audit_20261016/                    contre-audit du 16 octobre : bilans et scripts (version 1.1)
v14_P1151s24_et_candidat_P461s91/         X(P₁₁₅₁σ₂₄) et le CANDIDAT X(P₄₆₁σ₉₁) : constructions, balayages, vérificateurs et contrôles rejoués (version 1.4 ; statuts de X(P₄₆₁σ₉₁) mis à jour par la version 1.5)
addendum3/                                addendum 3 (anglais, français ; sources, PDF) (version 1.5)
v15_P3359_et_P461s91/                     X(P₃₃₅₉) et X(P₄₆₁σ₉₁) : balayages et réplications, certificat 45 013 sans GRH, recoupement enum88, raccord, contrôles rejoués (version 1.5)
CHANGEMENTS_V15.md                        liste des corrections de la version 1.5 : fichier, ligne, avant, après
```

## Fichiers conservés tels quels

Pour ne pas altérer les preuves, plusieurs fichiers sont des copies octet pour octet : `Rang88CertZ.java` (SHA-256 `9e467c75…c3c5`, cité par les reçus et par la note) et les huit classes compilées ; les reçus (`*.ckpt`), catalogues (`*.taches`) et journaux d'exécution ; les sept témoins de norme 6 dont la note cite l'empreinte abrégée, et le témoin de P₁₄₇₁ ; les fichiers d'entrée et `data/corps/rang88_m115c0_data.txt`. **L'en-tête de `Rang88CertZ.java` (lignes 12 à 33) et la première ligne de commentaire de sept fichiers témoins contiennent des mentions internes d'origine** (nom d'outil, auteur du code, date) ; elles sont laissées telles quelles, puisque toute modification changerait l'empreinte citée. Les vérificateurs repris du travail ont été adaptés (chemins relatifs au dépôt, commentaires) ; la logique des contrôles est inchangée, sauf mention dans leur en-tête.

## Ce qui n'est pas inclus

- **Le fichier de R. Sakamoto** (`data/L0/integer_input.txt` de son dépôt, révision `628ce2a7`, SHA-256 `68af477caf3f6d6a8980c40f234bcb47c0bac6caf3582c1757280cb64457631f`) : à télécharger soi-même (`externe/LISEZMOI.md`). Les vérificateurs contrôlent son empreinte avant toute lecture.
- **Le premier programme certifiant**, à intervalles, dont `Rang88CertZ` reprend des parties, et sa preuve.
- **Les journaux de lancement** (scripts de chaînage, relevés d'environnement) des deux ordinateurs, et le journal du rejeu des tâches reprises de P₅₉₉ : ils contiennent des chemins propres aux postes de travail. Leurs lignes de bilan sont recopiées dans `REPRODUIRE.md` ; les reçus correspondants sont inclus et contrôlés.
- **Les journaux de la campagne de validation** du § 5.2 (seuls les essais rejoués ici sont documentés), le filtre des survivants partiels (tableau 3) et les recherches non certifiantes (énumérateur flottant, filtre PARI/GP) : énoncés « constatés », sans rôle dans les preuves.

## Formalisation ultérieure

Aucune formalisation n'est fournie. Les énoncés finis suivants s'y prêteraient (par exemple en Lean, avec des certificats vérifiés par calcul) : les identités matricielles entières (unimodularité, parité et définie-positivité des matrices de Gram ; P G Pᵀ = G_H ; témoins xᵀGx = 6 et 8) ; le calcul exact de h⁻(115) et des normes de B₁,χ ; le décompte des orbites ; les certificats de classe dans K₂₂ (rangs de matrices modulo 331) ; l'arithmétique du seuil 1057/200. La non-omission du programme certifiant relève d'une vérification de programme, beaucoup plus lourde.

## Historique des versions

- **1.0** (15 octobre 2026, commit `f20d0bd`) : note, programmes, données et vérifications.
- **1.1** (17 octobre 2026, commit `89d8679`) : addendum (X₄₉₆₉ et X₄₀₄₉ extrémaux, jumeaux de la couche σ₂₄, cadran sans GRH), balayages certifiés et réplications, fiches au format du catalogue de Nebe et Sloane, contre-audit du 16 octobre.
- **1.2** (18 octobre 2026) : témoins de norme 6 des quatre rejets du tableau 4 et de la prop. 4.6 de l'addendum, avec leurs vérificateurs en PARI/GP et en Python ; bilan, audit et journaux des 21 filtres ; précision, dans ce README, du statut de la non-isométrie. Les textes de la note et de l'addendum sont inchangés.
- **1.3** (étiquette v1.3 du 22 octobre 2026 ; archivée sur Zenodo le 25 octobre 2026 sous la release v1.3.1, même contenu, la release v1.3 n'ayant pas été archivée) : traduction anglaise de la note (`article/rang88_en`), texte français mis à jour (celui de la soumission arXiv du 15 octobre), métadonnées `.zenodo.json` pour l'archivage avec DOI. Aucun nouveau calcul.
- **1.4** (31 octobre 2026) : horodatage de X(P₁₁₅₁σ₂₄), extrémal, et du **candidat** X(P₄₆₁σ₉₁), dans `v14_P1151s24_et_candidat_P461s91/`. X(P₁₁₅₁σ₂₄), I = (1151, ζ − 6)(1151, ζ − 605) : minimum 8 assisté par calcul, balayé deux fois sur deux machines (reçus identiques), non isométrique aux six extrémaux connus sans GRH. X(P₄₆₁σ₉₁), I = (461, ζ − 5)(461, ζ − 115), **CANDIDAT** : balayage exhaustif sans touche, **non répliqué** (seule la partie courte des reçus est recoupée, par ceux de P₄₆₁σ₂₄), minimum **annoncé par les auteurs** ; non isométrique sans GRH à X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉, X(P₁₁₅₁σ₂₄) et L_S, et à L₀ seulement sous GRH. Constructions, entrées, reçus, journaux, vérificateurs et contrôles rejoués. La note et l'addendum sont inchangés.
- **1.5** (7 novembre 2026) : addendum 3 (`addendum3/`) et dossier `v15_P3359_et_P461s91/`. X(P₃₃₅₉) : minimum 8 assisté par calcul, balayé deux fois sur deux machines (SpiraleG, Bertha), reçus identiques. X(P₄₆₁σ₉₁) : seconde exécution neuve sur Bertha, reçus identiques à l'octet à ceux de la version 1.4 ; ce n'est plus un candidat non répliqué. Certificat sans GRH de la composante 45 013 de sa classe, d'où sa non-isométrie à L₀ sans GRH. Recoupement numérique par une seconde implantation (`enum88.c`). Corrections de la note et de l'addendum (Quebbemann 1981, Bayer-Fluckiger 1984, statut de la non-isométrie, références), relevées dans `CHANGEMENTS_V15.md` ; avertissement en tête de `README_v14.md`.

## Attribution

Auteur : **Ivan Gauvin**, seul responsable scientifique. Claude Opus 5.5 (Anthropic) et Astra (OpenAI) ont assisté l'auteur ; ils ne sont pas auteurs. Leur usage est déclaré à la fin de la note et de chaque addendum ; Astra n'a relu aucune pièce de la version 1.5. La matrice de Gram de L₀ et les réseaux L₀ et L_S sont dus à R. Sakamoto (arXiv:2609.15633, v2).

**Licences** : les programmes de `code/` sont sous licence MIT (`LICENSE`) ; la note, les données, les preuves, les résultats de vérification et la documentation sont sous licence CC BY 4.0 (`LICENSE-CC-BY-4.0.md`). Les données de R. Sakamoto ne sont pas redistribuées. **Adresse publique du dépôt :** https://github.com/Katabolanga/rang88-reseaux-ideaux.

---

# English summary

Data, programs and checks accompanying the note *“Even unimodular ideal lattices of rank 88 over Q(ζ₁₁₅)”* by Ivan Gauvin (October 15, 2026, revised November 7, 2026; source and PDF in `article/`, compiled with pdfLaTeX, three passes), its addendum of October 17, 2026 (`addendum/`) and its Addendum 3 of November 7, 2026 (`addendum3/`).

**Version 1.5 (November 7, 2026).** Addendum 3 and the folder `v15_P3359_et_P461s91/` (see its `README_v15.md`). X(P₃₃₅₉), with I = (3359, ζ² + 2202ζ + 1829), a partial survivor of the note, was swept completely, twice, on two machines (SpiraleG, Oct. 19–21; Bertha, Nov. 6–7), with the same program and receipts identical task by task. X(P₄₆₁σ₉₁), a candidate in version 1.4, was swept again by a fresh run on Bertha (Nov. 7), which reproduces all 146 603 receipts byte for byte; it is no longer an unreplicated candidate. **The minimum 8 of both lattices is computer-assisted** (Thm. 4.6 of the note, `Rang88CertZ`, M1, M2, H1–H3), with a single program and no human audit; they are extremal only under these hypotheses. A certificate checked by a standard-library Python program shows, without GRH, that the 45 013-component of the class of X(P₄₆₁σ₉₁) is non-zero, so that X(P₄₆₁σ₉₁) is isometric neither to L₀ nor to L_S without GRH and without any computer-assisted step on our side. A second implementation of the criterion (`enum88.c`) gives a numerical cross-check, not a certificate. Under these hypotheses the family contains at least nine pairwise non-isometric extremal lattices of rank 88. The note and the addendum were corrected: the isometry theorem of the note extends an argument of Quebbemann (J. reine angew. Math. 326, 1981), which the note did not cite; Bayer-Fluckiger's Cor. 3.3 (1984) is cited as the upper bound it is; the status lines of the non-isometry now say that it requires the computer-assisted minimum of one of the two lattices compared, except with respect to L₀ and L_S. Every correction is listed in `CHANGEMENTS_V15.md`. The release v1.3 of October 22, 2026 was not archived on Zenodo; the first archive is that of release v1.3.1 (October 25, 2026).

The repository is self-contained, except for R. Sakamoto's Gram matrix of L₀, which is **not redistributed**: download `data/L0/integer_input.txt` from his repository at revision `628ce2a7` (SHA-256 `68af477c…631f`) and put it in `externe/` (see `externe/LISEZMOI.md`); the scripts check its digest before reading it as plain integers.

What can be checked (commands from the repository root; real outputs in `verification/RESULTATS.md`): h⁻(115) = 44 697 909 and the 508 463 Galois orbits (two independent exact computations, PARI/GP and Python); the integer isometry certificate H ≅ L₀; the eight norm-6 witnesses (two independent checkers); the exact link between the certifying program's input files and the lattices X₁₃₉, X₅₉₉, with a norm-8 vector; the receipts, logs and task catalogues of the certifying enumeration `Rang88CertZ`, run twice on two computers (Windows/OpenJDK 11 and Linux/OpenJDK 21) with byte-identical sorted receipts, the reference runs being fresh runs without resume and without any touch file; the class certificates in K₂₂ (without GRH); the GRH-dependent orbit labels; and the regeneration of all input files, byte for byte. The non-omission proof of the program is in `preuve/`, linked line by line to the source.

Status: the minimum 8 of X₁₃₉ and X₅₉₉ is a **computer-assisted proof** under the explicit execution model M1, M2, H1–H3 of the note. Non-isometry is proved without GRH, given the minimum 8 of at least one of the two lattices compared, which the isometry theorem requires; non-isometry to L₀ and L_S does not depend on the computer-assisted minimum. No independent implementation of the enumeration has been run, and no human specialist has reviewed the proofs.

Version 1.3 adds an English translation of the note (`article/rang88_en.pdf`; the French original prevails), the updated French text submitted to arXiv on October 15, 2026, and Zenodo archive metadata (`.zenodo.json`); no new computation. Version 1.1 (October 17, 2026) adds the addendum (X₄₉₆₉ and X₄₀₄₉, twins of the σ₂₄-layer, the dial without GRH) and its data. Version 1.2 (October 18, 2026) adds the norm-6 witnesses of the addendum: the four filter rejections of Table 4, and Proposition 4.6, on which Theorem B relies. They come with a PARI/GP checker and a PARI-free Python checker, in `addendum/temoins_norme6/`.

Version 1.4 timestamps two further lattices in `v14_P1151s24_et_candidat_P461s91/`: X(P₁₁₅₁σ₂₄), whose minimum 8 is computer-assisted and was swept twice on two machines with identical receipts, and the **candidate** X(P₄₆₁σ₉₁), swept once without touch (not replicated, only the short part of its receipts cross-checked; minimum claimed by the authors; non-isometric to L₀ only under GRH). The note and the addendum are unchanged.

Author: Ivan Gauvin. Claude Opus 5.5 (Anthropic) and Astra (OpenAI) assisted the author; they are not authors. **Licences:** MIT for the programs in `code/` (`LICENSE`); CC BY 4.0 for the article, data, proofs, verification results and documentation (`LICENSE-CC-BY-4.0.md`); public address of the repository: https://github.com/Katabolanga/rang88-reseaux-ideaux.
