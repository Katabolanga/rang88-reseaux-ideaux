#!/bin/bash
# lancer_cert_P461s91.sh -- BALAYAGE CERTIFIANT COMPLET (premiere execution) des deux cotes de X = (I, beta0/nu), rang 88,
# L = Q(zeta_115), I = P_5 sigma_91(P_5) = (461, zeta - 5)(461, zeta - 115), 115 = 5^91 mod 461 (anneau sigma_91, heure 885 sous GRH ; jumeau de recollement de P461 sigma_24(P461), orbite de X139).
# Lot R88_P461S91_CERT_V2_20261019 : tranche 1 de la campagne des survivants (autorisation d'Ivan, 19 oct. 2026 vers 16 h 55).  Claude (SpiraleG),
# 19 oct. 2026.  Aucun reseau, aucun secret.  Gabarit : lancer_replication_P1151s24.sh (lot R88_P1151S24_REPLIC_20261019), avec
# deux corrections : (a) SHA256SUMS_SORTIES.txt est calcule EN DERNIER, apres l'ecriture du verdict dans le recu et dans
# VERDICT.txt ; (b) tout code natif non nul (TestCertZ, validation P461, Java, controle_execution.py) est refuse, meme si un
# marqueur de succes est present.
# Invocation (identique aux executions publiees et a P1151s24 ; seul le nombre de fils change) :
#   java -Xmx1g -DstopTouche=1 -Dveille=600 -DDmax=16 -Dseuil=0.2 -Dckpt=... -Dcat=... -cp classes Rang88CertZ run java_P461s91/coteN 1057 200 12 <FILS> 6
#
# Usage (Linux, depuis une copie de travail du lot ; rien n'est ecrit hors de sorties/) :
#   JAVA=/usr/lib/jvm/java-21-openjdk-amd64/bin/java PYTHON=python3 bash lancer_cert_P461s91.sh [FILS=8] [MAXH=24]
#   reprise apres interruption ou preemption (les recus deja ecrits sont gardes, les taches recues sont sautees) :
#   JAVA=... PYTHON=python3 bash lancer_cert_P461s91.sh --reprendre [FILS] [MAXH]
#   ESSAI_TACHES=n (reserve a l'essai court sur SpiraleG ; NE PAS DEFINIR sur Crapaud08) : taches 0..n-1 de chaque cote seulement,
#   sorties dans sorties_essai/, comparaison a l'octet aux recus de reference ; verdict ESSAI_OK (9) ou ESSAI_ECHEC (8), jamais 0.
# Etapes : 0 empreintes du lot ; 1 autotest (TestCertZ 910 controles ; validation P461 : 697 u, 2 touches attendues, 3658/3658),
#   codes natifs exiges nuls ; 2 cote 1 puis cote 2, arret a la premiere touche (l'autre cote n'est alors pas lance) ;
#   3 pour chaque cote termine : controle_execution.py (E1-E6, et E7 contre les recus de reference de ref/), empreinte canonique
#   et predictions exactes du jumeau P461 sigma_24 (COMPTE_U et NOEUDS court identiques, meme cote court) ; 4 verdict, puis SHA256SUMS_SORTIES.txt en dernier.
# Codes de sortie :
#   0  COMPLET_SANS_TOUCHE : deux cotes complets, un seul lancement chacun, 0 touche, controles 100 %, E7 identique ;
#   2  TOUCHE : vecteur de norme <= 6 signale (rendre sorties/run_*/cote*.ckpt.touches ; verification exacte sur SpiraleG) ;
#   3  INCOMPLET (garde-fou de MAXH h, signal, preemption) : relancer avec --reprendre ;
#   4  A_EXAMINER : complet sans touche, mais un controle differe (rendre tel quel, ne rien corriger) ;
#   5  REFUS (verrou tenu par un processus actif, sortie existante sans --reprendre, verdict final deja rendu) ;
#   6  COMPLET_SANS_TOUCHE_REPRISE_DECLAREE : complet sans touche apres reprise(s) ; seuls les controles E1 lies a la reprise
#      echouent (attendu) ; a confirmer sur SpiraleG ;
#   7  ERREUR_JAVA : code natif Java non nul autre que 124/137/143 (exception...) : rendre tel quel, ne pas reprendre sans examen ;
#   8/9 ESSAI_ECHEC / ESSAI_OK (mode ESSAI_TACHES seulement) ;
#   11 empreintes du lot ; 12 TestCertZ ; 13 validation P461 : rien n'est lance.
set -u
cd "$(dirname "$0")" || exit 9
REPRENDRE=0; if [ "${1:-}" = "--reprendre" ]; then REPRENDRE=1; shift; fi
FILS=${1:-8}; MAXH=${2:-24}; ESSAI=${ESSAI_TACHES:-0}
case "$FILS/$MAXH/$ESSAI" in *[!0-9/]*) echo "REFUS : FILS, MAXH et ESSAI_TACHES doivent etre des entiers"; exit 5;; esac
J="${JAVA:-java}"; PY="${PYTHON:-python3}"
NOM=P461s91; DJ=java_P461s91
if [ "$ESSAI" -gt 0 ]; then S=sorties_essai; else S=sorties; fi
mkdir -p "$S"; REC="$S/RECU_$NOM.txt"
log() { echo "$(date '+%F %T')  $*" | tee -a "$REC"; }
liberer() { rm -f "$S/.verrou/pid"; rmdir "$S/.verrou" 2>/dev/null; }
refus() { echo "$(date '+%F %T')  REFUS : $* (le recu n'est pas modifie)"; liberer; exit 5; }
terminer() {   # $1 code, $2 verdict : VERDICT.txt, ligne VERDICT du recu, verrou libere, puis SHA256SUMS_SORTIES.txt EN DERNIER (correction a)
  echo "$2" > "$S/VERDICT.txt"
  log "VERDICT : $2 (code de sortie $1)"
  liberer
  ( cd "$S" && find . -type f ! -name SHA256SUMS_SORTIES.txt -exec sha256sum {} + | LC_ALL=C sort -k2 > SHA256SUMS_SORTIES.txt )
  echo "$(date '+%F %T')  SHA256SUMS_SORTIES.txt ecrit en dernier ($(grep -c . "$S/SHA256SUMS_SORTIES.txt") fichiers) ; fin, code $1"
  exit "$1"
}
# ---- verrou (avec PID : un verrou tenu par un processus vivant n'est jamais repris) ; un refus ne modifie jamais le recu
ORPH=""
if mkdir "$S/.verrou" 2>/dev/null; then echo $$ > "$S/.verrou/pid"
else
  P0=$(cat "$S/.verrou/pid" 2>/dev/null)
  if [ -n "$P0" ] && kill -0 "$P0" 2>/dev/null; then echo "REFUS : verrou $S/.verrou tenu par le processus actif $P0"; exit 5; fi
  if [ "$REPRENDRE" = 1 ]; then echo $$ > "$S/.verrou/pid"; ORPH="${P0:-?}"
  else echo "REFUS : verrou $S/.verrou present (calcul interrompu ? utiliser --reprendre)"; exit 5; fi
