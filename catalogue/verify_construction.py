#!/usr/bin/env python3
"""Reconstruction of the .std data from the ideal-lattice data (complementary to verify_std.py).

For X = X139, X599, X4969 or X4049, reads X_construction.gp (PRIME, ALPHA, A_SEMI, LAMBDA, BASIS, NORM8) and X.std, and checks in
exact rational arithmetic (Python standard library only; Phi_115, traces and polynomial arithmetic are computed here):
  0. P = (p, g(zeta)) is a prime ideal of Z[zeta] of norm p^2 (p prime, g monic quadratic, irreducible mod p, dividing
     Phi_115 mod p), and BASIS is a Z-basis of P (every column lies in P and |det BASIS| = p^2);
  1. GRAM = BASIS^T * H * BASIS with H[i][j] = Tr_{L/Q}(ALPHA * zeta^(i-j)), L = Q(zeta), zeta = zeta_115;
  2. the generator g1 of X.std is the matrix of u -> -zeta*u in the basis BASIS (row convention);
  3. the generator g2 of X.std is the matrix of u -> LAMBDA*sigma_a(u), sigma_a(zeta) = zeta^a, a = A_SEMI;
  4. NORM8 is the vector of the NORM8 line of X.std, and NORM8 * GRAM * NORM8^T = 8.
It reads the data P, ALPHA, LAMBDA and BASIS from the file; it does not rediscover them from the field alone. It shares
its reader of the .std format with verify_std.py; the two scripts are complementary checks, not independent proofs.
NOT checked here: that the minimum is 8 (computer-assisted theorem of the paper), the full automorphism group.

Usage: python3 verify_construction.py X139 X599 X4969 X4049   (run in the folder containing the files; exit code 0 only on success)
Version 2 (17 October 2026): reads the generators from %SUBGROUP_GENERATORS (format of the catalogue) or %GROUP_GENERATORS.
"""
import re
import sys
from fractions import Fraction
from math import gcd, isqrt

from verify_std import CheckError, require, read_std, ints, parse_gram, parse_gens, parse_norm8, gens_lines

M, N = 115, 88


def poly_mul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return r


def poly_divexact(a, b):          # b monic
    a, q = a[:], [0] * (len(a) - len(b) + 1)
    for k in range(len(q) - 1, -1, -1):
        c = a[k + len(b) - 1]
        q[k] = c
        for i, y in enumerate(b):
            a[k + i] -= c * y
    require(not any(a), "inexact polynomial division")
    return q


def xn1(n):                       # x^n - 1, coefficients from the constant term
    return [-1] + [0] * (n - 1) + [1]


PHI = poly_divexact(poly_mul(xn1(115), xn1(1)), poly_mul(xn1(5), xn1(23)))
require(len(PHI) == N + 1 and PHI[-1] == 1, "Phi_115")


def reduce_phi(a):                # remainder modulo Phi_115 (Phi monic), after reducing exponents modulo 115
    r = [0] * M
    for k, c in enumerate(a):
        r[k % M] += c
    for k in range(M - 1, N - 1, -1):
        c = r[k]
        if c:
            for i, y in enumerate(PHI):
                r[k - N + i] -= c * y
    return r[:N]


