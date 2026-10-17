# -*- coding: utf-8 -*-
"""verifier_cadran.py -- verification EXACTE, SANS PARI/GP et SANS GRH, des etiquettes du cadran de la couche sigma_24.
Claude, 17 octobre 2026.  Reprend les fonctions de verifier_non_isometrie_P4969_v2.py (verification_P4969/code/verification).

Entrees : ../../verification_P4969/data/P139/certificat_K22.txt (P22, RACINE, GAMMA = Gamma_139, XI_2..XI_11 ; paru avec la note)
          cadran_sans_GRH_certificats.txt (une ligne par ideal I : nom|sorte|p|lien|r|e|c|Gamma, produite par cadran_sans_GRH.gp).
Pour chaque ideal I de L (sorte a/A : P = (p, g(zeta)), g = y^2 + g1 y + g0 de degre 2 ; sorte b : I = P sigma_24(P), P = (p, zeta - rP) ;
sorte c : I = P = (p, zeta - rP), de degre 1), on verifie SANS faire confiance a PARI :
  (L) le lien : g divise Phi_115 mod p et est irreductible (discriminant non residu), ou Phi_115(rP) = 0 mod p ; et theta mod P = r ;
      N_{L/K}(I) = q^e avec q = (p, theta - r), e = 2 (sortes a, A, b) ou 1 (sorte c) ;
  (G) Gamma entier algebrique de K, |N(Gamma)| = p^331, valuation 331 en q et 0 aux 21 autres premiers au-dessus de p : (Gamma) = q^331 ;
  (D) logarithmes discrets mod 331 aux 88 premiers de degre 1 au-dessus des 4 premiers l = 1 mod 331*115 : rangs 10 et 11, puis
      resolution de e lambda(Gamma_q) = 2 c lambda(Gamma_139) mod <lambda(xi_a)> ; c doit egaler la valeur de PARI ;
  (H) heure : c dans 2^h mu_22 ; composante 3 : 4p = a^2 + 23 b^2 ou non.
Preuve que c est l'etiquette [I]_331 = c [P139]_331 : addendum, proposition « le cadran sans GRH ».
Usage : python verifier_cadran.py   (depuis ce dossier).  Code de sortie 0 seulement si tout passe."""
import os, sys, hashlib
from fractions import Fraction as Fr
from math import lcm

ICI = os.path.dirname(os.path.abspath(__file__))
F139 = os.path.normpath(os.path.join(ICI, "..", "..", "verification_P4969", "data", "P139", "certificat_K22.txt"))
FCAD = os.path.join(ICI, "cadran_sans_GRH_certificats.txt")
for f in (__file__, F139, FCAD):
    print("%s : SHA-256 %s" % (os.path.basename(f), hashlib.sha256(open(f, "rb").read()).hexdigest()))
OK = []
def controle(nom, cond):
    OK.append((nom, bool(cond)))
    print(("OK    " if cond else "ECHEC ") + nom); sys.stdout.flush()
    if not cond: raise SystemExit("ECHEC : " + nom)

def lire_poly(s, var):
    s = s.replace(" ", "").replace("-", "+-")
    co = {}
    for t in s.split("+"):
        if not t: continue
        if var in t:
            c, _, e = t.partition(var)
            e = int(e[1:]) if e else 1
            c = c.rstrip("*")
            c = Fr(1) if c == "" else (Fr(-1) if c == "-" else Fr(c))
        else:
            c, e = Fr(t), 0
        co[e] = co.get(e, 0) + c
    return [co.get(i, Fr(0)) for i in range(max(co) + 1)]

C139 = {}
for l in open(F139, encoding="ascii"):
    k, _, v = l.strip().partition(" = ")
    if k: C139[k] = v
P22 = [int(c) for c in lire_poly(C139["P22"], "w")]
controle("P22 unitaire de degre 22, a coefficients entiers", len(P22) == 23 and P22[22] == 1)
XI = {a: lire_poly(C139["XI_%d" % a], "w") for a in range(2, 12)}
G139 = lire_poly(C139["GAMMA"], "w"); R139 = int(C139["RACINE"])
CIBLES = []
for l in open(FCAD, encoding="ascii"):
    l = l.strip()
    if not l or l.startswith("#"): continue
    nom, s, p, lien, r, e, c, gam = l.split("|")
    CIBLES.append(dict(nom=nom, s=s, p=int(p), lien=lien, r=int(r), e=int(e), c=int(c), G=lire_poly(gam, "w")))
