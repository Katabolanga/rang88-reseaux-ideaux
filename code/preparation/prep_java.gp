/* code/preparation/prep_java.gp — données EXACTES pour le programme certifiant Rang88CertZ (critère 6, recollement généralisé, seuil 1057/200).
   Pour I (liste de premiers, conventions de outils115.gp ; [] = O_L), écrit dans DIR/ :
     cote1 (a court, CVP en b) et cote2 (b court, CVP en a), chacun :
       <c>_A.gram  : Gram ENTIÈRE DA * (Ha~ QA Ha) de la projection courte, base LLL (u = coordonnées)
       <c>_B.gram  : Gram ENTIÈRE DB * (Hb~ QB Hb) de la fibre (2 nu O+), base LLL (y = coordonnées)
       <c>_T.mat   : Tn, entier, avec T = Tn / d = Hb^-1 * Hl : le relèvement de u a pour coordonnées de fibre s = T u
       <c>_meta.txt: "DA DB d" (entiers)
     Point de M : (court, fibre) = (Ha u, Hl u + Hb y) en coordonnées de O+ = Z[c] ; énergie courte = u~A u / DA ;
     énergie fibre = w~ B w / (DB d^2), w = d y + Tn u ; N(z) = (énergie courte + énergie fibre) / 2.
     Contrôles exacts : isométrie I -> M (AB~ diag(QB,QA) AB / 2 = Gram(I)), det des Gram, cohérence des relèvements.
   Écrit aussi DIR/I_data.gp (BASE, GRAM, AB, bases Ha, Hl, Hb des deux côtés) pour reconstruire x dans la base de I.
   Paramètres : FBNFP, PREM (liste), DIR.  Ne pas lancer directement : utiliser code/preparation/preparer.sh. */
