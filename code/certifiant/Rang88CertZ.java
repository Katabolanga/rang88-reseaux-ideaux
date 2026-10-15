import java.io.*;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

/**
 * Rang88CertZ — version CERTIFIANTE (non-omission) du critère 6, à CENTRES ENTIERS EXACTS, avec CHECKPOINT.
 * Agent Claude, 10 octobre 2026.  Dérivée de Rang88CertRoot (Codex root, SHA-256 9eff0c1f...), dont elle reprend
 * L1 (LDL^T rationnelle), L2 (encadre), la récursion, la normalisation de signe, la structure du cache et les
 * feuilles exactes.  Seule différence scientifique : les sommes partielles des centres ne sont plus des intervalles
 * de doubles mais des ENTIERS EXACTS (virgule fixe 2^-F, arithmétique long contrôlée), cf. lemmes Z1-Z5.
 * Mêmes entrées que Rang88Gen / Rang88CertRoot (prefixe_A.gram, _B.gram, _T.mat, _meta.txt de prep_java.gp).
 *
 * Chaque balise [Lx]/[Zx] renvoie au lemme de même nom de certifiant/PREUVE_NON_OMISSION.md.
 *
 * Usage : java [-Dopt=val ...] Rang88CertZ run    prefixe BAnum BAden S fils [D]
 *         java [-Dopt=val ...] Rang88CertZ compte prefixe BAnum BAden fils [D]
 *         java [-Dopt=val ...] Rang88CertZ taches prefixe BAnum BAden S fils [D]     (catalogue seul)
 * Options : -DF=40        bits de la virgule fixe des q_ij                       [Z1]
 *           -DDmax=D      profondeur maximale du découpage adaptatif (>= D)      [Z7]
 *           -Dseuil=0.5   une tâche est émise à la profondeur D si PL >= seuil * B_U, sinon découpée jusqu'à Dmax
 *           -Dckpt=f      fichier checkpoint (tâches terminées ; reprise automatique)   [Z10]
 *           -Dcat=f       écrit le catalogue des tâches
 *           -Ddebut=a -Dfin=b   ne traite que les tâches d'indice a <= t < b ; -Dliste=f : indices lus dans f
 *           -Dveille=600  période du journal de veille (s) ; -DmaxImpr=200 ; -Dverif=1 : recalcul exact des caches
 *           -DstopTouche=1  après une première touche, les tâches non commencées ne sont pas exécutées (couverture partielle)
 * Code de sortie : 0 = sélection entièrement traitée ; 2 = exception (aucun certificat) ; 3 = arguments.
 */
