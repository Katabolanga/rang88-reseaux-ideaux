/* verifier_temoins.gp -- rejeu EXACT des huit temoins de norme 6 (note, prop. 6.1 et tableau 2) ; aucun bnfinit, aucune
   donnee de session.  Pour chaque fichier data/rejets/temoin_*.gp (donnees : affectations seulement), controle :
   (1) PM est le polynome minimal de zeta + 1/zeta ; ALPHA = BETA0 / NU dans Q[x]/PM ; PM et BETA0 sont ceux de
       data/corps/rang88_m115c0_data.txt ;
   (2) BASE est une Z-base d'un ideal entier I de Z[zeta] : colonnes entieres, |det| = NORME_ABS_I = produit des p^f,
       stabilite par multiplication par zeta (BASE^-1 * Mzeta * BASE entiere) ; I contient p ; pour un premier de
       degre 1 donne par [p, r], y - r est dans I ;
   (3) GRAM = BASE~ * H * BASE avec H[i, j] = Tr_{L/Q}(alpha zeta^(i - j)) recalcule ; GRAM entiere, paire, det 1,
       definie positive (qfsign exact) ;
   (4) X entier non nul, X~ * GRAM * X = NORME = 6, et Z = BASE * X.
   Usage (depuis la racine du depot) :
     gp -q -D parisize=400000000 code/verification/verifier_temoins.gp < /dev/null      (environ 1 min) */
default(breakloop, 0);
m = 115; n = 88; Phi = polcyclo(m, 'y); z = Mod('y, Phi);
DATC = read("data/corps/rang88_m115c0_data.txt");
Mz = matrix(n, n, i, j, i == j + 1); Mz[, n] = -Colrev(Phi - 'y^n, n);   /* multiplication par zeta, base des puissances */
FICHIERS = ["temoin_P461r5.gp", "temoin_P691r4.gp", "temoin_P1151r6.gp", "temoin_P1381r21.gp", "temoin_P1471d2.gp", "temoin_P829d2.gp", "temoin_P1289d2.gp", "temoin_P1979d2.gp"];
nvalides = 0; ok = 1;
chk(c, s) = if (!c, ok = 0; print("  ECHEC : ", s));
{
for (kf = 1, #FICHIERS,
  F = Str("data/rejets/", FICHIERS[kf]);
  read(F);
  ok = 1;
  chk(PM == minpoly(z + 1/z, 'x), "PM");
  chk(PM == DATC[1] && BETA0 == DATC[2], "PM et BETA0 = data/corps");
  chk(Mod(ALPHA, PM) == Mod(BETA0, PM) / Mod(NU, PM), "ALPHA = BETA0/NU");
  aL = Mod(subst(ALPHA, 'x, 'y + 1/'y), Phi);
  chk(matsize(BASE) == [n, n] && denominator(content(BASE)) == 1, "BASE entiere");
  chk(abs(matdet(BASE)) == NORME_ABS_I, "det BASE = N(I)");
  chk(NORME_ABS_I == prod(k = 1, #PREMIERS, PREMIERS[k][1]^if (#PREMIERS[k] == 3, PREMIERS[k][2], 1)), "N(I) = prod p^f");
  chk(Mz * vector(n, j, j == 2)~ == vector(n, j, j == 3)~, "Mzeta");
  T = matsolve(BASE, Mz * BASE); chk(denominator(content(T)) == 1, "I stable par zeta");
  foreach(PREMIERS, pr, chk(denominator(content(matsolve(BASE, pr[1] * matid(n)))) == 1, Str("p = ", pr[1], " dans I")));
  if (#PREMIERS == 1 && #PREMIERS[1] == 2, chk(denominator(content(matsolve(BASE, Colrev('y - PREMIERS[1][2], n)))) == 1, "y - r dans I"));
  t = vector(m, k, trace(aL * z^(k - 1)));
  H = matrix(n, n, i, j, t[(i - j) % m + 1]);
  G = BASE~ * H * BASE;
  chk(G == GRAM, "GRAM recalculee");
  chk(denominator(content(G)) == 1, "GRAM entiere");
  chk(vecsum(vector(n, i, G[i, i] % 2)) == 0, "GRAM paire");
  chk(matdet(G) == 1, "det GRAM = 1");
  chk(qfsign(G) == [n, 0], "definie positive");
  chk(type(X) == "t_COL" && #X == n && denominator(content(X)) == 1 && X != 0, "X entier non nul");
  N = qfeval(G, X); chk(N == NORME && N == 6, "norme 6");
  chk(Polrev(BASE * X, 'y) == Z, "Z = BASE * X");
  if (ok, nvalides++);
  printf("%s (%s) : %s ; norme du temoin = %d ; I d'indice %d dans Z[zeta]\n", NOM, FICHIERS[kf],
         if (ok, "TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal)", "ECHEC"), N, NORME_ABS_I));
printf("BILAN : %d temoins valides sur %d\n", nvalides, #FICHIERS);
}
quit
