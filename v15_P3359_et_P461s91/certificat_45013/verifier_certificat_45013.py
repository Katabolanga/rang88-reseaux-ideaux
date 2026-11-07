# -*- coding: utf-8 -*-
"""verifier_certificat_45013.py -- M10, 7 nov. 2026 (Claude).  Verificateur AUTONOME (bibliotheque standard seulement) du
certificat sans GRH : la composante 45 013 de [P5 sigma_91(P5)], P5 = (461, zeta - 5), est non nulle dans Cl(Q(zeta_115)).

Le certificat (certificat_45013_P461s91.json) donne un element alpha de Z[zeta] (115 coefficients), l'exposant omega, le caractere chi
et trois premiers auxiliaires.  Le verificateur NE recalcule PAS de somme de Jacobi : il controle seulement
  (C1) alpha * conj(alpha) = 461 dans Z[zeta] (reduction exacte modulo Phi_115) ;
  (C2) (alpha) = P5^omega : alpha est dans sigma_t(P5) = (461, zeta - 5^(t^-1)) exactement pour les t ou omega_t = 1, et
       omega a 44 coefficients 1 ; avec (C1), cela donne (alpha) = prod_{omega_t = 1} sigma_t(P5) ;
  (C3) omega = sigma_{-1} (2 - sigma_2) theta (formule de Stickelberger), donc omega annule Cl(L) (Washington, th. 6.10) ;
  (C4) chi est un caractere G -> F_p^* (multiplicatif), impair, de noyau {1, 91}, et chi(omega) = 0 dans F_p ;
  (C5) aux trois premiers auxiliaires l = 1 mod 115 p, le symbole S = sum_t chi(t)^-1 log_w (sigma_t(alpha) mod (l, zeta - s))^((l-1)/p)
       est NON NUL (w = h^((l-1)/p), s = h^((l-1)/115), h racine primitive mod l, verifiee).
Conclusion (lemme 2 de NOTE.md, section 2.2) : [P5]_chi != 0, donc, chi(91) = 1, [P5 sigma_91(P5)]_45013 = 2 [P5]_45013 != 0.
Usage : python -I verifier_certificat_45013.py certificat_45013_P461s91.json      (code 0 si tout passe)"""
import sys, json
from math import gcd

def main(f):
    C = json.load(open(f))
    M, q, r, p = 115, C["q"], C["r"], C["p"]
    G = [t for t in range(1, M) if gcd(t, M) == 1]
    a = C["alpha"]; om = {int(t): v for t, v in C["omega"].items()}; chi = {int(t): v for t, v in C["chi"].items()}
    ok = ko = 0
    def ctl(b, txt):
        nonlocal ok, ko
        if b: ok += 1
        else: ko += 1; print("ECHEC :", txt)
    # Phi_115 = (x^115 - 1)(x - 1) / ((x^5 - 1)(x^23 - 1))
    def pmul(u, v):
        w = [0] * (len(u) + len(v) - 1)
        for i, x in enumerate(u):
            for j, y in enumerate(v): w[i + j] += x * y
        return w
    def pdiv(u, v):
        u = list(u); qq = [0] * (len(u) - len(v) + 1)
        for i in range(len(u) - len(v), -1, -1):
            c = u[i + len(v) - 1]; qq[i] = c
            for j, y in enumerate(v): u[i + j] -= c * y
        assert all(x == 0 for x in u); return qq
    X = lambda n: [-1] + [0] * (n - 1) + [1]
    PHI = pdiv(pmul(X(115), X(1)), pmul(X(5), X(23)))
    ctl(len(PHI) == 89, "degre de Phi_115")
    def red(v):
        v = list(v) + [0] * max(0, 89 - len(v))
        for i in range(len(v) - 1, 87, -1):
            c = v[i]
            if c:
                for j in range(89): v[i - 88 + j] -= c * PHI[j]
        return v[:88]
    ctl(len(a) == M, "alpha : 115 coefficients")
    abar = [a[(-k) % M] for k in range(M)]
    prod = [0] * M
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(abar):
                if y: prod[(i + j) % M] += x * y
    pr = red(prod)
    ctl(pr[0] == q and all(x == 0 for x in pr[1:]), "(C1) alpha * conj(alpha) = q")
    def ev(v, z, mod): return sum(c * pow(z, k, mod) for k, c in enumerate(v)) % mod
    ctl(pow(r, 115, q) == 1 and pow(r, 23, q) != 1 and pow(r, 5, q) != 1, "r racine primitive 115-ieme mod q")
    for t in G:
        u = pow(t, -1, M)
        ctl((ev(a, pow(r, u, q), q) == 0) == (om[t] == 1), "(C2) appartenance a sigma_%d(P)" % t)
    ctl(sum(om.values()) == 44 and set(om.values()) <= {0, 1}, "(C2) omega : 44 coefficients 1")
    for t in G:
        uu = (-pow(t, -1, M)) % M
        ctl(om[t] == (2 * (uu % M) - (2 * uu) % M) // M, "(C3) omega_%d = 2{u/m} - {2u/m}, u = -t^-1" % t)
    ctl(all(chi[s] * chi[t] % p == chi[s * t % M] for s in G for t in G), "(C4) chi multiplicatif (complet)")
    ctl(chi[M - 1] == p - 1, "(C4) chi impair")
    ctl(sorted(t for t in G if chi[t] == 1) == [1, 91], "(C4) noyau {1, 91}")
    ctl(sum(om[t] * chi[t] for t in G) % p == 0, "(C4) chi(omega) = 0")
    for l, h in C["auxiliaires"]:
        ctl(all(l % d for d in range(2, int(l ** 0.5) + 1)) and (l - 1) % (M * p) == 0, "l premier, l = 1 mod 115 p")
        # h racine primitive mod l : h^((l-1)/f) != 1 pour tout facteur premier f de l-1
        n, fs, d = l - 1, [], 2
        while d * d <= n:
            if n % d == 0:
                fs.append(d)
                while n % d == 0: n //= d
            d += 1
        if n > 1: fs.append(n)
        ctl(all(pow(h, (l - 1) // f, l) != 1 for f in fs), "h racine primitive mod l")
        s_ = pow(h, (l - 1) // M, l); w = pow(h, (l - 1) // p, l)
        tab = {}; x = 1
        for i in range(p): tab[x] = i; x = x * w % l
        S = 0
        for t in G:
            v = ev(a, pow(s_, t, l), l)
            ctl(v != 0, "alpha premier a l")
            S += pow(chi[t], p - 2, p) * tab[pow(v, (l - 1) // p, l)]
        S %= p
        print("l = %d : S = %d" % (l, S))
        ctl(S != 0, "(C5) symbole non nul en l = %d" % l)
        ctl(S == C.get("S_attendus", {}).get(str(l), S), "symbole egal a la valeur annoncee")
    ctl(chi[91] == 1, "chi(91) = 1 : [P sigma91(P)]_chi = 2 [P]_chi")
    print("BILAN verifier_certificat_45013 : %d controles, %d echecs" % (ok, ko))
    print("CONCLUSION : composante 45013 de [P5 sigma91(P5)] NON NULLE" if ko == 0 else "CONCLUSION : certificat REJETE")
    return 0 if ko == 0 else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
