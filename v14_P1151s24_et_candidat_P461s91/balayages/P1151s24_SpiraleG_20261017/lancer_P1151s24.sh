#!/bin/bash
# lancer_P1151s24.sh -- balayage certifiant COMPLET de P1151s24 (I = P6 * P605 au-dessus de 1151) sur SpiraleG, cote 1 PUIS cote 2,
# 14 fils chacun, invocation des executions publiees : -DstopTouche=1 -Dveille=600 -DDmax=16 -Dseuil=0.2 ... Rang88CertZ run
# java_P1151s24/coteN 1057 200 12 14 6 (classes = calcul_externe_P4969/classes, empreintes controlees). Garde-fou 36 h par cote.
# Verrou mkdir (pas de doublon) ; refus si un dossier de sortie existe. Accord d'Ivan : 17 oct. 2026 vers 22 h 45. Claude.
set -u
cd "$(dirname "$0")" || exit 9
JAVA="/c/Program Files/Microsoft/jdk-11.0.16.101-hotspot/bin/java"
mkdir .verrou_P1151s24 2>/dev/null || { echo "REFUS : verrou .verrou_P1151s24 present (calcul deja lance ?)"; exit 6; }
[ -s DERNIER_AUTOTEST.txt ] && grep -q "TOTAL : 910 controles, 0 echecs" "$(cat DERNIER_AUTOTEST.txt)/testcertz.log" || { echo "REFUS : autotest absent"; exit 3; }
OUT=run_P1151s24; [ -e "$OUT" ] && { echo "REFUS : $OUT existe"; exit 4; }; mkdir "$OUT"
sha256sum classes/* java_P1151s24/* > "$OUT/empreintes_entrees.txt"
for c in 1 2; do
  if [ $c = 1 ]; then TOT=74027; else TOT=101373; fi
  echo "$(date '+%F %T')  DEBUT cote $c ($TOT taches), 14 fils, garde-fou 36 h" >> "$OUT/chaine.log"
  nice -n 10 timeout 36h "$JAVA" -Xmx3g -DstopTouche=1 -Dveille=600 -DDmax=16 -Dseuil=0.2 -Dckpt="$OUT/cote$c.ckpt" -Dcat="$OUT/cote$c.taches" \
    -cp classes Rang88CertZ run java_P1151s24/cote$c 1057 200 12 14 6 > "$OUT/cote$c.stdout.log" 2> "$OUT/cote$c.stderr.log"
  code=$?; echo "$code" > "$OUT/cote$c.java.exit"
  echo "$(date '+%F %T')  FIN cote $c, code java $code" >> "$OUT/chaine.log"
  nt=$(grep -a -c '^TOUCHE' "$OUT/cote$c.stdout.log")
  if [ "$nt" -gt 0 ]; then echo "$(date '+%F %T')  REJETE : $nt touche(s) au cote $c (vecteur de norme <= 6)" >> "$OUT/chaine.log"; echo "REJETE cote $c" > "$OUT/VERDICT.txt"; exit 2; fi
  if [ "$code" != 0 ]; then echo "INCONCLUSIF cote $c (code $code ; 124 = garde-fou ; reprise possible par le checkpoint)" > "$OUT/VERDICT.txt"; exit 3; fi
  grep -a -q "^COUVERTURE_COMPLETE $TOT/$TOT ; CATALOGUE" "$OUT/cote$c.stdout.log" && grep -a -q "^TOTAL_TOUCHES 0$" "$OUT/cote$c.stdout.log" || { echo "INCONCLUSIF cote $c : marqueurs terminaux absents" > "$OUT/VERDICT.txt"; exit 3; }
  echo "$(date '+%F %T')  cote $c : COUVERTURE_COMPLETE $TOT/$TOT, TOTAL_TOUCHES 0" >> "$OUT/chaine.log"
done
echo "DEUX_COTES_COMPLETS_SANS_TOUCHE (a confirmer par raccord et contre-audit)" > "$OUT/VERDICT.txt"
exit 0
