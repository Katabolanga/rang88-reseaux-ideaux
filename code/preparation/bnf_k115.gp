/* code/preparation/bnf_k115.gp — bnfinit de K115 = Q(zeta_115)^+ (degré 44, variable x, x = c = zeta + 1/zeta), sous GRH ;
   sauvegarde binaire dans FBNF (fichier de travail, non conserve dans le depot).  Sert seulement à trouver des générateurs totalement
   positifs de N(I) ; chaque Gram finale est contrôlée exactement (paire, déterminant 1), indépendamment de GRH.
   Ne pas lancer directement : utiliser code/preparation/preparer.sh (depuis la racine du depot), qui fixe FBNF. */
t0 = getabstime();
Phi = polcyclo(115, 'y);
Pm = minpoly(Mod('y, Phi) + Mod('y, Phi)^(-1), 'x);
D = read("data/corps/rang88_m115c0_data.txt");
if (D[1] != Pm, error("Pm different de celui de rang88_m115c0_data.txt"));
print("Pm identique a rang88_m115c0_data.txt ; beta0 relu.");
bnfp = bnfinit(Pm, 1);
printf("bnfinit(K115) : Cl = %s ; h = %d ; #fu = %d ; Cl+ = %s  [%d s]\n", bnfp.cyc, bnfp.no, #bnfp.fu, bnfnarrow(bnfp)[2], (getabstime() - t0) \ 1000);
writebin(FBNF, bnfp);
printf("sauvegarde %s  [%d s]\n", FBNF, (getabstime() - t0) \ 1000);
quit
