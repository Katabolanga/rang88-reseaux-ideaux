# -*- coding: utf-8 -*-
"""verifier_conformite_article.py -- verification exacte (Python, entiers et rationnels, sans PARI/GP) de la CONFORMITE de la
matrice de Gram G de L_0 publiee par R. Sakamoto (fichier externe, data/L0/integer_input.txt de son depot) a la
construction tensorielle de l'article arXiv:2609.15633 v2, par. 5.4 (note, par. 2.5 : seconde identite Q G_art Q~ = G) :
    (L_0, B_0) = (E, h_4) (x)_{O_F} (J_0, h_11^(0)),   B_0 = Tr_{F/Q} o (h_4 (x) h_11^(0)).
Le script reconstruit B_0 a partir des SEULES constantes de l'article, ecrites en clair ci-dessous avec leur reference, en
n'utilisant que les deux petits corps F(zeta_5) (degre 4 sur F) et T = Q(zeta_23) (degre 11 sur F).
  Enonce verifie :  G[(i,j),(k,l)] == Tr_{F/Q}( h_4(p_i, p_k) * h_11^(0)(x''_j, x''_l) )   pour tous i, k = 1..4, j, l = 1..22,
      p_i : base de E (rem. 3.3 de l'article) ; x''_j = sum_l X[j][l] j_0 zeta_23^(l-1), X = matrice entiere de
      data/L0/certificat_conformite.txt, det X = +-1.  Autrement dit Q G_art Q~ == G avec Q = I_4 (x) X (det Q = 1).
  Controles annexes : Gram de h_4 == matrice de la rem. 3.3 ; p_i base de E sur O_F ; normes de delta_4, a, delta_11, j_0 ;
      G_art paire, det 1, definie positive ; M23~ == multiplication par zeta_23 sur le facteur J_0 ; chaine
      article -> fichier externe -> H avec data/L0/certificat_H_L0.txt : P G P~ == G_H et (P Q) G_art (P Q)~ == G_H.
Le fichier externe n'est lu qu'apres controle de son SHA-256 ; il est lu comme du TEXTE (entiers seulement), rien n'est execute.
Usage (depuis la racine du depot) : python -I code/verification/verifier_conformite_article.py [externe/integer_input.txt]"""
import sys, re
from fractions import Fraction as Fr
from math import comb, gcd

import os, hashlib
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SHA_SAKAMOTO = "68af477caf3f6d6a8980c40f234bcb47c0bac6caf3582c1757280cb64457631f"
f_gram = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RACINE, "externe", "integer_input.txt")
f_cert = os.path.join(RACINE, "data", "L0", "certificat_conformite.txt")
f_certL0 = os.path.join(RACINE, "data", "L0", "certificat_H_L0.txt")
N = 88
if not os.path.isfile(f_gram):
    raise SystemExit("ARRET : fichier externe absent (%s). Voir externe/LISEZMOI.md." % f_gram)
_h = hashlib.sha256()
with open(f_gram, "rb") as _fh:
    for _b in iter(lambda: _fh.read(1 << 16), b""): _h.update(_b)
print("fichier externe : SHA-256", _h.hexdigest())
if _h.hexdigest() != SHA_SAKAMOTO:
    raise SystemExit("ARRET : SHA-256 different de %s ; le fichier n'est pas lu." % SHA_SAKAMOTO)

# ---------------------------------------------------------------- lecture (texte, entiers seulement)
def lit_sakamoto(path):
    t = open(path, "rb").read().decode("ascii")
    assert re.fullmatch(r"[-0-9 \r\n]*", t), "caracteres inattendus"
    L = [l.split() for l in t.splitlines() if l.strip()]
    assert L[0] == ["88"] and len(L) == 1 + 3 * N and all(len(r) == N for r in L[1:])
    M = [[int(x) for x in r] for r in L[1:]]
    return M[:N], M[N:2 * N], M[2 * N:]

def lit_sections(path, noms):
    lignes = [l.strip() for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]
    sec, cur = {}, None
    for l in lignes:
        if l in noms or l == "FIN":
            cur = l; sec[cur] = []; continue
        assert re.fullmatch(r"[-0-9/ ]*", l), "caracteres inattendus dans " + path
        sec[cur].append(l)
    return sec

