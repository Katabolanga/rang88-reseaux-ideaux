/* C4_compte_U_P139_qfminim.gp -- contre-audit, experience C4 (Claude, 16 octobre 2026).
   Recompte INDEPENDANT du code Java, par qfminim de PARI/GP (Fincke-Pohst de PARI ; non certifiant), des projections courtes
   du cote 1 de P139 : u dans Z^44, u~ A u <= B, A = cote1_A.gram (entiere, echelle DA = 139), energie = u~ A u / 139.
   Comptes attendus (histogramme imprime par Rang88CertZ, data/P139/premiere_execution/cote1.log, cumule ; au signe pres) :
     energie < 3.0 : 162 ; < 3.5 : 4878 ; < 4.0 : 92734 ; < 4.5 : 1260158 ; < 5.0 : 12651642 ; <= 1057/200 : 42957972.
   qfminim(A, B, 0)[1] compte les vecteurs v et -v (deux fois le nombre de paires) ; on divise par 2.
   Lancer depuis contre_audit_20261016/ : gp -q -D parisize=2000000000 C4_compte_U_P139_qfminim.gp */
f = "C:/Users/ivang/Desktop/DeBoreAh/PREMIERS/AnacondaSpyder/conversations636_02072026/Conversations705/16_CONVERSATIONS_PDF_ET_ANNEXES/_UNIFICATION_CLAUDE_20260925/23_DEPOT_PUBLIC_RANG88/github/rang88-reseaux-ideaux/data/P139/entrees/cote1_A.gram";
L = readstr(f); t = strsplit(L[1], " "); n = eval(t[1]);
A = matrix(n, n, i, j, eval(strsplit(L[i + 1], " ")[j]));
if (A != A~, error("A non symetrique"));
printf("A : %d x %d, entiere, symetrique ; det = %s\n", n, n, matdet(A));
DA = 139; t0 = getabstime();
att = [[3, 162], [7/2, 4878], [4, 92734], [9/2, 1260158], [5, 12651642]];
{for (i = 1, #att, my(e = att[i][1], B = ceil(DA * e) - 1, c = qfminim(A, B, 0)[1] / 2);
  printf("energie < %s : B = %d : compte PARI = %d ; attendu %d : %s  [%d s]\n", e, B, c, att[i][2], if (c == att[i][2], "IDENTIQUE", "DIFFERENT"), (getabstime() - t0) \ 1000));}
B = floor(DA * 1057 / 200); c = qfminim(A, B, 0)[1] / 2;
printf("energie <= 1057/200 : B = %d : compte PARI = %d ; attendu 42957972 : %s  [%d s]\n", B, c, if (c == 42957972, "IDENTIQUE", "DIFFERENT"), (getabstime() - t0) \ 1000);
quit