public strictfp class Rang88CertZ {

    // ------------------------------------------------------------------ options
    static final int F = Integer.getInteger("F", 40);
    static final long DEUXF = 1L << F;
    static final double DEUXF_D = (double) DEUXF, INV_DEUXF = 1.0 / DEUXF_D;   // puissances de 2 : exactes
    static final boolean VERIF = Integer.getInteger("verif", 0) != 0;
    static { if (F < 8 || F > 52) throw new IllegalArgumentException("F hors [8,52]"); }

    // ------------------------------------------------------------------ lecture
    static String[] jetons(String f) throws IOException {
        StringBuilder sb = new StringBuilder(); String l;
        try (BufferedReader br = new BufferedReader(new FileReader(f))) { while ((l = br.readLine()) != null) sb.append(l).append(' '); }
        return sb.toString().trim().split("\\s+");
    }
    static long[][] lireCarree(String f) throws IOException {
        String[] t = jetons(f); int r = Integer.parseInt(t[0]), c = Integer.parseInt(t[1]);
        if (r < 1 || r != c || t.length != 2 + r * c) throw new IOException("matrice non carree ou nombre de jetons incorrect dans " + f);
        long[][] M = new long[r][c]; int k = 2;
        for (int i = 0; i < r; i++) for (int j = 0; j < c; j++) M[i][j] = new BigInteger(t[k++]).longValueExact();
        return M;
    }

    // ------------------------------------------------------------------ [L2] encadrement exact d'un rationnel p/q (q > 0)
    static int cmpDoubleRat(double x, BigInteger p, BigInteger q) {   // signe de x - p/q, exact
        return new BigDecimal(x).multiply(new BigDecimal(q)).compareTo(new BigDecimal(p));   // BigDecimal(double) = valeur binaire exacte
    }
    static double[] encadre(BigInteger p, BigInteger q) {
        if (q.signum() <= 0) throw new ArithmeticException("denominateur");
        double x = new BigDecimal(p).divide(new BigDecimal(q), java.math.MathContext.DECIMAL128).doubleValue();
        if (!Double.isFinite(x)) throw new ArithmeticException("non fini");
        double lo = x, hi = x;
        while (cmpDoubleRat(lo, p, q) > 0) { lo = Math.nextDown(lo); if (!Double.isFinite(lo)) throw new ArithmeticException("non fini"); }
        while (cmpDoubleRat(hi, p, q) < 0) { hi = Math.nextUp(hi); if (!Double.isFinite(hi)) throw new ArithmeticException("non fini"); }
        return new double[]{lo, hi};
    }

    // ------------------------------------------------------------------ [L3] voisins flottants extérieurs (refus si non fini)
    // Pour x > 0 fini, l'ordre des doubles est celui de leurs motifs binaires : motif - 1 = prédécesseur, motif + 1 = successeur.
    static double dn(double x) {
        if (x > 0.0 && x <= Double.MAX_VALUE) return Double.longBitsToDouble(Double.doubleToRawLongBits(x) - 1L);   // = Math.nextDown(x), fini
        if (!(x > -Double.MAX_VALUE && x <= Double.MAX_VALUE)) throw new ArithmeticException("non fini");
        return Math.nextDown(x);
    }
    static double up(double x) {
        if (x > 0.0 && x < Double.MAX_VALUE) return Double.longBitsToDouble(Double.doubleToRawLongBits(x) + 1L);    // = Math.nextUp(x), fini
        if (!(x >= -Double.MAX_VALUE && x < Double.MAX_VALUE)) throw new ArithmeticException("non fini");
        return Math.nextUp(x);
    }
    /** [Z4] plancher EXACT de a / M (M > 0).  L'estimation flottante n'est qu'un point de départ : les deux boucles
     *  ne s'arrêtent que lorsque q M <= a < (q + 1) M, vérifié en entiers exacts. */
    static long plancherDiv(long a, long M, double invM) {
        final double est = Math.floor((double) a * invM);
        if (!(est > -0x1p62 && est < 0x1p62)) throw new ArithmeticException("quotient hors domaine");
        long q = (long) est, p = Math.multiplyExact(q, M);
        while (p > a) { q--; p = Math.subtractExact(p, M); }
        while (Math.subtractExact(a, p) >= M) { q++; p = Math.addExact(p, M); }
        return q;
    }

    // ------------------------------------------------------------------ rationnels exacts (num, den > 0), réduits
    static BigInteger[] red(BigInteger a, BigInteger b) { if (b.signum() == 0) throw new ArithmeticException("division par zero"); if (b.signum() < 0) { a = a.negate(); b = b.negate(); } BigInteger g = a.gcd(b); return new BigInteger[]{a.divide(g), b.divide(g)}; }
    static BigInteger[] mul(BigInteger[] x, BigInteger[] y) { return red(x[0].multiply(y[0]), x[1].multiply(y[1])); }
    static BigInteger[] add(BigInteger[] x, BigInteger[] y) { return red(x[0].multiply(y[1]).add(y[0].multiply(x[1])), x[1].multiply(y[1])); }
    static BigInteger[] sub(BigInteger[] x, BigInteger[] y) { return red(x[0].multiply(y[1]).subtract(y[0].multiply(x[1])), x[1].multiply(y[1])); }
    static BigInteger[] div(BigInteger[] x, BigInteger[] y) { return red(x[0].multiply(y[1]), x[1].multiply(y[0])); }
    static BigInteger[] rat(long a) { return new BigInteger[]{BigInteger.valueOf(a), BigInteger.ONE}; }

    // ------------------------------------------------------------------ [L1][Z1] LDL^T rationnelle exacte, q en virgule fixe
    static final class FormeZ {
        final int n; final long[][] G;
        final double[] dL;          // [L2] 0 < dL[i] <= d_i
        final long[][] qI;          // [Z1] qI[i][j] = floor(2^F q_ij), j > i
        final double maxAbsQ; final String resume;
        FormeZ(long[][] G) {
            n = G.length; this.G = G;
            for (int i = 0; i < n; i++) { if (G[i].length != n) throw new IllegalArgumentException("non carree"); for (int j = 0; j < n; j++) if (G[i][j] != G[j][i]) throw new IllegalArgumentException("non symetrique"); }
            BigInteger[][] dr = new BigInteger[n][]; BigInteger[][][] q = new BigInteger[n][n][];
            dL = new double[n]; qI = new long[n][n]; double mq = 0;
            for (int i = 0; i < n; i++) {
                BigInteger[] s = rat(G[i][i]);                      // d_i = G_ii - sum_{k<i} d_k q_ki^2
                for (int k = 0; k < i; k++) s = sub(s, mul(dr[k], mul(q[k][i], q[k][i])));
                if (s[0].signum() <= 0) throw new IllegalStateException("forme non definie positive (pivot exact <= 0)");
                dr[i] = s;
                dL[i] = encadre(s[0], s[1])[0];
                if (!(dL[i] > 0)) throw new IllegalStateException("minorant de d_i non strictement positif");
                for (int j = i + 1; j < n; j++) {
                    BigInteger[] t = rat(G[i][j]);                  // q_ij = (G_ij - sum_{k<i} d_k q_ki q_kj) / d_i
                    for (int k = 0; k < i; k++) t = sub(t, mul(dr[k], mul(q[k][i], q[k][j])));
                    q[i][j] = div(t, s);
                    BigInteger[] qr = q[i][j][0].shiftLeft(F).divideAndRemainder(q[i][j][1]);   // troncature vers 0
                    BigInteger fl = (qr[1].signum() < 0) ? qr[0].subtract(BigInteger.ONE) : qr[0];   // plancher exact
                    // contrôle exact : fl <= 2^F q < fl + 1
                    BigInteger num = q[i][j][0].shiftLeft(F), den = q[i][j][1];
                    if (fl.multiply(den).compareTo(num) > 0 || fl.add(BigInteger.ONE).multiply(den).compareTo(num) <= 0) throw new IllegalStateException("plancher");
                    qI[i][j] = fl.longValueExact();
                    mq = Math.max(mq, Math.abs(q[i][j][0].doubleValue() / q[i][j][1].doubleValue()));
                }
            }
            // [L1] contrôle exact de l'identité G_ij = sum_{k <= min(i,j)} d_k q_ki q_kj (q_kk = 1)
            for (int i = 0; i < n; i++) for (int j = i; j < n; j++) {
                BigInteger[] s = (i == j) ? dr[i] : mul(dr[i], q[i][j]);
                for (int k = 0; k < i; k++) s = add(s, mul(dr[k], mul(q[k][i], q[k][j])));
                if (!s[1].equals(BigInteger.ONE) || !s[0].equals(BigInteger.valueOf(G[i][j]))) throw new IllegalStateException("identite LDL^T fausse en (" + i + "," + j + ")");
            }
            maxAbsQ = mq;
            double mn = Double.MAX_VALUE, mx = 0; for (double x : dL) { mn = Math.min(mn, x); mx = Math.max(mx, x); }
            resume = "min dL = " + mn + " , max dL = " + mx + " , max |q| ~ " + mq;
        }
        long normeExacte(long[] y) {   // y~ G y exact, ou ArithmeticException
            long s = 0;
            for (int i = 0; i < n; i++) { if (y[i] == 0) continue; long t = 0; for (int j = 0; j < n; j++) t = Math.addExact(t, Math.multiplyExact(G[i][j], y[j])); s = Math.addExact(s, Math.multiplyExact(y[i], t)); }
            return s;
        }
    }

    // ------------------------------------------------------------------ données (immuables après chargement)
    static int n; static FormeZ FA, FB; static long[][] TnL;
    static long BAnum, BAden, S, DAl, DBl, dl; static double bornAU, DA_D;
    static long DA_BAnum, DBd2, S_DA; static BigInteger DA, DB, d, d2;
    static boolean modeCompte = false; static int maxImpr = Integer.getInteger("maxImpr", 200);
    static final AtomicLong imprimes = new AtomicLong(0);
    interface Recepteur { void touche(long la, long[] u, long[] y, long[] w, BigInteger e); }
    static volatile Recepteur recepteur = null;   // tests seulement

    static final class Compteurs { long u = 0, cvp = 0, noeudsA = 0, noeudsB = 0, touches = 0; final long[] hist = new long[64]; }
    static final class Tache {
        final int niveau; final long[] y; final double PL; final boolean zero;
        Tache(int niveau, long[] y, double PL, boolean zero) { this.niveau = niveau; this.y = y; this.PL = PL; this.zero = zero; }
    }

    /** Énumérateur certifié.  Coordonnées exactes w_j = t_j + pas * y_j (long) ; côté court : t = 0, pas = 1. */
    static final class EnumZ {
        final FormeZ Fm; final int n; final long[][] qI; final double[] dL;
        final long[] y, w, t;            // w_j = t_j + pas y_j, exact
        final long[] absW;               // [Z1] absW[j] = sum_{l >= j} |w_l| ; absW[n] = 0
        final long[][] cS;               // [Z2] cS[k][j] = sum_{l >= j} qI[k][l] w_l (j > k) ; cS[k][n] = 0
        final int[] top;                 // [Z2] ligne k à jour pour les colonnes j > top[k]
        long pas = 1, M = DEUXF; double invM = INV_DEUXF;   // M = pas 2^F exact ; invM ~ 1/M (estimation seulement)
        void pas(long p) { if (p < 1) throw new IllegalArgumentException("pas"); pas = p; M = Math.multiplyExact(p, DEUXF); invM = 1.0 / (double) M; }
        double borneU; long noeuds = 0;
        boolean signe = false; Runnable feuille;
        boolean gen = false; int arretHaut, arretBas; double seuilPL; List<Tache> out;
        EnumZ(FormeZ Fm) {
            this.Fm = Fm; n = Fm.n; qI = Fm.qI; dL = Fm.dL; y = new long[n]; w = new long[n]; t = new long[n];
            absW = new long[n + 1]; cS = new long[n][n + 1]; top = new int[n];
        }
        void raz() { Arrays.fill(top, n - 1); absW[n] = 0; for (int k = 0; k < n; k++) cS[k][n] = 0; }
        void fixe(int i, long yv, long wv) { y[i] = yv; w[i] = wv; absW[i] = Math.addExact(absW[i + 1], wv < 0 ? Math.negateExact(wv) : wv); }
        /** [Z2] met à jour la ligne k du cache (entiers exacts) */
        void descend(int k) {
            if (k >= 1 && top[k - 1] < top[k]) top[k - 1] = top[k];
            final long[] c = cS[k], q = qI[k];
            for (int j = top[k]; j > k; j--) c[j] = Math.addExact(c[j + 1], Math.multiplyExact(q[j], w[j]));
            top[k] = k;
        }
        void verifie(int i, long Sg, long W) {   // -Dverif=1 : recalcul exact indépendant du cache
            BigInteger s = BigInteger.ZERO, a = BigInteger.ZERO;
            for (int j = i + 1; j < n; j++) { s = s.add(BigInteger.valueOf(qI[i][j]).multiply(BigInteger.valueOf(w[j]))); a = a.add(BigInteger.valueOf(w[j]).abs()); if (w[j] != Math.addExact(t[j], Math.multiplyExact(pas, y[j]))) throw new IllegalStateException("w incoherent"); }
            if (!s.equals(BigInteger.valueOf(Sg)) || !a.equals(BigInteger.valueOf(W))) throw new IllegalStateException("cache faux au niveau " + i);
        }
        /** niveau i ; PL = minorant certifié de l'énergie exacte des niveaux > i [Z5] */
        void rec(int i, double PL, boolean zeroDessus) {
            noeuds++;
            if (gen && i <= arretHaut && (i <= arretBas || PL >= seuilPL)) { out.add(new Tache(i, y.clone(), PL, zeroDessus)); return; }   // [Z7]
            final long Sg = cS[i][i + 1], W = absW[i + 1];           // [Z1][Z2] 2^F T_i dans [Z - W, Z + W], Z = 2^F w_i + Sg
            if (VERIF) verifie(i, Sg, W);
            final double reste = up(borneU - PL);                     // [Z3][Z4] reste >= budget exact - énergie exacte fixée
            if (reste < 0) return;                                    // [Z5] alors énergie fixée > budget : rien d'admissible dessous
            final double r = up(Math.sqrt(up(reste / dL[i])));       // [Z4] r >= |T_i| pour tout prolongement admissible
            final double rs = r * DEUXF_D;                            // exact (puissance de 2) si fini
            if (!(rs < 0x1p62)) throw new ArithmeticException("rayon hors domaine certifie");
            final long H = Math.addExact((long) Math.ceil(rs), W);    // [Z4] |Z| <= H, Z = 2^F w_i + Sg = C + M y_i
            final long C = Math.addExact(Math.multiplyExact(t[i], DEUXF), Sg);
            long yhi = plancherDiv(Math.subtractExact(H, C), M, invM);                    // [Z4] floor((H - C) / M)
            long ylo = Math.negateExact(plancherDiv(Math.addExact(H, C), M, invM));       // [Z4] ceil((-H - C) / M) = -floor((H + C) / M)
            if (signe && zeroDessus) { if (ylo < 0) ylo = 0; if (i == 0 && ylo < 1) ylo = 1; }   // [Z6]
            if (ylo > yhi) return;
            final double dLi = dL[i];
            long Z = Math.addExact(C, Math.multiplyExact(M, ylo));
            for (long yv = ylo; ; yv++) {
                if (Z == Long.MIN_VALUE) throw new ArithmeticException("Z hors domaine");
                final long delta = (Z < 0 ? -Z : Z) - W;              // [Z5] |2^F T_i| >= delta (exact)
                double PL2 = PL; boolean garde = true;
                if (delta > 0) {
                    final double dd = dn((double) delta) * INV_DEUXF;   // [L3] 0 < dd <= delta / 2^F <= |T_i|
                    PL2 = dn(PL + dn(dn(dd * dd) * dLi));               // [Z5] PL2 <= énergie exacte des niveaux >= i
                    garde = !(PL2 > borneU);                            // [Z5] coupe sûre si PL2 > B_U
                }
                if (garde) {
                    fixe(i, yv, Math.addExact(t[i], Math.multiplyExact(pas, yv)));
                    if (i == 0) feuille.run();                          // [Z8]
                    else {
                        if (top[i - 1] < i) top[i - 1] = i;             // [Z2]
                        descend(i - 1);
                        rec(i - 1, PL2, zeroDessus && yv == 0);
                    }
                }
                if (yv == yhi) break;
                Z = Math.addExact(Z, M);
            }
        }
    }

    static final class Travail {
        Compteurs C = new Compteurs();
        final EnumZ eA = new EnumZ(FA), eB = new EnumZ(FB);
        long laCourant;
        Travail() { eA.signe = true; eA.borneU = bornAU; eA.pas(1); eB.pas(dl); eA.feuille = this::feuilleA; eB.feuille = this::feuilleB; }
        /** [Z8] feuille du côté court : tests exacts, puis CVP certifié dans la fibre */
        void feuilleA() {
            final long[] u = eA.y;
            final long la = FA.normeExacte(u);
            if (la <= 0) return;                                              // u = 0 exclu [Z6]
            if (Math.multiplyExact(la, BAden) > DA_BAnum) return;             // exact : u~Au / DA <= BAnum / BAden
            C.u++;
            C.hist[(int) Math.min(63L, Math.multiplyExact(la, 10L) / DAl)]++;
            if (modeCompte) return;
            for (int i = 0; i < n; i++) {                                     // t = Tn u exact
                long num = 0; final long[] Ti = TnL[i];
                for (int j = 0; j < n; j++) if (u[j] != 0) num = Math.addExact(num, Math.multiplyExact(Ti[j], u[j]));
                eB.t[i] = num;
            }
            final long N = Math.multiplyExact(DBd2, Math.subtractExact(S_DA, la));   // budget exact de w~Bw : N / DA
            if (N < 0) return;                                                // énergie courte seule > S : aucune touche possible
            eB.borneU = up(up((double) N) / DA_D);                            // [Z3] >= N / DA
            laCourant = la; C.cvp++;
            eB.raz();
            final long avant = eB.noeuds;
            eB.rec(n - 1, 0.0, false);
            C.noeudsB += eB.noeuds - avant;
        }
        /** [Z8] feuille de la fibre : contrôle EXACT en BigInteger */
        void feuilleB() {
            final long[] u = eA.y, yy = eB.y, ww = eB.w;
            BigInteger[] wb = new BigInteger[n];
            for (int i = 0; i < n; i++) {
                BigInteger tt = d.multiply(BigInteger.valueOf(yy[i]));
                for (int j = 0; j < n; j++) if (u[j] != 0) tt = tt.add(BigInteger.valueOf(TnL[i][j]).multiply(BigInteger.valueOf(u[j])));
                if (!tt.equals(BigInteger.valueOf(ww[i]))) throw new IllegalStateException("w de la feuille incoherent");
                wb[i] = tt;
            }
            BigInteger e = BigInteger.ZERO;
            for (int i = 0; i < n; i++) { if (wb[i].signum() == 0) continue; BigInteger tt = BigInteger.ZERO; for (int j = 0; j < n; j++) if (wb[j].signum() != 0 && FB.G[i][j] != 0) tt = tt.add(wb[j].multiply(BigInteger.valueOf(FB.G[i][j]))); e = e.add(wb[i].multiply(tt)); }
            BigInteger gauche = BigInteger.valueOf(laCourant).multiply(DB).multiply(d2).add(DA.multiply(e));
            BigInteger droite = BigInteger.valueOf(S).multiply(DA).multiply(DB).multiply(d2);
            if (gauche.compareTo(droite) > 0) return;
            C.touches++;
            Recepteur rc = recepteur;
            if (rc != null) { rc.touche(laCourant, u.clone(), yy.clone(), ww.clone(), e); return; }
            String txt = "TOUCHE court=" + laCourant + "/" + DA + " fibre(num)=" + e + "/(" + DB + "*" + d + "^2) u=" + Arrays.toString(u) + " y=" + Arrays.toString(yy);
            ecrireTouche(txt);
            if (imprimes.incrementAndGet() <= maxImpr) synchronized (Rang88CertZ.class) { System.out.println(txt); System.out.flush(); }
        }
        /** [Z7] exécute une tâche du catalogue ; renvoie ses compteurs propres */
        Compteurs executer(Tache tc) {
            C = new Compteurs();
            final EnumZ e = eA; e.raz();
            for (int i = n - 1; i > tc.niveau; i--) e.fixe(i, tc.y[i], tc.y[i]);
            e.descend(tc.niveau);
            final long avant = e.noeuds;
            e.rec(tc.niveau, tc.PL, tc.zero);
            C.noeudsA = e.noeuds - avant;
            return C;
        }
    }

    // ------------------------------------------------------------------ chargement et catalogue
    static void charger(long[][] A, long[][] B, long[][] T, long DA_, long DB_, long d_, long BAn, long BAd, long S_) {
        if (A.length < 1 || A.length != B.length || T.length != A.length) throw new IllegalArgumentException("rangs");
        for (long[] row : T) if (row.length != A.length) throw new IllegalArgumentException("colonnes T");
        if (DA_ <= 0 || DB_ <= 0 || d_ <= 0 || BAn < 0 || BAd <= 0 || S_ < 0) throw new IllegalArgumentException("domaine des parametres");
        if (DA_ > (1L << 53)) throw new IllegalArgumentException("DA > 2^53");
        FA = new FormeZ(A); FB = new FormeZ(B); n = FA.n; TnL = T;
        DAl = DA_; DBl = DB_; dl = d_; BAnum = BAn; BAden = BAd; S = S_;
        DA = BigInteger.valueOf(DA_); DB = BigInteger.valueOf(DB_); d = BigInteger.valueOf(d_); d2 = d.multiply(d);
        DA_D = (double) DA_;                                                    // exact (DA <= 2^53)
        DA_BAnum = Math.multiplyExact(DA_, BAn); DBd2 = Math.multiplyExact(DB_, Math.multiplyExact(d_, d_)); S_DA = Math.multiplyExact(S_, DA_);
        bornAU = encadre(DA.multiply(BigInteger.valueOf(BAn)), BigInteger.valueOf(BAd))[1];   // [Z3] côté court : >= DA BAnum / BAden
    }
    /** [Z7] catalogue : même récursion certifiée, arrêt adaptatif entre les profondeurs D et Dmax */
    static List<Tache> catalogue(int D, int Dmax, double seuil, long[] noeudsGen) {
        EnumZ g = new EnumZ(FA); g.signe = true; g.borneU = bornAU; g.pas(1); g.raz();
        g.gen = true; g.arretHaut = Math.max(0, n - 1 - D); g.arretBas = Math.max(0, n - 1 - Dmax); g.seuilPL = seuil * bornAU; g.out = new ArrayList<>();
        g.feuille = () -> { throw new IllegalStateException("feuille pendant la generation"); };
        g.rec(n - 1, 0.0, true);
        if (noeudsGen != null) noeudsGen[0] = g.noeuds;
        return g.out;
    }
    static String ligneTache(int t, Tache tc) {
        StringBuilder sb = new StringBuilder().append(t).append("|niv=").append(tc.niveau).append("|prefix=");
        for (int i = tc.niveau + 1; i < n; i++) { if (i > tc.niveau + 1) sb.append(","); sb.append(i).append("=").append(tc.y[i]); }
        return sb.append("|PL=").append(Double.toHexString(tc.PL)).append("|zero=").append(tc.zero).append("\n").toString();
    }
    static String hex(byte[] b) { StringBuilder sb = new StringBuilder(); for (byte x : b) sb.append(String.format(Locale.ROOT, "%02x", x & 255)); return sb.toString(); }
    static String shaFichier(String f) throws Exception { return hex(MessageDigest.getInstance("SHA-256").digest(Files.readAllBytes(Paths.get(f)))); }

    // ------------------------------------------------------------------ [Z10] checkpoint (ajout seul, une ligne complète par tâche terminée)
    static FileChannel ckptCanal = null; static final Object ckptVerrou = new Object(); static String touchesFichier = null;
    static void ecrireCkpt(String ligne) throws IOException {
        if (ckptCanal == null) return;
        synchronized (ckptVerrou) { ckptCanal.write(java.nio.ByteBuffer.wrap(ligne.getBytes(StandardCharsets.US_ASCII))); ckptCanal.force(false); }
    }
    static void ecrireTouche(String txt) {
        if (touchesFichier == null) return;
        synchronized (ckptVerrou) {
            try (FileChannel c = FileChannel.open(Paths.get(touchesFichier), StandardOpenOption.CREATE, StandardOpenOption.WRITE, StandardOpenOption.APPEND)) { c.write(java.nio.ByteBuffer.wrap((txt + "\n").getBytes(StandardCharsets.US_ASCII))); c.force(false); }
            catch (IOException ex) { throw new UncheckedIOException(ex); }
        }
    }
    static String ligneResultat(int t, Compteurs c) {
        StringBuilder h = new StringBuilder();
        for (int i = 0; i < 64; i++) if (c.hist[i] != 0) { if (h.length() > 0) h.append(","); h.append(i).append(":").append(c.hist[i]); }
        return "T|" + t + "|U=" + c.u + "|CVP=" + c.cvp + "|NA=" + c.noeudsA + "|NB=" + c.noeudsB + "|TOUCHES=" + c.touches + "|HIST=" + h + "|FIN\n";
    }
    static Compteurs lireResultat(String l, int[] indice) {
        String[] p = l.split("\\|", -1);
        if (p.length != 9 || !p[0].equals("T") || !p[8].equals("FIN")) return null;
        Compteurs c = new Compteurs(); indice[0] = Integer.parseInt(p[1]);
        c.u = val(p[2], "U="); c.cvp = val(p[3], "CVP="); c.noeudsA = val(p[4], "NA="); c.noeudsB = val(p[5], "NB="); c.touches = val(p[6], "TOUCHES=");
        if (!p[7].startsWith("HIST=")) throw new IllegalStateException("checkpoint : " + l);
        String hs = p[7].substring(5);
        if (!hs.isEmpty()) for (String kv : hs.split(",")) { String[] ab = kv.split(":"); c.hist[Integer.parseInt(ab[0])] = Long.parseLong(ab[1]); }
        return c;
    }
    static long val(String s, String cle) { if (!s.startsWith(cle)) throw new IllegalStateException("checkpoint : champ " + cle); return Long.parseLong(s.substring(cle.length())); }

    public static void main(String[] a) {
        int code;
        try { code = lance(a); } catch (Throwable t) { System.out.println("ERREUR " + t); t.printStackTrace(System.out); code = 2; }
        System.out.flush(); System.exit(code);
    }

    static int lance(String[] a) throws Exception {
        final long t0 = System.currentTimeMillis();
        if (a.length < 5) { System.out.println("arguments insuffisants"); return 3; }
        final String mode = a[0];
        modeCompte = mode.equals("compte");
        final boolean catalogueSeul = mode.equals("taches");
        if (!modeCompte && !catalogueSeul && !mode.equals("run")) { System.out.println("mode inconnu " + mode); return 3; }
        final String pre = a[1]; final long ban = Long.parseLong(a[2]), bad = Long.parseLong(a[3]);
        int k = 4; final long s_ = modeCompte ? 0 : Long.parseLong(a[k++]);
        final int nf = Integer.parseInt(a[k++]); final int D = a.length > k ? Integer.parseInt(a[k++]) : 6;
        if (k != a.length || nf < 1 || D < 0) { System.out.println("domaine des parametres"); return 3; }
        final int Dmax = Integer.getInteger("Dmax", D); final double seuil = Double.parseDouble(System.getProperty("seuil", "0.5"));
        if (Dmax < D || !(seuil >= 0)) { System.out.println("Dmax < D ou seuil"); return 3; }
        final String ckpt = System.getProperty("ckpt"), cat = System.getProperty("cat"), liste = System.getProperty("liste");
        final int veilleS = Integer.getInteger("veille", 600);
        String[] meta = jetons(pre + "_meta.txt"); if (meta.length != 3) throw new IOException("meta");
        charger(lireCarree(pre + "_A.gram"), lireCarree(pre + "_B.gram"), lireCarree(pre + "_T.mat"),
                Long.parseLong(meta[0]), Long.parseLong(meta[1]), Long.parseLong(meta[2]), ban, bad, s_);
        final String params = "mode=" + mode + "|n=" + n + "|BA=" + BAnum + "/" + BAden + "|S=" + S + "|DA=" + DA + "|DB=" + DB + "|d=" + d + "|F=" + F + "|D=" + D + "|Dmax=" + Dmax + "|seuil=" + seuil;
        System.out.println("Rang88CertZ " + mode + " : " + pre + " ; " + params + " ; " + nf + " fils ; verif=" + VERIF);
        System.out.println("  JVM " + System.getProperty("java.vm.name") + " " + System.getProperty("java.version") + " ; " + System.getProperty("os.name") + " " + System.getProperty("os.arch") + " ; processeurs " + Runtime.getRuntime().availableProcessors() + " ; PID " + ProcessHandle.current().pid() + " ; " + new Date());
        final String hA = shaFichier(pre + "_A.gram"), hB = shaFichier(pre + "_B.gram"), hT = shaFichier(pre + "_T.mat"), hM = shaFichier(pre + "_meta.txt");
        System.out.println("  ENTREES SHA-256 : A " + hA + " ; B " + hB + " ; T " + hT + " ; meta " + hM);
        List<String> noms = new ArrayList<>(); noms.add("Rang88CertZ"); for (Class<?> c : Rang88CertZ.class.getDeclaredClasses()) noms.add(c.getName()); Collections.sort(noms);
        StringBuilder cl = new StringBuilder("  CLASSES SHA-256 :");
        for (String nm : noms) try (InputStream in = Rang88CertZ.class.getResourceAsStream("/" + nm + ".class")) { if (in == null) throw new IOException("classe introuvable " + nm); cl.append(" ").append(nm).append("=").append(hex(MessageDigest.getInstance("SHA-256").digest(in.readAllBytes()))); }
        System.out.println(cl);
        // [Z10] lien du checkpoint aux entrées et aux classes réellement chargées
        final String lien = "entrees=" + hex(MessageDigest.getInstance("SHA-256").digest((hA + hB + hT + hM).getBytes(StandardCharsets.US_ASCII)))
            + "|classes=" + hex(MessageDigest.getInstance("SHA-256").digest(cl.toString().getBytes(StandardCharsets.US_ASCII)));
        System.out.println("  LIEN " + lien);
        System.out.println("  LDL^T exacte verifiee : court : " + FA.resume + " ; fibre : " + FB.resume + " ; B_U(court) = " + bornAU);

        // ---- catalogue certifié [Z7]
        long[] ng = new long[1];
        final List<Tache> taches = catalogue(D, Dmax, seuil, ng);
        final int nt = taches.size();
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        final String enTete = "R88Z_TACHES_V1|" + params.substring(params.indexOf("|n=") + 1) + "|total=" + nt + "\n";
        md.update(enTete.getBytes(StandardCharsets.US_ASCII));
        BufferedWriter cw = cat == null ? null : Files.newBufferedWriter(Paths.get(cat), StandardCharsets.US_ASCII);
        if (cw != null) cw.write(enTete);
        int[] parNiv = new int[n];
        for (int t = 0; t < nt; t++) { String l = ligneTache(t, taches.get(t)); md.update(l.getBytes(StandardCharsets.US_ASCII)); if (cw != null) cw.write(l); parNiv[taches.get(t).niveau]++; }
        if (cw != null) cw.close();
        final String shaCat = hex(md.digest());
        StringBuilder pn = new StringBuilder(); for (int i = n - 1; i >= 0; i--) if (parNiv[i] != 0) pn.append(" niv").append(i).append(":").append(parNiv[i]);
        System.out.println("  " + nt + " taches certifiees (" + ng[0] + " noeuds de generation) ;" + pn);
        System.out.println("CATALOGUE_SHA256 " + shaCat + " ; TOTAL_TACHES " + nt);
        if (catalogueSeul) { System.out.println("CATALOGUE_SEUL_AUCUNE_CERTIFICATION"); System.out.println("FIN [" + (System.currentTimeMillis() - t0) / 1000 + " s]"); return 0; }

        // ---- checkpoint : relecture [Z10]
        final Compteurs[] res = new Compteurs[nt];
        final String enTeteCk = "R88Z_CKPT_V1|" + params + "|total=" + nt + "|catalogue=" + shaCat + "|" + lien + "\n";
        int repris = 0;
        if (ckpt != null) {
            Path pc = Paths.get(ckpt);
            if (Files.exists(pc) && Files.size(pc) > 0) {
                byte[] brut = Files.readAllBytes(pc);
                String tout = new String(brut, StandardCharsets.US_ASCII);
                if (!tout.startsWith(enTeteCk)) throw new IllegalStateException("checkpoint incompatible (en-tete different) : " + ckpt);
                // seules les lignes complètes (terminées par \n) comptent ; un reste tronqué par un arrêt brutal est retiré du fichier
                final int valide = tout.lastIndexOf('\n') + 1; final int incompletes = valide < brut.length ? 1 : 0;
                String[] ls = tout.substring(0, valide).split("\n", -1);
                for (int i = 1; i < ls.length; i++) {
                    if (ls[i].isEmpty()) { if (i != ls.length - 1) throw new IllegalStateException("checkpoint : ligne vide " + i); continue; }
                    int[] idx = new int[1]; Compteurs c = lireResultat(ls[i], idx);
                    if (c == null) throw new IllegalStateException("checkpoint : ligne complete mal formee " + i);
                    if (idx[0] < 0 || idx[0] >= nt) throw new IllegalStateException("checkpoint : indice");
                    if (res[idx[0]] != null) throw new IllegalStateException("checkpoint : tache en double " + idx[0]);
                    res[idx[0]] = c; repris++;
                }
                if (incompletes > 0) try (FileChannel tr = FileChannel.open(pc, StandardOpenOption.WRITE)) { tr.truncate(valide); tr.force(true); }
                ckptCanal = FileChannel.open(pc, StandardOpenOption.WRITE, StandardOpenOption.APPEND);
                System.out.println("REPRISE : " + repris + " taches deja terminees lues dans " + ckpt + " (SHA-256 a la lecture " + hex(MessageDigest.getInstance("SHA-256").digest(brut)) + ")" + (incompletes > 0 ? " ; 1 ligne finale tronquee retiree (" + (brut.length - valide) + " octets)" : ""));
            } else {
                ckptCanal = FileChannel.open(pc, StandardOpenOption.CREATE, StandardOpenOption.WRITE, StandardOpenOption.APPEND);
                ecrireCkpt(enTeteCk);
                System.out.println("CHECKPOINT nouveau : " + ckpt);
            }
            touchesFichier = ckpt + ".touches";
        }
        // ---- sélection
        final boolean[] choisi = new boolean[nt];
        if (liste != null) { for (String tk : jetons(liste)) if (!tk.isEmpty()) choisi[Integer.parseInt(tk)] = true; }
        else { int deb = Integer.getInteger("debut", 0), fin = Integer.getInteger("fin", nt); if (deb < 0 || fin > nt || deb > fin) throw new IllegalArgumentException("debut/fin"); for (int t = deb; t < fin; t++) choisi[t] = true; }
        final List<Integer> aFaire = new ArrayList<>(); int selection = 0;
        for (int t = 0; t < nt; t++) if (choisi[t]) { selection++; if (res[t] == null) aFaire.add(t); }
        System.out.println("SELECTION " + selection + "/" + nt + " ; A_FAIRE " + aFaire.size() + " ; DEJA_AU_CHECKPOINT " + repris);

        // ---- exécution [Z7][Z10]
        final AtomicLong TERMINEES = new AtomicLong(0), enCours = new AtomicLong(0);
        final boolean stopTouche = Integer.getInteger("stopTouche", 0) != 0; final AtomicBoolean arret = new AtomicBoolean(false);
        final ExecutorService ex = Executors.newFixedThreadPool(nf);
        final ThreadLocal<Travail> tl = ThreadLocal.withInitial(Travail::new);
        final Set<Travail> vivants = ConcurrentHashMap.newKeySet();
        final AtomicLong aU = new AtomicLong(), aCvp = new AtomicLong(), aNA = new AtomicLong(), aNB = new AtomicLong(), aT = new AtomicLong();
        final List<Future<Compteurs>> fs = new ArrayList<>();
        for (final int t : aFaire) {
            final Tache tc = taches.get(t);
            fs.add(ex.submit(() -> {
                if (stopTouche && arret.get()) return null;     // tâche NON exécutée : jamais comptée comme terminée
                Travail w = tl.get(); vivants.add(w); enCours.incrementAndGet();
                Compteurs c = w.executer(tc);
                ecrireCkpt(ligneResultat(t, c));               // ligne écrite et forcée sur disque AVANT de déclarer la tâche terminée
                aU.addAndGet(c.u); aCvp.addAndGet(c.cvp); aNA.addAndGet(c.noeudsA); aNB.addAndGet(c.noeudsB); aT.addAndGet(c.touches);
                if (c.touches > 0) arret.set(true);
                enCours.decrementAndGet(); TERMINEES.incrementAndGet();
                return c;
            }));
        }
        ex.shutdown();
        final int dejaFaites = repris;
        ScheduledExecutorService veille = Executors.newSingleThreadScheduledExecutor(r -> { Thread th = new Thread(r); th.setDaemon(true); return th; });
        veille.scheduleAtFixedRate(() -> {
            long nA = 0, nB = 0; for (Travail w : vivants) { nA += w.eA.noeuds; nB += w.eB.noeuds; }
            System.out.println("  [veille] taches terminees " + TERMINEES.get() + "/" + aFaire.size() + " (+" + dejaFaites + " reprises ; " + enCours.get() + " en cours) ; u(terminees) " + aU.get() + " ; cvp " + aCvp.get()
                + " ; noeuds A ~" + nA + " B ~" + nB + " ; touches " + aT.get() + " [" + (System.currentTimeMillis() - t0) / 1000 + " s]");
            System.out.flush();
        }, veilleS, veilleS, TimeUnit.SECONDS);
        int faites = 0, sautees = 0;
        for (int i = 0; i < fs.size(); i++) {                    // Future.get : propage toute exception d'une tâche
            Compteurs c = fs.get(i).get(); int t = aFaire.get(i);
            if (c == null) { sautees++; continue; }              // sautée après une touche (-DstopTouche=1) : res[t] reste vide
            if (res[t] != null) throw new IllegalStateException("double execution"); res[t] = c; faites++;
        }
        if (!ex.awaitTermination(1, TimeUnit.MINUTES)) throw new IllegalStateException("executor non termine");
        veille.shutdownNow();
        if (faites + sautees != aFaire.size() || TERMINEES.get() != faites || (sautees > 0 && !stopTouche)) throw new IllegalStateException("selection incompletement terminee");
        if (sautees > 0) System.out.println("ARRET_SUR_TOUCHE : " + sautees + " taches non executees (temoin positif trouve ; aucune conclusion negative)");
        if (ckptCanal != null) { ckptCanal.force(true); ckptCanal.close(); System.out.println("CHECKPOINT_SHA256 " + shaFichier(ckpt) + " ; " + ckpt); }

        // ---- bilan : couverture et totaux (y compris tâches reprises du checkpoint) [Z10]
        long su = 0, sc = 0, sA = 0, sB = 0, st = 0; long[] h = new long[64]; int couvertes = 0, selFaites = 0;
        for (int t = 0; t < nt; t++) {
            if (res[t] == null) continue;
            couvertes++; if (choisi[t]) selFaites++;
            Compteurs c = res[t];
            su = Math.addExact(su, c.u); sc = Math.addExact(sc, c.cvp); sA = Math.addExact(sA, c.noeudsA); sB = Math.addExact(sB, c.noeudsB); st = Math.addExact(st, c.touches);
            for (int i = 0; i < 64; i++) h[i] = Math.addExact(h[i], c.hist[i]);
        }
        if (selFaites != selection - sautees) throw new IllegalStateException("selection non couverte");
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 64; i++) if (h[i] != 0) { if (i == 63) sb.append(">=6.3:").append(h[i]).append(" "); else sb.append("[").append(i / 10.0).append(",").append((i + 1) / 10.0).append("):").append(h[i]).append(" "); }
        System.out.println("EXECUTEES_CE_LANCEMENT " + faites + " ; REPRISES_DU_CHECKPOINT " + repris);
        System.out.println("TACHES_TERMINEES " + couvertes + "/" + nt);
        System.out.println("COMPTE_U (au signe pres, energie courte <= " + BAnum + "/" + BAden + ") " + su + " ; histogramme " + sb);
        System.out.println("NOEUDS court " + Math.addExact(sA, ng[0]) + " ; fibre " + sB + " ; CVP " + sc);
        if (!modeCompte) System.out.println("TOTAL_TOUCHES " + st);
        System.out.println(couvertes == nt ? "COUVERTURE_COMPLETE " + nt + "/" + nt + " ; CATALOGUE " + shaCat : "COUVERTURE_PARTIELLE " + couvertes + "/" + nt + " : AUCUNE CONCLUSION GLOBALE");
        System.out.println("FIN [" + (System.currentTimeMillis() - t0) / 1000 + " s]");
        return 0;
    }
}
