/* code/preparation/bkz.gp — BKZ simple pour Gram ENTIÈRE définie positive (exact), et coût de Fincke–Pohst exact par
   les mineurs principaux (même ordre que l'énumération Java : dernière coordonnée en premier).
   bkz(G, beta, tours) renvoie U unimodulaire (contrôlé) avec U~ G U « BKZ-réduite » :
     pour chaque bloc [k, k + beta - 1], Gram projetée exacte (complément de Schur), vecteur minimal par qfminim exact
     sur la Gram projetée mise à l'échelle entière ; insertion si strictement plus court, puis LLL exact du système
     générateur (qflllgram(., 4) : noyau entier éliminé).
   */
{
gsoq(G) = my(n = #G, m = vector(n + 1, i, if (i == 1, 1, matdet(G[1 .. i - 1, 1 .. i - 1])))); vector(n, i, m[i + 1] / m[i]);
}
{
coutq(G, Bn) = my(n = #G, qd = gsoq(G) * 1.); vecsum(vector(n, k, (Pi * Bn)^(k / 2) / gamma(k / 2 + 1) / prod(i = n - k + 1, n, sqrt(qd[i]))));
}
{
bkz(G0, beta, tours) =
  my(n = #G0, U = qflllgram(G0), G = U~ * G0 * U, change, k2, pre, blk, Gk, D, R, v, W, T, Gw, nb = 0);
  for (t = 1, tours,
    change = 0;
    for (k = 1, n - 1,
      k2 = min(k + beta - 1, n);
      if (k == 1, Gk = G[k .. k2, k .. k2],
        Gk = G[k .. k2, k .. k2] - G[k .. k2, 1 .. k - 1] * matsolve(G[1 .. k - 1, 1 .. k - 1], G[1 .. k - 1, k .. k2]));
      /* recherche flottante d'un vecteur plus court que b_k* (borne < Gk[1,1]) ; contrôle exact ensuite */
      R = qfminim(Gk * 1., Gk[1, 1] * (1 - 1e-9), 5000, 2);
      if (#R[3] == 0, next);
      if (qfeval(Gk, R[3][, 1]) >= Gk[1, 1], next);
      v = R[3][, 1]; my(bv = qfeval(Gk, v)); for (j = 2, #R[3], my(w = R[3][, j], bw = qfeval(Gk, w)); if (bw < bv, bv = bw; v = w));   /* le plus court trouvé */
      /* système générateur : b_1..b_{k-1}, w = sum v_i b_{k+i-1}, b_k..b_n */
      W = matrix(n, n + 1, i, j, if (j < k, i == j, if (j == k, if (i >= k && i <= k2, v[i - k + 1], 0), i == j - 1)));
      Gw = W~ * G * W;
      T = qflllgram(Gw, 4)[2];
      if (matsize(T)[2] != n, error("bkz : rang"));
      W = W * T;
      if (abs(matdet(W)) != 1, error("bkz : non unimodulaire"));
      U = U * W; G = W~ * G * W; change = 1; nb++);
    if (!change, break));
  if (abs(matdet(U)) != 1 || U~ * G0 * U != G, error("bkz : controle final"));
  [U, nb];
}
