#!/bin/bash
# M10, mission 4 (7 nov. 2026) : APRES la fin du lanceur Java de la replication (PID 398281, verifie par /proc/PID/cmdline),
# lance la seconde implantation enum88 (mode 1 = critere complet du th. 4.6) sur les deux cotes de X(P461 sigma_91),
# 4 fils par cote (8 fils au total = part de M10), nice 6, timeout 12 h chacun.  Ecrit seulement dans ~/m10/enum88/.
# NB : la garde thermique de Claude principal vise gp, julia, java et python ; enum88 n'en fait pas partie (signale dans la NOTE).
set -u
R=~/m10/R88_P461S91_CERT_V2_20261019; W=~/m10/enum88; PIDJ=398281
mkdir -p "$W" && cd "$W" || exit 9
J=journal_enum88.txt
cp /mnt/c/Users/Joueur/m10/enum88_n5_statique . && chmod +x enum88_n5_statique
ATT=53a2b7640345b183c1a9138abe0b17f7eed5f6f1b207e3968eedec5cd8fdcf70
H=$(sha256sum enum88_n5_statique | cut -c1-64)
[ "$H" = "$ATT" ] || { echo "$(date '+%F %T') ECHEC empreinte du binaire $H" >> $J; exit 11; }
if kill -0 $PIDJ 2>/dev/null; then
  grep -q lancer_cert_P461s91 /proc/$PIDJ/cmdline 2>/dev/null || { echo "$(date '+%F %T') REFUS : $PIDJ n'est pas le lanceur" >> $J; exit 5; }
fi
echo "$(date '+%F %T') attente de la fin du lanceur Java $PIDJ" >> $J
while kill -0 $PIDJ 2>/dev/null; do sleep 120; done
echo "$(date '+%F %T') lanceur Java termine ; verdict : $(cat $R/sorties/VERDICT.txt 2>/dev/null)" >> $J
grep MemAvailable /proc/meminfo >> $J
for c in 1 2; do
  setsid nohup bash -c "timeout 12h nice -n 6 ./enum88_n5_statique $R/java_P461s91/cote$c 1057 200 12 4 1 > m1_P461s91_cote$c.log 2>&1; echo \"code \$?\" >> m1_P461s91_cote$c.log" > /dev/null 2>&1 < /dev/null &
  echo "$(date '+%F %T') enum88 cote $c lance (enveloppe $!)" >> $J
done
sleep 20; ps -eo pid,ni,pcpu,etime,args | grep enum88_n5_statique | grep -v grep >> $J
