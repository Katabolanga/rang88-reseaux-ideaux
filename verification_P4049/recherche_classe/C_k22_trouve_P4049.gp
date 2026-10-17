/* C_k22_trouve_P4049.gp -- RECHERCHE (non certifiante, bnfinit SOUS GRH) des pieces d'un certificat SANS GRH de
   « X_4049 n'est isometrique ni a X_139 ni a X_4969 », sur le modele de rang88_p139/B_k22_trouve.gp (11 octobre 2026) ; adapte de C_k22_trouve_P4969.gp.
   K22 = Fix<sigma_22> = Q(theta), theta = zeta + zeta^22 + zeta^24 + zeta^68 (degre 22).
   P4049 = (4049, zeta^2 + 105 zeta + 2084) : l'ideal des fichiers d'entree (verifier_raccord.py, G1).
   On ecrit dans C_k22_certificat_P4049.txt (une affectation par ligne, lisible par Python) :
     P22    : polynome minimal de theta (variable w) ;
     RACINE : r mod 4049, image de theta modulo P4049 (q = (4049, theta - r) = P4049 inter K22) ;
     GAMMA  : element de K22 avec (GAMMA) = q^331 (trouve par bnfisprincipal, bnfinit SOUS GRH).
   Rien de ceci n'est cru : le verificateur Python recontrole tout en arithmetique exacte, sans PARI.
   On imprime aussi, A TITRE INDICATIF (sous GRH), les classes de q4049 et des 22 conjugues de q139 dans Cl(K22).
   Lancer depuis verification_P4049/ : gp -q -D parisize=600000000 recherche_classe/C_k22_trouve_P4049.gp
   Claude, 16 octobre 2026. */
m = 115; Phi = polcyclo(m, 'y); z = Mod('y, Phi);
t0 = getabstime(); tm() = (getabstime() - t0) \ 1000;
th22 = z + z^22 + z^24 + z^68; P22 = minpoly(th22, 'w);
if (poldegree(P22) != 22, error("degre"));
b22 = bnfinit(P22, 1);
printf("K22 : Cl = %s (GRH) ; disc = %s  [%d s]\n", b22.cyc, factor(b22.disc), tm());
p = 4049; g = Mod(1, p) * ('y^2 + 105*'y + 2084);
{
  if (polisirreducible(g) == 0, error("g reductible mod 4049"));
  if (lift(Phi * Mod(1, p)) % g != 0, error("g ne divise pas Phi_115 mod 4049"));
}
rt = lift(lift(Mod(lift(th22) * Mod(1, p), g)));
if (poldegree(rt) > 0, error("theta mod P4049 hors de F_4049"));
r = polcoeff(rt, 0);
printf("RACINE : theta = %d mod P4049\n", r);
{
  if (subst(P22, 'w, Mod(r, p)) != 0, error("r n'est pas racine de P22 mod 4049"));
}
D = idealprimedec(b22, p);
qs = select(pp -> idealval(b22, Mod('w - r, P22), pp) > 0, D);
if (#qs != 1, error("premier sous P4049"));
q = qs[1]; if (q.f != 1, error("q de degre 1 attendu"));
cl = bnfisprincipal(b22, q, 0);
printf("classe de q4049 dans Cl(K22) (GRH) : %s\n", cl~);
/* indicatif : classes des conjugues de q139 = (139, theta - 0) */
q139s = select(pp -> idealval(b22, Mod('w, P22), pp) > 0, idealprimedec(b22, 139));
if (#q139s != 1, error("q139"));
q139 = q139s[1]; c139 = bnfisprincipal(b22, q139, 0);
G = nfgaloisconj(b22); if (#G != 22, error("Gal(K22/Q) attendu d'ordre 22"));
cls = vector(#G, k, bnfisprincipal(b22, nfgaloisapply(b22, G[k], q139), 0)[1]);
printf("classe de q139 (GRH) : %s ; classes de ses 22 conjugues (GRH) : %s\n", c139~, cls);
printf("INDICATIF (GRH) : classe de q4049 parmi celles des conjugues de q139 : %s\n", if (setsearch(Set(cls), cl[1]), "OUI", "NON"));
/* indicatif : classes des conjugues de q4969 = (4969, theta - 4770) (RACINE du certificat de P4969) */
q4969s = select(pp -> idealval(b22, Mod('w - 4770, P22), pp) > 0, idealprimedec(b22, 4969));
if (#q4969s != 1, error("q4969"));
cls4969 = vector(#G, k, bnfisprincipal(b22, nfgaloisapply(b22, G[k], q4969s[1]), 0)[1]);
printf("classes des 22 conjugues de q4969 (GRH) : %s\n", cls4969);
printf("INDICATIF (GRH) : classe de q4049 parmi celles des conjugues de q4969 : %s\n", if (setsearch(Set(cls4969), cl[1]), "OUI", "NON"));
res = bnfisprincipal(b22, idealpow(b22, q, 331), 1);
if (res[1] != 0 * res[1], error("q^331 non principal ?"));
gam = nfbasistoalg(b22, res[2]);
if (idealhnf(b22, gam) != idealpow(b22, q, 331), error("generateur"));
printf("generateur de q4049^331 trouve ; norme = 4049^%d  [%d s]\n", valuation(norm(gam), p), tm());
F = fileopen("recherche_classe/C_k22_certificat_P4049.txt", "w");
filewrite(F, Str("P22 = ", P22));
filewrite(F, Str("RACINE = ", r));
filewrite(F, Str("GAMMA = ", lift(gam)));
fileclose(F);
printf("ecrit recherche_classe/C_k22_certificat_P4049.txt  [%d s]\n", tm());
quit