fi
if [ -f "$S/VERDICT.txt" ] && grep -q -E "^(COMPLET|TOUCHE|A_EXAMINER|ERREUR|ESSAI)" "$S/VERDICT.txt"; then refus "verdict final deja rendu ($(head -1 "$S/VERDICT.txt")) : rien a reprendre"; fi
if [ "$REPRENDRE" = 0 ] && ls "$S"/run_"$NOM"_cote*/cote*.ckpt > /dev/null 2>&1; then refus "des recus existent deja dans $S (calcul interrompu ?) : utiliser --reprendre"; fi
[ -n "$ORPH" ] && log "verrou orphelin (processus $ORPH absent) : repris (--reprendre)"
INTERRUPTION=0; JPID=""
trap 'INTERRUPTION=1; [ -n "$JPID" ] && kill -TERM "$JPID" 2>/dev/null' TERM INT HUP
log "DEBUT $NOM ; lot R88_P461S91_CERT_V2_20261019 ; hote $(hostname) ; $(nproc) processeurs ; FILS=$FILS ; MAXH=$MAXH ; reprise=$REPRENDRE ; ESSAI_TACHES=$ESSAI"
log "java : $("$J" -version 2>&1 | head -1) ; python : $("$PY" --version 2>&1)"
# ---- 0 empreintes du lot
if ! sha256sum --quiet -c SHA256SUMS.txt > "$S/verif_empreintes_lot.txt" 2>&1; then terminer 11 "ECHEC_EMPREINTES_LOT (voir $S/verif_empreintes_lot.txt)"; fi
log "0 OK : empreintes du lot ($(grep -c . SHA256SUMS.txt) fichiers)"
# ---- 1 autotest (une fois par dossier de sortie) : marqueurs ET codes natifs nuls (correction b)
if [ ! -f "$S/AUTOTEST_OK" ]; then
  A="$S/autotest"; mkdir -p "$A"
  nice -n 10 timeout 3600 "$J" -Xmx1g -Dverif=1 -cp classes TestCertZ 1 300 > "$A/testcertz.log" 2>&1; CT=$?; echo "$CT" > "$A/testcertz.exit"
  if [ "$CT" = 0 ] && grep -q "^TEST_OK" "$A/testcertz.log" && grep -q "TOTAL : 910 controles, 0 echecs" "$A/testcertz.log"; then log "1a OK : TestCertZ, 910 controles, 0 echec, code natif 0"
  else terminer 12 "ECHEC_AUTOTEST_TESTCERTZ (code natif $CT ; voir $A/testcertz.log)"; fi
  rm -f "$A/P461.ckpt" "$A/P461.taches" "$A/P461.ckpt.touches"
  nice -n 10 timeout 3600 "$J" -Xmx1g -Dckpt="$A/P461.ckpt" -Dcat="$A/P461.taches" -cp classes Rang88CertZ run java_P461/cote1 7 2 12 "$FILS" 6 > "$A/p461.log" 2>&1; CP=$?; echo "$CP" > "$A/p461.exit"
  if [ "$CP" = 0 ] && grep -q "^COMPTE_U .*) 697 ;" "$A/p461.log" && grep -q "^TOTAL_TOUCHES 2$" "$A/p461.log" && grep -q "^COUVERTURE_COMPLETE 3658/3658" "$A/p461.log"; then
    log "1b OK : validation P461 (697 u, 2 touches attendues, couverture 3658/3658), code natif 0"
  else terminer 13 "ECHEC_AUTOTEST_P461 (code natif $CP ; voir $A/p461.log)"; fi
  date '+%F %T' > "$S/AUTOTEST_OK"
