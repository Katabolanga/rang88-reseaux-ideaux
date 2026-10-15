# -*- coding: utf-8 -*-
"""verifier_hmoins_caracteres.py -- second calcul, en Python (entiers et rationnels exacts, sans PARI/GP et sans aucun
calcul de groupe de classes), de h^-(115), des normes des nombres de Bernoulli generalises et du nombre d'orbites
(note, prop. 2.2 et 2.5, tableau 1).  Meme methode que hmoins115.gp et caracteres115.gp, ecriture independante.

  H1  h^-(m) = Q w prod_{chi impair} (-B_{1,chi*}/2), Q = 2, w = 2m, pour m = 87, 65, 85 (valeurs de controle 1536, 64,
      6205) et m = 115 ; arithmetique exacte dans Q(zeta_N), N = ppcm(p - 1, q - 1), modulo Phi_N ;
  H2  pour chaque classe de conjugaison rationnelle de caracteres impairs modulo 115 : ordre, conducteur, norme de
      -B_{1,chi*}/2 ; une seule classe a une norme divisible par 3, par 331, par 45 013, avec valuation 1 ;
  H3  noyaux des trois caracteres chi_3, chi_331, chi_45013 ; nombre de classes et d'orbites par support (tableau 1) ;
      total 44 697 909 classes et 508 463 orbites ; recomptage par la formule de Burnside.
  (h(L^+) = 1 est le theoreme de Miller, cite par la note ; il n'est pas recalcule ici.)
Usage (depuis la racine du depot) : python -I code/verification/verifier_hmoins_caracteres.py      (quelques secondes)"""
import sys
from fractions import Fraction as Fr
from math import gcd
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

NB = [0, 0]
def controle(nom, cond):
    NB[0] += 1
    if not cond: NB[1] += 1
    print(("OK    " if cond else "ECHEC ") + nom); sys.stdout.flush()

def polcyclo(N):
    """Phi_N a coefficients entiers, par divisions successives de x^N - 1"""
    P = [-1] + [0] * (N - 1) + [1]
    for d in range(1, N):
        if N % d == 0:
            Q = polcyclo(d); P = divex(P, Q)
    return P
