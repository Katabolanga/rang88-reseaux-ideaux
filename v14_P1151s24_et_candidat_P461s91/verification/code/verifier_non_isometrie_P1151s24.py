# -*- coding: utf-8 -*-
"""verifier_non_isometrie_P1151s24.py -- verification EXACTE, sans PARI/GP et SANS GRH, que la classe de l'ideal
I = P_6 sigma_24(P_6) = (1151, zeta - 6)(1151, zeta - 605) n'est conjuguee sous Gal(L/Q), L = Q(zeta_115), a aucune des classes
des six reseaux extremaux connus : L0, LS (Sakamoto), X139, X599, X4969, X4049 (et donc a aucun membre des paires de jumeaux
extremales de l'addendum, (L0, LS) et (X4049, X599)).
Adapte de verifier_non_isometrie_P4969_v2.py (methode (C1)-(C5)) et de la proposition 4.7 de l'addendum (cadran sans GRH).
Claude, 19 octobre 2026.

Notations : K = K22 = Q(theta), theta = zeta + zeta^22 + zeta^24 + zeta^68 ; Gal(L/K) = <sigma_22> = {1, 22, 24, 68}.
Pieces (CANDIDATS trouves par PARI sous GRH ; RIEN n'est cru, tout est recontrole ici) :
  data/P139/certificat_K22.txt     : P22, RACINE, GAMMA_139, unites XI_2..XI_11 (certificat de [Gau26], par. 6.4) ;
  data/cadran/cadran_sans_GRH_certificats.txt : une ligne par ideal (nom|sorte|p|lien|r|e|c|Gamma), addendum, prop. 4.7.
Controles :
  (C1) P22(theta) = 0 dans Z[zeta_115] ; {1,22,24,68} sous-groupe ; pour I (fichiers d'entree du balayage) : BASE engendre
       EXACTEMENT (1151, g(zeta)), g = (y - 6)(y - 605) scinde, 605 = 6^24 (indice |det BASE| = 1151^2) ; theta = 76 modulo P_6
       et modulo P_605 : q = P_6 inter K = P_605 inter K = (1151, theta - 76) de degre 1, N_{L/K}(I) = q^2 (e = 2) ;
       meme lien pour P139, P599, P4969, P4049 a partir de LEURS fichiers I_data.gp publies (premiers de degre 2, e = 2) ;
  (C2) XI_a unites ; pour chaque cible, Gamma entier algebrique, |N(Gamma)| = p^331, valuation 331 en q et 0 aux 21 autres
       premiers de K au-dessus de p : (Gamma) = q^331 ;
  (C3) logarithmes discrets modulo 331 aux 88 premiers de degre 1 de K au-dessus des 4 premiers auxiliaires l = 1 mod 331*115 :
       rang 10 (unites), rang 11 avec Gamma_139 ; pour chaque cible, l'unique c de F_331 tel que (e/2) lambda(Gamma) = c lambda(Gamma_139)
       modulo U (prop. 4.7 : [I]_331 = c [P139]_331) ; comparaison aux c publies ; heure h (c dans 2^h mu_22) ;
  (C4) controle direct, a la maniere de v2 : pour chacun des 22 tau de Gal(K/Q) et chaque T dans {P139, P599, P4969, P4049} :
       [unites | lambda(Gamma_I) - lambda(tau Gamma_T)] de rang 11 ;
  (C5) composante 3 : 1151 = 1 mod 23 et 4*1151 = 48^2 + 23*10^2 ; (24/23) = 1 ; composantes 3 des cibles publiees.
Consequences (preuves : [Gau26] prop. 2.2, 2.5, par. 6.4 ; addendum prop. 4.1, 4.7, cor. 4.2) : support de [I] = {331}
(composante 3 nulle par (C5), composante 45013 nulle car sigma_24(I) = I et 24 n'est pas dans ker chi_45013 = {1, 91},
composante 331 non nulle par (C3)) ; non-conjugaison a L0 (classe nulle), LS (support {3}), X139, X4969, X4049 (support {3,331}),
et a X599 (meme support {331}, mais c(I)/c(P599) hors de mu_22, et (C4)).
Usage (depuis la racine de p1151s24_preparation/) : python3 -I code/verifier_non_isometrie_P1151s24.py"""
import re, sys, os, hashlib
from fractions import Fraction as Fr
from math import lcm

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()
print("source : %s SHA-256 %s" % (os.path.basename(__file__), sha(os.path.abspath(__file__))))
_o = os.path.join(RACINE, "code", "outils_inchanges", "verifier_non_isometrie_P4969_v2_ORIGINAL.py")
if os.path.exists(_o): print("methode adaptee de : verifier_non_isometrie_P4969_v2.py SHA-256 %s" % sha(_o))
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
f139 = os.path.join(RACINE, "data", "P139", "certificat_K22.txt")
C139 = {}
for l in open(f139, encoding="ascii"):
    k, _, v = l.strip().partition(" = ")
    if k: C139[k] = v
