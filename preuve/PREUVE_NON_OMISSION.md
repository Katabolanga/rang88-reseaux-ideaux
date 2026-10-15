# Rang88CertZ : preuve de non-omission

Ce document est la preuve complète annoncée au § 5.2 de la note (théorème 5.1 et corollaire 5.2). Il porte sur le source `code/certifiant/Rang88CertZ.java`, SHA-256 `9e467c750470301ec0612c087b84636da6b46538a0fe33458970af6cb97bc3c5`, et sur les classes compilées de `code/certifiant/classes/` (empreintes au § 9). La liaison ligne à ligne avec le source est dans `LIAISON_PREUVE_CODE.md`.

**Statut.** Preuve rédigée par l'auteur du code, relue une fois dans une portée limitée : le mécanisme Z1–Z8 sous M1 et M2, et les refus de domaine. Cette relecture a formulé les quatre réserves rappelées au § 8. Elle ne vaut pas certification d'un résultat final. Aucun spécialiste humain n'a relu cette preuve (note, § 5.3 et § 7.2).

**Origine.** `Rang88CertZ` reprend d'un premier programme certifiant, à intervalles de flottants (non inclus dans ce dépôt) : la factorisation rationnelle (L1), l'encadrement exact d'un rationnel (L2), les voisins flottants extérieurs (L3), la récursion, la normalisation de signe, la structure du cache et les feuilles exactes. **Seul changement scientifique** : les sommes partielles des centres sont des **entiers exacts** (virgule fixe 2⁻ᶠ, type `long` à débordement détecté), au lieu d'intervalles de flottants. Les lemmes Z1 à Z5 traitent ce point. S'y ajoutent le découpage adaptatif des tâches (Z7) et le fichier de reprise (Z10). Ce premier programme, plus lent, a certifié six tâches isolées de P₁₃₉ sans touche ; il n'a pas été mené à son terme.

---

## 1. Énoncé certifié

**Données** (fichiers `prefixe_A.gram`, `_B.gram`, `_T.mat`, `_meta.txt`) : matrices entières A, B symétriques n × n, matrice entière Tn, entiers DA, DB, d > 0 ; paramètres : rationnel BA = BAnum/BAden ≥ 0, entier S ≥ 0.

