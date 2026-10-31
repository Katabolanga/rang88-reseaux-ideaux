# -*- coding: utf-8 -*-
"""verifier_integrite_P1151s24.py -- controle d'integrite, en LECTURE SEULE, de l'execution certifiante de P1151*sigma24(P1151)
sur SpiraleG (17-19 oct. 2026), avant raccord et non-isometrie.  Claude, 19 oct. 2026.  Aucun fichier n'est ecrit.

Usage : python3 -I verifier_integrite_P1151s24.py <dossier r88p> <dossier p1151s24_preparation>

I1  empreintes : SHA-256 recalcules des 8 classes et des 11 entrees dans r88p (originaux) = copies de la preparation
    = empreintes_entrees.txt (ecrit par le lanceur avant le calcul) = attendu.sha (classes) = entrees_source.sha (entrees) ;
    les 4 empreintes d'entree et les 7 empreintes de classe imprimees par CHAQUE journal Java = fichiers ;
I2  journaux (par cote) : un seul en-tete de lancement, parametres = invocation publiee et meta (1151 1 2302), 14 fils,
    CHECKPOINT nouveau, SELECTION n/n, DEJA_AU_CHECKPOINT 0, EXECUTEES_CE_LANCEMENT n, REPRISES 0, TACHES_TERMINEES n/n,
    TOTAL_TOUCHES 0, COUVERTURE_COMPLETE n/n avec le catalogue, FIN ; aucune ligne TOUCHE / ERREUR / ARRET / REPRISE /
    Exception ; code de sortie Java 0 ; stderr vide ; chaine.log et VERDICT.txt coherents ;
I3  catalogues : SHA du fichier .taches = CATALOGUE_SHA256 du journal = catalogue de l'autotest du 17 oct. (genere avant le
    calcul) ; en-tete R88Z_TACHES_V1 aux memes parametres, total = n ; n lignes de tache d'indices 0..n-1 dans l'ordre ;
    « n taches certifiees » dans le journal de calcul et dans le journal de catalogue de l'autotest ;
I4  recus : en-tete du .ckpt (catalogue, total, empreinte LIEN des entrees et des classes = celles du journal), n recus,
    SHA du .ckpt = CHECKPOINT_SHA256 du journal ; aucun fichier *.touches dans le dossier d'execution ;
I5  autotest prealable : TestCertZ « TOTAL : 910 controles, 0 echecs » et TEST_OK ; validation P461 (697 u, 2 touches,
    couverture 3658/3658)."""
import sys, os, re, glob, hashlib

if len(sys.argv) != 3:
    raise SystemExit(__doc__)
R88P, PREP = sys.argv[1], sys.argv[2]
RUN = os.path.join(R88P, "run_P1151s24")
NT = {1: 74027, 2: 101373}
CAT = {1: "287b1e724cb845e266356bbaed182a6c95d47f207dc7def9acf10c5d78711b8e", 2: "fe2b7eb6d4d0218117b840ca1d7dc5353bf1e5b6c276ed7bbaede563c25ae4b4"}
PARAMS = "n=44|BA=1057/200|S=12|DA=1151|DB=1|d=2302|F=40|D=6|Dmax=16|seuil=0.2"
NB = [0, 0]
def controle(nom, cond):
    NB[0] += 1
    if not cond: NB[1] += 1
    print(("OK    " if cond else "ECHEC ") + nom); sys.stdout.flush()
def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def lire_sums(f):
    d = {}
    for l in open(f, encoding="ascii"):
        l = l.strip()
        if not l: continue
        h, _, nom = l.partition(" ")
        d[nom.strip().lstrip("*")] = h
    return d
src = os.path.abspath(__file__)
print("source : %s SHA-256 %s" % (os.path.basename(src), sha(src)))