print("certificat : data/P139/certificat_K22.txt SHA-256 %s" % sha(f139))
fcad = os.path.join(RACINE, "data", "cadran", "cadran_sans_GRH_certificats.txt")
print("certificat : data/cadran/cadran_sans_GRH_certificats.txt SHA-256 %s" % sha(fcad))
CAD = {}
for l in open(fcad, encoding="ascii"):
    if l.startswith("#") or not l.strip(): continue
    nom, sorte, p, lien, r, e, c, gam = l.rstrip("\r\n").split("|")
    CAD[nom] = dict(sorte=sorte, p=int(p), lien=lien, r=int(r), e=int(e), c=int(c), G=lire_poly(gam, "w"))
# cibles : l'ideal du balayage, les quatre ideaux publies, et (pour information) des ideaux de la couche deja tranches
PRINC = ["P1151s24", "P139pub", "P599pub", "P4969pub", "P4049pub"]
INFO = ["P691s24", "P829", "P39239", "P6211s24", "P53269"]
controle("cadran : les %d cibles sont presentes, une ligne chacune" % len(PRINC + INFO), all(n in CAD for n in PRINC + INFO))
P22 = lire_poly(C139["P22"], "w"); assert all(c.denominator == 1 for c in P22); P22 = [int(c) for c in P22]
controle("P22 unitaire de degre 22", len(P22) == 23 and P22[22] == 1)
XI = {a: lire_poly(C139["XI_%d" % a], "w") for a in range(2, 12)}
G139 = lire_poly(C139["GAMMA"], "w")
def sans_zeros(pl):
    pl = list(pl)
    while pl and pl[-1] == 0: pl.pop()
    return pl
controle("Gamma_139 du certificat de [Gau26] = Gamma de la ligne P139pub du cadran (meme element)", sans_zeros(G139) == sans_zeros(CAD["P139pub"]["G"]))
N = 22
DEN = lcm(*[c.denominator for el in list(XI.values()) + [G139] + [CAD[n]["G"] for n in PRINC + INFO] for c in el])
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
controle("(C1) {1,22,24,68} est un sous-groupe de (Z/115)^* (K = Fix<sigma_22>, de degre 22) et contient 24 : sigma_24 est dans Gal(L/K)",
         all((a * b) % 115 in H for a in H for b in H) and 24 in H)

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
def det_entier(Mx):
    Mx = [r[:] for r in Mx]; nn = len(Mx); sg = 1; prec = 1
    for k in range(nn - 1):
        if Mx[k][k] == 0:
            piv = next((i for i in range(k + 1, nn) if Mx[i][k] != 0), None)
            if piv is None: return 0
            Mx[k], Mx[piv] = Mx[piv], Mx[k]; sg = -sg
        for i in range(k + 1, nn):
            for j in range(k + 1, nn):
                Mx[i][j] = (Mx[i][j] * Mx[k][k] - Mx[i][k] * Mx[k][j]) // prec
        prec = Mx[k][k]
    return sg * Mx[nn - 1][nn - 1]
