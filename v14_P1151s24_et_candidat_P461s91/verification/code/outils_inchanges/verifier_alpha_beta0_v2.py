# -*- coding: utf-8 -*-
"""verifier_alpha_beta0.py -- reponse a la lacune relevee par Astra (contre-audit, raccord, 16 octobre 2026) : le verificateur de
raccord annonce alpha = beta0 / nu sans le tester.  Controle EXACT, en rationnels, sans PARI/GP (Claude, 16 octobre 2026) :
  B1  le fichier du corps data/corps/rang88_m115c0_data.txt donne [Pm, BETA0, ...] ; Pm unitaire de degre 44 ;
  B2  beta0 engendre l'inverse de la differente de O+ = Z[c] : la forme Tr_{L+/Q}(beta0 x y) sur la base (c^i) est entiere et
      de determinant +-1 (note, prop. 4.1 (b) : « Tr+(beta0 x y) est de determinant 1 sur O+ ») ;
  B3  pour P139, P599, P4969, P4049 : ALPHA * NU = BETA0 dans Q[x]/(Pm), ALPHA et NU etant ceux de I_data.gp (ceux dont le
      verificateur de raccord deduit GRAM).
Aucun determinant 88 x 88, aucun balayage.
Historique : v1 (SHA b4687d9b...) avait un defaut dans les identites de Newton (i = k inclus pour k <= d), trouve par Claude a 13 h 27 et par Astra (13 h 29) ; v2 corrige Newton et sort avec un code non nul en cas d echec.  Usage : python3 -I verifier_alpha_beta0.py DONNEES_CORPS I_data_P139 I_data_P599 ..."""
import sys, re, hashlib
from fractions import Fraction as Fr

def poly(s, var="x"):
    s = s.replace(" ", "").replace("\n", "").replace("-", "+-"); co = {}
    for t in s.split("+"):
        if not t: continue
        if var in t:
            c, _, e = t.partition(var); e = int(e[1:]) if e else 1; c = c.rstrip("*")
            c = Fr(1) if c == "" else (Fr(-1) if c == "-" else Fr(c))
        else: c, e = Fr(t), 0
        co[e] = co.get(e, 0) + c
    return [co.get(i, Fr(0)) for i in range(max(co) + 1)]
def mul(a, b):
    r = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i + j] += x * y
    return r
def red(a, P):        # reduction modulo P unitaire
    a = a[:]; d = len(P) - 1
    for i in range(len(a) - 1, d - 1, -1):
        c = a[i]
        if c:
            for j in range(d + 1): a[i - d + j] -= c * P[j]
    a = a[:d]; return a + [Fr(0)] * (d - len(a))
def det_bareiss(M):
    M = [r[:] for r in M]; n = len(M); signe = 1; prec = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            p = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if p is None: return 0
            M[k], M[p] = M[p], M[k]; signe = -signe
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prec
        prec = M[k][k]
    return signe * M[n - 1][n - 1]
NB = [0, 0]
def controle(nom, c):
    NB[0] += 1; NB[1] += (not c); print(("OK    " if c else "ECHEC ") + nom)

f = sys.argv[1]
txt = open(f, encoding="ascii").read()
print("donnees du corps : %s SHA-256 %s" % (f.split("/")[-1], hashlib.sha256(open(f, "rb").read()).hexdigest()))
champs = txt[txt.index("[") + 1: txt.rindex("]")].split(",")
Pm = poly(champs[0]); B0 = poly(champs[1])
controle("B1 Pm unitaire de degre 44, a coefficients entiers", len(Pm) == 45 and Pm[44] == 1 and all(c.denominator == 1 for c in Pm))
d = 44
# traces Tr(x^k), k = 0..2d-2, par les sommes de Newton des racines de Pm
a = [Pm[d - i] for i in range(d + 1)]          # x^d + a1 x^(d-1) + ... : a[i] = coefficient de x^(d-i)
s = [Fr(d)] + [Fr(0)] * (2 * d)
for k in range(1, 2 * d + 1):            # identites de Newton : k <= d : s_k + a1 s_{k-1} + ... + a_{k-1} s_1 + k a_k = 0 ;
    if k <= d:                           #                       k > d  : s_k + a1 s_{k-1} + ... + a_d s_{k-d} = 0
        acc = sum((a[i] * s[k - i] for i in range(1, k)), Fr(0)) + k * a[k]
    else:
        acc = sum((a[i] * s[k - i] for i in range(1, d + 1)), Fr(0))
    s[k] = -acc
def trace(pl):      # Tr_{L+/Q}(pl(x)) pour pl de degre < 2d-1 ... on reduit d'abord
    pl = red(pl, Pm); return sum(c * s[k] for k, c in enumerate(pl))
controle("B1 Tr(1) = 44 et Tr(c) = 1 (somme des zeta^k + zeta^-k sur (Z/115)^*/{+-1}, = mu(115) = 1)", s[0] == 44 and s[1] == 1)
# forme Tr(beta0 c^(i+j))
tb = [trace(mul(B0, [Fr(0)] * k + [Fr(1)])) for k in range(2 * d - 1)]
entiere = all(t.denominator == 1 for t in tb)
G = [[int(tb[i + j]) for j in range(d)] for i in range(d)] if entiere else None
dg = det_bareiss(G) if entiere else None
controle("B2 Tr(beta0 c^(i+j)) entiere sur la base (c^i) de O+ ; determinant = %s (attendu +-1 : beta0 * Differente = O+)" % dg, entiere and abs(dg) == 1)
for g in sys.argv[2:]:
    t = open(g, encoding="ascii").read()
    m = {k: re.search(r"^%s = (.*?);\s*$" % k, t, re.S | re.M).group(1) for k in ("NU", "ALPHA", "PREMIERS")}
    al, nu = poly(m["ALPHA"]), poly(m["NU"])
    prod = red(mul(al, nu), Pm)
    controle("B3 %s (PREMIERS = %s ; I_data.gp SHA-256 %s...) : ALPHA * NU = BETA0 modulo Pm" % (g.split("/")[-3] if "/entrees/" in g else g, m["PREMIERS"],
             hashlib.sha256(open(g, "rb").read()).hexdigest()[:16]), prod == red(B0, Pm))
print("BILAN : %d controles, %d echecs" % (NB[0], NB[1]))
print("ALPHA_BETA0_OK" if NB[1] == 0 else "ALPHA_BETA0_ECHEC")
sys.exit(0 if NB[1] == 0 else 1)          # v2 (remarque d'Astra, 13 h 29) : code de sortie non nul en cas d'echec
