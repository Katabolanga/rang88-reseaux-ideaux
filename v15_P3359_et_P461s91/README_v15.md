# Version 1.5 : X(P₃₃₅₉) et X(P₄₆₁σ₉₁), de minimum 8 assisté par calcul ; la composante 45 013 sans GRH

> **Statuts, à lire d'abord.** Le minimum 8 de X(P₃₃₅₉) et de X(P₄₆₁σ₉₁) est **assisté par calcul** : critère du th. 4.6 de la note, programme `Rang88CertZ`, modèle d'exécution M1, M2, H1–H3 (note, § 5.4). Chaque côté a été balayé sans touche **deux fois, sur deux machines, avec le même programme** ; il n'existe **aucune implantation indépendante** qui certifie ce minimum, et **aucun humain n'a audité** ces pièces. Ces deux réseaux ne sont extrémaux que sous ces hypothèses, comme X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉ et X(P₁₁₅₁σ₂₄).

*English version below.*

Ce dossier publie les données de l'**addendum 3** (`addendum3/addendum3_en.pdf`, `addendum3/addendum3_fr.pdf`) : les deux balayages complets de X(P₃₃₅₉), les deux balayages de X(P₄₆₁σ₉₁) (le premier, publié comme candidat dans la version 1.4 ; le second, neuf), un certificat sans GRH sur la composante 45 013 de la classe de X(P₄₆₁σ₉₁), un recoupement numérique par une seconde implantation, et les journaux des contrôles rejoués le 7 novembre 2026.

| Réseau | Minimum 8 | Exécutions | Non-isométrie |
|---|---|---|---|
| **X(P₃₃₅₉)**, I = (3359, ζ² + 2202ζ + 1829), premier de degré 2 | **assisté par calcul** (M1, M2, H1–H3) ; non audité | SpiraleG (19–21 oct.) et Bertha (6–7 nov.), même programme, reçus identiques tâche par tâche | non-conjugaison aux huit autres classes : démontrée sans GRH ; non-isométrie : par le th. 3.3, sous le minimum 8 assisté de l'un des deux réseaux comparés ; à L₀, L_S : sans calcul assisté de notre part |
| **X(P₄₆₁σ₉₁)**, I = (461, ζ − 5)(461, ζ − 115) | **assisté par calcul** (M1, M2, H1–H3) ; non audité | Crapaud08 (19–20 oct., version 1.4) et Bertha (7 nov.), même programme ; les 146 603 reçus sont identiques à l'octet | à L₀ et L_S : **démontrée sans GRH**, modulo le th. 3.3 et le minimum 8 de Sakamoto, sans calcul assisté de notre part (certificat 45 013) ; aux six autres : sous le minimum 8 assisté de l'un des deux |

Les statuts suivent ceux de la note (§ 1.3) : démontré, sous GRH, assisté par calcul, constaté, ouvert.

## 1. Ce qui change par rapport à la version 1.4

- **X(P₄₆₁σ₉₁) n'est plus un candidat non répliqué.** L'exécution de Bertha, neuve et en un seul lancement par côté, redonne tous les reçus de Crapaud08, à l'octet, partie fibre comprise ; les 670 reçus hérités que rien ne recoupait le sont désormais. Les statuts « candidat, non répliqué » et « minimum annoncé par les auteurs » du dossier `v14_P1151s24_et_candidat_P461s91/` sont caducs ; ce dossier est conservé tel quel, avec un avertissement en tête de son README.
- **La non-isométrie de X(P₄₆₁σ₉₁) à L₀ ne dépend plus de GRH.** Le certificat de `certificat_45013/` montre que la composante 45 013 de sa classe est non nulle (addendum 3, prop. 1.2 et cor. 1.3).
- **X(P₃₃₅₉)**, « survivant partiel » de la note (tableau 3), a été balayé en entier, deux fois. Ses entrées, publiées ici, sont celles du lot du 19 octobre ; leur `I_data.gp` est identique à celui que la version 1.4 publiait déjà (`v14_…/verification/data/P3359/entrees/I_data.gp`).

## 2. Statuts détaillés

### 2.1 X(P₃₃₅₉)

