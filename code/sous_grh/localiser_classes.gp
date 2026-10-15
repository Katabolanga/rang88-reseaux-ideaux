/* localiser_classes.gp -- pilote de classes_sous_corps.gp pour les idéaux de la note : les huit rejets (tableau 2), les deux
   candidats et les quatre survivants partiels (tableau 3).  Degré 1 : P = (p, y - r), r = plus petite racine de Phi_115
   modulo p ; degré 2 : [p, 2, 1] = premier idéal de idealprimedec(nfL, p).  Les composantes 331 et 45013 sont SOUS GRH
   (bnfinit en degrés 22 et 44) ; la composante 3 est lue dans Cl(Q(sqrt(-23))), certifié (bnfcertify).
   Usage (depuis la racine du dépôt) : gp -q -D parisize=800000000 code/sous_grh/localiser_classes.gp < /dev/null   (environ 1 min) */
default(breakloop, 0);
rr(p, k) = vecsort(apply(t -> lift(t), polrootsmod(polcyclo(115, 'y), p)))[k];
LISTE = concat([[461, rr(461, 1)], [691, rr(691, 1)], [1151, rr(1151, 1)], [1381, rr(1381, 1)], [1471, 2, 1]], apply(p -> [p, 2, 1], select(p -> isprime(p), vector(52, k, 24 + 115 * k))));
print("LISTE = ", LISTE);
read("code/sous_grh/classes_sous_corps.gp");
