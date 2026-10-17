/* jumeaux_K22.gp -- certificats de JUMELAGE sans GRH (Claude, 17 octobre 2026).
   Deux classes c, c' de L = Q(zeta_115) fixees par sigma_24 sont JUMELLES si leurs composantes 331 sont dans la meme orbite de Galois.
   K = K22 = Q(theta), theta = zeta + zeta^22 + zeta^24 + zeta^68 (fixe de <sigma_22>) ; pour un ideal I de L stable par sigma_24,
   N_{L/K}(I) = q^2 avec q premier de degre 1 de K.  Si un element delta de K verifie (delta) = q_a^2 * tau(q_b)^(-2) pour un tau de
   Gal(K/Q), alors [q_a^2] = tau[q_b^2] dans Cl(K) ; comme j o N_{L/K} = 4 sur la composante 331 de Cl(L) (j : extension des ideaux),
   les composantes 331 de [I_a] et sigma[I_b] sont egales (sigma relevant tau) : I_a et I_b sont jumelles.
   RECHERCHE : bnfinit / bnfisprincipal (SOUS GRH) ne servent qu'a TROUVER tau et delta.
   VERIFICATION : sans bnf -- ordre maximal certifie (nfcertify), facteurs premiers, valuations de delta (idealval) et norme exacte.
   Paires traitees : (P4969, P691 . sigma24(P691)) et (P4049, P599).
   Lancer : gp -q jumeaux_K22.gp < /dev/null */
default(parisizemax, 4 * 10^9);
m = 115; Phi = polcyclo(m, 'y); z = Mod('y, Phi);
th = z + z^22 + z^24 + z^68;
f = charpoly(th, 'x); Ff = factor(f);
if (#Ff[, 1] != 1 || Ff[1, 2] != 4 || poldegree(Ff[1, 1]) != 22, error("charpoly de theta"));
P22 = Ff[1, 1];
printf("P22 = polynome minimal de theta (degre 22) ; charpoly(theta) = P22^4\n");
nf = nfinit(P22);
cert = nfcertify(nf);
printf("nfinit : disc(K) = %s ; nfcertify = %s (liste vide : ordre maximal certifie)\n", factor(nf.disc), cert);
if (#cert, error("ordre maximal non certifie"));
/* image de theta modulo un ideal premier P de L : degre 1 (p, zeta - r) ou degre 2 (p, g(zeta)) */
rac1(p, r) = lift(subst(lift(th), 'y, Mod(r, p)));
{
rac2(p, g) =
  my(t = Mod(lift(th), g * Mod(1, p)), u = lift(lift(t)));
  if (poldegree(u) > 0, error("theta mod P hors de F_p"));
  lift(polcoef(u, 0) * Mod(1, p));
}
qideal(p, r) = my(Q = idealhnf(nf, p, 'x - r)); if (idealnorm(nf, Q) != p, error("q pas de norme p")); Q;
/* (nom, p, r) des ideaux q = (p, theta - r) de K */
r4969 = rac2(4969, 'y^2 + 3763*'y + 2809);
r4049 = rac2(4049, 'y^2 + 105*'y + 2084);
r599  = rac2(599,  'y^2 + 87*'y + 322);
r691  = rac1(691, 4);
r691b = rac1(691, 596);
printf("theta mod P : P4969 -> %d ; P4049 -> %d ; P599 -> %d ; P691 = (691, zeta - 4) -> %d ; sigma24(P691) = (691, zeta - 596) -> %d\n", r4969, r4049, r599, r691, r691b);
if (r691 != r691b, error("P691 et sigma24(P691) n'ont pas la meme trace sur K"));
if (r4969 != 4770 || r4049 != 512, error("racines differentes des certificats de non-isometrie"));
q4969 = qideal(4969, r4969); q4049 = qideal(4049, r4049); q599 = qideal(599, r599); q691 = qideal(691, r691);
gal = nfgaloisconj(nf);
if (#gal != 22, error("Gal(K/Q)"));
printf("Gal(K/Q) : 22 automorphismes\n");
t0 = getabstime();
bnf = bnfinit(P22, 1);
printf("bnfinit (SOUS GRH, recherche seulement) : Cl(K) = %s  [%d s]\n", bnf.cyc, (getabstime() - t0) \ 1000);
{
jumeau(na, qa, nb, qb) =
  my(A2 = idealpow(nf, qa, 2), trouve = 0, tq, A, r, de, nr, okv, pa, pb, res = 0);
  for (i = 1, #gal,
    tq = nfgaloisapply(nf, gal[i], qb);
    A = idealdiv(nf, A2, idealpow(nf, tq, 2));
    r = bnfisprincipal(bnf, A);
    if (r[1] == 0 * r[1],
      de = nfbasistoalg(nf, r[2]);
      /* VERIFICATION SANS bnf : norme exacte et valuations en tous les premiers au-dessus de a et b */
      nr = norm(de);
      okv = (abs(nr) == (idealnorm(nf, qa) / idealnorm(nf, tq))^2);
      pa = idealprimedec(nf, idealnorm(nf, qa)); pb = idealprimedec(nf, idealnorm(nf, tq));
      foreach(pa, pr, okv = okv && idealval(nf, de, pr) == if (idealhnf(nf, pr) == qa, 2, 0));
      foreach(pb, pr, okv = okv && idealval(nf, de, pr) == if (idealhnf(nf, pr) == tq, -2, 0));
      /* la norme etant +-(a/b)^2, aucun autre premier n'intervient : (delta) = qa^2 tq^-2 exactement */
      okv = okv && (idealhnf(nf, de) == A);
      printf("%s / %s : tau numero %d ; delta trouve (hauteur %d chiffres) ; N(delta) = %s ; verification sans GRH : %s\n",
        na, nb, i, #Str(de), nr, if (okv, "OK", "ECHEC"));
      if (okv, res = [i, de]; break)));
  if (res == 0, printf("%s / %s : AUCUN tau ne donne une classe triviale (pas jumelles, sous GRH)\n", na, nb));
  res;
}
J1 = jumeau("q4969", q4969, "q691", q691);
J2 = jumeau("q4049", q4049, "q599", q599);
writebin("jumeaux_K22.bin", [P22, r4969, r4049, r599, r691, J1, J2]);
{
F = fileopen("jumeaux_K22_certificats.txt", "w");
filewrite(F, "/* certificats de jumelage (PARI/GP) : (delta) = q_a^2 * tau(q_b)^(-2) dans K22 = Q(theta) ; tau = gal[i], gal = nfgaloisconj(nfinit(P22)) */");
filewrite(F, Str("P22 = ", P22, ";"));
filewrite(F, Str("R = [4969, ", r4969, "; 4049, ", r4049, "; 599, ", r599, "; 691, ", r691, "];"));
if (J1, filewrite(F, Str("JUMEAU_4969_691 = [", J1[1], ", ", lift(J1[2]), "];")));
if (J2, filewrite(F, Str("JUMEAU_4049_599 = [", J2[1], ", ", lift(J2[2]), "];")));
fileclose(F);
}
printf("FIN  [%d s]\n", (getabstime() - t0) \ 1000);
quit