- **Place dans S** (démontré, sans GRH). Couche σ₂₄, anneau extérieur, heure 2 (addendum, tableau 3, prop. 4.7, cor. 4.8). Composante 3 nulle (4·3359 = 48² + 23·22²), composante 45 013 nulle (classe fixée par σ₂₄, χ₄₅₀₁₃(24) = −1). L'idéal des fichiers est un conjugué galoisien du représentant du cadran, (3359, ζ² + 17ζ + 417) : même orbite.
- **Raccord exact** (démontré). `verifier_raccord_tranche1.py P3359` : 37 contrôles sur 37, en entiers et rationnels, sans PARI/GP. Gram en base LLL (`verification/detecteur_copie/gram/P3359.gram`, diagonale de 26 à 54) raccordée à la construction exacte : 8 + 5 contrôles PARI/GP.
- **Balayages** (assisté par calcul). B_A = 1057/200, S = 12, les huit classes publiées de `code/certifiant/classes/`, même invocation :

| Côté | Tâches | Catalogue (SHA-256) | Exécution 1 : SpiraleG, Windows 11, OpenJDK 11.0.16.1, 14 fils | Exécution 2 : Bertha, Linux (WSL Ubuntu 24.04), OpenJDK 21.0.12.1, 16 fils | Empreinte canonique (les deux exécutions) |
|---|---|---|---|---|---|
| 1 | 109 662 | `32900e663a387c75…` | 19 oct. 18 h 34 → 20 oct. 19 h 10 (CEST), 88 546 s | 6 nov. 13 h 11 → 22 h 45 (CET), 34 448 s | `9fc5bb7437cf86d8ed076c0358caab0eb889170942391e434bacf0c2346387ad` |
| 2 | 107 548 | `088d53a7470411c7…` | 20 oct. 19 h 10 → 21 oct. 23 h 16 (CEST), 101 155 s | 6 nov. 22 h 45 → 7 nov. 9 h 40 (CET), 39 337 s | `a5e5f7b989218a71a087db648cd2fe73a8e130833a50b93a7c5bf9792ebf96b3` |

  - Chaque exécution est un lancement unique : point de contrôle neuf, aucune reprise, code Java 0, flux d'erreur vide, couverture complète, **aucune touche**, aucun fichier de touche ; verdict du lanceur `COMPLET_SANS_TOUCHE` (code 0) sur les deux machines.
  - |U| = 1 044 123 618 sur chaque côté ; les nombres de nœuds sont identiques d'une machine à l'autre.
  - Les reçus des deux exécutions sont identiques tâche par tâche (109 662 et 107 548 reçus) ; les fichiers bruts ne diffèrent que par l'ordre d'écriture des fils.
- **Non-conjugaison** (démontré, sans GRH, modulo note prop. 2.2, 2.5 et addendum prop. 4.7) : `verifier_non_isometrie_tranche1.py` de la version 1.4 (123 contrôles sur 123) traite P₃₃₅₉ : composante 331 non nulle d'heure 2, hors des orbites de X₅₉₉ (heure 8), X(P₁₁₅₁σ₂₄) (heure 6), X₁₃₉, X₄₉₆₉, X₄₀₄₉ (anneau intérieur), L₀, L_S ; et la composante 331 de X(P₄₆₁σ₉₁) est nulle.

### 2.2 X(P₄₆₁σ₉₁)

