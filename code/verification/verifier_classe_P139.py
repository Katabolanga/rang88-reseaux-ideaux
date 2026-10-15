# -*- coding: utf-8 -*-
"""verifier_classe_P139.py -- verification EXACTE, sans PARI/GP et sans GRH, du certificat de classe de P139
(note, prop. 6.6 : P139^3 n'est pas principal dans L = Q(zeta_115) ; preuve au par. 6.4).

Enonce verifie :
  K = Q(theta), theta = zeta + zeta^22 + zeta^24 + zeta^68, P22 = polynome minimal de theta (degre 22) ;
  q = (139, theta - r) premier de degre 1 de K sous un premier P de L au-dessus de 139, f(P/q) = 2 ;
  (C1) P22(theta) = 0 dans Z[zeta_115] ; P22 mod 139 et mod chaque l utilise est sans facteur carre ;
  (C2) GAMMA et les XI_a sont des entiers algebriques (polynome caracteristique entier) ;
       N(XI_a) = +-1 ; N(GAMMA) = +-139^331 ; v_q(GAMMA) = 331 et v_q'(GAMMA) = 0 pour les 21 autres premiers au-dessus de 139 ;
       donc (GAMMA) = q^331 ;
  (C3) pour des premiers l = 1 mod 331 totalement decomposes dans K, la matrice des logarithmes discrets modulo 331
       (lignes : les 22 premiers de K au-dessus de l ; colonnes : XI_2..XI_11, GAMMA) est de rang 11 sur F_331,
       et ses 10 premieres colonnes sont de rang 10.
Consequence (note, preuve des prop. 6.6 et 6.7) : q^6 n'est pas principal, donc P^3 non plus.
Aucune donnee de PARI/GP n'est crue : le fichier data/P139/certificat_K22.txt n'apporte que des CANDIDATS.
Lien avec le reseau du calcul : le premier P est relu dans data/P139/entrees/I_data.gp (BASE).
Usage (depuis la racine du depot) : python -I code/verification/verifier_classe_P139.py   (environ 10 s)"""
import re, sys, os, hashlib
from fractions import Fraction as Fr

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CERT = os.path.join(RACINE, "data", "P139", "certificat_K22.txt")
IDATA = os.path.join(RACINE, "data", "P139", "entrees", "I_data.gp")
OK = []
def controle(nom, cond):
    OK.append((nom, bool(cond)))
    print(("OK    " if cond else "ECHEC ") + nom); sys.stdout.flush()
    if not cond: raise SystemExit("ECHEC : " + nom)

def lire_poly(s, var):
    """polynôme à coefficients rationnels, syntaxe GP ; rend la liste des coefficients (degré croissant)"""
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

cert = {}
for l in open(CERT, encoding="ascii"):
    k, _, v = l.strip().partition(" = ")
    cert[k] = v
print("certificat : data/P139/certificat_K22.txt SHA-256", hashlib.sha256(open(CERT, "rb").read()).hexdigest())
P22 = lire_poly(cert["P22"], "w"); assert all(c.denominator == 1 for c in P22)
P22 = [int(c) for c in P22]
controle("P22 unitaire de degre 22", len(P22) == 23 and P22[22] == 1)
GAM = lire_poly(cert["GAMMA"], "w")
XI = {a: lire_poly(cert["XI_%d" % a], "w") for a in range(2, 12)}
RAC = int(cert["RACINE"])
N = 22

# ---------------------------------------------------------------- (C1) P22(theta) = 0 dans Z[y]/Phi_115
M = 115
def mulc(a, b):   # produit dans Z[y]/(y^115 - 1)
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
def poldivex(a, b):   # division exacte de polynômes entiers, b unitaire
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        q[i] = a[i + len(b) - 1]
        for j, y in enumerate(b): a[i + j] -= q[i] * y
    assert not any(a); return q
def cyclo_prod(n): return [-1] + [0] * (n - 1) + [1]   # y^n - 1
PHI = poldivex(polmul(cyclo_prod(115), cyclo_prod(1)), polmul(cyclo_prod(5), cyclo_prod(23)))
controle("Phi_115 de degre 88, unitaire", len(PHI) == 89 and PHI[88] == 1)
def redphi(a):   # reste modulo Phi_115 d'un élément de Z[y]/(y^115-1)
    a = a[:]
    for i in range(len(a) - 1, 87, -1):
        c = a[i]
        if c:
            for j, y in enumerate(PHI): a[i - 88 + j] -= c * y
    return a[:88]
