#!/bin/sh
# preparer.sh -- regenere les fichiers d'entree du programme certifiant pour P139 et P599 et les compare, octet pour
# octet, a ceux du depot (data/P139/entrees, data/P599/entrees).  A lancer depuis la racine du depot :
#     GP=gp sh code/preparation/preparer.sh            (environ 2 min ; PARI/GP 2.15.4 ; ecrit dans sortie_preparation/)
# bnfinit (sous GRH) ne sert qu'a trouver un generateur totalement positif nu de la norme de l'ideal ; chaque matrice
# produite est ensuite controlee exactement, ici par prep_java.gp et, independamment, par verifier_raccord.py.
set -eu
GP=${GP:-gp}
mkdir -p sortie_preparation/P139 sortie_preparation/P599
"$GP" -q -D parisize=800000000 code/preparation/preparer_bnf.gp < /dev/null > sortie_preparation/bnf.log 2>&1
cat sortie_preparation/bnf.log
for c in P139 P599; do
  "$GP" -q -D parisize=800000000 code/preparation/preparer_$c.gp < /dev/null > sortie_preparation/$c/prep.log 2>&1
  cat sortie_preparation/$c/prep.log
  for f in I_data.gp cote1_A.gram cote1_B.gram cote1_T.mat cote1_meta.txt cote1_bases.gp cote2_A.gram cote2_B.gram cote2_T.mat cote2_meta.txt cote2_bases.gp; do
    if cmp -s "sortie_preparation/$c/$f" "data/$c/entrees/$f"; then echo "IDENTIQUE  $c/$f"; else echo "DIFFERENT  $c/$f"; fi
  done
done
