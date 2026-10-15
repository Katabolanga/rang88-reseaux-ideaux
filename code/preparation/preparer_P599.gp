/* pilote : entrees du programme certifiant pour P599 = (599, g(zeta)), premier de degre 2 (PREM = [[599, 2, 1]] :
   premier ideal de idealprimedec(nfL, 599), convention de outils115.gp) ; ecrit sortie_preparation/P599/ */
default(breakloop, 0);
FBNFP = "sortie_preparation/bnf_k115.bin";
PREM = [[599, 2, 1]];
DIR = "sortie_preparation/P599";
read("code/preparation/prep_java.gp");