# ---------------------------------------------------------------- I1 empreintes
classes = sorted(os.path.basename(f) for f in glob.glob(os.path.join(R88P, "classes", "*.class")))
entrees = sorted(os.listdir(os.path.join(R88P, "java_P1151s24")))
controle("I1 8 classes et 11 fichiers d'entree dans r88p (%d, %d)" % (len(classes), len(entrees)), len(classes) == 8 and len(entrees) == 11)
H = {}
for c in classes: H["classes/" + c] = sha(os.path.join(R88P, "classes", c))
for e in entrees: H["java_P1151s24/" + e] = sha(os.path.join(R88P, "java_P1151s24", e))
for k in sorted(H): print("      %s  %s" % (H[k], k))
COP = {"java_P1151s24/" + e: sha(os.path.join(PREP, "data", "P1151s24", "entrees", e)) for e in entrees}
controle("I1 copies de la preparation (data/P1151s24/entrees) identiques aux originaux de r88p (11 fichiers)", all(COP[k] == H[k] for k in COP))
EMP = lire_sums(os.path.join(RUN, "empreintes_entrees.txt"))
controle("I1 empreintes_entrees.txt (ecrit par le lanceur le 17 oct. 22 h 48, avant le calcul) : %d lignes, toutes egales aux fichiers actuels" % len(EMP),
         len(EMP) == 19 and set(EMP) == set(H) and all(EMP[k] == H[k] for k in H))
ATT = lire_sums(os.path.join(R88P, "attendu.sha"))
attc = {k: v for k, v in ATT.items() if k.startswith("classes/")}
controle("I1 attendu.sha : les 8 classes = classes publiees attendues (%d lignes de classe)" % len(attc), len(attc) == 8 and all(H.get(k) == v for k, v in attc.items()))
attp = {k: v for k, v in ATT.items() if k.startswith("java_P461/")}
controle("I1 attendu.sha : les 4 entrees de validation java_P461 (autotest) sont intactes", len(attp) == 4 and all(sha(os.path.join(R88P, k)) == v for k, v in attp.items()))
SRC = lire_sums(os.path.join(R88P, "entrees_source.sha"))
controle("I1 entrees_source.sha (11 lignes, empreintes des entrees a leur source) = fichiers actuels", len(SRC) == 11 and all(H.get("java_P1151s24/" + k) == v for k, v in SRC.items()))

