# -*- coding: utf-8 -*-
"""verifier_temoins.py -- second controle, INDEPENDANT de PARI/GP, des huit temoins de norme 6 (note, prop. 6.1, tableau 2).

Les fichiers data/rejets/temoin_*.gp sont lus comme du TEXTE par une grammaire limitee (polynomes a coefficients
rationnels, matrices et vecteurs d'entiers) ; rien n'est evalue ni execute.  Pour chaque temoin, en entiers et
rationnels exacts :
  T1  PM et BETA0 du fichier sont ceux de data/corps/rang88_m115c0_data.txt ; PM(c) = 0 dans Z[zeta], c = zeta + 1/zeta ;
      ALPHA * NU = BETA0 dans Q[x]/PM ;
  T2  BASE (88 x 88, entiere) : |det| = p^f ; BASE^-1 (p I_88) et BASE^-1 M_zeta BASE entieres : I est un ideal de
      Z[zeta] contenant p, d'indice p^f ; identification : I mod p = (g), g unitaire divisant Phi_115 mod p, de degre f
      (irreductible si f = 2), et p, g(zeta) dans I : I = (p, g(zeta)) ;
  T3  GRAM = BASE~ H BASE, H_ij = Tr_L(alpha zeta^(i-j)) (rationnels) recalcule par les sommes de Ramanujan ; GRAM symetrique,
      entiere, paire, definie positive (88 mineurs principaux > 0, Bareiss), det = 1 ;
  T4  X entier non nul, X~ GRAM X = 6 ; Z (coefficients en zeta^0..zeta^87) = BASE X ;
  T5  pour P829, P1289, P1979 : une rotation zeta^k z a les energies (courte, fibre) imprimees au par. 6.1 de la note.
Usage (depuis la racine du depot) : python -I code/verification/verifier_temoins.py      (environ 1 min)"""
import re, sys, os, hashlib
from fractions import Fraction as Fr
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
FICHIERS = ["temoin_P461r5.gp", "temoin_P691r4.gp", "temoin_P1151r6.gp", "temoin_P1381r21.gp",
            "temoin_P1471d2.gp", "temoin_P829d2.gp", "temoin_P1289d2.gp", "temoin_P1979d2.gp"]
ATTENDU = {"P461": (461, 1, [-5, 1]), "P691": (691, 1, [-4, 1]), "P1151": (1151, 1, [-6, 1]), "P1381": (1381, 1, [-21, 1]),
           "P1471": (1471, 2, [948, 879, 1]), "P829": (829, 2, None), "P1289": (1289, 2, None), "P1979": (1979, 2, None)}
DECOMP = {"P829": (Fr(3161, 829), Fr(22505692, 1658 ** 2)), "P1289": (Fr(5683, 1289), Fr(50451460, 2578 ** 2)),
          "P1979": (Fr(9260, 1979), Fr(114687008, 3958 ** 2))}
n, nh, m = 88, 44, 115

# ---------------------------------------------------------------- lecture (texte seulement)
def lire_affectations(f):
    t = open(f, encoding="ascii").read()
    d = {}
    for mm in re.finditer(r"^([A-Z][A-Z_0-9]*) = (.*?);\s*$", t, re.S | re.M):
        d[mm.group(1)] = mm.group(2)
    return d
def poly(s, var):
    s = s.replace(" ", "").replace("\n", "")
    assert re.fullmatch(r"[-+*/^0-9%s]+" % var, s), "polynome inattendu"
    s = s.replace("-", "+-"); co = {}
    for t in s.split("+"):
        if not t: continue
        if var in t:
            c, _, e = t.partition(var); e = int(e[1:]) if e else 1; c = c.rstrip("*")
            c = Fr(1) if c == "" else (Fr(-1) if c == "-" else Fr(c))
        else: c, e = Fr(t), 0
        co[e] = co.get(e, 0) + c
    return [co.get(i, Fr(0)) for i in range(max(co) + 1)]
def matint(s):
    s = s.strip(); assert s[0] == "[" and s[-1] == "]" and re.fullmatch(r"[-0-9,; \n]*", s[1:-1])
    return [[int(t) for t in row.split(",")] for row in s[1:-1].split(";")]
def colint(s):
    s = s.strip(); assert s.endswith("]~") and s[0] == "["
    return [int(t) for t in s[1:-2].split(",")]
def lire_Z(s):
    s = s.strip()
    mm = re.fullmatch(r"Polrev\(\[([-0-9, ]*)\], 'y\)", s)
    if mm: v = [int(t) for t in mm.group(1).split(",")]
    else: v = [int(c) for c in poly(s, "y")]
    return v + [0] * (n - len(v))
def lire_premiers(s):
    assert re.fullmatch(r"\[\[[0-9, ]*\]\]", s.strip()); return [int(t) for t in s.strip()[2:-2].split(",")]

