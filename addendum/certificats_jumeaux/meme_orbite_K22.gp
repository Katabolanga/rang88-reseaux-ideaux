/* meme_orbite_K22.gp -- certificats « meme orbite » sans GRH pour les tests d'invariance (Claude, 17 octobre 2026).
   Meme methode que jumeaux_K22.gp : un delta de K22 avec (delta) = q_a^2 tau(q_b)^(-2) donne des composantes 331 conjuguees ;
   si de plus les composantes 3 sont toutes deux non nulles (ou toutes deux nulles), les deux classes fixees par sigma_24 sont
   dans la MEME orbite (pour un support donne, l'orbite est determinee par celle de la composante 331).
   Composante 3 de [P_p], p = 1 mod 23 : nulle si et seulement si 4p = a^2 + 23 b^2 ; celle de [P sigma24(P)] est le double.
   Paires : (P139, P461 s24), (P1289, P1381 s24), (P1979, P3221 s24), (P829, P5521 s24).
   Lancer : gp -q meme_orbite_K22.gp < /dev/null */
default(parisizemax, 4 * 10^9);
m = 115; Phi = polcyclo(m, 'y); z = Mod('y, Phi);
th = z + z^22 + z^24 + z^68;
P22 = factor(charpoly(th, 'x))[1, 1];
nf = nfinit(P22);
if (#nfcertify(nf), error("ordre maximal"));
rac1(p, r) = lift(subst(lift(th), 'y, Mod(r, p)));
{
rac2(p, g) =
  my(u = lift(lift(Mod(lift(th), g * Mod(1, p)))));
  if (poldegree(u) > 0, error("theta mod P"));
  lift(polcoef(u, 0) * Mod(1, p));
}
qideal(p, r) = my(Q = idealhnf(nf, p, 'x - r)); if (idealnorm(nf, Q) != p, error("norme")); Q;
repr(N) = for (b = 0, sqrtint(N \ 23), my(t = N - 23 * b^2); if (issquare(t), return([sqrtint(t), b]))); 0;
gal = nfgaloisconj(nf);
bnf = bnfinit(P22, 1);
{
cert(na, qa, nb, qb) =
  my(A2 = idealpow(nf, qa, 2), tq, A, r, de);
  for (i = 1, #gal,
    tq = nfgaloisapply(nf, gal[i], qb);
    A = idealdiv(nf, A2, idealpow(nf, tq, 2));
    r = bnfisprincipal(bnf, A);
    if (r[1] == 0 * r[1] && #r[2],
      de = nfbasistoalg(nf, r[2]);
      if (idealhnf(nf, de) == A && abs(norm(de)) == (idealnorm(nf, qa) / idealnorm(nf, tq))^2,
        printf("%s ~ %s : tau numero %d ; (delta) = q_a^2 tau(q_b)^-2 VERIFIE sans GRH (delta : %d chiffres)\n", na, nb, i, #Str(de));
        /* v2 (contrelecture d'Astra, 17 oct.) : le delta est exporte, comme dans jumeaux_K22_certificats.txt */
        Fc = fileopen("meme_orbite_K22_certificats.txt", "a");
        filewrite(Fc, Str(na, "|", nb, "|tau=", i, "|delta=", lift(de)));
        fileclose(Fc);
        return(1))));
  printf("%s ~ %s : aucun certificat trouve\n", na, nb);
  0;
}
{
foreach([139, 461, 1289, 1381, 1979, 3221, 829, 5521], p,
  my(s = repr(4 * p));
  printf("p = %5d : p mod 23 = %d ; 4p = a^2 + 23 b^2 : %s => composante 3 de [P_p] %s\n", p, p % 23, if (s, Str(s), "non"), if (s, "NULLE", "non nulle")));
}
{
qdeg2(p) =
  my(F = factormod(Phi, p)[, 1], g = 0);
  for (i = 1, #F, if (poldegree(F[i]) == 2, g = lift(F[i]); break));
  qideal(p, rac2(p, g));
}
qdeg1(p, r) = if (subst(Phi, 'y, Mod(r, p)) != 0, error("r")); qideal(p, rac1(p, r));
{
qs24(p, r) =
  my(q1 = qdeg1(p, r), q2 = qdeg1(p, lift(Mod(r, p)^24)));
  if (q1 != q2, error("sigma24(P) et P n'ont pas la meme trace sur K22"));
  q1;
}
F0 = fileopen("meme_orbite_K22_certificats.txt", "w"); filewrite(F0, "# certificats de meme orbite : q_a|q_b|tau=i (gal = nfgaloisconj(nfinit(P22)))|delta (polynome en x = theta, P22 = polynome minimal de theta) avec (delta) = q_a^2 tau(q_b)^-2"); fileclose(F0);
c1 = cert("q139",  qdeg2(139),  "q461 (s24)",  qs24(461, 5));
c2 = cert("q1289", qdeg2(1289), "q1381 (s24)", qs24(1381, 21));
c3 = cert("q1979", qdeg2(1979), "q3221 (s24)", qs24(3221, 20));
c4 = cert("q829",  qdeg2(829),  "q5521 (s24)", qs24(5521, 34));
printf("BILAN : %d certificats sur 4\n", c1 + c2 + c3 + c4);
quit(if (c1 + c2 + c3 + c4 == 4, 0, 1))
