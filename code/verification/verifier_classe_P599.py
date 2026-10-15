# -*- coding: utf-8 -*-
"""verifier_classe_P599.py -- verification EXACTE, sans PARI/GP et sans GRH, du certificat
<< l'ordre de la classe de P599 dans Cl(Q(zeta_115)) est divisible par 331 >> (donc [P599]^3 != 1), et du fait
<< la norme de P599 dans Q(sqrt(-23)) est principale >> (composante 3 nulle) (note, prop. 6.7 ; preuve au par. 6.4).

Enonces verifies :
  K = Q(theta), theta = zeta + zeta^22 + zeta^24 + zeta^68, P22 = polynome minimal de theta (degre 22) ;
  P = le premier de L relu dans data/P599/entrees/I_data.gp (BASE) ; q = P inter K ;
  (I1) P22(theta) = 0 dans Z[zeta_115] ; H = {1,22,24,68} sous-groupe d'ordre 4 ; 22 classes aH distinctes ;
       -1 hors de H ; pgcd(21, 115) = 1 (seules racines de l'unite de K : +-1) ;
  (I2) |det BASE| = 599^2 ; toutes les colonnes de BASE sont dans (599, g(zeta)), g irreductible de degre 2 divisant
       Phi_115 mod 599 : BASE Z^88 = P = (599, g(zeta)) ; theta mod P = RACINE dans F_599 ; P22 a 22 racines simples
       mod 599 : q = (599, theta - RACINE), f(P/q) = 2, N_{L/K}(P) = q^2 ;
  (I3) GAMMA et les XI_a sont des entiers algebriques (polynome caracteristique unitaire entier) ; N(XI_a) = +-1 ;
       |N(GAMMA)| = 599^(331 T) ; v_q(GAMMA) = 331 T et 0 aux 21 autres premiers au-dessus de 599 : (GAMMA) = q^(331 T) ;
  (I4) pour trois premiers l = 1 mod 331*115 (primalite par divisions exhaustives), P22 a 22 racines simples mod l ;
       la matrice 66 x 11 des logarithmes discrets modulo 331 (colonnes : XI_2..XI_11, GAMMA) est de rang 11 sur F_331,
       ses 10 premieres colonnes de rang 10 ;
  (F)  sqrt(-23) = somme de Gauss dans Z[zeta] ; 599 = N(24 +- sqrt(-23)) ; l'un des deux elements 24 +- sqrt(-23) est
       dans P : P inter Q(sqrt(-23)) est principal ; par contraste, 4*139 n'est pas de la forme a^2 + 23 b^2.
Aucune donnee de PARI/GP n'est crue : le fichier data/P599/certificat_K22.txt n'apporte que des CANDIDATS.
Usage (depuis la racine du depot) : python -I code/verification/verifier_classe_P599.py   (environ 10 s)"""
import re, sys, os, hashlib
from fractions import Fraction as Fr

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CERT = os.path.join(RACINE, "data", "P599", "certificat_K22.txt")
IDATA = os.path.join(RACINE, "data", "P599", "entrees", "I_data.gp")
PP = 599
OK = []
def controle(nom, cond):
    OK.append((nom, bool(cond)))
    print(("OK    " if cond else "ECHEC ") + nom); sys.stdout.flush()
    if not cond: raise SystemExit("ECHEC : " + nom)
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()

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
def premier_exhaustif(n):
    """primalite par divisions exhaustives (pas de test probabiliste)"""
    if n < 2: return False
    d = 2
    while d * d <= n:
        if n % d == 0: return False
        d += 1
    return True

cert = {}
for l in open(CERT, encoding="ascii"):
    k, _, v = l.strip().partition(" = ")
    cert[k] = v
print("certificat : data/P599/certificat_K22.txt SHA-256", sha(CERT))
print("ideal      : data/P599/entrees/I_data.gp SHA-256", sha(IDATA))
P22 = lire_poly(cert["P22"], "w"); assert all(c.denominator == 1 for c in P22)
P22 = [int(c) for c in P22]
controle("P22 unitaire de degre 22", len(P22) == 23 and P22[22] == 1)
GAM = lire_poly(cert["GAMMA"], "w")
XI = {a: lire_poly(cert["XI_%d" % a], "w") for a in range(2, 12)}
RAC = int(cert["RACINE"]); TT = int(cert["T"])
controle("T du certificat dans {1, 2} ; 599 et 331 premiers (divisions exhaustives)", TT in (1, 2) and premier_exhaustif(PP) and premier_exhaustif(331))
N = 22
dens = sorted({c.denominator for el in [GAM] + list(XI.values()) for c in el})
print("      denominateurs des coordonnees du certificat (base 1, w, ..., w^21) :", dens)

# ---------------------------------------------------------------- (I1) P22(theta) = 0 dans Z[y]/Phi_115 ; le corps K
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
controle("(I1) P22(theta) = 0 dans Z[zeta_115], theta = zeta + zeta^22 + zeta^24 + zeta^68", not any(redphi(acc)))
H = {1, 22, 24, 68}
controle("(I1) H = {1,22,24,68} = <22> est un sous-groupe d'ordre 4 de (Z/115)^*",
         all((a * b) % 115 in H for a in H for b in H) and {pow(22, k, 115) for k in range(4)} == H)
