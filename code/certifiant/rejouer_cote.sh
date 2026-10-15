#!/bin/sh
# rejouer_cote.sh -- relance UN cote du balayage certifiant Rang88CertZ, avec les classes compilees du depot, dans un
# repertoire de sortie NEUF, en reproduisant l'invocation des executions publiees.  A lancer depuis la racine du depot :
#     sh code/certifiant/rejouer_cote.sh P139 1 /chemin/vers/un/repertoire/neuf [fils]
# Duree : plusieurs heures par cote (voir REPRODUIRE.md).  Memoire : -Xmx2g.  Le nombre de fils ne change pas les recus.
# Le script n'efface rien ; il refuse un repertoire de sortie qui contient deja un fichier de recus (une reprise ne
# rejouerait pas les taches deja recues).  Variables facultatives : JAVA (defaut java), BA_NUM et BA_DEN (defaut 1057 et
# 200 : seuil de la note ; une autre valeur ne sert qu'aux essais, par exemple data/validation/P461 avec 7 et 2).
set -eu
if [ $# -lt 3 ]; then echo "usage : sh code/certifiant/rejouer_cote.sh <P139|P599|validation/L0|validation/P461> <1|2> <repertoire_neuf> [fils]"; exit 3; fi
C=$1; COTE=$2; OUT=$3; FILS=${4:-6}
JAVA=${JAVA:-java}; BA_NUM=${BA_NUM:-1057}; BA_DEN=${BA_DEN:-200}
RAC=$(pwd)
case "$C" in
  P139|P599) SRC="$RAC/data/$C/entrees"; NOM="java_$C" ;;
  validation/L0|validation/P461) SRC="$RAC/data/$C"; NOM="java_${C#validation/}" ;;
  *) echo "candidat inconnu : $C"; exit 3 ;;
esac
case "$COTE" in 1|2) ;; *) echo "cote : 1 ou 2"; exit 3 ;; esac
[ -f "$RAC/code/certifiant/classes/Rang88CertZ.class" ] || { echo "lancer depuis la racine du depot"; exit 3; }
mkdir -p "$OUT"
if [ -e "$OUT/cote$COTE.ckpt" ]; then echo "REFUS : $OUT/cote$COTE.ckpt existe deja ; il faut un fichier de recus neuf"; exit 4; fi
mkdir -p "$OUT/$NOM"
for s in A.gram B.gram T.mat meta.txt; do cp "$SRC/cote${COTE}_$s" "$OUT/$NOM/"; done
cd "$OUT"
"$JAVA" -Xmx2g -DstopTouche=1 -Dveille=600 -DDmax=16 -Dseuil=0.2 -Dckpt="cote$COTE.ckpt" -Dcat="cote$COTE.taches" \
  -cp "$RAC/code/certifiant/classes" Rang88CertZ run "$NOM/cote$COTE" "$BA_NUM" "$BA_DEN" 12 "$FILS" 6 \
  > "cote$COTE.stdout.log" 2> "cote$COTE.stderr.log" && code=0 || code=$?
echo "$code" > "cote$COTE.java.exit"
echo "code de sortie Java : $code"
grep -E '^(SELECTION|EXECUTEES_CE_LANCEMENT|TOTAL_TOUCHES|COUVERTURE_|CATALOGUE_SHA256|CHECKPOINT_SHA256|FIN)' "cote$COTE.stdout.log" || true
echo "contenu du repertoire de sortie :"; ls -1 "$OUT"