# ---------------------------------------------------------------- arithmetique exacte
def montante(A, B=None, pivotage=True):
    nn = len(A); w = 0 if B is None else len(B[0])
    Mx = [[int(v) for v in A[i]] + ([int(v) for v in B[i]] if B is not None else []) for i in range(nn)]
    prev = 1; piv = []; signe = 1
    for k in range(nn):
        if Mx[k][k] == 0:
            if not pivotage: raise ZeroDivisionError("pivot nul")
            l = next((i for i in range(k + 1, nn) if Mx[i][k] != 0), None)
            if l is None: raise ZeroDivisionError("matrice singuliere")
            Mx[k], Mx[l] = Mx[l], Mx[k]; signe = -signe
        pk = Mx[k][k]; piv.append(pk); rk = Mx[k]
        for i in range(nn):
            if i == k: continue
            ri = Mx[i]; f = ri[k]
            nv = [pk * ri[j] - f * rk[j] for j in range(nn + w)]
            assert all(v % prev == 0 for v in nv)
            Mx[i] = [v // prev for v in nv]
        prev = pk
    det = signe * piv[-1]
    X = None if B is None else [[Fr(Mx[i][nn + j], Mx[i][i]) for j in range(w)] for i in range(nn)]
    return det, piv, X
def mm_(A, B):
    Bt = list(zip(*B))
    return [[sum(x * y for x, y in zip(r, c) if x and y) for c in Bt] for r in A]
def tr_(A): return [list(r) for r in zip(*A)]
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
    for i in range(len(a) - 1, n - 1, -1):
        c = a[i]
        if c:
            for j, y in enumerate(PHI): a[i - n + j] -= c * y
    return a[:n]
def mulc(a, b):
    r = [0] * m
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y: r[(i + j) % m] += x * y
    return r
def ram(k):   # Tr_L(zeta^k), somme de Ramanujan c_115(k)
    k %= m
    if k == 0: return 88
    if k % 23 == 0: return -22
    if k % 5 == 0: return -4
    return 1
cc = [0] * m; cc[1] = 1; cc[114] = 1
cp = [[1] + [0] * (m - 1)]
for k in range(1, 45): cp.append(mulc(cp[-1], cc))
def plonge(pl):
    r = [Fr(0)] * m
    for k, c in enumerate(pl):
        if c:
            for i, v in enumerate(cp[k]):
                if v: r[i] += c * v
    return r
def mulmod(a, b, P):   # produit dans Q[x]/P, P unitaire
    r = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y: r[i + j] += x * y
    d = len(P) - 1
    for i in range(len(r) - 1, d - 1, -1):
        c = r[i]
        if c:
            for j, y in enumerate(P): r[i - d + j] -= c * y
    r = r[:d]; return r + [Fr(0)] * (d - len(r))
def pgcd_mod(a, b, p):
    def nz(a):
        while a and a[-1] % p == 0: a.pop()
        return a
    a = nz([x % p for x in a]); b = nz([x % p for x in b])
    while b:
        inv = pow(b[-1], -1, p)
        while a and len(a) >= len(b):
            c = a[-1] * inv % p; s = len(a) - len(b)
            for j, y in enumerate(b): a[s + j] = (a[s + j] - c * y) % p
            a = nz(a)
        a, b = b, a
    inv = pow(a[-1], -1, p); return [x * inv % p for x in a]

# ---------------------------------------------------------------- donnees du corps
DAT = open(os.path.join(RACINE, "data", "corps", "rang88_m115c0_data.txt"), encoding="ascii").read().strip()
assert DAT[0] == "[" and DAT[-1] == "]"
parts = DAT[1:-1].split(",", 2)
PMc = poly(parts[0], "x"); B0c = poly(parts[1], "x")
acc = [0] * m
for k, c in enumerate(PMc): acc = [x + int(c) * y for x, y in zip(acc, cp[k])]
assert len(PMc) == 45 and PMc[44] == 1 and not any(redphi(acc)), "Pm"

NBT = [0, 0]
for nomf in FICHIERS:
    f = os.path.join(RACINE, "data", "rejets", nomf)
    d = lire_affectations(f)
    NOM = d["NOM"].strip('"'); cle = NOM.split("_")[0]
    p, fdeg, gatt = ATTENDU[cle]
    pr = lire_premiers(d["PREMIERS"])
    erreurs = []
    def chk(c, s):
        if not c: erreurs.append(s)
    # T1
    PM = poly(d["PM"], "x"); BETA0 = poly(d["BETA0"], "x"); NU = poly(d["NU"], "x"); ALPHA = poly(d["ALPHA"], "x")
    chk(PM == PMc and BETA0 + [Fr(0)] * (44 - len(BETA0)) == B0c + [Fr(0)] * (44 - len(B0c)), "PM, BETA0 = data/corps")
    pad = lambda v: v + [Fr(0)] * (44 - len(v))
    chk(mulmod(pad(ALPHA), pad(NU), PM) == pad(BETA0), "ALPHA * NU = BETA0")
    # T2
    BASE = matint(d["BASE"]); NI = int(d["NORME_ABS_I"])
    chk(len(BASE) == n and all(len(r) == n for r in BASE), "BASE 88 x 88")
    chk(pr[0] == p and NI == p ** fdeg, "PREMIERS, NORME_ABS_I")
    detB, _, Binv = montante(BASE, [[int(i == j) for j in range(n)] for i in range(n)])
    chk(abs(detB) == p ** fdeg, "|det BASE| = p^f")
    def dans_I(v88): return all(sum(Binv[i][j] * v88[j] for j in range(n)).denominator == 1 for i in range(n))
    chk(all(dans_I(redphi([0] + [BASE[i][j] for i in range(n)])) for j in range(n)), "zeta I dans I")
    g = [x % p for x in PHI]
    for j in range(n): g = pgcd_mod(g, [BASE[i][j] for i in range(n)], p)
    chk(len(g) == fdeg + 1, "I mod p = (g), deg g = f")
    if fdeg == 2:
        disc = (g[1] * g[1] - 4 * g[0]) % p
        chk(pow(disc, (p - 1) // 2, p) == p - 1, "g irreductible mod p")
    chk(dans_I([p] + [0] * 87) and dans_I(g + [0] * (n - len(g))), "p et g(zeta) dans I : I = (p, g(zeta))")
    if gatt is not None: chk(g == [x % p for x in gatt], "g = celui du tableau 2 de la note")
    # T3
    al = plonge(ALPHA)
    t = [sum(al[i] * ram(i + k) for i in range(m)) for k in range(m)]
    chk(all(t[k] == t[(-k) % m] for k in range(m)), "alpha reel")
    Hm = [[t[(i - j) % m] for j in range(n)] for i in range(n)]       # rationnelle : alpha n'est pas dans la codifferente
    G = mm_(tr_(BASE), mm_(Hm, BASE)); GRAM = matint(d["GRAM"])
    chk(all(x.denominator == 1 for r in G for x in r), "BASE~ H BASE entiere")
    G = [[int(x) for x in r] for r in G]
    chk(G == GRAM, "GRAM = BASE~ H BASE")
    chk(all(G[i][j] == G[j][i] for i in range(n) for j in range(n)) and all(G[i][i] % 2 == 0 for i in range(n)), "GRAM symetrique paire")
    detG, pivG, _ = montante(G, pivotage=False)
    chk(all(x > 0 for x in pivG) and detG == 1, "GRAM definie positive, det 1")
    # T4
    X = colint(d["X"]); Zv = lire_Z(d["Z"])
    N6 = sum(X[i] * G[i][j] * X[j] for i in range(n) for j in range(n) if X[i] and X[j])
    chk(len(X) == n and any(X) and N6 == 6 and int(d["NORME"]) == 6, "X~ GRAM X = 6")
    chk([sum(BASE[i][j] * X[j] for j in range(n)) for i in range(n)] == Zv, "Z = BASE X")
    # T5 : decomposition (energie courte, energie de fibre) des trois touches de Rang88CertZ (note, par. 6.1) :
    #      il existe k tel que Lambda(a_k) = 6 + f(k) et Lambda'(b_k) = 6 - f(k) valent les deux fractions imprimees,
    #      avec f(k) = Tr_L(alpha zeta^(2k) z^2) (lemme 4.2).
    if cle in DECOMP:
        zc = Zv + [0] * (m - n)
        w2 = mulc(zc, zc)
        v = [Fr(0)] * m
        for i, x in enumerate(al):
            if x:
                for j, y in enumerate(w2):
                    if y: v[(i + j) % m] += x * y
        fk = [sum(v[r] * ram(r + 2 * k) for r in range(m) if v[r]) for k in range(m)]
        ea, eb = DECOMP[cle]
        trouve = [k for k in range(m) if 6 + fk[k] == ea and 6 - fk[k] == eb]
        chk(len(trouve) >= 1, "decomposition des energies")
        print("        %s : rotation k = %s : Lambda(a_k) = %s et Lambda'(b_k) = %s (somme 12)" % (cle, trouve, ea, eb))
    ok = not erreurs
    NBT[0] += 1; NBT[1] += (not ok)
    gtxt = " + ".join(("%d*z^%d" % (c, k) if k else "%d" % c) for k, c in reversed(list(enumerate(g))) if c)
    print("%-7s %-20s SHA-256 %s : I = (%d, %s) ; |det BASE| = %d ; GRAM paire, det 1, definie positive ; X~ GRAM X = %d : %s"
          % (cle, nomf, hashlib.sha256(open(f, "rb").read()).hexdigest()[:16] + "...", p, gtxt, abs(detB), N6,
             "TEMOIN VALIDE" if ok else "ECHEC " + "; ".join(erreurs)))
    sys.stdout.flush()
print("BILAN : %d temoins, %d echecs" % (NBT[0], NBT[1]))
print("FIN_OK" if NBT[1] == 0 else "FIN_ECHEC")
sys.exit(0 if NBT[1] == 0 else 1)