# ---------------------------------------------------------------- F = Q(sqrt(-23)) : (u, v) = u + v g
F0, F1, Fg = (Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(1))
def fadd(a, b): return (a[0] + b[0], a[1] + b[1])
def fneg(a): return (-a[0], -a[1])
def fmul(a, b): return (a[0] * b[0] - 23 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])
def fconj(a): return (a[0], -a[1])
def finv(a):
    d = a[0] * a[0] + 23 * a[1] * a[1]
    return (a[0] / d, -a[1] / d)
def fq(x): return (Fr(x), Fr(0))
def fnorm(a): return a[0] * a[0] + 23 * a[1] * a[1]          # N_{F/Q}
def ftr(a): return 2 * a[0]                                  # Tr_{F/Q}
def dans_OF(a): return (2 * a[1]).denominator == 1 and (a[0] - a[1]).denominator == 1     # O_F = Z + Z alpha
alpha = (Fr(1, 2), Fr(1, 2))

# ---------------------------------------------------------------- F(zeta_5) = F[t]/(1 + t + t^2 + t^3 + t^4) : 5 coefficients dans F (écriture cyclique)
def E(d): return [d.get(k, F0) for k in range(5)]
def eadd(a, b): return [fadd(x, y) for x, y in zip(a, b)]
def esc(c, a): return [fmul(c, x) for x in a]
def emul(a, b):
    c = [F0] * 5
    for i, x in enumerate(a):
        if x != F0:
            for j, y in enumerate(b):
                if y != F0: c[(i + j) % 5] = fadd(c[(i + j) % 5], fmul(x, y))
    return c
def esig(a, s):                                              # zeta_5 -> zeta_5^s, F fixe
    c = [F0] * 5
    for k in range(5): c[(k * s) % 5] = a[k]
    return c
def econj(a):                                                # conjugaison complexe de F(zeta_5)
    c = [F0] * 5
    for k in range(5): c[(-k) % 5] = fconj(a[k])
    return c
def ecanon(a): return [fadd(x, fneg(a[4])) for x in a]       # coefficient de t^4 ramené à 0
def e_versF(a):
    c = ecanon(a); assert c[1] == F0 and c[2] == F0 and c[3] == F0, "pas dans F"
    return c[0]
def e_trace(a):                                              # Tr_{F(zeta_5)/F}
    s = a
    for k in (2, 3, 4): s = eadd(s, esig(a, k))
    return e_versF(s)
def e_cofacteur(a): return emul(emul(esig(a, 2), esig(a, 3)), esig(a, 4))
def e_norme(a): return e_versF(emul(a, e_cofacteur(a)))      # N_{F(zeta_5)/F}
def einv(a): return esc(finv(e_norme(a)), e_cofacteur(a))

# ---------------------------------------------------------------- T = Q(zeta_23) : 23 coefficients rationnels (écriture cyclique)
QR = [q for q in range(1, 23) if pow(q, 11, 23) == 1]        # carrés modulo 23 = Gal(T/F)
def Tm(d): return [Fr(d.get(k, 0)) for k in range(23)]
def tadd(a, b): return [x + y for x, y in zip(a, b)]
def tsc(c, a): return [c * x for x in a]
def tmul(a, b):
    c = [Fr(0)] * 23
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y: c[(i + j) % 23] += x * y
    return c
def tsig(a, q):                                              # zeta_23 -> zeta_23^q
    c = [Fr(0)] * 23
    for k in range(23): c[(k * q) % 23] = a[k]
    return c
def tconj(a): return tsig(a, 22)
def tcanon(a): return [x - a[22] for x in a]
def tpow(k): return Tm({k % 23: 1})
gT = [Fr(0)] + [Fr(1 if k in QR else -1) for k in range(1, 23)]      # somme de Gauss = sqrt(-23)
def F_dansT(c): return tadd(Tm({0: c[0]}), tsc(c[1], gT))
def t_versF(a):
    # élément de F écrit dans T : A S_Q + B S_N (S_Q, S_N sommes des zeta^k sur les carrés / non-carrés) = -(A+B)/2 + (A-B)/2 g
    c0 = a[0]; A = a[1] - c0; B = a[5] - c0
    assert all(a[k] - c0 == (A if k in QR else B) for k in range(1, 23)), "pas dans F"
    return (-(A + B) / 2, (A - B) / 2)
