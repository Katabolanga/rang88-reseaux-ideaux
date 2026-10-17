#!/usr/bin/env python3
"""Check of X139.std, X599.std, X4969.std and X4049.std (format of the Nebe-Sloane Catalogue of Lattices), version 2.

Checks, in exact integer arithmetic and with the Python standard library only:
  1. the file structure (required sections, no repeated section, declared dimensions, number of entries) and, since
     version 2 (17 October 2026), the catalogue conventions: only sections used by the catalogue entries, in their
     order (NAME, DIMENSION, DET, GRAM, DIVISORS, MINIMAL_NORM, KISSING_NUMBER, HERMITE_NUMBER, [SUB]GROUP_ORDER,
     [SUB]GROUP_NAME, [SUB]GROUP_GENERATORS, PROPERTIES, REFERENCES, NOTES, LAST_LINE), exactly one generator
     section (SUBGROUP_GENERATORS when only a subgroup of the automorphism group is known, as here);
     DET and DIVISORS, if present, must be 1;
  2. the Gram matrix is symmetric and even, has determinant 1 and is positive definite
     (all leading principal minors > 0, computed by fraction-free Gaussian elimination);
  3. each generator g satisfies g * G * g^T = G (row convention, as in the catalogue);
  4. g1 has order exactly 230; g2 normalises <g1> (g1 * g2 = g2 * g1^e for some e);
     k = the least k >= 1 with g2^k in <g1>; hence <g1, g2> has order 230 * k, which must equal SUBGROUP_ORDER
     (or GROUP_ORDER) when that section is present;
  5. if the NOTES contain a line "NORM8: v_1 ... v_n", then v * G * v^T = 8 (a vector of norm 8, so the minimum is <= 8).
NOT checked here: that the minimum is 8 (computer-assisted theorem of the paper), the kissing number, the construction
as an ideal lattice (see verify_construction.py), and the full automorphism group.

Usage: python3 verify_std.py X139.std X599.std X4969.std X4049.std     (exit code 0 only if every check passes)
"""
import sys

REQUIRED = ("NAME", "DIMENSION", "GRAM", "LAST_LINE")
GENERATOR_SECTIONS = ("SUBGROUP_GENERATORS", "GROUP_GENERATORS")
# order of the sections in the catalogue entries (e.g. L_56c, subgroup known; CQ48a, full group known)
CATALOGUE_ORDER = ("NAME", "DIMENSION", "DET", "GRAM", "DIVISORS", "MINIMAL_NORM", "KISSING_NUMBER", "HERMITE_NUMBER",
                   "GROUP_ORDER", "GROUP_NAME", "GROUP_GENERATORS", "SUBGROUP_ORDER", "SUBGROUP_NAME",
                   "SUBGROUP_GENERATORS", "PROPERTIES", "REFERENCES", "NOTES", "LAST_LINE")


class CheckError(Exception):
    pass


def require(cond, msg):
    if not cond:
        raise CheckError(msg)


def read_std(path):
    sections, order, cur = {}, [], None
    with open(path, encoding="ascii") as f:
        for line in f:
            s = line.strip()
            if s.startswith("%"):
                cur = s[1:]
                require(cur not in sections, "%s: section %%%s repeated" % (path, cur))
                sections[cur] = []
                order.append(cur)
            elif cur is not None and s:
                sections[cur].append(s)
    for r in REQUIRED:
        require(r in sections, "%s: missing section %%%s" % (path, r))
    require(order[-1] == "LAST_LINE", "%s: %%LAST_LINE is not the last section" % path)
    gs = [s for s in GENERATOR_SECTIONS if s in sections]
    require(len(gs) == 1, "%s: exactly one of %%SUBGROUP_GENERATORS, %%GROUP_GENERATORS expected" % path)
    for s in order:
        require(s in CATALOGUE_ORDER, "%s: section %%%s is not used by the catalogue" % (path, s))
    pos = [CATALOGUE_ORDER.index(s) for s in order]
    require(pos == sorted(pos), "%s: sections not in the order of the catalogue entries" % path)
    return sections


def gens_lines(S):
    """lines of the generator section (SUBGROUP_GENERATORS in version 2, GROUP_GENERATORS in version 1)"""
    return S["SUBGROUP_GENERATORS"] if "SUBGROUP_GENERATORS" in S else S["GROUP_GENERATORS"]


def order_value(lines):
    """value of an order written as in the catalogue, e.g. 2^2*5*23"""
    s = "".join(lines).replace(" ", "")
    v = 1
    try:
        for f in s.split("*"):
            b, _, e = f.partition("^")
            v *= int(b) ** (int(e) if e else 1)
    except ValueError:
        raise CheckError("cannot read the order %r" % s)
    return v


def ints(lines):
    try:
        return [int(t) for l in lines for t in l.split()]
    except ValueError as e:
        raise CheckError("non-integer entry: %s" % e)


