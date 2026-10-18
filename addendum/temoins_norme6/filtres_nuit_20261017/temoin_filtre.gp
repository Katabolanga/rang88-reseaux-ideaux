/* temoin_filtre.gp -- verification EXACTE et autonome des touches de norme 6 d'un filtre Rang88CertZ (Claude, 17 oct. 2026).
   Generalise tinv/temoin_P691s24.gp a tout ideal I donne par une liste de premiers (conventions de outils115.gp) :
   [p, r] = (p, zeta - r) de degre 1 ; [p, 2, k] = premier de degre 2 au-dessus de p.
   Parametres, definis avant read() : D (dossier java_X des entrees), T (dossier des touches), NOM (prefixe NOM_c<cote>),
   PREMATT (liste attendue), COTES (cotes dont le fichier .ckpt.touches existe).
   Ce script ne fait confiance a aucune sortie du programme Java autre que les coordonnees (u, y) des touches :
   1. BASE engendre exactement I : chaque colonne est dans chaque premier de la liste, et |det BASE| = N(I) ;
   2. GRAM = BASE~ * (Tr(ALPHA zeta^(i-j))) * BASE est recalculee : entiere, paire, de determinant 1, definie positive ;
      (I, ALPHA) est donc LE reseau ideal unimodulaire de la classe [I] (note, prop. 2.3 (b)) ;
   3. chaque touche (u, y) donne x = AB^-1 (b ; a), qui doit etre entier, avec x~ GRAM x = 6. */
default(parisizemax, 2 * 10^9);
m = 115; n = 88; Phi = polcyclo(m, 'y); z = Mod('y, Phi);
read(Str(D, "/I_data.gp"));
nb = 0; nok = 0;
ok(nom, c) = nb++; if (c, nok++); printf("%s %s\n", if (c, "OK   ", "ECHEC"), nom);
ok(Str("PREMIERS = ", PREMATT), PREMIERS == PREMATT);
col(j) = Pol(Vecrev(BASE[, j]), 'y);
{
dans(P) =
  my(p = P[1]);
  if (#P == 2,
    if (subst(Phi, 'y, Mod(P[2], p)) != 0, return(0));
    prod(j = 1, n, subst(col(j), 'y, Mod(P[2], p)) == 0),
    my(F = factormod(Phi, p)[, 1], t = 0);
    for (i = 1, #F, if (poldegree(F[i]) == 2 && prod(j = 1, n, lift(Mod(col(j) * Mod(1, p), F[i])) == 0), t++));
    t == 1);
}
/* v3 (contrelecture d'Astra, 17 oct., 4 h 03) : le CONTRAT est restreint aux deux formes reellement couvertes, verifiees ici :
   (A) un seul premier de degre 2, [p, 2, k] ; dans() trouve alors l'UNIQUE facteur quadratique de Phi_115 mod p contenant les
       colonnes : c'est un conjugue de l'ideal annonce, et des premiers conjugues donnent des reseaux isometriques ;
   (B) deux premiers de degre 1 au-dessus du MEME p, [[p, r1], [p, r2]], avec 0 < r1, r2 < p (racines reduites modulo p),
       r1 != r2 et r2 = r1^24 mod p : ce sont P et sigma_24(P), distincts donc comaximaux, et « colonnes dans chaque premier +
       indice p^2 » identifie exactement leur produit.  Toute autre forme de liste est refusee (ECHEC). */
formeA = (#PREMATT == 1 && #PREMATT[1] == 3 && PREMATT[1][2] == 2 && isprime(PREMATT[1][1]));
formeB = (#PREMATT == 2 && #PREMATT[1] == 2 && #PREMATT[2] == 2 && PREMATT[1][1] == PREMATT[2][1] && isprime(PREMATT[1][1]) && PREMATT[1][2] > 0 && PREMATT[1][2] < PREMATT[1][1] && PREMATT[2][2] > 0 && PREMATT[2][2] < PREMATT[1][1] && PREMATT[1][2] != PREMATT[2][2] && Mod(PREMATT[1][2], PREMATT[1][1])^24 == PREMATT[2][2]);
ok("forme de la liste couverte par ce verificateur : (A) un premier de degre 2 seul, ou (B) P et sigma_24(P) de degre 1, racines reduites modulo p, distinctes, r2 = r1^24", formeA || formeB);
foreach(PREMATT, P, ok(Str("chaque colonne de BASE est dans le premier ", P, " (degre ", if (#P == 2, 1, 2), ")"), dans(P)));
NI = prod(i = 1, #PREMATT, PREMATT[i][1]^if (#PREMATT[i] == 2, 1, 2));
ok(Str("BASE 88 x 88 entiere et |det BASE| = N(I) = ", NI, " : BASE engendre exactement I"), matsize(BASE) == [88, 88] && denominator(content(BASE)) == 1 && abs(matdet(BASE)) == NI);
aL = subst(lift(ALPHA), 'x, z + 1/z);
tr = vector(m, k, trace(aL * z^(k - 1)));
H = matrix(n, n, i, j, tr[(i - j) % m + 1]);
G = BASE~ * H * BASE;
ok("GRAM recalculee depuis ALPHA = GRAM du fichier", G == GRAM);
ok("GRAM entiere, paire, de determinant 1", denominator(content(G)) == 1 && vecsum(vector(n, i, G[i, i] % 2)) == 0 && matdet(G) == 1);
Q = qfgaussred(G);
ok("GRAM definie positive (88 pivots de Gauss > 0)", vecmin(vector(n, i, Q[i, i])) > 0);
ntouches = 0;
{
foreach(COTES, cote,
  read(Str(D, "/cote", cote, "_bases.gp"));
  my(L = readstr(Str(T, "/", NOM, "_c", cote, ".ckpt.touches")));
  for (i = 1, #L, my(s = L[i], u, yy, cs, fb, v, x, nr);
    u = eval(Str("[", strsplit(strsplit(s, " u=[")[2], "] y=")[1], "]"))~;
    yy = eval(Str("[", strsplit(strsplit(s, " y=[")[2], "]")[1], "]"))~;
    cs = Hc * u; fb = Hl * u + Hf * yy;
    v = if (cote == 1, concat(fb, cs), concat(cs, fb));
    x = matsolve(AB, v);
    nr = if (denominator(content(x)) == 1, x~ * G * x, -1);
    ntouches++;
    ok(Str("cote ", cote, ", touche ", i, " : x entier dans BASE et x~ GRAM x = 6 (norme ", nr, ")"), nr == 6);
    printf("      x = %s\n", x~)));
}
ok("au moins une touche verifiee", ntouches > 0);
/* GP poursuit apres une erreur de commande : le verdict exige le nombre COMPLET de controles. */
natt = 7 + #PREMATT + ntouches;
printf("BILAN : %d controles (attendus %d), %d echecs\n", nb, natt, nb - nok);
verdict = (nok == nb && nb == natt);
print(if (verdict, "TEMOIN_NORME6_OK", "TEMOIN_NORME6_ECHEC"));
quit(if (verdict, 0, 1))
