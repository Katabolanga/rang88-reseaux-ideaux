/* enum88.c -- M10, 7 nov. 2026 (Claude).  SECONDE IMPLANTATION, ecrite sans reprendre le code de Rang88CertZ, du critere
   du theoreme 4.6 de la note (rang 88, Q(zeta_115)) pour UN cote :
     pour tout u != 0 (au signe pres) de Z^n avec la = u~Au <= DA*BA (cote court), et tout y de Z^n,
     TOUCHE  <=>  la*DB*d^2 + DA*e <= S*DA*DB*d^2,  ou w = Tu + d*y et e = w~Bw.
   Algorithme : Fincke-Pohst par intervalles (pas de zigzag), Cholesky en double, sommes partielles des centres tenues
   paresseusement (rafraichissement des seuls niveaux modifies), marge relative 1e-9 sur les bornes ; decisions finales
   EXACTES en entiers (int64 pour u~Au, __int128 pour la fibre).  Parallelisme : taches = valeurs des NIV coordonnees du
   haut, distribuees par compteur atomique.  Ne certifie rien seul (flottants sans analyse d'erreur) : sert a recouper
   COMPTE_U, l'histogramme et l'absence de touche de Rang88CertZ (memes entrees, autre code, autre arithmetique).
   Compilation : gcc -O3 -march=native -pthread -o enum88 enum88.c -lm
   Usage : ./enum88 prefixe BAnum BAden S fils mode     (mode 0 : compte de U seulement ; mode 1 : critere complet)      */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
#include <stdatomic.h>
#include <time.h>
#include <stdint.h>

#define NMAX 48
typedef __int128 i128;
static int n; static long long A[NMAX][NMAX], B[NMAX][NMAX], T[NMAX][NMAX];
static long long DA, DB, d, BAn, BAd, S, QAmax; static int mode;
static double RA[NMAX], MA[NMAX][NMAX], RB[NMAX], MB[NMAX][NMAX];   /* R_ii^2 et m_ij = R_ij/R_ii (j > i) */
static const double MARGE = 1e-9;

static void lire(const char *f, long long M[NMAX][NMAX]) {
  FILE *F = fopen(f, "r"); if (!F) { fprintf(stderr, "ERREUR lecture %s\n", f); exit(2); }
  int r, c; if (fscanf(F, "%d %d", &r, &c) != 2 || r != c || r > NMAX) { fprintf(stderr, "ERREUR format %s\n", f); exit(2); }
  if (n && r != n) { fprintf(stderr, "ERREUR dimension %s\n", f); exit(2); }
  n = r;
  for (int i = 0; i < r; i++) for (int j = 0; j < c; j++) if (fscanf(F, "%lld", &M[i][j]) != 1) { fprintf(stderr, "ERREUR jeton %s\n", f); exit(2); }
  long long x; if (fscanf(F, "%lld", &x) == 1) { fprintf(stderr, "ERREUR jetons en trop %s\n", f); exit(2); }
  fclose(F);
}
static void cholesky(long long G[NMAX][NMAX], double r2[NMAX], double m[NMAX][NMAX]) {
  static double R[NMAX][NMAX];
  for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (G[i][j] != G[j][i]) { fprintf(stderr, "ERREUR Gram non symetrique\n"); exit(2); }
  memset(R, 0, sizeof R);
  for (int i = 0; i < n; i++) {
    double s = (double) G[i][i];
    for (int k = 0; k < i; k++) s -= R[k][i] * R[k][i];
    if (!(s > 0)) { fprintf(stderr, "ERREUR Gram non definie positive (pivot %d)\n", i); exit(2); }
    R[i][i] = sqrt(s);
    for (int j = i + 1; j < n; j++) { double t = (double) G[i][j]; for (int k = 0; k < i; k++) t -= R[k][i] * R[k][j]; R[i][j] = t / R[i][i]; }
  }
  for (int i = 0; i < n; i++) { r2[i] = R[i][i] * R[i][i]; for (int j = 0; j < n; j++) m[i][j] = (j > i) ? R[i][j] / R[i][i] : 0.0; }
}

