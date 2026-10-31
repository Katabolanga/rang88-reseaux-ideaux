# Version 1.4 : horodatage de X(P₁₁₅₁σ₂₄), extrémal, et du CANDIDAT X(P₄₆₁σ₉₁)

> **X(P₄₆₁σ₉₁) est publié comme CANDIDAT.** Son minimum 8 est seulement **annoncé par les auteurs** : le balayage n'a **pas été répliqué**, et seule la partie courte de ses reçus est recoupée, par ceux de P₄₆₁σ₂₄ (la partie fibre ne l'est pas). Sa non-isométrie à L₀ n'est démontrée que **sous GRH**. Seul X(P₁₁₅₁σ₂₄) a un minimum assisté par calcul et répliqué.

*English version below.*

Ce dossier date publiquement deux réseaux idéaux pairs unimodulaires de rang 88 sur L = ℚ(ζ₁₁₅), construits comme ceux de la note et de son addendum : X(P₁₁₅₁σ₂₄), extrémal (minimum assisté par calcul et répliqué), et X(P₄₆₁σ₉₁), **candidat** (minimum annoncé, non répliqué). Il contient leurs constructions exactes, les entrées, les reçus et les journaux de leurs balayages, ainsi que les vérificateurs et leurs journaux. **La note et l'addendum ne changent pas.** Aucune pièce de ce dossier n'a été relue par un spécialiste humain.

Les deux réseaux n'ont pas le même statut ; X(P₄₆₁σ₉₁) est un **candidat** :

| Réseau | Minimum 8 | Réplication | Non-isométrie aux réseaux connus |
|---|---|---|---|
| **X(P₁₁₅₁σ₂₄)** | **assisté par calcul** (M1, M2, H1–H3), par balayage exhaustif des deux côtés du critère, sans touche | **oui** : deux exécutions sur deux machines différentes, reçus identiques (empreintes canoniques égales) | démontrée sans GRH, aux six réseaux extrémaux connus (L₀, L_S, X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉) |
| **X(P₄₆₁σ₉₁) : CANDIDAT** | **annoncé par les auteurs, NON répliqué** : balayage exhaustif des deux côtés, sans touche, sur une seule machine | **non** ; seule la partie courte des reçus est recoupée (par les reçus de P₄₆₁σ₂₄), pas la partie fibre | démontrée sans GRH à X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉, X(P₁₁₅₁σ₂₄) et L_S ; **à L₀, seulement sous GRH** |

Les statuts suivent ceux de la note (§ 1.3) : démontré, sous GRH, assisté par calcul, constaté, ouvert.

## 1. Les deux réseaux

Comme dans la note, X_I = (I, β₀/ν) désigne le réseau idéal de rang 88 attaché à un idéal entier I de 𝒪_L tel que I + Ī = 𝒪_L, où ν ∈ 𝒪_{L⁺} engendre IĪ. Les deux idéaux sont des produits de **deux premiers de degré résiduel 1**, échangés par un automorphisme de Galois σ_k. Ce ne sont pas des premiers de degré 2, comme P₁₃₉ ou P₄₉₆₉.

| | X(P₁₁₅₁σ₂₄) | X(P₄₆₁σ₉₁) (**candidat**) |
|---|---|---|
| Idéal | I = P·σ₂₄(P) = (1151, ζ − 6)(1151, ζ − 605), car 6²⁴ ≡ 605 (mod 1151) | I = P·σ₉₁(P) = (461, ζ − 5)(461, ζ − 115), car 5⁹¹ ≡ 115 (mod 461) ; σ₉₁ est une involution |
| Norme de I | 1151² = 1 324 801 | 461² = 212 521 |
| Stabilité | σ₂₄(I) = I (couche σ₂₄) | σ₉₁(I) = I |
| Ī | (1151, ζ − 192)(1151, ζ − 1073) | (461, ζ − 369)(461, ζ − 457) |
| Construction exacte (BASE, GRAM, ALPHA, NU, AB) | `verification/data/P1151s24/entrees/I_data.gp`, SHA-256 `1d2b926698ec42f5…` | `verification/data/P461s91/entrees/I_data.gp`, SHA-256 `31e138c88dac1c9d…` |
| Gram en base LLL (88 lignes de 88 entiers) | `verification/detecteur_copie/gram/P1151s24.gram` ; diagonale de 28 à 68 | `verification/detecteur_copie/gram/P461s91.gram` ; diagonale de 22 à 60 |
| Rang, parité, déterminant | 88, pair, dét 1, défini positif : **démontré** (contrôles exacts G2) | idem |
| Minimum | 8, assisté par calcul et répliqué (§ 2.1) | 8 **annoncé par les auteurs, non répliqué** (§ 2.2) |
| Vecteurs de norme 8 | si le minimum vaut 8, la série thêta extrémale de poids 44 en donne 168 498 000 (signes comptés) ; **non dénombrés**, aucun exemple explicite publié | idem |

