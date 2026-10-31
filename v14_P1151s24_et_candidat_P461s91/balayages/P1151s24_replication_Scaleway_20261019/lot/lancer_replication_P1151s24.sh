#!/bin/bash
# lancer_replication_P1151s24.sh -- REPLICATION du balayage certifiant de X = (I, beta0/nu), I = P6 * sigma24(P6) = (1151, zeta-6)(1151, zeta-605)
# sur L = Q(zeta_115).  Memes classes publiees (Rang88CertZ, empreintes controlees), memes entrees, meme invocation que la premiere
# execution (SpiraleG, 17-19 oct. 2026, 14 fils, lanceur r88p/lancer_P1151s24.sh) :
#   java -Xmx3g -DstopTouche=1 -Dveille=600 -DDmax=16 -Dseuil=0.2 -Dckpt=... -Dcat=... -cp classes Rang88CertZ run java_P1151s24/coteN 1057 200 12 <FILS> 6
# Seules differences : le nombre de fils et la version de Java (sans effet sur les recus : 402 902 recus identiques sous Java 11, 17, 21
# pour X4969 et X4049).  Claude (SpiraleG), 19 oct. 2026.  Aucun reseau, aucun secret.
#
# Usage (Linux, depuis une copie de travail du lot ; rien n'est ecrit hors de sorties/) :
#   JAVA=/usr/lib/jvm/java-21-openjdk-amd64/bin/java PYTHON=python3 bash lancer_replication_P1151s24.sh [FILS=8] [MAXH=72]
#   reprise apres interruption (les recus deja ecrits sont gardes, les taches recues sont sautees) :
#   JAVA=... bash lancer_replication_P1151s24.sh --reprendre [FILS] [MAXH]
#   un seul cote sur cette machine (deux machines en parallele) : COTES=2 bash lancer_replication_P1151s24.sh 32 12
# Etapes : 0 empreintes du lot (SHA256SUMS.txt) ; 1 autotest (TestCertZ 910 controles ; validation P461 : 697 u, 2 touches,
#          couverture 3658/3658) ; 2 cote 1 puis cote 2 (arret a la premiere touche) ; 3 pour chaque cote : controle_execution.py
#          (E1-E6) et empreinte canonique comparee a ref/ATTENDU_PREMIERE_EXECUTION_SpiraleG.txt ; 4 recu et SHA-256 des sorties.
# Codes de sortie : 0 = cotes demandes complets, sans touche, empreintes canoniques IDENTIQUES a la premiere execution ;
#   2 = touche (vecteur de norme <= 6 : rendre sorties/run_*/cote*.ckpt.touches ; NE PAS lancer l'autre cote) ;
#   3 = cote incomplet (garde-fou, interruption) : relancer avec --reprendre ;
#   4 = complet sans touche mais empreinte canonique ou catalogue DIFFERENT (a signaler tel quel, sans correction) ;
#   5 = refus (verrou present, sortie existante sans --reprendre) ; 11-13 = echec des empreintes ou de l'autotest.
set -u
cd "$(dirname "$0")" || exit 9
REPRENDRE=0; if [ "${1:-}" = "--reprendre" ]; then REPRENDRE=1; shift; fi
FILS=${1:-8}; MAXH=${2:-72}; COTES=${COTES:-1 2}
J="${JAVA:-java}"; PY="${PYTHON:-python3}"
S=sorties; mkdir -p "$S"; REC="$S/RECU_REPLICATION_P1151s24.txt"
log() { echo "$(date '+%F %T')  $*" | tee -a "$REC"; }
if ! mkdir "$S/.verrou" 2>/dev/null; then
  if [ "$REPRENDRE" = 1 ]; then log "verrou present, repris (--reprendre)"; else echo "REFUS : verrou $S/.verrou present (calcul deja lance ? utiliser --reprendre)"; exit 5; fi