typedef struct {
  long long u, cvp, touches, noeudsA, noeudsB, hist[64];
  long long uu[NMAX], yy[NMAX], t[NMAX]; double tau[NMAX];
  double csA[NMAX][NMAX + 1], csB[NMAX][NMAX + 1]; int hcA[NMAX], hcB[NMAX];
  int silence;
} Ctx;
static long long qexact(long long G[NMAX][NMAX], const long long *x) {
  long long s = 0; for (int i = 0; i < n; i++) if (x[i]) { long long r = 0; for (int j = 0; j < n; j++) r += G[i][j] * x[j]; s += x[i] * r; } return s;
}
static pthread_mutex_t verrou = PTHREAD_MUTEX_INITIALIZER;
static inline int imax(int a, int b) { return a > b ? a : b; }

/* ---------------- fibre ---------------- */
static void feuilleB(Ctx *c, long long la) {
  i128 e = 0; long long w[NMAX];
  for (int i = 0; i < n; i++) w[i] = c->t[i] + d * c->yy[i];
  for (int i = 0; i < n; i++) if (w[i]) { i128 r = 0; for (int j = 0; j < n; j++) r += (i128) B[i][j] * w[j]; e += (i128) w[i] * r; }
  i128 gauche = (i128) la * DB * d * d + (i128) DA * e, droite = (i128) S * DA * DB * d * d;
  if (gauche > droite) return;
  c->touches++;
  if (c->silence) return;
  pthread_mutex_lock(&verrou);
  printf("TOUCHE court=%lld/%lld fibre(num)=%lld/(%lld*%lld^2) u=[", la, DA, (long long) e, DB, d);
  for (int i = 0; i < n; i++) printf(i ? ",%lld" : "%lld", c->uu[i]);
  printf("] y=["); for (int i = 0; i < n; i++) printf(i ? ",%lld" : "%lld", c->yy[i]); printf("]\n"); fflush(stdout);
  pthread_mutex_unlock(&verrou);
}
/* invariant : la ligne i est a jour (csB[i][i+1] = sum_{l>i} m_il (y_l + tau_l)) a l'entree de recB(i) */
static void recB(Ctx *c, int i, double P, double Bnd, long long la) {
  double s = c->tau[i] + c->csB[i][i + 1];
  double rest = Bnd - P; if (rest < 0) return;
  double h = sqrt(rest / RB[i]) * (1 + MARGE) + 1e-12;
  long long lo = (long long) ceil(-s - h), hi = (long long) floor(-s + h);
  for (long long y = lo; y <= hi; y++) {
    c->noeudsB++;
    double z = (double) y + s, P2 = P + RB[i] * z * z;
    if (P2 > Bnd) continue;
    c->yy[i] = y;
    if (i == 0) { feuilleB(c, la); continue; }
    c->hcB[i - 1] = imax(c->hcB[i - 1], i);
    int top = c->hcB[i - 1];
    for (int j = top; j >= i; j--) c->csB[i - 1][j] = c->csB[i - 1][j + 1] + MB[i - 1][j] * ((double) c->yy[j] + c->tau[j]);
    if (i - 2 >= 0) c->hcB[i - 2] = imax(c->hcB[i - 2], top);
    c->hcB[i - 1] = i - 1;
    recB(c, i - 1, P2, Bnd, la);
  }
  c->yy[i] = 0;
  if (i > 0) c->hcB[i - 1] = imax(c->hcB[i - 1], i);
}
static void cvp(Ctx *c, double Bnd, long long la) {
  for (int i = 0; i < n; i++) { c->yy[i] = 0; c->csB[i][n] = 0.0; c->hcB[i] = n - 1; }
  /* ligne n-1 : csB[n-1][n] = 0, a jour */
  recB(c, n - 1, 0.0, Bnd, la);
}
/* ---------------- cote court ---------------- */
static void feuilleA(Ctx *c) {
  long long la = qexact(A, c->uu);
  if (la <= 0 || la > QAmax) return;
  c->u++; long long b = la * 10 / DA; c->hist[b > 63 ? 63 : b]++;
  if (mode == 0) return;
  for (int i = 0; i < n; i++) { long long s = 0; for (int j = 0; j < n; j++) s += T[i][j] * c->uu[j]; c->t[i] = s; c->tau[i] = (double) s / (double) d; }
  double R = (double) DB * ((double) S - (double) la / (double) DA);
  if (R < 0) return;
  c->cvp++;
  cvp(c, R * (1 + MARGE) + 1e-9, la);
}
static void recA(Ctx *c, int i, double P, double Bnd, int zero) {
  double s = c->csA[i][i + 1];
  double rest = Bnd - P; if (rest < 0) return;
  double h = sqrt(rest / RA[i]) * (1 + MARGE) + 1e-12;
  long long lo = (long long) ceil(-s - h), hi = (long long) floor(-s + h);
  if (zero && lo < 0) lo = 0;
  for (long long y = lo; y <= hi; y++) {
    c->noeudsA++;
    double z = (double) y + s, P2 = P + RA[i] * z * z;
    if (P2 > Bnd) continue;
    c->uu[i] = y;
    if (i == 0) { if (!(zero && y == 0)) feuilleA(c); continue; }
    c->hcA[i - 1] = imax(c->hcA[i - 1], i);
    int top = c->hcA[i - 1];
    for (int j = top; j >= i; j--) c->csA[i - 1][j] = c->csA[i - 1][j + 1] + MA[i - 1][j] * (double) c->uu[j];
    if (i - 2 >= 0) c->hcA[i - 2] = imax(c->hcA[i - 2], top);
    c->hcA[i - 1] = i - 1;
    recA(c, i - 1, P2, Bnd, zero && y == 0);
  }
  c->uu[i] = 0;
  if (i > 0) c->hcA[i - 1] = imax(c->hcA[i - 1], i);
}
/* ---------------- taches ---------------- */
#ifndef NIV
#define NIV 3
#endif
typedef struct { long long y[NIV]; double P; int zero; } Tache;
static Tache *taches; static long long ntaches, cap; static atomic_llong suivante; static double BndA;
static void gen(int i, int k, long long *pre, double P, int zero) {
  if (k == NIV) { if (ntaches == cap) { cap = cap ? 2 * cap : 1024; taches = realloc(taches, cap * sizeof(Tache)); }
    for (int a = 0; a < NIV; a++) { taches[ntaches].y[a] = pre[a]; }
    taches[ntaches].P = P; taches[ntaches].zero = zero; ntaches++; return; }
  long long uu[NMAX]; memset(uu, 0, sizeof uu); for (int a = 0; a < k; a++) uu[n - 1 - a] = pre[a];
  double s = 0; for (int j = i + 1; j < n; j++) s += MA[i][j] * (double) uu[j];
  double rest = BndA - P; if (rest < 0) return;
  double h = sqrt(rest / RA[i]) * (1 + MARGE) + 1e-12;
  long long lo = (long long) ceil(-s - h), hi = (long long) floor(-s + h);
  if (zero && lo < 0) lo = 0;
  for (long long y = lo; y <= hi; y++) { double z = (double) y + s, P2 = P + RA[i] * z * z; if (P2 > BndA) continue; pre[k] = y; gen(i - 1, k + 1, pre, P2, zero && y == 0); }
}
static Ctx tot;
static void *travail(void *arg) {
  (void) arg; Ctx *c = calloc(1, sizeof(Ctx));
  for (;;) {
    long long k = atomic_fetch_add(&suivante, 1); if (k >= ntaches) break;
    memset(c->uu, 0, sizeof c->uu);
    for (int a = 0; a < NIV; a++) c->uu[n - 1 - a] = taches[k].y[a];
    int i0 = n - 1 - NIV;
    /* ligne i0 a jour, les autres a rafraichir entierement */
    for (int r = 0; r < n; r++) { c->csA[r][n] = 0.0; c->hcA[r] = n - 1; }
    for (int j = n - 1; j > i0; j--) c->csA[i0][j] = c->csA[i0][j + 1] + MA[i0][j] * (double) c->uu[j];
    if (i0 - 1 >= 0) c->hcA[i0 - 1] = n - 1;
    c->hcA[i0] = i0;
    recA(c, i0, taches[k].P, BndA, taches[k].zero);
  }
  pthread_mutex_lock(&verrou);
  tot.u += c->u; tot.cvp += c->cvp; tot.touches += c->touches; tot.noeudsA += c->noeudsA; tot.noeudsB += c->noeudsB;
  for (int b = 0; b < 64; b++) tot.hist[b] += c->hist[b];
  pthread_mutex_unlock(&verrou);
  free(c); return NULL;
}
int main(int argc, char **argv) {
  if (argc != 7) { fprintf(stderr, "usage : enum88 prefixe BAnum BAden S fils mode\n"); return 3; }
  char f[1024]; const char *pre = argv[1];
  snprintf(f, sizeof f, "%s_A.gram", pre); lire(f, A); snprintf(f, sizeof f, "%s_B.gram", pre); lire(f, B); snprintf(f, sizeof f, "%s_T.mat", pre); lire(f, T);
  snprintf(f, sizeof f, "%s_meta.txt", pre); FILE *F = fopen(f, "r"); if (!F || fscanf(F, "%lld %lld %lld", &DA, &DB, &d) != 3) { fprintf(stderr, "ERREUR meta\n"); return 2; } fclose(F);
  BAn = atoll(argv[2]); BAd = atoll(argv[3]); S = atoll(argv[4]); int fils = atoi(argv[5]); mode = atoi(argv[6]);
  if (n <= NIV + 1) { fprintf(stderr, "ERREUR n trop petit\n"); return 2; }
  QAmax = (DA * BAn) / BAd;   /* la entier : la*BAd <= DA*BAn  <=>  la <= floor(DA*BAn/BAd) */
  cholesky(A, RA, MA); cholesky(B, RB, MB);
  BndA = (double) QAmax * (1 + MARGE) + 1e-9;
  printf("enum88 : %s ; n = %d ; DA = %lld DB = %lld d = %lld ; BA = %lld/%lld (u~Au <= %lld) ; S = %lld ; %d fils ; mode %d\n", pre, n, DA, DB, d, BAn, BAd, QAmax, S, fils, mode);
  if (mode == 1) {   /* u = 0 : y (signes compris, y = 0 compris) avec Q_B(y) <= S*DB */
    Ctx *c0 = calloc(1, sizeof(Ctx)); c0->silence = 1;
    cvp(c0, (double) S * DB * (1 + MARGE) + 1e-9, 0);
    printf("U0 : %lld vecteurs y (y = 0 et signes compris) avec Q_B(y) <= S*DB ; attendu 1 (y = 0 seul)\n", c0->touches);
    free(c0);
  }
  long long p0[NIV]; gen(n - 1, 0, p0, 0.0, 1);
  printf("TACHES %lld (prefixes de %d coordonnees)\n", ntaches, NIV); fflush(stdout);
  struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
  pthread_t th[256]; if (fils < 1) fils = 1; if (fils > 256) fils = 256;
  for (int k = 0; k < fils; k++) pthread_create(&th[k], NULL, travail, NULL);
  for (int k = 0; k < fils; k++) pthread_join(th[k], NULL);
  clock_gettime(CLOCK_MONOTONIC, &t1);
  printf("COMPTE_U %lld\nHIST", tot.u); for (int b = 0; b < 64; b++) if (tot.hist[b]) printf(" [%d.%d,%d.%d):%lld", b / 10, b % 10, (b + 1) / 10, (b + 1) % 10, tot.hist[b]);
  printf("\nCVP %lld ; NOEUDS court %lld ; fibre %lld\nTOTAL_TOUCHES %lld\nFIN [%.0f s]\n", tot.cvp, tot.noeudsA, tot.noeudsB, tot.touches,
         (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec));
  return 0;
}
