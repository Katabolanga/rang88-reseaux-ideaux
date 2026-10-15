/* code/sous_grh/classes_sous_corps.gp — (note, par. 6.4, « Localisation sous GRH » ; colonnes « orbite » des tableaux 2 et 3) localisation de la classe [P] d'un idéal premier P de L = Q(zeta_115) dans
   Cl(L) = Cl_3 x Cl_331 x Cl_45013, lue dans les sous-corps où se factorisent les caractères :
     Cl_3     ~ Cl(F)_3,        F = Q(sqrt(-23))                          (bnfcertify : SANS GRH)
     Cl_331   ~ Cl(K22)_331,    K22 = Fix<sigma_22>, theta22 = zeta + zeta^22 + zeta^24 + zeta^68   (bnfinit : GRH)
     Cl_45013 ~ Cl(K44)_45013,  K44 = Fix<sigma_91>, theta44 = zeta + zeta^91                        (bnfinit : GRH)
   Pour K où se factorise chi (p ne divisant pas [L:K]), N_{L/K} : Cl(L)_chi -> Cl(K)_chi est un isomorphisme
   (N o j = [L:K] inversible mod p, j o N = somme sur Gal(L/K) = [L:K] sur A_chi).  N_{L/K}(P) = q^f(P/q), q = P inter K.
   On imprime la classe de N_{L/K}(P) dans Cl(K) (coordonnées sur bnf.gen) ; la composante utile est sa partie p.
   Entrées : LISTE de [p, r] (P = (p, y - r), degré 1) ou [p, f, k] (k-ième premier de idealprimedec(nfL, p)).
   Ne pas lancer directement : utiliser code/sous_grh/localiser_classes.gp, depuis la racine du dépôt.
   */
m = 115; Phi = polcyclo(m, 'y); z = Mod('y, Phi);
t0 = getabstime(); tm() = (getabstime() - t0) \ 1000;
nfL = nfinit([Phi, [5, 23]]);
gs = sum(a = 1, 22, kronecker(a, 23) * z^(5 * a));            /* sqrt(-23) dans L */
if (gs^2 != -23, error("somme de Gauss"));
th22 = z + z^22 + z^24 + z^68; th44 = z + z^91;
P2 = 'w^2 + 23; P22 = minpoly(th22, 'w); P44 = minpoly(th44, 'w);
printf("degres des sous-corps : 2, %d, %d  [%d s]\n", poldegree(P22), poldegree(P44), tm());
bF = bnfinit(P2, 1); printf("F = Q(sqrt(-23)) : Cl = %s ; bnfcertify = %d\n", bF.cyc, bnfcertify(bF));
b22 = bnfinit(P22, 1); printf("K22 : Cl = %s (GRH)  [%d s]\n", b22.cyc, tm());
b44 = bnfinit(P44, 1); printf("K44 : Cl = %s (GRH)  [%d s]\n", b44.cyc, tm());
plonge(el, th) = Mod(subst(lift(el), 'w, lift(th)), Phi);   /* élément de K (polynôme en w) -> L */
{
sous(bK, th, P) = my(D = idealprimedec(bK, P.p), q);
  q = select(pp -> idealval(nfL, plonge(nfbasistoalg(bK, pp.gen[2]), th), P) > 0, D);
  if (#q != 1, error("premier sous P"));
  q = q[1];
  bnfisprincipal(bK, idealpow(bK, q, P.f / q.f), 0);
}
{
premier(pr) = if (#pr == 3, idealprimedec(nfL, pr[1])[pr[3]],
  my(D = idealprimedec(nfL, pr[1]), Q = select(P -> idealval(nfL, Mod('y - pr[2], Phi), P) > 0, D)); if (#Q != 1, error("P")); Q[1]);
}
{
foreach(LISTE, pr, my(P = premier(pr), c3, c22, c44);
  c3 = sous(bF, gs, P); c22 = sous(b22, th22, P); c44 = sous(b44, th44, P);
  printf("P = %s (f = %d) : [N P] dans Cl(Q(sqrt-23)) = %s ; dans Cl(K22) = %s (cyc %s) ; dans Cl(K44) = %s (cyc %s)  [%d s]\n",
         pr, P.f, c3~, c22~, b22.cyc, c44~, b44.cyc, tm()));
}
quit
