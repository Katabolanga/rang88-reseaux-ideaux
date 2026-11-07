/* commun_rang88.gp -- reconstruction EXACTE et controlee du reseau ideal (I, Tr(alpha x ybar)) de rang 88 sur L = Q(zeta_115)
   (Claude, 19 oct. 2026, detecteur G6K).  Adapte de addendum/temoins_norme6/verifier_temoins_norme6.gp (depot public,
   version 1.2), sans le modifier.  A lire apres avoir fixe FCORPS (fichier data/corps/rang88_m115c0_data.txt), FIDATA
   (fichier I_data.gp de la chaine prep_java.gp : PREMIERS, Q, NU, ALPHA, BASE, GRAM) et NOM (ex. "P3911s24", "P8419").
   La fonction reconstruit() :
   A1  type de l'ideal d'apres PREMIERS :
       [[p, r1], [p, r2]] : p premier, p = 1 mod 115, r1 != r2 racines PRIMITIVES 115-iemes de l'unite mod p ;
           l'exposant k (mod 115) tel que r2 = r1^k est calcule ; il doit etre 24 si NOM contient "s24", 91 si "s91" ;
           I = P sigma_k(P), GEN = (y - r1)(y - r2) mod p ;
       [[p, 2, j]] : p premier d'ordre 2 mod 115 ; GEN = l'UNIQUE facteur irreductible de degre 2 de Phi_115 mod p dont la
           colonne est dans le Z-module engendre par BASE (controle exact : un et un seul) ;
       [[p, r]]   : p premier, Phi_115(r) = 0 mod p, GEN = y - r (premier de degre 1) ;
   A2  base C de I construite ICI depuis (p, GEN) seuls : p zeta^i (i < d = deg GEN), GEN(zeta) zeta^j (0 <= j < 88 - d) ;
       |det C| = p^d = Q et C^-1 M_zeta C entiere (module stable par zeta, contenu dans (p, GEN(zeta)), de meme indice : = I) ;
   A3  BASE (fichier) engendre le meme module : |det BASE| = Q et C^-1 BASE entiere ;
   B1  PM (lu) = polynome minimal de zeta + 1/zeta et ALPHA * NU = BETA0 mod PM ;
   B2  G = C~ H C, H[i, j] = Tr(alpha zeta^(i - j)), entiere, symetrique, paire ;  B3  det G = 1 ;  B4  qfsign(G) = [88, 0] ;
   B5  GRAM (fichier) = BASE~ H BASE (provenance) ;
   R1  U = qflllgram(G), |det U| = 1, Gr = U~ G U (Gram LLL, celle qu'on donne a G6K).
   Chaque controle imprime sa ligne ; le verdict exige le nombre COMPLET de controles et aucun echec (GP poursuit apres
   une erreur). */
