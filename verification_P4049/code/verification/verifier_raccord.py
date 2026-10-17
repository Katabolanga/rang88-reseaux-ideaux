# -*- coding: utf-8 -*-
"""verifier_raccord.py -- raccord geometrique EXACT des fichiers d'entree du programme certifiant au reseau ideal
X_p = (P_p, beta_0/nu) sur L = Q(zeta_115), pour p = 139 ou 599 (note, prop. 6.3 et 6.4, points (1) et (2) ; th. 6.11 (A)).

Independant de PARI/GP : seules les DONNEES (data/Pp/entrees/I_data.gp, cote*_bases.gp, fichiers d'entree du programme,
data/corps/rang88_m115c0_data.txt) sont relues ; toutes les relations sont recalculees en entiers et rationnels exacts.

Controles G1..G9 :
  G1  BASE est une Z-base d'un ideal I de Z[zeta], d'indice p^2, I = (p, g(zeta)) premier de degre 2, I != Ibar ;
  G2  GRAM = BASE~ H BASE avec H_ij = Tr_L(alpha zeta^(i-j)) recalculee a partir de ALPHA ; GRAM entiere, symetrique,
      paire, definie positive (mineurs principaux > 0, Bareiss exact), det = 1 ;
  G3  nu : N(nu) = p^2, nu dans I, (nu) = I Ibar ; Pm polynome minimal de c = zeta + 1/zeta ;
  G4  AB : pour chaque vecteur de base z de I, z + zbar = sum a_k c^k et z - zbar = e * sum b_k c^k (identites dans Z[zeta]) ;
  G5  QA = (Tr+(alpha c^(i+j))), QB = (Tr+(alpha (4-c^2) c^(i+j))) ; AB~ diag(QB, QA) AB / 2 = GRAM (prop. 4.1) ;
  G6  pour chaque cote : le reseau colonne de [[Hf, Hl], [0, Hc]] est celui de R (= AB, lignes (fibre ; courte)) ;
      A.gram = DA Hc~ QC Hc ; B.gram = DB Hf~ QF Hf ; Hf Tn = d Hl ; meta = (DA, DB, d) ; fibre = 2 nu O+ ;
      les empreintes des 4 fichiers d'entree sont celles qu'ont imprimees TOUTES les executions conservees
      (data/Pp/replication/*.stdout.log et data/Pp/premiere_execution/*.log) ;
  G7  arithmetique du seuil : (6 - 1057/200)^2 < 45/88 ;
  G8  lemmes 4.2 et 4.3, relation a cinq termes : controle exact sur quelques vecteurs (illustration ; la preuve est dans la note) ;
  G9  vecteur de norme 8 : fichier data/Pp/norme8.txt (cote, u, y) -> x dans la base de I, x~ GRAM x = 8.
Usage (depuis la racine du depot) : python -I code/verification/verifier_raccord.py P139     (ou P599 ; 1 a 3 min)"""
import re, sys, os, hashlib, random, glob
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
from fractions import Fraction as Fr

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if len(sys.argv) != 2 or sys.argv[1] not in ("P139", "P599", "P4969", "P4049"): raise SystemExit("usage : verifier_raccord.py P139|P599|P4969|P4049")
CAND = sys.argv[1]; PP = int(CAND[1:])
DJ = os.path.join(RACINE, "data", CAND, "entrees")
print("candidat", CAND)
NB = [0, 0]
def controle(nom, cond):
    NB[0] += 1
    print(("OK    " if cond else "ECHEC ") + nom); sys.stdout.flush()
    if not cond: NB[1] += 1; raise SystemExit("ECHEC : " + nom)
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()

# ------------------------------------------------------------------ lecture
def lire_gp(f):
    d = {}
    for mm in re.finditer(r"(\w+) = (.*?);\s*$", open(f, encoding="ascii").read(), re.S | re.M):
        d[mm.group(1)] = mm.group(2)
    return d
def mat(s):
    s = s.strip(); assert s[0] == "[" and s[-1] == "]"
    return [[Fr(t) for t in row.split(",")] for row in s[1:-1].split(";")]
