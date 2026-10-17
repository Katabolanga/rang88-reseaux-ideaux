# Contre-audit, expérience C3 : prédiction par GP, détection par Rang88CertZ

*Claude, 16 octobre 2026, de 10 h à 10 h 40. Dossier `contre_audit_20261016/C3/`. Ce bilan complète `C1_C4_BILAN.md` et `C2_MUTATIONS_BILAN.md`.*

## Principe

On veut savoir si le programme trouve **toutes** les touches qu'il doit trouver, et pas seulement « une touche ».

On part d'un réseau **rejeté** et du témoin de norme 6 publié dans le dépôt (`data/rejets/temoin_*.gp`). Ce vecteur z ∈ ℤ[ζ] a été trouvé par PARI, indépendamment du programme Java.

**Prédiction exacte, en GP** (`C3_prediction.gp`). On calcule les 115 rotations ζᵏz, et pour chacune :
- son image (b ; a) = AB·x_k ;
- ses coordonnées (u, y) des deux côtés, avec les bases `cote*_bases.gp` ;
- ses énergies Λ(a_k) et Λ′(b_k).

Une rotation donne une touche prédite si sa projection courte est non nulle et d'énergie ≤ B_A. On normalise le signe comme le programme. **Le script ne lit aucune donnée produite par le programme Java.**

**Détection** (`C3_detecter.sh`) :
1. Le catalogue des tâches est régénéré par les classes testées.
2. Chaque u prédit doit se trouver dans **exactement une** tâche. Le catalogue doit être une partition ; sinon, il serait incomplet ou se chevaucherait.
3. On ne rejoue que ces tâches, sans arrêt sur touche.
4. Chaque touche prédite doit être obtenue **à l'identique**, avec les mêmes u, y et numérateurs d'énergie.
5. Les touches obtenues en plus doivent être des vecteurs **exacts** de norme 6, hors de l'orbite du témoin (`C3_verifier_en_plus.gp`).

**Contrôles exacts faits au passage**, en rationnels, sur les 3 × 115 rotations :
- lemme A : Λ(a_k) = 6 + f(k) et Λ′(b_k) = 6 − f(k), où f(k) = Tr_{L/ℚ}(α ζ^{2k} z²) est calculé **directement dans L** ;
- somme nulle des f(k) et les 23 relations à cinq termes (R5) ;
- inégalité de Parseval et max|f| ≥ N√(5/352) ;
- les énergies recalculées à partir des fichiers d'entrée eux-mêmes : uᵀAu = D_A·Λ et wᵀBw = D_B·d²·Λ′.

## C3a : aux paramètres publiés (B_A = 1057/200, S = 12)

Programme : classes publiées, `calcul_externe_P4969/classes`.

| Réseau rejeté | Côté | Touches prédites | Énergies courtes prédites | Retrouvées à l'identique | En plus, vérifiées |
|---|---|---|---|---|---|
| P₆₉₁ (r = 4) | 1 | 20 | 3,4009 à 5,2287 | 20 | 0 |
| P₆₉₁ | 2 | 22 | 3,8683 à 5,2721 | 22 | 2 |
| P₁₁₅₁ (r = 6) | 1 | 26 | 3,3206 à **5,284970** | 26 | 0 |
| P₁₁₅₁ | 2 | 28 | 3,8897 à 5,2615 | 28 | 3 |
| P₁₃₈₁ (r = 21) | 1 | 22 | 2,9529 à 5,2317 | 22 | 3 |
| P₁₃₈₁ | 2 | 23 | 3,9413 à 5,2419 | 23 | 3 |
| **Total** | | **141** | | **141** | **11** |

- **Aucune touche manquante.** Chaque touche prédite se trouve dans exactement une tâche du catalogue.
- Les 11 touches en plus sont des vecteurs exacts de norme 6, d'autres orbites que celle du témoin.
- Le catalogue régénéré pour P₆₉₁ côté 1 est identique (SHA 4b6bff6a…) à celui de l'expérience C1.
- **Cas limite de P₁₁₅₁ côté 1.** Une touche prédite a l'énergie courte 6083/1151 ≈ 5,284970. C'est la plus grande valeur admissible, puisque 1057/200 × 1151 = 6083,035 : elle est à 3·10⁻⁵ du seuil, et le programme la trouve.
  - Cette énergie dépasse le seuil de Parseval 6 − √(45/88) ≈ 5,284902.
  - Le lemme garantit seulement qu'**une** rotation passe sous ce seuil. D'autres rotations peuvent se trouver entre 5,2849 et 5,285, et le programme doit les trouver aussi : c'est le cas.

## C3c : idéaux rejetés de degré 2 (ajout du 16 oct., 11 h 15)

Ce volet porte sur la même structure que X₁₃₉, X₅₉₉, X₄₉₆₉ et X₄₀₄₉ : P = (p, g(ζ)) avec deg g = 2, D_A = p et d = 2p. Entrées : `agents/rang88_ideaux/java_P<p>/`. Programme : classes publiées. Batterie lancée de 10 h 29 à 11 h 12.