fi
log "DEBUT replication P1151s24 ; hote $(hostname) ; $(nproc) processeurs ; FILS=$FILS ; MAXH=$MAXH ; COTES=$COTES ; reprise=$REPRENDRE"
log "java : $("$J" -version 2>&1 | head -1) ; python : $("$PY" --version 2>&1)"
# ---- 0 empreintes du lot
if ! sha256sum --quiet -c SHA256SUMS.txt > "$S/verif_empreintes_lot.txt" 2>&1; then log "ECHEC 0 : empreintes du lot (voir $S/verif_empreintes_lot.txt)"; exit 11; fi
log "0 OK : empreintes du lot ($(grep -c . SHA256SUMS.txt) fichiers)"
# ---- 1 autotest (une seule fois)
if [ ! -f "$S/AUTOTEST_OK" ]; then
  A="$S/autotest"; mkdir -p "$A"
  "$J" -Xmx1g -Dverif=1 -cp classes TestCertZ 1 300 > "$A/testcertz.log" 2>&1; echo $? > "$A/testcertz.exit"
  if grep -q "^TEST_OK" "$A/testcertz.log" && grep -q "TOTAL : 910 controles, 0 echecs" "$A/testcertz.log"; then log "1a OK : TestCertZ, 910 controles, 0 echec"
  else log "ECHEC 1a : TestCertZ (voir $A/testcertz.log)"; exit 12; fi
  rm -f "$A/P461.ckpt" "$A/P461.taches" "$A/P461.ckpt.touches"
  "$J" -Xmx2g -Dckpt="$A/P461.ckpt" -Dcat="$A/P461.taches" -cp classes Rang88CertZ run java_P461/cote1 7 2 12 "$FILS" 6 > "$A/p461.log" 2>&1; echo $? > "$A/p461.exit"
  if grep -q "^COMPTE_U .*) 697 ;" "$A/p461.log" && grep -q "^TOTAL_TOUCHES 2$" "$A/p461.log" && grep -q "^COUVERTURE_COMPLETE 3658/3658" "$A/p461.log"; then
    log "1b OK : validation P461 (697 u, 2 touches attendues, couverture 3658/3658)"
  else log "ECHEC 1b : validation P461 (voir $A/p461.log)"; exit 13; fi
  date '+%F %T' > "$S/AUTOTEST_OK"