def matint(s):
    Mx = mat(s); assert all(x.denominator == 1 for r in Mx for x in r)
    return [[int(x) for x in r] for r in Mx]
def poly(s, var="x"):
    s = s.replace(" ", "").replace("-", "+-"); co = {}
    for t in s.split("+"):
        if not t: continue
        if var in t:
            c, _, e = t.partition(var); e = int(e[1:]) if e else 1; c = c.rstrip("*")
            c = Fr(1) if c == "" else (Fr(-1) if c == "-" else Fr(c))
        else: c, e = Fr(t), 0
        co[e] = co.get(e, 0) + c
    return [co.get(i, Fr(0)) for i in range(max(co) + 1)]
def lire_java(f):
    t = open(f).read().split(); r, c = int(t[0]), int(t[1]); assert len(t) == 2 + r * c
    return [[int(t[2 + i * c + j]) for j in range(c)] for i in range(r)]

ID = lire_gp(os.path.join(DJ, "I_data.gp"))
print("I_data.gp SHA-256", sha(os.path.join(DJ, "I_data.gp")), "; PREMIERS =", ID["PREMIERS"], "; Q =", ID["Q"])
BASE = matint(ID["BASE"]); GRAM = matint(ID["GRAM"]); AB = matint(ID["AB"])
NU = poly(ID["NU"]); ALPHA = poly(ID["ALPHA"]); Q = int(ID["Q"])
n, nh, m = 88, 44, 115
controle("dimensions : BASE, GRAM, AB 88 x 88 ; NU, ALPHA de degre <= 43 ; Q = %d^2" % PP,
         all(len(X) == n and all(len(r) == n for r in X) for X in (BASE, GRAM, AB)) and len(NU) <= nh and len(ALPHA) <= nh and Q == PP ** 2)

# ------------------------------------------------------------------ algèbre linéaire exacte
def mm_(A, B):
    Bt = list(zip(*B))
    return [[sum(x * y for x, y in zip(r, c) if x and y) for c in Bt] for r in A]
def tr_(A): return [list(r) for r in zip(*A)]
def montante(A, B=None, pivotage=True):
    """Gauss-Jordan sans fraction (Bareiss/Montante) sur des ENTIERS.  Rend (det, pivots, X) avec A X = B (X rationnel exact).
    Sans échange de lignes, pivots[k] = mineur principal dominant d'ordre k+1 (pivotage=False : erreur si un pivot est nul)."""
    nn = len(A); w = 0 if B is None else len(B[0])
    Mx = [[int(v) for v in A[i]] + ([int(v) for v in B[i]] if B is not None else []) for i in range(nn)]
    assert all(Mx[i][j] == (list(A[i]) + (list(B[i]) if B is not None else []))[j] for i in range(nn) for j in range(nn + w))
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

# ------------------------------------------------------------------ Z[y]/(y^115 - 1), Phi_115, traces
def mulc(a, b):
    r = [0] * m
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y: r[(i + j) % m] += x * y
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
ym = lambda k: [-1] + [0] * (k - 1) + [1]
PHI = poldivex(polmul(ym(115), ym(1)), polmul(ym(5), ym(23)))
def redphi(a):
    a = list(a) + [0] * (m - len(a))
    for i in range(m - 1, n - 1, -1):
        c = a[i]
        if c:
            for j, y in enumerate(PHI): a[i - n + j] -= c * y
    return a[:n]
def ram(k):   # Tr_L(zeta^k)
    k %= m
    if k == 0: return 88
    if k % 23 == 0: return -22
    if k % 5 == 0: return -4
    return 1
def conj(a): return [a[(-i) % m] for i in range(m)]
cc = [0] * m; cc[1] = 1; cc[114] = 1             # c = zeta + zeta^-1
ee = [0] * m; ee[1] = 1; ee[114] = -1            # e = zeta - zeta^-1
cp = [[1] + [0] * (m - 1)]
for k in range(1, 140): cp.append(mulc(cp[-1], cc))   # c^k dans l'anneau cyclique
tau = [sum(v * ram(i) for i, v in enumerate(cp[k])) for k in range(140)]   # Tr_L(c^k)
def plonge(pl):    # élément de L+ (polynôme en x = c, coefficients rationnels) -> vecteur cyclique
    r = [Fr(0)] * m
    for k, c in enumerate(pl):
        if c:
            for i, v in enumerate(cp[k]):
                if v: r[i] += c * v
    return r
