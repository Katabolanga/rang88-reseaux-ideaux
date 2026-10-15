# Résultats des vérifications rejouées depuis ce dépôt

Ces sorties sont celles d'un rejeu complet fait **depuis une copie neuve de ce dépôt**, placée dans un répertoire court du répertoire temporaire (les chemins de plus de 260 caractères sont refusés par PARI/GP et Python sous Windows), le jour de la version de la note. Aucun balayage certifiant complet n'a été relancé. Seuls ont été remplacés, dans les sorties ci-dessous : le chemin des exécutables (`python`, `gp`), celui du répertoire temporaire des essais Java (`$T`), le numéro de processus et la date imprimés par la machine virtuelle (essai J3), et les lignes de durée de l'interpréteur de commandes.

Environnement : Windows 11, processeur Ryzen 7 5700U ; Python 3.11.5 (Anaconda, bibliothèque standard seulement, `-I -B`) ; PARI/GP 2.15.4 ; OpenJDK 11.0.16.1 (Microsoft). Le fichier de R. Sakamoto a été placé en `externe/integer_input.txt` pour ce rejeu (SHA-256 `68af477caf3f6d6a8980c40f234bcb47c0bac6caf3582c1757280cb64457631f`, contrôlé par les deux scripts qui le lisent) ; il n'est pas dans le dépôt.

## Bilan