- **Exécution 2** (Bertha, 7 nov., OpenJDK 21.0.12.1, 8 fils, lot de la version 1.4 inchangé, 35 empreintes sur 35) : côté 1 (73 244 tâches) de 10 h 09 à 13 h 39 (12 628 s), côté 2 (73 359 tâches) de 13 h 39 à 17 h 03 (12 191 s), un seul lancement neuf par côté, aucune touche, verdict `COMPLET_SANS_TOUCHE` (code 0). Contrôle d'exécution : 28 sur 28 par côté (E7 contre les filtres du 17 oct.), 29 sur 29 avec E7 contre les reçus de Crapaud08.
- **Comparaison** : 73 244 et 73 359 reçus identiques à l'octet à ceux de Crapaud08 publiés en version 1.4 ; empreintes canoniques `db04c32e641f75bcce3739f09921e3aab27917903b4b4e36aedafae518eaa1e4` et `652ef2f89497cb0784326c1ab280b86b99febb3206749f3ee4592c4f59936d13`, égales à celles de la version 1.4. Le contrôle de fin (`controle_fin/CONTROLE_FIN_P461s91.txt`, fait sur Bertha le 7 nov. à 20 h 41) imprime 14 OK et 0 échec.
- **Composante 45 013** (démontré, sans GRH, modulo le théorème de Stickelberger et l'indice des unités, Washington, th. 6.10 et 4.12). `certificat_45013/certificat_45013_P461s91.json` (SHA-256 `512b1944…`) et son vérificateur `verifier_certificat_45013.py` (SHA-256 `836a0a1a…`, bibliothèque standard de Python seulement, ne recalcule aucune somme de Jacobi) : 462 contrôles, 0 échec ; symboles 24 733, 30 643 et 4 522 aux premiers auxiliaires 20 705 981, 62 117 941 et 186 353 821. Trois certificats altérés (`essais_negatifs/`) sont rejetés : α altéré (49 échecs), autre caractère (4), ω complémentaire (176). Le « lemme 2 de NOTE.md » cité dans l'en-tête du vérificateur est le lemme 3.2 de l'addendum 3 ; le vérificateur n'a pas été modifié, pour garder son empreinte. Il ne contrôle pas que p = 45 013 est premier (c'est immédiat).

### 2.3 Recoupement par une seconde implantation (constaté)

`recoupement_enum88/enum88.c` est un second programme pour le critère du th. 4.6, écrit par l'assistant sans reprendre le code de `Rang88CertZ` (Fincke–Pohst par intervalles, Cholesky en double, décisions finales en entiers). Binaire statique utilisé : SHA-256 `53a2b7640345b183…` (`compiler_statique.sh`).
- Contrôle positif (validation P₄₆₁, seuil 7/2) : 697 projections courtes et les deux mêmes touches que `Rang88CertZ` (`controle_positif_P461_seuil_7_2.log`, rejoué le 7 nov. à 22 h 01).
- X(P₄₆₁σ₉₁), mode complet, les deux côtés, Bertha, 7 nov. (`m1_P461s91_cote1.log`, `m1_P461s91_cote2.log`) : même |U| = 143 529 602, même histogramme sur ses 32 cases, même nombre de CVP, **aucune touche**, code 0. `comparer_enum88.py` : 6 contrôles sur 6 par côté, contre les journaux de Bertha et de Crapaud08.
- **Ce n'est pas un certificat** : bornes en flottants sans analyse d'erreur, mêmes fichiers d'entrée, même critère, même auteur. Il n'a pas été exécuté sur X(P₃₃₅₉).

## 3. Contenu

```
README_v15.md
balayages/
  P3359_SpiraleG_20261019/            exécution 1 de X(P3359) : sorties/ (reçus, catalogues, journaux, contrôles, verdict, RECU_P3359.txt,
                                      SHA256SUMS_SORTIES.txt, autotest/), lancer_spiraleg.out ; lot/ (lanceur, SHA256SUMS.txt du lot,
                                      ref/ATTENDU_P3359.txt et six fichiers de reçus de référence pour E7)
  P3359_replication_Bertha_20261106/  exécution 2 de X(P3359) : sorties/ sans les catalogues .taches (identiques à ceux de l'exécution 1), lancer_bertha.out
  P461s91_replication_Bertha_20261107/  exécution 2 de X(P461σ91) : sorties/ sans les catalogues .taches (identiques à ceux de la version 1.4),
                                      lancer_bertha_P461s91.out ; controle_fin/ (CONTROLE_FIN_P461s91.txt, sorties intermédiaires, controle_fin_p461.sh)
certificat_45013/                     certificat, vérificateur, essais_negatifs/ (trois certificats altérés)
recoupement_enum88/                   enum88.c, scripts de compilation et de lancement, journaux, comparer_enum88.py
verification/                         raccord exact de X(P3359) (lancer les commandes depuis ce dossier)
  code/                               verifier_raccord_tranche1.py et ses deux originaux (outils_inchanges/), copies identiques à ceux de la version 1.4 ;
                                      raccord_detecteur.gp (identique) et son pilote raccord_detecteur_P3359.gp
  data/P3359/entrees/                 les 11 entrées (I_data.gp, coteN_A.gram, coteN_B.gram, coteN_T.mat, coteN_meta.txt, coteN_bases.gp)
  data/P3359/journaux/                journaux des catalogues du 19 oct. et des exécutions partielles antérieures (lus par le contrôle G6)
  data/corps/                         rang88_m115c0_data.txt, identique à celui du dépôt
  detecteur_copie/                    Gram de X(P3359) en base LLL, matrice de passage U, journal ; commun_rang88.gp (identique)
controles_preparation_20261107/journaux/   journaux des contrôles rejoués le 7 novembre 2026 (§ 5)
```

## 4. Rejouer

Depuis la racine du dépôt, avec Python ≥ 3.9 (bibliothèque standard seulement). `O` désigne `v14_P1151s24_et_candidat_P461s91/balayages/outils` et `V` désigne `v15_P3359_et_P461s91`.

```
# certificat sans GRH (quelques minutes)
cd v15_P3359_et_P461s91/certificat_45013
python3 -I verifier_certificat_45013.py certificat_45013_P461s91.json          # 462 controles, 0 echecs ; code 0
python3 -I verifier_certificat_45013.py essais_negatifs/chi_autre.json          # certificat REJETE ; code 1 (idem pour les deux autres)
cd ../..

# exécution 1 de X(P3359), avec E7 contre les références du lot
python3 -I $O/controle_execution.py $V/balayages/P3359_SpiraleG_20261019/sorties/run_P3359_cote1 1 109662 32900e663a387c75d112bf5b9effba06ece70822b1fad4d1be10f74e85386ea0 $V/balayages/P3359_SpiraleG_20261019/lot/ref/*cote1.ckpt     # 31 controles, 0 echecs
python3 -I $O/controle_execution.py $V/balayages/P3359_SpiraleG_20261019/sorties/run_P3359_cote2 2 107548 088d53a7470411c74729dc1068267fb949483abb6c9412e5df4f46442b4b5518 $V/balayages/P3359_SpiraleG_20261019/lot/ref/*cote2.ckpt     # 29 controles, 0 echecs

# empreintes canoniques et comparaison des reçus des deux machines
python3 -I $O/empreinte_canonique.py $V/balayages/*/sorties/run_*_cote*/cote*.ckpt
python3 -I $O/compare_recus.py $V/balayages/P3359_replication_Bertha_20261106/sorties/run_P3359_cote1/cote1.ckpt $V/balayages/P3359_SpiraleG_20261019/sorties/run_P3359_cote1/cote1.ckpt     # COMPARAISON_OK (idem cote 2)
python3 -I $O/compare_recus.py $V/balayages/P461s91_replication_Bertha_20261107/sorties/run_P461s91_cote1/cote1.ckpt v14_P1151s24_et_candidat_P461s91/balayages/CANDIDAT_P461s91_non_replique_Crapaud08_V2_20261019/sorties/run_P461s91_cote1/cote1.ckpt     # COMPARAISON_OK (idem cote 2)

# recoupement enum88
python3 -I $V/recoupement_enum88/comparer_enum88.py $V/recoupement_enum88/m1_P461s91_cote1.log $V/balayages/P461s91_replication_Bertha_20261107/sorties/run_P461s91_cote1/cote1_20261107_100928.stdout.log     # 6 controles, 0 echecs
```

`controle_execution.py` lit le catalogue `cote<s>.taches` dans le dossier de l'exécution. Pour les deux exécutions de Bertha, dont les catalogues ne sont pas republiés, le lancer sur une copie du dossier `run_*_cote<s>/` où l'on a placé le catalogue de la première exécution (même SHA-256) ; on peut ajouter les reçus de la première exécution comme référence E7. Résultats attendus : 28 contrôles sur 28 (X(P₃₃₅₉), E7 contre SpiraleG) et 29 sur 29 (X(P₄₆₁σ₉₁), E7 contre Crapaud08 et contre les filtres du 17 oct.).

Depuis `v15_P3359_et_P461s91/verification/` :

```
python3 -I code/verifier_raccord_tranche1.py P3359                              # BILAN : 37 controles, 0 echecs ; FIN_OK
gp -q -D parisize=400000000 code/raccord_detecteur_P3359.gp < /dev/null          # RACCORD_DETECTEUR_OK P3359 (PARI/GP 2.15.4)
```

Depuis `v14_P1151s24_et_candidat_P461s91/verification/` (non-conjugaison de P₃₃₅₉, composantes 3 et 331 de P₄₆₁σ₉₁) :

```
python3 -I code/verifier_non_isometrie_tranche1.py                             # BILAN : 123 controles, 0 echecs
```

Les balayages eux-mêmes (de 3 à 28 heures par côté) ne sont pas relancés ; l'invocation figure en tête de chaque journal et dans `lot/lancer_cert_P3359.sh` (pour X(P₄₆₁σ₉₁), dans le lanceur du lot de la version 1.4).

## 5. Contrôles rejoués le 7 novembre 2026

Sur le poste de l'auteur (Windows 11, Python 3.11, PARI/GP 2.15.4), sur les fichiers de ce dossier. Journaux dans `controles_preparation_20261107/journaux/`.

| Journal | Contrôle | Résultat |
|---|---|---|
| 01, 02 | certificat 45 013 ; trois certificats altérés | 462 contrôles, 0 échec, code 0 ; les trois altérés rejetés (49, 4 et 176 échecs), code 1 |
| 03 (×2) | `controle_execution.py`, exécution 1 de X(P₃₃₅₉), E7 contre les références du lot | 31/31 et 29/29 |
| 04 (×2) | idem, exécution 2 (Bertha), sur une copie avec catalogue, E7 contre l'exécution 1 | 28/28 par côté ; 109 662 et 107 548 reçus communs, 0 différent |
| 05 (×2) | idem, X(P₄₆₁σ₉₁) sur Bertha, E7 contre Crapaud08 et les filtres du 17 oct. | 29/29 par côté ; 73 244 et 73 359 reçus communs, 0 différent |
| 06 | empreintes canoniques des huit fichiers de reçus | égales deux à deux, conformes aux tableaux ; aucune touche |
| 07, 08 | `compare_recus.py`, Bertha contre SpiraleG (X(P₃₃₅₉)) et contre Crapaud08 (X(P₄₆₁σ₉₁)) | COMPARAISON_OK, 0 différent, 4 fois |
| 09 (×2) | `comparer_enum88.py`, contre Bertha et contre Crapaud08 | 6/6, 4 fois |
| 10 | `verifier_raccord_tranche1.py P3359` | 37/37, FIN_OK |
| 11 | `verifier_non_isometrie_tranche1.py` (version 1.4) | 123/123 |
| 12 | `raccord_detecteur_P3359.gp` | 8 + 5 contrôles, RACCORD_DETECTEUR_OK |

Les tables `SHA256SUMS_SORTIES.txt` des trois exécutions publiées ici ont été vérifiées avec `sha256sum -c` : toutes conformes, aux catalogues non republiés près (leurs empreintes, dans ces tables, sont celles des catalogues publiés).

## 6. Ce qui n'est pas revendiqué

- **Aucune preuve formelle.** Le minimum 8 est assisté par calcul, sous M1, M2, H1–H3 ; les réplications étayent ce modèle sans le démontrer. Un seul programme (`Rang88CertZ`), un seul auteur ; `enum88.c` n'est qu'un recoupement numérique, du même auteur.
- **Non-isométries.** La non-conjugaison des classes est démontrée sans GRH ; la non-isométrie s'en déduit par le th. 3.3 de la note (relu par un second assistant, pas par un spécialiste), sous le minimum 8 assisté de l'un des deux réseaux comparés, sauf vis-à-vis de L₀ et L_S.
- Le lemme de type Kummer (addendum 3, lemme 3.2) a été rédigé par l'assistant et relu par une seconde instance du même assistant, pas par un humain. Le théorème de Stickelberger et l'indice des unités sont cités, non redémontrés.
- Aucune étiquette ni heure sur l'anneau σ₉₁ n'est revendiquée. Les énoncés de la remarque 3.4 de l'addendum 3 (colonnes « orbite » de la note sans GRH, quatre orbites de taille 88 distinctes, nullité pour le premier au-dessus de 157 146 581) sont constatés, et leurs programmes ne sont pas publiés.
- Aucun vecteur de norme 8, groupe d'automorphismes ou fiche de catalogue n'est donné pour X(P₃₃₅₉) ou X(P₄₆₁σ₉₁) ; rien n'est affirmé sur le nombre total de réseaux extrémaux de rang 88.
- Les scripts et vérificateurs écrits pour ce dossier (`comparer_enum88.py`, `enum88.c`, le certificat et son vérificateur) sont dus à l'assistant (Claude) ; aucun humain ne les a relus.

## 7. Pièces non incluses

- Les catalogues `.taches` des deux exécutions de Bertha : identiques à l'octet à ceux de la première exécution (`32900e66…`, `088d53a7…` pour X(P₃₃₅₉) ; `0189bac3…`, `388a5734…` pour X(P₄₆₁σ₉₁)) et au catalogue d'autotest (`30d7a99f…`).
- Les autres fichiers du lot de X(P₃₃₅₉), listés dans `lot/SHA256SUMS.txt` : les classes, sources et entrées de validation sont identiques à celles de `code/certifiant/` et de `data/validation/P461/` ; la description du lot (`README_LOT.md`) et son manifeste contiennent des éléments internes et ne sont pas publiés.
- Le programme de contre-vérification du certificat écrit par la seconde instance de l'assistant (quatrième premier auxiliaire 310 589 701, symbole 19 454), et les programmes de la remarque 3.4 de l'addendum 3.

**Chemins et noms internes.** Plusieurs journaux et scripts (`lancer_*.sh`, `compiler_statique.sh`, `lancer_enum88_apres_java.sh`, journaux 04 et 05 du § 5, journaux de `enum88`) contiennent des chemins des postes de l'auteur ou des noms de machines (SpiraleG, Bertha, Crapaud08). Ils sont publiés à l'identique.

## Attribution

Auteur : Ivan Gauvin. Claude Opus 5.5 (Anthropic) a assisté l'auteur ; il n'est pas auteur. Astra (OpenAI) n'a relu aucune pièce de ce dossier. Licences du dépôt : MIT pour les programmes, CC BY 4.0 pour les données et la documentation.

---

# Version 1.5: X(P₃₃₅₉) and X(P₄₆₁σ₉₁), of computer-assisted minimum 8; the 45 013-component without GRH

> **Statuses first.** The minimum 8 of X(P₃₃₅₉) and X(P₄₆₁σ₉₁) is **computer-assisted**: criterion of Thm. 4.6 of the note, program `Rang88CertZ`, execution model M1, M2, H1–H3 (note, § 5.4). Each side was swept without any hit **twice, on two machines, with the same program**; **no independent implementation** certifies this minimum, and **no human has audited** these records. The two lattices are extremal only under these hypotheses, like X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉ and X(P₁₁₅₁σ₂₄).

This folder holds the data of **Addendum 3** (`addendum3/addendum3_en.pdf`, `addendum3/addendum3_fr.pdf`): both complete sweeps of X(P₃₃₅₉); both sweeps of X(P₄₆₁σ₉₁) (the first one published as a candidate in version 1.4, the second one new); a certificate, without GRH, on the 45 013-component of the class of X(P₄₆₁σ₉₁); a numerical cross-check by a second implementation; and the logs of the checks replayed on November 7, 2026.

| Lattice | Minimum 8 | Runs | Non-isometry |
|---|---|---|---|
| **X(P₃₃₅₉)**, I = (3359, ζ² + 2202ζ + 1829), a prime of degree 2 | **computer-assisted** (M1, M2, H1–H3); not audited | SpiraleG (Oct. 19–21) and Bertha (Nov. 6–7), same program, receipts identical task by task | non-conjugacy to the eight other classes: proved without GRH; non-isometry: by Thm. 3.3, under the computer-assisted minimum 8 of one of the two lattices compared; to L₀, L_S: no computer-assisted step on our side |
| **X(P₄₆₁σ₉₁)**, I = (461, ζ − 5)(461, ζ − 115) | **computer-assisted** (M1, M2, H1–H3); not audited | Crapaud08 (Oct. 19–20, version 1.4) and Bertha (Nov. 7), same program; all 146 603 receipts byte-identical | to L₀ and L_S: **proved without GRH**, modulo Thm. 3.3 and Sakamoto's minimum 8, with no computer-assisted step on our side (45 013 certificate); to the six others: under the computer-assisted minimum 8 of one of the two |

**What changes since version 1.4.** X(P₄₆₁σ₉₁) is no longer an unreplicated candidate: the Bertha run, fresh and in a single launch per side, reproduces every receipt of the Crapaud08 run byte for byte, fibre part included, so the 670 inherited receipts that nothing cross-checked are now cross-checked. Its non-isometry to L₀ no longer depends on GRH: the certificate in `certificat_45013/` shows that the 45 013-component of its class is non-zero (Addendum 3, Prop. 1.2 and Cor. 1.3). X(P₃₃₅₉), a "partial survivor" of the note (Table 3), was swept completely, twice. The folder `v14_P1151s24_et_candidat_P461s91/` is kept unchanged, with a notice at the top of its README.

**X(P₃₃₅₉).** Exact link of the inputs: 37/37 (`verifier_raccord_tranche1.py P3359`, no PARI/GP); LLL Gram linked to the exact construction by 8 + 5 PARI/GP checks. Place in S: σ₂₄-layer, outer ring, hour 2 (addendum, Table 3, Prop. 4.7), without GRH. Run 1: SpiraleG (Windows 11, OpenJDK 11.0.16.1, 14 threads), Oct. 19–21, 88 546 s and 101 155 s. Run 2: Bertha (Linux under WSL, OpenJDK 21.0.12.1, 16 threads), Nov. 6–7, 34 448 s and 39 337 s. Side 1: 109 662 tasks, catalogue `32900e66…`, canonical fingerprint `9fc5bb74…87ad`; side 2: 107 548 tasks, catalogue `088d53a7…`, canonical fingerprint `a5e5f7b9…96b3`; equal for both runs. Each run is a single fresh launch, Java exit code 0, empty error stream, no hit; |U| = 1 044 123 618 per side; receipts identical task by task.

**X(P₄₆₁σ₉₁).** Run 2 on Bertha (Nov. 7, OpenJDK 21.0.12.1, 8 threads, unchanged batch of version 1.4): 12 628 s and 12 191 s, single fresh launch per side, no hit, launcher verdict `COMPLET_SANS_TOUCHE`. Execution check 28/28 per side (29/29 with E7 against the Crapaud08 receipts); 73 244 and 73 359 receipts byte-identical to the published ones; canonical fingerprints `db04c32e…a1e4` and `652ef2f8…6d13`, as in version 1.4. **45 013-component** (proved, without GRH, modulo Stickelberger's theorem and the unit index, Washington, Thms 6.10 and 4.12): the checker `verifier_certificat_45013.py` uses only the Python standard library and recomputes no Jacobi sum; 462 checks, no failure; symbols 24 733, 30 643, 4 522 at the auxiliary primes 20 705 981, 62 117 941, 186 353 821; three altered certificates are rejected. The "lemme 2 de NOTE.md" quoted in the checker's header is Lemma 3.2 of Addendum 3; the checker is unchanged, to keep its fingerprint.

**Cross-check (observed).** `enum88.c`, a second program for the criterion of Thm. 4.6, written by the assistant without reusing the code of `Rang88CertZ`, reproduces the validation case (697 short projections, the same two hits) and, on both sides of X(P₄₆₁σ₉₁), the same |U| = 143 529 602, the same 32-bin histogram, the same number of closest-vector searches and no hit. It is not a certificate (floating-point bounds without error analysis, same inputs, same criterion, same author), and it was not run on X(P₃₃₅₉).

**Replay.** Commands are in § 4 above (they are the same in English); the expected results are given in comments. The checks replayed on November 7, 2026 are listed in § 5 and logged in `controles_preparation_20261107/journaux/`. For the two Bertha runs, whose task catalogues are not republished, run `controle_execution.py` on a copy of the run folder with the catalogue of the first run (same SHA-256) added.

**Not claimed.** No formal proof; a single program and a single author for the minimum; non-isometry to lattices other than L₀ and L_S requires the computer-assisted minimum of one of the two; the Kummer-type lemma was reread by a second instance of the same assistant, not by a human; no orbit label on the σ₉₁-ring; the statements of Remark 3.4 of Addendum 3 are observed only, and their programs are not published; no norm-8 vector, automorphism group or catalogue entry; nothing on the total number of extremal lattices of rank 88. **Not included:** the duplicate task catalogues of the Bertha runs; the lot description and manifest of X(P₃₃₅₉) (internal); the counter-check program of the second instance of the assistant. Several scripts and logs contain local paths or machine names; they are published unchanged.

Author: Ivan Gauvin. Claude Opus 5.5 (Anthropic) assisted the author; it is not an author. Astra (OpenAI) did not review this folder. Licences: MIT for the programs, CC BY 4.0 for data and documentation.