def theta_mod_lin(rr, p): return sum(pow(rr, k, p) for k in (1, 22, 24, 68)) % p        # theta modulo (p, zeta - rr)
def theta_mod_quad(g, p):                                                                # theta modulo (p, g(zeta)), g = y^2 + g1 y + g0
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
    return [sum(powg(k)[i] for k in (1, 22, 24, 68)) % p for i in range(2)]
def base_gp(nomdir):
    f = os.path.join(RACINE, "data", nomdir, "entrees", "I_data.gp")
    txt = open(f, encoding="ascii").read()
    mB = re.search(r"BASE = \[(.*?)\];", txt, re.S)
    print("      %s : I_data.gp SHA-256 %s ; %s" % (nomdir, sha(f), re.search(r"PREMIERS = (.*?);", txt).group(1)))
    return [[int(t) for t in row.split(",")] for row in mB.group(1).split(";")]
def g_de_base(lignes, p):
    g = [x % p for x in PHI]
    for j in range(88):
        col = [lignes[i][j] for i in range(88)]
        if any(x % p for x in col): g = pgcd_mod(g, col, p)
    return g
RACS = {}
def racines_P22(p):
    if p not in RACS: RACS[p] = [x for x in range(p) if horner(P22, x, p) == 0]
    return RACS[p]
# --- l'ideal du balayage
p = 1151
B = base_gp("P1151s24")
controle("(C1) P1151s24 : BASE de I_data.gp 88 x 88", len(B) == 88 and all(len(r) == 88 for r in B))
g = g_de_base(B, p)
rac = [x for x in range(p) if horner(g, x, p) == 0]
controle("(C1) P1151s24 : I mod 1151 = (g), g = (y - 6)(y - 605) de degre 2 SCINDE a racines distinctes (racines %s)" % rac, len(g) == 3 and rac == [6, 605])
controle("(C1) P1151s24 : 6 et 605 racines primitives 115-iemes mod 1151 (P_6, P_605 premiers de degre 1) et 605 = 6^24 (sigma_24(P_6) = P_605)",
         all(horner(PHI, x, p) == 0 for x in rac) and pow(6, 24, p) == 605 and pow(605, 24, p) == 6)
controle("(C1) P1151s24 : |det BASE| = 1151^2 : BASE engendre exactement (1151, g(zeta)) = P_6 P_605 (C1 autonome)", abs(det_entier(B)) == p * p)
t6, t605 = theta_mod_lin(6, p), theta_mod_lin(605, p)
controle("(C1) P1151s24 : theta = %d mod P_6 et %d mod P_605 : un seul premier q = (1151, theta - %d) de K sous I, de degre 1 ; N_{L/K}(I) = q^2, e = 2" % (t6, t605, t6),
         t6 == t605 and CAD["P1151s24"]["r"] == t6 and CAD["P1151s24"]["sorte"] == "b" and CAD["P1151s24"]["lien"] == "6" and CAD["P1151s24"]["e"] == 2)
controle("(C1) P1151s24 : P22 a 22 racines simples mod 1151 (1151 totalement decompose dans K), dont 76",
         len(racines_P22(p)) == 22 and all(horner(dP22, x, p) for x in racines_P22(p)) and 76 in racines_P22(p))