controle("%d ideaux lus dans le certificat du cadran" % len(CIBLES), len(CIBLES) >= 30)
N = 22; M = 115; H = {1, 22, 24, 68}

# ------------------------------------------------------------ Phi_115, theta, P22(theta) = 0
def mulc(a, b):
    r = [0] * M
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y: r[(i + j) % M] += x * y
    return r
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
def cyclo_prod(n): return [-1] + [0] * (n - 1) + [1]
PHI = poldivex(polmul(cyclo_prod(115), cyclo_prod(1)), polmul(cyclo_prod(5), cyclo_prod(23)))
controle("Phi_115 de degre 88, unitaire", len(PHI) == 89 and PHI[88] == 1)
def redphi(a):
    a = a[:]
    for i in range(len(a) - 1, 87, -1):
        c = a[i]
        if c:
            for j, y in enumerate(PHI): a[i - 88 + j] -= c * y
    return a[:88]
th = [0] * M
for k in H: th[k] = 1
acc = [0] * M; pw = [1] + [0] * (M - 1)
for c in P22:
    acc = [x + c * y for x, y in zip(acc, pw)]; pw = mulc(pw, th)
controle("P22(theta) = 0 dans Z[zeta_115], theta = zeta + zeta^22 + zeta^24 + zeta^68", not any(redphi(acc)))
controle("{1,22,24,68} sous-groupe de (Z/115)^* (K = Fix<sigma_22>)", all((a * b) % 115 in H for a in H for b in H))
reps = []; vus = set()
for a in range(1, 115):
    if a % 5 and a % 23 and a not in vus:
        reps.append(a); vus |= {(a * h) % 115 for h in H}
controle("22 classes de (Z/115)^* modulo <22>", len(reps) == 22)

def horner(p, x, mod):
    r = 0
    for c in reversed(p): r = (r * x + c) % mod
    return r
def horner_fr(p, x, mod):
    r = 0
    for c in reversed(p): r = (r * x + c.numerator * pow(c.denominator, -1, mod)) % mod
    return r
def dpoly(p): return [i * c for i, c in enumerate(p)][1:]
dP22 = dpoly(P22)

# ------------------------------------------------------------ polynome caracteristique (multiplication dans K)
def matmul_elt(el):
    cols = []; v = el[:] + [Fr(0)] * (N - len(el))
    for _ in range(N):
        cols.append(v[:])
        top = v[N - 1]
        v = [Fr(0)] + v[:N - 1]
        if top:
            for i in range(N): v[i] -= top * P22[i]
    return [[cols[j][i] for j in range(N)] for i in range(N)]
