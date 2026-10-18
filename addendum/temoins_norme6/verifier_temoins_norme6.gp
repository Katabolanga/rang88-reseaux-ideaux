/* verifier_temoins_norme6.gp -- controle EXACT et autonome des cinq temoins de norme 6 de l'addendum (version 1.2 du depot) :
   les quatre rejets des filtres du par. 4.5 (tableau 4 : P2531 s24(P2531), P5981 s24(P5981), P18401 s24(P18401), P39239)
   et le temoin de la proposition 4.6 (I = P691 s24(P691), jumeau de X4969 ; le theoreme B en depend).
   Aucun bnfinit, aucun programme Java, aucune sortie de session.  Pour chaque fichier temoin_<NOM>.gp de ce dossier
   (affectations de constantes seulement), et d'apres une liste FIGEE des cibles (ideaux et energies des touches imprimees
   dans l'addendum), ce script controle :
   A1  NOM, PREMIERS, NORME_ABS_I, NORME et le nombre de temoins sont ceux de la cible ;
   A2  l'ideal : forme (B) [[p, r1], [p, r2]] : p premier, 0 < r1 != r2 < p, Phi_115(r1) = Phi_115(r2) = 0 mod p,
       r2 = r1^24 mod p (donc (p, zeta - r2) = sigma_24(p, zeta - r1)), et GEN = (y - r1)(y - r2) reduit mod p ;
       forme (A) [[p, 2, k]] : p premier d'ordre 2 modulo 115, GEN unitaire de degre 2, irreductible modulo p et divisant
       Phi_115 modulo p (I = (p, GEN(zeta)) est alors un premier de degre 2 au-dessus de p ; tous sont conjugues) ;
   A3  la base C de I construite ICI, sans la base du preparateur : colonnes p, p zeta, GEN(zeta) zeta^j (0 <= j <= 85) ;
       |det C| = p^2 et C^-1 M_zeta C entiere : le Z-module engendre est un ideal, contenu dans (p, GEN(zeta)) et qui
       contient p et GEN(zeta), donc egal a I ;
   B1  PM et BETA0 sont lus dans data/corps/rang88_m115c0_data.txt ; PM est le polynome minimal de zeta + 1/zeta, et
       ALPHA * NU = BETA0 modulo PM (alpha = beta0 / nu, comme dans la note) ;
   B2-B4  la matrice de Gram G = C~ H C, H[i, j] = Tr_{L/Q}(alpha zeta^(i-j)), recalculee depuis ALPHA seul, est entiere,
       symetrique, paire, de determinant 1 et definie positive (qfsign exact) : (I, alpha) est un reseau pair unimodulaire
       defini positif de rang 88, donc l'element de S de classe [I] (note, prop. 2.3 (b)) ;
   C1  pour chaque temoin z (colonne de Z, coefficients en zeta^0..zeta^87) : z entier, non nul, coordonnees w = C^-1 z
       entieres (z est dans I) et w~ G w = 6 ;
   C2  Tr_{L/Q}(alpha z zbar) = 6, calcule directement dans Q(zeta), sans aucune base ;
   C3  les energies (courte, de fibre) imprimees dans l'addendum pour la touche sont retrouvees exactement : avec
       f = Tr_{L/Q}(alpha z^2), on a Lambda(a) = 6 + f et Lambda'(b) = 6 - f (note, lemme 4.2, k = 0) ; la projection
       courte porte sur a au cote 1 et sur b au cote 2 (note, prop. 4.1 (c)) ; donc (courte, fibre) = (6 + f, 6 - f) au
       cote 1 et (6 - f, 6 + f) au cote 2.  Ce controle relie le vecteur publie a la colonne « energies » du tableau 4 ;
   D1-D3  provenance : BASE (base du preparateur, celle des fichiers d'entree du programme) est entiere, |det BASE| = p^2
       et C^-1 BASE est entiere (BASE engendre I) ; GRAM = BASE~ H BASE ; Z = BASE X et X~ GRAM X = 6 (X : coordonnees
       issues de la touche du programme).
   GP poursuit apres une erreur : le verdict exige le nombre COMPLET de controles (9 + 4 x nombre de temoins par fichier,
   69 en tout) et aucun echec.  Code de sortie 0 si et seulement si tout passe.
   Usage (depuis la racine du depot ; moins d'une minute) :
     gp -q -D parisize=400000000 addendum/temoins_norme6/verifier_temoins_norme6.gp < /dev/null */
