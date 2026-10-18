# -*- coding: utf-8 -*-
"""verifier_temoins_norme6.py -- second controle, SANS PARI/GP, des cinq temoins de norme 6 de l'addendum (version 1.2) :
les quatre rejets des filtres du par. 4.5 (tableau 4) et le temoin de la proposition 4.6 (I = P691 s24(P691), jumeau de X4969).

Les fichiers temoin_<NOM>.gp de ce dossier sont lus comme du TEXTE par une grammaire limitee (polynomes a coefficients
rationnels, matrices et vecteurs d'entiers, chaines) ; rien n'est evalue ni execute.  Bibliotheque standard seulement ;
arithmetique exacte sur les entiers et les rationnels.  Liste FIGEE des cibles (ideaux, cotes et energies imprimes dans
l'addendum).  Memes controles, numerotes de meme, que verifier_temoins_norme6.gp :
  A1  NOM, PREMIERS, NORME_ABS_I, NORME, COTES et le nombre de temoins sont ceux de la cible ;
  A2  l'ideal : forme (B) [[p, r1], [p, r2]] : p premier (divisions d'essai), 0 < r1 != r2 < p, Phi_115(r1) = Phi_115(r2) = 0
      mod p, r2 = r1^24 mod p, GEN = (y - r1)(y - r2) mod p ; forme (A) [[p, 2, k]] : p premier d'ordre 2 modulo 115, GEN
      unitaire de degre 2, irreductible mod p (discriminant non carre, critere d'Euler), divisant Phi_115 mod p ;
  A3  la base C de I construite ICI (colonnes p, p zeta, GEN(zeta) zeta^j, 0 <= j <= 85 ; triangulaire, |det C| = p^2) ;
      un vecteur z est dans le Z-module engendre si et seulement si le reste de la division de z par GEN (unitaire) a ses
      deux coefficients divisibles par p ; le module est stable par zeta (88 controles reduits modulo Phi_115), contient p et
      GEN(zeta), et est contenu dans (p, GEN(zeta)) : il est egal a I ;
  B1  PM et BETA0 sont lus dans data/corps/rang88_m115c0_data.txt ; PM(zeta + 1/zeta) = 0 ; ALPHA * NU = BETA0 dans Q[x]/PM ;
  B2-B4  G = C~ H C, H[i, j] = Tr_{L/Q}(alpha zeta^(i-j)) (sommes de Ramanujan), est entiere, symetrique, paire, de
      determinant 1 et definie positive (88 mineurs principaux > 0, elimination de Bareiss sans pivot) ;
  C1  pour chaque temoin z : z entier non nul, dans I, coordonnees w entieres et w~ G w = 6 ;
  C2  Tr_{L/Q}(alpha z zbar) = 6, calcule dans Q[t]/(t^115 - 1), sans aucune base ;
  C3  avec f = Tr_{L/Q}(alpha z^2) : (courte, fibre) = (6 + f, 6 - f) au cote 1, (6 - f, 6 + f) au cote 2 (note, lemme 4.2
      et prop. 4.1 (c)) ; ce sont les energies imprimees dans l'addendum ;
  D1-D3  provenance : BASE entiere, |det BASE| = p^2, colonnes dans I ; GRAM = BASE~ H BASE ; Z = BASE X, X~ GRAM X = 6 ;
et en plus :
  E1  pour chaque temoin, la ligne « x = [...] » du journal d'audit du 17 octobre 2026 (filtres_nuit_20261017/ ou
      prop46_P691s24_execution/) est egale, entier pour entier, a la colonne correspondante de X.
Verdict : nombre complet de controles (9 + 5 x nombre de temoins par fichier, 75 en tout) et aucun echec ; code de
sortie 0 si et seulement si tout passe.
Usage (depuis la racine du depot ; une a deux minutes) :  python3 -I addendum/temoins_norme6/verifier_temoins_norme6.py"""
import hashlib, os, re, sys
from fractions import Fraction as Fr
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.normpath(os.path.join(ICI, "..", ".."))
n, m = 88, 115
CIBLES = [  # (nom, PREMIERS, [(energie courte, energie de fibre, cote)], journal d'audit du 17 octobre)
    ("P2531s24", [[2531, 12], [2531, 483]], [(Fr(11913, 2531), Fr(186878916, 5062 ** 2), 2)],
     "filtres_nuit_20261017/temoin_P2531s24.audit_20261017_044917.log"),
    ("P5981s24", [[5981, 16], [5981, 5092]], [(Fr(28185, 5981), Fr(1042775388, 11962 ** 2), 1)],
     "filtres_nuit_20261017/temoin_P5981s24.audit_20261017_044917.log"),
    ("P18401s24", [[18401, 22], [18401, 8441]], [(Fr(85506, 18401), Fr(9959062824, 36802 ** 2), 1)],
     "filtres_nuit_20261017/temoin_P18401s24.audit_20261017_044917.log"),
    ("P39239", [[39239, 2, 1]], [(Fr(164472, 39239), Fr(48090690576, 78478 ** 2), 2)],
     "filtres_nuit_20261017/temoin_P39239.audit_20261017_044917.log"),
    ("P691s24", [[691, 4], [691, 596]], [(Fr(3542, 691), Fr(13129000, 1382 ** 2), 1), (Fr(2406, 691), Fr(16268904, 1382 ** 2), 2)],
     "prop46_P691s24_execution/temoin_P691s24.log"),
]