| Vérification | Énoncé de la note | Résultat | Durée |
|---|---|---|---|
| `verifier_sha256.py` | intégrité du dépôt | 140 fichiers conformes, 0 absent ou différent, 0 non listé (rejeu fait avant l'écriture de ce fichier ; le `SHA256SUMS.txt` final couvre aussi ce fichier) | 1 s |
| `verifier_corps.py` | notations : β₀, H | 5 contrôles, 0 échec | 1 s |
| `hmoins115.gp` | prop. 2.2 | h⁻(115) = 44 697 909 = 3·331·45 013 ; h⁻(87) = 1 536, h⁻(65) = 64, h⁻(85) = 6 205 | 1 s |
| `caracteres115.gp` | prop. 2.5, tableau 1 | six classes de caractères impairs ; 508 463 orbites ; Burnside 508 463 | 1 s |
| `verifier_hmoins_caracteres.py` | prop. 2.2, 2.5, tableau 1 (second calcul) | 13 contrôles, 0 échec | 1 s |
| `verifier_H_L0.py` | § 2.5 : H ≅ L₀ | VALIDE (det P = −1, P G Pᵀ = G_H, P TXᵃ = Z P) | 5 s |
| `verifier_conformite_article.py` | § 2.5 : Q G_art Qᵀ = G | VALIDE | 3 s |
| `verifier_temoins.gp` | prop. 6.1, tableau 2 | 8 témoins valides sur 8 | 10 s |
| `verifier_temoins.py` | prop. 6.1, tableau 2, § 6.1 | 8 témoins, 0 échec ; empreintes abrégées conformes au tableau 2 ; décompositions des trois touches | 1 min |
| `verifier_raccord.py P139` | prop. 6.3 (1), (2) | 37 contrôles, 0 échec ; I = (139, ζ² + ζ + 77) | 50 s |
| `verifier_recus.py P139` | prop. 6.3 (3), réplication | 87 contrôles, 0 échec | 5 s |
| `verifier_classe_P139.py` | prop. 6.6 | 24 contrôles, 0 échec | 10 s |
| `verifier_raccord.py P599` | prop. 6.4 (1), (2) | 37 contrôles, 0 échec ; I = (599, ζ² + 87ζ + 322) | 50 s |
| `verifier_recus.py P599` | prop. 6.4 (3), H4, rejeu, réplication | 98 contrôles, 0 échec | 10 s |
| `verifier_classe_P599.py` | prop. 6.7 | 37 contrôles, 0 échec | 10 s |
| `localiser_classes.gp` (S1) | tableaux 2 et 3, colonne « orbite » (sous GRH) | sorties identiques aux journaux d'origine | 1 min 15 s |
| `preparer.sh` (S2) | § 5.1 (préparation) | 22 fichiers d'entrée régénérés, tous IDENTIQUES | 1 min 30 s |
| J1 recompilation | § 5.3, « Identité » | 8 classes sur 8 identiques octet pour octet | 3 s |
| J2 harnais `TestCertZ 1 300` | § 5.2, « Validation » | 910 contrôles, 0 échec | 25 s |
| J3 P₄₆₁ au seuil 7/2 | § 5.2, « Validation » | 697 u ; 2 touches (1595/461 + 7 259 828/922², 1579/461 + 7 289 332/922²) ; `COUVERTURE_COMPLETE 3658/3658` | 7 s |
| J4 lanceur `rejouer_cote.sh` | — | 1 touche, couverture partielle, fichier `.touches` créé ; refus d'un répertoire non neuf | 3 s |
| J5 catalogues | Z7, R5 | quatre catalogues identiques octet pour octet | 2 s chacun |
| J6 tâches isolées | déterminisme des reçus | 6 + 6 reçus rejoués identiques aux reçus publiés | 2 s chacun |
| J7 `empreinte_canonique.py` | § 6.2 | `c99dcf87…5122`, `8ab1f40a…daf7`, `f3cf379a…2689`, `b9c93a83…8ef6` | 1 s |

Remarque sur J4 : dans la sortie ci-dessous, « code de sortie du lanceur : 0 » est celui du tube `… | sed` utilisé pour masquer le chemin temporaire ; appelé directement, le lanceur rend le code 4 sur ce refus.

Remarque sur les nombres de contrôles : `verifier_raccord.py` fait 37 contrôles pour chaque candidat, contre 43 et 47 dans les versions de travail dont il est tiré. La différence vient des contrôles d'empreinte : les versions de travail comparaient les fichiers d'entrée à des manifestes internes (8 à 10 contrôles) ; la version publiée les compare aux empreintes imprimées par chacune des exécutions conservées (2 contrôles). Les contrôles mathématiques G1 à G9 sont inchangés.

## Sortie complète de `sh code/verification/tout_verifier.sh`

```

==== python -I -B code/verification/verifier_sha256.py
BILAN : 140 fichiers conformes, 0 absents ou differents, 0 fichiers non listes
==== code de sortie 0

==== python -I -B code/verification/verifier_corps.py
donnees : data/corps/rang88_m115c0_data.txt SHA-256 7b71b5f176b8bdac1d1236e5e59376674012089b3fb66b72e4a9b48ddf116f3a
   Pm = x^44 - x^43 - 44*x^42 + ... + 24*x + 1 ; beta_0 = -19/5*x^43 + ... + -1236/115
OK    K1 Pm entier, unitaire, de degre 44, et Pm(c) = 0 dans Z[zeta_115]
OK    K2 T = (Tr+(beta_0 c^(i+j))) entiere et symetrique
OK    K2 det T = 1 et T definie positive (44 mineurs principaux > 0) : beta_0 totalement positif et beta_0 D = O+
OK    K3 Tr_L(beta_0 zeta^r) entier pour tout r, et reel (symetrie r -> -r)
OK    K3 G_H paire, de determinant 1, definie positive (88 mineurs > 0) ; diagonale 420
BILAN : 5 controles, 0 echecs
FIN_OK
==== code de sortie 0

==== gp -q -D parisize=400000000 code/verification/hmoins115.gp
m = 3*29 = 87 : [nb chi impairs, h^-] = [28, 1536]   (attendu 1536)
m = 5*13 = 65 : [24, 64]
m = 5*17 = 85 : [32, 6205]
m = 5*23 = 115 : [44, 44697909]
factorisation de h^-(115) : [3, 1; 331, 1; 45013, 1]
==== code de sortie 0

==== gp -q -D parisize=400000000 code/verification/caracteres115.gp
chi_(0,1) : ordre 22, conducteur 23, 10 conjugues ; N(-B1/2) = 1/23 = Mat([23, -1])
chi_(0,11) : ordre 2, conducteur 23, 1 conjugues ; N(-B1/2) = -3/2 = [2, -1; 3, 1]
chi_(1,0) : ordre 4, conducteur 5, 2 conjugues ; N(-B1/2) = 1/10 = [2, -1; 5, -1]
chi_(1,2) : ordre 44, conducteur 115, 20 conjugues ; N(-B1/2) = 45013 = Mat([45013, 1])
chi_(2,1) : ordre 22, conducteur 115, 10 conjugues ; N(-B1/2) = 331 = Mat([331, 1])
chi_(2,11) : ordre 2, conducteur 115, 1 conjugues ; N(-B1/2) = -1 = matrix(0,2)
produit des normes * Q * w = 44697909 (attendu 44697909)
p = 3 : classes de caracteres avec p | N(B1/2) : [[[0, 11], 2, 23, 1]]
p = 331 : classes de caracteres avec p | N(B1/2) : [[[2, 1], 22, 115, 1]]
p = 45013 : classes de caracteres avec p | N(B1/2) : [[[1, 2], 44, 115, 1]]
p = 3 : chi d'ordre 2, conducteur 23, |noyau| = 44 ; corps fixe de degre 2
p = 331 : chi d'ordre 22, conducteur 115, |noyau| = 4 ; corps fixe de degre 22
p = 45013 : chi d'ordre 44, conducteur 115, |noyau| = 2 ; corps fixe de degre 44
support [] : 1 classes, orbites de taille 1, 1 orbites
support [45013] : 45012 classes, orbites de taille 44, 1023 orbites
support [331] : 330 classes, orbites de taille 22, 15 orbites
support [331, 45013] : 14853960 classes, orbites de taille 88, 168795 orbites
support [3] : 2 classes, orbites de taille 2, 1 orbites
support [3, 45013] : 90024 classes, orbites de taille 88, 1023 orbites
support [3, 331] : 660 classes, orbites de taille 44, 15 orbites
support [3, 331, 45013] : 29707920 classes, orbites de taille 88, 337590 orbites
TOTAL : 44697909 classes (attendu 44697909), 508463 orbites galoisiennes dans S
Burnside : (1/88) sum |Fix| = 508463
==== code de sortie 0

==== python -I -B code/verification/verifier_hmoins_caracteres.py
== H1 nombre de classes relatif
OK    H1 h^-(87) = 1536 (28 caracteres impairs) ; valeur attendue 1536
OK    H1 h^-(65) = 64 (24 caracteres impairs) ; valeur attendue 64
OK    H1 h^-(85) = 6205 (32 caracteres impairs) ; valeur attendue 6205
OK    H1 h^-(115) = 44697909 = 3 * 331 * 45013 (44 caracteres impairs)
== H2 classes rationnelles de caracteres impairs modulo 115
   chi_(0,1) : ordre 22, conducteur 23, 10 conjugues ; N(-B1/2) = 1/23
   chi_(0,11) : ordre 2, conducteur 23, 1 conjugues ; N(-B1/2) = 3/2
   chi_(1,0) : ordre 4, conducteur 5, 2 conjugues ; N(-B1/2) = 1/10
   chi_(1,2) : ordre 44, conducteur 115, 20 conjugues ; N(-B1/2) = 45013
   chi_(2,1) : ordre 22, conducteur 115, 10 conjugues ; N(-B1/2) = 331
   chi_(2,11) : ordre 2, conducteur 115, 1 conjugues ; N(-B1/2) = 1
OK    H2 six classes rationnelles ; produit des normes * Q * w = 44697909
OK    H2 p = 3 : une seule classe de caracteres a une norme divisible par p, de valuation 1 (chi_(0, 11), ordre 2)
OK    H2 p = 331 : une seule classe de caracteres a une norme divisible par p, de valuation 1 (chi_(2, 1), ordre 22)
OK    H2 p = 45013 : une seule classe de caracteres a une norme divisible par p, de valuation 1 (chi_(1, 2), ordre 44)
== H3 noyaux et orbites
OK    H3 noyau de chi_3 : ordre 44 (corps fixe Q(sqrt(-23))) ; chi_3 = symbole de Legendre modulo 23
OK    H3 noyau de chi_331 = {1, 22, 24, 68}
OK    H3 noyau de chi_45013 = {1, 91}
   support []                 :         1 classes, orbites de taille  1,       1 orbites
   support [3]                :         2 classes, orbites de taille  2,       1 orbites
   support [331]              :       330 classes, orbites de taille 22,      15 orbites
   support [3, 331]           :       660 classes, orbites de taille 44,      15 orbites
   support [45013]            :     45012 classes, orbites de taille 44,    1023 orbites
   support [3, 45013]         :     90024 classes, orbites de taille 88,    1023 orbites
   support [331, 45013]       :  14853960 classes, orbites de taille 88,  168795 orbites
   support [3, 331, 45013]    :  29707920 classes, orbites de taille 88,  337590 orbites
OK    H3 tableau 1 de la note : classes, tailles et nombres d'orbites par support ; total 44697909 classes, 508463 orbites
OK    H3 formule de Burnside : (1/88) sum_a |Fix(a)| = 508463
BILAN : 13 controles, 0 echecs
FIN_OK
==== code de sortie 0

==== python -I -B code/verification/verifier_H_L0.py
fichier externe : SHA-256 68af477caf3f6d6a8980c40f234bcb47c0bac6caf3582c1757280cb64457631f
fichier externe : empreinte conforme (revision 628ce2a7, data/L0/integer_input.txt) ; lecture comme texte
G (fichier externe) : n = 88, symetrique True, det 1, paire True, definie positive True, diagonale 12..16
G_H = (Tr_L(beta zeta^(i-j))) recalculee sans GP : det 1, paire True, definie positive True, diagonale 420
beta du certificat == beta_0 de data/corps : True
det P = -1 ; max |P_ij| = 73 ; P G P~ == G_H : True
TX = (M5 M23)~ : TX G TX~ == G : True ; TX d'ordre 115 : True ; P TX^a == Z P (a = 1) : True
RESULTAT (Python, entiers exacts) : certificat H = (O_L, beta_0) ~= L_0 (Sakamoto) : VALIDE
==== code de sortie 0

==== python -I -B code/verification/verifier_conformite_article.py
fichier externe : SHA-256 68af477caf3f6d6a8980c40f234bcb47c0bac6caf3582c1757280cb64457631f
delta_4 reel, N_{F(zeta_5)/Q}(delta_4) = 5^6 23^4 (= |disc F(zeta_5)|) : True
p_1..p_4 : coefficients dans O_F, det dans la base 1, zeta_5, zeta_5^2, zeta_5^3 = unite de O_F (det = 1 + 0 g) : True
Gram de h_4 dans la base p_i == matrice de la rem. 3.3 : True
a reel, a(21) = 0 mod 47, N_{T/Q}(a) = 47^2  (=> a O_T = J Jbar) : True
N_{T/Q}(delta_11) = 23^10 (norme de la differente de T/F) : True
j_0(21) = 0 mod 47, N_{T/Q}(j_0) = 2^11 47, j_0 alpha dans 2 O_T, j_0 alphabar hors de 2 O_T  (=> j_0 O_T = pbar J = J_0) : True
h_11^(0)(j_0 z^j, j_0 z^l) dans O_F, hermitienne : True
G_art (base p_i (x) j_0 zeta_23^(j-1)) : entiere, symetrique, paire, det 1, definie positive (det = 1, diagonale 380449932) : True
X entiere 22 x 22, det X = +-1 (det = -1, max |X_jl| = 31) : True
PRINCIPAL : G (depot, integer_input.txt) == (Tr_{F/Q}(h_4(p_i, p_k) h_11^(0)(x''_j, x''_l))), x''_j = sum_l X[j][l] j_0 zeta_23^(l-1) : True
Q = I_4 (x) X : Q G_art Q~ == G : True
M23~ (depot) == multiplication par zeta_23 sur le facteur J_0 : M23~ Q == Q (I_4 (x) Z23) : True
chaine : P G P~ == G_H (certificat_H_L0) et (P Q) G_art (P Q)~ == G_H, det(P Q) = -1 : True
RESULTAT (Python, exact) : la Gram du depot de Sakamoto (L_0) est la Gram de B_0 = Tr_{F/Q}(h_4 (x) h_11^(0)) de l'article dans la base p_i (x) x''_j : VALIDE
==== code de sortie 0

==== gp -q -D parisize=400000000 code/verification/verifier_temoins.gp
P461 (temoin_P461r5.gp) : TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal) ; norme du temoin = 6 ; I d'indice 461 dans Z[zeta]
P691 (temoin_P691r4.gp) : TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal) ; norme du temoin = 6 ; I d'indice 691 dans Z[zeta]
P1151 (temoin_P1151r6.gp) : TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal) ; norme du temoin = 6 ; I d'indice 1151 dans Z[zeta]
P1381 (temoin_P1381r21.gp) : TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal) ; norme du temoin = 6 ; I d'indice 1381 dans Z[zeta]
P1471_quadratic_879_948 (temoin_P1471d2.gp) : TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal) ; norme du temoin = 6 ; I d'indice 2163841 dans Z[zeta]
P829 (temoin_P829d2.gp) : TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal) ; norme du temoin = 6 ; I d'indice 687241 dans Z[zeta]
P1289 (temoin_P1289d2.gp) : TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal) ; norme du temoin = 6 ; I d'indice 1661521 dans Z[zeta]
P1979 (temoin_P1979d2.gp) : TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal) ; norme du temoin = 6 ; I d'indice 3916441 dans Z[zeta]
BILAN : 8 temoins valides sur 8
==== code de sortie 0

==== python -I -B code/verification/verifier_temoins.py
P461    temoin_P461r5.gp     SHA-256 d41592a857441799... : I = (461, 1*z^1 + 456) ; |det BASE| = 461 ; GRAM paire, det 1, definie positive ; X~ GRAM X = 6 : TEMOIN VALIDE
P691    temoin_P691r4.gp     SHA-256 f3cf48f3a39b50b5... : I = (691, 1*z^1 + 687) ; |det BASE| = 691 ; GRAM paire, det 1, definie positive ; X~ GRAM X = 6 : TEMOIN VALIDE
P1151   temoin_P1151r6.gp    SHA-256 a5705522d65707ef... : I = (1151, 1*z^1 + 1145) ; |det BASE| = 1151 ; GRAM paire, det 1, definie positive ; X~ GRAM X = 6 : TEMOIN VALIDE
P1381   temoin_P1381r21.gp   SHA-256 4a45c630cc2ff139... : I = (1381, 1*z^1 + 1360) ; |det BASE| = 1381 ; GRAM paire, det 1, definie positive ; X~ GRAM X = 6 : TEMOIN VALIDE
P1471   temoin_P1471d2.gp    SHA-256 11b4d4cbc81f0b35... : I = (1471, 1*z^2 + 879*z^1 + 948) ; |det BASE| = 2163841 ; GRAM paire, det 1, definie positive ; X~ GRAM X = 6 : TEMOIN VALIDE
        P829 : rotation k = [0] : Lambda(a_k) = 3161/829 et Lambda'(b_k) = 6787/829 (somme 12)
P829    temoin_P829d2.gp     SHA-256 52222d1ce3d0de52... : I = (829, 1*z^2 + 357*z^1 + 502) ; |det BASE| = 687241 ; GRAM paire, det 1, definie positive ; X~ GRAM X = 6 : TEMOIN VALIDE
        P1289 : rotation k = [0] : Lambda(a_k) = 5683/1289 et Lambda'(b_k) = 9785/1289 (somme 12)
P1289   temoin_P1289d2.gp    SHA-256 4c5f7602b55ae23d... : I = (1289, 1*z^2 + 979*z^1 + 669) ; |det BASE| = 1661521 ; GRAM paire, det 1, definie positive ; X~ GRAM X = 6 : TEMOIN VALIDE
        P1979 : rotation k = [0] : Lambda(a_k) = 9260/1979 et Lambda'(b_k) = 14488/1979 (somme 12)
P1979   temoin_P1979d2.gp    SHA-256 71d980e2348c1943... : I = (1979, 1*z^2 + 1150*z^1 + 1044) ; |det BASE| = 3916441 ; GRAM paire, det 1, definie positive ; X~ GRAM X = 6 : TEMOIN VALIDE
BILAN : 8 temoins, 0 echecs
FIN_OK
==== code de sortie 0

==== python -I -B code/verification/verifier_raccord.py P139
candidat P139
I_data.gp SHA-256 a133ab58a8e95ded67f38e2e1c8d224ce0cb9a4849555d61e2c4f0b6f269bbd4 ; PREMIERS = [[139, 2, 1]] ; Q = 19321
OK    dimensions : BASE, GRAM, AB 88 x 88 ; NU, ALPHA de degre <= 43 ; Q = 139^2
OK    G1 |det BASE| = 139^2 (indice de I dans Z[zeta])
OK    G1 zeta * I contenu dans I (I est un ideal de Z[zeta_115])
OK    G1 I mod 139 = (g), g unitaire de degre 2 divisant Phi_115 mod 139
OK    G1 g irreductible mod 139 (discriminant non residu)
OK    G1 139 dans I et g(zeta) dans I : I = (139, g(zeta)), premier de degre residuel 2
OK    G1 I different de son conjugue (g* != g), donc I + Ibar = O_L
      g = y^2 + 1 y + 77 ; g* = y^2 + 65 y + 65 (mod 139)
OK    G2 alpha reel : Tr(alpha zeta^k) = Tr(alpha zeta^-k)
OK    G2 BASE~ H BASE = GRAM (H recalculee depuis ALPHA), entiere
OK    G2 GRAM symetrique et paire
OK    G2 GRAM definie positive (88 mineurs principaux dominants > 0, exact)
OK    G2 det GRAM = 1
      diagonale de GRAM : min 854532, max 443265592
OK    G3 nu dans I (donc dans I inter Ibar = I Ibar, nu etant reel)
OK    G3 Pm(c) = 0 dans Z[zeta], Pm unitaire de degre 44 (polynome minimal de c = zeta + 1/zeta)
OK    G3 N_{L+/Q}(nu) = 139^2 = N(I) : (nu) O_L = I Ibar
OK    G4 pour les 88 vecteurs de base z de I : z + zbar = a(c), z - zbar = e b(c), (b ; a) = colonne de AB
OK    G4 |det AB| = 2^44 * 139^2
OK    G5 AB~ diag(QB, QA) AB / 2 = GRAM : N(z) = (Lambda(a) + Lambda'(b)) / 2 sur tout I
OK    G5 QA (denominateur commun 139) definie positive, det = 1/139^2
OK    G5 QB (denominateur commun 139) definie positive, det = 1/139^2
      SHA-256 e7f509e2fffc5fc86d69d5f7ac45a8b5a180146fb7e39dbfc3db3cbf94c4fa26  cote1_A.gram
      SHA-256 fc229cd0c4c09090c2e858324526852359668eec35e703f5a7a349dbca8c3e14  cote1_B.gram
      SHA-256 f3c1f7600f08404d099d6a4247363a5bef9246707015f977fbf9d76c46cdabe5  cote1_T.mat
      SHA-256 4ed14f1782911811eff6471b78758a91b2f4c6012ac5380b2d2a9fc98d93be91  cote1_meta.txt
      SHA-256 37c33888013ddabda81f4d42e11249c8af2b66d39609c579c08096c155bef8d7  cote1_bases.gp
OK    G6 cote 1 : les 4 empreintes d'entrees imprimees par chacun des 2 journaux d'execution (premiere_execution/cote1.log, replication/cote1.stdout.log) = fichiers actuels
OK    G6 cote 1 : R^-1 [[Hf, Hl], [0, Hc]] entiere et |det| egaux : meme reseau M (bijection I <-> (u, y) dans Z^44 x Z^44)
OK    G6 cote 1 : A.gram = DA Hc~ QC Hc (DA = 139)
OK    G6 cote 1 : B.gram = DB Hf~ QF Hf (DB = 1)
OK    G6 cote 1 : Hf Tn = d Hl (d = 278) : coordonnees de fibre du relevement = Tn u / d
OK    G6 cote 1 : reseau de fibre Hf Z^44 = 2 nu O+ (meme reseau colonne)
      SHA-256 877dc5f596680d464e440a37197ec1293a6cfb3ac8d58d510fdfc2299426cc94  cote2_A.gram
      SHA-256 eda51cf5c5fbad90a61b4a39ce5d57e5646e8eb07a50d315d58a751aa7e221d8  cote2_B.gram
      SHA-256 f7fb1298ef841ccf821a73f97d5bae97d415c22802db4c5a9c8a10378cc24ca0  cote2_T.mat
      SHA-256 4ed14f1782911811eff6471b78758a91b2f4c6012ac5380b2d2a9fc98d93be91  cote2_meta.txt
      SHA-256 681301dbf14e2e51933636fc1dda52951a57c8fa96c47f626022430559cbfcab  cote2_bases.gp
OK    G6 cote 2 : les 4 empreintes d'entrees imprimees par chacun des 2 journaux d'execution (premiere_execution/cote2.log, replication/cote2.stdout.log) = fichiers actuels
OK    G6 cote 2 : R^-1 [[Hf, Hl], [0, Hc]] entiere et |det| egaux : meme reseau M (bijection I <-> (u, y) dans Z^44 x Z^44)
OK    G6 cote 2 : A.gram = DA Hc~ QC Hc (DA = 139)
OK    G6 cote 2 : B.gram = DB Hf~ QF Hf (DB = 1)
OK    G6 cote 2 : Hf Tn = d Hl (d = 278) : coordonnees de fibre du relevement = Tn u / d
OK    G6 cote 2 : reseau de fibre Hf Z^44 = 2 nu O+ (meme reseau colonne)
OK    G7 (6 - 1057/200)^2 < 45/88, soit 6 (1 - sqrt(5/352)) < 1057/200 ; et 3*6/4 <= 1057/200
OK    G8 rotation zeta sur les coordonnees de I : matrice entiere, Rot~ GRAM Rot = GRAM
      vecteur 0 : N = 932369588 ; max |f| = 898929894.4460 >= N sqrt(5/352) = 111122440.1885
      vecteur 1 : N = 9606177320 ; max |f| = 8682167223.0144 >= N sqrt(5/352) = 1144891337.5349
      vecteur 2 : N = 11659059782 ; max |f| = 11350226615.7122 >= N sqrt(5/352) = 1389559665.9894
OK    G8 sur 3 vecteurs : Lambda(a_k) + Lambda'(b_k) = 2N, somme a cinq termes nulle, Parseval, max |f| >= N sqrt(5/352)
OK    G9 le point (u, y) fourni est dans I : coordonnees entieres dans BASE
OK    G9 x~ GRAM x = 8 : vecteur de norme 8 exhibe (min <= 8)
      x (base de I) = [364, 288, -46, -21, -61, -60, -40, -20, -2, -19, -23, -53, -23, -49, -20, -6, 10, -2, -19, -15, -2, -8, -54, -34, -44, -33, -35, -31, 16, -4, -37, -63, -10, -20, -8, -12, 19, 23, 4, 3, 7, 26, -34, -31, -21, 20, 15, -4, 23, 34, -9, -47, 11, 15, 20, 3, 18, 45, 26, 27, 6, 27, -21, -14, -26, 36, 44, 30, 7, 27, 16, -18, 11, 25, 40, 30, -41, -3, 0, -48, -2, -10, 8, -31, -68, 31, -13, -12]
      z (puissances de zeta, degre 0..87) = [-108, -13, -2, 8, 10, -81, 4, 16, 21, 19, -72, 27, 23, 42, 18, -73, 22, 7, 42, 7, -81, 11, -12, -89, -12, -98, 30, -2, -56, 15, -83, 59, 23, -22, 68, -45, 94, 45, -21, 84, -52, 104, 45, -40, 66, -89, -46, 8, -71, 59, -98, -54, 13, -85, 71, -75, -34, 63, -57, 99, -53, -21, 92, -32, 119, -31, -31, 79, -48, -21, -51, -53, 73, -63, -34, -62, -63, 67, -45, -31, -35, -47, 82, -21, -14, -1, -18, 109]
BILAN : 37 controles, 0 echecs
FIN_OK
==== code de sortie 0

==== python -I -B code/verification/verifier_recus.py P139
== R1 source et classes
   9e467c750470301ec0612c087b84636da6b46538a0fe33458970af6cb97bc3c5  code/certifiant/Rang88CertZ.java
OK    R1 SHA-256 de Rang88CertZ.java = 9e467c75...c3c5 (empreinte citee par la note)
   9db7355dc8cad2ecfa8056b9bff569642544ebbab23e3db30833fafdda9152a8  code/certifiant/classes/Rang88CertZ$Compteurs.class
   a1ed4ee2f289e88cd440246ce066455ac3fed9d414a0525ab80bdf12342830af  code/certifiant/classes/Rang88CertZ$EnumZ.class
   b7028cb6168c77ed08dd552dcf9760946c7e8bddbb0d245ab4b31fdae8ed6cb9  code/certifiant/classes/Rang88CertZ$FormeZ.class
   5c47eba99fa800f0dbbdf8adb5de1efb5f1a11e08bac5158f97787eb3b2b526b  code/certifiant/classes/Rang88CertZ$Recepteur.class
   5e3b4b4877e242bcd76f202c87929473af00944b277d815d2b0c8cc95f7aa2b3  code/certifiant/classes/Rang88CertZ$Tache.class
   a33c837d37c4d03ac0a064170fb6f853790ae0010e14d5a52e217c47076857e3  code/certifiant/classes/Rang88CertZ$Travail.class
   35130e199599a72f6c65b199a13f0190c6ba0438899594d9a0cea48c38c652e5  code/certifiant/classes/Rang88CertZ.class
   60aed39c3fc32a76da5e61fad04465a45a224edef1dd069cbeabf30961638fc4  code/certifiant/classes/TestCertZ.class
== R7 inventaire du repertoire de sortie de l'execution de reference (data/P139/replication/INVENTAIRE_SORTIE.txt) : preflight.log, science/cote1.ckpt, science/cote1.java.exit, science/cote1.stderr.log, science/cote1.stdout.log, science/cote1.taches, science/cote2.ckpt, science/cote2.java.exit, science/cote2.stderr.log, science/cote2.stdout.log, science/cote2.taches, wrapper.log
OK    R7 aucun fichier de touche (*.touches) dans le repertoire de sortie de l'execution de reference ; les deux recus y figurent
OK    R7 les fichiers conserves dans data/P139/replication/ ont les tailles de l'inventaire
== execution de reference (second ordinateur), cote 1
   JVM : OpenJDK 64-Bit Server VM 21.0.12.1 ; Linux amd64 ; processeurs 8 ; PID 24 ; Mon Oct 12 06:11:59 GMT 2026 ; 8 fils ; 48227 taches ; duree imprimee 12539 s
OK    R2 reference cote 1 : empreintes d'entrees imprimees = fichiers data/P139/entrees/cote1_*
OK    R1 reference cote 1 : empreintes des 7 classes chargees = fichiers code/certifiant/classes/
OK    R1 reference cote 1 : LIEN recalcule = LIEN imprime (entrees=5a88405e32d5ebec10e1a7...)
OK    R3 reference cote 1 : parametres mode=run, BA=1057/200, S=12, F=40, D=6, Dmax=16, seuil=0.2 ; prefixe java_P139/cote1
OK    R3 reference cote 1 : JVM OpenJDK 21 sous Linux
OK    R3 reference cote 1 : un seul en-tete, une seule JVM ; CHECKPOINT nouveau ; aucune ligne REPRISE ; SELECTION 48227/48227 ; A_FAIRE 48227 ; DEJA_AU_CHECKPOINT 0
OK    R3 reference cote 1 : EXECUTEES_CE_LANCEMENT 48227 ; REPRISES_DU_CHECKPOINT 0 ; TACHES_TERMINEES 48227/48227
OK    R3 reference cote 1 : TOTAL_TOUCHES 0 ; une ligne COUVERTURE_COMPLETE 48227/48227 ; CATALOGUE fd9e41bd2b65... ; FIN [12539 s] ; aucune ligne ERREUR, TOUCHE, ARRET
OK    R3 reference cote 1 : code de sortie Java = 0 (cote1.java.exit) ; stderr = la seule ligne d'information de la JVM, sans exception
OK    R4 reference cote 1 : SHA du fichier de recus = CHECKPOINT_SHA256 imprime en fin d'execution (e618553cedaa...)
OK    R4 reference cote 1 : recus en ASCII pur, sans CR, termines par LF
OK    R4 reference cote 1 : en-tete = R88Z_CKPT_V1|parametres|total=48227|catalogue=fd9e41bd2b65...|LIEN du journal
OK    R4 reference cote 1 : 48227 lignes de recu, toutes au format strict
OK    R4 reference cote 1 : indices des recus = permutation de 0..48226 (ni doublon ni lacune)
OK    R4 reference cote 1 : chaque recu a TOUCHES = 0, CVP = U, somme de l'histogramme = U, NA >= 1
OK    R4 reference cote 1 : sommes des recus = totaux du journal : U 42957972 ; CVP 42957972 ; noeuds courts 93388475228 (= recus + 59912 de generation) ; fibre 1023203070978 ; histogramme
OK    R6 reference cote 1 : empreinte canonique des recus (deux calculs distincts) = valeur publiee c99dcf87...5122
      empreinte canonique cote 1 : c99dcf87db02e6b51f448cdb3e51da1f8b0ee4bd782b6b0e78d686bed5575122 ; 48227 recus ; SHA brut e618553cedaac1c54039a9308e12c56bba440cb62c197a46becf5cc6c9fc9693
OK    R5 reference cote 1 : SHA du catalogue data/P139/cote1.taches = CATALOGUE_SHA256 imprime (fd9e41bd2b65...)
OK    R5 cote 1 : en-tete du catalogue coherent ; 48227 lignes au format ; indices 0..48226 dans l'ordre
OK    R5 cote 1 : chaque tache fixe exactement les coordonnees niv+1..43 ; PL >= 0 ; repartition par niveau = journal
OK    R5 cote 1 : prefixes deux a deux incomparables (sous-arbres disjoints)
OK    R5 cote 1 : normalisation de signe : premiere coordonnee non nulle > 0 ; drapeau zero <=> prefixe nul
== execution de reference (second ordinateur), cote 2
   JVM : OpenJDK 64-Bit Server VM 21.0.12.1 ; Linux amd64 ; processeurs 8 ; PID 61 ; Mon Oct 12 09:40:59 GMT 2026 ; 8 fils ; 61174 taches ; duree imprimee 13648 s
OK    R2 reference cote 2 : empreintes d'entrees imprimees = fichiers data/P139/entrees/cote2_*
OK    R1 reference cote 2 : empreintes des 7 classes chargees = fichiers code/certifiant/classes/
OK    R1 reference cote 2 : LIEN recalcule = LIEN imprime (entrees=243f8bb42723c667b3f6d2...)
OK    R3 reference cote 2 : parametres mode=run, BA=1057/200, S=12, F=40, D=6, Dmax=16, seuil=0.2 ; prefixe java_P139/cote2
OK    R3 reference cote 2 : JVM OpenJDK 21 sous Linux
OK    R3 reference cote 2 : un seul en-tete, une seule JVM ; CHECKPOINT nouveau ; aucune ligne REPRISE ; SELECTION 61174/61174 ; A_FAIRE 61174 ; DEJA_AU_CHECKPOINT 0
OK    R3 reference cote 2 : EXECUTEES_CE_LANCEMENT 61174 ; REPRISES_DU_CHECKPOINT 0 ; TACHES_TERMINEES 61174/61174
OK    R3 reference cote 2 : TOTAL_TOUCHES 0 ; une ligne COUVERTURE_COMPLETE 61174/61174 ; CATALOGUE 39e9d80bbf69... ; FIN [13648 s] ; aucune ligne ERREUR, TOUCHE, ARRET
OK    R3 reference cote 2 : code de sortie Java = 0 (cote2.java.exit) ; stderr = la seule ligne d'information de la JVM, sans exception
OK    R4 reference cote 2 : SHA du fichier de recus = CHECKPOINT_SHA256 imprime en fin d'execution (56430bed905b...)
OK    R4 reference cote 2 : recus en ASCII pur, sans CR, termines par LF
OK    R4 reference cote 2 : en-tete = R88Z_CKPT_V1|parametres|total=61174|catalogue=39e9d80bbf69...|LIEN du journal
OK    R4 reference cote 2 : 61174 lignes de recu, toutes au format strict
OK    R4 reference cote 2 : indices des recus = permutation de 0..61173 (ni doublon ni lacune)
OK    R4 reference cote 2 : chaque recu a TOUCHES = 0, CVP = U, somme de l'histogramme = U, NA >= 1
OK    R4 reference cote 2 : sommes des recus = totaux du journal : U 42957972 ; CVP 42957972 ; noeuds courts 90863039900 (= recus + 76342 de generation) ; fibre 1118094663881 ; histogramme
OK    R6 reference cote 2 : empreinte canonique des recus (deux calculs distincts) = valeur publiee 8ab1f40a...daf7
      empreinte canonique cote 2 : 8ab1f40a48c416dd4eab8dde92d0c5866a6ca1951b5edd5d579c5f2ee0bedaf7 ; 61174 recus ; SHA brut 56430bed905b8463374050ed5be70482c3f04373e033a91705185df49b970e7e
OK    R5 reference cote 2 : SHA du catalogue data/P139/cote2.taches = CATALOGUE_SHA256 imprime (39e9d80bbf69...)
OK    R5 cote 2 : en-tete du catalogue coherent ; 61174 lignes au format ; indices 0..61173 dans l'ordre
OK    R5 cote 2 : chaque tache fixe exactement les coordonnees niv+1..43 ; PL >= 0 ; repartition par niveau = journal
OK    R5 cote 2 : prefixes deux a deux incomparables (sous-arbres disjoints)
OK    R5 cote 2 : normalisation de signe : premiere coordonnee non nulle > 0 ; drapeau zero <=> prefixe nul
== premiere execution (premier ordinateur), cote 1
   JVM : OpenJDK 64-Bit Server VM 11.0.16.1 ; Windows 11 amd64 ; processeurs 16 ; PID 13000 ; Sat Oct 10 22:46:08 CEST 2026 ; 6 fils ; duree imprimee 14562 s
OK    R2 premiere cote 1 : empreintes d'entrees imprimees = fichiers data/P139/entrees/cote1_*
OK    R1 premiere cote 1 : empreintes des 7 classes chargees = fichiers code/certifiant/classes/
OK    R1 premiere cote 1 : LIEN recalcule = LIEN imprime (entrees=5a88405e32d5ebec10e1a7...)
OK    R3 premiere cote 1 : parametres mode=run, BA=1057/200, S=12, F=40, D=6, Dmax=16, seuil=0.2 ; prefixe java_P139/cote1
OK    R3 premiere cote 1 : un seul en-tete, une seule JVM ; CHECKPOINT nouveau ; aucune ligne REPRISE ; SELECTION 48227/48227 ; A_FAIRE 48227 ; DEJA_AU_CHECKPOINT 0
OK    R3 premiere cote 1 : EXECUTEES_CE_LANCEMENT 48227 ; REPRISES_DU_CHECKPOINT 0 ; TACHES_TERMINEES 48227/48227
OK    R3 premiere cote 1 : TOTAL_TOUCHES 0 ; une ligne COUVERTURE_COMPLETE 48227/48227 ; CATALOGUE fd9e41bd2b65... ; FIN [14562 s] ; aucune ligne ERREUR, TOUCHE, ARRET
OK    R8 premiere cote 1 : stderr vide
OK    R4 premiere cote 1 : SHA du fichier de recus = CHECKPOINT_SHA256 imprime en fin d'execution (c32d099d0f74...)
OK    R4 premiere cote 1 : recus en ASCII pur, sans CR, termines par LF
OK    R4 premiere cote 1 : en-tete = R88Z_CKPT_V1|parametres|total=48227|catalogue=fd9e41bd2b65...|LIEN du journal
OK    R4 premiere cote 1 : 48227 lignes de recu, toutes au format strict
OK    R4 premiere cote 1 : indices des recus = permutation de 0..48226 (ni doublon ni lacune)
OK    R4 premiere cote 1 : chaque recu a TOUCHES = 0, CVP = U, somme de l'histogramme = U, NA >= 1
OK    R4 premiere cote 1 : sommes des recus = totaux du journal : U 42957972 ; CVP 42957972 ; noeuds courts 93388475228 (= recus + 59912 de generation) ; fibre 1023203070978 ; histogramme
OK    R6 premiere cote 1 : empreinte canonique des recus (deux calculs distincts) = valeur publiee c99dcf87...5122
      empreinte canonique cote 1 : c99dcf87db02e6b51f448cdb3e51da1f8b0ee4bd782b6b0e78d686bed5575122 ; 48227 recus ; SHA brut c32d099d0f74af3239d4d382a762f134ff3ba46bd4d2ba2f2d580fd25fc9dbec
OK    R8 premiere cote 1 : JVM OpenJDK 11.0.16.1 sous Windows
OK    R5 premiere cote 1 : SHA du catalogue data/P139/cote1.taches = CATALOGUE_SHA256 imprime (fd9e41bd2b65...)
OK    R6 premiere cote 1 : memes recus que l'execution de reference (ensembles de lignes egaux)
== premiere execution (premier ordinateur), cote 2
   JVM : OpenJDK 64-Bit Server VM 11.0.16.1 ; Windows 11 amd64 ; processeurs 16 ; PID 6464 ; Sun Oct 11 02:48:51 CEST 2026 ; 6 fils ; duree imprimee 15856 s
OK    R2 premiere cote 2 : empreintes d'entrees imprimees = fichiers data/P139/entrees/cote2_*
OK    R1 premiere cote 2 : empreintes des 7 classes chargees = fichiers code/certifiant/classes/
OK    R1 premiere cote 2 : LIEN recalcule = LIEN imprime (entrees=243f8bb42723c667b3f6d2...)
OK    R3 premiere cote 2 : parametres mode=run, BA=1057/200, S=12, F=40, D=6, Dmax=16, seuil=0.2 ; prefixe java_P139/cote2
OK    R3 premiere cote 2 : un seul en-tete, une seule JVM ; CHECKPOINT nouveau ; aucune ligne REPRISE ; SELECTION 61174/61174 ; A_FAIRE 61174 ; DEJA_AU_CHECKPOINT 0
OK    R3 premiere cote 2 : EXECUTEES_CE_LANCEMENT 61174 ; REPRISES_DU_CHECKPOINT 0 ; TACHES_TERMINEES 61174/61174
OK    R3 premiere cote 2 : TOTAL_TOUCHES 0 ; une ligne COUVERTURE_COMPLETE 61174/61174 ; CATALOGUE 39e9d80bbf69... ; FIN [15856 s] ; aucune ligne ERREUR, TOUCHE, ARRET
OK    R8 premiere cote 2 : stderr vide
OK    R4 premiere cote 2 : SHA du fichier de recus = CHECKPOINT_SHA256 imprime en fin d'execution (6f556f1a0e0b...)
OK    R4 premiere cote 2 : recus en ASCII pur, sans CR, termines par LF
OK    R4 premiere cote 2 : en-tete = R88Z_CKPT_V1|parametres|total=61174|catalogue=39e9d80bbf69...|LIEN du journal
OK    R4 premiere cote 2 : 61174 lignes de recu, toutes au format strict
OK    R4 premiere cote 2 : indices des recus = permutation de 0..61173 (ni doublon ni lacune)
OK    R4 premiere cote 2 : chaque recu a TOUCHES = 0, CVP = U, somme de l'histogramme = U, NA >= 1
OK    R4 premiere cote 2 : sommes des recus = totaux du journal : U 42957972 ; CVP 42957972 ; noeuds courts 90863039900 (= recus + 76342 de generation) ; fibre 1118094663881 ; histogramme
OK    R6 premiere cote 2 : empreinte canonique des recus (deux calculs distincts) = valeur publiee 8ab1f40a...daf7
      empreinte canonique cote 2 : 8ab1f40a48c416dd4eab8dde92d0c5866a6ca1951b5edd5d579c5f2ee0bedaf7 ; 61174 recus ; SHA brut 6f556f1a0e0be35b805629432beb3dd03cccbf5d0d2ae5ddfc68285cc394fd24
OK    R8 premiere cote 2 : JVM OpenJDK 11.0.16.1 sous Windows
OK    R5 premiere cote 2 : SHA du catalogue data/P139/cote2.taches = CATALOGUE_SHA256 imprime (39e9d80bbf69...)
OK    R6 premiere cote 2 : memes recus que l'execution de reference (ensembles de lignes egaux)
== R9 coherence
OK    R9 meme COMPTE_U (42957972) et meme histogramme pour les deux cotes et les deux executions
   plus grand compteur d'un recu = 1130711327 (< 2^31) ; plus grand total de noeuds d'une execution = 1208957703781 (< 2^41)
OK    R9 (Z9) tous les compteurs des recus et tous les totaux sont < 2^43, loin de 2^63
BILAN : 87 controles, 0 echecs
FIN_OK
==== code de sortie 0

==== python -I -B code/verification/verifier_classe_P139.py
certificat : data/P139/certificat_K22.txt SHA-256 4ad7bbfdd9fc171d4657513ec8a60810703a1d68e00c0c5d001a8fee574eb09d
OK    P22 unitaire de degre 22
OK    Phi_115 de degre 88, unitaire
OK    (C1) P22(theta) = 0 dans Z[zeta_115], theta = zeta + zeta^22 + zeta^24 + zeta^68
OK    (C1) {1,22,24,68} est un sous-groupe de (Z/115)^*, stabilisateur de theta (base normale : 115 sans facteur carre)
OK    BASE de I_data.gp : 88 x 88
OK    I mod 139 est engendre par un facteur g de degre 2 de Phi_115 mod 139 (P de degre residuel 2)
OK    theta mod P est dans F_139 (q = P inter K de degre 1, f(P/q) = 2)
      theta = 0 mod P ; RACINE du certificat = 0
OK    la racine du certificat est celle du premier P de I_data.gp
OK    (C1) P22 a 22 racines simples modulo 139 (139 totalement decompose dans K, Z[theta] maximal en 139)
OK    (C2) XI_2 entier algebrique de norme +-1 (unite de K)
OK    (C2) XI_3 entier algebrique de norme +-1 (unite de K)
OK    (C2) XI_4 entier algebrique de norme +-1 (unite de K)
OK    (C2) XI_5 entier algebrique de norme +-1 (unite de K)
OK    (C2) XI_6 entier algebrique de norme +-1 (unite de K)
OK    (C2) XI_7 entier algebrique de norme +-1 (unite de K)
OK    (C2) XI_8 entier algebrique de norme +-1 (unite de K)
OK    (C2) XI_9 entier algebrique de norme +-1 (unite de K)
OK    (C2) XI_10 entier algebrique de norme +-1 (unite de K)
OK    (C2) XI_11 entier algebrique de norme +-1 (unite de K)
OK    (C2) GAMMA entier algebrique
OK    (C2) |N(GAMMA)| = 139^331
      valuations de GAMMA aux 22 premiers au-dessus de 139 : [(0, 331), (1, 0), (4, 0), (11, 0), (12, 0), (26, 0), (29, 0), (35, 0), (36, 0), (43, 0), (60, 0), (63, 0), (76, 0), (79, 0), (96, 0), (103, 0), (104, 0), (110, 0), (113, 0), (127, 0), (128, 0), (135, 0)]
OK    (C2) v_q(GAMMA) = 331 en q = (139, theta - RACINE) et 0 aux 21 autres : (GAMMA) = q^331
      l = 380651 : 22 racines simples de P22, rang des 10 colonnes d'unites = 10, rang total = 10
      l = 1065821 : 22 racines simples de P22, rang des 10 colonnes d'unites = 10, rang total = 11
      l = 1522601 : 22 racines simples de P22, rang des 10 colonnes d'unites = 10, rang total = 11
      premiers l utilises : [380651, 1065821, 1522601] ; matrice 66 x 11 ; rang(unites) = 10 ; rang(unites, GAMMA) = 11
OK    (C3) les 10 unites XI_a sont independantes modulo les puissances 331-iemes (rang 10)
OK    (C3) GAMMA n'est pas dans <unites> . K^{*331} (rang 11)
BILAN : 24 controles, 0 echecs
CONCLUSION (preuve : note, par. 6.4, prop. 6.6) : q^6 n'est pas principal dans K22, donc P139^3 n'est pas principal dans Q(zeta_115). SANS GRH.
==== code de sortie 0

==== python -I -B code/verification/verifier_raccord.py P599
candidat P599
I_data.gp SHA-256 19b69c8ecbd8ad256b02afc0717e92898f3d4438f92ff863498139a041922692 ; PREMIERS = [[599, 2, 1]] ; Q = 358801
OK    dimensions : BASE, GRAM, AB 88 x 88 ; NU, ALPHA de degre <= 43 ; Q = 599^2
OK    G1 |det BASE| = 599^2 (indice de I dans Z[zeta])
OK    G1 zeta * I contenu dans I (I est un ideal de Z[zeta_115])
OK    G1 I mod 599 = (g), g unitaire de degre 2 divisant Phi_115 mod 599
OK    G1 g irreductible mod 599 (discriminant non residu)
OK    G1 599 dans I et g(zeta) dans I : I = (599, g(zeta)), premier de degre residuel 2
OK    G1 I different de son conjugue (g* != g), donc I + Ibar = O_L
      g = y^2 + 87 y + 322 ; g* = y^2 + 523 y + 426 (mod 599)
OK    G2 alpha reel : Tr(alpha zeta^k) = Tr(alpha zeta^-k)
OK    G2 BASE~ H BASE = GRAM (H recalculee depuis ALPHA), entiere
OK    G2 GRAM symetrique et paire
OK    G2 GRAM definie positive (88 mineurs principaux dominants > 0, exact)
OK    G2 det GRAM = 1
      diagonale de GRAM : min 1353466, max 2238300454
OK    G3 nu dans I (donc dans I inter Ibar = I Ibar, nu etant reel)
OK    G3 Pm(c) = 0 dans Z[zeta], Pm unitaire de degre 44 (polynome minimal de c = zeta + 1/zeta)
OK    G3 N_{L+/Q}(nu) = 599^2 = N(I) : (nu) O_L = I Ibar
OK    G4 pour les 88 vecteurs de base z de I : z + zbar = a(c), z - zbar = e b(c), (b ; a) = colonne de AB
OK    G4 |det AB| = 2^44 * 599^2
OK    G5 AB~ diag(QB, QA) AB / 2 = GRAM : N(z) = (Lambda(a) + Lambda'(b)) / 2 sur tout I
OK    G5 QA (denominateur commun 599) definie positive, det = 1/599^2
OK    G5 QB (denominateur commun 599) definie positive, det = 1/599^2
      SHA-256 5ec6165d2cf7d3e41bb3835cc3a0ceb56637de19c81957d7bef15a3b720ff85a  cote1_A.gram
      SHA-256 76ec26aa8c107272828f55155f00b9fba73c83081bcaa8798abe6a5e87eeb215  cote1_B.gram
      SHA-256 c2d5344208e2cf6038cb76aa2e83f85fe6db5ec4ede64dcbc3492e5027fac09c  cote1_T.mat
      SHA-256 53e836f17bbfe5c938257f0905eda20a357d3b4a1f16818517714a031a82088b  cote1_meta.txt
      SHA-256 baff8ec7f36a2e396bd1d998059588627ea9bc9836313b3a41987c1d5045e540  cote1_bases.gp
OK    G6 cote 1 : les 4 empreintes d'entrees imprimees par chacun des 3 journaux d'execution (premiere_execution/cote1_lancement1.log, premiere_execution/cote1_lancement2.log, replication/cote1.stdout.log) = fichiers actuels
OK    G6 cote 1 : R^-1 [[Hf, Hl], [0, Hc]] entiere et |det| egaux : meme reseau M (bijection I <-> (u, y) dans Z^44 x Z^44)
OK    G6 cote 1 : A.gram = DA Hc~ QC Hc (DA = 599)
OK    G6 cote 1 : B.gram = DB Hf~ QF Hf (DB = 1)
OK    G6 cote 1 : Hf Tn = d Hl (d = 1198) : coordonnees de fibre du relevement = Tn u / d
OK    G6 cote 1 : reseau de fibre Hf Z^44 = 2 nu O+ (meme reseau colonne)
      SHA-256 b35977a38d074f9eef8500710525eb801b9b18a88c5a86634ff6219c28c81070  cote2_A.gram
      SHA-256 ebc6e5a53569c942dac64b863869c6a001c4a7237c5f3020e1ae12e455d92366  cote2_B.gram
      SHA-256 46bcab7a32c75846e78bad0413880758b1339e9af6c6e6ddfb682aa669e9b9a0  cote2_T.mat
      SHA-256 53e836f17bbfe5c938257f0905eda20a357d3b4a1f16818517714a031a82088b  cote2_meta.txt
      SHA-256 311ba349fe998383fa45e5cc1a4e48c56147027c06cb64455d9561f89d5d0b40  cote2_bases.gp
OK    G6 cote 2 : les 4 empreintes d'entrees imprimees par chacun des 2 journaux d'execution (premiere_execution/cote2.log, replication/cote2.stdout.log) = fichiers actuels
OK    G6 cote 2 : R^-1 [[Hf, Hl], [0, Hc]] entiere et |det| egaux : meme reseau M (bijection I <-> (u, y) dans Z^44 x Z^44)
OK    G6 cote 2 : A.gram = DA Hc~ QC Hc (DA = 599)
OK    G6 cote 2 : B.gram = DB Hf~ QF Hf (DB = 1)
OK    G6 cote 2 : Hf Tn = d Hl (d = 1198) : coordonnees de fibre du relevement = Tn u / d
OK    G6 cote 2 : reseau de fibre Hf Z^44 = 2 nu O+ (meme reseau colonne)
OK    G7 (6 - 1057/200)^2 < 45/88, soit 6 (1 - sqrt(5/352)) < 1057/200 ; et 3*6/4 <= 1057/200
OK    G8 rotation zeta sur les coordonnees de I : matrice entiere, Rot~ GRAM Rot = GRAM
      vecteur 0 : N = 20022782720 ; max |f| = 17426050908.2337 >= N sqrt(5/352) = 2386371782.0141
      vecteur 1 : N = 6125474902 ; max |f| = 5896036717.7513 >= N sqrt(5/352) = 730051395.0525
      vecteur 2 : N = 31544851328 ; max |f| = 29169432908.3172 >= N sqrt(5/352) = 3759604453.0703
OK    G8 sur 3 vecteurs : Lambda(a_k) + Lambda'(b_k) = 2N, somme a cinq termes nulle, Parseval, max |f| >= N sqrt(5/352)
OK    G9 le point (u, y) fourni est dans I : coordonnees entieres dans BASE
OK    G9 x~ GRAM x = 8 : vecteur de norme 8 exhibe (min <= 8)
      x (base de I) = [78, -110, -42, -66, -8, 23, 95, 8, -9, -75, -11, 9, 36, -3, -44, 0, 20, 105, 50, 20, -59, -35, -32, -36, -4, 11, 58, -5, -1, -54, -4, 19, 13, -29, -70, 0, 21, 110, 44, 14, -78, -39, -17, -17, -15, -18, 30, -15, 19, -32, -1, 15, 15, -28, -73, 3, 29, 116, 31, 8, -94, -48, -21, -10, -32, -57, -17, -36, 36, -6, 9, 3, 12, -23, -45, 18, 44, 112, 27, 4, -65, 10, -23, 7, 5, -31, -44, 69]
      z (puissances de zeta, degre 0..87) = [-13, -12, -9, 5, 20, -24, -8, -1, -18, 21, -43, -19, 19, -16, 29, -59, -36, 36, -19, 40, -30, -30, 69, -22, 19, -40, -38, 105, -31, 7, -19, -64, 110, -35, -22, 3, -63, 116, -44, -61, 29, -58, 108, -19, -79, 45, -42, 91, -7, -79, 85, -32, 54, 0, -105, 79, -17, 26, 3, -108, 66, -21, -21, 13, -80, 58, 7, -35, 4, -66, 39, 9, -35, 24, -36, 26, 19, -35, 18, -17, 16, 15, -32, 12, -10, -5, 3, -17]
BILAN : 37 controles, 0 echecs
FIN_OK
==== code de sortie 0

==== python -I -B code/verification/verifier_recus.py P599
== R1 source et classes
   9e467c750470301ec0612c087b84636da6b46538a0fe33458970af6cb97bc3c5  code/certifiant/Rang88CertZ.java
OK    R1 SHA-256 de Rang88CertZ.java = 9e467c75...c3c5 (empreinte citee par la note)
   9db7355dc8cad2ecfa8056b9bff569642544ebbab23e3db30833fafdda9152a8  code/certifiant/classes/Rang88CertZ$Compteurs.class
   a1ed4ee2f289e88cd440246ce066455ac3fed9d414a0525ab80bdf12342830af  code/certifiant/classes/Rang88CertZ$EnumZ.class
   b7028cb6168c77ed08dd552dcf9760946c7e8bddbb0d245ab4b31fdae8ed6cb9  code/certifiant/classes/Rang88CertZ$FormeZ.class
   5c47eba99fa800f0dbbdf8adb5de1efb5f1a11e08bac5158f97787eb3b2b526b  code/certifiant/classes/Rang88CertZ$Recepteur.class
   5e3b4b4877e242bcd76f202c87929473af00944b277d815d2b0c8cc95f7aa2b3  code/certifiant/classes/Rang88CertZ$Tache.class
   a33c837d37c4d03ac0a064170fb6f853790ae0010e14d5a52e217c47076857e3  code/certifiant/classes/Rang88CertZ$Travail.class
   35130e199599a72f6c65b199a13f0190c6ba0438899594d9a0cea48c38c652e5  code/certifiant/classes/Rang88CertZ.class
   60aed39c3fc32a76da5e61fad04465a45a224edef1dd069cbeabf30961638fc4  code/certifiant/classes/TestCertZ.class
== R7 inventaire du repertoire de sortie de l'execution de reference (data/P599/replication/INVENTAIRE_SORTIE.txt) : preflight.log, science/cote1.ckpt, science/cote1.java.exit, science/cote1.stderr.log, science/cote1.stdout.log, science/cote1.taches, science/cote2.ckpt, science/cote2.java.exit, science/cote2.stderr.log, science/cote2.stdout.log, science/cote2.taches, wrapper.log
OK    R7 aucun fichier de touche (*.touches) dans le repertoire de sortie de l'execution de reference ; les deux recus y figurent
OK    R7 les fichiers conserves dans data/P599/replication/ ont les tailles de l'inventaire
== execution de reference (second ordinateur), cote 1
   JVM : OpenJDK 64-Bit Server VM 21.0.12.1 ; Linux amd64 ; processeurs 14 ; PID 24 ; Mon Oct 12 15:34:28 GMT 2026 ; 14 fils ; 59255 taches ; duree imprimee 26212 s
OK    R2 reference cote 1 : empreintes d'entrees imprimees = fichiers data/P599/entrees/cote1_*
OK    R1 reference cote 1 : empreintes des 7 classes chargees = fichiers code/certifiant/classes/
OK    R1 reference cote 1 : LIEN recalcule = LIEN imprime (entrees=149502ab6fb0a89c7cb0a6...)
OK    R3 reference cote 1 : parametres mode=run, BA=1057/200, S=12, F=40, D=6, Dmax=16, seuil=0.2 ; prefixe java_P599/cote1
OK    R3 reference cote 1 : JVM OpenJDK 21 sous Linux
OK    R3 reference cote 1 : un seul en-tete, une seule JVM ; CHECKPOINT nouveau ; aucune ligne REPRISE ; SELECTION 59255/59255 ; A_FAIRE 59255 ; DEJA_AU_CHECKPOINT 0
OK    R3 reference cote 1 : EXECUTEES_CE_LANCEMENT 59255 ; REPRISES_DU_CHECKPOINT 0 ; TACHES_TERMINEES 59255/59255
OK    R3 reference cote 1 : TOTAL_TOUCHES 0 ; une ligne COUVERTURE_COMPLETE 59255/59255 ; CATALOGUE b9ff8375cdbb... ; FIN [26212 s] ; aucune ligne ERREUR, TOUCHE, ARRET
OK    R3 reference cote 1 : code de sortie Java = 0 (cote1.java.exit) ; stderr = la seule ligne d'information de la JVM, sans exception
OK    R4 reference cote 1 : SHA du fichier de recus = CHECKPOINT_SHA256 imprime en fin d'execution (c705a72bef5f...)
OK    R4 reference cote 1 : recus en ASCII pur, sans CR, termines par LF
OK    R4 reference cote 1 : en-tete = R88Z_CKPT_V1|parametres|total=59255|catalogue=b9ff8375cdbb...|LIEN du journal
OK    R4 reference cote 1 : 59255 lignes de recu, toutes au format strict
OK    R4 reference cote 1 : indices des recus = permutation de 0..59254 (ni doublon ni lacune)
OK    R4 reference cote 1 : chaque recu a TOUCHES = 0, CVP = U, somme de l'histogramme = U, NA >= 1
OK    R4 reference cote 1 : sommes des recus = totaux du journal : U 185794630 ; CVP 185794630 ; noeuds courts 210988560353 (= recus + 72906 de generation) ; fibre 3167158293042 ; histogramme
OK    R6 reference cote 1 : empreinte canonique des recus (deux calculs distincts) = valeur publiee f3cf379a...2689
      empreinte canonique cote 1 : f3cf379ad157b1595f9ad96c38d3734a920ea24de3afc5d12dfa617bb3e42689 ; 59255 recus ; SHA brut c705a72bef5f98db8745c98e34a57a660c67734b2b75911235c10ae4bb54f59a
OK    R5 reference cote 1 : SHA du catalogue data/P599/cote1.taches = CATALOGUE_SHA256 imprime (b9ff8375cdbb...)
OK    R5 cote 1 : en-tete du catalogue coherent ; 59255 lignes au format ; indices 0..59254 dans l'ordre
OK    R5 cote 1 : chaque tache fixe exactement les coordonnees niv+1..43 ; PL >= 0 ; repartition par niveau = journal
OK    R5 cote 1 : prefixes deux a deux incomparables (sous-arbres disjoints)
OK    R5 cote 1 : normalisation de signe : premiere coordonnee non nulle > 0 ; drapeau zero <=> prefixe nul
== execution de reference (second ordinateur), cote 2
   JVM : OpenJDK 64-Bit Server VM 21.0.12.1 ; Linux amd64 ; processeurs 14 ; PID 71 ; Mon Oct 12 22:51:21 GMT 2026 ; 14 fils ; 74398 taches ; duree imprimee 25956 s
OK    R2 reference cote 2 : empreintes d'entrees imprimees = fichiers data/P599/entrees/cote2_*
OK    R1 reference cote 2 : empreintes des 7 classes chargees = fichiers code/certifiant/classes/
OK    R1 reference cote 2 : LIEN recalcule = LIEN imprime (entrees=a5ecee940befacee9feec8...)
OK    R3 reference cote 2 : parametres mode=run, BA=1057/200, S=12, F=40, D=6, Dmax=16, seuil=0.2 ; prefixe java_P599/cote2
OK    R3 reference cote 2 : JVM OpenJDK 21 sous Linux
OK    R3 reference cote 2 : un seul en-tete, une seule JVM ; CHECKPOINT nouveau ; aucune ligne REPRISE ; SELECTION 74398/74398 ; A_FAIRE 74398 ; DEJA_AU_CHECKPOINT 0
OK    R3 reference cote 2 : EXECUTEES_CE_LANCEMENT 74398 ; REPRISES_DU_CHECKPOINT 0 ; TACHES_TERMINEES 74398/74398
OK    R3 reference cote 2 : TOTAL_TOUCHES 0 ; une ligne COUVERTURE_COMPLETE 74398/74398 ; CATALOGUE a97cb23d0b7c... ; FIN [25956 s] ; aucune ligne ERREUR, TOUCHE, ARRET
OK    R3 reference cote 2 : code de sortie Java = 0 (cote2.java.exit) ; stderr = la seule ligne d'information de la JVM, sans exception
OK    R4 reference cote 2 : SHA du fichier de recus = CHECKPOINT_SHA256 imprime en fin d'execution (9268d23dfbee...)
OK    R4 reference cote 2 : recus en ASCII pur, sans CR, termines par LF
OK    R4 reference cote 2 : en-tete = R88Z_CKPT_V1|parametres|total=74398|catalogue=a97cb23d0b7c...|LIEN du journal
OK    R4 reference cote 2 : 74398 lignes de recu, toutes au format strict
OK    R4 reference cote 2 : indices des recus = permutation de 0..74397 (ni doublon ni lacune)
OK    R4 reference cote 2 : chaque recu a TOUCHES = 0, CVP = U, somme de l'histogramme = U, NA >= 1
OK    R4 reference cote 2 : sommes des recus = totaux du journal : U 185794630 ; CVP 185794630 ; noeuds courts 240413424839 (= recus + 91026 de generation) ; fibre 3094115348574 ; histogramme
OK    R6 reference cote 2 : empreinte canonique des recus (deux calculs distincts) = valeur publiee b9c93a83...8ef6
      empreinte canonique cote 2 : b9c93a83d2b370fad5de5b3d0edc317718ebe4900960642ef98f72c219458ef6 ; 74398 recus ; SHA brut 9268d23dfbee058c42bc5697f50490f84f6e7d13aa0122d9b221bc3e35ba7ad4
OK    R5 reference cote 2 : SHA du catalogue data/P599/cote2.taches = CATALOGUE_SHA256 imprime (a97cb23d0b7c...)
OK    R5 cote 2 : en-tete du catalogue coherent ; 74398 lignes au format ; indices 0..74397 dans l'ordre
OK    R5 cote 2 : chaque tache fixe exactement les coordonnees niv+1..43 ; PL >= 0 ; repartition par niveau = journal
OK    R5 cote 2 : prefixes deux a deux incomparables (sous-arbres disjoints)
OK    R5 cote 2 : normalisation de signe : premiere coordonnee non nulle > 0 ; drapeau zero <=> prefixe nul
== premiere execution (premier ordinateur), cote 1
   JVM : OpenJDK 64-Bit Server VM 11.0.16.1 ; Windows 11 amd64 ; processeurs 16 ; PID 21912 ; Sun Oct 11 07:15:57 CEST 2026 ; 6 fils
OK    R2 premiere cote 1, lancement 1 : empreintes d'entrees imprimees = fichiers data/P599/entrees/cote1_*
OK    R1 premiere cote 1, lancement 1 : empreintes des 7 classes chargees = fichiers code/certifiant/classes/
OK    R1 premiere cote 1, lancement 1 : LIEN recalcule = LIEN imprime (entrees=149502ab6fb0a89c7cb0a6...)
OK    R3 premiere cote 1, lancement 1 : parametres mode=run, BA=1057/200, S=12, F=40, D=6, Dmax=16, seuil=0.2 ; prefixe java_P599/cote1
OK    R8 premiere cote 1, lancement 1 : stderr vide
   JVM : OpenJDK 64-Bit Server VM 11.0.16.1 ; Windows 11 amd64 ; processeurs 16 ; PID 10912 ; Sun Oct 11 12:56:17 CEST 2026 ; 10 fils
OK    R2 premiere cote 1, lancement 2 : empreintes d'entrees imprimees = fichiers data/P599/entrees/cote1_*
OK    R1 premiere cote 1, lancement 2 : empreintes des 7 classes chargees = fichiers code/certifiant/classes/
OK    R1 premiere cote 1, lancement 2 : LIEN recalcule = LIEN imprime (entrees=149502ab6fb0a89c7cb0a6...)
OK    R3 premiere cote 1, lancement 2 : parametres mode=run, BA=1057/200, S=12, F=40, D=6, Dmax=16, seuil=0.2 ; prefixe java_P599/cote1
OK    R8 premiere cote 1, lancement 2 : stderr vide
OK    R8 lancement 1 : CHECKPOINT nouveau, SELECTION 59255/59255, puis arret force (aucun bilan, aucune touche ni erreur)
OK    R8 lancement 2 : REPRISE de 21459 recus ; SHA a la lecture = SHA de cote1_avant_reprise.ckpt ; SELECTION 59255/59255 ; A_FAIRE 37796 ; DEJA_AU_CHECKPOINT 21459
OK    R3 premiere cote 1, lancement 2 : TOTAL_TOUCHES 0 ; une ligne COUVERTURE_COMPLETE 59255/59255 ; CATALOGUE b9ff8375cdbb... ; FIN [19765 s] ; aucune ligne ERREUR, TOUCHE, ARRET
OK    R4 premiere cote 1 : SHA du fichier de recus = CHECKPOINT_SHA256 imprime en fin d'execution (044f7b6fdfa2...)
OK    R4 premiere cote 1 : recus en ASCII pur, sans CR, termines par LF
OK    R4 premiere cote 1 : en-tete = R88Z_CKPT_V1|parametres|total=59255|catalogue=b9ff8375cdbb...|LIEN du journal
OK    R4 premiere cote 1 : 59255 lignes de recu, toutes au format strict
OK    R4 premiere cote 1 : indices des recus = permutation de 0..59254 (ni doublon ni lacune)
OK    R4 premiere cote 1 : chaque recu a TOUCHES = 0, CVP = U, somme de l'histogramme = U, NA >= 1
OK    R4 premiere cote 1 : sommes des recus = totaux du journal : U 185794630 ; CVP 185794630 ; noeuds courts 210988560353 (= recus + 72906 de generation) ; fibre 3167158293042 ; histogramme
OK    R6 premiere cote 1 : empreinte canonique des recus (deux calculs distincts) = valeur publiee f3cf379a...2689
      empreinte canonique cote 1 : f3cf379ad157b1595f9ad96c38d3734a920ea24de3afc5d12dfa617bb3e42689 ; 59255 recus ; SHA brut 044f7b6fdfa234ed9b1869253afcb402b4dd91b4c4650970d88d084af17218a2
OK    R8 reprise : cote1_avant_reprise.ckpt est, octet pour octet, le debut du fichier final ; pas de ligne tronquee
OK    R8 reprise : 21459 indices repris et 37796 executes ensuite, disjoints, de reunion 0..59254
OK    R8 rejeu : la liste des taches rejouees est exactement l'ensemble des 21459 indices repris
OK    R8 rejeu : meme en-tete que les recus d'origine (memes parametres, catalogue, entrees, classes)
OK    R8 rejeu : les 21459 recus rejoues sont identiques octet pour octet a ceux d'avant reprise (comparaison par indice)
OK    R8 rejeu : ces 21459 recus figurent aussi, a l'identique, dans le fichier final
      SHA du fichier de rejeu ba14ba4fb3ed7e321d5e111fd125ec3ade6e9c033791ee6d2c1b191b30890cc9 ; SHA du fichier d'avant reprise c4c66b0ce1fbb5c8c6bc36eda5273375277554dd6dd317b52a512c7ed10fe9d4
OK    R8 premiere cote 1 : JVM OpenJDK 11.0.16.1 sous Windows
OK    R5 premiere cote 1 : SHA du catalogue data/P599/cote1.taches = CATALOGUE_SHA256 imprime (b9ff8375cdbb...)
OK    R6 premiere cote 1 : memes recus que l'execution de reference (ensembles de lignes egaux)
== premiere execution (premier ordinateur), cote 2
   JVM : OpenJDK 64-Bit Server VM 11.0.16.1 ; Windows 11 amd64 ; processeurs 16 ; PID 27036 ; Sun Oct 11 18:25:43 CEST 2026 ; 10 fils ; duree imprimee 34114 s
OK    R2 premiere cote 2 : empreintes d'entrees imprimees = fichiers data/P599/entrees/cote2_*
OK    R1 premiere cote 2 : empreintes des 7 classes chargees = fichiers code/certifiant/classes/
OK    R1 premiere cote 2 : LIEN recalcule = LIEN imprime (entrees=a5ecee940befacee9feec8...)
OK    R3 premiere cote 2 : parametres mode=run, BA=1057/200, S=12, F=40, D=6, Dmax=16, seuil=0.2 ; prefixe java_P599/cote2
OK    R3 premiere cote 2 : un seul en-tete, une seule JVM ; CHECKPOINT nouveau ; aucune ligne REPRISE ; SELECTION 74398/74398 ; A_FAIRE 74398 ; DEJA_AU_CHECKPOINT 0
OK    R3 premiere cote 2 : EXECUTEES_CE_LANCEMENT 74398 ; REPRISES_DU_CHECKPOINT 0 ; TACHES_TERMINEES 74398/74398
OK    R3 premiere cote 2 : TOTAL_TOUCHES 0 ; une ligne COUVERTURE_COMPLETE 74398/74398 ; CATALOGUE a97cb23d0b7c... ; FIN [34114 s] ; aucune ligne ERREUR, TOUCHE, ARRET
OK    R8 premiere cote 2 : stderr vide
OK    R4 premiere cote 2 : SHA du fichier de recus = CHECKPOINT_SHA256 imprime en fin d'execution (55c55c86e7a0...)
OK    R4 premiere cote 2 : recus en ASCII pur, sans CR, termines par LF
OK    R4 premiere cote 2 : en-tete = R88Z_CKPT_V1|parametres|total=74398|catalogue=a97cb23d0b7c...|LIEN du journal
OK    R4 premiere cote 2 : 74398 lignes de recu, toutes au format strict
OK    R4 premiere cote 2 : indices des recus = permutation de 0..74397 (ni doublon ni lacune)
OK    R4 premiere cote 2 : chaque recu a TOUCHES = 0, CVP = U, somme de l'histogramme = U, NA >= 1
OK    R4 premiere cote 2 : sommes des recus = totaux du journal : U 185794630 ; CVP 185794630 ; noeuds courts 240413424839 (= recus + 91026 de generation) ; fibre 3094115348574 ; histogramme
OK    R6 premiere cote 2 : empreinte canonique des recus (deux calculs distincts) = valeur publiee b9c93a83...8ef6
      empreinte canonique cote 2 : b9c93a83d2b370fad5de5b3d0edc317718ebe4900960642ef98f72c219458ef6 ; 74398 recus ; SHA brut 55c55c86e7a0d1779fea69cdcac6d777025e4362e88434d25a1ad886539476e8
OK    R8 premiere cote 2 : JVM OpenJDK 11.0.16.1 sous Windows
OK    R5 premiere cote 2 : SHA du catalogue data/P599/cote2.taches = CATALOGUE_SHA256 imprime (a97cb23d0b7c...)
OK    R6 premiere cote 2 : memes recus que l'execution de reference (ensembles de lignes egaux)
== R9 coherence
OK    R9 meme COMPTE_U (185794630) et meme histogramme pour les deux cotes et les deux executions
   plus grand compteur d'un recu = 3424899791 (< 2^32) ; plus grand total de noeuds d'une execution = 3378146853395 (< 2^42)
OK    R9 (Z9) tous les compteurs des recus et tous les totaux sont < 2^43, loin de 2^63
BILAN : 98 controles, 0 echecs
FIN_OK
==== code de sortie 0

==== python -I -B code/verification/verifier_classe_P599.py
certificat : data/P599/certificat_K22.txt SHA-256 b05cad287e3b667a72447d09dc1e771980669271f653bdcecf5999023a5d9101
ideal      : data/P599/entrees/I_data.gp SHA-256 19b69c8ecbd8ad256b02afc0717e92898f3d4438f92ff863498139a041922692
OK    P22 unitaire de degre 22
OK    T du certificat dans {1, 2} ; 599 et 331 premiers (divisions exhaustives)
      denominateurs des coordonnees du certificat (base 1, w, ..., w^21) : [1, 28657]
OK    Phi_115 de degre 88, unitaire
OK    (I1) P22(theta) = 0 dans Z[zeta_115], theta = zeta + zeta^22 + zeta^24 + zeta^68
OK    (I1) H = {1,22,24,68} = <22> est un sous-groupe d'ordre 4 de (Z/115)^*
OK    (I1) 88 unites mod 115, 22 classes aH distinctes : theta a 22 conjugues (les 88 puissances primitives sont independantes), P22 irreductible, K = L^H
OK    (I1) -1 hors de H (K est CM, unites de rang 10) ; pgcd(21, 115) = 1 (racines de l'unite de K : +-1)
OK    I_data.gp : PREMIERS = [[599, 2, 1]] ; Q = 599^2
OK    BASE de I_data.gp : 88 x 88
OK    (I2) |det BASE| = 599^2 : BASE Z^88 est d'indice 599^2 dans Z[zeta]
OK    (I2) le pgcd de Phi_115 et des 88 colonnes de BASE modulo 599 est un polynome g unitaire de degre 2
      g = y^2 + 87 y + 322 (mod 599)
OK    (I2) g divise Phi_115 mod 599 ; les 88 colonnes de BASE sont nulles modulo (599, g) : BASE Z^88 contenu dans (599, g(zeta))
OK    (I2) g irreductible mod 599 (discriminant non residu) : (599, g(zeta)) est premier d'indice 599^2 ; donc BASE Z^88 = P = (599, g(zeta)), f(P) = 2
OK    (I2) theta mod P est dans F_599 (q = P inter K de degre 1, f(P/q) = 2)
      theta = 333 mod P ; RACINE du certificat = 333
OK    (I2) la racine du certificat est celle du premier P de I_data.gp
OK    (I2) P22 a 22 racines simples modulo 599 (599 totalement decompose dans K, Z[theta] maximal en 599) ; q = (599, theta - RACINE), N_{L/K}(P) = q^2
OK    (F) s = somme_{a=1..22} (a/23) zeta^(5a) verifie s^2 = -23 dans Z[zeta_115] : s = sqrt(-23)
OK    (F) s mod P est dans F_599 et (s mod P)^2 = -23
OK    (F) 24^2 + 23 = 599 ; pi = 24 - sqrt(-23) est dans P (pi = 0 modulo (599, g)) : P inter Q(sqrt(-23)) = (pi) est principal, N_{L/F}(P) = (pi^2)
OK    (F) contraste avec P139 : 4*139 n'est pas de la forme a^2 + 23 b^2 (premiers au-dessus de 139 non principaux dans Q(sqrt(-23))), alors que 4*599 = 48^2 + 23*2^2
OK    (I3) XI_2 entier algebrique de norme +-1 (unite de K)
OK    (I3) XI_3 entier algebrique de norme +-1 (unite de K)
OK    (I3) XI_4 entier algebrique de norme +-1 (unite de K)
OK    (I3) XI_5 entier algebrique de norme +-1 (unite de K)
OK    (I3) XI_6 entier algebrique de norme +-1 (unite de K)
OK    (I3) XI_7 entier algebrique de norme +-1 (unite de K)
OK    (I3) XI_8 entier algebrique de norme +-1 (unite de K)
OK    (I3) XI_9 entier algebrique de norme +-1 (unite de K)
OK    (I3) XI_10 entier algebrique de norme +-1 (unite de K)
OK    (I3) XI_11 entier algebrique de norme +-1 (unite de K)
OK    (I3) GAMMA entier algebrique (polynome caracteristique unitaire entier)
OK    (I3) |N(GAMMA)| = 599^331
OK    (I3) les denominateurs du certificat sont premiers a 599 (evaluation 599-adique legitime)
      valuations de GAMMA aux 22 premiers au-dessus de 599 : [(10, 0), (27, 0), (41, 0), (73, 0), (79, 0), (96, 0), (98, 0), (194, 0), (321, 0), (333, 331), (343, 0), (350, 0), (363, 0), (377, 0), (397, 0), (410, 0), (454, 0), (462, 0), (467, 0), (541, 0), (557, 0), (597, 0)]
OK    (I3) v_q(GAMMA) = 331 en q = (599, theta - 333) et 0 aux 21 autres (precision 599^340) : (GAMMA) = q^331
      l = 380651 (premier, = 1 mod 331*115) : 22 racines simples de P22, images non nulles ; rang des 10 colonnes d'unites = 10, rang total = 10
      l = 1065821 (premier, = 1 mod 331*115) : 22 racines simples de P22, images non nulles ; rang des 10 colonnes d'unites = 10, rang total = 11
      l = 1522601 (premier, = 1 mod 331*115) : 22 racines simples de P22, images non nulles ; rang des 10 colonnes d'unites = 10, rang total = 11
      premiers l utilises : [380651, 1065821, 1522601] ; matrice 66 x 11 ; rang(unites) = 10 ; rang(unites, GAMMA) = 11
OK    (I4) trois premiers l, 66 lignes de degre 1, l different de 599 et premier aux denominateurs
OK    (I4) les 10 unites XI_a sont independantes modulo les puissances 331-iemes (rang 10)
OK    (I4) GAMMA n'est pas dans <unites> . K^{*331} (rang 11)
BILAN : 37 controles, 0 echecs
CONCLUSION (preuve : note, par. 6.4, prop. 6.7) : pour tout m premier a 331, q^(2m) n'est pas principal dans K22, donc P599^m n'est pas
principal dans Q(zeta_115) : l'ordre de [P599] est divisible par 331 ; en particulier P599 et P599^3 ne sont pas principaux. SANS GRH.
FIN_OK
==== code de sortie 0

TOUTES LES VERIFICATIONS : code 0
```

## Sorties des essais supplémentaires (S1, S2, J0 à J7)

Commandes : celles de `REPRODUIRE.md`, § 2 et § 4.

```
==== (S1) gp -q -D parisize=800000000 code/sous_grh/localiser_classes.gp < /dev/null
LISTE = [[461, 5], [691, 4], [1151, 6], [1381, 21], [1471, 2, 1], [139, 2, 1], [599, 2, 1], [829, 2, 1], [1289, 2, 1], [1979, 2, 1], [3359, 2, 1], [4049, 2, 1], [4969, 2, 1], [5659, 2, 1]]
degres des sous-corps : 2, 22, 44  [0 s]
F = Q(sqrt(-23)) : Cl = [3] ; bnfcertify = 1
K22 : Cl = [662] (GRH)  [1 s]
K44 : Cl = [45013] (GRH)  [70 s]
P = [461, 5] (f = 1) : [N P] dans Cl(Q(sqrt-23)) = [1] ; dans Cl(K22) = [368] (cyc [662]) ; dans Cl(K44) = [36393] (cyc [45013])  [71 s]
P = [691, 4] (f = 1) : [N P] dans Cl(Q(sqrt-23)) = [0] ; dans Cl(K22) = [538] (cyc [662]) ; dans Cl(K44) = [6282] (cyc [45013])  [72 s]
P = [1151, 6] (f = 1) : [N P] dans Cl(Q(sqrt-23)) = [0] ; dans Cl(K22) = [500] (cyc [662]) ; dans Cl(K44) = [13875] (cyc [45013])  [74 s]
P = [1381, 21] (f = 1) : [N P] dans Cl(Q(sqrt-23)) = [2] ; dans Cl(K22) = [64] (cyc [662]) ; dans Cl(K44) = [35737] (cyc [45013])  [75 s]
P = [1471, 2, 1] (f = 2) : [N P] dans Cl(Q(sqrt-23)) = [0] ; dans Cl(K22) = [0] (cyc [662]) ; dans Cl(K44) = [38216] (cyc [45013])  [75 s]
P = [139, 2, 1] (f = 2) : [N P] dans Cl(Q(sqrt-23)) = [2] ; dans Cl(K22) = [588] (cyc [662]) ; dans Cl(K44) = [0] (cyc [45013])  [76 s]
P = [599, 2, 1] (f = 2) : [N P] dans Cl(Q(sqrt-23)) = [0] ; dans Cl(K22) = [634] (cyc [662]) ; dans Cl(K44) = [0] (cyc [45013])  [77 s]
P = [829, 2, 1] (f = 2) : [N P] dans Cl(Q(sqrt-23)) = [0] ; dans Cl(K22) = [530] (cyc [662]) ; dans Cl(K44) = [0] (cyc [45013])  [77 s]
P = [1289, 2, 1] (f = 2) : [N P] dans Cl(Q(sqrt-23)) = [2] ; dans Cl(K22) = [130] (cyc [662]) ; dans Cl(K44) = [0] (cyc [45013])  [78 s]
P = [1979, 2, 1] (f = 2) : [N P] dans Cl(Q(sqrt-23)) = [1] ; dans Cl(K22) = [430] (cyc [662]) ; dans Cl(K44) = [0] (cyc [45013])  [79 s]
P = [3359, 2, 1] (f = 2) : [N P] dans Cl(Q(sqrt-23)) = [0] ; dans Cl(K22) = [244] (cyc [662]) ; dans Cl(K44) = [0] (cyc [45013])  [80 s]
P = [4049, 2, 1] (f = 2) : [N P] dans Cl(Q(sqrt-23)) = [1] ; dans Cl(K22) = [50] (cyc [662]) ; dans Cl(K44) = [0] (cyc [45013])  [80 s]
P = [4969, 2, 1] (f = 2) : [N P] dans Cl(Q(sqrt-23)) = [2] ; dans Cl(K22) = [276] (cyc [662]) ; dans Cl(K44) = [0] (cyc [45013])  [81 s]
P = [5659, 2, 1] (f = 2) : [N P] dans Cl(Q(sqrt-23)) = [0] ; dans Cl(K22) = [238] (cyc [662]) ; dans Cl(K44) = [0] (cyc [45013])  [82 s]
==== code de sortie 0
==== (S2) GP=gp sh code/preparation/preparer.sh
Pm identique a rang88_m115c0_data.txt ; beta0 relu.
bnfinit(K115) : Cl = [] ; h = 1 ; #fu = 43 ; Cl+ = [2]  [5 s]
sauvegarde sortie_preparation/bnf_k115.bin  [5 s]
I : q = 19321 ; isometrie exacte verifiee ; Gram(I) paire de det 1  [7 s]
cote 1 : BKZ-20 : 159 + 476 insertions ; noeuds estimes : court (1057/200) 1.869 e11 (signe compris) ; CVP (borne 12 - 1057/200) 1.862 e4 par recherche  [21 s]
cote 1 : DA = 139, DB = 1, d = 278 ; det(court) = 1/19321 ; det(fibre) = 5979559874758208072831494782976 ; diag court 334..707 ; diag fibre 16..32 (echelle)  [22 s]
cote 2 : BKZ-20 : 210 + 248 insertions ; noeuds estimes : court (1057/200) 1.818 e11 (signe compris) ; CVP (borne 12 - 1057/200) 2.041 e4 par recherche  [33 s]
cote 2 : DA = 139, DB = 1, d = 278 ; det(court) = 1/19321 ; det(fibre) = 5979559874758208072831494782976 ; diag court 334..658 ; diag fibre 16..32 (echelle)  [33 s]
ecrit sortie_preparation/P139  [33 s]
IDENTIQUE  P139/I_data.gp
IDENTIQUE  P139/cote1_A.gram
IDENTIQUE  P139/cote1_B.gram
IDENTIQUE  P139/cote1_T.mat
IDENTIQUE  P139/cote1_meta.txt
IDENTIQUE  P139/cote1_bases.gp
IDENTIQUE  P139/cote2_A.gram
IDENTIQUE  P139/cote2_B.gram
IDENTIQUE  P139/cote2_T.mat
IDENTIQUE  P139/cote2_meta.txt
IDENTIQUE  P139/cote2_bases.gp
I : q = 358801 ; isometrie exacte verifiee ; Gram(I) paire de det 1  [7 s]
cote 1 : BKZ-20 : 553 + 127 insertions ; noeuds estimes : court (1057/200) 4.223 e11 (signe compris) ; CVP (borne 12 - 1057/200) 1.344 e4 par recherche  [24 s]
cote 1 : DA = 599, DB = 1, d = 1198 ; det(court) = 1/358801 ; det(fibre) = 111043531008908432003520167673856 ; diag court 1376..2937 ; diag fibre 20..44 (echelle)  [24 s]
cote 2 : BKZ-20 : 447 + 298 insertions ; noeuds estimes : court (1057/200) 4.812 e11 (signe compris) ; CVP (borne 12 - 1057/200) 1.312 e4 par recherche  [42 s]
cote 2 : DA = 599, DB = 1, d = 1198 ; det(court) = 1/358801 ; det(fibre) = 111043531008908432003520167673856 ; diag court 1376..3030 ; diag fibre 20..32 (echelle)  [42 s]
ecrit sortie_preparation/P599  [42 s]
IDENTIQUE  P599/I_data.gp
IDENTIQUE  P599/cote1_A.gram
IDENTIQUE  P599/cote1_B.gram
IDENTIQUE  P599/cote1_T.mat
IDENTIQUE  P599/cote1_meta.txt
IDENTIQUE  P599/cote1_bases.gp
IDENTIQUE  P599/cote2_A.gram
IDENTIQUE  P599/cote2_B.gram
IDENTIQUE  P599/cote2_T.mat
IDENTIQUE  P599/cote2_meta.txt
IDENTIQUE  P599/cote2_bases.gp
==== code de sortie 0
==== (J0) java -version ; javac -version
openjdk version "11.0.16.1" 2022-08-12 LTS
OpenJDK Runtime Environment Microsoft-40648 (build 11.0.16.1+1-LTS)
OpenJDK 64-Bit Server VM Microsoft-40648 (build 11.0.16.1+1-LTS, mixed mode)
javac 11.0.16.1
==== (J1) javac -d $T/recomp code/certifiant/Rang88CertZ.java code/certifiant/TestCertZ.java ; comparaison aux classes du depot
javac : code 0
identique Rang88CertZ$Compteurs.class
identique Rang88CertZ$EnumZ.class
identique Rang88CertZ$FormeZ.class
identique Rang88CertZ$Recepteur.class
identique Rang88CertZ$Tache.class
identique Rang88CertZ$Travail.class
identique Rang88CertZ.class
identique TestCertZ.class
classes recompilees : 8 ; classes du depot : 8
==== (J2) java -Xmx1g -Dverif=1 -cp code/certifiant/classes TestCertZ 1 300
E8 : 10 controles, 0 echecs
FORMES : 300 essais (graine 1, F=40, verif=true) ; u compares 8541 ; touches comparees 71546 ; cas de frontiere exacte 2157
TOTAL : 910 controles, 0 echecs
TEST_OK
==== code de sortie 0
==== (J3) validation P461, seuil 7/2, D = 6 : Rang88CertZ run java_P461/cote1 7 2 12 6 6
code de sortie 0
  JVM OpenJDK 64-Bit Server VM 11.0.16.1 ; Windows 11 amd64 ; processeurs 16 ; (numero de processus et date omis)
  LIEN entrees=7f34ac6bde43c264d6fe45ce86a36ef554aca48dd9635ec028286a6810508530|classes=4f1ed5ad5834cdca3c34b7b70c5af9bdf3f942c6f4e088c6f9083c73cec8d20c
CATALOGUE_SHA256 30d7a99ff07be5bf938c52ad9a24316312e0c49001ae5b2eb13d695dfe3c010a ; TOTAL_TACHES 3658
SELECTION 3658/3658 ; A_FAIRE 3658 ; DEJA_AU_CHECKPOINT 0
TOUCHE court=1595/461 fibre(num)=7259828/(1*922^2) u=[-2, 1, -2, 0, -2, 0, 1, 0, -1, 0, 2, 1, -1, 0, 1, 2, 1, 1, 0, -1, 1, 0, 1, 1, 0, -2, 0, 0, -1, 0, -1, 1, -1, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0] y=[
TOUCHE court=1579/461 fibre(num)=7289332/(1*922^2) u=[0, 3, -1, 4, -2, -2, -1, -3, 0, -1, -1, 0, 0, 1, 0, -1, 1, 1, 1, -1, 0, -1, 1, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0] y
EXECUTEES_CE_LANCEMENT 3658 ; REPRISES_DU_CHECKPOINT 0
COMPTE_U (au signe pres, energie courte <= 7/2) 697 ; histogramme [2.3,2.4):1 [2.4,2.5):2 [2.6,2.7):1 [2.7,2.8):2 [2.8,2.9):5 [2.9,3.0):14 [3.0,3.1):28 [3.1,3.2):52 [3.2,3.3):94 [3.3,3.4):152 [3.4,3.5
TOTAL_TOUCHES 2
COUVERTURE_COMPLETE 3658/3658 ; CATALOGUE 30d7a99ff07be5bf938c52ad9a24316312e0c49001ae5b2eb13d695dfe3c010a
FIN [8 s]
==== (J4) BA_NUM=7 BA_DEN=2 sh code/certifiant/rejouer_cote.sh validation/P461 1 $T/P461_7_2 4
code de sortie Java : 0
CATALOGUE_SHA256 cbcf85f4ad192efc6716b0f2f58bd95456ae1060012846d889f6ccdb507cdd9c ; TOTAL_TACHES 5003
SELECTION 5003/5003 ; A_FAIRE 5003 ; DEJA_AU_CHECKPOINT 0
CHECKPOINT_SHA256 a790c56ccdf0d0c01c3ada7ac37f8dadf4a2e7bd4abcf386b1de6afbe4d0a6f2 ; cote1.ckpt
EXECUTEES_CE_LANCEMENT 392 ; REPRISES_DU_CHECKPOINT 0
TOTAL_TOUCHES 1
COUVERTURE_PARTIELLE 392/5003 : AUCUNE CONCLUSION GLOBALE
FIN [3 s]
contenu du repertoire de sortie :
cote1.ckpt
cote1.ckpt.touches
cote1.java.exit
cote1.stderr.log
cote1.stdout.log
cote1.taches
java_P461
-- second appel sur le meme repertoire (doit refuser) :
REFUS : $T/P461_7_2/cote1.ckpt existe deja ; il faut un fichier de recus neuf
code de sortie du lanceur : 0
==== (J5) catalogues seuls (mode taches), quatre cotes
P139 cote 1 : code 0 ; CATALOGUE_SHA256 fd9e41bd2b65ede6a33342dc665ec48c565509665ea14b554d5f72620332cdb3 ; TOTAL_TACHES 48227 ; fichier IDENTIQUE a data/P139/cote1.taches
P139 cote 2 : code 0 ; CATALOGUE_SHA256 39e9d80bbf691f56bed5684303dea9dfa48e640d0f7b342239657d3890f17ecb ; TOTAL_TACHES 61174 ; fichier IDENTIQUE a data/P139/cote2.taches
P599 cote 1 : code 0 ; CATALOGUE_SHA256 b9ff8375cdbb906a78daf01c07ae523b76165fa73ff34a3fcadba3b0ce130155 ; TOTAL_TACHES 59255 ; fichier IDENTIQUE a data/P599/cote1.taches
P599 cote 2 : code 0 ; CATALOGUE_SHA256 a97cb23d0b7cdb1403386a1b51f335c7a3c96765bbe736e44dc582ab3767bf2c ; TOTAL_TACHES 74398 ; fichier IDENTIQUE a data/P599/cote2.taches
==== (J6) six taches isolees par cote, fichier de recus neuf (-Dliste) ; comparaison aux recus publies
P139 cote 1 : code 0 ; taches 15730 29320 4426 7055 14107 32661
SELECTION 6/48227 ; A_FAIRE 6 ; DEJA_AU_CHECKPOINT 0
EXECUTEES_CE_LANCEMENT 6 ; REPRISES_DU_CHECKPOINT 0
TOTAL_TOUCHES 0
COUVERTURE_PARTIELLE 6/48227 : AUCUNE CONCLUSION GLOBALE
  en-tete identique a celui des recus publies : True
  recus rejoues identiques aux lignes de meme indice des recus publies : True (6 recus)
P599 cote 2 : code 0 ; taches 11259 659 13278 37465 1667 29852
SELECTION 6/74398 ; A_FAIRE 6 ; DEJA_AU_CHECKPOINT 0
EXECUTEES_CE_LANCEMENT 6 ; REPRISES_DU_CHECKPOINT 0
TOTAL_TOUCHES 0
COUVERTURE_PARTIELLE 6/74398 : AUCUNE CONCLUSION GLOBALE
  en-tete identique a celui des recus publies : True
  recus rejoues identiques aux lignes de meme indice des recus publies : True (6 recus)
==== (J7) empreinte_canonique.py sur les recus de reference
data/P139/replication/cote1.ckpt : 48227 recus (total annonce 48227, indices 0..n-1 complets) ; touches 0 ; empreinte canonique c99dcf87db02e6b51f448cdb3e51da1f8b0ee4bd782b6b0e78d686bed5575122
data/P139/replication/cote2.ckpt : 61174 recus (total annonce 61174, indices 0..n-1 complets) ; touches 0 ; empreinte canonique 8ab1f40a48c416dd4eab8dde92d0c5866a6ca1951b5edd5d579c5f2ee0bedaf7
data/P599/replication/cote1.ckpt : 59255 recus (total annonce 59255, indices 0..n-1 complets) ; touches 0 ; empreinte canonique f3cf379ad157b1595f9ad96c38d3734a920ea24de3afc5d12dfa617bb3e42689
data/P599/replication/cote2.ckpt : 74398 recus (total annonce 74398, indices 0..n-1 complets) ; touches 0 ; empreinte canonique b9c93a83d2b370fad5de5b3d0edc317718ebe4900960642ef98f72c219458ef6
```
