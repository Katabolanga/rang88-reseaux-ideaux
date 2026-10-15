# -*- coding: utf-8 -*-
"""verifier_corps.py -- controle exact des donnees du corps (note, notations et prop. 2.3) : data/corps/rang88_m115c0_data.txt.

  K1  Pm (premier element du fichier) est unitaire, de degre 44, et Pm(c) = 0 dans Z[zeta], c = zeta + zeta^-1 ; comme
      [Q(c) : Q] = 44, c'est le polynome minimal de c, et O+ = Z[c] a pour base (c^k), 0 <= k < 44 ;
  K2  beta_0 (second element) : la matrice T = (Tr_{L+/Q}(beta_0 c^(i+j))) est entiere, de determinant 1 et definie
      positive ; donc beta_0 est totalement positif (forme trace definie positive) et beta_0 D = O+ (le dual de O+ pour
      Tr(beta_0 x y) est (beta_0 D)^-1, egal a O+ puisque T est entiere de determinant 1) ;
  K3  la matrice de Gram de H = (O_L, beta_0), G_H = (Tr_L(beta_0 zeta^(i-j))), base zeta^(i-1), est entiere, paire, de
      determinant 1 et definie positive.
Usage (depuis la racine du depot) : python -I code/verification/verifier_corps.py      (quelques secondes)"""
import re, sys, os, hashlib
from fractions import Fraction as Fr
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
F = os.path.join(RACINE, "data", "corps", "rang88_m115c0_data.txt")
NB = [0, 0]
def controle(nom, cond):
    NB[0] += 1
    if not cond: NB[1] += 1
    print(("OK    " if cond else "ECHEC ") + nom); sys.stdout.flush()
def poly(s, var="x"):
    s = s.replace(" ", "").replace("\n", ""); assert re.fullmatch(r"[-+*/^0-9x]+", s)
    s = s.replace("-", "+-"); co = {}
    for t in s.split("+"):
        if not t: continue
        if var in t:
            c, _, e = t.partition(var); e = int(e[1:]) if e else 1; c = c.rstrip("*")
            c = Fr(1) if c == "" else (Fr(-1) if c == "-" else Fr(c))
        else: c, e = Fr(t), 0
        co[e] = co.get(e, 0) + c
    return [co.get(i, Fr(0)) for i in range(max(co) + 1)]
def bareiss(M):
    n = len(M); A = [list(r) for r in M]; prev = 1; mineurs = []
    for k in range(n):
        piv = A[k][k]
        if piv == 0: return 0, None
        mineurs.append(piv)
        for i in range(k + 1, n):
            aik = A[i][k]; Ai = A[i]; Ak = A[k]
            for j in range(k + 1, n): Ai[j] = (Ai[j] * piv - aik * Ak[j]) // prev
            Ai[k] = 0
        prev = piv
    return A[n - 1][n - 1], mineurs
m, n, nh = 115, 88, 44
print("donnees : data/corps/rang88_m115c0_data.txt SHA-256", hashlib.sha256(open(F, "rb").read()).hexdigest())
t = open(F, encoding="ascii").read().strip(); assert t[0] == "[" and t[-1] == "]"
parts = t[1:-1].split(",", 2)
Pm = poly(parts[0]); B0 = poly(parts[1])
print("   Pm = x^44 - x^43 - 44*x^42 + ... + 24*x + 1 ; beta_0 = %s*x^43 + ... + %s" % (B0[43], B0[0]))
def mulc(a, b):
    r = [0] * m
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y: r[(i + j) % m] += x * y
    return r
def ram(k):
    k %= m
    if k == 0: return 88
    if k % 23 == 0: return -22
    if k % 5 == 0: return -4
    return 1
def polmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return r
def poldivex(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        q[i] = a[i + len(b) - 1]
        for j, y in enumerate(b): a[i + j] -= q[i] * y
    assert not any(a); return q
ym = lambda k: [-1] + [0] * (k - 1) + [1]
PHI = poldivex(polmul(ym(115), ym(1)), polmul(ym(5), ym(23)))
def redphi(a):
    a = list(a) + [0] * (m - len(a))
    for i in range(m - 1, n - 1, -1):
        c = a[i]
        if c:
            for j, y in enumerate(PHI): a[i - n + j] -= c * y
    return a[:n]
cc = [0] * m; cc[1] = 1; cc[114] = 1
cp = [[1] + [0] * (m - 1)]
for k in range(1, 2 * nh): cp.append(mulc(cp[-1], cc))
acc = [0] * m
for k, c in enumerate(Pm): acc = [x + int(c) * y for x, y in zip(acc, cp[k])]
controle("K1 Pm entier, unitaire, de degre 44, et Pm(c) = 0 dans Z[zeta_115]", all(c.denominator == 1 for c in Pm) and len(Pm) == 45 and Pm[44] == 1 and not any(redphi(acc)))
tau = [sum(v * ram(i) for i, v in enumerate(cp[k])) for k in range(2 * nh)]     # Tr_L(c^k)
B0p = B0 + [Fr(0)] * (nh - len(B0))
s = [sum(B0p[j] * tau[j + k] for j in range(nh)) / 2 for k in range(nh)]         # Tr+(beta_0 c^k), k < 44
# Tr+(beta_0 c^k) pour 44 <= k < 88 : reduction de c^k modulo Pm dans la base c^0..c^43
red = {}
for k in range(2 * nh - 1):
    if k < nh: red[k] = [Fr(int(i == k)) for i in range(nh)]
    else:
        prev = red[k - 1]; top = prev[nh - 1]
        v = [Fr(0)] + prev[:nh - 1]
        red[k] = [v[i] - top * Pm[i] for i in range(nh)]
T = [[sum(red[i + j][l] * s[l] for l in range(nh)) for j in range(nh)] for i in range(nh)]
controle("K2 T = (Tr+(beta_0 c^(i+j))) entiere et symetrique", all(x.denominator == 1 for r in T for x in r) and all(T[i][j] == T[j][i] for i in range(nh) for j in range(nh)))
dT, mT = bareiss([[int(x) for x in r] for r in T])
controle("K2 det T = 1 et T definie positive (44 mineurs principaux > 0) : beta_0 totalement positif et beta_0 D = O+", dT == 1 and mT is not None and all(x > 0 for x in mT))
# K3 : Gram de H
bL = [Fr(0)] * m
for k, c in enumerate(B0p):
    if c:
        for i, v in enumerate(cp[k]):
            if v: bL[i] += c * v
tb = [sum(bL[i] * ram(i + r) for i in range(m)) for r in range(m)]
controle("K3 Tr_L(beta_0 zeta^r) entier pour tout r, et reel (symetrie r -> -r)", all(x.denominator == 1 for x in tb) and all(tb[r] == tb[(-r) % m] for r in range(m)))
GH = [[int(tb[(i - j) % m]) for j in range(n)] for i in range(n)]
dG, mG = bareiss(GH)
controle("K3 G_H paire, de determinant 1, definie positive (88 mineurs > 0) ; diagonale %d" % GH[0][0], all(GH[i][i] % 2 == 0 for i in range(n)) and dG == 1 and mG is not None and all(x > 0 for x in mG))
print("BILAN : %d controles, %d echecs" % (NB[0], NB[1]))
print("FIN_OK" if NB[1] == 0 else "FIN_ECHEC")
sys.exit(0 if NB[1] == 0 else 1)