th = [0] * M
for k in (1, 22, 24, 68): th[k] = 1
acc = [0] * M; pw = [1] + [0] * (M - 1)
for c in P22:
    acc = [x + c * y for x, y in zip(acc, pw)]; pw = mulc(pw, th)
controle("(C1) P22(theta) = 0 dans Z[zeta_115], theta = zeta + zeta^22 + zeta^24 + zeta^68", not any(redphi(acc)))
H = {1, 22, 24, 68}
controle("(C1) {1,22,24,68} est un sous-groupe de (Z/115)^*, stabilisateur de theta (base normale : 115 sans facteur carre)",
         all((a * b) % 115 in H for a in H for b in H))
# => theta a exactement 88/4 = 22 conjugués : P22 est irréductible et K = Q(theta) = Fix<sigma_22>.

# ---------------------------------------------------------------- arithmétique modulo p
def horner(p, x, mod):
    r = 0
    for c in reversed(p): r = (r * x + c) % mod
    return r
def horner_fr(p, x, mod):   # coefficients rationnels, dénominateurs inversibles modulo mod
    r = 0
    for c in reversed(p): r = (r * x + c.numerator * pow(c.denominator, -1, mod)) % mod
    return r
def dpoly(p): return [i * c for i, c in enumerate(p)][1:]
dP22 = dpoly(P22)
def racines_brutes(p):   # p petit : recherche exhaustive
    return [x for x in range(p) if horner(P22, x, p) == 0]

# ---------------------------------------------------------------- lien avec le premier P du calcul (I_data.gp)
txt = open(IDATA, encoding="ascii").read()
mB = re.search(r"BASE = \[(.*?)\];", txt, re.S)
lignes = [[int(t) for t in row.split(",")] for row in mB.group(1).split(";")]
controle("BASE de I_data.gp : 88 x 88", len(lignes) == 88 and all(len(r) == 88 for r in lignes))
p = 139
def pgcd_mod(a, b, p):
    def norm(a):
        while a and a[-1] % p == 0: a.pop()
        return a
    a = norm([x % p for x in a]); b = norm([x % p for x in b])
    while b:
        inv = pow(b[-1], -1, p)
        while len(a) >= len(b):
            c = a[-1] * inv % p; s = len(a) - len(b)
            for j, y in enumerate(b): a[s + j] = (a[s + j] - c * y) % p
            a = norm(a)
            if not a: break
        a, b = b, a
    inv = pow(a[-1], -1, p)
    return [x * inv % p for x in a]
g = [x % p for x in PHI]
for j in range(88):
    col = [lignes[i][j] for i in range(88)]
    if any(x % p for x in col): g = pgcd_mod(g, col, p)
controle("I mod 139 est engendre par un facteur g de degre 2 de Phi_115 mod 139 (P de degre residuel 2)", len(g) == 3)
# theta modulo (139, g) : calcul dans F_139[y]/g
def mulg(a, b):
    r = [0, 0, 0]
    for i in range(2):
        for j in range(2): r[i + j] += a[i] * b[j]
    c = r[2] % p
    return [(r[0] - c * g[0]) % p, (r[1] - c * g[1]) % p]
def powg(k):
    r = [1, 0]; b = [0, 1]
    while k:
        if k & 1: r = mulg(r, b)
        b = mulg(b, b); k >>= 1
    return r
tg = [sum(powg(k)[i] for k in (1, 22, 24, 68)) % p for i in range(2)]
controle("theta mod P est dans F_139 (q = P inter K de degre 1, f(P/q) = 2)", tg[1] == 0)
print("      theta = %d mod P ; RACINE du certificat = %d" % (tg[0], RAC))
controle("la racine du certificat est celle du premier P de I_data.gp", tg[0] == RAC % p)
r139 = racines_brutes(139)
controle("(C1) P22 a 22 racines simples modulo 139 (139 totalement decompose dans K, Z[theta] maximal en 139)",
         len(r139) == 22 and all(horner(dP22, x, 139) for x in r139) and RAC % 139 in r139)

# ---------------------------------------------------------------- (C2) polynômes caractéristiques (Faddeev–LeVerrier exact)
def matmul_elt(el):   # matrice de la multiplication par el dans la base 1, w, ..., w^21 de Q[w]/P22
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
    return c   # c[k] = coefficient de t^(n-k)
