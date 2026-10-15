# -*- coding: utf-8 -*-
"""verifier_H_L0.py -- verification exacte (Python, entiers et rationnels, sans PARI/GP) du certificat d'isometrie
    H = (O_L, Tr_L(beta_0 z zbar)) ~= L_0 (R. Sakamoto, arXiv:2609.15633 v2),  L = Q(zeta_115)      (note, par. 2.5).

Le fichier de Sakamoto N'EST PAS dans ce depot.  L'utilisateur le telecharge lui-meme (voir externe/LISEZMOI.md) et le
place en externe/integer_input.txt.  AVANT TOUTE LECTURE de son contenu, le script calcule son SHA-256 et refuse de
continuer s'il differe de 68af477caf3f6d6a8980c40f234bcb47c0bac6caf3582c1757280cb64457631f (revision 628ce2a7 du depot
de l'auteur, fichier data/L0/integer_input.txt).  Le fichier est ensuite lu comme du TEXTE : seuls des entiers sont
acceptes, rien n'est execute.  Il contient « 88 » puis trois matrices 88 x 88 : la Gram G de L_0, puis M5 et M23.

Controles :
  - G est symetrique, paire, de determinant 1, definie positive ;
  - G_H = (Tr_L(beta zeta^(i-j))), beta = sum g_k c^k (certificat), est recalculee sans GP par les sommes de Ramanujan :
      Tr_L(beta zeta^r) = sum_k g_k sum_t C(k, t) c_115(k - 2t + r) ; G_H paire, de determinant 1, definie positive ;
  - beta du certificat = beta_0 de data/corps/rang88_m115c0_data.txt ;
  - P (certificat) entiere, det P = +-1 (Bareiss), P G P~ = G_H : c'est l'isometrie ;
  - TX := (M5 M23)~ (recalcule a partir du fichier de Sakamoto, non stocke ici) : TX G TX~ = G, TX^115 = 1, TX^5 != 1,
    TX^23 != 1, et P TX^a = Z P (Z = multiplication par zeta dans la base zeta^(i-1)) : P entrelace TX^a et zeta.
Usage (depuis la racine du depot) : python -I code/verification/verifier_H_L0.py [externe/integer_input.txt]   (environ 1 min)"""
import sys, re, os, hashlib
from fractions import Fraction
from math import comb, gcd
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SHA_SAKAMOTO = "68af477caf3f6d6a8980c40f234bcb47c0bac6caf3582c1757280cb64457631f"
f_gram = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RACINE, "externe", "integer_input.txt")
cert_txt = os.path.join(RACINE, "data", "L0", "certificat_H_L0.txt")
f_corps = os.path.join(RACINE, "data", "corps", "rang88_m115c0_data.txt")
N, m = 88, 115

# ---------------------------------------------------------------- 0. empreinte du fichier externe, avant toute lecture
if not os.path.isfile(f_gram):
    raise SystemExit("ARRET : fichier externe absent (%s). Voir externe/LISEZMOI.md." % f_gram)
h = hashlib.sha256()
with open(f_gram, "rb") as fh:
    for bloc in iter(lambda: fh.read(1 << 16), b""): h.update(bloc)
print("fichier externe : SHA-256", h.hexdigest())
if h.hexdigest() != SHA_SAKAMOTO:
    raise SystemExit("ARRET : SHA-256 different de %s ; le fichier n'est pas lu." % SHA_SAKAMOTO)
print("fichier externe : empreinte conforme (revision 628ce2a7, data/L0/integer_input.txt) ; lecture comme texte")

def lit_sakamoto(path):
    t = open(path, "rb").read().decode("ascii")
    assert re.fullmatch(r"[-0-9 \r\n]*", t), "caracteres inattendus"
    L = [l.split() for l in t.splitlines() if l.strip()]
    assert L[0] == ["88"] and len(L) == 1 + 3 * N and all(len(r) == N for r in L[1:])
    M = [[int(x) for x in r] for r in L[1:]]
    return M[:N], M[N:2 * N], M[2 * N:]
def lit_txt(path):
    lignes = [l.strip() for l in open(path, encoding="ascii") if l.strip() and not l.startswith("#")]
    sec, cur = {}, None
    for l in lignes:
        if l in ("P", "beta", "a", "FIN"):
            cur = l; sec[cur] = []; continue
        assert re.fullmatch(r"[-0-9/ ]*", l), "caracteres inattendus dans le certificat"
        sec[cur].append(l)
    P = [[int(t) for t in r.split()] for r in sec["P"]]
    return P, [Fraction(t) for t in " ".join(sec["beta"]).split()], int(sec["a"][0])
