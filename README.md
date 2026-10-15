# rang88-reseaux-ideaux

Données, programmes et vérifications qui accompagnent la note **« Réseaux idéaux pairs unimodulaires de rang 88 sur Q(ζ₁₁₅) »** d'Ivan Gauvin (15 octobre 2026), dont le texte source et le PDF sont dans `article/`. *English summary below.*

Le dépôt est autoportant : avec PARI/GP 2.15, Python ≥ 3.9 (bibliothèque standard seulement) et, pour les essais facultatifs, Java 11 ou plus, on peut rejouer toutes les vérifications exactes de la note, sauf les deux qui lisent la matrice de Gram de L₀ publiée par R. Sakamoto : ce fichier n'est pas redistribué et doit être téléchargé à part (`externe/LISEZMOI.md`). Les balayages certifiants eux-mêmes (plusieurs heures par côté) ne sont pas relancés par les vérificateurs : leurs reçus, journaux et catalogues sont fournis et contrôlés exactement ; la commande pour les refaire est dans `REPRODUIRE.md`.

## Ce que dit la note, et comment le vérifier

Statuts de la note (§ 1.3) : **démontré** (preuve complète, ou identité exacte rejouable) ; **sous GRH** (dépend de `bnfinit`) ; **assisté par calcul** (démontré sous des hypothèses nommées sur une exécution : M1, M2, H1–H3) ; **constaté** (sortie de programme sans valeur de preuve) ; **ouvert**. Les commandes se lancent depuis la racine du dépôt ; `py` désigne `python -I`, `gp` désigne `gp -q -D parisize=400000000 … < /dev/null`. Les sorties réelles sont dans `verification/RESULTATS.md`.

| Énoncé de la note | Statut (note) | Fichiers | Commande | Résultat rejoué |
|---|---|---|---|---|
| Notations : β₀ ≫ 0, β₀𝔇 = O⁺ ; H = (O_L, β₀) pair, unimodulaire | démontré | `data/corps/` | `py code/verification/verifier_corps.py` | 5 contrôles, 0 échec |
| Prop. 2.2 : h⁻(115) = 44 697 909 = 3·331·45 013 (formule analytique, arithmétique exacte) ; h⁻(87), h⁻(65), h⁻(85) | démontré (h⁺ = 1 : Miller) | — | `gp code/verification/hmoins115.gp` ; second calcul indépendant : `py code/verification/verifier_hmoins_caracteres.py` | 44 697 909 par les deux programmes ; 1 536, 64, 6 205 |
| Prop. 2.5, tableau 1 : caractères χ₃, χ₃₃₁, χ₄₅₀₁₃, noyaux, 508 463 orbites | démontré | — | `gp code/verification/caracteres115.gp` ; `py code/verification/verifier_hmoins_caracteres.py` | 508 463 orbites (et par Burnside) ; noyaux {1,22,24,68}, {1,91} |
| § 2.5 : H ≅ L₀ (P G Pᵀ = G_H, det P = −1) et Q G_art Qᵀ = G | démontré, sans GRH ; Sakamoto a la priorité | `data/L0/`, `externe/integer_input.txt` (à télécharger) | `py code/verification/verifier_H_L0.py` ; `py code/verification/verifier_conformite_article.py` | VALIDE ; VALIDE (avec le fichier de Sakamoto de SHA-256 `68af477c…631f`) |
| Th. 3.3 (isométrie), prop. 4.1, lemmes 4.2–4.5, th. 4.6 (critère) | démontré | preuves dans la note ; contrôles exacts du recollement et du seuil dans `verifier_raccord.py` (G5, G7, G8) | — | — |
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

## Attribution

Auteur : **Ivan Gauvin**, seul responsable scientifique. Claude Opus 5.5 (Anthropic) et Astra (OpenAI) ont assisté l'auteur ; ils ne sont pas auteurs. Leur usage est déclaré à la fin de la note. La matrice de Gram de L₀ et les réseaux L₀ et L_S sont dus à R. Sakamoto (arXiv:2609.15633, v2).

**Licences** : les programmes de `code/` sont sous licence MIT (`LICENSE`) ; la note, les données, les preuves, les résultats de vérification et la documentation sont sous licence CC BY 4.0 (`LICENSE-CC-BY-4.0.md`). Les données de R. Sakamoto ne sont pas redistribuées. **Adresse publique du dépôt :** https://github.com/Katabolanga/rang88-reseaux-ideaux.

---

# English summary

Data, programs and checks accompanying the note *“Even unimodular ideal lattices of rank 88 over Q(ζ₁₁₅)”* by Ivan Gauvin (October 15, 2026; source and PDF in `article/`, compiled with pdfLaTeX, three passes).

The repository is self-contained, except for R. Sakamoto's Gram matrix of L₀, which is **not redistributed**: download `data/L0/integer_input.txt` from his repository at revision `628ce2a7` (SHA-256 `68af477c…631f`) and put it in `externe/` (see `externe/LISEZMOI.md`); the scripts check its digest before reading it as plain integers.

What can be checked (commands from the repository root; real outputs in `verification/RESULTATS.md`): h⁻(115) = 44 697 909 and the 508 463 Galois orbits (two independent exact computations, PARI/GP and Python); the integer isometry certificate H ≅ L₀; the eight norm-6 witnesses (two independent checkers); the exact link between the certifying program's input files and the lattices X₁₃₉, X₅₉₉, with a norm-8 vector; the receipts, logs and task catalogues of the certifying enumeration `Rang88CertZ`, run twice on two computers (Windows/OpenJDK 11 and Linux/OpenJDK 21) with byte-identical sorted receipts, the reference runs being fresh runs without resume and without any touch file; the class certificates in K₂₂ (without GRH); the GRH-dependent orbit labels; and the regeneration of all input files, byte for byte. The non-omission proof of the program is in `preuve/`, linked line by line to the source.

Status: the minimum 8 of X₁₃₉ and X₅₉₉ is a **computer-assisted proof** under the explicit execution model M1, M2, H1–H3 of the note; non-isometry is proved without GRH. No independent implementation of the enumeration has been run, and no human specialist has reviewed the proofs.

Author: Ivan Gauvin. Claude Opus 5.5 (Anthropic) and Astra (OpenAI) assisted the author; they are not authors. **Licences:** MIT for the programs in `code/` (`LICENSE`); CC BY 4.0 for the article, data, proofs, verification results and documentation (`LICENSE-CC-BY-4.0.md`); public address of the repository: https://github.com/Katabolanga/rang88-reseaux-ideaux.