def divex(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        q[i] = a[i + len(b) - 1] // b[-1]
        for j, y in enumerate(b): a[i + j] -= q[i] * y
    assert not any(a); return q

class Cyclo:
    """arithmetique exacte dans Q(zeta_N) = Q[w]/Phi_N"""
    def __init__(self, N):
        self.N = N; self.P = polcyclo(N); self.d = len(self.P) - 1
        self.pw = []
        for e in range(N):                               # w^e reduit
            v = [0] * (e + 1); v[e] = 1; self.pw.append(self.red(v))
    def red(self, a):
        a = list(a) + [0] * max(0, self.d - len(a)); d = self.d
        for i in range(len(a) - 1, d - 1, -1):
            c = a[i]
            if c:
                for j, y in enumerate(self.P): a[i - d + j] -= c * y
        return a[:d]
    def mul(self, a, b):
        r = [0] * (2 * self.d - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y: r[i + j] += x * y
        return self.red(r)

def calcul(p, q, gp_, gq_, verbeux=False):
    m = p * q; a1, a2 = p - 1, q - 1; N = a1 * a2 // gcd(a1, a2); e1, e2 = N // a1, N // a2
    K = Cyclo(N)
    ind1 = {pow(gp_, k, p): k for k in range(a1)}; ind2 = {pow(gq_, k, q): k for k in range(a2)}
    assert len(ind1) == a1 and len(ind2) == a2, "racines primitives"
    def expo(i, j, a):   # chi_{i,j}(a) = w^expo, pour le caractere primitif associe
        return (e1 * i * (ind1[a % p] if i else 0) + e2 * j * (ind2[a % q] if j else 0)) % N
    def B1(i, j):
        f = (p if i else 1) * (q if j else 1)
        s = [Fr(0)] * K.d
        for a in range(1, f + 1):
            if gcd(a, f) == 1:
                v = K.pw[expo(i, j, a)]
                s = [x + a * y for x, y in zip(s, v)]
        return [x / f for x in s]
    impairs = []
    for i in range(a1):
        for j in range(a2):
            if expo(i, j, m - 1) == N // 2: impairs.append((i, j))
            else: assert expo(i, j, m - 1) == 0
    prod = [Fr(1)] + [Fr(0)] * (K.d - 1)
    Bs = {}
    for (i, j) in impairs:
        B = B1(i, j); Bs[(i, j)] = B
        prod = K.mul(prod, [-x / 2 for x in B])
    assert all(x == 0 for x in prod[1:]), "produit non rationnel"
    h = 2 * (2 * m) * prod[0]
    return len(impairs), h, (K, Bs, expo, N, e1, e2, ind1, ind2)

print("== H1 nombre de classes relatif")
for (p, q, g1, g2, att) in ((3, 29, 2, 2, 1536), (5, 13, 2, 2, 64), (5, 17, 2, 3, 6205)):
    ni, h, _ = calcul(p, q, g1, g2)
    controle("H1 h^-(%d) = %s (%d caracteres impairs) ; valeur attendue %d" % (p * q, h, ni, att), h == att)
ni, h, (K, Bs, expo, N, e1, e2, ind1, ind2) = calcul(5, 23, 2, 5)
controle("H1 h^-(115) = %s = 3 * 331 * 45013 (%d caracteres impairs)" % (h, ni), h == 44697909 == 3 * 331 * 45013 and ni == 44)

print("== H2 classes rationnelles de caracteres impairs modulo 115")
a1, a2 = 4, 22
units = [k for k in range(N) if gcd(k, N) == 1]
vus = set(); classes = []
for (i, j) in sorted(Bs):
    if (i, j) in vus: continue
    orb = sorted({((k * i) % a1, (k * j) % a2) for k in units})
    vus |= set(orb)
    nrm = [Fr(1)] + [Fr(0)] * (K.d - 1)
    for c in orb: nrm = K.mul(nrm, [-x / 2 for x in Bs[c]])
    assert all(x == 0 for x in nrm[1:])
    d = (a1 // gcd(i, a1)) * (a2 // gcd(j, a2)) // gcd(a1 // gcd(i, a1), a2 // gcd(j, a2))
    f = (5 if i else 1) * (23 if j else 1)
    classes.append(((i, j), d, f, len(orb), nrm[0]))
    print("   chi_(%d,%d) : ordre %d, conducteur %d, %d conjugues ; N(-B1/2) = %s" % (i, j, d, f, len(orb), nrm[0]))
tot = Fr(1)
for c in classes: tot *= c[4]
controle("H2 six classes rationnelles ; produit des normes * Q * w = 44697909", len(classes) == 6 and tot * 2 * 230 == 44697909)
def val(x, p):
    v = 0; x = Fr(x)
    while x != 0 and (x.numerator % p == 0): x /= p; v += 1
    return v
RESP = {}
for p in (3, 331, 45013):
    L = [c for c in classes if c[4] != 0 and c[4].numerator % p == 0]
    controle("H2 p = %d : une seule classe de caracteres a une norme divisible par p, de valuation 1 (chi_%s, ordre %d)" % (p, L[0][0] if L else None, L[0][1] if L else 0),
             len(L) == 1 and val(L[0][4], p) == 1)
    RESP[p] = L[0]
print("== H3 noyaux et orbites")
G = [a for a in range(1, 115) if gcd(a, 115) == 1]
KER = {p: {a for a in G if expo(RESP[p][0][0], RESP[p][0][1], a) == 0} for p in RESP}
controle("H3 noyau de chi_3 : ordre 44 (corps fixe Q(sqrt(-23))) ; chi_3 = symbole de Legendre modulo 23",
         len(KER[3]) == 44 and all((a in KER[3]) == (pow(a, 11, 23) == 1) for a in G))
controle("H3 noyau de chi_331 = {1, 22, 24, 68}", KER[331] == {1, 22, 24, 68})
controle("H3 noyau de chi_45013 = {1, 91}", KER[45013] == {1, 91})
attendu = {(): (1, 1, 1), (3,): (2, 2, 1), (331,): (330, 22, 15), (3, 331): (660, 44, 15), (45013,): (45012, 44, 1023),
           (3, 45013): (90024, 88, 1023), (331, 45013): (14853960, 88, 168795), (3, 331, 45013): (29707920, 88, 337590)}
okt = True; tcl = 0; tor = 0
for S, (ncl, taille, nor) in attendu.items():
    Kint = set(G); nel = 1
    for p in S: Kint &= KER[p]; nel *= p - 1
    osz = 88 // len(Kint); no = Fr(nel, osz)
    print("   support %-18s : %9d classes, orbites de taille %2d, %7s orbites" % (str(list(S)), nel, osz, no))
    okt &= (nel, osz, no) == (ncl, taille, nor); tcl += nel; tor += no
controle("H3 tableau 1 de la note : classes, tailles et nombres d'orbites par support ; total %d classes, %s orbites" % (tcl, tor), okt and tcl == 44697909 and tor == 508463)
bur = Fr(sum((3 if a in KER[3] else 1) * (331 if a in KER[331] else 1) * (45013 if a in KER[45013] else 1) for a in G), 88)
controle("H3 formule de Burnside : (1/88) sum_a |Fix(a)| = %s" % bur, bur == 508463)
print("BILAN : %d controles, %d echecs" % (NB[0], NB[1]))
print("FIN_OK" if NB[1] == 0 else "FIN_ECHEC")
sys.exit(0 if NB[1] == 0 else 1)