# --- les ideaux publies (premiers de degre 2)
PUB = {"P139pub": "P139", "P599pub": "P599", "P4969pub": "P4969", "P4049pub": "P4049"}
for nom, dossier in PUB.items():
    d = CAD[nom]; p = d["p"]
    Bp = base_gp(dossier)
    gp_ = g_de_base(Bp, p)
    g0, g1 = [int(x) for x in d["lien"].split(",")]
    disc = (gp_[1] ** 2 - 4 * gp_[0]) % p if len(gp_) == 3 else 0
    controle("(C1) %s : I mod %d = (y^2 + %d y + %d), irreductible (degre residuel 2), = lien du cadran ; |det BASE| = %d^2" % (dossier, p, g1, g0, p),
             len(gp_) == 3 and gp_[0] == g0 and gp_[1] == g1 and pow(disc, (p - 1) // 2, p) == p - 1 and abs(det_entier(Bp)) == p * p)
    tg = theta_mod_quad(gp_, p)
    controle("(C1) %s : theta mod P dans F_%d, egal a r = %d du cadran ; e = 2 ; P22 a 22 racines simples mod %d" % (dossier, p, d["r"], p),
             tg[1] == 0 and tg[0] == d["r"] and d["e"] == 2 and len(racines_P22(p)) == 22 and all(horner(dP22, x, p) for x in racines_P22(p)))
# --- cibles d'information (sans fichier de balayage) : lien abstrait, comme verifier_cadran.py
for nom in INFO:
    d = CAD[nom]; p = d["p"]
    if d["sorte"] == "b":
        rP = int(d["lien"]); ok = horner(PHI, rP, p) == 0 and theta_mod_lin(rP, p) == d["r"]
    else:
        g0, g1 = [int(x) for x in d["lien"].split(",")]; gq = [g0, g1, 1]
        ok = pgcd_mod([x % p for x in PHI], gq, p) == gq and theta_mod_quad(gq, p) == [d["r"], 0]       # g divise Phi_115 mod p
    controle("(C1) %s (information) : sorte %s, lien %s, theta = %d modulo le premier de L ; P22 a 22 racines simples mod %d" % (nom, d["sorte"], d["lien"], d["r"], p),
             ok and d["e"] == 2 and len(racines_P22(p)) == 22 and all(horner(dP22, x, p) for x in racines_P22(p)) and d["r"] in racines_P22(p))

# ---------------------------------------------------------------- (C2) polynomes caracteristiques et valuations
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
GAM = {"P139": G139}
for nom in PRINC + INFO:
    if nom != "P139pub": GAM[nom] = CAD[nom]["G"]
def verifie_gamma(nom, G, p, r):
    cg = polcar(matmul_elt(G))
    controle("(C2) %s : Gamma entier algebrique, |N(Gamma)| = %d^331" % (nom, p), all(x.denominator == 1 for x in cg) and abs(cg[N]) == p ** 331)
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
    vals = {x: valp(horner_fr(G, hensel(x), modK)) for x in racines_P22(p)}
    controle("(C2) %s : v(Gamma) = 331 en q = (%d, theta - %d) et 0 aux 21 autres premiers de K sur %d : (Gamma) = q^331" % (nom, p, r, p),
             vals[r % p] == 331 and sum(vals.values()) == 331)
verifie_gamma("P139 (certificat [Gau26])", G139, 139, 0)
for nom in PRINC + INFO:
    if nom != "P139pub": verifie_gamma(nom, GAM[nom], CAD[nom]["p"], CAD[nom]["r"])

# ---------------------------------------------------------------- (C3) logarithmes discrets modulo 331 ; etiquettes c
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
NOMS = ["P139"] + [n for n in PRINC + INFO if n != "P139pub"]
PS = {CAD[n]["p"] for n in PRINC + INFO} | {139}
lignes_dl = {}; premiers_l = []; l = 1
while len(premiers_l) < 4:
    l += 331 * 115
    if not est_premier(l) or l in PS or DEN % l == 0: continue
    z = None
    for h in range(2, 200):
        t = pow(h, (l - 1) // 115, l)
        if pow(t, 5, l) != 1 and pow(t, 23, l) != 1: z = t; break
    assert z is not None and pow(z, 115, l) == 1
    rac_l = {a: sum(pow(z, a * h, l) for h in H) % l for a in reps}
    if not (len(set(rac_l.values())) == 22 and all(horner(P22, x, l) == 0 for x in rac_l.values()) and all(horner(dP22, x, l) for x in rac_l.values())):
        continue
    om = None
    for h in range(2, 200):
        t = pow(h, (l - 1) // 331, l)
        if t != 1: om = t; break
    table = {pow(om, e, l): e for e in range(331)}
    assert len(table) == 331
    for a in reps:
        x = rac_l[a]; ligne = []
        for el in [XI[b] for b in range(2, 12)] + [GAM[n] for n in NOMS]:
            v = horner_fr(el, x, l)
            assert v != 0
            ligne.append(table[pow(v, (l - 1) // 331, l)])
        lignes_dl[(l, a)] = ligne
    premiers_l.append(l)
cles = sorted(lignes_dl)
col = {n: 10 + i for i, n in enumerate(NOMS)}
U = [lignes_dl[k][:10] for k in cles]
print("      premiers auxiliaires l :", premiers_l, "; %d lignes (22 premiers de K au-dessus de chaque l)" % len(cles))
controle("(C3) premiers auxiliaires = ceux de la prop. 4.7 de l'addendum (380651, 1065821, 1522601, 2055511)", premiers_l == [380651, 1065821, 1522601, 2055511])
controle("(C3) les 10 unites XI_a sont independantes modulo les puissances 331-iemes (rang 10)", rang_mod(U, 331) == 10)
v139 = [lignes_dl[k][col["P139"]] for k in cles]
controle("(C3) [unites | Gamma_139] de rang 11", rang_mod([U[i] + [v139[i]] for i in range(len(cles))], 331) == 11)
def etiquette(nom):
    e = CAD[nom]["e"] if nom in CAD else 2
    v = [lignes_dl[k][col[nom]] * e * pow(2, -1, 331) % 331 for k in cles]          # (e/2) lambda(Gamma)
    sol = [c for c in range(331) if rang_mod([U[i] + [(v[i] - c * v139[i]) % 331] for i in range(len(cles))], 331) == 10]
    return sol
def heure(c):
    return [h for h in range(15) if pow(c * pow(pow(2, h, 331), -1, 331) % 331, 22, 331) == 1]
ETIQ = {}
for nom in PRINC + INFO:
    nn = "P139" if nom == "P139pub" else nom
    sol = etiquette(nn)
    hh = heure(sol[0]) if len(sol) == 1 and sol[0] else []
    controle("(C3) %s : une seule solution c = %s (publie : %d) ; heure %s" % (nom, sol, CAD[nom]["c"], hh),
             len(sol) == 1 and sol[0] == CAD[nom]["c"] and (sol[0] == 0 or len(hh) == 1))
    ETIQ[nom] = (sol[0], hh[0] if hh else None)
cI = ETIQ["P1151s24"][0]
controle("(C3) c(I) = %d non nul : [unites | Gamma_I] de rang 11, la composante 331 de [I] est NON NULLE (I non principal ; support contient 331)" % cI,
         cI != 0 and rang_mod([U[i] + [lignes_dl[k][col["P1151s24"]]] for i, k in enumerate(cles)], 331) == 11)
mu22 = {x for x in range(1, 331) if pow(x, 22, 331) == 1}
controle("mu_22 de F_331 a 22 elements ; 3 racine primitive mod 331 ; F_331^*/mu_22 cyclique d'ordre 15 engendre par 2", len(mu22) == 22 and len({pow(3, k, 331) for k in range(330)}) == 330 and len({pow(2, k, 331) * m % 331 for k in range(15) for m in mu22}) == 330)
for T in ("P599pub", "P139pub", "P4969pub", "P4049pub"):
    q = cI * pow(ETIQ[T][0], -1, 331) % 331
    controle("(C3) c(I)/c(%s) = %d/%d = %d mod 331 n'est pas dans mu_22 : composantes 331 NON conjuguees (heures %d et %d)" % (T, cI, ETIQ[T][0], q, ETIQ["P1151s24"][1], ETIQ[T][1]),
             q not in mu22)

# ---------------------------------------------------------------- (C4) controle direct, 22 tau, a la maniere de v2
for T, nn in (("P139", "P139"), ("P599pub", "P599pub"), ("P4969pub", "P4969pub"), ("P4049pub", "P4049pub")):
    rangs = []
    for b in reps:
        cc = [(lignes_dl[(ll, a)][col["P1151s24"]] - lignes_dl[(ll, rep_de[(a * b) % 115])][col[nn]]) % 331 for (ll, a) in cles]
        rangs.append(rang_mod([U[i] + [cc[i]] for i in range(len(cles))], 331))
    controle("(C4) %s : pour les 22 tau de Gal(K/Q), Gamma_I / tau(Gamma_%s) n'est pas dans <unites> . K^{*331} (rangs %s)" % (T, T, sorted(set(rangs))),
             all(r == 11 for r in rangs))

# ---------------------------------------------------------------- (C5) composantes 3 (norme vers F = Q(sqrt(-23)))
def rep_F(p): return [(a, b) for b in range(0, int((4 * p / 23) ** 0.5) + 2) for a in range(0, int((4 * p) ** 0.5) + 2) if a * a + 23 * b * b == 4 * p]
controle("(C5) 1151 = 1 mod 23 (decompose dans F) et 4*1151 = 4604 = 48^2 + 23*10^2 : le premier de F sous P_6 est principal", 1151 % 23 == 1 and (48, 10) in rep_F(1151))
leg = pow(24, (23 - 1) // 2, 23)
controle("(C5) (24/23) = %d : chi_3(sigma_24) = 1, donc [I]_3 = [P_6]_3 + sigma_24[P_6]_3 = 2 [P_6]_3 = 0" % leg, leg == 1)
controle("(C5) 4p n'est pas de la forme a^2 + 23 b^2 pour p = 139, 4969, 4049 : composantes 3 de X139, X4969, X4049 non nulles",
         all(not rep_F(q) for q in (139, 4969, 4049)) and all(q % 23 == 1 for q in (139, 4969, 4049)))
controle("(C5) rappel : 599 = 24^2 + 23 (4*599 = 48^2 + 23*2^2), composante 3 de X599 nulle", (48, 2) in rep_F(599))
controle("(C5) information : 4*691 = 44^2 + 23*6^2 (composante 3 nulle), 4*829 = 2^2 + 23*12^2, 6211 : aucun (composante 3 non nulle), 53269 = 1 mod 23 : %s"
         % ("representation" if rep_F(53269) else "aucune"), (44, 6) in rep_F(691) and (2, 12) in rep_F(829) and not rep_F(6211))
print("      etiquettes (c, heure) : " + " ; ".join("%s %s" % (n, ETIQ[n]) for n in PRINC + INFO))
hI = ETIQ["P1151s24"][1]
rej = {ETIQ[n][1] for n in ("P691s24", "P829", "P39239")}
controle("information : heure de I = %d ; orbites exterieures REJETEES (norme 6 demontree) aux heures %s : I n'est conjugue a aucune (coherence avec le balayage)" % (hI, sorted(rej)),
         hI not in rej)
print("      information : jumeau de X_I = orbite interieure d'heure %d (P6211s24, heure %s, survivant partiel) ; jumeau de X139 = P53269 (heure %s)" % (hI, ETIQ["P6211s24"][1], ETIQ["P53269"][1]))

print("BILAN : %d controles, %d echecs" % (len(OK), sum(1 for _, b in OK if not b)))
print("CONCLUSION (SANS GRH, modulo [Gau26] prop. 2.2, 2.5) : [I], I = P_6 sigma_24(P_6) au-dessus de 1151, est de support {331},")
print("  d'etiquette c = %d et d'heure %d ; elle n'est conjuguee sous Gal(L/Q) ni a la classe nulle (L0), ni aux classes de support {3} (LS)," % (cI, hI))
print("  ni a [P139], [P4969], [P4049] (support {3,331}), ni a [P599] (heure 8). Avec le theoreme d'isometrie [Gau26, th. 3.3], qui demande")
print("  le minimum 8 d'au moins un des deux reseaux compares : X_I n'est isometrique a aucun des six reseaux extremaux connus.")
