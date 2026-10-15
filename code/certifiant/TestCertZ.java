import java.math.BigInteger;
import java.util.*;

/**
 * TestCertZ — harnais de validation de Rang88CertZ sur cas finis (aucune donnée de rang 88).
 *  1. E8 : 120 + 1080 = 1200 représentants (au signe près) de norme <= 4, par le catalogue adaptatif et les tâches.
 *  2. Comparaison ENSEMBLISTE avec une énumération exhaustive par boîte (arithmétique entière exacte) sur des formes
 *     aléatoires de dimension 2 à 4 : côté court + fibre (T, d, DA, DB), bornes rationnelles, cas de frontière compris.
 * À lancer avec -Dverif=1 (recalcul exact des caches à chaque nœud) et divers -DF.
 * Usage : java -Dverif=1 -cp classes TestCertZ [graine] [nombre de formes]
 */
public strictfp class TestCertZ {
    static int echecs = 0, controles = 0;
    static void ok(boolean b, String m) { controles++; if (!b) { echecs++; System.out.println("ECHEC " + m); } }

    // exécute toutes les tâches du catalogue, séquentiellement, par le même chemin que la production
    static long[] lancer(long[][] A, long[][] B, long[][] T, long DA, long DB, long d, long BAn, long BAd, long S, int D, int Dmax, double seuil, boolean compte, Set<String> touches) {
        Rang88CertZ.modeCompte = compte;
        Rang88CertZ.charger(A, B, T, DA, DB, d, BAn, BAd, S);
        Rang88CertZ.recepteur = (la, u, y, w, e) -> { if (!touches.add(Arrays.toString(u) + Arrays.toString(y))) throw new IllegalStateException("touche en double"); };
        List<Rang88CertZ.Tache> cat = Rang88CertZ.catalogue(D, Dmax, seuil, null);
        Rang88CertZ.Travail w = new Rang88CertZ.Travail();
        long u = 0, t = 0;
        for (Rang88CertZ.Tache tc : cat) { Rang88CertZ.Compteurs c = w.executer(tc); u += c.u; t += c.touches; }
        return new long[]{u, t, cat.size()};
    }

    static long q(long[][] G, long[] x) { long s = 0; for (int i = 0; i < x.length; i++) for (int j = 0; j < x.length; j++) s = Math.addExact(s, Math.multiplyExact(Math.multiplyExact(G[i][j], x[i]), x[j])); return s; }
    static long[] mv(long[][] M, long[] x) { long[] r = new long[x.length]; for (int i = 0; i < x.length; i++) for (int j = 0; j < x.length; j++) r[i] += M[i][j] * x[j]; return r; }

    /** forme G = U~ G0 U avec G0 à diagonale dominante (min propre >= mu[0] par Gershgorin), U unimodulaire, Uinv = U^-1 */
    static long[][][] forme(Random R, int n, int echelle, long[] mu) {
        long[][] G0 = new long[n][n];
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) G0[i][j] = G0[j][i] = R.nextInt(2 * echelle + 1) - echelle;
        long m = Long.MAX_VALUE;
        for (int i = 0; i < n; i++) { long s = 0; for (int j = 0; j < n; j++) if (j != i) s += Math.abs(G0[i][j]); G0[i][i] = s + 1 + R.nextInt(3 * echelle + 1); m = Math.min(m, G0[i][i] - s); }
        mu[0] = m;
        long[][] U = new long[n][n], V = new long[n][n];
        for (int i = 0; i < n; i++) U[i][i] = V[i][i] = 1;
        for (int op = 0; op < 3 * n; op++) {     // U <- U E_ij(c), Uinv <- E_ij(-c) Uinv
            int i = R.nextInt(n), j = R.nextInt(n); if (i == j) continue; long c = R.nextInt(5) - 2;
            for (int r = 0; r < n; r++) U[r][j] += c * U[r][i];
            for (int r = 0; r < n; r++) V[i][r] -= c * V[j][r];
        }
        long[][] G = new long[n][n];
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) { long s = 0; for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) s += U[a][i] * G0[a][b] * U[b][j]; G[i][j] = s; }
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) { long s = 0; for (int a = 0; a < n; a++) s += U[i][a] * V[a][j]; if (s != (i == j ? 1 : 0)) throw new IllegalStateException("inverse"); }
        return new long[][][]{G, G0, U, V};
    }
    /** tous les x entiers avec x~Gx <= num/den (exact), par boîte sur x0 = U x : |x0_i|^2 mu <= num/den */
    static List<long[]> boite(long[][][] f, long mu, BigInteger num, BigInteger den) {
        List<long[]> out = new ArrayList<>(); int n = f[0].length;
        if (num.signum() < 0) return out;
        long Rr = 0; while (BigInteger.valueOf((Rr + 1) * (Rr + 1) * mu).multiply(den).compareTo(num) <= 0) Rr++;
        long[] x0 = new long[n]; Arrays.fill(x0, -Rr);
        while (true) {
            long e0 = q(f[1], x0);
            if (BigInteger.valueOf(e0).multiply(den).compareTo(num) <= 0) { long[] x = mv(f[3], x0); if (q(f[0], x) != e0) throw new IllegalStateException("isometrie"); out.add(x); }
            int i = 0; while (i < n && x0[i] == Rr) { x0[i] = -Rr; i++; }
            if (i == n) break; x0[i]++;
        }
        return out;
    }

    public static void main(String[] a) {
        long graine = a.length > 0 ? Long.parseLong(a[0]) : 20261010L; int nb = a.length > 1 ? Integer.parseInt(a[1]) : 300;
        // ---- 1. E8 (diagramme de Dynkin : chaîne 0-1-2-3-4-5-6, sommet 7 lié à 4 ; bras de longueurs 1, 2, 4)
        long[][] E8 = new long[8][8];
        for (int i = 0; i < 8; i++) E8[i][i] = 2;
        for (int i = 0; i < 6; i++) E8[i][i + 1] = E8[i + 1][i] = -1;
        E8[4][7] = E8[7][4] = -1;
        long[][] Zr = new long[8][8];
        for (int[] cfg : new int[][]{{0, 0}, {3, 3}, {2, 7}, {6, 6}, {1, 5}}) {
            long[] r = lancer(E8, E8, Zr, 1, 1, 1, 4, 1, 0, cfg[0], cfg[1], 0.5, true, new HashSet<>());
            ok(r[0] == 1200, "E8 D=" + cfg[0] + " Dmax=" + cfg[1] + " : " + r[0] + " u (1200 attendus), " + r[2] + " taches");
            long[] r2 = lancer(E8, E8, Zr, 1, 1, 1, 2, 1, 0, cfg[0], cfg[1], 0.5, true, new HashSet<>());
            ok(r2[0] == 120, "E8 norme 2 : " + r2[0]);
        }
        System.out.println("E8 : " + controles + " controles, " + echecs + " echecs");
        // ---- 2. formes aléatoires : comparaison ensembliste avec la boîte exhaustive
        Random R = new Random(graine); long totU = 0, totT = 0, frontieres = 0;
        for (int essai = 0; essai < nb; essai++) {
            int n = 2 + R.nextInt(3);
            long[] muA = new long[1], muB = new long[1];
            long[][][] fA = forme(R, n, 1 + R.nextInt(3), muA), fB = forme(R, n, 1 + R.nextInt(2), muB);
            long DA = 1 + R.nextInt(6), DB = 1 + R.nextInt(3), d = 1 + R.nextInt(4);
            long[][] T = new long[n][n]; for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) T[i][j] = R.nextInt((int) (2 * d + 1)) - d;
            long BAd = 1 + R.nextInt(3), BAn = (2 + R.nextInt(10)) * BAd / (1 + R.nextInt(2)) + R.nextInt(2);
            long S = 3 + R.nextInt(8);
            int D = R.nextInt(n + 1), Dmax = D + R.nextInt(3); double seuil = R.nextDouble();
            Set<String> obtenu = new HashSet<>();
            long[] r = lancer(fA[0], fB[0], T, DA, DB, d, BAn, BAd, S, D, Dmax, seuil, false, obtenu);
            // référence exhaustive
            Set<String> attendu = new HashSet<>(); long nu = 0;
            for (long[] u : boite(fA, muA[0], BigInteger.valueOf(DA * BAn), BigInteger.valueOf(BAd))) {
                int h = n - 1; while (h >= 0 && u[h] == 0) h--;
                if (h < 0 || u[h] < 0) continue;                                 // u != 0, dernière coordonnée non nulle > 0
                nu++;
                long la = q(fA[0], u);
                if (la * BAd == DA * BAn) frontieres++;
                long[] t = mv(T, u);
                // w~Bw <= DB d^2 (S DA - la) / DA
                for (long[] w : boite(fB, muB[0], BigInteger.valueOf(DB * d * d).multiply(BigInteger.valueOf(S * DA - la)), BigInteger.valueOf(DA))) {
                    long[] y = new long[n]; boolean dans = true;
                    for (int i = 0; i < n && dans; i++) { long z = w[i] - t[i]; if (Math.floorMod(z, d) != 0) dans = false; else y[i] = z / d; }
                    if (!dans) continue;
                    if (BigInteger.valueOf(la * DB * d * d + DA * q(fB[0], w)).compareTo(BigInteger.valueOf(S * DA * DB * d * d)) == 0) frontieres++;
                    attendu.add(Arrays.toString(u) + Arrays.toString(y));
                }
            }
            ok(r[0] == nu, "essai " + essai + " : u " + r[0] + " != " + nu);
            ok(obtenu.equals(attendu), "essai " + essai + " : touches " + obtenu.size() + " != " + attendu.size());
            ok(r[1] == attendu.size(), "essai " + essai + " : compteur de touches");
            totU += nu; totT += attendu.size();
        }
        System.out.println("FORMES : " + nb + " essais (graine " + graine + ", F=" + Rang88CertZ.F + ", verif=" + Rang88CertZ.VERIF + ") ; u compares " + totU + " ; touches comparees " + totT + " ; cas de frontiere exacte " + frontieres);
        System.out.println("TOTAL : " + controles + " controles, " + echecs + " echecs");
        System.out.println(echecs == 0 ? "TEST_OK" : "TEST_ECHEC");
        System.exit(echecs == 0 ? 0 : 1);
    }
}