# ---------------------------------------------------------------- I2 journaux
J = {}
for s in (1, 2):
    f = os.path.join(RUN, "cote%d.stdout.log" % s)
    J[s] = open(f, "rb").read().decode("ascii", "replace").replace("\r\n", "\n")
    t = J[s]; n = NT[s]
    def un(rx): m = re.findall(rx, t, re.M); return m[0] if len(m) == 1 else None
    controle("I2 cote %d : copie du journal dans la preparation identique a l'original" % s, sha(f) == sha(os.path.join(PREP, "data", "P1151s24", "premiere_execution", "cote%d.stdout.log" % s)))
    controle("I2 cote %d : un seul en-tete, mode=run|%s, 14 fils, java_P1151s24/cote%d" % (s, PARAMS, s),
             len(re.findall(r"^Rang88CertZ ", t, re.M)) == 1 and un(r"^Rang88CertZ run : java_P1151s24/cote%d ; mode=run\|%s ; 14 fils ; verif=false$" % (s, re.escape(PARAMS))) is not None)
    m = re.search(r"ENTREES SHA-256 : A (\w+) ; B (\w+) ; T (\w+) ; meta (\w+)", t)
    controle("I2 cote %d : empreintes d'entree imprimees par Java (A, B, T, meta) = fichiers" % s,
             m is not None and list(m.groups()) == [H["java_P1151s24/cote%d_%s" % (s, x)] for x in ("A.gram", "B.gram", "T.mat", "meta.txt")])
    mc = dict(re.findall(r"(Rang88CertZ(?:\$\w+)?)=([0-9a-f]{64})", t.split("CLASSES SHA-256 :")[1].split("\n")[0]))
    controle("I2 cote %d : empreintes des 7 classes imprimees par Java = fichiers" % s, len(mc) == 7 and all(H["classes/%s.class" % k] == v for k, v in mc.items()))
    controle("I2 cote %d : JVM imprimee (OpenJDK 11.0.16.1, Windows 11)" % s, un(r"^  JVM OpenJDK 64-Bit Server VM 11\.0\.16\.1 ; Windows 11 amd64 ;") is not None)
    controle("I2 cote %d : %d taches certifiees annoncees ; CATALOGUE_SHA256 %s... ; TOTAL_TACHES %d" % (s, n, CAT[s][:8], n),
             un(r"^  %d taches certifiees \(" % n) is not None and un(r"^CATALOGUE_SHA256 %s ; TOTAL_TACHES %d$" % (CAT[s], n)) is not None)
    controle("I2 cote %d : CHECKPOINT nouveau ; SELECTION %d/%d ; A_FAIRE %d ; DEJA_AU_CHECKPOINT 0" % (s, n, n, n),
             un(r"^CHECKPOINT nouveau : ") is not None and un(r"^SELECTION %d/%d ; A_FAIRE %d ; DEJA_AU_CHECKPOINT 0$" % (n, n, n)) is not None)
    controle("I2 cote %d : EXECUTEES_CE_LANCEMENT %d ; REPRISES_DU_CHECKPOINT 0 ; TACHES_TERMINEES %d/%d" % (s, n, n, n),
             un(r"^EXECUTEES_CE_LANCEMENT %d ; REPRISES_DU_CHECKPOINT 0$" % n) is not None and un(r"^TACHES_TERMINEES %d/%d$" % (n, n)) is not None)
    controle("I2 cote %d : TOTAL_TOUCHES 0 ; COUVERTURE_COMPLETE %d/%d ; CATALOGUE %s... ; ligne FIN" % (s, n, n, CAT[s][:8]),
             un(r"^TOTAL_TOUCHES 0$") is not None and un(r"^COUVERTURE_COMPLETE %d/%d ; CATALOGUE %s$" % (n, n, CAT[s])) is not None and un(r"^FIN \[\d+ s\]$") is not None)
    veille = re.findall(r"touches (\d+) \[\d+ s\]$", t, re.M)
    controle("I2 cote %d : aucune ligne TOUCHE / ERREUR / ARRET / REPRISE / Exception ; %d lignes de veille, toutes « touches 0 »" % (s, len(veille)),
             not re.search(r"^(TOUCHE|ERREUR|ARRET|REPRISE)|Exception|Error", t, re.M) and veille and all(v == "0" for v in veille))
    ex = open(os.path.join(RUN, "cote%d.java.exit" % s)).read().strip()
    controle("I2 cote %d : code de sortie Java = %s ; stderr de %d octets" % (s, ex, os.path.getsize(os.path.join(RUN, "cote%d.stderr.log" % s))),
             ex == "0" and os.path.getsize(os.path.join(RUN, "cote%d.stderr.log" % s)) == 0)
    fin = re.search(r"^FIN \[(\d+) s\]$", t, re.M); print("      duree imprimee cote %d : %s s" % (s, fin.group(1) if fin else "?"))
cu = [re.search(r"^COMPTE_U \(au signe pres, energie courte <= 1057/200\) (\d+) ;", J[s], re.M) for s in (1, 2)]
print("      COMPTE_U : cote 1 %s ; cote 2 %s (constat : egaux, comme pour P4969 et P4049)" % (cu[0].group(1) if cu[0] else "?", cu[1].group(1) if cu[1] else "?"))
ch = open(os.path.join(RUN, "chaine.log"), encoding="ascii").read()
controle("I2 chaine.log : DEBUT/FIN des deux cotes, codes java 0, COUVERTURE_COMPLETE 74027/74027 et 101373/101373, TOTAL_TOUCHES 0, aucun REJETE",
         ch.count("DEBUT cote") == 2 and "FIN cote 1, code java 0" in ch and "FIN cote 2, code java 0" in ch
         and "cote 1 : COUVERTURE_COMPLETE 74027/74027, TOTAL_TOUCHES 0" in ch and "cote 2 : COUVERTURE_COMPLETE 101373/101373, TOTAL_TOUCHES 0" in ch and "REJETE" not in ch)
controle("I2 VERDICT.txt = « DEUX_COTES_COMPLETS_SANS_TOUCHE (a confirmer par raccord et contre-audit) »",
         open(os.path.join(RUN, "VERDICT.txt"), encoding="ascii").read().strip() == "DEUX_COTES_COMPLETS_SANS_TOUCHE (a confirmer par raccord et contre-audit)")

