/* raccord_detecteur.gp -- raccord EXACT des entrees regenerees (I_data.gp de la chaine prep_java.gp) a la Gram du detecteur G6K
   du 19 oct. (23_DEPOT_PUBLIC_RANG88/detecteur_g6k_20261019/gram/<NOM>.gram et <NOM>.U.gp, copies controlees dans
   detecteur_copie/).  Claude, lot R88_TRANCHE1, 19 oct. 2026.  A lire apres avoir fixe NOM, FIDATA, FGRAM, FU, CODE, FCORPS.
   D1  reconstruit() de detecteur_copie/code/commun_rang88.gp (inchange) sur l'I_data.gp REGENERE : ses 8 controles
       (A1 type, A2 base C depuis (p, GEN), A3 BASE engendre I, B1 alpha nu = beta0, B2-B4 G = C~ H C entiere paire det 1
       definie positive, B5 GRAM = BASE~ H BASE) ;
   D2  U du detecteur : 88 x 88 entiere, |det U| = 1 ;
   D3  U~ G U = Gram du detecteur (fichier <NOM>.gram, 88 lignes de 88 entiers), a l'identique ;
   D4  W = BASE^-1 C U entiere, |det W| = 1, W~ GRAM W = Gram du detecteur : la Gram GRAM des entrees Java (celle que raccorde
       verifier_raccord_tranche1.py, G2-G6) et la Gram donnee a G6K sont celles du MEME reseau, dans deux bases liees par W.
   Verdict : "RACCORD_DETECTEUR_OK NOM" si et seulement si 13 controles sur 13 (8 + 5) ont imprime OK (GP poursuit apres une erreur). */
read(Str(CODE, "/commun_rang88.gp"));
reconstruit();
nd = 0; nokd = 0;
okd(nom, c) = nd++; if (c, nokd++); printf("%s %s\n", if (c, "OK   ", "ECHEC"), nom); c;
okd(Str(NOM, " D1 : les 8 controles de reconstruit() (commun_rang88.gp du detecteur, inchange) sont OK"), nb == 8 && nok == 8);
U = 0; read(FU); Ud = U;
okd(Str(NOM, " D2 : U du detecteur 88 x 88 entiere, |det U| = 1"), type(Ud) == "t_MAT" && matsize(Ud) == [n, n] && denominator(content(Ud)) == 1 && abs(matdet(Ud)) == 1);
LG = readstr(FGRAM);
okd(Str(NOM, " D3a : fichier Gram du detecteur de 88 lignes"), #LG == n);
Grd = matrix(n, n, i, j, eval(strsplit(LG[i], " ")[j]));
okd(Str(NOM, " D3 : U~ G U = Gram du detecteur (", FGRAM, ")"), Ud~ * G * Ud == Grd);
W = matsolve(BASE, C * Ud);
okd(Str(NOM, " D4 : W = BASE^-1 C U entiere, |det W| = 1, W~ GRAM W = Gram du detecteur"), denominator(content(W)) == 1 && abs(matdet(W)) == 1 && W~ * GRAM * W == Grd);
printf("%s : diagonale de la Gram du detecteur : min %d, max %d\n", NOM, vecmin(vector(n, i, Grd[i, i])), vecmax(vector(n, i, Grd[i, i])));
printf("%s : %d + %d controles, %d echecs\n", NOM, nb, nd, (nb - nok) + (nd - nokd));
if (nb == 8 && nok == 8 && nd == 5 && nokd == 5, printf("RACCORD_DETECTEUR_OK %s\n", NOM), printf("RACCORD_DETECTEUR_ECHEC %s\n", NOM));
quit(if (nb == 8 && nok == 8 && nd == 5 && nokd == 5, 0, 1))