fi
# ---- 2 balayages
VERDICT=0; ESSAI_KO=0
for c in 1 2; do
  if [ "$c" = 1 ]; then TOT=73244; CAT=0189bac379e039fbc70a1747d76a3865a734065279ae7c90ab8538b0a132f5ef; REFS="filtre_s91_20261017_cote1.ckpt"; PRIM=filtre_s91_20261017_cote1.ckpt; UATT=143529602; NCATT=217258581578
  else TOT=73359; CAT=388a5734bb6ce7e5a700c8e08aaa54cae326bf787a451a1251639c5f834e0fd2; REFS="filtre_s91_20261017_cote2.ckpt"; PRIM=filtre_s91_20261017_cote2.ckpt; UATT=143529602; NCATT=179810114087; fi
  OUT="$S/run_${NOM}_cote$c"; mkdir -p "$OUT"
  if grep -q "^FIN_COTE $c " "$REC"; then log "cote $c deja termine ($(grep "^FIN_COTE $c " "$REC" | tail -1 | cut -d' ' -f3)) : saute"; continue; fi
  if [ -e "$OUT/cote$c.ckpt" ] && [ "$REPRENDRE" = 0 ]; then refus "$OUT/cote$c.ckpt existe ; utiliser --reprendre"; fi
  for f in $DJ/cote${c}_A.gram $DJ/cote${c}_B.gram $DJ/cote${c}_T.mat $DJ/cote${c}_meta.txt classes/*.class; do echo "sha256 $(sha256sum "$f" | cut -c1-64)  $f" >> "$REC"; done
  SEL=""; [ "$ESSAI" -gt 0 ] && SEL="-Ddebut=0 -Dfin=$ESSAI"
  H=$(date +%Y%m%d_%H%M%S); L="$OUT/cote${c}_$H.stdout.log"; E="$OUT/cote${c}_$H.stderr.log"
  log "DEBUT cote $c ($TOT taches${SEL:+ ; ESSAI : taches 0..$((ESSAI - 1))}), $FILS fils, garde-fou $MAXH h ; journal $L"
  nice -n 10 timeout "${MAXH}h" "$J" -Xmx1g -DstopTouche=1 -Dveille=600 -DDmax=16 -Dseuil=0.2 $SEL -Dckpt="$OUT/cote$c.ckpt" -Dcat="$OUT/cote$c.taches" \
    -cp classes Rang88CertZ run $DJ/cote$c 1057 200 12 "$FILS" 6 > "$L" 2> "$E" &
  JPID=$!
  wait "$JPID"; CODE=$?
  while kill -0 "$JPID" 2>/dev/null; do wait "$JPID"; CODE=$?; done
  JPID=""; echo "$CODE" > "$OUT/cote${c}_$H.java.exit"
  NT=$(cat "$OUT"/cote${c}_*.stdout.log | grep -a -c '^TOUCHE'); TF=0; ls "$OUT"/*.touches > /dev/null 2>&1 && TF=1
  NE=$(cat "$OUT"/cote${c}_*.stdout.log | grep -a -c -E '^(ERREUR|ARRET)|Exception')
  log "FIN cote $c : code natif Java $CODE (124 = garde-fou) ; lignes TOUCHE $NT ; fichier de touche $TF ; lignes ERREUR/ARRET/Exception $NE ; stderr $(stat -c %s "$E") octets"
  if [ "$NT" -gt 0 ] || [ "$TF" = 1 ]; then log "TOUCHE au cote $c (code natif $CODE) : arret ; vecteur de norme <= 6 a verifier exactement sur SpiraleG ; l'autre cote n'est pas lance"; VERDICT=2; break; fi
  if [ "$INTERRUPTION" = 1 ]; then terminer 3 "INCOMPLET cote $c (interruption par signal, code natif $CODE) : relancer avec --reprendre"; fi
  case "$CODE" in
    0) ;;
    124|137|143) terminer 3 "INCOMPLET cote $c (code natif $CODE : garde-fou ou signal) : relancer avec --reprendre";;
    *) terminer 7 "ERREUR_JAVA cote $c (code natif $CODE) : rendre tel quel, ne pas reprendre sans examen";;
  esac
  if ! grep -a -q "^CATALOGUE_SHA256 $CAT ; TOTAL_TACHES $TOT$" "$L"; then log "cote $c : CATALOGUE ou TOTAL different de l'attendu ($CAT, $TOT)"; VERDICT=4; continue; fi
  # ---- 2bis mode ESSAI : couverture partielle attendue, recus compares a l'octet a la reference
  if [ "$ESSAI" -gt 0 ]; then
    timeout 3600 "$PY" -I outils/compare_recus.py "$OUT/cote$c.ckpt" "ref/$PRIM" > "$OUT/COMPARAISON_ESSAI_cote$c.txt" 2>&1; CR=$?
    if [ "$CR" = 0 ] && [ "$NE" = 0 ] && grep -a -q "^TACHES_TERMINEES $ESSAI/$TOT$" "$L" && grep -a -q "^COUVERTURE_PARTIELLE $ESSAI/$TOT " "$L" && grep -a -q "^TOTAL_TOUCHES 0$" "$L"; then
      echo "FIN_COTE $c ESSAI_OK $(date '+%F %T') : $ESSAI/$TOT taches, 0 touche, recus identiques a ref/$PRIM ($(head -1 "$OUT/COMPARAISON_ESSAI_cote$c.txt"))" >> "$REC"
    else log "cote $c : ESSAI_ECHEC (compare_recus.py code $CR ; voir $OUT/COMPARAISON_ESSAI_cote$c.txt)"; ESSAI_KO=1; fi
    continue
  fi
  # ---- 3 controles du cote termine
  if ! grep -a -q "^COUVERTURE_COMPLETE $TOT/$TOT ; CATALOGUE $CAT$" "$L" || ! grep -a -q "^TOTAL_TOUCHES 0$" "$L"; then
    log "cote $c : code 0 mais marqueurs terminaux absents (COUVERTURE_COMPLETE, TOTAL_TOUCHES 0)"; VERDICT=4; continue; fi
  RA=""; for r in $REFS; do RA="$RA ref/$r"; done
  timeout 3600 "$PY" -I outils/controle_execution.py "$OUT" "$c" "$TOT" "$CAT" $RA > "$OUT/CONTROLE_EXECUTION_cote$c.txt" 2>&1; CE=$?
  EC=$(timeout 3600 "$PY" -I outils/empreinte_canonique.py "$OUT/cote$c.ckpt" 2>&1 | tail -1 | grep -o 'empreinte canonique [0-9a-f]\{64\}' | cut -c21-)
  NL=$(ls "$OUT"/cote${c}_*.stdout.log | wc -l)
  JUM=OK
  if [ -n "$UATT" ]; then
    grep -a -q "^COMPTE_U (au signe pres, energie courte <= 1057/200) $UATT ; " "$L" && grep -a -q "^NOEUDS court $NCATT ; " "$L" || JUM=DIFFERENT
  fi
  log "cote $c : controle_execution.py code natif $CE ($(grep -a '^BILAN' "$OUT/CONTROLE_EXECUTION_cote$c.txt" | cut -c1-80)) ; lancements $NL ; empreinte canonique $EC ; predictions du jumeau $JUM"
  AUTRES=$(grep -a '^ECHEC' "$OUT/CONTROLE_EXECUTION_cote$c.txt" | grep -a -v -E '^ECHEC E1 (un seul journal|CHECKPOINT nouveau|SELECTION|EXECUTEES_CE_LANCEMENT|aucune ligne ERREUR)' | wc -l)
  if [ "$CE" = 0 ] && [ "$NL" = 1 ] && [ "$JUM" = OK ] && [ "$NE" = 0 ]; then
    echo "FIN_COTE $c COMPLET $(date '+%F %T') : $TOT/$TOT taches, 0 touche, un seul lancement, controle_execution 100 %, catalogue $CAT, empreinte canonique $EC" >> "$REC"
  elif [ "$CE" != 0 ] && [ "$NL" -gt 1 ] && [ "$AUTRES" = 0 ] && [ "$JUM" = OK ] && [ "$NE" = 0 ]; then
    echo "FIN_COTE $c COMPLET_REPRISE $(date '+%F %T') : $TOT/$TOT taches, 0 touche, $NL lancements (reprise declaree : seuls des controles E1 echouent), catalogue $CAT, empreinte canonique $EC" >> "$REC"
    [ "$VERDICT" = 0 ] && VERDICT=6
  else
    echo "FIN_COTE $c A_EXAMINER $(date '+%F %T') : complet sans touche, mais controle_execution code $CE, $AUTRES echec(s) hors E1 de reprise, lancements $NL, jumeau $JUM, lignes ERREUR $NE" >> "$REC"
    VERDICT=4
  fi
done
# ---- 4 verdict, puis empreintes des sorties EN DERNIER
if [ "$VERDICT" = 2 ]; then terminer 2 "TOUCHE (voir le recu ; l'autre cote n'a pas ete lance si la touche est au cote 1)"; fi
if [ "$ESSAI" -gt 0 ]; then
  if [ "$VERDICT" = 0 ] && [ "$ESSAI_KO" = 0 ]; then terminer 9 "ESSAI_OK ($ESSAI taches par cote, recus identiques aux references ; AUCUNE conclusion)"; else terminer 8 "ESSAI_ECHEC"; fi
fi
case "$VERDICT" in
  0) terminer 0 "COMPLET_SANS_TOUCHE $NOM : deux cotes complets, 0 touche, un seul lancement chacun, controles 100 % (aucune affirmation d'extremalite avant raccord, non-isometrie et contre-audit)";;
  6) terminer 6 "COMPLET_SANS_TOUCHE_REPRISE_DECLAREE $NOM (a confirmer sur SpiraleG)";;
  *) terminer 4 "A_EXAMINER $NOM (rendre tout tel quel, ne rien corriger)";;
esac