# ---------------------------------------------------------------- I3 catalogues
ATD = os.path.join(R88P, open(os.path.join(R88P, "DERNIER_AUTOTEST.txt")).read().strip())
for s in (1, 2):
    n = NT[s]; f = os.path.join(RUN, "cote%d.taches" % s); h = sha(f)
    controle("I3 cote %d : SHA du catalogue .taches = CATALOGUE_SHA256 du journal (%s...)" % (s, CAT[s][:8]), h == CAT[s])
    controle("I3 cote %d : catalogue identique a celui de l'autotest du 17 oct. (genere avant le calcul)" % s, h == sha(os.path.join(ATD, "P1151s24_cote%d.taches" % s)))
    L = open(f, encoding="ascii").read().split("\n")
    if L and L[-1] == "": L = L[:-1]
    controle("I3 cote %d : en-tete R88Z_TACHES_V1|%s|total=%d" % (s, PARAMS, n), L[0] == "R88Z_TACHES_V1|%s|total=%d" % (PARAMS, n))
    idx = [int(x.split("|", 1)[0]) for x in L[1:]]
    controle("I3 cote %d : %d lignes de tache, indices 0..%d dans l'ordre" % (s, len(idx), n - 1), idx == list(range(n)))
    cl = open(os.path.join(ATD, "catalogue%d.log" % s), encoding="ascii", errors="replace").read()
    controle("I3 cote %d : le journal de catalogue de l'autotest annonce aussi %d taches certifiees" % (s, n), ("  %d taches certifiees (" % n) in cl)

# ---------------------------------------------------------------- I4 recus
for s in (1, 2):
    n = NT[s]; t = J[s]
    brut = open(os.path.join(RUN, "cote%d.ckpt" % s), "rb").read()
    L = brut.decode("ascii").split("\n")
    lien = re.search(r"LIEN entrees=([0-9a-f]{64})\|classes=([0-9a-f]{64})", t)
    controle("I4 cote %d : en-tete des recus R88Z_CKPT_V1|mode=run|%s|total=%d|catalogue=%s...|entrees, classes = LIEN du journal" % (s, PARAMS, n, CAT[s][:8]),
             lien is not None and L[0] == "R88Z_CKPT_V1|mode=run|%s|total=%d|catalogue=%s|entrees=%s|classes=%s" % (PARAMS, n, CAT[s], lien.group(1), lien.group(2)))
    corps = [x for x in L[1:] if x]
    controle("I4 cote %d : %d recus T|...|FIN, fichier termine par LF" % (s, len(corps)), len(corps) == n and all(x.startswith("T|") and x.endswith("|FIN") for x in corps) and brut.endswith(b"\n"))
    jck = re.search(r"^CHECKPOINT_SHA256 ([0-9a-f]{64}) ; ", t, re.M)
    controle("I4 cote %d : SHA du fichier de recus = CHECKPOINT_SHA256 du journal" % s, jck is not None and jck.group(1) == hashlib.sha256(brut).hexdigest())
controle("I4 aucun fichier *.touches dans run_P1151s24 (inventaire : %s)" % ", ".join(sorted(os.listdir(RUN))), not glob.glob(os.path.join(RUN, "*.touches")))

# ---------------------------------------------------------------- I5 autotest
tc = open(os.path.join(ATD, "testcertz.log"), encoding="ascii", errors="replace").read()
controle("I5 autotest %s : TestCertZ « TOTAL : 910 controles, 0 echecs » et TEST_OK" % os.path.basename(ATD), "TOTAL : 910 controles, 0 echecs" in tc and re.search(r"^TEST_OK", tc, re.M) is not None)
pv = open(os.path.join(ATD, "p461.log"), encoding="ascii", errors="replace").read()
controle("I5 autotest : validation P461 (COMPTE_U 697, TOTAL_TOUCHES 2, COUVERTURE_COMPLETE 3658/3658)",
         re.search(r"^COMPTE_U .*\) 697 ;", pv, re.M) is not None and re.search(r"^TOTAL_TOUCHES 2$", pv, re.M) is not None and re.search(r"^COUVERTURE_COMPLETE 3658/3658", pv, re.M) is not None)
print("BILAN : %d controles, %d echecs" % (NB[0], NB[1]))
print("INTEGRITE_OK" if NB[1] == 0 else "INTEGRITE_ECHEC")
sys.exit(0 if NB[1] == 0 else 1)
