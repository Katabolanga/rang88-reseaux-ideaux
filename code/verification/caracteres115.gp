default(breakloop, 0);
/* caracteres115.gp -- (note, prop. 2.5 et tableau 1) structure galoisienne de Cl(Q(zeta_115)) SANS GRH.
   h = h^- h^+ = 44 697 909 * 1 (h^+ = 1 : Miller 2014) = 3 * 331 * 45013, sans facteur carré : Cl cyclique.
   Pour p | h (p ne divise pas 88), Cl_p = F_p est un espace propre A_chi pour un caractère impair chi ; par Stickelberger
   (B_{1,chi^-1} annule A_chi), p doit diviser la norme de B_{1,chi^-1}/2.  On calcule, pour chaque classe de conjugaison
   rationnelle de caractères impairs, N(B_{1,chi}/2) en arithmétique exacte, puis on compte les orbites galoisiennes sur Cl
   (Burnside) et sur S (= Cl, fibres de cardinal 1).
   Usage (depuis la racine du dépôt) : gp -q code/verification/caracteres115.gp < /dev/null */
p1 = 5; q1 = 23; g1 = 2; g2 = 5; m = 115;
a1 = p1 - 1; a2 = q1 - 1; NN = lcm(a1, a2); PhiN = polcyclo(NN, 'w); W = Mod('w, PhiN); e1 = NN / a1; e2 = NN / a2;
ind1 = vector(p1 - 1); ind2 = vector(q1 - 1);
for (k = 0, a1 - 1, ind1[lift(Mod(g1, p1)^k)] = k);
for (k = 0, a2 - 1, ind2[lift(Mod(g2, q1)^k)] = k);
chiv(i, j, a) = W^(e1 * i * if (i, ind1[a % p1], 0) + e2 * j * if (j, ind2[a % q1], 0));
{
B1(i, j) = my(f = if (i, p1, 1) * if (j, q1, 1), B = 0);
  for (a = 1, f, if (gcd(a, f) == 1, B += chiv(i, j, a) * a)); B / f;
}
ordch(i, j) = lcm(a1 / gcd(i, a1), a2 / gcd(j, a2));
/* classes rationnelles : (i, j) ~ (k i, k j), k premier à NN */
{
vu = Set(); CL = List(); prodtot = 1;
for (i = 0, a1 - 1, for (j = 0, a2 - 1,
  if ((i + j) % 2 == 0, next);   /* chi(-1) = (-1)^(i + j), contrôlé ci-dessous */
  if (setsearch(vu, [i, j]), next);
  my(orb = Set(vector(NN, k, if (gcd(k, NN) == 1, [(k * i) % a1, (k * j) % a2], [i, j]))), d = ordch(i, j), B = B1(i, j), Nm, f);
  if (chiv(i, j, m - 1) != -1, error("caractere non impair"));
  vu = setunion(vu, orb);
  /* norme de B/2 de Q(zeta_d) à Q : produit sur l'orbite */
  Nm = prod(t = 1, #orb, B1(orb[t][1], orb[t][2]) / 2);
  Nm = lift(Nm); if (poldegree(Nm) > 0, error("norme")); Nm = polcoeff(Nm, 0);
  prodtot *= Nm;
  f = if (i, p1, 1) * if (j, q1, 1);
  listput(CL, [[i, j], d, f, #orb, Nm]);
  printf("chi_(%d,%d) : ordre %d, conducteur %d, %d conjugues ; N(-B1/2) = %s = %s\n", i, j, d, f, #orb, Nm, if (Nm == 0, 0, factor(abs(Nm))))));
printf("produit des normes * Q * w = %s (attendu 44697909)\n", prodtot * 2 * 230);
}
/* caractères responsables de 3, 331, 45013 */
{
PR = [3, 331, 45013]; RESP = vector(3);
for (t = 1, 3, my(p = PR[t], L = select(c -> c[5] % p == 0, Vec(CL)));
  printf("p = %d : classes de caracteres avec p | N(B1/2) : %s\n", p, apply(c -> [c[1], c[2], c[3], valuation(c[5], p)], L));
  if (#L == 1 && valuation(L[1][5], p) == 1, RESP[t] = L[1], error("cas non simple")));
}
/* action de (Z/115)^x sur Cl_p = F_p : a -> chi(a) mod un premier au-dessus de p ; la taille des orbites ne dépend que du
   noyau de chi (pas du choix du conjugué).  Noyaux et orbites (Burnside sur Cl = F_3 x F_331 x F_45013). */
G = select(a -> gcd(a, m) == 1, [1 .. m - 1]);
ker(c) = Set(select(a -> chiv(c[1][1], c[1][2], a) == 1, G));
K = vector(3, t, ker(RESP[t]));
for (t = 1, 3, printf("p = %d : chi d'ordre %d, conducteur %d, |noyau| = %d ; corps fixe de degre %d\n", PR[t], RESP[t][2], RESP[t][3], #K[t], 88 / #K[t]));
{
/* nombre d'orbites par support S ⊂ {3, 331, 45013} : prod_{p in S} (p - 1) / |G / inter_{p in S} ker| */
tot = 0; totel = 0;
forvec(s = vector(3, t, [0, 1]),
  my(S = select(t -> s[t], [1, 2, 3]), Kint = Set(G), nel = 1, osz, no);
  foreach(S, t, Kint = setintersect(Kint, K[t]); nel *= PR[t] - 1);
  osz = 88 / #Kint; no = nel / osz;
  if (denominator(no) != 1, error("orbites"));
  tot += no; totel += nel;
  printf("support %s : %d classes, orbites de taille %d, %d orbites\n", apply(t -> PR[t], S), nel, osz, no));
printf("TOTAL : %d classes (attendu 44697909), %d orbites galoisiennes dans S\n", totel, tot);
}
/* Burnside direct (contrôle) */
{
bur = sum(k = 1, #G, my(a = G[k]); prod(t = 1, 3, if (setsearch(K[t], a), PR[t], 1)));
printf("Burnside : (1/88) sum |Fix| = %s\n", bur / 88);
}
quit