al = plonge(ALPHA)

# ------------------------------------------------------------------ G1 : l'idéal I
detB, _, Binv = montante(tr_(tr_(BASE)), [[int(i == j) for j in range(n)] for i in range(n)])
controle("G1 |det BASE| = %d^2 (indice de I dans Z[zeta])" % PP, abs(detB) == PP ** 2)
def dans_I(v88): return all(sum(Binv[i][j] * v88[j] for j in range(n)).denominator == 1 for i in range(n))
okz = True
for j in range(n):
    col = [BASE[i][j] for i in range(n)]
    okz &= dans_I(redphi([0] + col))               # zeta * (colonne j)
controle("G1 zeta * I contenu dans I (I est un ideal de Z[zeta_115])", okz)
p = PP
def pgcd_mod(a, b):
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
g = [x % p for x in PHI]
for j in range(n): g = pgcd_mod(g, [BASE[i][j] for i in range(n)])
controle("G1 I mod %d = (g), g unitaire de degre 2 divisant Phi_115 mod %d" % (PP, PP), len(g) == 3)
disc = (g[1] * g[1] - 4 * g[0]) % p
controle("G1 g irreductible mod %d (discriminant non residu)" % PP, pow(disc, (p - 1) // 2, p) == p - 1)
controle("G1 %d dans I et g(zeta) dans I : I = (%d, g(zeta)), premier de degre residuel 2" % (PP, PP),
         dans_I([PP] + [0] * 87) and dans_I(g + [0] * 85))
gstar = [g[2] * pow(g[0], -1, p) % p, g[1] * pow(g[0], -1, p) % p, 1]   # polynôme réciproque normalisé : idéal conjugué
controle("G1 I different de son conjugue (g* != g), donc I + Ibar = O_L", gstar != g)
print("      g = y^2 + %d y + %d ; g* = y^2 + %d y + %d (mod %d)" % (g[1], g[0], gstar[1], gstar[0], PP))

# ------------------------------------------------------------------ G2 : la Gram
t = [sum(al[i] * ram(i + k) for i in range(m)) for k in range(m)]   # Tr_L(alpha zeta^k)
controle("G2 alpha reel : Tr(alpha zeta^k) = Tr(alpha zeta^-k)", all(t[k] == t[(-k) % m] for k in range(m)))
Hm = [[t[(i - j) % m] for j in range(n)] for i in range(n)]
G2 = mm_(tr_(BASE), mm_(Hm, BASE))
controle("G2 BASE~ H BASE = GRAM (H recalculee depuis ALPHA), entiere", all(G2[i][j] == GRAM[i][j] for i in range(n) for j in range(n)))
controle("G2 GRAM symetrique et paire", all(GRAM[i][j] == GRAM[j][i] for i in range(n) for j in range(n)) and all(GRAM[i][i] % 2 == 0 for i in range(n)))
detG, pivG, _ = montante(GRAM, pivotage=False)
controle("G2 GRAM definie positive (88 mineurs principaux dominants > 0, exact)", all(x > 0 for x in pivG))
controle("G2 det GRAM = 1", detG == 1)
print("      diagonale de GRAM : min %d, max %d" % (min(GRAM[i][i] for i in range(n)), max(GRAM[i][i] for i in range(n))))

# ------------------------------------------------------------------ G3 : nu
nuc = plonge(NU); assert all(x.denominator == 1 for x in nuc); nuc = [int(x) for x in nuc]
controle("G3 nu dans I (donc dans I inter Ibar = I Ibar, nu etant reel)", dans_I(redphi(nuc)))
# norme de nu dans L+ : déterminant de la multiplication par nu sur la base c^k de O+ = Z[c] ; il faut Pm
DAT = open(os.path.join(RACINE, "data", "corps", "rang88_m115c0_data.txt"), encoding="ascii").read()
Pm = poly(DAT[DAT.index("[") + 1: DAT.index(",")]); Pm = [int(x) for x in Pm]
acc = [0] * m
for k, c in enumerate(Pm): acc = [x + c * y for x, y in zip(acc, cp[k])]
controle("G3 Pm(c) = 0 dans Z[zeta], Pm unitaire de degre 44 (polynome minimal de c = zeta + 1/zeta)", len(Pm) == 45 and Pm[44] == 1 and not any(redphi(acc)))
def mulxmat(pl):   # matrice (44 x 44) de la multiplication par pl(x) dans Q[x]/Pm, base x^k
    cols = []; v = list(pl) + [0] * (nh - len(pl))
    for _ in range(nh):
        cols.append(v[:]); top = v[nh - 1]; v = [0] + v[:nh - 1]
        if top:
            for i in range(nh): v[i] -= top * Pm[i]
    return [[cols[j][i] for j in range(nh)] for i in range(nh)]
NUi = [int(x) for x in NU]
Mnu = mulxmat(NUi)
detnu, _, _ = montante(Mnu)
controle("G3 N_{L+/Q}(nu) = %d^2 = N(I) : (nu) O_L = I Ibar" % PP, abs(detnu) == PP ** 2)

# ------------------------------------------------------------------ G4 : le recollement AB
ok4 = True
ecp = [mulc(ee, cp[k]) for k in range(nh)]
for j in range(n):
    w = [BASE[i][j] for i in range(n)] + [0] * (m - n); wb = conj(w)
    som = [x + y for x, y in zip(w, wb)]; dif = [x - y for x, y in zip(w, wb)]
    a = [0] * m; b = [0] * m
    for k in range(nh):
        ak = AB[nh + k][j]; bk = AB[k][j]
        if ak: a = [x + ak * y for x, y in zip(a, cp[k])]
        if bk: b = [x + bk * y for x, y in zip(b, ecp[k])]
    ok4 &= redphi([x - y for x, y in zip(som, a)]) == [0] * n and redphi([x - y for x, y in zip(dif, b)]) == [0] * n
controle("G4 pour les 88 vecteurs de base z de I : z + zbar = a(c), z - zbar = e b(c), (b ; a) = colonne de AB", ok4)
detAB, _, ABinv = montante(AB, [[int(i == j) for j in range(n)] for i in range(n)])
controle("G4 |det AB| = 2^44 * %d^2" % PP, abs(detAB) == 2 ** 44 * PP ** 2)

# ------------------------------------------------------------------ G5 : les deux formes de rang 44
ALi = ALPHA + [Fr(0)] * (nh - len(ALPHA))
s = [sum(ALi[j] * tau[j + k] for j in range(nh)) / 2 for k in range(92)]   # Tr+(alpha c^k)
QA = [[s[i + j] for j in range(nh)] for i in range(nh)]
QB = [[4 * s[i + j] - s[i + j + 2] for j in range(nh)] for i in range(nh)]
Z0 = [[Fr(0)] * nh for _ in range(nh)]
DG = [QB[i] + Z0[i] for i in range(nh)] + [Z0[i] + QA[i] for i in range(nh)]
G5 = mm_(tr_(AB), mm_(DG, AB))
controle("G5 AB~ diag(QB, QA) AB / 2 = GRAM : N(z) = (Lambda(a) + Lambda'(b)) / 2 sur tout I", all(G5[i][j] == 2 * GRAM[i][j] for i in range(n) for j in range(n)))
from math import lcm
for nom, Qx in (("QA", QA), ("QB", QB)):
    Dq = lcm(*[x.denominator for r in Qx for x in r])
    dq, pq, _ = montante([[int(x * Dq) for x in r] for r in Qx], pivotage=False)
    controle("G5 %s (denominateur commun %d) definie positive, det = 1/%d^2" % (nom, Dq, PP), all(x > 0 for x in pq) and Fr(dq, Dq ** nh) == Fr(1, PP ** 2))

# ------------------------------------------------------------------ G6 : les deux côtés
JOURNAUX = {c: sorted(glob.glob(os.path.join(RACINE, "data", CAND, "replication", "cote%d.stdout.log" % c))
                    + glob.glob(os.path.join(RACINE, "data", CAND, "premiere_execution", "cote%d*.log" % c))) for c in (1, 2)}
def entrees_journal(f):
    mm = re.search(r"ENTREES SHA-256 : A (\w+) ; B (\w+) ; T (\w+) ; meta (\w+)", open(f, encoding="ascii", errors="replace").read())
    return list(mm.groups()) if mm else None
Mnu2 = [[2 * x for x in r] for r in Mnu]
BASES = {}
for cote in (1, 2):
    pre = os.path.join(DJ, "cote%d" % cote)
    for suf in ("_A.gram", "_B.gram", "_T.mat", "_meta.txt", "_bases.gp"):
        print("      SHA-256 %s  cote%d%s" % (sha(pre + suf), cote, suf))
    actuelles = [sha(pre + suf) for suf in ("_A.gram", "_B.gram", "_T.mat", "_meta.txt")]
    controle("G6 cote %d : les 4 empreintes d'entrees imprimees par chacun des %d journaux d'execution (%s) = fichiers actuels"
             % (cote, len(JOURNAUX[cote]), ", ".join(os.path.relpath(x, os.path.join(RACINE, "data", CAND)).replace(os.sep, "/") for x in JOURNAUX[cote])),
             len(JOURNAUX[cote]) >= 1 and all(entrees_journal(x) == actuelles for x in JOURNAUX[cote]))
    A = lire_java(pre + "_A.gram"); B = lire_java(pre + "_B.gram"); Tn = lire_java(pre + "_T.mat")
    DA, DB, d = [int(x) for x in open(pre + "_meta.txt").read().split()]
    bs = lire_gp(pre + "_bases.gp"); Hc = matint(bs["Hc"]); Hl = matint(bs["Hl"]); Hf = matint(bs["Hf"])
    BASES[cote] = (Hc, Hl, Hf)
    R = AB if cote == 1 else AB[nh:] + AB[:nh]            # lignes (fibre ; courte)
    QC, QF = (QA, QB) if cote == 1 else (QB, QA)
    Hbig = [Hf[i] + Hl[i] for i in range(nh)] + [[0] * nh + Hc[i] for i in range(nh)]
    detR, _, U = montante(R, Hbig)
    detH, _, _ = montante(Hbig)
    controle("G6 cote %d : R^-1 [[Hf, Hl], [0, Hc]] entiere et |det| egaux : meme reseau M (bijection I <-> (u, y) dans Z^44 x Z^44)" % cote,
             all(x.denominator == 1 for r in U for x in r) and abs(detR) == abs(detH))
    GC = mm_(tr_(Hc), mm_(QC, Hc)); GF = mm_(tr_(Hf), mm_(QF, Hf))
    controle("G6 cote %d : A.gram = DA Hc~ QC Hc (DA = %d)" % (cote, DA), all(DA * GC[i][j] == A[i][j] for i in range(nh) for j in range(nh)))
    controle("G6 cote %d : B.gram = DB Hf~ QF Hf (DB = %d)" % (cote, DB), all(DB * GF[i][j] == B[i][j] for i in range(nh) for j in range(nh)))
    HT = mm_(Hf, Tn)
    controle("G6 cote %d : Hf Tn = d Hl (d = %d) : coordonnees de fibre du relevement = Tn u / d" % (cote, d), all(HT[i][j] == d * Hl[i][j] for i in range(nh) for j in range(nh)))
    _, _, V = montante(Hf, Mnu2); detHf, _, _ = montante(Hf); det2nu, _, _ = montante(Mnu2)
    controle("G6 cote %d : reseau de fibre Hf Z^44 = 2 nu O+ (meme reseau colonne)" % cote, all(x.denominator == 1 for r in V for x in r) and abs(detHf) == abs(det2nu) == 2 ** 44 * PP ** 2)

# ------------------------------------------------------------------ G7 : seuil
controle("G7 (6 - 1057/200)^2 < 45/88, soit 6 (1 - sqrt(5/352)) < 1057/200 ; et 3*6/4 <= 1057/200", (6 - Fr(1057, 200)) ** 2 < Fr(45, 88) and Fr(18, 4) <= Fr(1057, 200))

# ------------------------------------------------------------------ G8 : lemmes sur des vecteurs (illustration exacte)
Zm = [[0] * n for _ in range(n)]
for j in range(n):
    v = redphi([0] * (j + 1) + [1])
    for i in range(n): Zm[i][j] = v[i]
Rot = mm_(Binv, mm_(Zm, BASE))
controle("G8 rotation zeta sur les coordonnees de I : matrice entiere, Rot~ GRAM Rot = GRAM", all(x.denominator == 1 for r in Rot for x in r) and mm_(tr_(Rot), mm_(GRAM, Rot)) == GRAM)
Rot = [[int(x) for x in r] for r in Rot]
random.seed(20261011); ok8 = True
for essai in range(3):
    x = [random.randint(-2, 2) if random.random() < 0.3 else 0 for _ in range(n)]
    if not any(x): x[0] = 1
    Nz = sum(x[i] * GRAM[i][j] * x[j] for i in range(n) for j in range(n))
    f = []; xk = x[:]
    for k in range(m):
        ba = [sum(AB[i][j] * xk[j] for j in range(n)) for i in range(n)]
        b_, a_ = ba[:nh], ba[nh:]
        La = sum(a_[i] * QA[i][j] * a_[j] for i in range(nh) for j in range(nh))
        Lb = sum(b_[i] * QB[i][j] * b_[j] for i in range(nh) for j in range(nh))
        ok8 &= (La + Lb == 2 * Nz); f.append(La - Nz)
        xk = [sum(Rot[i][j] * xk[j] for j in range(n)) for i in range(n)]
    ok8 &= xk == x and all(sum(f[(k + 23 * tt) % m] for tt in range(5)) == 0 for k in range(23))
    ok8 &= sum(v * v for v in f) * 88 >= 115 * Nz * Nz
    Mf = max(abs(v) for v in f); ok8 &= Mf * Mf * 352 >= 5 * Nz * Nz and all(abs(v) <= Nz for v in f)
    print("      vecteur %d : N = %d ; max |f| = %.4f >= N sqrt(5/352) = %.4f" % (essai, Nz, float(max(abs(v) for v in f)), Nz * (5 / 352) ** 0.5))
controle("G8 sur 3 vecteurs : Lambda(a_k) + Lambda'(b_k) = 2N, somme a cinq termes nulle, Parseval, max |f| >= N sqrt(5/352)", ok8)

# ------------------------------------------------------------------ G9 : vecteur de norme 8 (si fourni)
f8 = os.path.join(RACINE, "data", CAND, "norme8.txt")
if os.path.exists(f8):
    d8 = {}
    for l in open(f8, encoding="ascii"):
        if "=" in l: k, _, v = l.partition("="); d8[k.strip()] = v.strip()
    cote = int(d8["cote"]); u = [int(v) for v in d8["u"].strip("[]").split(",")]; y = [int(v) for v in d8["y"].strip("[]").split(",")]
    Hc, Hl, Hf = BASES[cote]
    fib = [sum(Hl[i][j] * u[j] + Hf[i][j] * y[j] for j in range(nh)) for i in range(nh)]
    crt = [sum(Hc[i][j] * u[j] for j in range(nh)) for i in range(nh)]
    ba = fib + crt if cote == 1 else crt + fib               # (b ; a)
    xx = [sum(ABinv[i][j] * ba[j] for j in range(n)) for i in range(n)]
    controle("G9 le point (u, y) fourni est dans I : coordonnees entieres dans BASE", all(v.denominator == 1 for v in xx))
    xx = [int(v) for v in xx]
    N8 = sum(xx[i] * GRAM[i][j] * xx[j] for i in range(n) for j in range(n))
    controle("G9 x~ GRAM x = 8 : vecteur de norme 8 exhibe (min <= 8)", N8 == 8)
    zz = [sum(BASE[i][j] * xx[j] for j in range(n)) for i in range(n)]
    print("      x (base de I) =", xx); print("      z (puissances de zeta, degre 0..87) =", zz)
else:
    print("      G9 : norme8.txt absent, controle non fait")
print("BILAN : %d controles, %d echecs" % (NB[0], NB[1]))
print("FIN_OK")
