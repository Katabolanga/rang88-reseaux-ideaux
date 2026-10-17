Four extremal even unimodular lattices of rank 88: X139, X599, X4969 and X4049
=============================================================================
Data in the format of the Catalogue of Lattices (version 2)

Ivan Gauvin, 17 October 2026. Data for the Catalogue of Lattices (G. Nebe and N. J. A. Sloane).
This version 2 follows the conventions of the catalogue entries for which only a subgroup of the automorphism group is
known (for instance L_56c): sections in the order of the catalogue, DIVISORS, SUBGROUP_ORDER, SUBGROUP_NAME and
SUBGROUP_GENERATORS. It supersedes the format of the package of 15 October 2026 (X139, X599); the Gram matrices and
the generators are unchanged (see section 5).
References: I. Gauvin, "Even unimodular ideal lattices of rank 88 over Q(zeta_115)" (French original: "Reseaux ideaux
pairs unimodulaires de rang 88 sur Q(zeta_115)"), preprint, 15 October 2026 (arXiv identifier pending), for X139 and
X599; its addendum (October 2026) for X4969 and X4049.
Programs and certificates: https://github.com/Katabolanga/rang88-reseaux-ideaux


1. The lattices
---------------
L = Q(zeta), zeta = zeta_115, [L:Q] = 88. For a prime ideal P of Z[zeta], X_p = (P, b) with
b(u, v) = Tr_{L/Q}(alpha u conj(v)), alpha = beta_0/nu totally positive in the real subfield, chosen so that X_p is
unimodular (it is then even). The four lattices are

    X139  :  P = (139, zeta^2 + zeta + 77)              (preprint)
    X599  :  P = (599, zeta^2 + 87 zeta + 322)          (preprint)
    X4969 :  P = (4969, zeta^2 + 3763 zeta + 2809)      (addendum)
    X4049 :  P = (4049, zeta^2 + 105 zeta + 2084)       (addendum)

All four primes are congruent to 24 mod 115, so P has residue degree 2 and its class is fixed by sigma_24.
Minimum 8 is established by the computer-assisted method of the preprint, in its execution model (section 5.4:
M1, M2, H1-H3): the certifying enumeration swept both sides of the extremality criterion completely, with no hit.
Every side of the four lattices was executed twice, with byte-identical receipts. No independent implementation of
the enumeration has been run. The preprint and its addendum also prove, without assuming GRH, that the four lattices
are pairwise non-isometric and isometric to neither of Sakamoto's two lattices (arXiv:2609.15633v2).
Given the minimum-8 statement, the extremal theta series of weight 44 gives the kissing number 168498000 (counting
vectors with both signs).


2. Files
--------
X139.std, X599.std, X4969.std, X4049.std
    Format of the catalogue entries, sections in this order: NAME, DIMENSION, DET, GRAM ("88 0" followed by the lower
    triangle of the Gram matrix in an LLL-reduced basis), DIVISORS, MINIMAL_NORM, KISSING_NUMBER, HERMITE_NUMBER,
    SUBGROUP_ORDER, SUBGROUP_NAME, SUBGROUP_GENERATORS (the number of generators, 2, then for each generator
    "88<TAB>88" and its 88 rows), PROPERTIES, REFERENCES, NOTES, LAST_LINE. The line "NORM8: ..." of NOTES gives the
    coordinates in this basis of a vector of norm 8.

X139_construction.gp, X599_construction.gp, X4969_construction.gp, X4049_construction.gp  (PARI/GP syntax; unchanged)
    PRIME = [p, g(y)] with P = (p, g(zeta)); ALPHA; BASIS; A_SEMI and LAMBDA, describing the second generator; NORM8.
    BASIS contains the basis vectors as columns, in 1, zeta, ..., zeta^87, and
    GRAM = BASIS^T * H * BASIS with H[i,j] = Tr(ALPHA zeta^(i-j)).
    The generator matrices act on row coordinates: for a matrix T acting on column coordinates, the exported matrix
    is g = T^T, and it satisfies g * GRAM * g^T = GRAM.

verify_std.py, verify_construction.py  (Python 3, standard library only, exact integer and rational arithmetic; version 2)
    python3 verify_std.py X139.std X599.std X4969.std X4049.std
    python3 verify_construction.py X139 X599 X4969 X4049
    Exit code 0 only if every check passes. Run verify_construction.py from the folder that contains verify_std.py
    (it imports it). The checks raise explicit errors (no assert), so they also run under -O.

SHA256SUMS.txt
    SHA-256 of the other files.

Source of the construction inputs (the files actually read by the certifying program):
    data/P139/entrees/I_data.gp    SHA-256 a133ab58a8e95ded67f38e2e1c8d224ce0cb9a4849555d61e2c4f0b6f269bbd4
    data/P599/entrees/I_data.gp    SHA-256 19b69c8ecbd8ad256b02afc0717e92898f3d4438f92ff863498139a041922692
    data/P4969/entrees/I_data.gp   SHA-256 768ab11514b21931102c0216765a1ccd153b15ecd6da2ad90d334be75dc8c907
    data/P4049/entrees/I_data.gp   SHA-256 7f8192d5968f65e32801a4c6a7d215b48b937bdb5713dcbda9eece40d8385960
and, for the vectors of norm 8, data/P<p>/norme8.txt (given there in the coordinates of the gluing construction, and
transported to the bases used here).


3. The generators: a subgroup of the automorphism group
------------------------------------------------------
g1 = multiplication by -zeta, of order 230 (the cyclic group of the ideal lattice).

g2 = a semilinear map u -> lambda * sigma_a(u), sigma_a(zeta) = zeta^a, lifting a generator of the Galois stabiliser of
     the class of P, with lambda * sigma_a(P) = P and alpha * lambda * conj(lambda) = sigma_a(alpha).

    X139, X4969, X4049: the stabiliser is <sigma_24> (order 2); lambda is a unit of Z[zeta]; g2^2 = -1 (= g1^115);
        g2^-1 g1 g2 = g1^139. SUBGROUP_ORDER 2^2*5*23 = 460, SUBGROUP_NAME C115 : C4 = <zeta> : <g2>, where g2 acts
        on <zeta> by zeta -> zeta^24 (so C4 acts through C2); equivalently C23 x Dic5. No lift of sigma_24 is an
        involution.
    X599: the stabiliser is <sigma_22> = {sigma_1, sigma_22, sigma_24, sigma_68} (cyclic of order 4); lambda generates
        the fractional ideal P sigma_22(P)^-1; g2 has order 8, g2^4 = -1, g2^2 lifts sigma_24; g2^-1 g1 g2 = g1^137.
        SUBGROUP_ORDER 2^3*5*23 = 920, SUBGROUP_NAME C115 : C8 = <zeta> : <g2>, where g2 acts by zeta -> zeta^22 (so C8
        acts through C4). Every lift of sigma_22 has order 8.

By the normaliser argument of the preprint (Remark 2.6) and the exact Galois stabilisers (preprint, sections 2.4 and
6.4, for X139 and X599; addendum, Proposition 2.3, for X4969 and X4049, all without assuming GRH), <g1, g2> is the
full normaliser in Aut(X) of the group of multiplications by roots of unity. The full automorphism groups have not
been determined: |Aut(X139)| >= 460, |Aut(X599)| >= 920, |Aut(X4969)| >= 460, |Aut(X4049)| >= 460.


4. Methods and scope of the checks
----------------------------------
- The multipliers lambda were found by floating point calculations and lattice reduction among explicit cyclotomic
  units (for X599, a generator of p / sigma_22(p) was sought in the degree-44 field M = L^<sigma_24>, with
  P = p O_L, a search that used a class group computation conditional on GRH). The resulting multipliers and the
  generator identities were checked exactly in PARI/GP 2.15.4; they do not depend on that class group computation.
- verify_std.py checks the file structure and the catalogue conventions (sections and their order, one generator
  section, DET and DIVISORS equal to 1), evenness, positive definiteness, determinant 1, Gram invariance, the order of
  <g1, g2> against SUBGROUP_ORDER, and the norm of NORM8. verify_construction.py checks that P is a prime ideal of
  norm p^2 and that BASIS is a Z-basis of P, and reconstructs the Gram matrices and generators from P, alpha, lambda
  and BASIS. The two scripts share the .std-reading routines; they are complementary checks, not independent proofs.
- These scripts do not check the minimum, non-isometry, novelty, the exactness of the Galois stabilisers or the full
  automorphism groups. The minimum is the computer-assisted statement of the preprint and its addendum.


5. Changes from version 1 (package of 15 October 2026)
-----------------------------------------------------
- Only the format changes. The lines of the Gram matrices and of the generator matrices are copied unchanged from
  version 1 (checked when the files were written), except the header "88 88" of each generator, now "88<TAB>88" as in
  the catalogue entries.
- %GROUP_GENERATORS becomes %SUBGROUP_GENERATORS, since only a subgroup of the automorphism group is known; the
  sections %DIVISORS (1), %SUBGROUP_ORDER and %SUBGROUP_NAME are added; %DET now follows %DIMENSION, as in the
  catalogue; two lines at the head of %NOTES explain the subgroup.
- The two verification scripts are extended accordingly (version 2): they read either generator section, and
  verify_std.py also checks the order of the sections, DET, DIVISORS and SUBGROUP_ORDER. Version 1 files are
  rejected by the version 2 check, because of the order of their sections.