unites115 = [a for a in range(1, 115) if a % 5 and a % 23]
classes = {frozenset((a * h) % 115 for h in H) for a in unites115}
controle("(I1) 88 unites mod 115, 22 classes aH distinctes : theta a 22 conjugues (les 88 puissances primitives sont independantes), P22 irreductible, K = L^H",
         len(unites115) == 88 and len(classes) == 22 and all(len(c) == 4 for c in classes))
from math import gcd
controle("(I1) -1 hors de H (K est CM, unites de rang 10) ; pgcd(21, 115) = 1 (racines de l'unite de K : +-1)", 114 not in H and gcd(21, 115) == 1)

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

# ---------------------------------------------------------------- (I2) le premier P du calcul (I_data.gp)
txt = open(IDATA, encoding="ascii").read()
controle("I_data.gp : PREMIERS = [[599, 2, 1]] ; Q = 599^2", "PREMIERS = [[599, 2, 1]];" in txt and re.search(r"^Q = (\d+);", txt, re.M).group(1) == str(PP * PP))
mB = re.search(r"BASE = \[(.*?)\];", txt, re.S)
lignes = [[int(t) for t in row.split(",")] for row in mB.group(1).split(";")]
controle("BASE de I_data.gp : 88 x 88", len(lignes) == 88 and all(len(r) == 88 for r in lignes))
def det_bareiss(A):
    A = [r[:] for r in A]; n = len(A); prev = 1; s = 1
    for k in range(n - 1):
        if A[k][k] == 0:
            l = next((i for i in range(k + 1, n) if A[i][k]), None)
            if l is None: return 0
            A[k], A[l] = A[l], A[k]; s = -s
        for i in range(k + 1, n):
            for j in range(k + 1, n): A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return s * A[n - 1][n - 1]
controle("(I2) |det BASE| = 599^2 : BASE Z^88 est d'indice 599^2 dans Z[zeta]", abs(det_bareiss(lignes)) == PP ** 2)
p = PP
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
controle("(I2) le pgcd de Phi_115 et des 88 colonnes de BASE modulo 599 est un polynome g unitaire de degre 2", len(g) == 3 and g[2] == 1)
print("      g = y^2 + %d y + %d (mod 599)" % (g[1], g[0]))
def reste_g(col):   # reste modulo (599, g) d'un polynôme entier
    a = [x % p for x in col]
    for i in range(len(a) - 1, 1, -1):
        c = a[i]
        if c: a[i] = 0; a[i - 1] = (a[i - 1] - c * g[1]) % p; a[i - 2] = (a[i - 2] - c * g[0]) % p
    return a[:2]
controle("(I2) g divise Phi_115 mod 599 ; les 88 colonnes de BASE sont nulles modulo (599, g) : BASE Z^88 contenu dans (599, g(zeta))",
         reste_g(PHI) == [0, 0] and all(reste_g([lignes[i][j] for i in range(88)]) == [0, 0] for j in range(88)))