read("code/preparation/outils115.gp");
t0 = getabstime(); tm() = (getabstime() - t0) \ 1000;
e = z - 1/z;
Mc = matrix(n, nh, r, i, polcoeff(lift((z + 1/z)^(i - 1)), r - 1, 'y));
toFpv(w) = my(v = matinverseimage(Mc, Colrev(lift(w), n))); if (#v == 0, error("hors de L+")); v;
cpow = vector(2 * nh, k, Mod('x, Pm)^(k - 1));
formeplus(gam) = my(t = vector(2 * nh - 1, k, trace(gam * cpow[k]))); matrix(nh, nh, i, j, t[i + j - 1]);
conj_(w) = Mod(subst(lift(w), 'y, 'y^(m - 1)), Phi);
coutfp(Gr, Bn) = my(Q = qfgaussred(Gr * 1.), qd = vector(nh, i, Q[i, i])); vecsum(vector(nh, k, (Pi * Bn)^(k / 2) / gamma(k / 2 + 1) / prod(i = nh - k + 1, nh, sqrt(qd[i]))));
BETA = if (type(BETA) == "t_INT", BETA, 20); read("code/preparation/bkz.gp");
{
ecrit(f, M) = my(F = fileopen(f, "w"), r = matsize(M)[1], c = matsize(M)[2]);
  filewrite(F, Str(r, " ", c));
  for (i = 1, r, filewrite(F, strjoin(apply(t -> Str(t), Vec(M[i, ])), " ")));
  fileclose(F);
}
In = ideal_et_nu(PREM); GBI = gramI(In[1], In[2]); G = GBI[1]; B = GBI[2]; al = beta0 / In[2]; q = idealnorm(nfL, In[1]);
QA = formeplus(al); QB = formeplus(al * (4 - Mod('x, Pm)^2));
/* lignes : (partie imaginaire b ; partie réelle a) */
AB = Mat(vector(n, j, my(w = Mod(Polrev(B[, j], 'y), Phi)); concat(toFpv((w - conj_(w)) / e), toFpv(w + conj_(w)))));
if (abs(matdet(AB)) != 2^nh * q, error("indice"));
if (AB~ * matconcat([QB, 0; 0, QA]) * AB / 2 != G, error("isometrie I -> M"));
printf("I : q = %d ; isometrie exacte verifiee ; Gram(I) paire de det %d  [%d s]\n", q, matdet(G), tm());
{
/* cote 1 : court = a (forme QA), fibre = b (forme QB) ; cote 2 : court = b, fibre = a */
for (cote = 1, 2,
  my(QC = if (cote == 1, QA, QB), QF = if (cote == 1, QB, QA), R, H, Hf, Hl, Hc, UC, UF, GC, GF, DA, DB, T, d, Tn, pre);
  /* HNF avec les lignes (fibre ; courte) : colonnes 1..44 = vecteurs à partie courte nulle */
  R = if (cote == 1, AB, matconcat([AB[nh + 1 .. n, ]; AB[1 .. nh, ]]));
  H = mathnf(R);
  Hf = H[1 .. nh, 1 .. nh]; Hl = H[1 .. nh, nh + 1 .. n]; Hc = H[nh + 1 .. n, nh + 1 .. n];
  /* réduction BKZ (bkz.gp, BETA, 30 tours au plus) des deux Gram, mises à l'échelle entière ; U unimodulaires contrôlées.
     Coûts de Fincke–Pohst estimés par les mineurs principaux (ordre de l'énumération Java) : court au seuil 1057/200,
     fibre à la borne 12 - 1057/200 (pire cas du CVP : la borne effective est 12 - Lam(court) >= 6,715). */
  GC = Hc~ * QC * Hc; my(DC = denominator(content(GC)), rb = bkz(DC * GC, BETA, 30)); UC = rb[1];
  Hc = Hc * UC; Hl = Hl * UC; GC = UC~ * GC * UC;
  GF = Hf~ * QF * Hf; my(DF = denominator(content(GF)), rf = bkz(DF * GF, BETA, 30)); UF = rf[1];
  Hf = Hf * UF; GF = UF~ * GF * UF;
  printf("cote %d : BKZ-%d : %d + %d insertions ; noeuds estimes : court (1057/200) %.3e (signe compris) ; CVP (borne 12 - 1057/200) %.3e par recherche  [%d s]\n",
         cote, BETA, rb[2], rf[2], coutq(GC, 1057/200), coutq(GF, 12 - 1057/200), tm());
  if (abs(matdet(UC)) != 1 || abs(matdet(UF)) != 1, error("LLL"));
  DA = denominator(content(GC)); DB = denominator(content(GF));
  T = matsolve(Hf, Hl); my(RT = round(T)); Hl = Hl - Hf * RT; T = T - RT;   /* relèvements réduits : coordonnées de fibre de T dans [-1/2, 1/2] */
  d = denominator(content(T)); Tn = d * T;
  /* contrôle : pour quelques u aléatoires, le point (Hc u, Hl u) est dans M modulo la fibre */
  for (k = 1, 5, my(u = vectorv(nh, i, random(7) - 3), pt = if (cote == 1, concat(Hl * u, Hc * u), concat(Hc * u, Hl * u)), x = matsolve(AB, pt));
    if (denominator(x) != 1, error("relevement")));
  pre = Str(DIR, "/cote", cote);
  ecrit(Str(pre, "_A.gram"), DA * GC); ecrit(Str(pre, "_B.gram"), DB * GF); ecrit(Str(pre, "_T.mat"), Tn);
  my(F = fileopen(Str(pre, "_meta.txt"), "w")); filewrite(F, Str(DA, " ", DB, " ", d)); fileclose(F);
  printf("cote %d : DA = %d, DB = %d, d = %d ; det(court) = %s ; det(fibre) = %s ; diag court %d..%d ; diag fibre %d..%d (echelle)  [%d s]\n",
         cote, DA, DB, d, matdet(GC), matdet(GF), vecmin(vector(nh, i, DA * GC[i, i])), vecmax(vector(nh, i, DA * GC[i, i])),
         vecmin(vector(nh, i, DB * GF[i, i])), vecmax(vector(nh, i, DB * GF[i, i])), tm());
  my(F = fileopen(Str(pre, "_bases.gp"), "w")); filewrite(F, Str("Hc = ", Hc, ";")); filewrite(F, Str("Hl = ", Hl, ";")); filewrite(F, Str("Hf = ", Hf, ";")); fileclose(F));
}
FF = fileopen(Str(DIR, "/I_data.gp"), "w");
filewrite(FF, Str("PREMIERS = ", PREM, ";")); filewrite(FF, Str("Q = ", q, ";")); filewrite(FF, Str("NU = ", lift(In[2]), ";"));
filewrite(FF, Str("ALPHA = ", lift(al), ";")); filewrite(FF, Str("BASE = ", B, ";")); filewrite(FF, Str("GRAM = ", G, ";")); filewrite(FF, Str("AB = ", AB, ";"));
fileclose(FF);
printf("ecrit %s  [%d s]\n", DIR, tm());
quit