**À ne pas confondre** avec les réseaux d'un seul premier de degré 1 : X_{P₁₁₅₁}, avec P₁₁₅₁ = (1151, ζ − 6), et X_{P₄₆₁}, avec P₄₆₁ = (461, ζ − 5), contiennent des vecteurs de norme 6 (note, prop. 6.1 et tableau 2 ; `verification/RESULTATS.md` du dépôt). Ce sont des réseaux différents.

Pour la borne extrémale, un réseau pair unimodulaire de rang 88 a un minimum au plus 2⌊88/24⌋ + 2 = 8. L'absence de vecteur non nul de norme au plus 6 donne donc un minimum égal à 8.

## 2. Statuts détaillés

### 2.1 X(P₁₁₅₁σ₂₄)

- **Raccord exact** (démontré). Les fichiers d'entrée du programme certifiant décrivent exactement X_I. Le vérificateur passe 38 contrôles sur 38 en entiers et rationnels, sans PARI/GP. Par rapport à X₄₉₆₉, seul le contrôle G1 change : g = (y − 6)(y − 605) est scindé modulo 1151, σ₂₄(I) = I, et I + Ī = 𝒪_L. Le contrôle α·ν = β₀ passe aussi, et la Gram réduite est raccordée à GRAM (13 contrôles en PARI/GP).
- **Minimum 8** (assisté par calcul, sous le modèle d'exécution M1, M2, H1–H3 de la note, § 5.4, et le critère du th. 4.6). Les deux côtés du critère sont balayés en entier, avec `Rang88CertZ`, B_A = 1057/200, S = 12, et les huit classes publiées dans `code/certifiant/classes/`, identiques à l'octet :

| Côté | Tâches | Catalogue (SHA-256) | Exécution 1 : poste Windows de l'auteur (SpiraleG), OpenJDK 11.0.16.1, 14 fils | Exécution 2 : Scaleway POP2-HC-32C-64G, Ubuntu, OpenJDK 21.0.12.1, 32 fils | Empreinte canonique des reçus (les deux exécutions) |
|---|---|---|---|---|---|
| 1 | 74 027 | `287b1e724cb845e2…` | 17 oct. 2026, 22 h 48 (CEST), 46 971 s | 19 oct., 09:44 UTC, zone AMS3, 12 368 s | `36c946d4551a6d403cfc8e8ecadabab8efa8b9090c8fe3898cdafcd04d2e32f7` |
| 2 | 101 373 | `fe2b7eb6d4d02181…` | 18 oct., 11 h 51 (CEST), 47 678 s | 19 oct., 09:45 UTC, zone AMS2, 11 846 s | `32818d454ff45e5a835e894cf1f0a1411a1aba516fb6eae14ba328f96d6065da` |

  - Chaque exécution est un lancement unique : point de contrôle neuf, aucune reprise, code Java 0, flux d'erreur vide, couverture complète, **aucune touche** et aucun fichier de touche. `controle_execution.py` passe 27 contrôles sur 27 pour chacune, et 28 sur 28 avec E7 contre les reçus de l'autre exécution, tous identiques.
  - |U| = 358 234 264 sur chacun des deux côtés.
  - Les reçus d'un même côté sont identiques une fois triés par indice ; les fichiers bruts diffèrent seulement par l'ordre d'écriture des fils.
  - Défaut bénin du lanceur de la réplication : sa table `SHA256SUMS_SORTIES.txt` a été écrite avant l'ajout de la dernière ligne (VERDICT) au reçu `RECU_REPLICATION_P1151s24.txt`. Le reçu privé de cette ligne a exactement l'empreinte de la table (journal 13 du § 6). Les fichiers de journaux de la réplication portent « crapaud08 » dans leur nom : c'est un nom fixé par le lanceur, préparé d'abord pour un autre poste ; la machine est bien celle de Scaleway (lignes JVM des journaux).
- **Non-isométrie** (démontrée sans GRH, modulo la note, prop. 2.2, 2.5 et th. 3.3, et l'addendum, prop. 4.7). La classe [I] a pour support {331} : composante 3 nulle (4·1151 = 48² + 23·10²), composante 45 013 nulle (σ₂₄(I) = I), composante 331 d'étiquette c = 67 (heure 6 de l'anneau extérieur). Elle n'est conjuguée à aucune des classes de L₀, L_S, X₁₃₉, X₅₉₉, X₄₉₆₉ et X₄₀₄₉ (85 contrôles sur 85). Le théorème d'isométrie, qui demande le minimum 8 d'au moins un des deux réseaux comparés, donne la non-isométrie. Vis-à-vis de L₀ et L_S, elle ne dépend d'aucun minimum assisté, puisque leur minimum 8 est établi par Sakamoto.
- **Ouvert.** Le jumeau intérieur d'heure 6 (représenté par P₆₂₁₁σ₂₄) n'est pas tranché.

Avec X(P₁₁₅₁σ₂₄), la famille compte au moins **sept** réseaux extrémaux pairs unimodulaires de rang 88, deux à deux non isométriques : L₀ et L_S (Sakamoto), et cinq réseaux à minimum assisté par calcul et répliqué, X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉, X(P₁₁₅₁σ₂₄).

### 2.2 X(P₄₆₁σ₉₁) : CANDIDAT (minimum annoncé, non répliqué ; non-isométrie à L₀ sous GRH seulement)

- **Raccord exact** (démontré). 38 contrôles sur 38 ; G1 : g = (y − 5)(y − 115) scindé modulo 461, σ₉₁(I) = I, I + Ī = 𝒪_L. α·ν = β₀ et raccord à la Gram réduite, comme ci-dessus.
- **Même côté court que P₄₆₁σ₂₄** (constat sur les fichiers). Les fichiers du côté court (`coteN_A.gram`, `coteN_B.gram`, `coteN_meta.txt`) et les catalogues de tâches sont identiques à l'octet à ceux de P₄₆₁σ₂₄(P₄₆₁), balayé en entier dans la version 1.1 (`calcul_externe_resultats_20261015/final_P461s24_AMS3/`) et isométrique à X₁₃₉. Seul le recollement `coteN_T.mat` diffère.
- **Balayage** (non répliqué). Poste Linux de l'auteur (Crapaud08), OpenJDK 21.0.12.1, 8 fils, même invocation et mêmes classes :

| Côté | Tâches | Catalogue | Exécution | Contrôles | Empreinte canonique |
|---|---|---|---|---|---|
| 1 | 73 244 | `0189bac379e039fb…` (celui de P₄₆₁σ₂₄) | 19 oct., 17:09 → 23:43 UTC ; **reprise** : 2 089 tâches héritées d'un lancement antérieur, interrompu deux fois par la réserve mémoire de l'hôte, et 71 155 tâches nouvelles | 28 contrôles, **4 échecs**, tous des contrôles E1 de « première exécution », incompatibles par construction avec une reprise | `db04c32e641f75bcce3739f09921e3aab27917903b4b4e36aedafae518eaa1e4` |
| 2 | 73 359 | `388a5734bb6ce7e5…` (celui de P₄₆₁σ₂₄) | 19 oct., 23:43 → 20 oct., 05:45 UTC ; lancement unique, sans reprise | 28 sur 28 | `652ef2f89497cb0784326c1ab280b86b99febb3206749f3ee4592c4f59936d13` |

  - Les deux côtés sont complets, **sans touche**, codes Java 0, flux d'erreur vides ; |U| = 143 529 602 sur chaque côté, comme pour P₄₆₁σ₂₄.
  - Le verdict brut du lanceur est **A_EXAMINER** (code 4). Il est conservé tel quel. Il vient d'une lacune du lanceur : son verdict « complet après reprise » exigeait plusieurs journaux de lancement, alors que le point de contrôle hérité avait été copié dans un dossier neuf. Ce n'est pas une nouvelle exécution.
  - **Les 2 089 reçus hérités** (`seed_inputs/cote1.ckpt`, SHA-256 `93d8b081…`, celui que Java annonce à la lecture) sont un préfixe exact du fichier final. 1 419 d'entre eux sont identiques à des reçus de référence produits sur un autre poste le 17 octobre (contrôle E7). **Les 670 autres ne sont recoupés par aucune autre exécution**, et les journaux natifs du lancement interrompu ne sont pas publiés.
  - **Recoupement par le jumeau** (constaté, 30 oct.). Pour chacune des 146 603 tâches, la partie courte des reçus (U, CVP, NA, HIST) est identique à celle des reçus publiés de P₄₆₁σ₂₄, calculés sur une autre machine ; les 670 tâches héritées sont comprises. **La partie fibre (NB, recherche des touches), propre à P₄₆₁σ₉₁, n'est pas répliquée.**
  - Par le critère du th. 4.6, ce balayage donnerait le minimum 8. Ce minimum est **annoncé par les auteurs** ; il n'a pas le niveau de X(P₁₁₅₁σ₂₄), faute de réplication.
- **Non-isométrie** (sans GRH, sauf pour L₀). Les composantes 3 et 331 de [I] sont nulles : (91/23) = −1 donne [I]₃ = 0, et l'étiquette 331 vaut c = 0 (123 contrôles sur 123). [I] n'est donc conjuguée ni aux classes de X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉, X(P₁₁₅₁σ₂₄), dont la composante 331 est non nulle, ni à celles de L_S, de support {3}. Avec le th. 3.3 et le minimum 8 de ces réseaux, X(P₄₆₁σ₉₁) n'est isométrique à aucun d'eux ; cela ne dépend pas de son propre balayage, non répliqué.
  - **Vis-à-vis de L₀, la non-isométrie n'est démontrée que sous GRH.** Elle équivaut à [I]₄₅₀₁₃ ≠ 0, vrai sous GRH (calcul par `bnfinit`). Si l'on avait [I] = 0, X(P₄₆₁σ₉₁) serait isométrique à L₀, donc extrémal, mais pas nouveau.

## 3. Méthode : renvois aux pièces du dépôt

- **Critère et programme.** Théorème 4.6 de la note (recollement, deux formes de rang 44 sur 𝒪⁺, Parseval, seuil 1057/200) ; programme `Rang88CertZ` (`code/certifiant/`), sa preuve de non-omission (`preuve/`) et le modèle d'exécution M1, M2, H1–H3 (note, § 5.4). Les classes utilisées ici sont celles du dépôt, identiques à l'octet (SHA-256 imprimés en tête de chaque journal).
- **Contrôle des exécutions.** `balayages/outils/controle_execution.py` (identique à `calcul_externe_resultats_20261015/controle_execution.py`, contrôles E1 à E7) et `empreinte_canonique.py` (identique à `code/verification/empreinte_canonique.py`).
- **Raccord.** `verification/code/verifier_raccord_P1151s24.py` et `verifier_raccord_tranche1.py` sont des copies adaptées de `verification_P4969/code/verification/verifier_raccord.py` ; les originaux sont dans `verification/code/outils_inchanges/`, et leurs empreintes s'impriment à l'exécution.
- **Non-isométrie.** `verifier_non_isometrie_P1151s24.py` et `verifier_non_isometrie_tranche1.py` reprennent `verification_P4969/code/verification/verifier_non_isometrie_P4969_v2.py` (contrôles C1 à C5) et la prop. 4.7 de l'addendum (cadran sans GRH, `addendum/cadran_sans_GRH/`). Toutes les pièces candidates, trouvées par PARI sous GRH, sont recontrôlées exactement.
- **α·ν = β₀.** `verification/code/outils_inchanges/verifier_alpha_beta0_v2.py`.
- **Gram réduite.** `verification/code/raccord_detecteur.gp` et ses pilotes (PARI/GP 2.15.4) ; `detecteur_copie/code/commun_rang88.gp`.

## 4. Contenu

```
README_v14.md
verification/                      racine des vérificateurs (lancer les commandes depuis ce dossier)
  code/                            raccord, non-isométrie, intégrité, raccord à la Gram réduite ; outils_inchanges/ : originaux et copies inchangées
  data/P1151s24/entrees/           11 entrées (I_data.gp, coteN_A.gram, coteN_B.gram, coteN_T.mat, coteN_meta.txt, coteN_bases.gp)
  data/P1151s24/premiere_execution/  journaux stdout de l'exécution 1 (lus par le contrôle G6)
  data/P461s91/entrees/            candidat X(P₄₆₁σ₉₁) (nom inchangé, lu par les vérificateurs) : 11 entrées ; data/P461s91/journaux/ : catalogues du 19 oct. et filtres du 17 oct. (lus par G6)
  data/P139, P599, P4969, P4049, corps, cadran   données de référence, identiques à celles du dépôt
  data/P3359/entrees/I_data.gp     lu par verifier_non_isometrie_tranche1.py, qui traite aussi P₃₃₅₉ (survivant non tranché)
  detecteur_copie/                 Gram en base LLL, matrices de passage U, journaux (dont la recherche heuristique G6K, sans témoin)
  journaux/                        journaux d'origine des vérificateurs (19 oct. 2026)
balayages/
  outils/                          controle_execution.py, empreinte_canonique.py, compare_recus.py
  P1151s24_SpiraleG_20261017/      exécution 1 : run_P1151s24/ (reçus, catalogues, journaux, verdict), autotest, lanceur, empreintes
  P1151s24_replication_Scaleway_20261019/   exécution 2 : cote1_AMS3/sorties/, cote2_AMS2/sorties/, lot/ (lanceur, empreintes, valeurs attendues)
  CANDIDAT_P461s91_non_replique_Crapaud08_V2_20261019/   candidat X(P₄₆₁σ₉₁), exécution unique : sorties/ (reçus, catalogues, journaux, contrôles, verdict, table SHA256SUMS_SORTIES.txt), seed_inputs/ (2 089 reçus hérités), lot/ (lanceur, valeurs attendues, références E7)
controles_preparation_20261030/    verifier_jumeau_P461s91.py et journaux des contrôles rejoués le 30 octobre 2026 (§ 6)
```

**Noms de dossiers.** Le 31 octobre 2026, ce dossier a été renommé de `v14_P1151s24_P461s91/` en `v14_P1151s24_et_candidat_P461s91/`, et le dossier du balayage de P₄₆₁σ₉₁ de `balayages/P461s91_Crapaud08_V2_20261019/` en `balayages/CANDIDAT_P461s91_non_replique_Crapaud08_V2_20261019/`, pour que le statut de candidat se voie dans les chemins ; aucun fichier n'a changé. Les journaux du 30 octobre (§ 6) citent encore les anciens noms. Le dossier `verification/data/P461s91/` et les fichiers `verification/detecteur_copie/gram/P461s91.*` gardent leur nom, parce que les vérificateurs les lisent.

## 5. Rejouer

Depuis la racine du dépôt, avec Python ≥ 3.9 (bibliothèque standard seulement) :

```
python3 -I v14_P1151s24_et_candidat_P461s91/balayages/outils/controle_execution.py v14_P1151s24_et_candidat_P461s91/balayages/P1151s24_replication_Scaleway_20261019/cote1_AMS3/sorties/run_P1151s24_cote1 1 74027 287b1e724cb845e266356bbaed182a6c95d47f207dc7def9acf10c5d78711b8e
python3 -I v14_P1151s24_et_candidat_P461s91/balayages/outils/controle_execution.py v14_P1151s24_et_candidat_P461s91/balayages/CANDIDAT_P461s91_non_replique_Crapaud08_V2_20261019/sorties/run_P461s91_cote2 2 73359 388a5734bb6ce7e5a700c8e08aaa54cae326bf787a451a1251639c5f834e0fd2
python3 -I v14_P1151s24_et_candidat_P461s91/balayages/outils/empreinte_canonique.py <fichier .ckpt> ...
```

Depuis `v14_P1151s24_et_candidat_P461s91/verification/` :

```
python3 -I code/verifier_raccord_P1151s24.py P1151s24          # BILAN : 38 controles, 0 echecs ; FIN_OK
python3 -I code/verifier_non_isometrie_P1151s24.py             # BILAN : 85 controles, 0 echecs
python3 -I code/verifier_raccord_tranche1.py P461s91           # BILAN : 38 controles, 0 echecs ; FIN_OK
python3 -I code/verifier_non_isometrie_tranche1.py             # BILAN : 123 controles, 0 echecs
python3 -I code/outils_inchanges/verifier_alpha_beta0_v2.py data/corps/rang88_m115c0_data.txt data/P461s91/entrees/I_data.gp data/P1151s24/entrees/I_data.gp
gp -q -D parisize=400000000 code/raccord_detecteur_P461s91.gp < /dev/null    # RACCORD_DETECTEUR_OK P461s91 (idem P1151s24)
```

`controle_execution.py` cherche un journal nommé `cote<s>_*.stdout.log`. Pour l'exécution 1 de P₁₁₅₁σ₂₄, dont les journaux s'appellent `cote<s>.stdout.log`, il faut le lancer sur une copie où ces journaux, et les fichiers `.java.exit` et `.stderr.log` correspondants, sont renommés `cote<s>_SpiraleG.*` ; les fichiers publiés restent inchangés. Pour le côté 1 de P₄₆₁σ₉₁, le résultat attendu est « 28 controles, 4 echecs » (les quatre E1 de reprise) et le code de sortie 1.

Les balayages eux-mêmes (de 3 à 13 heures par côté) ne sont pas relancés ; l'invocation figure en tête de chaque lanceur (`lancer_*.sh`) et de chaque journal.

## 6. Contrôles rejoués le 30 octobre 2026

Ils ont été rejoués sur une copie de ce dossier, placée comme dans le dépôt, sous Linux (WSL), Python 3.12.3. Leurs journaux sont dans `controles_preparation_20261030/journaux/`.

| Journal | Contrôle | Résultat |
|---|---|---|
| 01 (×2) | `controle_execution.py`, exécution 1 de P₁₁₅₁σ₂₄ (copie à journaux renommés) | 27/27 par côté ; empreintes `36c946d4…`, `32818d45…` |
| 02 (×2) | idem, exécution 2, avec E7 contre l'exécution 1 | 28/28 par côté ; 74 027 et 101 373 reçus communs, 0 différent |
| 03 (×2) | idem, P₄₆₁σ₉₁, avec E7 contre les filtres du 17 oct. | côté 1 : 28 contrôles, 4 échecs E1 de reprise (attendu) ; côté 2 : 28/28 |
| 04 | empreintes canoniques des six fichiers de reçus et du fichier hérité | conformes au tableau ; aucune touche |
| 05 (×2) | `verifier_jumeau_P461s91.py` : P₄₆₁σ₉₁ contre les reçus publiés de P₄₆₁σ₂₄ | partie courte identique pour 73 244 et 73 359 tâches ; 2 089 hérités = préfixe exact ; 1 419 dans E7, 670 hors E7, à partie courte identique |
| 06–10 | raccords, non-isométries, α·ν = β₀ | 38/38, 85/85, 38/38, 123/123, 6/6 |
| 13 | tables `SHA256SUMS_SORTIES.txt` des exécutions rapatriées | P₄₆₁σ₉₁ : conforme ; réplication de P₁₁₅₁σ₂₄ : seul le reçu diffère, à cause de sa ligne VERDICT ajoutée après la table (vérifié) |

Le raccord à la Gram réduite (PARI/GP) n'a pas été rejoué le 30 octobre ; ses journaux d'origine (13 contrôles sur 13 pour chaque réseau, 19 oct.) sont dans `verification/journaux/tranche1_20261019/`.

## 7. Antériorité

- **R. Sakamoto** (arXiv:2609.15633) a construit les premiers réseaux extrémaux pairs unimodulaires de rang 88, L et L₀. Le réseau H de la note est isométrique à L₀ (note, § 2.5).
- **X₁₃₉, X₅₉₉, X₄₀₄₉, X₄₉₆₉** (versions 1.0 et 1.1 de ce dépôt) figurent dans le catalogue de réseaux de G. Nebe et N. J. A. Sloane (fiches dim88c à dim88f), qui précise « Minimum claimed by the authors ».
- **X(P₁₁₅₁σ₂₄) et le candidat X(P₄₆₁σ₉₁)** : à notre connaissance, au 30 octobre 2026, ni ces réseaux ni ces résultats n'ont de trace publique antérieure à cette version. L'addendum (§ 5) nommait seulement P₁₁₅₁σ₂₄(P₁₁₅₁) comme candidat à balayer.
- Les méthodes sont celles de la note et de l'addendum. Ce dossier ne revendique aucune méthode nouvelle.

## 8. Ce qui n'est pas revendiqué

- **Aucune preuve formelle.** Le minimum 8 de X(P₁₁₅₁σ₂₄) est assisté par calcul, sous M1, M2, H1–H3 ; les réplications étayent ce modèle sans le démontrer. Aucune implantation indépendante de l'énumération n'a été exécutée.
- **X(P₄₆₁σ₉₁) est un candidat, non répliqué.** Son minimum 8 est seulement annoncé ; seule la partie courte de ses reçus est recoupée, par ceux de P₄₆₁σ₂₄. Ni sa non-isométrie à L₀ (sous GRH seulement), ni sa nouveauté ne sont démontrées sans GRH.
- Les étiquettes d'orbite et d'anneau sous GRH (par exemple l'heure 885 de P₄₆₁σ₉₁) ne sont pas revendiquées.
- Aucun vecteur de norme 8 explicite n'est publié pour ces deux réseaux (contrôle G9 non fait) ; le nombre 168 498 000 est une conséquence du minimum 8, pas un dénombrement.
- Aucun groupe d'automorphismes n'est calculé, et aucune fiche au format du catalogue n'est fournie.
- Rien n'est affirmé sur le nombre total de réseaux extrémaux de rang 88, ni sur les jumeaux non tranchés (P₆₂₁₁σ₂₄).
- La recherche G6K des journaux `detecteur_copie/journaux/*.g6k_*.log` est une heuristique, sans valeur de preuve.
- Les vérificateurs adaptés et `verifier_jumeau_P461s91.py` sont dus à l'assistant (Claude) ; ils ne sont pas indépendants les uns des autres, et aucun humain ne les a relus.

## 9. Pièces non incluses

- L'archive complète du retour de P₄₆₁σ₉₁ (7 567 885 octets, SHA-256 `02686656f1fd11d2397a73e7622f9c5bdb37abe753372b6149fc99b7ade068e9`) : elle contient aussi des messages de coordination et des relevés propres à l'hôte. Seuls ses dossiers `sorties/` et le fichier hérité `seed_inputs/cote1.ckpt` sont publiés, octet pour octet ; leurs empreintes concordent avec la liste d'empreintes de l'archive.
- Les journaux natifs du lancement interrompu du côté 1 de P₄₆₁σ₉₁ (ils ne figurent pas dans l'archive).
- Les journaux de location, de surveillance et d'extinction des machines Scaleway, et la description du lot de réplication (`README_LOT.md`), qui contient des éléments internes.
- Le catalogue de l'autotest de l'exécution 1 (`P1151s24_cote1.taches`, `P1151s24_cote2.taches`), identique à l'octet aux catalogues de `run_P1151s24/` (SHA-256 `287b1e72…`, `fe2b7eb6…`), et le catalogue copié avec le fichier hérité de P₄₆₁σ₉₁, identique à celui du côté 1 (`0189bac3…`).

**Chemins et noms internes.** Le lanceur `lancer_P1151s24.sh` contient le chemin de Java sur le poste de l'auteur. Deux journaux de filtre (`verification/data/P461s91/journaux/filtre_s91_*.log`) et un journal du 19 oct. citent des dossiers de travail internes. Ces fichiers sont publiés à l'identique.

## Attribution

Auteur : Ivan Gauvin. Claude Opus 5.5 (Anthropic) et Astra (OpenAI) ont assisté l'auteur ; ils ne sont pas auteurs. Licences du dépôt : MIT pour les programmes, CC BY 4.0 pour les données et la documentation.

---

# Version 1.4: timestamping X(P₁₁₅₁σ₂₄), extremal, and the CANDIDATE X(P₄₆₁σ₉₁)

> **X(P₄₆₁σ₉₁) is published as a CANDIDATE.** Its minimum 8 is only **claimed by the authors**: the sweep has **not been replicated**, and only the short part of its receipts is cross-checked, against those of P₄₆₁σ₂₄ (the fibre part is not). Its non-isometry to L₀ is proved **only under GRH**. Only X(P₁₁₅₁σ₂₄) has a computer-assisted and replicated minimum.

This folder publicly timestamps two even unimodular ideal lattices of rank 88 over L = ℚ(ζ₁₁₅), built as in the note and its addendum: X(P₁₁₅₁σ₂₄), extremal (computer-assisted and replicated minimum), and X(P₄₆₁σ₉₁), a **candidate** (claimed minimum, not replicated). It contains exact constructions, inputs, receipts and logs of their sweeps, checkers and their logs. **The note and the addendum are unchanged.** No human specialist has reviewed anything in this folder.

| Lattice | Minimum 8 | Replication | Non-isometry to known lattices |
|---|---|---|---|
| **X(P₁₁₅₁σ₂₄)** | **computer-assisted** (M1, M2, H1–H3), exhaustive sweep of both sides of the criterion, no touch | **yes**: two runs on two different machines, identical receipts (equal canonical fingerprints) | proved without GRH, to the six known extremal lattices (L₀, L_S, X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉) |
| **X(P₄₆₁σ₉₁): CANDIDATE** | **claimed by the authors, NOT replicated**: exhaustive sweep of both sides, no touch, on a single machine | **no**; only the short part of the receipts is cross-checked (against the receipts of P₄₆₁σ₂₄), not the fibre part | proved without GRH to X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉, X(P₁₁₅₁σ₂₄) and L_S; **to L₀ only under GRH** |

**Lattices.** X_I = (I, β₀/ν) as in the note, with I + Ī = 𝒪_L and ν generating IĪ. Both ideals are products of **two primes of residue degree 1** swapped by a Galois automorphism: I = (1151, ζ − 6)(1151, ζ − 605) = P·σ₂₄(P), of norm 1151², and I = (461, ζ − 5)(461, ζ − 115) = P·σ₉₁(P), of norm 461². Exact data (basis, Gram matrix, α, ν) are in `verification/data/<name>/entrees/I_data.gp`; Gram matrices in an LLL basis are in `verification/detecteur_copie/gram/`. Rank 88, even, determinant 1, positive definite: proved by exact checks. If the minimum is 8, the extremal theta series gives 168 498 000 vectors of norm 8; they were not counted, and no explicit norm-8 vector is published. Not to be confused with the lattices of the single primes (1151, ζ − 6) and (461, ζ − 5), which contain norm-6 vectors (note, Prop. 6.1 and Table 2).

**X(P₁₁₅₁σ₂₄).** Exact link of the input files to the lattice: 38/38 checks. Both sides swept with `Rang88CertZ` (B_A = 1057/200, S = 12, the published classes): 74 027 and 101 373 tasks, no touch, |U| = 358 234 264 per side. Run 1 on the author's Windows computer (OpenJDK 11, 17–19 October 2026); run 2 on rented Scaleway POP2-HC-32C-64G machines (Linux, OpenJDK 21, 19 October 2026, zones AMS3 and AMS2). Each run is a single launch without resume; `controle_execution.py` gives 27/27 for each run and side; canonical fingerprints `36c946d4…` (side 1) and `32818d45…` (side 2) are equal for both runs. The class [I] has support {331} (label c = 67, hour 6 of the outer ring), so it is not Galois conjugate to the classes of the six known extremal lattices (85/85, without GRH); the isometry theorem then gives non-isometry. The family thus contains at least **seven** pairwise non-isometric extremal lattices of rank 88 (L₀, L_S by Sakamoto; five computer-assisted and replicated). The inner twin of hour 6 is open.

**X(P₄₆₁σ₉₁): candidate.** Exact link: 38/38. Its short-side input files and task catalogues are byte-identical to those of P₄₆₁σ₂₄(P₄₆₁), swept in version 1.1 and isometric to X₁₃₉; only the gluing file differs. Both sides were swept on the author's Linux computer (OpenJDK 21, 8 threads, 19–20 October 2026): 73 244 and 73 359 tasks, no touch, |U| = 143 529 602 per side, canonical fingerprints `db04c32e…` and `652ef2f8…`. Side 2 is a single launch (28/28). Side 1 resumed from 2 089 receipts of an earlier launch interrupted by the host's memory reserve: its four failed checks are exactly the "first run" E1 checks, which a resume fails by design, and the launcher's raw verdict, A_EXAMINER, is kept as is. 1 419 inherited receipts match reference receipts computed elsewhere on 17 October; **670 are not cross-checked by any other run**, and the native logs of the interrupted launch are not published. On 30 October, the short part of every receipt (U, CVP, NA, HIST; 146 603 tasks, the 670 included) was found identical to that of the published receipts of P₄₆₁σ₂₄, computed on another machine; **the fibre part (NB, search for touches), specific to P₄₆₁σ₉₁, is not replicated**. The minimum 8 is therefore **claimed by the authors**. The 3- and 331-components of [I] vanish (123/123, without GRH), which gives non-isometry to X₁₃₉, X₅₉₉, X₄₉₆₉, X₄₀₄₉, X(P₁₁₅₁σ₂₄) and L_S. **Non-isometry to L₀ holds only under GRH**: it is equivalent to [I]₄₅₀₁₃ ≠ 0; if [I] were 0, the lattice would be isometric to L₀.

**Method.** Theorem 4.6 of the note, the certifying program `Rang88CertZ` and its non-omission proof (`code/certifiant/`, `preuve/`), the execution model M1, M2, H1–H3 (note, § 5.4), `controle_execution.py` (E1–E7), and checkers adapted from `verification_P4969/` and from the dial without GRH of the addendum (Prop. 4.7). Commands are in § 5 above; the checks replayed on 30 October 2026 are listed in § 6 and logged in `controles_preparation_20261030/journaux/`.

**Prior work.** R. Sakamoto (arXiv:2609.15633) built the first extremal even unimodular lattices of rank 88, L and L₀; the lattice H of the note is isometric to L₀. X₁₃₉, X₅₉₉, X₄₀₄₉ and X₄₉₆₉ are in the Nebe–Sloane catalogue of lattices (entries dim88c–dim88f, "Minimum claimed by the authors"). To our knowledge, as of 30 October 2026, X(P₁₁₅₁σ₂₄) and X(P₄₆₁σ₉₁) have no earlier public record; the addendum only named P₁₁₅₁σ₂₄(P₁₁₅₁) as a candidate. No new method is claimed.

**Not claimed.** No formal proof; no independent implementation of the enumeration; no replication of X(P₄₆₁σ₉₁); no proof without GRH of its non-isometry to L₀ or of its novelty; no GRH-dependent orbit labels; no explicit norm-8 vector, automorphism group or catalogue entry; nothing on the total number of extremal lattices of rank 88 or on unresolved twins. The G6K logs are heuristics. The adapted checkers and `verifier_jumeau_P461s91.py` were written by the assistant (Claude); they are not independent of each other, and no human has reviewed them.

**Not included.** The full return archive of the P₄₆₁σ₉₁ run (SHA-256 `02686656…`), which also holds coordination messages and host records: only its `sorties/` folder and the inherited receipts are published, byte for byte. The native logs of the interrupted launch; the rental logs of the Scaleway machines; duplicate catalogues (identical SHA-256 given above). A few published files contain local paths or internal folder names; they are published unchanged.

**Folder names.** On 31 October 2026 this folder was renamed from `v14_P1151s24_P461s91/` to `v14_P1151s24_et_candidat_P461s91/`, and the P₄₆₁σ₉₁ sweep folder from `balayages/P461s91_Crapaud08_V2_20261019/` to `balayages/CANDIDAT_P461s91_non_replique_Crapaud08_V2_20261019/`, so that the candidate status shows in the paths; no file changed, and the logs of 30 October still cite the old names. `verification/data/P461s91/` and `verification/detecteur_copie/gram/P461s91.*` keep their names because the checkers read them.

Author: Ivan Gauvin. Claude Opus 5.5 (Anthropic) and Astra (OpenAI) assisted the author; they are not authors. Licences: MIT for the programs, CC BY 4.0 for data and documentation.
