#!/bin/bash
# M10 : controle final de la replication de X(P461 sigma_91) sur Bertha, A LANCER APRES le verdict du lanceur.
# Lecture seule des sorties ; ecrit seulement ~/m10/CONTROLE_FIN_P461s91.txt.
# Compare : (1) verdict et recu ; (2) empreintes canoniques Bertha contre Crapaud08 (20 oct.) ;
#           (3) recus Bertha contre recus Crapaud08, tache par tache, a l'octet (couvre les 670 recus herites jamais recoupes) ;
#           (4) controle_execution.py rejoue (E7 contre ref/) ; (5) SHA256SUMS_SORTIES.txt.
set -u
R=~/m10/R88_P461S91_CERT_V2_20261019; REF=/mnt/c/Users/Joueur/m10/ref_crapaud08; OUT=~/m10/CONTROLE_FIN_P461s91.txt
EC1=db04c32e641f75bcce3739f09921e3aab27917903b4b4e36aedafae518eaa1e4
EC2=652ef2f89497cb0784326c1ab280b86b99febb3206749f3ee4592c4f59936d13
CAT1=0189bac379e039fbc70a1747d76a3865a734065279ae7c90ab8538b0a132f5ef
CAT2=388a5734bb6ce7e5a700c8e08aaa54cae326bf787a451a1251639c5f834e0fd2
cd "$R" || exit 9
{
echo "CONTROLE_FIN_P461s91 (M10) $(date '+%F %T') ; hote $(hostname)"
ok=0; ko=0; t() { if eval "$1"; then ok=$((ok+1)); echo "OK    $2"; else ko=$((ko+1)); echo "ECHEC $2"; fi; }
t '[ -f sorties/VERDICT.txt ]' "verdict present"
echo "verdict : $(cat sorties/VERDICT.txt 2>/dev/null)"
t 'grep -q "^COMPLET_SANS_TOUCHE P461s91" sorties/VERDICT.txt' "verdict COMPLET_SANS_TOUCHE (code 0 du lanceur)"
(cd "$REF" && sha256sum -c --quiet SHA256SUMS_REF.txt); RS=$?; t "[ $RS = 0 ]" "empreintes des recus de reference Crapaud08"
for c in 1 2; do
  CK=sorties/run_P461s91_cote$c/cote$c.ckpt
  if [ $c = 1 ]; then EC=$EC1; CAT=$CAT1; TOT=73244; else EC=$EC2; CAT=$CAT2; TOT=73359; fi
  t "[ ! -e sorties/run_P461s91_cote$c/cote$c.ckpt.touches ]" "cote $c : aucun fichier de touche"
  t "grep -q '^FIN_COTE $c COMPLET ' sorties/RECU_P461s91.txt" "cote $c : FIN_COTE COMPLET (un seul lancement, controles 100 %)"
  E=$(python3 -I outils/empreinte_canonique.py "$CK" | grep -o 'empreinte canonique [0-9a-f]\{64\}' | cut -c21-)
  echo "cote $c : empreinte canonique Bertha $E"
  t "[ '$E' = '$EC' ]" "cote $c : empreinte canonique identique a Crapaud08 ($EC)"
  python3 -I outils/compare_recus.py "$CK" "$REF/crapaud08_cote$c.ckpt" > $HOME/m10/tmp_m10_cmp$c.txt 2>&1; CR=$?
  cat $HOME/m10/tmp_m10_cmp$c.txt | head -3
  t "[ $CR = 0 ]" "cote $c : $TOT recus Bertha identiques a l'octet aux recus Crapaud08"
  RA=$(ls ref/filtre_s91_20261017_cote$c.ckpt)
  python3 -I outils/controle_execution.py sorties/run_P461s91_cote$c $c $TOT $CAT $RA > $HOME/m10/tmp_m10_ce$c.txt 2>&1; CE=$?
  grep -a '^BILAN' $HOME/m10/tmp_m10_ce$c.txt
  t "[ $CE = 0 ]" "cote $c : controle_execution.py rejoue, code 0"
done
(cd sorties && sha256sum -c --quiet SHA256SUMS_SORTIES.txt); RS=$?; t "[ $RS = 0 ]" "SHA256SUMS_SORTIES.txt"
echo "BILAN controle_fin : $ok OK, $ko echecs"
} > "$OUT" 2>&1
cat "$OUT"
