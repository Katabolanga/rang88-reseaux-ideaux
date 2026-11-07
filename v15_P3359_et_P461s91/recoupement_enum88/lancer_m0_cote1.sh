#!/bin/bash
# M10 mission 4 : comptage independant de U (cote court) de P461s91, cote 1, BA = 1057/200, sur SpiraleG (3 fils, nice 6).
M=/mnt/c/Users/ivang/lots/G64_AUTONOMIE_20261102/z2/couv/missions/M10/m4
L=/mnt/c/Users/ivang/lots/R88_P461S91_CERT_V2_20261019
cd ~/missions/M10 || exit 9
gcc -O3 -march=native -pthread -Wall -DNIV=5 -o enum88_n5 $M/enum88.c -lm || exit 8
sha256sum $M/enum88.c enum88_n5 > enum88_n5.sha256
grep MemAvailable /proc/meminfo
setsid nohup bash -c "timeout 6h nice -n 6 ./enum88_n5 $L/java_P461s91/cote1 1057 200 12 3 0 > m0_P461s91_cote1.log 2>&1; echo \"code \$?\" >> m0_P461s91_cote1.log" > /dev/null 2>&1 < /dev/null &
sleep 5; ps -eo pid,ni,pcpu,etime,args | grep enum88_n5 | grep -v grep; cat m0_P461s91_cote1.log
