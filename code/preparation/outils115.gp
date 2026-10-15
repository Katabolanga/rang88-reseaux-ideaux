/* code/preparation/outils115.gp — réseaux idéaux (I, Tr_L(alpha z zbar)) sur L = Q(zeta_115), rang 88.
   Unimodulaire <=> alpha N(I) D+ = O+, alpha >> 0 ; alors pair (note, prop. 2.1 ; m n'est pas une puissance de premier).
   Ici Cl(L) est d'ordre impair : la fibre au-dessus de [I] a UN élément ; on prend alpha = beta0 / nu, nu générateur
   totalement positif de N_{L/L+}(I) (beta0 de rang88_m115c0_data.txt, générateur totalement positif de D+^-1).
   Chaque Gram est contrôlée EXACTEMENT : entière, paire, déterminant 1 (indépendant de GRH).
   Paramètre : FBNFP (bnf de K115 sauvegardé par bnf_k115.gp ; GRH, sert seulement à trouver nu).
   */
m = 115; n = 88; nh = 44;
Phi = polcyclo(m, 'y); z = Mod('y, Phi);
DAT = read("data/corps/rang88_m115c0_data.txt"); Pm = DAT[1]; beta0 = Mod(DAT[2], Pm);
bnfp = read(FBNFP); nfp = bnfp.nf;
if (nfp.pol != Pm, error("bnf K115 : mauvais polynome"));
nfL = nfinit([Phi, [5, 23]]);
if (nfL.disc != (-1)^(n / 2) * 5^66 * 23^84 && abs(nfL.disc) != 5^66 * 23^84, print("disc(L) = ", factor(nfL.disc)));
toL(a) = Mod(subst(lift(a), 'x, lift(z + 1/z)), Phi);          /* élément de L+ (polynôme en x = c) -> L */
/* signes, unités, générateur totalement positif (comme classes_gen.gp) */
Up = concat([Mod(-1, Pm)], vector(#bnfp.fu, j, Mod(lift(bnfp.fu[j]), Pm)));
nu_ = #Up;
bits(s) = apply(t -> (1 - t) / 2, s);
S2 = matrix(nu_, nh, j, i, bits(nfeltsign(nfp, Up[j]))[i]) * Mod(1, 2);
{
totpos(w) = my(s = bits(nfeltsign(nfp, w)) * Mod(1, 2), c = matinverseimage(S2~, s~), u = Mod(1, Pm));
  if (#c == 0, error("pas de generateur totalement positif"));
  for (j = 1, nu_, if (lift(c[j]), u *= Up[j]));
  w * u;
}
/* idéal premier de degré 1 de L au-dessus de p = 1 mod 115, donné par la racine r de Phi mod p : P = (p, y - r) ;
   sa norme dans L+ est (p, x - (r + 1/r)). */
primeL(p, r) = idealhnf(nfL, p, Mod('y - r, Phi));
primeLp(p, r) = idealhnf(nfp, p, Mod('x - lift(Mod(r, p) + 1 / Mod(r, p)), Pm));
racines(p) = vecsort(apply(t -> lift(t), polrootsmod(Phi, p)));
/* I = prod P(p_k, r_k) ; renvoie [I (HNF dans nfL), nu (générateur >> 0 de N(I) dans L+)] */
/* premier P de L donné comme [p, f, k] : k-ième premier de idealprimedec(nfL, p) (degré résiduel f, contrôlé) ;
   sa norme relative est le premier de L+ en dessous (P et Pbar distincts supposés : contrôlé) */
{
primeLgen(p, f, k) = my(D = idealprimedec(nfL, p), P = D[k], Dp = idealprimedec(nfp, p), q);
  if (P.f != f, error("degre residuel"));
  if (idealhnf(nfL, P) == idealhnf(nfL, nfgaloisapply(nfL, Mod('y^(m - 1), Phi), P)), error("P ambigu"));
  q = select(pp -> idealval(nfL, toL(nfbasistoalg(nfp, pp.gen[2])), P) > 0, Dp);
  if (#q != 1, error("premier de L+ sous P"));
  [idealhnf(nfL, P), idealhnf(nfp, q[1])];   /* P et Pbar distincts : N(P) = P Pbar inter L+ = q, de norme p^f */
}
{
ideal_et_nu(L) = my(I = idealhnf(nfL, 1), Np = idealhnf(nfp, 1), g);
  foreach(L, pr, if (#pr == 3, my(Q = primeLgen(pr[1], pr[2], pr[3])); I = idealmul(nfL, I, Q[1]); Np = idealmul(nfp, Np, Q[2]),
                  I = idealmul(nfL, I, primeL(pr[1], pr[2])); Np = idealmul(nfp, Np, primeLp(pr[1], pr[2]))));
  if (idealnorm(nfL, I) != idealnorm(nfp, Np), error("N(I) != norme de nu"));
  g = bnfisprincipal(bnfp, Np, 1);
  if (g[1] != 0 * g[1], error("N(I) non principal ?"));
  g = totpos(nfbasistoalg(nfp, g[2]));
  if (idealhnf(nfp, g) != Np, error("generateur"));
  [I, g];
}
pw(col) = Colrev(lift(nfbasistoalg(nfL, col)), n);
{
gramI(I, nu) =
  my(al = beta0 / nu, aL = toL(al), t = vector(m, k, trace(aL * z^(k - 1))), H, B, G);
  H = matrix(n, n, i, j, t[(i - j) % m + 1]);
  B = Mat(vector(n, j, pw(I[, j])));
  G = B~ * H * B;
  if (denominator(content(G)) != 1, error("Gram non entiere"));
  if (matdet(G) != 1, error(Str("det = ", matdet(G))));
  if (vecsum(vector(n, i, G[i, i] % 2)) != 0, error("Gram impaire"));
  [G, B];
}
/* rejet rapide : LLL + mélanges unimodulaires aléatoires ; renvoie [plus petite norme vue, vecteur, Gram LLL] */
{
cherche(G, essais, graine) =
  my(best = [10^9, 0], U, M, Gr, W);
  U = qflllgram(G); M = U; Gr = M~ * G * M;
  for (i = 1, n, if (Gr[i, i] < best[1], best = [Gr[i, i], M[, i]]));
  setrand(graine);
  for (k = 1, essais,
    if (best[1] <= 6, break);
    W = matid(n);
    for (rr = 1, 3 * n, my(i = random(n) + 1, j = random(n) + 1); if (i != j, W[, i] += (random(5) - 2) * W[, j]));
    U = qflllgram(W~ * Gr * W); M = M * W * U; Gr = M~ * G * M;
    for (i = 1, n, if (Gr[i, i] < best[1], best = [Gr[i, i], M[, i]])));
  [best[1], best[2], Gr, M];
}