def tr_zeta(k):                   # Tr_{L/Q}(zeta^k) = mu(d) * 88 / phi(d), zeta^k of exact order d
    d = M // gcd(k % M, M) if k % M else 1
    mu, ph = {1: (1, 1), 5: (-1, 4), 23: (-1, 22), 115: (1, 88)}[d]
    return mu * (N // ph)


TR = [tr_zeta(k) for k in range(M)]


def parse_poly(s):
    s = s.replace(" ", "")
    if s[0] not in "+-":
        s = "+" + s
    coeffs = {}
    for t in re.findall(r"[+-][^+-]+", s):
        sign, body = (-1 if t[0] == "-" else 1), t[1:]
        m = re.fullmatch(r"(?:(\d+(?:/\d+)?)\*?)?(y(?:\^(\d+))?)?", body)
        require(m is not None and (m.group(1) or m.group(2)), "cannot parse term " + t)
        c = Fraction(m.group(1)) if m.group(1) else Fraction(1)
        e = (int(m.group(3)) if m.group(3) else 1) if m.group(2) else 0
        coeffs[e] = coeffs.get(e, 0) + sign * c
    return [coeffs.get(k, Fraction(0)) for k in range(max(coeffs) + 1)]


def parse_matrix(s):
    s = s.strip()
    require(s[0] == "[" and s[-1] == "]", "matrix expected")
    return [[int(x) for x in row.split(",")] for row in s[1:-1].split(";")]


def read_construction(path):
    text = open(path, encoding="ascii").read()
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    vals = {}
    for line in text.splitlines():           # one assignment per line: NAME = value;
        m = re.match(r"\s*(\w+)\s*=\s*(.*);\s*$", line)
        if m:
            vals[m.group(1)] = m.group(2)
    for k in ("PRIME", "ALPHA", "A_SEMI", "LAMBDA", "BASIS", "NORM8"):
        require(k in vals, "%s: missing %s" % (path, k))
    p, g = vals["PRIME"].strip()[1:-1].split(",", 1)
    norm8 = [int(x) for x in vals["NORM8"].strip()[1:-1].split(",")]
    return (int(p), parse_poly(g), parse_poly(vals["ALPHA"]), int(vals["A_SEMI"]), parse_poly(vals["LAMBDA"]),
            parse_matrix(vals["BASIS"]), norm8)


def det_int(A):
    """determinant of an integer matrix (Bareiss, with row exchanges)."""
    n, Mx, sign, prev = len(A), [r[:] for r in A], 1, 1
    for k in range(n - 1):
        if Mx[k][k] == 0:
            sw = next((r for r in range(k + 1, n) if Mx[r][k] != 0), None)
            if sw is None:
                return 0
            Mx[k], Mx[sw], sign = Mx[sw], Mx[k], -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                Mx[i][j] = (Mx[i][j] * Mx[k][k] - Mx[i][k] * Mx[k][j]) // prev
        prev = Mx[k][k]
    return sign * Mx[n - 1][n - 1]


def rem_mod(v, p, g):
    """remainder of the integer polynomial v modulo (p, g), g monic of degree 2."""
    r = [c % p for c in v]
    for k in range(len(r) - 1, 1, -1):
        c = r[k]
        if c:
            r[k] = 0
            r[k - 1] = (r[k - 1] - c * g[1]) % p
            r[k - 2] = (r[k - 2] - c * g[0]) % p
    return r[:2]


def check_prime_ideal(p, g):
    require(p > 1 and all(p % d for d in range(2, isqrt(p) + 1)), "p = %d is not prime" % p)
    require(len(g) == 3 and g[2] == 1 and all(c.denominator == 1 for c in g), "g must be a monic integer quadratic")
    g = [int(c) for c in g]
    disc = (g[1] * g[1] - 4 * g[0]) % p
    require(p > 2 and pow(disc, (p - 1) // 2, p) == p - 1, "g is not irreducible modulo p")
    require(rem_mod(PHI, p, g) == [0, 0], "g does not divide Phi_115 modulo p")
    return g


def solve_integral(B, W):
    """X with B X = W (B square, rational Gauss-Jordan); requires X to be integral."""
    n = len(B)
    A = [[Fraction(x) for x in B[i]] + [Fraction(x) for x in W[i]] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        inv = 1 / A[c][c]
        A[c] = [x * inv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    X = [row[n:] for row in A]
    require(all(x.denominator == 1 for row in X for x in row), "the map does not preserve the lattice")
    return [[int(x) for x in row] for row in X]


def check(name):
    p, g, alpha, a, lam, B, norm8 = read_construction(name + "_construction.gp")
    S = read_std(name + ".std")
    n = ints(S["DIMENSION"])[0]
    require(n == N and len(B) == N and all(len(r) == N for r in B), "dimensions")
    G, gens = parse_gram(S["GRAM"], n), parse_gens(gens_lines(S), n)
    cols = [[B[i][j] for i in range(N)] for j in range(N)]          # basis vectors (power-basis coordinates)
    # 0. P is a prime ideal of norm p^2, and BASIS is a Z-basis of P
    g = check_prime_ideal(p, g)
    require(all(rem_mod(v, p, g) == [0, 0] for v in cols), "a basis vector is not in P")
    require(abs(det_int(B)) == p * p, "BASIS does not span P")
    print("== %s: P = (%d, zeta^2 + %d zeta + %d) is a prime ideal of norm %d^2, and BASIS is a Z-basis of P"
          % (name, p, g[1], g[0], p))
    # 1. Gram
    t = [sum(c * TR[(k + d) % M] for k, c in enumerate(alpha)) for d in range(M)]   # Tr(alpha zeta^d)
    H = [[t[(i - j) % M] for j in range(N)] for i in range(N)]
    HB = [[sum(H[i][k] * B[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
    Gc = [[sum(B[k][i] * HB[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
    require(Gc == G, "Gram matrix does not match")
    print("   GRAM = BASIS^T * (Tr(ALPHA zeta^(i-j))) * BASIS")
    # 2. g1 = multiplication by -zeta
    W1 = [reduce_phi([0] + [-x for x in v]) for v in cols]
    T1 = solve_integral(B, [[W1[j][i] for j in range(N)] for i in range(N)])
    require(transpose_ok(T1, gens[0]), "g1 is not multiplication by -zeta")
    print("   g1 = multiplication by -zeta in this basis")
    # 3. g2 = u -> LAMBDA * sigma_a(u)
    W2 = []
    for v in cols:
        s = [0] * M                           # sigma_a(u): zeta^k -> zeta^(a k mod 115)
        for k, c in enumerate(v):
            s[(a * k) % M] += c
        W2.append(reduce_phi(poly_mul(lam, reduce_phi(s))))
    T2 = solve_integral(B, [[W2[j][i] for j in range(N)] for i in range(N)])
    require(transpose_ok(T2, gens[1]), "g2 is not u -> LAMBDA * sigma_a(u)")
    integral = all(x.denominator == 1 for x in lam)
    print("   g2 = (u -> LAMBDA * sigma_%d(u)) in this basis%s" % (a, "" if integral else " (LAMBDA not integral)"))
    # 4. the norm-8 vector
    require(len(norm8) == N, "NORM8: wrong length")
    require(parse_norm8(S.get("NOTES", []), n) == norm8, "NORM8 differs between the .std file and the construction file")
    require(sum(norm8[i] * Gc[i][j] * norm8[j] for i in range(N) for j in range(N)) == 8, "NORM8 does not have norm 8")
    print("   NORM8 (same in both files) has norm 8")


def transpose_ok(T, g):
    return [list(r) for r in zip(*T)] == g


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        print("error: no lattice name given")
        return 2
    try:
        for nm in argv[1:]:
            check(nm)
    except (CheckError, OSError, ValueError) as e:
        print("FAILED: %s" % e)
        return 1
    print("all reconstructions agree with the .std files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