disc = (g[1] * g[1] - 4 * g[0]) % p
controle("(I2) g irreductible mod 599 (discriminant non residu) : (599, g(zeta)) est premier d'indice 599^2 ; donc BASE Z^88 = P = (599, g(zeta)), f(P) = 2",
         pow(disc, (p - 1) // 2, p) == p - 1 and p % 115 == 24 and pow(24, 2, 115) == 1)
# theta modulo (599, g) : calcul dans F_599[y]/g
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
controle("(I2) theta mod P est dans F_599 (q = P inter K de degre 1, f(P/q) = 2)", tg[1] == 0)
print("      theta = %d mod P ; RACINE du certificat = %d" % (tg[0], RAC))
controle("(I2) la racine du certificat est celle du premier P de I_data.gp", tg[0] == RAC % p)
rp = [x for x in range(p) if horner(P22, x, p) == 0]
controle("(I2) P22 a 22 racines simples modulo 599 (599 totalement decompose dans K, Z[theta] maximal en 599) ; q = (599, theta - RACINE), N_{L/K}(P) = q^2",
         len(rp) == 22 and all(horner(dP22, x, p) for x in rp) and RAC % p in rp)

# ---------------------------------------------------------------- (F) composante 3 : la norme de P dans Q(sqrt(-23)) est principale
def legendre23(a): return 1 if pow(a, 11, 23) == 1 else -1
gs = [0] * M
for a in range(1, 23): gs[(5 * a) % M] += legendre23(a)
g2 = mulc(gs, gs); g2[0] += 23
controle("(F) s = somme_{a=1..22} (a/23) zeta^(5a) verifie s^2 = -23 dans Z[zeta_115] : s = sqrt(-23)", not any(redphi(g2)))
sg = [0, 0]
for k, c in enumerate(gs):
    if c:
        w = powg(k); sg = [(sg[0] + c * w[0]) % p, (sg[1] + c * w[1]) % p]
controle("(F) s mod P est dans F_599 et (s mod P)^2 = -23", sg[1] == 0 and (sg[0] * sg[0] + 23) % p == 0)
signe = +1 if (24 + sg[0]) % p == 0 else (-1 if (24 - sg[0]) % p == 0 else 0)
controle("(F) 24^2 + 23 = 599 ; pi = 24 %s sqrt(-23) est dans P (pi = 0 modulo (599, g)) : P inter Q(sqrt(-23)) = (pi) est principal, N_{L/F}(P) = (pi^2)"
         % ("+" if signe > 0 else "-"), 24 * 24 + 23 == PP and signe != 0)
def formes(n4):   # solutions de a^2 + 23 b^2 = n4, a, b >= 0
    out = []
    b = 0
    while 23 * b * b <= n4:
        r = n4 - 23 * b * b; a = int(r ** 0.5)
        while a * a > r: a -= 1
        while (a + 1) * (a + 1) <= r: a += 1
        if a * a == r: out.append((a, b))
        b += 1
    return out
controle("(F) contraste avec P139 : 4*139 n'est pas de la forme a^2 + 23 b^2 (premiers au-dessus de 139 non principaux dans Q(sqrt(-23))), alors que 4*599 = 48^2 + 23*2^2",
         formes(4 * 139) == [] and (48, 2) in formes(4 * 599))

# ---------------------------------------------------------------- (I3) polynômes caractéristiques (Faddeev–LeVerrier exact)
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
    controle("(I3) XI_%d entier algebrique de norme +-1 (unite de K)" % a, all(x.denominator == 1 for x in c) and abs(c[N]) == 1)
cg = polcar(matmul_elt(GAM))
controle("(I3) GAMMA entier algebrique (polynome caracteristique unitaire entier)", all(x.denominator == 1 for x in cg))
controle("(I3) |N(GAMMA)| = 599^%d" % (331 * TT), abs(cg[N]) == PP ** (331 * TT))
# valuations aux 22 premiers au-dessus de 599 : relèvement de Hensel des racines modulo 599^K_
K_ = 331 * TT + 9; modK = PP ** K_
controle("(I3) les denominateurs du certificat sont premiers a 599 (evaluation 599-adique legitime)", all(dd % PP for dd in dens))
def hensel(x):
    k = 1
    while k < K_:
        k = min(2 * k, K_); mk = PP ** k
        x = (x - horner(P22, x, mk) * pow(horner(dP22, x, mk), -1, mk)) % mk
    assert horner(P22, x, modK) == 0
    return x
def valp(x):
    if x == 0: return K_
    v = 0
    while x % PP == 0: x //= PP; v += 1
    return v
vals = {x: valp(horner_fr(GAM, hensel(x), modK)) for x in rp}
print("      valuations de GAMMA aux 22 premiers au-dessus de 599 :", sorted(vals.items()))
controle("(I3) v_q(GAMMA) = %d en q = (599, theta - %d) et 0 aux 21 autres (precision 599^%d) : (GAMMA) = q^%d" % (331 * TT, RAC, K_, 331 * TT),
         vals[RAC % p] == 331 * TT and sum(vals.values()) == 331 * TT and sorted(vals.values())[:21] == [0] * 21)

# ---------------------------------------------------------------- (I4) logarithmes discrets modulo 331
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
    if not premier_exhaustif(l) or l == PP or any(dd % l == 0 for dd in dens): continue
    # z d'ordre exactement 115 dans F_l^*
    z = None
    for h in range(2, 200):
        t = pow(h, (l - 1) // 115, l)
        if pow(t, 5, l) != 1 and pow(t, 23, l) != 1: z = t; break
    assert z is not None and pow(z, 115, l) == 1
    reps = []; vus = set()
    for a in unites115:
        if a not in vus:
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
    print("      l = %d (premier, = 1 mod 331*115) : 22 racines simples de P22, images non nulles ; rang des 10 colonnes d'unites = %d, rang total = %d"
          % (l, rang_mod([r[:10] for r in bloc], 331), rang_mod(bloc, 331)))
ru = rang_mod([r[:10] for r in lignes_dl], 331); rt = rang_mod(lignes_dl, 331)
print("      premiers l utilises :", premiers_l, "; matrice %d x 11 ; rang(unites) = %d ; rang(unites, GAMMA) = %d" % (len(lignes_dl), ru, rt))
controle("(I4) trois premiers l, 66 lignes de degre 1, l different de 599 et premier aux denominateurs", len(premiers_l) == 3 and len(lignes_dl) == 66)
controle("(I4) les 10 unites XI_a sont independantes modulo les puissances 331-iemes (rang 10)", ru == 10)
controle("(I4) GAMMA n'est pas dans <unites> . K^{*331} (rang 11)", rt == 11)
print("BILAN : %d controles, %d echecs" % (len(OK), sum(1 for _, b in OK if not b)))
print("CONCLUSION (preuve : note, par. 6.4, prop. 6.7) : pour tout m premier a 331, q^(2m) n'est pas principal dans K22, donc P599^m n'est pas")
print("principal dans Q(zeta_115) : l'ordre de [P599] est divisible par 331 ; en particulier P599 et P599^3 ne sont pas principaux. SANS GRH.")
print("FIN_OK")