| Idéal rejeté (degré 2) | Côté 1 : prédites → retrouvées (énergie max) | Côté 2 : prédites → retrouvées (énergie max) | En plus, vérifiées |
|---|---|---|---|
| P₈₂₉ | 23 → 23 (5,2774) | 23 → 23 (**5,2823**) | 3 |
| P₁₂₈₉ | 30 → 30 (5,2529) | 28 → 28 (5,2599) | 2 + 2 |
| P₁₄₇₁ | 24 → 24 (5,2712) | 23 → 23 (5,1312) | 1 + 3 |
| P₁₉₇₉ | 21 → 21 (5,1961) | 21 → 21 (5,2617) | 0 |
| **Total** | | | **193 → 193, 11 en plus** |

- Chaque touche prédite se trouve dans exactement une tâche, et elle est obtenue à l'identique.
- **Réserve d'indépendance.** Les témoins de P₈₂₉, P₁₂₈₉ et P₁₉₇₉ viennent d'une touche de Rang88CertZ du 11 octobre (en-têtes des fichiers témoins). Celui de P₁₄₇₁ vient d'une recherche par un programme Java (note, tableau 2 : « Java »). Le vecteur **de départ** n'est donc pas indépendant du programme Java.
- Restent indépendantes du programme :
  - la prédiction des 114 autres rotations ;
  - la prédiction de tout le côté 2 ;
  - la vérification exacte des 11 touches en plus.

**Total de C3a et C3c : 334 touches prédites sur 7 réseaux rejetés, 14 côtés. Toutes sont retrouvées à l'identique, plus 22 touches d'autres orbites, toutes de norme 6 exacte.**

## C3b : à frontière exacte, avec les mutants de C2

Le seuil court B_A est pris **égal** à l'énergie de la plus haute touche prédite d'un côté. Cette touche est alors exactement sur la frontière courte. Toutes les touches sont aussi exactement sur la frontière de la fibre, puisque l'énergie totale vaut 12.

Le programme de référence et chacun des mutants M0 à M8 régénèrent **leur propre** catalogue, puis rejouent les tâches concernées.

Résultats détaillés : `C3/C3_FRONTIERE_RESULTATS.txt`. La batterie a tourné de 10 h 11 à 10 h 26.

| Classes | P₆₉₁ côté 2, B_A = 3643/691 (22 touches) | P₁₁₅₁ côté 1, B_A = 6083/1151 (26 touches) | Verdict |
|---|---|---|---|
| référence (classes publiées) | 22/22, + 2 autres orbites | 26/26 | toutes trouvées, y compris la touche sur la frontière |
| M0 (source recompilé) | 22/22, + 2 | 26/26 | idem |
| M1 (égalité exclue à la feuille) | 0/22 | 0/26 | **tué** |
| M2 (élagage si budget = 0) | 22/22 | 26/26 | survit (équivalent, voir C2) |
| M3 (pas d'arrondi extérieur sur le budget) | 22/22 | 26/26 | survit |
| M4 (plage entière réduite de 2⁻⁴⁰) | 22/22 | 26/26 | survit |
| M5 (pas d'arrondi extérieur sur le rayon) | 22/22 | 26/26 | survit |
| M6 (budget de fibre diminué d'un cran) | 0/22 | 0/26 | **tué** |
| M7 (vecteur nul non exclu au dernier niveau) | 22/22 | 26/26 | survit (équivalent : ligne 248) |
| M8 (autre convention de signe) | catalogue sans les u prédits | idem | **détecté** : il garde −u au lieu de u |

**Lecture.**
- Même à frontière exacte, des deux côtés à la fois, M3, M4 et M5 ne perdent aucune touche.
- Chacun ne retire qu'**une** des couches d'arrondi extérieur. Les autres suffisent encore :
  - les minorants `dn()` de PL ;
  - la marge W des troncatures ;
  - le plafond de rs ;
  - le majorant `encadre()` du budget.
- Sur **ces seuls cas**, retirer une couche ne fait perdre aucune touche.
- *Correction du 16 oct., 10 h 45, après la remarque d'Astra* : une version précédente généralisait ce constat à « une erreur d'un ulp dans une étape de la preuve ». C'était abusif. La survie d'un mutant n'est **ni** une réfutation du programme, **ni** un certificat de robustesse.
- Aucun test fini ne valide ces marges. **Leur justification générale reste la preuve Z3–Z5 (avec L3), et elle seule.**

## Ce que C3 établit, et ce qu'il n'établit pas

- **Établi, sur 3 réseaux rejetés et 6 côtés :**
  - les fichiers d'entrée décrivent bien le réseau défini par l'algèbre (raccord) ;
  - le catalogue contient chaque touche prédite, une seule fois ;
  - le programme trouve chaque touche prédite, à l'identique, y compris à 3·10⁻⁵ du seuil et à frontière exacte.
- **Non établi :** l'absence d'omission dans **toutes** les branches. C3 est un test fini, qui porte sur environ 150 vecteurs ; la non-omission générale reste l'objet de la preuve (Z1 à Z10). Les mutants M3, M4 et M5 retirent des marges d'un ulp ou de 2⁻⁴⁰. Aucun test ne les détecte, même à frontière exacte (C3b) : seule la preuve couvre ces marges.
- **Constat annexe, vérifié le 16 oct. à 10 h 17 :** les sept classes publiées (`code/certifiant/classes/` du dépôt, et paquets de calcul externe) sont **identiques à l'octet** à la recompilation du source publié (SHA 9e467c75…) par javac 11.0.16.1. Le lien entre le source relu et le binaire exécuté est donc établi par une compilation reproductible, et non seulement par les empreintes imprimées dans les journaux.
