# -*- coding: utf-8 -*-
"""verifier_non_isometrie_P4969.py -- verification EXACTE, sans PARI/GP et SANS GRH, de la non-isometrie du reseau
X_4969 = (P4969, beta_0/nu) aux quatre reseaux extremaux deja connus sur L = Q(zeta_115) : L0, LS (Sakamoto), X_139, X_599.
Adapte de verifier_classe_P139.py (depot public, 11 octobre 2026) ; Claude, 16 octobre 2026.

Notations (note, par. 6.4) : K = K22 = Q(theta), theta = zeta + zeta^22 + zeta^24 + zeta^68, degre 22 ; pour p = 139, 4969,
P_p est l'ideal des fichiers d'entree (data/Pp/entrees/I_data.gp), q_p = P_p inter K est de degre 1 et N_{L/K}(P_p) = q_p^2.
Pieces (CANDIDATS trouves par PARI sous GRH, rien n'est cru) : data/P139/certificat_K22.txt (P22, RACINE, GAMMA, XI_2..XI_11)
et data/P4969/certificat_K22.txt (P22, RACINE, GAMMA).

Controles :
  (C1) P22(theta) = 0 dans Z[zeta_115] ; {1,22,24,68} sous-groupe ; pour p = 139, 4969 : I mod p = (g_p), deg g_p = 2,
       theta mod P_p dans F_p egal a RACINE_p, P22 a 22 racines simples mod p ;
  (C2) XI_a unites ; GAMMA_p entier algebrique, |N(GAMMA_p)| = p^331, v = 331 en q_p et 0 aux 21 autres premiers sur p ;
  (C3) logarithmes discrets modulo 331 aux 22 premiers de K au-dessus de premiers l = 1 mod 331*115 :
       colonnes des 10 unites de rang 10 ; [unites | GAMMA_4969] de rang 11 ;
  (C4) pour CHACUN des 22 elements tau_b de Gal(K/Q) : [unites | c_b] de rang 11, ou
       c_b(l, a) = lambda_{(l,a)}(GAMMA_4969) - lambda_{(l, a*b)}(GAMMA_139) (lambda_l(tau_b x) = lambda_{tau_b^-1 l}(x)) ;
  (C5) 4969 = 1 mod 23 (decompose dans F = Q(sqrt(-23))) et 4*4969 n'est pas de la forme a^2 + 23 b^2.
Consequences (preuves : note, par. 6.4, et le message a Astra du 16 octobre) :
  (C3) => q_4969^(2m) non principal pour m premier a 331 => [P4969]^3 != 1, alors que les classes de L0 et LS sont de cube 1 ;
  (C4) => pour tout tau, q_4969^2 tau(q_139)^-2 n'est pas principal => [P4969] n'est conjugue a [P139] par aucun sigma ;
  (C5) => N_{L/F}(P4969) n'est pas principal, alors que N_{L/F}(P599) l'est (599 = 24^2 + 23) => [P4969] non conjugue a [P599].
Avec le theoreme d'isometrie (th. 3.3 ; minima 8 : Sakamoto pour L0, LS ; calcul assiste pour X139, X599 et X4969) :
X_4969 n'est isometrique ni a L0, ni a LS, ni a X_139, ni a X_599.
Usage (depuis la racine de verification_P4969/) : python3 -I code/verification/verifier_non_isometrie_P4969.py"""
import re, sys, os, hashlib
from fractions import Fraction as Fr
from math import lcm

RACINE_DOSSIER = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
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
def lire_cert(f):
    d = {}
    for l in open(f, encoding="ascii"):
        k, _, v = l.strip().partition(" = ")
        if k: d[k] = v
    print("certificat : %s SHA-256 %s" % (os.path.relpath(f, RACINE_DOSSIER).replace(os.sep, "/"), hashlib.sha256(open(f, "rb").read()).hexdigest()))
    return d

