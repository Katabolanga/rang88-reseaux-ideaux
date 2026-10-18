# Addendum (17 octobre 2026) : textes et certificats

*Addendum à « Réseaux idéaux pairs unimodulaires de rang 88 sur Q(ζ₁₁₅) » (I. Gauvin, 15 octobre 2026). Il a la même numérotation que la note : la version anglaise vient d'abord, l'original français ensuite.*

## Textes

- `addendum_en.pdf` (14 p.) et `addendum_fr.pdf` (15 p.) : PDF compilés par pdflatex, en trois passes.
- `addendum_en.tex`, `addendum_fr.tex` : les sources.
- `figure_cadran.tex` : la figure du cadran (TikZ).
- `tableau_filtres_en.tex`, `tableau_filtres_fr.tex`, `comptes_filtres.tex`, `couts_recensement.tex` : tableaux et macros. Ils sont générés à partir des bilans des filtres ; depuis la version 1.2, `temoins_norme6/filtres_nuit_20261017/verifier_bilan_filtres.py` recalcule les trois premiers à partir des pièces publiées.

## Vérifications à relancer

| Énoncé | Dossier | Commande | Résultat attendu |
|---|---|---|---|
| Le cadran sans GRH (prop. 4.7, cor. 4.8, th. C) | `cadran_sans_GRH/` | `gp -q cadran_sans_GRH.gp < /dev/null` | `CADRAN_SANS_GRH_OK` : 97 contrôles, 40 idéaux |
| Idem, sans PARI | `cadran_sans_GRH/` | `python3 -I verifier_cadran.py` | `CADRAN_VERIFIE_SANS_PARI` : 186 contrôles ; manifeste figé des 40 idéaux |
| Certificats de jumelage (prop. 4.5 (a), (b)) | `certificats_jumeaux/` | `gp -q jumeaux_K22.gp < /dev/null` | deux certificats « verification sans GRH : OK », code de sortie 0 |
| Certificats de même orbite (prop. 4.5 (c), (d)) | `certificats_jumeaux/` | `gp -q meme_orbite_K22.gp < /dev/null` | `BILAN : 4 certificats sur 4`, code de sortie 0 |
| Témoins de norme 6 : les quatre rejets du tableau 4 (§ 4.5) et le jumeau de X₄₉₆₉ (prop. 4.6) (version 1.2) | `temoins_norme6/` | depuis la racine du dépôt : `gp -q -D parisize=400000000 addendum/temoins_norme6/verifier_temoins_norme6.gp < /dev/null` | `TEMOINS_NORME6_ADDENDUM_OK` : 69 contrôles, 5 témoins valides sur 5, code de sortie 0 |
| Idem, sans PARI (version 1.2) | `temoins_norme6/` | depuis la racine : `python3 -I addendum/temoins_norme6/verifier_temoins_norme6.py` | `TEMOINS_NORME6_VERIFIES_SANS_PARI` : 75 contrôles, code de sortie 0 |
| Bilan des 21 filtres ; tableau 4 et comptes recalculés (version 1.2) | `temoins_norme6/filtres_nuit_20261017/` | depuis la racine : `python3 -I addendum/temoins_norme6/filtres_nuit_20261017/verifier_bilan_filtres.py` | `BILAN_FILTRES_CONFORME` : 6 contrôles, code de sortie 0 |

### Le cadran

- Le script GP utilise `bnfinit`, qui dépend de GRH, **seulement pour trouver** les générateurs Γ_𝔮 de 𝔮³³¹.
- Tout ce qui est affirmé est ensuite revérifié sans groupe de classes :
  - l'ordre maximal, par `nfcertify` ;
  - les égalités exactes d'idéaux ;
  - les unités, les rangs modulo 331 et la résolution du système linéaire.
- Le vérificateur Python relit `cadran_sans_GRH_certificats.txt` et refait tout en entiers et en rationnels, sans PARI.
- **Chemin à adapter.** `cadran_sans_GRH.gp`, ligne 32, et `cadran_sans_GRH_v1.gp`, ligne 29, affectent à `CERT` un chemin absolu du poste de l'auteur. Ces scripts sont publiés à l'identique des versions exécutées. Avant de les relancer, remplacer ce chemin par `"cadran_sans_GRH_certificats.txt"`.

### Les versions antérieures

Les fichiers `*_v1*`, `*_avant_*` et `*essai1_echoue*` sont les versions antérieures aux corrections de la relecture. Ils sont conservés pour la traçabilité. Les versions qui font foi sont celles qui ne portent aucun de ces suffixes.

## Les autres pièces de l'addendum, dans ce dépôt

| Contenu | Dossier |
|---|---|
| raccord exact et non-isométrie de X₄₉₆₉ et X₄₀₄₉ | `verification_P4969/` et `verification_P4049/` |
| balayages certifiés de X₄₉₆₉ et X₄₀₄₉, et leurs réplications | `calcul_externe_resultats_20261015/` |
| contre-audit du 16 octobre | `contre_audit_20261016/` |
| fiches au format du catalogue de Nebe et Sloane | `catalogue/` |
| témoins de norme 6 du tableau 4 et de la prop. 4.6, bilan et journaux des 21 filtres (version 1.2) | `addendum/temoins_norme6/` |

Chaque dossier a son `LISEZMOI.md` ou son `README.txt`.

## Les témoins de norme 6 (version 1.2)

Le dossier `temoins_norme6/` contient les pièces annoncées dans la version 1.1, et une pièce qui n'y était pas annoncée :
- les témoins de norme 6 des quatre rejets des filtres du § 4.5 (tableau 4) ;
- le témoin de norme 6 de la proposition 4.6 : le réseau de P₆₉₁σ₂₄(P₆₉₁), jumeau de X₄₉₆₉, n'est pas extrémal ; le théorème B en dépend ;
- deux vérificateurs autonomes de ces cinq témoins, en PARI/GP et en Python sans PARI ;
- le bilan des 21 filtres, l'audit des rejets du 17 octobre, les journaux et reçus des filtres, et un script qui recalcule le tableau 4.

Restent à venir, dans une version ultérieure : les exécutions lourdes du contre-audit (voir `contre_audit_20261016/LISEZMOI.md`).

## Statuts

Les statuts sont ceux de la note : [démontré], [sous GRH], [assisté par calcul], [constaté], [ouvert], plus [heuristique].

Le minimum 8 de X₄₉₆₉ et X₄₀₄₉ est assisté par calcul, dans le modèle d'exécution du § 5.4 de la note (M1, M2, H1–H3).

---

**English summary.** This folder contains the addendum (English, then French) and the scripts that recheck its new statements without GRH:
- the dial of the σ₂₄-layer, by PARI/GP (97 checks) and by an independent Python verifier (186 checks);
- the twin and same-orbit certificates.

The certified sweeps of X₄₉₆₉ and X₄₀₄₉ and their replications are in `calcul_externe_resultats_20261015/`; the exact link and non-isometry checks are in `verification_P4969/` and `verification_P4049/`; the catalogue files are in `catalogue/`. Since version 1.2, `temoins_norme6/` contains the norm-6 witnesses of the four filter rejections of § 4.5 and of Proposition 4.6 (the twin of X₄₉₆₉), with a PARI/GP checker and a PARI-free Python checker, and the summary and logs of the 21 filters.
