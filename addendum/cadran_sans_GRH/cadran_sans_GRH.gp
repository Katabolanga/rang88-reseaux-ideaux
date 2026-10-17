/* cadran_sans_GRH.gp -- les etiquettes (heures) du cadran de la couche sigma24, SANS GRH.  Claude, 17 octobre 2026.

   PRINCIPE.  Cl_331(L) est cyclique d'ordre 331 (note, prop. 2.2, sans GRH) et engendre par [P139]_331 (P139^3 non principal).
   Pour un ideal I de L dont la classe est fixee par sigma_24, avec N_{L/K}(I) = q^e (K = K22 = Q(theta), q premier de degre 1),
   on veut l'unique c dans F_331 tel que [I]_331 = c [P139]_331.  Soit Gamma_q un generateur de q^331 (TROUVE par bnfinit sous
   GRH, puis VERIFIE exactement : (Gamma_q) = q^331), et lambda le vecteur des logarithmes discrets modulo 331 aux 88 premiers de
   degre 1 de K au-dessus de l = 380651, 1065821, 1522601, 2055511 (tous = 1 mod 331*115).  Soit U l'image des unites xi_2..xi_11.
   (1) phi : classe de [a] -> lambda(Gamma_a) mod U est un morphisme bien defini sur le groupe engendre par les q (si prod q_i^{a_i}
       = (delta), alors prod Gamma_i^{a_i} = epsilon delta^331 et sum a_i lambda(Gamma_i) est dans lambda(E) = U, car l'indice de
       <-1, xi_2, ..., xi_11> dans E est premier a 331 : etape 1 de la note, par le rang 10).
   (2) (v2, apres la contrelecture d'Astra du 17 oct.) N_{L/K}[I] = [q]^e est d'ordre divisant 331 ; les normes des composantes 3
       et 45013 de [I] sont d'ordres premiers a 331, donc nulles par unicite de la decomposition primaire de Cl(K) ; ainsi
       phi(N[I]) = e lambda(Gamma_q) mod U et phi(N[P139]) = 2 lambda(Gamma_139) mod U ; si [I]_331 = c [P139]_331, alors
       e lambda(Gamma_q) = 2c lambda(Gamma_139) mod U.  Ni j o N ni le groupe Cl(K) complet ne servent.  q doit etre premier aux
       quatre premiers auxiliaires (verifie ici : p n'est pas l'un d'eux), et toute classe contient des ideaux premiers a eux.
   (3) [U | lambda(Gamma_139)] est de rang 11 (verifie ici) : c est donc DETERMINE par la resolution du systeme lineaire mod 331.
   L'heure h est definie par c dans 2^h mu_22 (mu_22 = image de chi_331).  La composante 3 de [I] est lue par 4p = a^2 + 23 b^2.
   SANS GRH : maximalite de l'ordre (nfcertify), (Gamma_q) = q^331 par egalite exacte d'ideaux, unites (norme +-1, entieres),
   logarithmes discrets et algebre lineaire exacts mod 331.  GRH ne sert qu'a TROUVER les Gamma_q (bnfisprincipal).
   On compare enfin aux etiquettes o331 du recensement R1 (calculees sous GRH dans Cl(K22)).
   Lancer depuis ce dossier : gp -q cadran_sans_GRH.gp < /dev/null */