default(breakloop, 0);
m = 115; n = 88; Phi = polcyclo(m, 'y); zz = Mod('y, Phi);
DATC = read(FCORPS); PMc = DATC[1]; BETA0c = DATC[2]; PMmin = minpoly(zz + 1/zz, 'x);
Mz = matrix(n, n, i, j, i == j + 1); Mz[, n] = -Colrev(Phi - 'y^n, n);   /* multiplication par zeta */
nb = 0; nok = 0;
ok(nom, c) = nb++; if (c, nok++); printf("%s %s\n", if (c, "OK   ", "ECHEC"), nom); c;
estdans(Binv, col) = denominator(content(Binv * col)) == 1;
{
reconstruit() =
  my(p, d, k, r1, r2, typ, Binv, cands, tr, ok1);
  PREMIERS = 0; Q = 0; NU = 0; ALPHA = 0; BASE = 0; GRAM = 0; AB = 0;
  read(FIDATA);
  printf("== %s : I_data = %s\n", NOM, FIDATA);
  p = PREMIERS[1][1];
  if (type(BASE) != "t_MAT" || matsize(BASE) != [n, n], error("BASE absente"));
  Binv = matsolve(BASE, matid(n));
  if (#PREMIERS == 2,
    r1 = PREMIERS[1][2]; r2 = PREMIERS[2][2];
    k = 0; for (e = 2, m - 1, if (gcd(e, m) == 1 && Mod(r1, p)^e == Mod(r2, p), k = e; break));
    typ = Str("s", k);
    ok1 = isprime(p) && p % m == 1 && PREMIERS[2][1] == p && r1 != r2 && r1 > 0 && r2 > 0 && r1 < p && r2 < p
          && znorder(Mod(r1, p)) == m && znorder(Mod(r2, p)) == m && k > 0
          && (#strsplit(NOM, "s24") == 1 || k == 24) && (#strsplit(NOM, "s91") == 1 || k == 91)
          && (#strsplit(NOM, "s24") > 1 || #strsplit(NOM, "s91") > 1);
    GEN = lift(('y - Mod(r1, p)) * ('y - Mod(r2, p)));
    ok(Str(NOM, " A1 : I = P sigma_", k, "(P), P = (", p, ", zeta - ", r1, "), sigma_", k, "(P) = (", p, ", zeta - ", r2,
           ") ; p = 1 mod 115, racines primitives, exposant conforme au nom ; GEN = ", GEN), ok1),
  if (#PREMIERS == 1 && #PREMIERS[1] == 3,
    typ = "deg2";
    cands = [];
    my(F = factormod(Phi, p)[, 1]);
    for (i = 1, #F, my(g = lift(F[i])); if (poldegree(g) == 2 && estdans(Binv, Colrev(g, n)), cands = concat(cands, [g])));
    GEN = if (#cands == 1, cands[1], 0);
    ok(Str(NOM, " A1 : I = (", p, ", GEN) premier de degre 2 : p premier d'ordre 2 mod 115, un seul facteur quadratique de Phi mod p dans BASE (",
           #cands, ") : GEN = ", GEN),
       isprime(p) && znorder(Mod(p, m)) == 2 && PREMIERS[1][2] == 2 && #cands == 1),
  if (#PREMIERS == 1 && #PREMIERS[1] == 2,
    typ = "deg1"; r1 = PREMIERS[1][2]; GEN = 'y - r1;
    ok(Str(NOM, " A1 : I = (", p, ", zeta - ", r1, ") premier de degre 1"),
       isprime(p) && p % m == 1 && znorder(Mod(r1, p)) == m),
  error("PREMIERS de forme inconnue"))));
  d = poldegree(GEN);
  C = matrix(n, n); for (i = 1, d, C[i, i] = p);
  for (j = 0, n - 1 - d, my(v = Colrev(GEN * 'y^j, n)); for (i = 1, n, C[i, j + d + 1] = v[i]));
  ok(Str(NOM, " A2 : base C construite depuis (p, GEN) : |det C| = p^", d, " = Q = ", Q, " et C stable par zeta, donc C engendre I"),
     abs(matdet(C)) == p^d && Q == p^d && denominator(content(matsolve(C, Mz * C))) == 1);
  ok(Str(NOM, " A3 : BASE du fichier engendre le meme module (|det BASE| = Q, C^-1 BASE entiere)"),
     abs(matdet(BASE)) == Q && denominator(content(matsolve(C, BASE))) == 1);
  ok(Str(NOM, " B1 : PM = polynome minimal de zeta + 1/zeta, ALPHA * NU = BETA0 mod PM"),
     PMc == PMmin && Mod(ALPHA * NU - BETA0c, PMc) == 0);
  aL = subst(lift(Mod(ALPHA, PMc)), 'x, zz + 1/zz);
  tr = vector(m, kk, trace(aL * zz^(kk - 1)));
  H = matrix(n, n, i, j, tr[(i - j) % m + 1]);
  G = C~ * H * C;
  ok(Str(NOM, " B2 : G = C~ H C (depuis ALPHA seul) entiere, symetrique, paire"),
     denominator(content(G)) == 1 && G == G~ && vecsum(vector(n, i, G[i, i] % 2)) == 0);
  ok(Str(NOM, " B3 : det G = 1"), matdet(G) == 1);
  ok(Str(NOM, " B4 : G definie positive (qfsign exact)"), qfsign(G) == [n, 0]);
  ok(Str(NOM, " B5 : GRAM du fichier = BASE~ H BASE (provenance)"), type(GRAM) == "t_MAT" && BASE~ * H * BASE == GRAM);
  TYPE = typ;
}