def parse_gram(lines, n=None):
    v = ints(lines)
    require(len(v) >= 2, "GRAM: missing header")
    d, flag, vals = v[0], v[1], v[2:]
    require(n is None or d == n, "GRAM: dimension %d differs from %%DIMENSION %s" % (d, n))
    require(flag in (0, d), "GRAM: header must be 'n 0' (lower triangle) or 'n n' (full matrix)")
    full = flag == d
    require(len(vals) == (d * d if full else d * (d + 1) // 2), "GRAM: wrong number of entries")
    G, k = [[0] * d for _ in range(d)], 0
    for i in range(d):
        for j in range(d if full else i + 1):
            G[i][j] = vals[k]
            if not full:
                G[j][i] = vals[k]
            k += 1
    require(all(G[i][j] == G[j][i] for i in range(d) for j in range(d)), "GRAM: not symmetric")
    return G


def parse_gens(lines, n):
    v = ints(lines)
    require(len(v) >= 1, "generators: missing count")
    count, p, mats = v[0], 1, []
    for k in range(count):
        require(p + 2 <= len(v), "generators: generator %d truncated" % (k + 1))
        r, c = v[p], v[p + 1]
        require(r == n and c == n, "generators: generator %d is %d x %d, expected %d x %d" % (k + 1, r, c, n, n))
        p += 2
        require(p + r * c <= len(v), "generators: generator %d truncated" % (k + 1))
        mats.append([v[p + i * c: p + (i + 1) * c] for i in range(r)])
        p += r * c
    require(p == len(v), "generators: wrong number of entries")
    return mats


def parse_norm8(notes, n):
    for l in notes:
        if l.startswith("NORM8:"):
            v = ints([l[len("NORM8:"):]])
            require(len(v) == n, "NORM8: %d coordinates, expected %d" % (len(v), n))
            return v
    return None


def mul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]


def vecmul(x, A):
    return [sum(x[i] * A[i][j] for i in range(len(x))) for j in range(len(A[0]))]


def transpose(A):
    return [list(r) for r in zip(*A)]


def ident(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def power(A, e):
    R, P = ident(len(A)), A
    while e:
        if e & 1:
            R = mul(R, P)
        P = mul(P, P)
        e >>= 1
    return R


def leading_minors(G):
    """Bareiss elimination without pivoting: the k-th pivot is the k-th leading principal minor."""
    n, M, prev, minors = len(G), [r[:] for r in G], 1, []
    for k in range(n):
        piv = M[k][k]
        minors.append(piv)
        if piv == 0:
            break
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * piv - M[i][k] * M[k][j]) // prev
        prev = piv
    return minors


def power_index(g1, target, order):
    """the e in [0, order) with g1^e = target, or None (first row as a filter, then a full check)."""
    n = len(g1)
    row, first = [int(j == 0) for j in range(n)], target[0]
    for e in range(order):
        if row == first and power(g1, e) == target:
            return e
        row = vecmul(row, g1)
    return None


def check(path):
    S = read_std(path)
    name = S["NAME"][0]
    n = ints(S["DIMENSION"])
    require(len(n) == 1, "DIMENSION: one integer expected")
    n = n[0]
    G = parse_gram(S["GRAM"], n)
    gens = parse_gens(gens_lines(S), n)
    require(len(gens) == 2, "two generators expected (g1 = -zeta, g2 = semilinear lift)")
    print("== %s (%s): dimension %d, %d generators" % (name, path, n, len(gens)))
    require(all(G[i][i] % 2 == 0 for i in range(n)), "Gram not even")
    mins = leading_minors(G)
    require(len(mins) == n and all(d > 0 for d in mins), "Gram not positive definite")
    require(mins[-1] == 1, "determinant != 1")
    print("   Gram: symmetric, even, positive definite, determinant 1")
    if "DET" in S:
        require(ints(S["DET"]) == [1], "DET: 1 expected")
    if "DIVISORS" in S:
        require(ints(S["DIVISORS"]) == [1], "DIVISORS: 1 expected for a unimodular lattice")
    print("   DET and DIVISORS (when present): 1")
    for k, g in enumerate(gens, 1):
        require(mul(mul(g, G), transpose(g)) == G, "g%d does not preserve the Gram matrix" % k)
    print("   g * G * g^T = G for every generator")
    g1, g2 = gens
    I = ident(n)
    require(power(g1, 230) == I and all(power(g1, 230 // q) != I for q in (2, 5, 23)), "g1 does not have order 230")
    print("   g1 has order 230")
    # g2 normalises <g1>: find e with g1 * g2 = g2 * g1^e
    # (first rows of g2 * g1^t for t = 0..229 are computed incrementally, then the candidate is checked in full)
    lhs, e, r = mul(g1, g2), None, g2[0][:]
    for t in range(230):
        if r == lhs[0] and mul(g2, power(g1, t)) == lhs:
            e = t
            break
        r = vecmul(r, g1)
    require(e is not None, "g2 does not normalise <g1>")
    print("   g1 * g2 = g2 * g1^%d, i.e. g2^-1 g1 g2 = g1^%d: g2 normalises <g1>" % (e, e))
    P, k = g2, 1
    while True:
        j = power_index(g1, P, 230)
        if j is not None:
            break
        P, k = mul(P, g2), k + 1
        require(k <= 8, "no power g2^k (k <= 8) lies in <g1>")
    print("   least k with g2^k in <g1>: k = %d (g2^%d = g1^%d)" % (k, k, j))
    print("   => <g1, g2> has order 230 * %d = %d" % (k, 230 * k))
    for sec in ("SUBGROUP_ORDER", "GROUP_ORDER"):
        if sec in S:
            require(order_value(S[sec]) == 230 * k, "%s: %s differs from the computed order %d" % (sec, "".join(S[sec]), 230 * k))
            print("   %s = %s = %d, the computed order" % (sec, "".join(S[sec]), 230 * k))
    v = parse_norm8(S.get("NOTES", []), n)
    if v is None:
        print("   (no NORM8 line in the NOTES)")
    else:
        require(sum(v[i] * G[i][j] * v[j] for i in range(n) for j in range(n)) == 8, "NORM8: v G v^T != 8")
        print("   NORM8: v * G * v^T = 8 (a vector of norm 8)")
    return 230 * k


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        print("error: no file given")
        return 2
    try:
        for p in argv[1:]:
            check(p)
    except (CheckError, OSError) as e:
        print("FAILED: %s" % e)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