C139 = lire_cert(os.path.join(RACINE_DOSSIER, "data", "P139", "certificat_K22.txt"))
C4969 = lire_cert(os.path.join(RACINE_DOSSIER, "data", "P4969", "certificat_K22.txt"))
controle("meme polynome P22 dans les deux certificats", C139["P22"].replace(" ", "") == C4969["P22"].replace(" ", ""))
P22 = lire_poly(C139["P22"], "w"); assert all(c.denominator == 1 for c in P22)
P22 = [int(c) for c in P22]
controle("P22 unitaire de degre 22", len(P22) == 23 and P22[22] == 1)
XI = {a: lire_poly(C139["XI_%d" % a], "w") for a in range(2, 12)}
GAM = {139: lire_poly(C139["GAMMA"], "w"), 4969: lire_poly(C4969["GAMMA"], "w")}
RAC = {139: int(C139["RACINE"]), 4969: int(C4969["RACINE"])}
N = 22
DEN = lcm(*[c.denominator for el in list(XI.values()) + list(GAM.values()) for c in el])
print("      denominateur commun des pieces :", DEN)

# ---------------------------------------------------------------- (C1) P22(theta) = 0 dans Z[y]/Phi_115
M = 115
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
for k in (1, 22, 24, 68): th[k] = 1
acc = [0] * M; pw = [1] + [0] * (M - 1)
for c in P22:
    acc = [x + c * y for x, y in zip(acc, pw)]; pw = mulc(pw, th)
controle("(C1) P22(theta) = 0 dans Z[zeta_115], theta = zeta + zeta^22 + zeta^24 + zeta^68", not any(redphi(acc)))
H = {1, 22, 24, 68}
controle("(C1) {1,22,24,68} est un sous-groupe de (Z/115)^* (K = Fix<sigma_22>, de degre 22)", all((a * b) % 115 in H for a in H for b in H))

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

# ---------------------------------------------------------------- (C1) lien avec les premiers P_p des calculs
RACS = {}
for p in (139, 4969):
    txt = open(os.path.join(RACINE_DOSSIER, "data", "P%d" % p, "entrees", "I_data.gp"), encoding="ascii").read()
    mB = re.search(r"BASE = \[(.*?)\];", txt, re.S)
    lignes = [[int(t) for t in row.split(",")] for row in mB.group(1).split(";")]
    controle("P%d : BASE de I_data.gp 88 x 88" % p, len(lignes) == 88 and all(len(r) == 88 for r in lignes))
    g = [x % p for x in PHI]
    for j in range(88):
        col = [lignes[i][j] for i in range(88)]
        if any(x % p for x in col): g = pgcd_mod(g, col, p)
    controle("P%d : I mod %d = (g), g facteur de degre 2 de Phi_115 mod %d (P de degre residuel 2)" % (p, p, p), len(g) == 3)
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
    controle("P%d : theta mod P dans F_%d (q = P inter K de degre 1, f(P/q) = 2, N_{L/K}(P) = q^2)" % (p, p), tg[1] == 0)
    controle("P%d : RACINE du certificat (%d) = image de theta modulo P (%d)" % (p, RAC[p], tg[0]), tg[0] == RAC[p] % p)
    rp = [x for x in range(p) if horner(P22, x, p) == 0]
    controle("P%d : P22 a 22 racines simples modulo %d (%d totalement decompose dans K)" % (p, p, p),
             len(rp) == 22 and all(horner(dP22, x, p) for x in rp) and RAC[p] % p in rp)
    RACS[p] = rp

# ---------------------------------------------------------------- (C2) polynômes caractéristiques et valuations
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
    c = polcar(matmul_elt(XI[a]))
    controle("(C2) XI_%d entier algebrique de norme +-1 (unite de K)" % a, all(x.denominator == 1 for x in c) and abs(c[N]) == 1)
for p in (139, 4969):
    cg = polcar(matmul_elt(GAM[p]))
    controle("(C2) GAMMA_%d entier algebrique, |N(GAMMA_%d)| = %d^331" % (p, p, p), all(x.denominator == 1 for x in cg) and abs(cg[N]) == p ** 331)
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
    vals = {x: valp(horner_fr(GAM[p], hensel(x), modK)) for x in RACS[p]}
    controle("(C2) v(GAMMA_%d) = 331 en q_%d = (%d, theta - %d) et 0 aux 21 autres premiers : (GAMMA_%d) = q_%d^331" % (p, p, p, RAC[p], p, p),
             vals[RAC[p] % p] == 331 and sum(vals.values()) == 331)

# ---------------------------------------------------------------- (C3), (C4) logarithmes discrets modulo 331
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
reps = []; vus = set()
for a in range(1, 115):
    if a % 5 and a % 23 and a not in vus:
        reps.append(a); vus |= {(a * h) % 115 for h in H}