def polcar(A):
    n = len(A); Mk = [[Fr(0)] * n for _ in range(n)]; c = [Fr(1)]
    for k in range(1, n + 1):
        for i in range(n): Mk[i][i] += c[-1]
        Mk = [[sum(A[i][l] * Mk[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        c.append(-sum(Mk[i][i] for i in range(n)) / k)
    return c
for a in range(2, 12):
    cp = polcar(matmul_elt(XI[a]))
    controle("xi_%d entier algebrique de norme +-1 (unite de K)" % a, all(x.denominator == 1 for x in cp) and abs(cp[N]) == 1)

# ------------------------------------------------------------ racines de P22 modulo p : images de theta par les 22 plongements
def racines_K(p, s, lien):
    """22 images de theta modulo les premiers au-dessus de p (theta_a = somme des zeta^(a h)), par l'arithmetique de F_p[y]/(g)
    (sortes a, A) ou de F_p (sortes b, c)."""
    if s in ("a", "A"):
        g0, g1 = [int(t) for t in lien.split(",")]
        def mulg(u, v):
            t0 = u[0] * v[0]; t1 = u[0] * v[1] + u[1] * v[0]; t2 = u[1] * v[1]
            return [(t0 - t2 * g0) % p, (t1 - t2 * g1) % p]
        def powg(k):
            r = [1, 0]; b = [0, 1]
            while k:
                if k & 1: r = mulg(r, b)
                b = mulg(b, b); k >>= 1
            return r
        res = {}
        for a in reps:
            t = [sum(powg(a * h)[i] for h in H) % p for i in range(2)]
            if t[1] != 0: return None
            res[a] = t[0]
        return res
    rP = int(lien)
    return {a: sum(pow(rP, a * h, p) for h in H) % p for a in reps}

def lien_ok(p, s, lien, r):
    if s in ("a", "A"):
        g0, g1 = [int(t) for t in lien.split(",")]
        # g | Phi_115 mod p : reste de la division de Phi par g
        rem = [x % p for x in PHI]
        for i in range(len(rem) - 1, 1, -1):
            c = rem[i]
            if c:
                rem[i] = 0; rem[i - 1] = (rem[i - 1] - c * g1) % p; rem[i - 2] = (rem[i - 2] - c * g0) % p
        div = rem[0] == 0 and rem[1] == 0
        disc = (g1 * g1 - 4 * g0) % p
        irr = disc != 0 and pow(disc, (p - 1) // 2, p) == p - 1
        rac = racines_K(p, s, lien)
        return div and irr and rac is not None and rac[1] == r % p, rac
    rP = int(lien)
    rac = racines_K(p, s, lien)
    return horner(PHI, rP, p) == 0 and rac[1] == r % p, rac

# ------------------------------------------------------------ premiers auxiliaires et logarithmes discrets
def est_premier(n):
    if n < 2: return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0: return n == q
    d = n - 1; s = 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
LL = [380651, 1065821, 1522601, 2055511]
controle("premiers auxiliaires premiers (divisions d'essai jusqu'a la racine), = 1 mod 331*115",
         all(l % (331 * 115) == 1 and all(l % d for d in range(2, int(l ** 0.5) + 1)) for l in LL))
DEN = lcm(*[c.denominator for el in list(XI.values()) + [G139] + [C["G"] for C in CIBLES] for c in el])
controle("denominateurs des pieces premiers aux premiers auxiliaires", all(DEN % l for l in LL))
PLACES = []   # (l, x = image de theta, om = racine 331-ieme de 1, table des logarithmes)
for l in LL:
    z = None
    for hh in range(2, 200):
        t = pow(hh, (l - 1) // 115, l)
        if pow(t, 5, l) != 1 and pow(t, 23, l) != 1: z = t; break
    rac = {a: sum(pow(z, a * h, l) for h in H) % l for a in reps}
    assert len(set(rac.values())) == 22 and all(horner(P22, x, l) == 0 and horner(dP22, x, l) for x in rac.values())
    om = next(pow(hh, (l - 1) // 331, l) for hh in range(2, 200) if pow(hh, (l - 1) // 331, l) != 1)
    table = {pow(om, e, l): e for e in range(331)}
    assert len(table) == 331
    for a in reps: PLACES.append((l, rac[a], table))
controle("88 premiers de degre 1 de K au-dessus des 4 premiers auxiliaires", len(PLACES) == 88)
def lam(el):
    v = []
    for (l, x, table) in PLACES:
        y = horner_fr(el, x, l)
        assert y != 0
        v.append(table[pow(y, (l - 1) // 331, l)])
    return v
def rang_mod(Mx, p):
    Mx = [r[:] for r in Mx]; rg = 0; nc = len(Mx[0])
    for c in range(nc):
        piv = next((i for i in range(rg, len(Mx)) if Mx[i][c] % p), None)
        if piv is None: continue
        Mx[rg], Mx[piv] = Mx[piv], Mx[rg]
        inv = pow(Mx[rg][c], -1, p); Mx[rg] = [x * inv % p for x in Mx[rg]]
        for i in range(len(Mx)):
            if i != rg and Mx[i][c] % p:
                f = Mx[i][c]; Mx[i] = [(x - f * y) % p for x, y in zip(Mx[i], Mx[rg])]
        rg += 1
    return rg
def resout_mod(A, b, p):
    """Resout A x = b mod p (A : 88 x 11 de rang 11) ; renvoie x ou None si incompatible."""
    n = len(A[0]); Mx = [A[i][:] + [b[i]] for i in range(len(A))]; rg = 0; pivs = []
    for c in range(n):
        piv = next((i for i in range(rg, len(Mx)) if Mx[i][c] % p), None)
        if piv is None: return None
        Mx[rg], Mx[piv] = Mx[piv], Mx[rg]
        inv = pow(Mx[rg][c], -1, p); Mx[rg] = [x * inv % p for x in Mx[rg]]
        for i in range(len(Mx)):
            if i != rg and Mx[i][c] % p:
                f = Mx[i][c]; Mx[i] = [(x - f * y) % p for x, y in zip(Mx[i], Mx[rg])]
        pivs.append(c); rg += 1
    if any(Mx[i][n] % p for i in range(rg, len(Mx))): return None
    return [Mx[i][n] for i in range(n)]
LU = [lam(XI[a]) for a in range(2, 12)]
U = [[LU[j][i] for j in range(10)] for i in range(88)]
controle("unites : rang 10 modulo 331 (indice de <-1, xi_a> dans E premier a 331, etape 1 de la note)", rang_mod(U, 331) == 10)
L139 = lam(G139)
A = [U[i] + [L139[i]] for i in range(88)]
controle("[unites | Gamma_139] : rang 11 modulo 331", rang_mod(A, 331) == 11)

# ------------------------------------------------------------ Gamma_139 et chaque ideal
def valuations(G, p, rac):
    K_ = 340; modK = p ** K_
    def hensel(x):
        k = 1
        while k < K_:
            k = min(2 * k, K_); mk = p ** k
            x = (x - horner(P22, x, mk) * pow(horner(dP22, x, mk), -1, mk)) % mk
        assert horner(P22, x, modK) == 0
        return x
    def valp(x):
        if x == 0: return K_
        v = 0
        while x % p == 0: x //= p; v += 1
        return v
    return {a: valp(horner_fr(G, hensel(x), modK)) for a, x in rac.items()}
def gamma_ok(G, p, r, rac):
    cg = polcar(matmul_elt(G))
    if not (all(x.denominator == 1 for x in cg) and abs(cg[N]) == p ** 331): return False
    vals = valuations(G, p, rac)
    return sum(vals.values()) == 331 and vals[1] == 331 and rac[1] == r % p
rac139 = racines_K(139, "A", "77,1")
controle("Gamma_139 : entier algebrique, |N| = 139^331, (Gamma_139) = q_139^331, q_139 = (139, theta - %d)" % R139,
         len(set(rac139.values())) == 22 and gamma_ok(G139, 139, R139, rac139))
mu22 = {pow(3, 15 * i, 331) for i in range(22)}
assert len(mu22) == 22
def heure(c):
    for h in range(15):
        if c * pow(2, -h, 331) % 331 in mu22: return h
    return -1
def repr23(n): return any((n - 23 * b * b) >= 0 and int((n - 23 * b * b) ** 0.5 + 0.5) ** 2 == n - 23 * b * b for b in range(int((n / 23) ** 0.5) + 1))
BIL = []
for C in CIBLES:
    p, s, r, e = C["p"], C["s"], C["r"], C["e"]
    lk, rac = lien_ok(p, s, C["lien"], r)
    controle("%s : lien avec l'ideal de L (sorte %s, lien %s) et theta mod P = %d ; 22 racines simples de P22 mod p" % (C["nom"], s, C["lien"], r),
             lk and len(set(rac.values())) == 22 and all(horner(P22, x, p) == 0 and horner(dP22, x, p) % p for x in rac.values()))
    controle("%s : (Gamma) = q^331 (entier, |N| = p^331, valuations 331 et 0)" % C["nom"], gamma_ok(C["G"], p, r, rac))
    x = resout_mod(A, lam(C["G"]), 331)
    controle("%s : systeme mod 331 compatible" % C["nom"], x is not None)
    c = x[10] * e * pow(2, -1, 331) % 331
    h = heure(c); t3 = not repr23(4 * p)
    controle("%s : c = %d (PARI : %d), heure %d, support %s" % (C["nom"], c, C["c"], h, "{3,331}" if t3 else "{331}"), c == C["c"] and c != 0 and h >= 0)
    BIL.append((C["nom"], p, c, h, t3))
print()
for (nom, p, c, h, t3) in BIL:
    print("  %-12s p = %-10d c = %3d  heure %2d  support %s" % (nom, p, c, h, "{3,331}" if t3 else "{331}"))
natt = 2 + 1 + 3 + 10 + 2 + 1 + 2 + 1 + 4 * len(CIBLES)
print("BILAN : %d controles (attendus %d), %d echecs" % (len(OK), natt, sum(1 for _, b in OK if not b)))
ok = all(b for _, b in OK) and len(OK) == natt
print("CADRAN_VERIFIE_SANS_PARI" if ok else "CADRAN_ECHEC")
sys.exit(0 if ok else 1)