# ---------------------------------------------------------------- lecture (texte seulement)
def lire_affectations(f):
    t = open(f, encoding="ascii").read()
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)          # commentaires d'en-tete
    d = {}
    for mm in re.finditer(r"^([A-Z][A-Z_0-9]*) = (.*?);[ \t]*$", t, re.M):
        assert mm.group(1) not in d, "affectation en double"
        d[mm.group(1)] = mm.group(2)
    return d
def poly(s, var):
    s = s.replace(" ", "")
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
    s = s.strip(); assert s[0] == "[" and s[-1] == "]" and re.fullmatch(r"[-0-9,; ]*", s[1:-1]), "matrice inattendue"
    M = [[int(t) for t in row.split(",")] for row in s[1:-1].split(";")]
    assert len(set(len(r) for r in M)) == 1, "lignes de longueurs differentes"
    return M
def listes_int(s):   # [[a, b], [c, d, e]] ou [a, b]
    s = s.strip(); assert re.fullmatch(r"[\[\]0-9, -]+", s), "liste inattendue"
    return eval_liste(s)
def eval_liste(s):
    pile = [[]]; nombre = ""
    for ch in s:
        if ch == "[": pile.append([])
        elif ch in ",]":
            if nombre.strip(): pile[-1].append(int(nombre)); nombre = ""
            if ch == "]": x = pile.pop(); pile[-1].append(x)
        elif ch != " ": nombre += ch
    assert len(pile) == 1 and len(pile[0]) == 1 and not nombre.strip()
    return pile[0][0]