fi
# ---- 2 balayages
VERDICT=0
for c in $COTES; do
  if [ "$c" = 1 ]; then TOT=74027; CAT=287b1e724cb845e266356bbaed182a6c95d47f207dc7def9acf10c5d78711b8e; EMP=36c946d4551a6d403cfc8e8ecadabab8efa8b9090c8fe3898cdafcd04d2e32f7
  else TOT=101373; CAT=fe2b7eb6d4d0218117b840ca1d7dc5353bf1e5b6c276ed7bbaede563c25ae4b4; EMP=32818d454ff45e5a835e894cf1f0a1411a1aba516fb6eae14ba328f96d6065da; fi
  OUT="$S/run_P1151s24_cote$c"; mkdir -p "$OUT"
  if grep -q "^FIN_COTE $c IDENTIQUE" "$REC"; then log "cote $c deja complet et identique : saute"; continue; fi
  if [ -e "$OUT/cote$c.ckpt" ] && [ "$REPRENDRE" = 0 ]; then log "REFUS : $OUT/cote$c.ckpt existe ; utiliser --reprendre"; exit 5; fi
  for f in java_P1151s24/cote${c}_A.gram java_P1151s24/cote${c}_B.gram java_P1151s24/cote${c}_T.mat java_P1151s24/cote${c}_meta.txt classes/*.class; do echo "sha256 $(sha256sum "$f" | cut -c1-64)  $f" >> "$REC"; done
  H=$(date +%Y%m%d_%H%M%S)
  log "DEBUT cote $c ($TOT taches), $FILS fils, garde-fou $MAXH h ; journal $OUT/cote${c}_crapaud08_$H.stdout.log"
  nice -n 10 timeout "${MAXH}h" "$J" -Xmx3g -DstopTouche=1 -Dveille=600 -DDmax=16 -Dseuil=0.2 -Dckpt="$OUT/cote$c.ckpt" -Dcat="$OUT/cote$c.taches" \
    -cp classes Rang88CertZ run java_P1151s24/cote$c 1057 200 12 "$FILS" 6 > "$OUT/cote${c}_crapaud08_$H.stdout.log" 2> "$OUT/cote${c}_crapaud08_$H.stderr.log"
  CODE=$?; echo "$CODE" > "$OUT/cote${c}_crapaud08_$H.java.exit"
  L="$OUT/cote${c}_crapaud08_$H.stdout.log"
  NT=$(grep -a -c '^TOUCHE' "$L"); TF=0; ls "$OUT"/*.touches > /dev/null 2>&1 && TF=1
  log "FIN cote $c : code natif Java $CODE (124 = garde-fou) ; lignes TOUCHE $NT ; fichier de touche $TF ; stderr $(stat -c %s "$OUT/cote${c}_crapaud08_$H.stderr.log") octets"
  if [ "$NT" -gt 0 ] || [ "$TF" = 1 ]; then log "TOUCHE au cote $c : arret (vecteur de norme <= 6, a verifier exactement par SpiraleG)"; echo "TOUCHE cote $c" > "$S/VERDICT.txt"; VERDICT=2; break; fi
  if [ "$CODE" != 0 ] || ! grep -a -q "^COUVERTURE_COMPLETE $TOT/$TOT ; CATALOGUE" "$L" || ! grep -a -q "^TOTAL_TOUCHES 0$" "$L"; then
    log "INCOMPLET cote $c (code $CODE) : relancer avec --reprendre"; echo "INCOMPLET cote $c" > "$S/VERDICT.txt"; VERDICT=3; break; fi
  # ---- 3 controles du cote termine
  "$PY" -I outils/controle_execution.py "$OUT" "$c" "$TOT" "$CAT" > "$OUT/CONTROLE_EXECUTION_cote$c.txt" 2>&1; CE=$?
  E=$("$PY" -I outils/empreinte_canonique.py "$OUT/cote$c.ckpt" 2>&1 | tail -1 | grep -o 'empreinte canonique [0-9a-f]\{64\}' | cut -c21-)
  log "cote $c : controle_execution.py code $CE ($(tail -2 "$OUT/CONTROLE_EXECUTION_cote$c.txt" | head -1)) ; empreinte canonique $E (attendue $EMP)"
  if grep -a -q "^COUVERTURE_COMPLETE $TOT/$TOT ; CATALOGUE $CAT$" "$L" && [ "$E" = "$EMP" ]; then
    echo "FIN_COTE $c IDENTIQUE $(date '+%F %T') : $TOT/$TOT taches, 0 touche, catalogue $CAT, empreinte canonique $E" >> "$REC"
    [ "$CE" = 0 ] || log "NOTE cote $c : controle_execution.py a signale un ecart (une reprise fait echouer E1 « un seul lancement » : a declarer)"
  else
    log "DIFFERENCE cote $c : catalogue ou empreinte canonique differents de la premiere execution (rendre tout, ne rien corriger)"; VERDICT=4
  fi
done
# ---- 4 recu final
find "$S" -type f ! -name 'SHA256SUMS_SORTIES.txt' ! -path "$S/.verrou/*" -exec sha256sum {} + | sort -k2 > "$S/SHA256SUMS_SORTIES.txt"
case $VERDICT in
  0) log "VERDICT : REPLICATION_IDENTIQUE pour les cotes $COTES (aucune touche ; recus identiques a ceux de SpiraleG, par l'empreinte canonique)"; echo "REPLICATION_IDENTIQUE cotes $COTES" > "$S/VERDICT.txt";;
  4) log "VERDICT : DIFFERENCE_A_EXAMINER"; echo "DIFFERENCE_A_EXAMINER" > "$S/VERDICT.txt";;
esac
rmdir "$S/.verrou" 2>/dev/null
exit $VERDICT