def t_trace(a):                                              # Tr_{T/F}
    s = [Fr(0)] * 23
    for q in QR: s = tadd(s, tsig(a, q))
    return t_versF(s)
def t_cofacteur(a):
    c = Tm({0: 1})
    for q in QR:
        if q != 1: c = tmul(c, tsig(a, q))
    return c
def t_norme(a): return t_versF(tmul(a, t_cofacteur(a)))      # N_{T/F}
def tinv(a): return tmul(F_dansT(finv(t_norme(a))), t_cofacteur(a))
def t_eval47(a): return sum(int(x) * pow(21, k, 47) for k, x in enumerate(a)) % 47       # O_T -> O_T/J = F_47, zeta_23 -> 21

# ---------------------------------------------------------------- matrices entières
def bareiss(M):
    n = len(M); A = [list(r) for r in M]; sg = 1; prev = 1; mineurs = []; pur = True
    for k in range(n):
        if A[k][k] == 0:
            p = next((r for r in range(k + 1, n) if A[r][k] != 0), None)
            if p is None: return 0, None
            A[k], A[p] = A[p], A[k]; sg = -sg; pur = False
        piv = A[k][k]; mineurs.append(piv)
        for i in range(k + 1, n):
            aik = A[i][k]; Ai = A[i]; Ak = A[k]
            for j in range(k + 1, n): Ai[j] = (Ai[j] * piv - aik * Ak[j]) // prev
            Ai[k] = 0
        prev = piv
    return sg * A[n - 1][n - 1], (mineurs if pur else None)
def mul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(r, c)) for c in Bt] for r in A]
def tr(A): return [list(r) for r in zip(*A)]

# ================================================================ CONSTANTES DE L'ARTICLE (arXiv:2609.15633 v2)
t = lambda k: E({k % 5: F1})
# éq. (1), § 3.1 : delta_4 = (11 g (z - z^-1)(z + z^-1) - 2 g (z - z^-1) - 115 (z + z^-1) + 115) / 2,  z = zeta_5
zm = eadd(t(1), esc(fq(-1), t(4))); zp = eadd(t(1), t(4))
delta4 = esc(fq(Fr(1, 2)), eadd(eadd(esc(fmul(fq(11), Fg), emul(zm, zp)), esc(fmul(fq(-2), Fg), zm)), eadd(esc(fq(-115), zp), E({0: fq(115)}))))
# rem. 3.3 : base p_1..p_4 de E = O_{F(zeta_5)} sur O_F
al1 = fadd(F1, alpha)
p = [E({0: fadd(F1, fneg(alpha)), 1: alpha, 3: fq(-2)}),
     E({0: fq(-2), 1: fq(-2), 3: fq(-3)}),
     E({0: F1, 1: fq(-3), 3: fneg(al1)}),
     E({0: fneg(alpha), 2: fq(-1), 3: fneg(al1)})]
# rem. 3.3 : matrice de Gram de h_4 dans la base p_i
ig = finv(Fg); q4 = fmul(fq(4), ig); qa = fmul(alpha, ig); qb = fmul(fadd(alpha, fneg(F1)), ig)
A4 = [[F1, F0, q4, qa], [F0, F1, qb, q4], [fneg(q4), qa, F1, F0], [qb, fneg(q4), F0, F1]]
# début du § 4 : a = 13 - (z + z^-1) - 4 (z^2 + z^-2) - (z^3 + z^-3) + 6 (z^4 + z^-4) + 5 (z^5 + z^-5) - 5 (z^6 + z^-6)
#                    + 4 (z^8 + z^-8) + 3 (z^9 + z^-9) + (z^10 + z^-10),  z = zeta_23 ;  delta_11 = (2 - z - z^-1)^5
acf = {1: -1, 2: -4, 3: -1, 4: 6, 5: 5, 6: -5, 8: 4, 9: 3, 10: 1}
d = {0: 13}
for k, c in acf.items(): d[k] = c; d[23 - k] = c
a_ = Tm(d)
b1 = Tm({0: 2, 1: -1, 22: -1}); delta11 = b1
for _ in range(4): delta11 = tmul(delta11, b1)
# § 5.4 : J_0 = pbar J, J = (47, zeta_23 - 21), p = (2, alpha) ; J_0 = j_0 O_T, j_0 = 1 + z + z^4 + z^6 + z^8 + z^9 + z^12 + z^20 ;
#         h_11^(0)(u, v) = Tr_{T/F}((2 delta_11 a)^-1 u vbar)
j0 = Tm({k: 1 for k in (0, 1, 4, 6, 8, 9, 12, 20)})
# déf. 3.1 : h_4(u, v) = Tr_{F(zeta_5)/F}(delta_4^-1 u vbar) ; déf. 3.10, § 5.4 : h^(0) = h_4 (x) h_11^(0), B_0 = Tr_{F/Q} h^(0)

