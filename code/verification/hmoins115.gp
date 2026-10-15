default(breakloop, 0);
/* hmoins115.gp -- (note, prop. 2.2) h^-(Q(zeta_115)) par la formule analytique, en arithmétique EXACTE (sans GRH).
   h^- = Q * w * prod_{chi impair} (-B_{1,chi}/2), Q = 2 (115 non puissance de premier), w = 2*115 = 230,
   B_{1,chi} = (1/f) sum_{a=1}^{f} chi_f(a) a, chi_f caractère primitif associé (conducteur f).
   (Z/115)^x = (Z/5)^x x (Z/23)^x, générateurs 2 mod 5 et 5 mod 23 ; chi_{i,j}(a) = z4^(i ind5 a) z22^(j ind23 a) dans Q(zeta_44).
   chi(-1) = (-1)^(i+j) ; conducteur 5^[i!=0] 23^[j!=0].
   Contrôle : la même fonction générale hm redonne h^-(87) = 1536, h^-(65) = 64 et h^-(85) = 6205.
   Usage (depuis la racine du dépôt) : gp -q code/verification/hmoins115.gp < /dev/null */
{
hm(p, q, gp_, gq_) =
  /* m = p*q, p, q premiers impairs distincts, gp_, gq_ racines primitives mod p, mod q */
  my(m = p * q, a1 = p - 1, a2 = q - 1, N = lcm(a1, a2), PhiN = polcyclo(N, 'w), W = Mod('w, PhiN), e1 = N / a1, e2 = N / a2,
     ind1 = vector(p - 1), ind2 = vector(q - 1), prodB = Mod(1, PhiN), nimp = 0);
  for (k = 0, a1 - 1, ind1[lift(Mod(gp_, p)^k)] = k);
  for (k = 0, a2 - 1, ind2[lift(Mod(gq_, q)^k)] = k);
  for (i = 0, a1 - 1, for (j = 0, a2 - 1,
    my(s1 = ind1[p - 1], s2 = ind2[q - 1], f, B = 0);
    /* chi(-1) = W^(e1 i s1 + e2 j s2) */
    if (W^(e1 * i * s1 + e2 * j * s2) != -1, next);
    nimp++;
    f = if (i, p, 1) * if (j, q, 1);
    for (a = 1, f, if (gcd(a, f) == 1,
      my(ch = W^(e1 * i * if (i, ind1[a % p], 0) + e2 * j * if (j, ind2[a % q], 0)));
      B += ch * a));
    B /= f;
    prodB *= -B / 2));
  my(r = lift(prodB));
  if (poldegree(r) > 0, error("produit non rationnel"));
  r = polcoeff(r, 0);
  [nimp, 2 * 2 * m * r];
}
print("m = 3*29 = 87 : [nb chi impairs, h^-] = ", hm(3, 29, 2, 2), "   (attendu 1536)");
print("m = 5*13 = 65 : ", hm(5, 13, 2, 2));
print("m = 5*17 = 85 : ", hm(5, 17, 2, 3));
print("m = 5*23 = 115 : ", hm(5, 23, 2, 5));
H = hm(5, 23, 2, 5)[2];
print("factorisation de h^-(115) : ", factor(H));
quit
