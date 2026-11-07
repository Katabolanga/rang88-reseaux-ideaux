# -*- coding: utf-8 -*-
"""comparer_enum88.py -- recoupement numerique (Claude, 7 nov. 2026, preparation de la version 1.5).

Compare, pour un cote de X(P461 sigma_91), le journal de la seconde implantation enum88 (mode 1, critere complet)
au journal de Rang88CertZ : COMPTE_U, histogramme des energies courtes (32 cases), nombre de CVP et TOTAL_TOUCHES.
Les nombres de noeuds ne sont pas compares : les deux programmes n'enumerent pas dans le meme ordre.
Ce n'est pas un certificat : enum88 calcule ses bornes en flottants, sans analyse d'erreur, et il a le meme auteur.

Usage : python3 -I comparer_enum88.py m1_P461s91_cote<s>.log <journal stdout de Rang88CertZ du meme cote>
Code de sortie 0 si tout concorde."""
import re, sys

def lire_enum88(f):
    t = open(f, encoding="ascii", errors="replace").read()
    cu = int(re.search(r"^COMPTE_U (\d+)$", t, re.M).group(1))
    h = re.search(r"^HIST (.*)$", t, re.M).group(1)
    cvp = int(re.search(r"^CVP (\d+) ;", t, re.M).group(1))
    tt = int(re.search(r"^TOTAL_TOUCHES (\d+)$", t, re.M).group(1))
    u0 = re.search(r"^U0 : (\d+) vecteurs", t, re.M)
    code = re.search(r"^code (\d+)$", t, re.M)
    return cu, hist(h), cvp, tt, (int(u0.group(1)) if u0 else None), (int(code.group(1)) if code else None)

def lire_java(f):
    t = open(f, encoding="ascii", errors="replace").read().replace("\r\n", "\n")
    m = re.search(r"^COMPTE_U \(au signe pres, energie courte <= [0-9/]+\) (\d+) ; histogramme (.*)$", t, re.M)
    no = re.search(r"^NOEUDS court \d+ ; fibre \d+ ; CVP (\d+)$", t, re.M)
    tt = int(re.search(r"^TOTAL_TOUCHES (\d+)$", t, re.M).group(1))
    return int(m.group(1)), hist(m.group(2)), int(no.group(1)), tt

def hist(s):
    return {(a, b): int(v) for a, b, v in re.findall(r"\[(\d+\.\d),(\d+\.\d)\):(\d+)", s)}

if len(sys.argv) != 3:
    raise SystemExit(__doc__)
e, j = lire_enum88(sys.argv[1]), lire_java(sys.argv[2])
NB = [0, 0]
def ctl(nom, ok):
    NB[0] += 1; NB[1] += (not ok)
    print(("OK    " if ok else "ECHEC ") + nom)
ctl("code de sortie d'enum88 = 0", e[5] == 0)
ctl("U0 = 1 (seul y = 0 dans la boule de la fibre au rayon S*DB)", e[4] == 1)
ctl("COMPTE_U enum88 = COMPTE_U Rang88CertZ (%d, %d)" % (e[0], j[0]), e[0] == j[0])
ctl("histogramme identique case par case (%d cases, %d cases)" % (len(e[1]), len(j[1])), e[1] == j[1] and len(e[1]) > 0)
ctl("CVP enum88 = CVP Rang88CertZ (%d, %d)" % (e[2], j[2]), e[2] == j[2])
ctl("TOTAL_TOUCHES = 0 dans les deux journaux (%d, %d)" % (e[3], j[3]), e[3] == 0 and j[3] == 0)
print("BILAN comparer_enum88 : %d controles, %d echecs" % tuple(NB))
sys.exit(0 if NB[1] == 0 else 1)