ok = True
def controle(texte, cond):
    global ok
    ok = ok and bool(cond)
    print("%s : %s" % (texte, bool(cond)))

# ---------------------------------------------------------------- 1. contrôles des constantes
n4 = e_norme(delta4)
controle("delta_4 reel, N_{F(zeta_5)/Q}(delta_4) = 5^6 23^4 (= |disc F(zeta_5)|)", ecanon(econj(delta4)) == ecanon(delta4) and fnorm(n4) == 5**6 * 23**4)
# déterminant (sur O_F) des p_i dans la base 1, t, t^2, t^3
def det4(M):
    from itertools import permutations
    s = F0
    for pm in permutations(range(4)):
        sg = 1
        for i in range(4):
            for j in range(i + 1, 4):
                if pm[i] > pm[j]: sg = -sg
        tm = fq(sg)
        for i in range(4): tm = fmul(tm, M[i][pm[i]])
        s = fadd(s, tm)
    return s
dp = det4([[x for x in ecanon(pi)[:4]] for pi in p])
controle("p_1..p_4 : coefficients dans O_F, det dans la base 1, zeta_5, zeta_5^2, zeta_5^3 = unite de O_F (det = %s + %s g)" % dp,
         all(dans_OF(x) for pi in p for x in ecanon(pi)) and dans_OF(dp) and fnorm(dp) == 1)
d4i = einv(delta4)
H4 = [[e_trace(emul(d4i, emul(p[i], econj(p[k])))) for k in range(4)] for i in range(4)]
controle("Gram de h_4 dans la base p_i == matrice de la rem. 3.3", H4 == A4)
na, nd, nj = t_norme(a_), t_norme(delta11), t_norme(j0)
controle("a reel, a(21) = 0 mod 47, N_{T/Q}(a) = 47^2  (=> a O_T = J Jbar)", tcanon(tconj(a_)) == tcanon(a_) and t_eval47(a_) == 0 and fnorm(na) == 47**2)
controle("N_{T/Q}(delta_11) = 23^10 (norme de la differente de T/F)", fnorm(nd) == 23**10)
alT = F_dansT(alpha)
ja = tcanon(tmul(j0, alT)); jb = tcanon(tmul(j0, tconj(alT)))
controle("j_0(21) = 0 mod 47, N_{T/Q}(j_0) = 2^11 47, j_0 alpha dans 2 O_T, j_0 alphabar hors de 2 O_T  (=> j_0 O_T = pbar J = J_0)",
         t_eval47(j0) == 0 and fnorm(nj) == 2**11 * 47 and all(x.denominator == 1 and x % 2 == 0 for x in ja) and not all(x % 2 == 0 for x in jb))

# ---------------------------------------------------------------- 2. h_11^(0) sur la base j_0 zeta_23^(l-1), puis G_art
c0 = tmul(tmul(j0, tconj(j0)), tinv(tsc(Fr(2), tmul(delta11, a_))))
hd = {dd: t_trace(tmul(c0, tpow(dd))) for dd in range(-21, 22)}
controle("h_11^(0)(j_0 z^j, j_0 z^l) dans O_F, hermitienne", all(dans_OF(v) for v in hd.values()) and all(hd[-dd] == fconj(hd[dd]) for dd in hd))
U = [[hd[j - l][0] for l in range(22)] for j in range(22)]
V = [[hd[j - l][1] for l in range(22)] for j in range(22)]
def gram88(Hu, Hv):
    Gm = [[None] * N for _ in range(N)]
    for i in range(4):
        for k in range(4):
            cu, cv = H4[i][k]
            for j in range(22):
                for l in range(22):
                    x = 2 * (cu * Hu[j][l] - 23 * cv * Hv[j][l])          # Tr_{F/Q}((cu + cv g)(Hu + Hv g))
                    assert x.denominator == 1
                    Gm[22 * i + j][22 * k + l] = int(x)
    return Gm