for a in range(2, 12):
    c = polcar(matmul_elt(XI[a]))
    controle("(C2) XI_%d entier algebrique de norme +-1 (unite de K)" % a, all(x.denominator == 1 for x in c) and abs(c[N]) == 1)
cg = polcar(matmul_elt(GAM))
controle("(C2) GAMMA entier algebrique", all(x.denominator == 1 for x in cg))
controle("(C2) |N(GAMMA)| = 139^331", abs(cg[N]) == 139 ** 331)
# valuations aux 22 premiers au-dessus de 139 : relèvement de Hensel des racines modulo 139^340
K_ = 340; modK = 139 ** K_
def hensel(x):
    k = 1
    while k < K_:
        k = min(2 * k, K_); mk = 139 ** k
        x = (x - horner(P22, x, mk) * pow(horner(dP22, x, mk), -1, mk)) % mk
    assert horner(P22, x, modK) == 0
    return x
def val139(x):
    if x == 0: return K_
    v = 0
    while x % 139 == 0: x //= 139; v += 1
    return v
vals = {x: val139(horner_fr(GAM, hensel(x), modK)) for x in r139}
print("      valuations de GAMMA aux 22 premiers au-dessus de 139 :", sorted(vals.items()))
controle("(C2) v_q(GAMMA) = 331 en q = (139, theta - RACINE) et 0 aux 21 autres : (GAMMA) = q^331",
         vals[RAC % 139] == 331 and sum(vals.values()) == 331)

# ---------------------------------------------------------------- (C3) logarithmes discrets modulo 331
def est_premier(n):
    if n < 2: return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0: return n == q
    d = n - 1; s = 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):   # déterministe pour n < 3,3e24
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
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
lignes_dl = []; premiers_l = []
l = 1
while len(premiers_l) < 3:
    l += 331 * 115
    if not est_premier(l) or l in (139, 28657): continue
    # z d'ordre exactement 115 dans F_l^*
    z = None
    for h in range(2, 200):
        t = pow(h, (l - 1) // 115, l)
        if pow(t, 5, l) != 1 and pow(t, 23, l) != 1: z = t; break
    assert z is not None and pow(z, 115, l) == 1
    reps = []; vus = set()
    for a in range(1, 115):
        if a % 5 and a % 23 and a not in vus:
            reps.append(a); vus |= {(a * h) % 115 for h in H}
    rac = [sum(pow(z, a * h, l) for h in H) % l for a in reps]
    if not (len(set(rac)) == 22 and all(horner(P22, x, l) == 0 for x in rac) and all(horner(dP22, x, l) for x in rac)):
        continue
    # générateur omega de mu_331 dans F_l^* et table
    om = None
    for h in range(2, 200):
        t = pow(h, (l - 1) // 331, l)
        if t != 1: om = t; break
    table = {pow(om, e, l): e for e in range(331)}
    assert len(table) == 331
    bloc = []
    for x in rac:
        ligne = []
        for el in [XI[a] for a in range(2, 12)] + [GAM]:
            v = horner_fr(el, x, l)
            assert v != 0
            ligne.append(table[pow(v, (l - 1) // 331, l)])
        bloc.append(ligne)
    premiers_l.append(l); lignes_dl += bloc
    print("      l = %d : 22 racines simples de P22, rang des 10 colonnes d'unites = %d, rang total = %d"
          % (l, rang_mod([r[:10] for r in bloc], 331), rang_mod(bloc, 331)))
ru = rang_mod([r[:10] for r in lignes_dl], 331); rt = rang_mod(lignes_dl, 331)
print("      premiers l utilises :", premiers_l, "; matrice %d x 11 ; rang(unites) = %d ; rang(unites, GAMMA) = %d" % (len(lignes_dl), ru, rt))
controle("(C3) les 10 unites XI_a sont independantes modulo les puissances 331-iemes (rang 10)", ru == 10)
controle("(C3) GAMMA n'est pas dans <unites> . K^{*331} (rang 11)", rt == 11)
print("BILAN : %d controles, %d echecs" % (len(OK), sum(1 for _, b in OK if not b)))
print("CONCLUSION (preuve : note, par. 6.4, prop. 6.6) : q^6 n'est pas principal dans K22, donc P139^3 n'est pas principal dans Q(zeta_115). SANS GRH.")
