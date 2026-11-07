#!/bin/bash
M=/mnt/c/Users/ivang/lots/G64_AUTONOMIE_20261102/z2/couv/missions/M10/m4
cd ~/missions/M10 || exit 9
gcc -O3 -march=x86-64-v3 -pthread -static -DNIV=5 -o enum88_n5_statique $M/enum88.c -lm || exit 8
cp enum88_n5_statique $M/../bertha/
sha256sum $M/enum88.c enum88_n5_statique
L=/mnt/c/Users/ivang/lots/R88_P461S91_CERT_V2_20261019
echo "controle positif du binaire statique :"; timeout 300 ./enum88_n5_statique $L/java_P461/cote1 7 2 12 2 1 | grep -E 'COMPTE_U|TOTAL_TOUCHES|U0|FIN'