Gart = gram88(U, V)
dA, mnA = bareiss(Gart)
controle("G_art (base p_i (x) j_0 zeta_23^(j-1)) : entiere, symetrique, paire, det 1, definie positive (det = %s, diagonale %s)" % (dA, Gart[0][0]),
         Gart == tr(Gart) and all(Gart[i][i] % 2 == 0 for i in range(N)) and dA == 1 and mnA is not None and all(x > 0 for x in mnA))

# ---------------------------------------------------------------- 3. le dépôt
G, M5, M23 = lit_sakamoto(f_gram)
sec = lit_sections(f_cert, ("X",))
X = [[int(x) for x in r.split()] for r in sec["X"]]
assert len(X) == 22 and all(len(r) == 22 for r in X)
dX, _ = bareiss(X)
controle("X entiere 22 x 22, det X = +-1 (det = %s, max |X_jl| = %d)" % (dX, max(abs(x) for r in X for x in r)), abs(dX) == 1)
Xf = [[Fr(x) for x in r] for r in X]
Hu = mul(mul(Xf, U), tr(Xf)); Hv = mul(mul(Xf, V), tr(Xf))
Grec = gram88(Hu, Hv)
controle("PRINCIPAL : G (depot, integer_input.txt) == (Tr_{F/Q}(h_4(p_i, p_k) h_11^(0)(x''_j, x''_l))), x''_j = sum_l X[j][l] j_0 zeta_23^(l-1)", Grec == G)
Q = [[X[r % 22][s % 22] if r // 22 == s // 22 else 0 for s in range(N)] for r in range(N)]
controle("Q = I_4 (x) X : Q G_art Q~ == G", mul(mul(Q, Gart), tr(Q)) == G)
# multiplication par zeta_23 dans la base zeta_23^(l-1), l = 1..22 (vecteurs lignes) : zeta^21 . zeta = -(1 + ... + zeta^21)
Z23 = [[int(l == j + 1) for l in range(22)] for j in range(21)] + [[-1] * 22]
Zb = [[Z23[r % 22][s % 22] if r // 22 == s // 22 else 0 for s in range(N)] for r in range(N)]
controle("M23~ (depot) == multiplication par zeta_23 sur le facteur J_0 : M23~ Q == Q (I_4 (x) Z23)", mul(tr(M23), Q) == mul(Q, Zb))

# ---------------------------------------------------------------- 4. chaîne article -> dépôt -> H (facultatif)
if f_certL0:
    s2 = lit_sections(f_certL0, ("P", "beta", "a"))
    P = [[int(x) for x in r.split()] for r in s2["P"]]
    beta = [Fr(x) for x in " ".join(s2["beta"]).split()]
    assert len(P) == N and all(len(r) == N for r in P) and len(beta) == N // 2
    def mobius(k):
        r, q = 1, 2
        while q * q <= k:
            if k % q == 0:
                k //= q
                if k % q == 0: return 0
                r = -r
            q += 1
        return -r if k > 1 else r
    def ramanujan(Nn, s):
        gg = gcd(Nn, s % Nn) if s % Nn else Nn
        return sum(mobius(Nn // dd) * dd for dd in range(1, gg + 1) if gg % dd == 0)
    tb = []
    for r in range(115):
        s = Fr(0)
        for k, gk in enumerate(beta):
            if gk: s += gk * sum(comb(k, tt) * ramanujan(115, k - 2 * tt + r) for tt in range(k + 1))
        tb.append(s)
    assert all(x.denominator == 1 for x in tb)
    GH = [[int(tb[(i - j) % 115]) for j in range(N)] for i in range(N)]
    PQ = mul(P, Q); dPQ, _ = bareiss(PQ)
    controle("chaine : P G P~ == G_H (certificat_H_L0) et (P Q) G_art (P Q)~ == G_H, det(P Q) = %s" % dPQ,
             mul(mul(P, G), tr(P)) == GH and mul(mul(PQ, Gart), tr(PQ)) == GH and abs(dPQ) == 1)

print("RESULTAT (Python, exact) : la Gram du depot de Sakamoto (L_0) est la Gram de B_0 = Tr_{F/Q}(h_4 (x) h_11^(0)) de l'article dans la base p_i (x) x''_j : %s"
      % ("VALIDE" if ok else "INVALIDE"))
sys.exit(0 if ok else 1)