def beta0_corps(path):
    t = open(path, encoding="ascii").read().strip()
    s = t[1:-1].split(",", 2)[1].replace(" ", "").replace("\n", "")
    assert re.fullmatch(r"[-+*/^x0-9]*", s)
    c = [Fraction(0)] * (N // 2)
    for sg, num, x, e in re.findall(r"([+-]?)(\d+(?:/\d+)?)?\*?(x?)(?:\^(\d+))?", s):
        if not num and not x: continue
        v = Fraction(num) if num else Fraction(1)
        k = (int(e) if e else 1) if x else 0
        c[k] += -v if sg == "-" else v
    return c
def mobius(k):
    r, p = 1, 2
    while p * p <= k:
        if k % p == 0:
            k //= p
            if k % p == 0: return 0
            r = -r
        p += 1
    return -r if k > 1 else r
def ramanujan(Nn, s):
    g = gcd(Nn, s % Nn) if s % Nn else Nn
    return sum(mobius(Nn // d) * d for d in range(1, g + 1) if g % d == 0)
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
            for j in range(k + 1, n):
                Ai[j] = (Ai[j] * piv - aik * Ak[j]) // prev
            Ai[k] = 0
        prev = piv
    return sg * A[n - 1][n - 1], (mineurs if pur else None)
def posdef(M):
    d, mn = bareiss(M)
    return d, (mn is not None and all(x > 0 for x in mn))
def mul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(r, c)) for c in Bt] for r in A]
def tr(A): return [list(r) for r in zip(*A)]
def puissance(A, e):
    R = [[int(i == j) for j in range(len(A))] for i in range(len(A))]
    while e:
        if e & 1: R = mul(R, A)
        A = mul(A, A); e >>= 1
    return R
def phi115():
    def polmul(p, q):
        r = [0] * (len(p) + len(q) - 1)
        for i, x in enumerate(p):
            for j, y in enumerate(q): r[i + j] += x * y
        return r
    def poldiv(p, q):
        p = p[:]; out = [0] * (len(p) - len(q) + 1)
        for i in range(len(out) - 1, -1, -1):
            out[i] = p[i + len(q) - 1] // q[-1]
            for j, y in enumerate(q): p[i + j] -= out[i] * y
        assert not any(p); return out
    xn = lambda k: [-1] + [0] * (k - 1) + [1]
    return poldiv(polmul(xn(115), xn(1)), polmul(xn(5), xn(23)))

G, M5, M23 = lit_sakamoto(f_gram)
P, beta, a = lit_txt(cert_txt)
assert len(P) == N and all(len(r) == N for r in P) and len(beta) == N // 2
tb = []
for r in range(m):
    s = Fraction(0)
    for k, gk in enumerate(beta):
        if gk: s += gk * sum(comb(k, t) * ramanujan(m, k - 2 * t + r) for t in range(k + 1))
    tb.append(s)
assert all(t.denominator == 1 for t in tb), "traces non entieres"
H = [[int(tb[(i - j) % m]) for j in range(N)] for i in range(N)]
phi = phi115(); assert len(phi) == N + 1 and phi[-1] == 1
Z = [[int(j == i + 1) for j in range(N)] for i in range(N - 1)] + [[-phi[j] for j in range(N)]]
TX = tr(mul(M5, M23))
dG, pG = posdef(G); dH, pH = posdef(H); dP, _ = bareiss(P)
r1 = mul(mul(P, G), tr(P)) == H
r2 = mul(mul(TX, G), tr(TX)) == G
I88 = [[int(i == j) for j in range(N)] for i in range(N)]
r5 = puissance(TX, 115) == I88 and puissance(TX, 23) != I88 and puissance(TX, 5) != I88
r4 = mul(P, puissance(TX, a)) == mul(Z, P)
rb = beta0_corps(f_corps) == beta
print("G (fichier externe) : n = %d, symetrique %s, det %s, paire %s, definie positive %s, diagonale %s..%s"
      % (N, G == tr(G), dG, all(G[i][i] % 2 == 0 for i in range(N)), pG, min(G[i][i] for i in range(N)), max(G[i][i] for i in range(N))))
print("G_H = (Tr_L(beta zeta^(i-j))) recalculee sans GP : det %s, paire %s, definie positive %s, diagonale %s" % (dH, all(H[i][i] % 2 == 0 for i in range(N)), pH, H[0][0]))
print("beta du certificat == beta_0 de data/corps : %s" % rb)
print("det P = %s ; max |P_ij| = %d ; P G P~ == G_H : %s" % (dP, max(abs(x) for r in P for x in r), r1))
print("TX = (M5 M23)~ : TX G TX~ == G : %s ; TX d'ordre 115 : %s ; P TX^a == Z P (a = %d) : %s" % (r2, r5, a, r4))
ok = abs(dP) == 1 and r1 and dG == 1 and pG and G == tr(G) and all(G[i][i] % 2 == 0 for i in range(N)) and dH == 1 and pH and r2 and r4 and r5 and rb
print("RESULTAT (Python, entiers exacts) : certificat H = (O_L, beta_0) ~= L_0 (Sakamoto) : %s" % ("VALIDE" if ok else "INVALIDE"))
sys.exit(0 if ok else 1)
