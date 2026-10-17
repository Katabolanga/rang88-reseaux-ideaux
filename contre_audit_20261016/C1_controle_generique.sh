#!/bin/bash
# controle_generique.sh -- contre-audit, experience C1 (groupe temoin), Claude, 16 octobre 2026.
# Pour des ideaux premiers de degre 1, P = (p, zeta - r), p = 1 mod 115 (classes generiques : l'heuristique prevoit ~4,4 % d'extremaux),
# prepare les entrees (prep_java.gp, memes parametres que P139/P599/P4969) puis passe Rang88CertZ cote 1 avec les parametres
# des executions publiees (1057/200, S = 12), ARRET A LA PREMIERE TOUCHE, au plus TMAX secondes, 8 fils.
# 691, 1151, 1381 : re-detection (un temoin de norme 6 a deja ete trouve par le filtre PARI, methode independante).
# Lancer depuis agents/ : bash rang88_ideaux/controle_generique_20261016/controle_generique.sh
cd "$(dirname "$0")/../.." || exit 9
R=rang88_ideaux/ctl1016   # chemin court : limite Windows de 260 caracteres (MAX_PATH)
CL=../../23_DEPOT_PUBLIC_RANG88/calcul_externe_P4969/classes
FBNFP="C:/Users/ivang/AppData/Local/Temp/claude/C--Users-ivang-Desktop-DeBoreAh-PREMIERS-AnacondaSpyder-conversations636-02072026-Conversations705-16-CONVERSATIONS-PDF-ET-ANNEXES/03becf37-77c0-4b55-bfdf-7947ae0aba44/scratchpad/bnf_k115.bin"
TMAX=${TMAX:-300}
RES=$R/RESULTATS.txt
echo "# p r | taches du cote 1 | touche ? | taches terminees avant arret | duree | statut   ($(date '+%F %T'), TMAX = $TMAX s)" >> $RES
for pr in "691 4" "1151 6" "1381 21" "2531 12" "3221 20" "3911 24" "4831 39" "5521 34" "5981 16" "6211 9" "7591 52" "8741 226" "8971 177" "9431 47" "9661 19" "11731 106"; do
  set -- $pr; p=$1; r=$2; D=$R/P$p; mkdir -p $D
  if [ ! -f $D/cote1_A.gram ]; then
    echo "FBNFP=\"$FBNFP\"; PREM=[[$p,$r]]; DIR=\"$D\"; read(\"rang88_ideaux/prep_java.gp\")" | timeout 900 gp -q -D parisize=800000000 > $D/prep.log 2>&1
  fi
  if [ ! -f $D/cote1_A.gram ]; then echo "$p $r | preparation ECHOUEE (voir $D/prep.log)" >> $RES; continue; fi
  t0=$(date +%s)
  timeout $TMAX java -Xmx2g -DstopTouche=1 -Dveille=30 -DDmax=16 -Dseuil=0.2 -Dckpt=$D/cote1.ckpt -Dcat=$D/cote1.taches -cp $CL Rang88CertZ run $D/cote1 1057 200 12 8 6 > $D/run_cote1.log 2>&1
  code=$?; t1=$(date +%s)
  tot=$(grep -a -m1 '^SELECTION' $D/run_cote1.log | sed -E 's/SELECTION ([0-9]+)\/.*/\1/')
  nt=$(grep -a -c '^TOUCHE' $D/run_cote1.log); faites=$(grep -a -c '^T|' $D/cote1.ckpt 2>/dev/null)
  if [ "$nt" -gt 0 ]; then st="REJETE (vecteur de norme <= 6 trouve)"; elif [ $code = 124 ]; then st="SURVIVANT PARTIEL (limite de temps)"; else st="FIN SANS TOUCHE (code $code) : A EXAMINER"; fi
  echo "$p $r | $tot | $nt | $faites | $((t1 - t0)) s | $st" >> $RES
done
echo "# fin $(date '+%F %T')" >> $RES
