#!/bin/sh
# tout_verifier.sh -- rejoue toutes les verifications rapides du depot (environ 4 min au total), dans l'ordre de la note.
# A lancer depuis la racine du depot :
#     PY=python3 GP=gp sh code/verification/tout_verifier.sh
# Python 3.9 ou plus (bibliotheque standard seulement), PARI/GP 2.15 (uniquement pour les trois scripts .gp).
# Les deux verifications qui lisent le fichier de R. Sakamoto sont sautees si externe/integer_input.txt est absent.
# Aucun calcul Java n'est lance ici ; aucun fichier n'est ecrit hors de la sortie standard.
set -u
PY=${PY:-python3}; GP=${GP:-gp}
echec=0
lance() { echo; echo "==== $*"; "$@" < /dev/null; rc=$?; echo "==== code de sortie $rc"; [ $rc -eq 0 ] || echec=1; }
lance "$PY" -I -B code/verification/verifier_sha256.py
lance "$PY" -I -B code/verification/verifier_corps.py
lance "$GP" -q -D parisize=400000000 code/verification/hmoins115.gp
lance "$GP" -q -D parisize=400000000 code/verification/caracteres115.gp
lance "$PY" -I -B code/verification/verifier_hmoins_caracteres.py
if [ -f externe/integer_input.txt ]; then
  lance "$PY" -I -B code/verification/verifier_H_L0.py
  lance "$PY" -I -B code/verification/verifier_conformite_article.py
else
  echo; echo "==== externe/integer_input.txt absent : verifier_H_L0.py et verifier_conformite_article.py sautes (voir externe/LISEZMOI.md)"
fi
lance "$GP" -q -D parisize=400000000 code/verification/verifier_temoins.gp
lance "$PY" -I -B code/verification/verifier_temoins.py
for cand in P139 P599; do
  lance "$PY" -I -B code/verification/verifier_raccord.py $cand
  lance "$PY" -I -B code/verification/verifier_recus.py $cand
  lance "$PY" -I -B code/verification/verifier_classe_$cand.py
done
echo
if [ $echec -eq 0 ]; then echo "TOUTES LES VERIFICATIONS : code 0"; else echo "AU MOINS UNE VERIFICATION A ECHOUE"; fi
exit $echec
