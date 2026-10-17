/* C4b_compte_U_P139_complet_v2.gp -- contre-audit, experience C4, palier COMPLET, VERSION 2 (Claude, 16 octobre 2026, 15 h 15).
   Seule difference avec la v1 (C4b_compte_U_P139_complet.gp, SHA a4b11c25...) : le code de sortie.  La v1 imprimait DIFFERENT
   sans sortir en erreur (remarque d'Astra, 15 h) ; la v2 sort avec quit(1) si le compte differe de l'attendu, quit(0) sinon.
   La v2 n'a PAS ete relancee (3 h de calcul) : le resultat reste celui de la v1, journal C4b_compte_U_P139_complet.log
   (IDENTIQUE, 11 260 s) ; le code 0 de la v1 a ete capte par l'enveloppe shell (C4b_enveloppe_execution.txt).
   Recompte INDEPENDANT du code Java, par qfminim de PARI/GP 2.15.4 (Fincke-Pohst de PARI ; non certifiant, en flottants),
   du nombre |U| de projections courtes du cote 1 de P139 : u dans Z^44 non nul, u~ A u <= floor(139 * 1057/200) = 734,
   A = data/P139/entrees/cote1_A.gram du depot (entiere, echelle DA = 139), au signe pres.
   Attendu : COMPTE_U = 42 957 972 (journal de la premiere execution de P139, cote 1 ; idem replication).
   Lancer depuis contre_audit_20261016/ : gp -q -D parisize=200000000 C4b_compte_U_P139_complet_v2.gp < /dev/null ; echo $? */
f = "C:/Users/ivang/Desktop/DeBoreAh/PREMIERS/AnacondaSpyder/conversations636_02072026/Conversations705/16_CONVERSATIONS_PDF_ET_ANNEXES/_UNIFICATION_CLAUDE_20260925/23_DEPOT_PUBLIC_RANG88/github/rang88-reseaux-ideaux/data/P139/entrees/cote1_A.gram";
L = readstr(f); t = strsplit(L[1], " "); n = eval(t[1]);
A = matrix(n, n, i, j, eval(strsplit(L[i + 1], " ")[j]));
if (A != A~, error("A non symetrique"));
DA = 139; B = floor(DA * 1057 / 200); t0 = getabstime();
printf("A : %d x %d, entiere, symetrique ; B = floor(139 * 1057/200) = %d ; debut\n", n, n, B);
c = qfminim(A, B, 0)[1] / 2;
ok = (c == 42957972);
printf("energie <= 1057/200 : B = %d : compte PARI = %d ; attendu 42957972 : %s  [%d s]\n", B, c, if (ok, "IDENTIQUE", "DIFFERENT"), (getabstime() - t0) \ 1000);
print(if (ok, "FIN_C4B", "FIN_C4B_DIFFERENT"));
quit(if (ok, 0, 1))