# ---------------------------------------------------------------- arithmetique exacte
def bareiss(A, pivotage=True):
    """determinant et pivots (mineurs principaux successifs si aucun echange) d'une matrice entiere carree"""
    M = [list(map(int, r)) for r in A]; N = len(M); prev = 1; piv = []; signe = 1
    for k in range(N):
        if M[k][k] == 0:
            if not pivotage: return 0, piv + [0]
            l = next((i for i in range(k + 1, N) if M[i][k] != 0), None)
            if l is None: return 0, piv + [0]
            M[k], M[l] = M[l], M[k]; signe = -signe
        pk = M[k][k]; piv.append(pk)
        for i in range(k + 1, N):
            f = M[i][k]
            if f == 0:
                M[i] = [v * pk // prev for v in M[i]]; continue
            Mi, Mk = M[i], M[k]
            nv = [pk * Mi[j] - f * Mk[j] for j in range(N)]
            M[i] = [v // prev for v in nv]
        prev = pk
    return signe * piv[-1], piv
def polmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i + j] += x * y
    return r
def poldivex(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        q[i] = a[i + len(b) - 1]
        for j, y in enumerate(b): a[i + j] -= q[i] * y
    assert not any(a); return q
ym = lambda k: [-1] + [0] * (k - 1) + [1]
PHI = poldivex(polmul(ym(115), ym(1)), polmul(ym(5), ym(23)))     # Phi_115, degre 88, unitaire
assert len(PHI) == n + 1 and PHI[-1] == 1
def redphi(a):
    a = list(a) + [0] * max(0, m - len(a))
    for i in range(len(a) - 1, n - 1, -1):
        c = a[i]
        if c:
            for j, y in enumerate(PHI): a[i - n + j] -= c * y
    return a[:n]
def mulc(a, b):   # produit dans Q[t]/(t^115 - 1)
    r = [0] * m
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y: r[(i + j) % m] += x * y
    return r
def ram(k):   # Tr_{L/Q}(zeta^k) : somme de Ramanujan c_115(k)
    k %= m
    if k == 0: return 88
    if k % 23 == 0: return -22
    if k % 5 == 0: return -4
    return 1
def trace(v): return sum(c * ram(r) for r, c in enumerate(v) if c)
cc = [0] * m; cc[1] = 1; cc[114] = 1
cp = [[1] + [0] * (m - 1)]
for k in range(1, 45): cp.append(mulc(cp[-1], cc))
def plonge(pl):   # polynome en c = zeta + 1/zeta  ->  element de Q[t]/(t^115 - 1)
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
def est_premier(p):
    if p < 2: return False
    k = 2
    while k * k <= p:
        if p % k == 0: return False
        k += 1
    return True
def reste_mod(a, g, p):   # reste de a par g (unitaire) dans F_p[y]
    a = [x % p for x in a]
    for i in range(len(a) - 1, len(g) - 2, -1):
        c = a[i]
        if c:
            for j, y in enumerate(g): a[i - len(g) + 1 + j] = (a[i - len(g) + 1 + j] - c * y) % p
    return a[:len(g) - 1]
def coord_C(z, g, p):
    """coordonnees de z (88 entiers) dans la base C = (p, p y, g, y g, ..., y^85 g), ou None si z n'est pas dans le module"""
    a = list(z); q = [0] * (n - 2)
    for i in range(n - 1, 1, -1):          # division euclidienne par g unitaire de degre 2, sur Z
        c = a[i]; q[i - 2] = c
        if c:
            a[i - 2] -= c * g[0]; a[i - 1] -= c * g[1]; a[i] -= c
    r0, r1 = a[0], a[1]
    if r0 % p or r1 % p: return None
    return [r0 // p, r1 // p] + q

# ---------------------------------------------------------------- donnees du corps
DAT = open(os.path.join(RACINE, "data", "corps", "rang88_m115c0_data.txt"), encoding="ascii").read().strip()
assert DAT[0] == "[" and DAT[-1] == "]"
parts = DAT[1:-1].split(",", 2)
PMc = poly(parts[0], "x"); B0c = poly(parts[1], "x")
acc = [0] * m
for k, c in enumerate(PMc): acc = [x + int(c) * y for x, y in zip(acc, cp[k])]
PM_OK = len(PMc) == 45 and PMc[44] == 1 and not any(redphi(acc))    # PM(zeta + 1/zeta) = 0 et PM unitaire de degre 44
pad = lambda v: v + [Fr(0)] * (44 - len(v))

NB = [0, 0]; NATT = 0; NVAL = 0
def chk(c, s):
    NB[0] += 1; NB[1] += bool(c)
    print("%s %s" % ("OK   " if c else "ECHEC", s)); sys.stdout.flush()
    return bool(c)

for nom, PRatt, energies, journal in CIBLES:
    nt = len(energies); NATT += 9 + 5 * nt; nb0 = list(NB)
    f = os.path.join(ICI, "temoin_%s.gp" % nom)
    print("== %s (%s, SHA-256 %s)" % (nom, os.path.relpath(f, RACINE).replace(os.sep, "/"), hashlib.sha256(open(f, "rb").read()).hexdigest()))
    try:
        d = lire_affectations(f)
        p = PRatt[0][0]
        PR = listes_int(d["PREMIERS"]); CO = listes_int(d["COTES"])
        X = matint(d["X"]); Z = matint(d["Z"]); BASE = matint(d["BASE"]); GRAM = matint(d["GRAM"])
        GEN = [int(c) for c in poly(d["GEN"], "y")]
        NU = poly(d["NU"], "x"); ALPHA = poly(d["ALPHA"], "x")
        lu = True
    except Exception as e:
        print("ECHEC lecture de %s : %r" % (f, e)); lu = False
    if not lu:
        continue
    # A1
    chk(d["NOM"] == '"%s"' % nom and PR == PRatt and int(d["NORME_ABS_I"]) == p * p and int(d["NORME"]) == 6
        and CO == [e[2] for e in energies] and len(Z) == n and len(Z[0]) == nt and len(X) == n and len(X[0]) == nt,
        "%s A1 : NOM, PREMIERS = %s, NORME_ABS_I = p^2, NORME = 6, COTES = %s, %d temoin(s)" % (nom, PRatt, CO, nt))
    # A2
    if len(PR) == 2:
        r1, r2 = PR[0][1], PR[1][1]
        okA2 = (len(PR[0]) == 2 and len(PR[1]) == 2 and PR[1][0] == p and est_premier(p) and 0 < r1 < p and 0 < r2 < p and r1 != r2
                and sum(c * pow(r1, i, p) for i, c in enumerate(PHI)) % p == 0 and sum(c * pow(r2, i, p) for i, c in enumerate(PHI)) % p == 0
                and pow(r1, 24, p) == r2 and GEN == [r1 * r2 % p, (-(r1 + r2)) % p, 1])
        txt = "= P sigma_24(P), P = (%d, zeta - %d) de degre 1" % (p, r1)
    else:
        disc = (GEN[1] * GEN[1] - 4 * GEN[0]) % p if len(GEN) == 3 else 0
        okA2 = (len(PR) == 1 and len(PR[0]) == 3 and PR[0][1] == 2 and est_premier(p) and p * p % m == 1 and p % m != 1
                and len(GEN) == 3 and GEN[2] == 1 and all(0 <= c < p for c in GEN) and p % 2 == 1 and pow(disc, (p - 1) // 2, p) == p - 1
                and not any(reste_mod(PHI, GEN, p)))
        txt = "est un premier de degre 2 au-dessus de %d" % p
    chk(okA2, "%s A2 : I = (%d, %s) %s" % (nom, p, d["GEN"], txt))
    # A3 : la base C ; stabilite par zeta
    colsC = [[p] + [0] * (n - 1), [0, p] + [0] * (n - 2)] + [[0] * j + GEN + [0] * (n - 3 - j) for j in range(n - 2)]
    def dans_I(z): return coord_C(z, GEN, p) is not None
    stable = all(dans_I(redphi([0] + c)) for c in colsC)
    chk(all(len(c) == n for c in colsC) and stable and all(dans_I(c) for c in colsC),
        "%s A3 : base C (p, p zeta, GEN zeta^j), triangulaire, |det C| = p^2 ; le module engendre est stable par zeta : C engendre I" % nom)
    # B1
    chk(PM_OK and len(ALPHA) <= 44 and len(NU) <= 44 and mulmod(pad(ALPHA), pad(NU), PMc) == pad(B0c),
        "%s B1 : PM et BETA0 lus dans data/corps, PM(zeta + 1/zeta) = 0, ALPHA * NU = BETA0 dans Q[x]/PM" % nom)
    # B2-B4 : Gram de I dans C, depuis ALPHA seul
    al = plonge(ALPHA)
    t = [sum(al[i] * ram(i + k) for i in range(m) if al[i]) for k in range(m)]
    def forme(u, v):   # Tr(alpha u vbar), u, v listes creuses (indice, coefficient)
        return sum(cu * cv * t[(a - b) % m] for a, cu in u for b, cv in v)
    sp = [[(i, c) for i, c in enumerate(col) if c] for col in colsC]
    G = [[forme(sp[i], sp[j]) for j in range(n)] for i in range(n)]
    entiere = all(x.denominator == 1 for r in G for x in r)
    chk(entiere and all(G[i][j] == G[j][i] for i in range(n) for j in range(n)) and all(G[i][i] % 2 == 0 for i in range(n)),
        "%s B2 : Gram G = C~ H C (depuis ALPHA seul) entiere, symetrique, paire" % nom)
    Gi = [[int(x) for x in r] for r in G] if entiere else None
    detG, pivG = bareiss(Gi, pivotage=False) if entiere else (0, [0])
    chk(entiere and detG == 1, "%s B3 : det G = 1" % nom)
    chk(entiere and len(pivG) == n and all(x > 0 for x in pivG), "%s B4 : G definie positive (88 mineurs principaux > 0)" % nom)
    # C1-C3 et E1
    xs_journal = [[int(v) for v in mm.group(1).split(",")] for mm in re.finditer(r"^\s*x = \[([-0-9, ]+)\]\s*$",
                  open(os.path.join(ICI, journal), encoding="utf-8", errors="replace").read(), re.M)]
    for k in range(nt):
        z = [Z[i][k] for i in range(n)]; w = coord_C(z, GEN, p)
        N6 = sum(w[i] * Gi[i][j] * w[j] for i in range(n) if w[i] for j in range(n) if w[j]) if (w is not None and Gi) else None
        chk(any(z) and w is not None and N6 == 6,
            "%s C1, temoin %d : z entier non nul, dans I (coordonnees entieres dans C), w~ G w = %s" % (nom, k + 1, N6))
        zc = z + [0] * (m - n); zb = [0] * m
        for i, c in enumerate(zc): zb[(-i) % m] += c
        tz = trace(mulc(al, mulc(zc, zb)))
        chk(tz == 6, "%s C2, temoin %d : Tr(alpha z zbar) = %s (sans base)" % (nom, k + 1, tz))
        fz = trace(mulc(al, mulc(zc, zc)))
        ea, eb, cote = energies[k]
        bon = (6 + fz == ea and 6 - fz == eb) if cote == 1 else (6 - fz == ea and 6 + fz == eb)
        chk(ea + eb == 12 and CO[k] == cote and bon,
            "%s C3, temoin %d (cote %d) : energies courte %s et de fibre %s retrouvees (f = Tr(alpha z^2) = %s)" % (nom, k + 1, cote, ea, eb, fz))
        chk(len(xs_journal) == nt and xs_journal[k] == [X[i][k] for i in range(n)],
            "%s E1, temoin %d : X = ligne « x = [...] » du journal du 17 octobre (%s)" % (nom, k + 1, journal))
    # D1-D3 : provenance (base du preparateur)
    detB, _ = bareiss(BASE)
    chk(len(BASE) == n and len(BASE[0]) == n and abs(detB) == p * p and all(dans_I([BASE[i][j] for i in range(n)]) for j in range(n)),
        "%s D1 : BASE entiere, |det BASE| = p^2, colonnes dans I (BASE engendre I)" % nom)
    den = 1
    for x in t: den = den * x.denominator // __import__("math").gcd(den, x.denominator)
    ti = [int(x * den) for x in t]                                   # H = Hs / den, Hs entiere
    HB = [[sum(ti[(a - b) % m] * BASE[b][j] for b in range(n) if BASE[b][j]) for j in range(n)] for a in range(n)]
    BtHB = [[sum(BASE[a][i] * HB[a][j] for a in range(n) if BASE[a][i]) for j in range(n)] for i in range(n)]
    chk(all(BtHB[i][j] == GRAM[i][j] * den for i in range(n) for j in range(n)),
        "%s D2 : GRAM du fichier = BASE~ H BASE" % nom)
    for k in range(nt):
        xk = [X[i][k] for i in range(n)]
        chk(any(xk) and [sum(BASE[i][j] * xk[j] for j in range(n)) for i in range(n)] == [Z[i][k] for i in range(n)]
            and sum(xk[i] * GRAM[i][j] * xk[j] for i in range(n) if xk[i] for j in range(n) if xk[j]) == 6,
            "%s D3, temoin %d : Z = BASE X et X~ GRAM X = 6" % (nom, k + 1))
    valide = (NB[0] - nb0[0] == 9 + 5 * nt) and (NB[1] - nb0[1] == NB[0] - nb0[0])
    NVAL += valide
    print("   %s : %s" % (nom, "TEMOIN VALIDE (reseau pair unimodulaire de rang 88 avec un vecteur de norme 6 : NON extremal)" if valide else "ECHEC"))
print("BILAN : %d controles (attendus %d), %d echecs ; %d temoins valides sur %d fichiers" % (NB[0], NATT, NB[0] - NB[1], NVAL, len(CIBLES)))
verdict = NB[0] == NATT == 75 and NB[1] == NB[0] and NVAL == len(CIBLES)
print("TEMOINS_NORME6_VERIFIES_SANS_PARI" if verdict else "TEMOINS_NORME6_ECHEC")
sys.exit(0 if verdict else 1)