Pour u, y ∈ ℤⁿ, on pose a(u) = uᵀAu, w = d·y + Tn·u, e = wᵀBw. On dit que u est **normalisé** si u ≠ 0 et si sa dernière coordonnée non nulle (celle d'indice le plus grand) est > 0.

- 𝒰 = { u normalisé : a(u)·BAden ≤ DA·BAnum }.
- 𝒯 = { (u, y) : u ∈ 𝒰, y ∈ ℤⁿ, a(u)·DB·d² + DA·e ≤ S·DA·DB·d² }.

**Théorème (note, th. 5.1).** On suppose que la machine Java respecte sa spécification (§ 2). Si une exécution `run` se termine avec le code 0 et la ligne `COUVERTURE_COMPLETE nt/nt`, alors, sous l'hypothèse d'intégrité du fichier de reprise (Z10) :
1. A et B sont définies positives ;
2. si aucun compteur n'a débordé (hypothèse de représentabilité), `COMPTE_U` = |𝒰| ;
3. sous la même hypothèse, `TOTAL_TOUCHES` = |𝒯|, et chaque ligne `TOUCHE` décrit un élément de 𝒯.

**Corollaire (note, cor. 5.2 : absence de touche, sans hypothèse sur les compteurs).** Sous M1 et M2, soit une exécution en mode `run`, avec un fichier de reprise **neuf** et sans récepteur de test, terminée avec le code 0 et la ligne `COUVERTURE_COMPLETE`. Si le répertoire du fichier de reprise ne contient aucun fichier de touche, et si aucun n'en a été retiré, alors 𝒯 = ∅. La preuve est au § 5 bis.

**Portée.** Le théorème porte sur les matrices lues. Il ne dit rien de leur lien avec le réseau idéal. Ce raccordement est une prémisse distincte, contrôlée exactement et sans PARI/GP par `code/verification/verifier_raccord.py` (note, prop. 6.3 et 6.4, point (1)) :
- avec ces fichiers, Λ_court(u) = a(u)/DA et Λ_fibre = e/(DB·d²). La norme du vecteur du réseau est (Λ_court + Λ_fibre)/2. Avec BA = 1057/200 et S = 12, 𝒯 est l'ensemble des vecteurs de norme ≤ 6 dont la projection courte est non nulle et d'énergie ≤ 1057/200, au signe près ;
- le signe ne perd rien : (u, y) ↦ (−u, −y) change w en −w et conserve les deux énergies ;
- le critère (note, th. 4.6, avec le lemme de Parseval et la relation à cinq termes) conclut : 𝒯 = ∅ **pour les deux côtés** entraîne l'absence de vecteur non nul de norme ≤ 6.

---

## 2. Modèle de la machine

- **M1.** Les opérations `+ − × /` sur `double` et la conversion `long → double` rendent l'arrondi au plus proche IEEE 754 binary64 du résultat exact (JLS § 15.17, § 15.18, § 5.1.2 ; classe `strictfp`, pas de contraction en FMA). `Math.sqrt` rend le double le plus proche de la racine exacte (spécification de `java.lang.Math`).
- **M2.** `Math.addExact`, `subtractExact`, `multiplyExact`, `negateExact` rendent le résultat entier exact ou lèvent `ArithmeticException`. `BigInteger` et `BigDecimal` sont exacts ; `new BigDecimal(double)` est la valeur binaire exacte du double.
- **M3.** Les pannes matérielles et les altérations de fichiers sont hors du modèle.

---

## 3. Lemmes repris du premier programme certifiant

**L1 (LDLᵀ rationnelle).** Pour G entière symétrique, le constructeur `FormeZ` calcule en rationnels exacts des d_i et des q_ij (j > i), refuse tout pivot d_i ≤ 0, puis **vérifie exactement** l'identité G_ij = Σ_{k ≤ min(i,j)} d_k q_ki q_kj (avec q_kk = 1). Donc, pour tout x réel,

 xᵀGx = Σ_i d_i T_i(x)², T_i(x) = x_i + Σ_{j>i} q_ij x_j,

et G est définie positive.

*Preuve.* Le coefficient de x_i x_j dans Σ_k d_k T_k(x)² est Σ_{k ≤ min(i,j)} d_k q_ki q_kj. L'identité est contrôlée à l'exécution : la preuve ne dépend pas de la justesse des récurrences. □

**L2 (encadrement d'un rationnel).** `encadre(p, q)` rend deux doubles finis lo ≤ p/q ≤ hi.

*Preuve.* Les deux boucles ne s'arrêtent que sur une comparaison exacte en `BigDecimal` (M2). L'approximation de départ ne sert jamais de borne. □

On note dL_i le minorant ainsi obtenu : 0 < dL_i ≤ d_i (le programme refuse dL_i ≤ 0).

**L3 (voisins extérieurs).** Soit ρ un réel et f le double fini rendu par une opération de M1 dont le résultat exact est ρ. Alors `dn(f)` ≤ ρ ≤ `up(f)`. `dn` et `up` lèvent une exception si leur argument ou leur résultat n'est pas fini.

*Preuve.* f est un double le plus proche de ρ, donc ρ est entre le prédécesseur et le successeur de f. `dn` rend le prédécesseur : par `Math.nextDown`, ou, pour x > 0 fini, par le motif binaire diminué de 1 (pour les doubles positifs, l'ordre est celui des motifs ; le motif de +0 suit par décrément celui de `MIN_VALUE`). De même pour `up`, avec x < `MAX_VALUE` pour que le successeur soit fini. Les gardes refusent NaN, ±∞ et les deux extrêmes dont le voisin est infini. □

**Remarque (puissances de 2).** La multiplication d'un double par 2^±F est exacte si le résultat est fini et normal, ou si elle augmente l'exposant. C'est le cas aux deux endroits où le code l'emploie (Z4, Z5).

---

## 4. Lemmes propres à Rang88CertZ

Dans tout ce paragraphe, une forme G est fixée (A pour le côté court, B pour la fibre), avec ses d_i, q_ij, dL_i. L'énumérateur `EnumZ` porte un vecteur entier w, de coordonnées **w_j = t_j + pas·y_j**, exactes en `long` :
- côté court : t = 0, pas = 1, donc w = y = u ;
- fibre : t = Tn·u (entier exact), pas = d, donc w = d·y + Tn·u.

L'énergie est Q(w) = wᵀGw = Σ_i d_i T_i(w)². Le budget exact est noté 𝔅 : un vecteur est **admissible** si Q(w) ≤ 𝔅.

### Z1 (virgule fixe)

Le constructeur calcule qI_ij = ⌊2ᶠ q_ij⌋ et **vérifie exactement** qI_ij ≤ 2ᶠ q_ij < qI_ij + 1. Pour w entier et un niveau i, on pose

 Sg_i = Σ_{j>i} qI_ij w_j, W_i = Σ_{j>i} |w_j|, Z_i = 2ᶠ w_i + Sg_i.

Alors **|2ᶠ T_i(w) − Z_i| ≤ W_i**. Par suite :
- (a) |2ᶠ T_i(w)| ≥ δ_i := max(0, |Z_i| − W_i) ;
- (b) |Z_i| ≤ 2ᶠ |T_i(w)| + W_i.

*Preuve.* 2ᶠ T_i − Z_i = Σ_{j>i} (2ᶠ q_ij − qI_ij) w_j, et chaque facteur 2ᶠ q_ij − qI_ij est dans [0, 1[. □

### Z2 (cache exact)

À chaque entrée dans `rec(i, …)`, on a exactement `cS[i][i+1]` = Sg_i et `absW[i+1]` = W_i pour les coordonnées courantes w_{i+1}, …, w_{n−1}.

*Preuve pour absW.* `fixe(j, ·)` pose absW[j] = absW[j+1] + |w_j|. Quand `rec(i)` est appelé, les coordonnées j > i ont été fixées dans l'ordre décroissant de j le long du chemin courant, chacune après la dernière modification de la suivante. On conclut par récurrence descendante depuis absW[n] = 0.

*Preuve pour cS.* On dit que l'entrée cS[k][j] (j > k) est *juste* si elle vaut Σ_{l ≥ j} qI_kl w_l pour le contenu courant du tableau w. Soit τ_k le plus grand j > k tel que cS[k][j] ne soit pas juste (τ_k = k s'il n'y en a pas). Deux faits simples : top[k] ≥ k toujours (`raz` pose n − 1, `descend(k)` pose k, les autres écritures sont des maxima) ; cS[k][n] = 0 est juste.

**Invariant (K).** Quand le contrôle est dans le corps de `rec(c)`, hors des appels à `descend` et à `rec(c − 1)`, on a pour toute ligne k < c : τ_k ≤ max(top[k], top[k+1], …, top[c−1]).

- *Départ* (`raz`, puis `executer` ou `feuilleA`) : tous les top valent n − 1 ≥ τ_k. Les `fixe` du préfixe ne touchent pas top. Le premier `descend(niv)` recalcule la ligne niv depuis cS[niv][n] = 0.
- *`fixe(c, ·)` dans `rec(c)`* : seul w_c change. Les entrées cS[k][j] avec j > c ne dépendent pas de w_c ; les autres peuvent devenir fausses. Donc τ_k ≤ max(ancien τ_k, c). L'instruction suivante pose top[c−1] ≥ c : (K) est rétabli. Rien ne lit le cache entre les deux.
- *`descend(c − 1)`* : (1) top[c−2] ← max(top[c−2], top[c−1]) ; (2) recalcul de cS[c−1][j] pour j = top[c−1], …, c, à partir de cS[c−1][top[c−1] + 1], juste par (K) appliqué à k = c − 1 ; après la boucle, toute la ligne c − 1 est juste ; (3) top[c−1] ← c − 1. Pour les lignes k < c − 1, l'ancien majorant max(top[k..c−1]) est conservé par (1). Donc (K) vaut à l'entrée de `rec(c − 1)`, et cS[c−1][c] = Sg_{c−1}.
- *Retour de `rec(c − 1)` vers `rec(c)`* : pour k < c − 1, (K) au niveau c − 1 donne la majoration voulue. Pour k = c − 1 : pendant `rec(c − 1)`, seules des coordonnées d'indice ≤ c − 1 ont changé et seules des lignes d'indice ≤ c − 2 ont été écrites ; la ligne c − 1, qui ne dépend que de w_l avec l ≥ c, est restée juste : τ_{c−1} = c − 1 ≤ top[c−1].
- *Enfant coupé* : rien n'est modifié.

Les opérations entières passent par `addExact` et `multiplyExact` : un débordement lève une exception (Z9), jamais une valeur fausse. □

**Contrôle à l'exécution.** Avec `-Dverif=1`, `verifie` recalcule Sg_i et W_i en `BigInteger` à chaque nœud et compare. Le harnais `TestCertZ` et P₄₆₁ côté 1 en entier (rang 44, 2,96·10⁸ nœuds) ont tourné dans ce mode (§ 7).

### Z3 (budgets majorés)

- **Côté court.** 𝔅 = DA·BAnum/BAden. `bornAU` = `encadre(DA·BAnum, BAden)[1]` ≥ 𝔅 (L2).
- **Fibre**, pour u donné, la = a(u). (u, y) ∈ 𝒯 équivaut à wᵀBw ≤ N/DA, avec N = DB·d²·(S·DA − la), entier calculé exactement. Si N < 0, aucun y ne convient. Sinon `borneU` = `up(up((double) N) / (double) DA)` ≥ N/DA.

*Preuve du second point.* Par L3, up((double) N) ≥ N ≥ 0. DA ≤ 2⁵³ (contrôlé) est converti exactement. Le quotient exact des deux doubles est ≥ N/DA, et L3 s'applique encore. □

Dans les deux cas on note B_U le majorant : 𝔅 ≤ B_U.

### Z5 (minorant d'énergie et coupe)

**Invariant.** À l'entrée de `rec(i, PL, ·)`, PL ≤ P_i := Σ_{k>i} d_k T_k(w)², énergie exacte des niveaux déjà fixés.

*Preuve.* Au sommet, PL = 0 = P_{n−1}. Soit un enfant de valeur y_i, donc w_i, Z_i, δ = |Z_i| − W_i (entiers exacts, Z2).
- Si δ ≤ 0 : PL2 = PL ≤ P_i ≤ P_{i−1}.
- Si δ > 0 : δ ≥ 1, donc (double) δ ≥ 1 et dd = dn((double) δ)·2⁻ᶠ vérifie 0 < dd ≤ δ/2ᶠ ≤ |T_i| (L3, mise à l'échelle exacte, Z1 (a)). Le produit dd·dd est un nombre normal > 0, donc x = dn(dd·dd) vérifie 0 < x ≤ T_i². Comme 0 < dL_i ≤ d_i, dn(x·dL_i) ≤ x·dL_i ≤ d_i T_i². Enfin PL2 = dn(PL + dn(x·dL_i)) ≤ PL + d_i T_i² ≤ P_{i−1}. □

**Coupe.** Un enfant n'est écarté que si PL2 > B_U. Alors tout vecteur prolongeant ce préfixe a Q(w) ≥ P_{i−1} ≥ PL2 > B_U ≥ 𝔅 : il n'est pas admissible. La valeur PL stockée dans une tâche du catalogue est le PL de son nœud : l'invariant se transmet à l'exécutant de la tâche.

### Z4 (plage entière)

Soit un nœud de niveau i, et w un vecteur admissible prolongeant son préfixe. Alors y_i ∈ [ylo, yhi].

*Preuve.* Par Z5, d_i T_i² ≤ 𝔅 − P_i ≤ B_U − PL ≤ `reste` = up(B_U − PL) (L3).
- Si `reste` < 0, c'est contradictoire : il n'y a aucun vecteur admissible sous ce nœud, et le retour immédiat est sûr.
- Sinon T_i² ≤ reste/d_i ≤ reste/dL_i ≤ up(reste / dL_i), puis |T_i| ≤ r := up(sqrt(up(reste / dL_i))) (L3 pour le quotient et pour la racine, par monotonie).
- `rs` = r·2ᶠ est exact (le programme refuse rs ≥ 2⁶² ou non fini). Par Z1 (b) et Z2 : |Z_i| ≤ ⌈rs⌉ + W_i = H.
- Z_i = C + M·y_i, avec C = 2ᶠ t_i + Sg_i et M = pas·2ᶠ, entiers exacts. Donc (−H − C)/M ≤ y_i ≤ (H − C)/M, soit −⌊(H + C)/M⌋ ≤ y_i ≤ ⌊(H − C)/M⌋.
- `plancherDiv(a, M, ·)` rend exactement ⌊a/M⌋ : ses deux boucles ne s'arrêtent que lorsque q·M ≤ a < (q + 1)·M, testé en entiers exacts. Son estimation flottante initiale n'a aucun rôle dans la preuve. □

La boucle parcourt tous les entiers de ylo à yhi. Elle calcule Z par ajouts exacts de M et s'arrête par un test d'égalité avant tout incrément inutile.

### Z6 (signe et vecteur nul)

Le drapeau `zeroDessus` de `rec(i)` vaut vrai si et seulement si y_k = 0 pour tout k > i (vrai au sommet, puis `zeroDessus && yv == 0`). Côté court (`signe` vrai), quand il est vrai, le code impose y_i ≥ 0, et y_0 ≥ 1 au niveau 0. Cela retire exactement le vecteur nul et les vecteurs dont la dernière coordonnée non nulle est négative. Il reste exactement les u normalisés. Dans la fibre, `signe` est faux : aucune restriction.

### Z7 (catalogue et tâches)

Le catalogue est produit par la même récursion sur A, en mode `gen`. À l'entrée de `rec(i)`, si i ≤ arretHaut = max(0, n − 1 − D) et si (i ≤ arretBas = max(0, n − 1 − Dmax) ou PL ≥ seuil·B_U), le nœud est **émis** comme tâche (niveau i, préfixe y_{i+1..n−1}, PL, drapeau zéro) et n'est pas développé.

- Tout nœud de niveau ≤ arretBas atteint est émis. Comme arretBas ≥ 0, `rec(0)` est toujours émis en mode `gen` : aucune feuille n'est traitée pendant la génération (une exception le garantit).
- Le test PL ≥ seuil·B_U ne décide que de la **profondeur** du découpage. Quel que soit son résultat, tout nœud non coupé de niveau ≤ arretBas a un unique ancêtre (ou lui-même) émis : les tâches forment une partition des sous-arbres.
- Par Z4, Z5, Z6, tout u ∈ 𝒰 a son chemin dans l'arbre non coupé, donc sous exactement une tâche.
- L'exécutant (`executer`) remet les caches à zéro, réinstalle le préfixe dans l'ordre décroissant des indices, recalcule la ligne du niveau (Z2), puis appelle `rec(niveau, PL, zéro)` hors mode `gen`. Il parcourt donc exactement le sous-arbre de la tâche.

Avec Dmax = D, le catalogue de P₁₃₉ côté 1 a les mêmes 19 426 préfixes et drapeaux, dans le même ordre, que celui du premier programme certifiant (§ 7).

### Z8 (feuilles exactes)

- **Feuille courte.** Par Z4 à Z7, `feuilleA` est appelée exactement une fois pour chaque u ∈ 𝒰 : au moins une fois par non-omission, au plus une fois parce que deux chemins distincts de l'arbre portent deux vecteurs distincts. Elle peut l'être pour d'autres u, admis par le jeu des encadrements. Les tests exacts `la <= 0` et `la·BAden > DA·BAnum` (en `long` à débordement détecté) retirent exactement ceux qui ne sont pas dans 𝒰. Donc `C.u` compte 𝒰.
- **Fibre.** Pour u ∈ 𝒰, `feuilleA` pose t = Tn·u (exact), le budget de Z3, puis énumère sur B. Par Z3, Z4, Z5 (appliqués à B), `feuilleB` est appelée pour tout y tel que (u, y) ∈ 𝒯.
- **Feuille de fibre.** `feuilleB` recalcule w = d·y + Tn·u en `BigInteger`, exige l'égalité avec le w de l'énumérateur, calcule e = wᵀBw et teste exactement la·DB·d² + DA·e ≤ S·DA·DB·d². Une touche est comptée si et seulement si (u, y) ∈ 𝒯 ; elle est alors écrite dans le fichier `.touches` (si un fichier de reprise est utilisé) et au journal (dans la limite de `maxImpr`).

### Z9 (domaine et exceptions)

Toute opération entière dont le débordement pourrait fausser une décision passe par une méthode `…Exact`. S'y ajoutent des refus explicites : Z = `Long.MIN_VALUE`, rs ≥ 2⁶², quotient estimé hors de ]−2⁶², 2⁶²[, valeur non finie dans `dn`/`up`, pivot ≤ 0, DA > 2⁵³, F hors de [8, 52].

Les seules opérations entières non contrôlées sont :
- les compteurs (`noeuds`, `C.u`, `C.cvp`, `C.touches`, histogramme), incrémentés d'une unité par événement ;
- `(Z < 0 ? -Z : Z) - W`, sans débordement puisque Z ≠ `MIN_VALUE` et W ≥ 0 ;
- `yv++`, exécuté seulement si yv < yhi.

Toute exception d'une tâche est propagée par `Future.get`, imprimée (`ERREUR …`), et donne le **code de sortie 2**. La ligne `COUVERTURE_COMPLETE` n'est alors pas imprimée. Un refus de domaine n'est jamais une décision d'absence.

### Z10 (fichier de reprise, bilan)

- **Liaison.** L'en-tête du fichier de reprise contient : le mode, n, BA, S, DA, DB, d, F, D, Dmax, seuil, le nombre de tâches, le SHA-256 du catalogue (indice, niveau, préfixe, bits de PL et drapeau de chaque tâche), le SHA-256 des quatre fichiers d'entrée et celui des classes chargées. Une reprise recalcule tout cela et **refuse** un fichier dont l'en-tête diffère d'un octet.
- **Écriture.** La ligne `T|t|U=…|CVP=…|NA=…|NB=…|TOUCHES=…|HIST=…|FIN` de la tâche t est écrite et forcée sur disque (`FileChannel.force`) seulement **après** le retour normal de `executer`. À la relecture, seules comptent les lignes complètes, terminées par un saut de ligne. Un reste sans saut de ligne final, laissé par un arrêt brutal en cours d'écriture, est retiré du fichier (troncature), et sa tâche est refaite. Toute ligne complète mal formée, toute tâche présente deux fois, tout indice hors catalogue lève une exception.
- **Arrêt sur touche.** Avec `-DstopTouche=1`, dès qu'une tâche terminée contient une touche, les tâches non commencées ne sont pas exécutées. Elles n'ont pas de ligne au fichier de reprise et ne sont jamais comptées : la sortie est alors `COUVERTURE_PARTIELLE`. Une touche est un témoin positif exact, rejouable seul ; ce mode ne produit jamais de conclusion négative.
- **Bilan.** `COUVERTURE_COMPLETE nt/nt` n'est imprimé que si chaque indice 0 ≤ t < nt possède un résultat, venu de ce lancement par `Future.get` ou relu du fichier de reprise. `COMPTE_U` et `TOTAL_TOUCHES` sont les sommes sur **tous** ces résultats.
- **Hypothèse d'intégrité.** Le fichier de reprise n'est pas signé. On suppose qu'il n'a été écrit que par ce programme. Chaque lancement imprime le SHA-256 du fichier qu'il relit et de celui qu'il laisse, ainsi que `EXECUTEES_CE_LANCEMENT` et `REPRISES_DU_CHECKPOINT`, pour un contrôle croisé par les journaux. Avec un fichier de reprise **neuf**, aucun reçu n'est relu et cette hypothèse n'intervient pas (§ 5 bis).
- Les options `-Ddebut`, `-Dfin`, `-Dliste` ne traitent qu'une partie des tâches. La sortie dit alors `COUVERTURE_PARTIELLE`, sauf si le fichier de reprise complète la couverture.

---

## 5. Preuve du théorème

1. `charger` construit `FormeZ(A)` et `FormeZ(B)` : par L1, A et B sont définies positives, sinon exception.
2. Code 0 et `COUVERTURE_COMPLETE` : par Z9 et Z10, chaque tâche du catalogue a été exécutée entièrement, sans exception, une fois.
3. Par Z7, chaque u ∈ 𝒰 est sous exactement une tâche ; par Z8, il est compté exactement une fois et aucun autre vecteur n'est compté. D'où `COMPTE_U` = |𝒰| si aucun compteur n'a débordé.
4. Par Z8, pour chaque u ∈ 𝒰, les touches comptées sont exactement les y avec (u, y) ∈ 𝒯. D'où le point 3, sous la même hypothèse. □

## 5 bis. Preuve du corollaire (absence de touche)

Par Z1 à Z8, tout élément de 𝒯 est une feuille admissible d'une tâche du catalogue, et le catalogue est une partition de l'arbre non coupé (Z7). Avec un fichier de reprise neuf, aucun reçu antérieur n'est chargé (branche « CHECKPOINT nouveau ») : le bilan n'est construit qu'à partir des tâches de ce lancement, et la ligne `COUVERTURE_COMPLETE` n'est imprimée que si chacune a rendu un résultat par `Future.get`, donc a été exécutée en entier. Une feuille admissible provoque, **sans condition sur la valeur d'un compteur**, l'appel de `ecrireTouche`, qui ajoute une ligne au fichier `<reprise>.touches`, créé au besoin ; une erreur d'écriture lève une exception (`UncheckedIOException`), qui remonte par `Future.get` jusqu'au code de sortie 2. Donc, si 𝒯 ≠ ∅, ou bien un fichier de touche existe, ou bien le code de sortie n'est pas 0. □

Pour les exécutions publiées, les prémisses du corollaire se contrôlent sur les pièces du dépôt : journaux (« CHECKPOINT nouveau », `SELECTION nt/nt ; A_FAIRE nt ; DEJA_AU_CHECKPOINT 0`, `EXECUTEES_CE_LANCEMENT nt ; REPRISES_DU_CHECKPOINT 0`, `COUVERTURE_COMPLETE`), codes de sortie, inventaire des répertoires de sortie (aucun fichier `.touches`) : `code/verification/verifier_recus.py`, contrôles R3, R4 et R7.

---

## 6. Table code ↔ lemmes

| Élément du source | Rôle | Lemme |
|---|---|---|
| `FormeZ` : récurrences, pivots, contrôle final de l'identité | LDLᵀ exacte | L1 |
| `encadre`, `cmpDoubleRat` ; `dL[i]` | minorant certifié de d_i | L2 |
| `dn`, `up` | voisins extérieurs | L3 |
| `FormeZ` : `qI[i][j]`, contrôle du plancher | virgule fixe | Z1 |
| `EnumZ.fixe`, `descend`, `top`, `raz` ; `verifie` | sommes partielles entières exactes | Z2 |
| `charger` : `bornAU` ; `feuilleA` : `N`, `eB.borneU` | budgets majorés | Z3 |
| `rec` : `reste`, `r`, `rs`, `H`, `C`, `ylo`, `yhi` ; `plancherDiv` | plage entière | Z4 |
| `rec` : `delta`, `dd`, `PL2`, `garde` | minorant et coupe | Z5 |
| `rec` : `signe && zeroDessus` | signe, vecteur nul | Z6 |
| `rec` : branche `gen` ; `catalogue` ; `Travail.executer` | partition en tâches | Z7 |
| `feuilleA`, `feuilleB` | tests exacts | Z8 |
| appels `…Exact`, refus de domaine, `main` (code 2) | exceptions | Z9 |
| `lance` : en-têtes, `ecrireCkpt`, relecture, `Future.get`, bilan ; `ecrireTouche` | reprise, couverture, fichier de touche | Z10, corollaire |

Les numéros de ligne sont dans `LIAISON_PREUVE_CODE.md`.

---

## 7. Validation exécutée (constaté)

Machine du premier ordinateur : OpenJDK 11.0.16.1 sous Windows, 6 fils. Ces validations portent sur des cas finis ; elles ne remplacent pas la preuve et ne disent rien de P₁₃₉ ni de P₅₉₉. Les journaux historiques de cette campagne ne sont pas inclus ; les résultats ci-dessous sont ceux de la note (§ 5.2). Les lignes marquées « rejoué » ont été refaites depuis ce dépôt (`verification/RESULTATS.md`).

| test | attendu | obtenu |
|---|---|---|
| Harnais `TestCertZ`, E8 (10 découpages) | 120 puis 1 200 représentants | identique |
| Harnais, 5 400 formes aléatoires de dimension 2 à 4 (côté court + fibre, T, d, DA, DB), F = 8, 20, 40, 52, recalcul exact des caches | mêmes ensembles qu'une énumération exhaustive par boîte en entiers | 16 250 contrôles, 0 échec ; **rejoué** sur 300 formes (graine 1) : 910 contrôles, 0 échec |
| L₀ côté 1, 1057/200, S = 12, D = 6 | 4 004 + 399 872 u (valeurs d'autres programmes) ; 0 touche | 403 876 u ; TOTAL_TOUCHES 0 ; COUVERTURE_COMPLETE 9 423/9 423 ; 551 s |
| L₀ côté 2, découpage adaptatif de production (Dmax = 16, seuil 0,2), fichier de reprise | idem | 403 876 u ; 0 touche ; 15 664/15 664 ; 618 s |
| L₀, témoin positif (BA = 4, S = 16) | 4 004 u ; 97 152 touches | 4 004 u ; 97 152 touches ; 634 s |
| P₄₆₁ côté 1, BA = 7/2 | 697 u ; 2 touches de norme 6 | 697 u ; 2 touches : (1595/461 + 7 259 828/922²)/2 = 6 et (1579/461 + 7 289 332/922²)/2 = 6 ; **rejoué** : identique, catalogue `30d7a99f…` |
| P₄₆₁ côté 1 en entier avec `-Dverif=1` (rang 44, 2,96·10⁸ nœuds) | aucun écart du cache | aucun écart ; mêmes 697 u et 2 touches |
| Arrêt brutal de L₀ côté 1 puis reprise | mêmes totaux | 210 tâches reprises + 9 213 exécutées ; 403 876 u ; 0 touche |
| Fichier de reprise tronqué au milieu de sa dernière ligne (P₄₆₁ côté 2) | ligne retirée, tâche refaite | 1 ligne retirée, 1 tâche refaite, mêmes totaux ; troisième lancement : 0 tâche à faire |
| Reprise avec d'autres classes | refus | refus (« checkpoint incompatible ») |
| `-DstopTouche=1` sur P₄₆₁ côté 1 | arrêt après la touche, pas de conclusion | `COUVERTURE_PARTIELLE` ; **rejoué** avec le découpage de production : 1 touche, `COUVERTURE_PARTIELLE 388/5003`, fichier `.touches` créé |
| Catalogue P₁₃₉ côté 1, D = 6 | celui du premier programme certifiant (19 426 tâches) | mêmes 19 426 préfixes et drapeaux, même ordre |
| Catalogues de production des quatre côtés (mode `taches`) | empreintes `fd9e41bd…`, `39e9d80b…`, `b9ff8375…`, `a97cb23d…` | **rejoué** : quatre catalogues identiques octet pour octet à ceux du dépôt |

**Nombres de nœuds.** Sur L₀ (deux côtés) et sur le témoin, le nombre de nœuds de fibre est identique à l'unité près à celui d'un énumérateur flottant non certifiant, et les nœuds courts ne diffèrent que des nœuds de génération du catalogue. Cela ne dit rien de P₁₃₉ ni de P₅₉₉.

---

## 8. Limites et réserves

Réserves formulées à la relecture (note, § 5.3) :
1. **Z9.** Les compteurs locaux ne détectent pas leur propre débordement. Le comptage exact (points 2 et 3 du théorème) demande une hypothèse de représentabilité. La conclusion 𝒯 = ∅ ne dépend d'aucun compteur (corollaire). Dans les exécutions publiées, le plus grand compteur d'un reçu est < 2³² et le plus grand total < 2⁴² (`verifier_recus.py`, R9) : argument de cohérence, sans borne démontrée sur les compteurs internes.
2. **Z10.** Une couverture complète qui s'appuie sur des reçus relus ne prouve pas, à elle seule, que les tâches correspondantes ont été exécutées : le chargeur contrôle la syntaxe, les indices et les doublons, et ne rejoue rien. La conclusion de la note s'appuie sur des exécutions sans reprise (fichier de reprise neuf), où ce cas ne se présente pas.
3. **Écritures.** L'écriture d'un reçu n'est pas bouclée jusqu'à épuisement du tampon, et le verrou est interne à la machine virtuelle ; l'unicité de l'écrivain n'est pas garantie entre processus.
4. **Identité.** Le programme calcule l'empreinte des fichiers de classes relus, non celle des octets chargés en mémoire. Une recompilation du source avec le même compilateur redonne les classes octet pour octet (rejoué, `verification/RESULTATS.md`).

Autres limites :
5. Points à relire en priorité : Z2 (invariant du cache), Z4 et Z5 (les deux seuls endroits où des flottants décident ; chaque opération flottante y est suivie d'un `dn` ou d'un `up`, sauf les deux mises à l'échelle par 2^±F, exactes), Z1 (le signe de l'erreur de troncature : qI est un plancher, l'erreur 2ᶠq − qI est dans [0, 1[).
6. Le théorème ne couvre pas le raccordement géométrique (§ 1), ni l'identification de la classe d'idéaux (sous GRH pour les composantes 331 et 45 013).
7. Aucune implantation indépendante de l'énumération n'a été exécutée.

## 9. Empreintes SHA-256

| fichier | SHA-256 |
|---|---|
| `code/certifiant/Rang88CertZ.java` | 9e467c750470301ec0612c087b84636da6b46538a0fe33458970af6cb97bc3c5 |
| `code/certifiant/TestCertZ.java` | d77831aa7bb8d4c03fa3028bc649cc873c49c4e0ead0d394bfd80000713a5db5 |
| `classes/Rang88CertZ.class` | 35130e199599a72f6c65b199a13f0190c6ba0438899594d9a0cea48c38c652e5 |
| `classes/Rang88CertZ$Compteurs.class` | 9db7355dc8cad2ecfa8056b9bff569642544ebbab23e3db30833fafdda9152a8 |
| `classes/Rang88CertZ$EnumZ.class` | a1ed4ee2f289e88cd440246ce066455ac3fed9d414a0525ab80bdf12342830af |
| `classes/Rang88CertZ$FormeZ.class` | b7028cb6168c77ed08dd552dcf9760946c7e8bddbb0d245ab4b31fdae8ed6cb9 |
| `classes/Rang88CertZ$Recepteur.class` | 5c47eba99fa800f0dbbdf8adb5de1efb5f1a11e08bac5158f97787eb3b2b526b |
| `classes/Rang88CertZ$Tache.class` | 5e3b4b4877e242bcd76f202c87929473af00944b277d815d2b0c8cc95f7aa2b3 |
| `classes/Rang88CertZ$Travail.class` | a33c837d37c4d03ac0a064170fb6f853790ae0010e14d5a52e217c47076857e3 |
| `classes/TestCertZ.class` | 60aed39c3fc32a76da5e61fad04465a45a224edef1dd069cbeabf30961638fc4 |

Compilation : `javac -d <dossier neuf> Rang88CertZ.java TestCertZ.java`, OpenJDK 11.0.16.1. Chaque journal d'exécution imprime les empreintes des sept classes du programme et des quatre fichiers d'entrée ; toutes les exécutions publiées portent le même lien de classes `4f1ed5ad…`.