default(parisizemax, 4 * 10^9);
m = 115; Phi = polcyclo(m, 'y); z = Mod('y, Phi);
th = z + z^22 + z^24 + z^68;
P22 = minpoly(th, 'w);
nf = nfinit(P22);
NB = 0; NOK = 0;
ok(nom, c) = NB++; if (c, NOK++); printf("%s %s\n", if (c, "OK   ", "ECHEC"), nom);
ok("ordre maximal de K22 certifie (nfcertify)", #nfcertify(nf) == 0);
/* unites xi_a et Gamma_139 : lues dans le certificat de P139 (paru avec la note), puis reverifiees ici */
P22ref = P22;
CERT = "C:/Users/ivang/Desktop/DeBoreAh/PREMIERS/AnacondaSpyder/conversations636_02072026/Conversations705/16_CONVERSATIONS_PDF_ET_ANNEXES/_UNIFICATION_CLAUDE_20260925/23_DEPOT_PUBLIC_RANG88/verification_P4969/data/P139/certificat_K22.txt";
foreach(readstr(CERT), s, if (#s, eval(s)));
ok("certificat P139 : meme polynome P22", P22 == P22ref);
GAM139 = GAMMA; R139 = RACINE;
XI = vector(10, i, eval(Str("XI_", i + 1)));
{
for (i = 1, 10,
  my(x = Mod(XI[i], P22));
  ok(Str("xi_", i + 1, " entier algebrique de norme +-1"), denominator(content(nfalgtobasis(nf, x))) == 1 && abs(norm(x)) == 1));
}
/* ideaux q */
rac1(p, r) = lift(subst(lift(th), 'y, Mod(r, p)));
{
rac2(p, g) =
  my(u = lift(lift(Mod(lift(th), g * Mod(1, p)))));
  if (poldegree(u) > 0, error("theta mod P"));
  lift(polcoef(u, 0) * Mod(1, p));
}
{
deg2(p) =
  my(F = factormod(Phi, p)[, 1]);
  for (i = 1, #F, if (poldegree(F[i]) == 2, return(lift(F[i]))));
  error("pas de facteur de degre 2");
}
qideal(p, r) = my(Q = idealhnf(nf, p, 'w - r)); if (idealnorm(nf, Q) != p, error("norme de q")); Q;
repr(N) = for (b = 0, sqrtint(N \ 23), my(t = N - 23 * b^2); if (issquare(t), return([sqrtint(t), b]))); 0;
/* recherche des generateurs (SOUS GRH, recherche seulement) */
bnf = bnfinit(P22, 1);
{
gen331(Q) =
  my(A = idealpow(nf, Q, 331), r = bnfisprincipal(bnf, A, 1), g);
  if (r[1] != 0 * r[1], error("q^331 non principal ?"));
  g = nfbasistoalg(nf, r[2]);
  if (idealhnf(nf, g) != A, error("generateur faux"));
  lift(g);
}
ok("Gamma_139 : (Gamma_139) = q_139^331, egalite exacte d'ideaux", idealhnf(nf, Mod(GAM139, P22)) == idealpow(nf, qideal(139, R139), 331));
/* logarithmes discrets mod 331 aux 88 premiers auxiliaires */
LL = [380651, 1065821, 1522601, 2055511];
ok("premiers auxiliaires : premiers, = 1 mod 331*115", prod(i = 1, 4, isprime(LL[i]) && LL[i] % (331 * 115) == 1));
PL = List();
{
foreach(LL, l,
  my(rts = polrootsmod(P22, l), g = znprimroot(l), e = (l - 1) / 331);
  if (#rts != 22, error("l non totalement decompose"));
  foreach(rts, rho, listput(PL, [l, lift(rho), g^e, e])));
}
PL = Vec(PL);
ok("88 premiers de degre 1 au-dessus des 4 premiers auxiliaires", #PL == 88);
{
lam(x) =
  vector(88, i, my(l = PL[i][1], v, d = denominator(content(x)));
    if (d % l == 0, error("denominateur"));
    v = subst(x, 'w, Mod(PL[i][2], l));
    if (v == 0, error("pas une unite en l"));
    znlog(v^PL[i][4], PL[i][3], 331));
}
U = matrix(88, 10, i, j, 0); LU = vector(10, j, lam(XI[j])); for (j = 1, 10, for (i = 1, 88, U[i, j] = LU[j][i]));
L139 = lam(GAM139);
A = Mod(matconcat([U, L139~]), 331);
ok("unites : rang 10 modulo 331", matrank(Mod(U, 331)) == 10);
ok("[unites | Gamma_139] : rang 11 modulo 331", matrank(A) == 11);
/* table des heures : o331 de R1 -> heure */
HEURE_DE = Map(); foreach([[1,0],[2,1],[4,2],[8,3],[16,4],[32,5],[7,6],[14,7],[28,8],[56,9],[13,10],[5,11],[10,12],[20,13],[19,14]], v, mapput(HEURE_DE, v[1], v[2]));
heure(c) = for (h = 0, 14, if ((Mod(c, 331) * Mod(2, 331)^(-h))^22 == 1, return(h))); -1;
/* cibles : [nom, sorte, donnees, o331 de R1 (sous GRH) ou -1]  ; sorte "a" : premier de degre 2 (e = 2) ;
   "b" : P sigma24(P), P = (p, zeta - r) (e = 2) ; "c" : premier de degre 1 (e = 1) */
{CIBLES = [
 ["P139", "a", 139, 1], ["P599", "a", 599, 28], ["P691s24", "b", [691, 4], 20], ["P829", "a", 829, 32],
 ["P1151s24", "b", [1151, 6], 7], ["P1289", "a", 1289, 14], ["P1979", "a", 1979, 16], ["P2531s24", "b", [2531, 12], 10],
 ["P3359", "a", 3359, 4], ["P3911s24", "b", [3911, 24], 8], ["P4049", "a", 4049, 28], ["P4831s24", "b", [4831, 39], 5],
 ["P4969", "a", 4969, 20], ["P5981s24", "b", [5981, 16], 5], ["P6211s24", "b", [6211, 9], 7], ["P7591s24", "b", [7591, 52], 56],
 ["P8419", "a", 8419, 32], ["P8741s24", "b", [8741, 226], 13], ["P8971s24", "b", [8971, 177], 19], ["P9109", "a", 9109, 8],
 ["P9431s24", "b", [9431, 47], 4], ["P9661s24", "b", [9661, 19], 2], ["P14951s24", "b", [14951, 2], 19], ["P15319", "a", 15319, 16],
 ["P17389", "a", 17389, 13], ["P18401s24", "b", [18401, 22], 2], ["P23599", "a", 23599, 14], ["P33581s24", "b", [33581, 83], 56],
 ["P39239", "a", 39239, 10], ["P53269", "a", 53269, 1],
 ["P5659", "a", 5659, 5], ["P461s24", "b", [461, 5], 1], ["P1381s24", "b", [1381, 21], 14], ["P3221s24", "b", [3221, 20], 16],
 ["P5521s24", "b", [5521, 34], 32], ["P157146581", "c", [157146581, 890366], 13],
 ["P139pub", "A", [139, [77, 1]], 1], ["P599pub", "A", [599, [322, 87]], 28], ["P4969pub", "A", [4969, [2809, 3763]], 20],
 ["P4049pub", "A", [4049, [2084, 105]], 28]];}
/* sorte "A" : premier de degre 2 DONNE, P = (p, zeta^2 + g1 zeta + g0) : les ideaux de la note et de l'addendum (X139, X599,
   X4969, X4049) ; l'etiquette c depend du conjugue choisi (a mu_22 pres), l'heure n'en depend pas. */
RES = List();
F = fileopen("cadran_sans_GRH_certificats.txt", "w");
filewrite(F, "# une ligne par cible : nom|sorte|p|lien|r|e|c|Gamma ; lien = g0,g1 (P = (p, y^2 + g1 y + g0), sortes a, A) ou rP (P = (p, y - rP), sortes b, c) ; q = (p, theta - r) ; (Gamma) = q^331 ; [I]_331 = c [P139]_331");
{
foreach(CIBLES, C,
  my(nom = C[1], s = C[2], p, r, e, Q, G, Lq, x, c, t3, h, hR, sol, g, lien);
  if (s == "a" || s == "A",
    if (s == "a", p = C[3]; g = deg2(p), p = C[3][1]; g = 'y^2 + C[3][2][2] * 'y + C[3][2][1]);
    if (poldegree(g) != 2 || polcoef(g, 2) != 1 || !polisirreducible(g * Mod(1, p)) || lift(Phi * Mod(1, p)) % (g * Mod(1, p)) != 0, error(Str(nom, " : g")));
    r = rac2(p, g); e = 2; lien = Str(lift(polcoef(g, 0) * Mod(1, p)), ",", lift(polcoef(g, 1) * Mod(1, p))),
    p = C[3][1]; if (subst(Phi, 'y, Mod(C[3][2], p)) != 0, error(Str(nom, " : racine"))); r = rac1(p, C[3][2]); e = if (s == "b", 2, 1); lien = Str(C[3][2]));
  Q = qideal(p, r);
  G = if (p == 139 && r == R139, GAM139, gen331(Q));
  ok(Str(nom, " : (Gamma_q) = q^331 exactement, q = (", p, ", theta - ", r, "), p distinct des premiers auxiliaires"), idealhnf(nf, Mod(G, P22)) == idealpow(nf, Q, 331) && !setsearch(Set(LL), p));
  Lq = lam(G);
  /* e lambda(Gamma_q) = 2 c lambda(Gamma_139) mod U  <=>  lambda(Gamma_q) = (2c/e) lambda(Gamma_139) mod U */
  sol = matinverseimage(A, Mod(Lq~, 331));
  if (#sol == 0, ok(Str(nom, " : systeme mod 331 compatible"), 0); next);
  x = lift(sol[11]); c = lift(Mod(x * e, 331) / 2);
  t3 = if (repr(4 * p), 0, 1);
  h = heure(c); hR = if (C[4] > 0, mapget(HEURE_DE, C[4]), -1);
  ok(Str(nom, " : c = ", c, " (non nul), heure SANS GRH = ", h, " ; heure de R1 (GRH) = ", hR, " ; ", if (s == "c", Str("composantes 3 et 331 ", if (t3, "non nulles", ": 3 nulle, 331 non nulle"), ", composante 45013 NON verifiee (sous GRH)"), Str("support ", if (t3, "{3,331}", "{331}")))), c != 0 && h >= 0 && h == hR);
  filewrite(F, Str(nom, "|", s, "|", p, "|", lien, "|", r, "|", e, "|", c, "|", G));
  listput(RES, [nom, p, t3, c, h, hR]));
}
fileclose(F);
print();
print("BILAN DES ETIQUETTES (c : [I]_331 = c [P139]_331 ; heure h : c dans 2^h mu_22) :");
foreach(RES, v, printf("  %-12s p = %-10d support %-10s c = %3d  heure %2d   (R1 sous GRH : %2d)\n", v[1], v[2], Str(if (v[3], "{3,331}", "{331}"), if (v[1] == "P157146581", "*", "")), v[4], v[5], v[6]));
print("  (*) premier de degre 1 de R2 : composantes 3 et 331 certifiees ; l'annulation de la composante 45013 reste sous GRH.");
/* GP poursuit apres une erreur de commande : le verdict exige donc le nombre COMPLET de controles et de cibles traitees.
   Controles attendus : 2 (ordre, P22) + 10 (unites) + 1 (Gamma_139) + 2 (premiers auxiliaires) + 2 (rangs) + 2 par cible. */
NATT = 17 + 2 * #CIBLES;
printf("BILAN : %d controles (attendus %d), %d echecs ; %d cibles traitees sur %d\n", NB, NATT, NB - NOK, #RES, #CIBLES);
VERDICT = (NOK == NB && NB == NATT && #RES == #CIBLES);
print(if (VERDICT, "CADRAN_SANS_GRH_OK", "CADRAN_SANS_GRH_ECHEC"));
quit(if (VERDICT, 0, 1))
