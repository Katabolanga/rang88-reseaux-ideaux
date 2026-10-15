/* pilote : entrees du programme certifiant pour P139 = (139, g(zeta)), premier de degre 2 (PREM = [[139, 2, 1]] :
   premier ideal de idealprimedec(nfL, 139), convention de outils115.gp) ; ecrit sortie_preparation/P139/ */
default(breakloop, 0);
FBNFP = "sortie_preparation/bnf_k115.bin";
PREM = [[139, 2, 1]];
DIR = "sortie_preparation/P139";
read("code/preparation/prep_java.gp");