controle("22 classes de (Z/115)^* modulo <22> : les 22 elements tau_b de Gal(K/Q)", len(reps) == 22)
rep_de = {}
for a in reps:
    for h in H: rep_de[(a * h) % 115] = a
NB_L = int(os.environ.get("NB_L", "4"))
lignes_dl = {}   # (l, a) -> [lambda(XI_2..XI_11), lambda(GAMMA_139), lambda(GAMMA_4969)]
premiers_l = []
l = 1
while len(premiers_l) < NB_L:
    l += 331 * 115
    if not est_premier(l) or l in (139, 4969) or DEN % l == 0: continue
    z = None
    for h in range(2, 200):
        t = pow(h, (l - 1) // 115, l)
        if pow(t, 5, l) != 1 and pow(t, 23, l) != 1: z = t; break
    assert z is not None and pow(z, 115, l) == 1
    rac = {a: sum(pow(z, a * h, l) for h in H) % l for a in reps}
    if not (len(set(rac.values())) == 22 and all(horner(P22, x, l) == 0 for x in rac.values()) and all(horner(dP22, x, l) for x in rac.values())):
        continue
    om = None
    for h in range(2, 200):
        t = pow(h, (l - 1) // 331, l)
        if t != 1: om = t; break
    table = {pow(om, e, l): e for e in range(331)}
    assert len(table) == 331
    for a in reps:
        x = rac[a]; ligne = []
        for el in [XI[b] for b in range(2, 12)] + [GAM[139], GAM[4969]]:
            v = horner_fr(el, x, l)
            assert v != 0
            ligne.append(table[pow(v, (l - 1) // 331, l)])
        lignes_dl[(l, a)] = ligne
    premiers_l.append(l)
cles = sorted(lignes_dl)
U = [lignes_dl[k][:10] for k in cles]
ru = rang_mod(U, 331)
print("      premiers l utilises :", premiers_l, "; %d lignes (22 premiers de K au-dessus de chaque l)" % len(cles))
controle("(C3) les 10 unites XI_a sont independantes modulo les puissances 331-iemes (rang 10)", ru == 10)
r4969 = rang_mod([lignes_dl[k][:10] + [lignes_dl[k][11]] for k in cles], 331)
controle("(C3) GAMMA_4969 n'est pas dans <unites> . K^{*331} (rang 11) : [P4969]^3 != 1", r4969 == 11)
r139 = rang_mod([lignes_dl[k][:10] + [lignes_dl[k][10]] for k in cles], 331)
controle("(C3) rappel : GAMMA_139 n'est pas dans <unites> . K^{*331} (rang 11)", r139 == 11)
rangs = {}
for b in reps:
    col = [(lignes_dl[(ll, a)][11] - lignes_dl[(ll, rep_de[(a * b) % 115])][10]) % 331 for (ll, a) in cles]
    rangs[b] = rang_mod([U[i] + [col[i]] for i in range(len(cles))], 331)
print("      rangs de [unites | c_b] pour les 22 tau_b :", [rangs[b] for b in reps])
controle("(C4) pour chacun des 22 tau dans Gal(K/Q) : GAMMA_4969 / tau(GAMMA_139) n'est pas dans <unites> . K^{*331} (rang 11)",
         all(rangs[b] == 11 for b in reps))

# ---------------------------------------------------------------- (C5) norme vers F = Q(sqrt(-23))
controle("(C5) 4969 = 1 mod 23 : 4969 est decompose dans F = Q(sqrt(-23))", 4969 % 23 == 1)
reps_F = [(a, b) for b in range(0, 30) for a in range(0, 141) if a * a + 23 * b * b == 4 * 4969]
controle("(C5) 4*4969 = 19876 n'est pas de la forme a^2 + 23 b^2 : le premier de F au-dessus de 4969 n'est pas principal", not reps_F)
controle("(C5) rappel (note, rem. 6.11) : 599 = 24^2 + 23, N_{L/F}(P599) est principal", 24 ** 2 + 23 == 599)

print("BILAN : %d controles, %d echecs" % (len(OK), sum(1 for _, b in OK if not b)))
print("CONCLUSION (SANS GRH) : [P4969] n'est conjugue sous Gal(L/Q) ni a la classe principale, ni aux classes de 3-torsion,")
print("  ni a [P139], ni a [P599]. Avec le theoreme d'isometrie : X_4969 n'est isometrique ni a L0, ni a LS, ni a X_139, ni a X_599.")