default(breakloop, 0);
m = 115; n = 88; Phi = polcyclo(m, 'y); zz = Mod('y, Phi);
REP = "addendum/temoins_norme6/";
DATC = read("data/corps/rang88_m115c0_data.txt");
PMc = DATC[1]; BETA0c = DATC[2]; PMmin = minpoly(zz + 1/zz, 'x);
Mz = matrix(n, n, i, j, i == j + 1); Mz[, n] = -Colrev(Phi - 'y^n, n);   /* multiplication par zeta, base des puissances */
{
/* [nom, PREMIERS, [[energie courte, energie de fibre, cote] pour chaque touche]] : tableau 4 et preuve de la prop. 4.6 */
CIBLES = [["P2531s24", [[2531, 12], [2531, 483]], [[11913/2531, 186878916/5062^2, 2]]],
          ["P5981s24", [[5981, 16], [5981, 5092]], [[28185/5981, 1042775388/11962^2, 1]]],
          ["P18401s24", [[18401, 22], [18401, 8441]], [[85506/18401, 9959062824/36802^2, 1]]],
          ["P39239", [[39239, 2, 1]], [[164472/39239, 48090690576/78478^2, 2]]],
          ["P691s24", [[691, 4], [691, 596]], [[3542/691, 13129000/1382^2, 1], [2406/691, 16268904/1382^2, 2]]]];
}
nb = 0; nok = 0; natt = 0; nvalides = 0;
ok(nom, c) = nb++; if (c, nok++); printf("%s %s\n", if (c, "OK   ", "ECHEC"), nom);
idealB(PR, g) =
{
  my(p = PR[1][1], r1 = PR[1][2], r2 = PR[2][2]);
  #PR[1] == 2 && #PR[2] == 2 && PR[2][1] == p && isprime(p) && r1 > 0 && r1 < p && r2 > 0 && r2 < p && r1 != r2
  && subst(Phi, 'y, Mod(r1, p)) == 0 && subst(Phi, 'y, Mod(r2, p)) == 0 && Mod(r1, p)^24 == r2
  && g == lift(('y - Mod(r1, p)) * ('y - Mod(r2, p)));
}
idealA(PR, g) =
{
  my(p = PR[1][1]);
  #PR == 1 && #PR[1] == 3 && PR[1][2] == 2 && isprime(p) && znorder(Mod(p, m)) == 2
  && type(g) == "t_POL" && variable(g) == 'y && poldegree(g) == 2 && pollead(g) == 1
  && vecmin(Vec(g)) >= 0 && vecmax(Vec(g)) < p
  && polisirreducible(g * Mod(1, p)) && (Phi * Mod(1, p)) % (g * Mod(1, p)) == 0;
}
{
for (kc = 1, #CIBLES,
  my(cib = CIBLES[kc], F = Str(REP, "temoin_", cib[1], ".gp"), nt = #cib[3], nb0 = nb, nok0 = nok, p, C, aL, tr, H, G, w, zk, zp, zb, fk, e);
  natt += 9 + 4 * nt;
  NOM = 0; PREMIERS = 0; NORME_ABS_I = 0; GEN = 0; NU = 0; ALPHA = 0; BASE = 0; GRAM = 0; COTES = 0; TOUCHES = 0; X = 0; Z = 0; NORME = 0;
  read(F);
  printf("== %s (%s)\n", cib[1], F);
  p = cib[2][1][1];
  ok(Str(cib[1], " A1 : NOM, PREMIERS = ", cib[2], ", NORME_ABS_I = p^2, NORME = 6, ", nt, " temoin(s)"),
     NOM == cib[1] && PREMIERS == cib[2] && NORME_ABS_I == p^2 && NORME == 6 && type(Z) == "t_MAT" && matsize(Z) == [n, nt]
     && type(X) == "t_MAT" && matsize(X) == [n, nt]);
  ok(Str(cib[1], " A2 : I = (", p, ", ", GEN, ") ", if (#PREMIERS == 2, "= P sigma_24(P), P de degre 1", "est un premier de degre 2")),
     if (#PREMIERS == 2, idealB(PREMIERS, GEN), idealA(PREMIERS, GEN)));
  C = matrix(n, n); C[1, 1] = p; C[2, 2] = p;
  for (j = 0, n - 3, my(v = Colrev(GEN * 'y^j, n)); for (i = 1, n, C[i, j + 3] = v[i]));
  ok(Str(cib[1], " A3 : base C (p, p zeta, GEN zeta^j) : |det C| = p^2 et C stable par zeta, donc C engendre I"),
     abs(matdet(C)) == p^2 && denominator(content(matsolve(C, Mz * C))) == 1);
  ok(Str(cib[1], " B1 : PM et BETA0 lus dans data/corps, PM = polynome minimal de zeta + 1/zeta, ALPHA * NU = BETA0 mod PM"),
     PMc == PMmin && Mod(ALPHA * NU - BETA0c, PMc) == 0);
  aL = subst(lift(Mod(ALPHA, PMc)), 'x, zz + 1/zz);
  tr = vector(m, k, trace(aL * zz^(k - 1)));
  H = matrix(n, n, i, j, tr[(i - j) % m + 1]);
  G = C~ * H * C;
  ok(Str(cib[1], " B2 : Gram G = C~ H C (depuis ALPHA seul) entiere, symetrique, paire"),
     denominator(content(G)) == 1 && G == G~ && vecsum(vector(n, i, G[i, i] % 2)) == 0);
  ok(Str(cib[1], " B3 : det G = 1"), matdet(G) == 1);
  ok(Str(cib[1], " B4 : G definie positive (qfsign exact)"), qfsign(G) == [n, 0]);
  for (k = 1, nt,
    zk = Z[, k]; w = matsolve(C, zk);
    ok(Str(cib[1], " C1, temoin ", k, " : z entier non nul, coordonnees entieres dans C (z dans I), w~ G w = ", if (denominator(content(w)) == 1, qfeval(G, w), "?")),
       zk != 0 && denominator(content(zk)) == 1 && denominator(content(w)) == 1 && qfeval(G, w) == 6);
    zp = Mod(Pol(Vecrev(zk), 'y), Phi); zb = Mod(subst(lift(zp), 'y, lift(1/zz)), Phi);
    ok(Str(cib[1], " C2, temoin ", k, " : Tr(alpha z zbar) = ", trace(aL * zp * zb), " (sans base)"), trace(aL * zp * zb) == 6);
    fk = trace(aL * zp^2);
    e = cib[3][k];
    ok(Str(cib[1], " C3, temoin ", k, " (cote ", e[3], ") : energies courte ", e[1], " et de fibre ", e[2],
           " retrouvees (f = Tr(alpha z^2) = ", fk, ")"),
       e[1] + e[2] == 12 && COTES[k] == e[3]
       && if (e[3] == 1, 6 + fk == e[1] && 6 - fk == e[2], 6 - fk == e[1] && 6 + fk == e[2])));
  ok(Str(cib[1], " D1 : BASE du preparateur entiere, |det BASE| = p^2, colonnes dans I (BASE engendre I)"),
     type(BASE) == "t_MAT" && matsize(BASE) == [n, n] && denominator(content(BASE)) == 1 && abs(matdet(BASE)) == p^2
     && denominator(content(matsolve(C, BASE))) == 1);
  ok(Str(cib[1], " D2 : GRAM du fichier = BASE~ H BASE"), BASE~ * H * BASE == GRAM);
  for (k = 1, nt,
    ok(Str(cib[1], " D3, temoin ", k, " : Z = BASE X et X~ GRAM X = 6"),
       X[, k] != 0 && denominator(content(X[, k])) == 1 && BASE * X[, k] == Z[, k] && qfeval(GRAM, X[, k]) == 6));
  if (nb - nb0 == 9 + 4 * nt && nok - nok0 == nb - nb0, nvalides++);
  printf("   %s : %s\n", cib[1], if (nb - nb0 == 9 + 4 * nt && nok - nok0 == nb - nb0,
         "TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal)", "ECHEC")));
}
printf("BILAN : %d controles (attendus %d), %d echecs ; %d temoins valides sur %d fichiers\n", nb, natt, nb - nok, nvalides, #CIBLES);
verdict = (nok == nb && nb == natt && natt == 69 && nvalides == #CIBLES);
print(if (verdict, "TEMOINS_NORME6_ADDENDUM_OK", "TEMOINS_NORME6_ADDENDUM_ECHEC"));
quit(if (verdict, 0, 1))
