# -*- coding: utf-8 -*-
"""verifier_recus.py -- controle exact, en lecture seule, des executions du programme certifiant Rang88CertZ pour un candidat
(P139 ou P599) : recus (checkpoints), journaux, catalogues, empreintes canoniques.  Ne lance aucun Java, n'ecrit rien.

Ce que le script controle (note, prop. 6.3 (3), prop. 6.4 (3), cor. 5.2, th. 6.11 (B)) :
  R1  source et classes : SHA-256 de code/certifiant/Rang88CertZ.java = 9e467c75...c3c5 ; les 7 classes du programme
      ont les empreintes imprimees par CHAQUE journal (ligne CLASSES SHA-256) ; la ligne LIEN est recalculee ;
  R2  entrees : les 4 fichiers d'entree de chaque cote ont les empreintes imprimees par chaque journal (ligne ENTREES SHA-256) ;
  R3  journaux des executions de reference (second ordinateur, data/<C>/replication/) : un seul lancement par cote,
      CHECKPOINT nouveau, SELECTION nt/nt ; A_FAIRE nt ; DEJA_AU_CHECKPOINT 0, EXECUTEES_CE_LANCEMENT nt ;
      REPRISES_DU_CHECKPOINT 0, TACHES_TERMINEES nt/nt, TOTAL_TOUCHES 0, COUVERTURE_COMPLETE nt/nt, FIN ; aucune ligne
      ERREUR, TOUCHE, ARRET, REPRISE ; code de sortie (cote*.java.exit) = 0 ; stderr sans exception ;
  R4  recus : en-tete = parametres | total | catalogue | LIEN ; nt lignes au format strict ; indices = permutation de
      0..nt-1 ; TOUCHES = 0 dans chaque recu ; sommes des recus = totaux du journal ; SHA du fichier = CHECKPOINT_SHA256 ;
  R5  catalogue (data/<C>/cote*.taches) : SHA = CATALOGUE_SHA256 de toutes les executions = champ catalogue des recus ;
      format, indices, repartition par niveau, prefixes deux a deux incomparables, normalisation de signe ;
  R6  empreintes canoniques (recus tries par indice, sans en-tete, chacun suivi de LF, puis SHA-256), calculees de deux
      facons distinctes, pour l'execution de reference ET la premiere execution : egales aux valeurs publiees ;
  R7  inventaire du repertoire de sortie de l'execution de reference : aucun fichier de touche ;
  R8  premiere execution (premier ordinateur, data/<C>/premiere_execution/) : memes bilans ; pour P599 cote 1, controle
      exact de la reprise (prefixe, indices disjoints, union complete) et du rejeu des 21 459 taches reprises ;
  R9  coherence : meme COMPTE_U et meme histogramme pour les deux cotes et les deux executions ; bornes des compteurs (Z9).
Usage (depuis la racine du depot) : python -I code/verification/verifier_recus.py P139      (ou P599 ; quelques secondes)"""
import re, sys, os, hashlib
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if len(sys.argv) != 2 or sys.argv[1] not in ("P139", "P599"): raise SystemExit("usage : verifier_recus.py P139|P599")
CAND = sys.argv[1]
DC = os.path.join(RACINE, "data", CAND); CERT = os.path.join(RACINE, "code", "certifiant")
SRC_SHA = "9e467c750470301ec0612c087b84636da6b46538a0fe33458970af6cb97bc3c5"
CANON = {"P139": {1: "c99dcf87db02e6b51f448cdb3e51da1f8b0ee4bd782b6b0e78d686bed5575122", 2: "8ab1f40a48c416dd4eab8dde92d0c5866a6ca1951b5edd5d579c5f2ee0bedaf7"},
         "P599": {1: "f3cf379ad157b1595f9ad96c38d3734a920ea24de3afc5d12dfa617bb3e42689", 2: "b9c93a83d2b370fad5de5b3d0edc317718ebe4900960642ef98f72c219458ef6"}}[CAND]
NB = [0, 0]
def controle(nom, cond):
    NB[0] += 1
    if not cond: NB[1] += 1
    print(("OK    " if cond else "ECHEC ") + nom); sys.stdout.flush()
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()
def lire(f): return open(f, "rb").read().decode("ascii")
def rel(f): return os.path.relpath(f, RACINE).replace(os.sep, "/")

# ---------------------------------------------------------------- R1 : source et classes
print("== R1 source et classes")
h = sha(os.path.join(CERT, "Rang88CertZ.java")); print("   %s  code/certifiant/Rang88CertZ.java" % h)
controle("R1 SHA-256 de Rang88CertZ.java = 9e467c75...c3c5 (empreinte citee par la note)", h == SRC_SHA)
CLS = {}
for nm in sorted(os.listdir(os.path.join(CERT, "classes"))):
    if nm.endswith(".class"): CLS[nm[:-6]] = sha(os.path.join(CERT, "classes", nm)); print("   %s  code/certifiant/classes/%s" % (CLS[nm[:-6]], nm))

# ---------------------------------------------------------------- analyse d'un journal
def analyse_journal(f, cote):
    T = lire(f).replace("\r\n", "\n"); L = T.split("\n")    # journaux du premier ordinateur : fins de ligne CRLF
    J = {"texte": T, "lignes": L}
    J["params"] = re.search(r"^Rang88CertZ run : \S+ ; (mode=.*?) ; (\d+) fils", T, re.M).group(1)
    J["fils"] = int(re.search(r"^Rang88CertZ run : \S+ ; mode=.*? ; (\d+) fils", T, re.M).group(1))
    J["prefixe"] = re.search(r"^Rang88CertZ run : (\S+) ;", T, re.M).group(1)
    J["jvm"] = re.search(r"^  JVM (.*)$", T, re.M).group(1)
    J["nt"] = int(re.search(r"TOTAL_TACHES (\d+)", T).group(1))
    J["shacat"] = re.search(r"CATALOGUE_SHA256 ([0-9a-f]{64})", T).group(1)
    m = re.search(r"CHECKPOINT_SHA256 ([0-9a-f]{64})", T); J["shack"] = m.group(1) if m else None
    J["entrees"] = list(re.search(r"ENTREES SHA-256 : A (\w+) ; B (\w+) ; T (\w+) ; meta (\w+)", T).groups())
    lcl = next(x for x in L if x.startswith("  CLASSES SHA-256 :")); J["lcl"] = lcl
    J["classes"] = dict(kv.split("=") for kv in lcl.split(":", 1)[1].split())
    J["lien"] = re.search(r"^  LIEN (\S+)$", T, re.M).group(1)
    m = re.search(r"^COMPTE_U .*?\) (\d+) ;", T, re.M); J["U"] = int(m.group(1)) if m else None
    J["hist"] = {int(round(float(a) * 10)): int(b) for a, b in re.findall(r"\[(\d+\.\d),\d+\.\d\):(\d+)", T)}
    m = re.search(r"^NOEUDS court (\d+) ; fibre (\d+) ; CVP (\d+)", T, re.M); J["noeuds"] = [int(x) for x in m.groups()] if m else None
    J["ngen"] = int(re.search(r"\((\d+) noeuds de generation\)", T).group(1))
    J["parniv"] = {int(a): int(b) for a, b in re.findall(r"niv(\d+):(\d+)", T)}
    m = re.search(r"^FIN \[(\d+) s\]", T, re.M); J["duree"] = int(m.group(1)) if m else None
    return J

def controle_journal_commun(J, nom, cote):
    ent = [sha(os.path.join(DC, "entrees", "cote%d_%s" % (cote, s))) for s in ("A.gram", "B.gram", "T.mat", "meta.txt")]
    controle("R2 %s : empreintes d'entrees imprimees = fichiers data/%s/entrees/cote%d_*" % (nom, CAND, cote), J["entrees"] == ent)
    controle("R1 %s : empreintes des 7 classes chargees = fichiers code/certifiant/classes/" % nom,
             len(J["classes"]) == 7 and all(CLS.get(k) == v for k, v in J["classes"].items()))
    lien = "entrees=" + hashlib.sha256("".join(J["entrees"]).encode("ascii")).hexdigest() + "|classes=" + hashlib.sha256(J["lcl"].encode("ascii")).hexdigest()
    controle("R1 %s : LIEN recalcule = LIEN imprime (%s...)" % (nom, lien[:30]), lien == J["lien"])
    controle("R3 %s : parametres mode=run, BA=1057/200, S=12, F=40, D=6, Dmax=16, seuil=0.2 ; prefixe java_%s/cote%d" % (nom, CAND, cote),
             re.fullmatch(r"mode=run\|n=44\|BA=1057/200\|S=12\|DA=\d+\|DB=1\|d=\d+\|F=40\|D=6\|Dmax=16\|seuil=0\.2", J["params"]) is not None
             and J["prefixe"] == "java_%s/cote%d" % (CAND, cote))

def controle_lancement_neuf(J, nom):
    T, L, nt = J["texte"], J["lignes"], J["nt"]
    controle("R3 %s : un seul en-tete, une seule JVM ; CHECKPOINT nouveau ; aucune ligne REPRISE ; SELECTION %d/%d ; A_FAIRE %d ; DEJA_AU_CHECKPOINT 0" % (nom, nt, nt, nt),
             len(re.findall(r"^Rang88CertZ run", T, re.M)) == 1 and len(re.findall(r"; PID \d+ ;", T)) == 1
             and re.search(r"^CHECKPOINT nouveau : \S+cote\d\.ckpt$", T, re.M) is not None and "REPRISE :" not in T
             and ("SELECTION %d/%d ; A_FAIRE %d ; DEJA_AU_CHECKPOINT 0" % (nt, nt, nt)) in L)
    controle("R3 %s : EXECUTEES_CE_LANCEMENT %d ; REPRISES_DU_CHECKPOINT 0 ; TACHES_TERMINEES %d/%d" % (nom, nt, nt, nt),
             ("EXECUTEES_CE_LANCEMENT %d ; REPRISES_DU_CHECKPOINT 0" % nt) in L and ("TACHES_TERMINEES %d/%d" % (nt, nt)) in L)
    controle_fin(J, nom)

def controle_fin(J, nom):
    T, L, nt = J["texte"], J["lignes"], J["nt"]
    nl = [x for x in L if x]
    fin_ok = nl[-1].startswith("FIN [") or (nl[-1] == "EXIT=0" and nl[-2].startswith("FIN ["))
    controle("R3 %s : TOTAL_TOUCHES 0 ; une ligne COUVERTURE_COMPLETE %d/%d ; CATALOGUE %s... ; FIN [%s s] ; aucune ligne ERREUR, TOUCHE, ARRET" % (nom, nt, nt, J["shacat"][:12], J["duree"]),
             "TOTAL_TOUCHES 0" in L and L.count("COUVERTURE_COMPLETE %d/%d ; CATALOGUE %s" % (nt, nt, J["shacat"])) == 1 and fin_ok
             and not re.search(r"^(ERREUR|TOUCHE|ARRET)", T, re.M) and "COUVERTURE_PARTIELLE" not in T)

# ---------------------------------------------------------------- analyse d'un fichier de recus
RX = re.compile(r"^T\|(0|[1-9]\d*)\|U=(\d+)\|CVP=(\d+)\|NA=(\d+)\|NB=(\d+)\|TOUCHES=(\d+)\|HIST=((?:\d+:\d+(?:,\d+:\d+)*)?)\|FIN$")
def lire_recus(f):
    brut = open(f, "rb").read()
    ok_brut = all(b < 128 for b in brut) and b"\r" not in brut and brut.endswith(b"\n")
    lk = brut.decode("ascii").split("\n")[:-1]
    return brut, ok_brut, lk[0], lk[1:]
def canon1(corps):
    return hashlib.sha256("".join(l + "\n" for l in sorted(corps, key=lambda l: int(l.split("|")[1]))).encode("ascii")).hexdigest()
def canon2(corps, nt):
    tab = [None] * nt
    for l in corps:
        i = int(l[2:l.index("|", 2)]); assert tab[i] is None; tab[i] = l
    hh = hashlib.sha256()
    for l in tab: hh.update(l.encode("ascii")); hh.update(b"\n")
    return hh.hexdigest()

def controle_recus(f, J, nom, cote, sommes=True):
    brut, ok_brut, entete, corps = lire_recus(f)
    nt = J["nt"]
    if J["shack"]: controle("R4 %s : SHA du fichier de recus = CHECKPOINT_SHA256 imprime en fin d'execution (%s...)" % (nom, J["shack"][:12]), hashlib.sha256(brut).hexdigest() == J["shack"])
    controle("R4 %s : recus en ASCII pur, sans CR, termines par LF" % nom, ok_brut)
    controle("R4 %s : en-tete = R88Z_CKPT_V1|parametres|total=%d|catalogue=%s...|LIEN du journal" % (nom, nt, J["shacat"][:12]),
             entete == "R88Z_CKPT_V1|" + J["params"] + "|total=%d|catalogue=%s|" % (nt, J["shacat"]) + J["lien"])
    rec = [RX.match(x) for x in corps]
    controle("R4 %s : %d lignes de recu, toutes au format strict" % (nom, len(rec)), len(rec) == nt and all(rec))
    idx = [int(r.group(1)) for r in rec]
    controle("R4 %s : indices des recus = permutation de 0..%d (ni doublon ni lacune)" % (nom, nt - 1), sorted(idx) == list(range(nt)))
    U = [int(r.group(2)) for r in rec]; CVP = [int(r.group(3)) for r in rec]; NA = [int(r.group(4)) for r in rec]; NBf = [int(r.group(5)) for r in rec]; TO = [int(r.group(6)) for r in rec]
    hist = {}; okh = True
    for r, u in zip(rec, U):
        s = 0
        if r.group(7):
            for kv in r.group(7).split(","):
                a, b = kv.split(":"); hist[int(a)] = hist.get(int(a), 0) + int(b); s += int(b)
        okh &= (s == u)
    controle("R4 %s : chaque recu a TOUCHES = 0, CVP = U, somme de l'histogramme = U, NA >= 1" % nom, all(x == 0 for x in TO) and CVP == U and okh and min(NA) >= 1)
    if sommes:
        nc, nf, ncvp = J["noeuds"]
        controle("R4 %s : sommes des recus = totaux du journal : U %d ; CVP %d ; noeuds courts %d (= recus + %d de generation) ; fibre %d ; histogramme"
                 % (nom, J["U"], ncvp, nc, J["ngen"], nf),
                 sum(U) == J["U"] and sum(CVP) == ncvp and sum(NA) + J["ngen"] == nc and sum(NBf) == nf and hist == J["hist"])
    c1, c2 = canon1(corps), canon2(corps, nt)
    controle("R6 %s : empreinte canonique des recus (deux calculs distincts) = valeur publiee %s...%s" % (nom, CANON[cote][:8], CANON[cote][-4:]), c1 == c2 == CANON[cote])
    print("      empreinte canonique cote %d : %s ; %d recus ; SHA brut %s" % (cote, c1, len(corps), hashlib.sha256(brut).hexdigest()))
    return dict(U=U, NA=NA, NB=NBf, hist=hist, corps=corps, entete=entete)

def controle_catalogue(cote, J, nom):
    fcat = os.path.join(DC, "cote%d.taches" % cote); bc = open(fcat, "rb").read()
    controle("R5 %s : SHA du catalogue data/%s/cote%d.taches = CATALOGUE_SHA256 imprime (%s...)" % (nom, CAND, cote, J["shacat"][:12]), hashlib.sha256(bc).hexdigest() == J["shacat"])
    return bc

def controle_structure_catalogue(bc, J, cote):
    nt, params = J["nt"], J["params"]
    lc = bc.decode("ascii").split("\n")[:-1]
    rc = re.compile(r"^(\d+)\|niv=(\d+)\|prefix=([-\d=,]*)\|PL=(\S+)\|zero=(true|false)$")
    tc = [rc.match(x) for x in lc[1:]]
    controle("R5 cote %d : en-tete du catalogue coherent ; %d lignes au format ; indices 0..%d dans l'ordre" % (cote, len(tc), nt - 1),
             lc[0] == "R88Z_TACHES_V1|" + params[params.index("|n=") + 1:] + "|total=%d" % nt and len(tc) == nt and all(tc) and [int(x.group(1)) for x in tc] == list(range(nt)))
    parniv = {}; prefs = []; okp = True
    for x in tc:
        niv = int(x.group(2)); parniv[niv] = parniv.get(niv, 0) + 1
        kv = [q.split("=") for q in x.group(3).split(",")] if x.group(3) else []
        okp &= [int(a) for a, _ in kv] == list(range(niv + 1, 44))
        prefs.append(tuple(int(b) for _, b in reversed(kv)))
        okp &= float.fromhex(x.group(4)) >= 0
    controle("R5 cote %d : chaque tache fixe exactement les coordonnees niv+1..43 ; PL >= 0 ; repartition par niveau = journal" % cote, okp and parniv == J["parniv"])
    sp = sorted(prefs)
    controle("R5 cote %d : prefixes deux a deux incomparables (sous-arbres disjoints)" % cote, all(a != b[:len(a)] for a, b in zip(sp, sp[1:])))
    oks = True
    for x, pf in zip(tc, prefs):
        nzv = next((v for v in pf if v != 0), None)
        oks &= (nzv is None) == (x.group(5) == "true") and (nzv is None or nzv > 0)
    controle("R5 cote %d : normalisation de signe : premiere coordonnee non nulle > 0 ; drapeau zero <=> prefixe nul" % cote, oks)

# ---------------------------------------------------------------- R7 : inventaire
INV = {}
finv = os.path.join(DC, "replication", "INVENTAIRE_SORTIE.txt")
for l in open(finv, encoding="ascii"):
    if l.strip() and not l.startswith("#"):
        nm, taille = l.split(); INV[nm] = int(taille)
print("== R7 inventaire du repertoire de sortie de l'execution de reference (%s) : %s" % (rel(finv), ", ".join(sorted(INV))))
controle("R7 aucun fichier de touche (*.touches) dans le repertoire de sortie de l'execution de reference ; les deux recus y figurent",
         not any(nm.endswith(".touches") for nm in INV) and "science/cote1.ckpt" in INV and "science/cote2.ckpt" in INV)
okt = all(os.path.getsize(os.path.join(DC, "replication", os.path.basename(nm))) == t for nm, t in INV.items()
          if os.path.exists(os.path.join(DC, "replication", os.path.basename(nm))) and nm.startswith("science/"))
controle("R7 les fichiers conserves dans data/%s/replication/ ont les tailles de l'inventaire" % CAND, okt)

# ---------------------------------------------------------------- execution de reference (second ordinateur)
BIL = {}
for cote in (1, 2):
    print("== execution de reference (second ordinateur), cote %d" % cote)
    nom = "reference cote %d" % cote
    J = analyse_journal(os.path.join(DC, "replication", "cote%d.stdout.log" % cote), cote)
    print("   JVM : %s ; %d fils ; %d taches ; duree imprimee %s s" % (J["jvm"], J["fils"], J["nt"], J["duree"]))
    controle_journal_commun(J, nom, cote)
    controle("R3 %s : JVM OpenJDK 21 sous Linux" % nom, re.search(r"VM 21\.[\d.]+ ; Linux", J["jvm"]) is not None)
    controle_lancement_neuf(J, nom)
    ex = open(os.path.join(DC, "replication", "cote%d.java.exit" % cote), "rb").read()
    err = lire(os.path.join(DC, "replication", "cote%d.stderr.log" % cote))
    controle("R3 %s : code de sortie Java = 0 (cote%d.java.exit) ; stderr = la seule ligne d'information de la JVM, sans exception" % (nom, cote),
             ex.strip() == b"0" and [x for x in err.split("\n") if x] == [x for x in err.split("\n") if x.startswith("NOTE: Picked up JDK_JAVA_OPTIONS")] and "Exception" not in err)
    R = controle_recus(os.path.join(DC, "replication", "cote%d.ckpt" % cote), J, nom, cote)
    bc = controle_catalogue(cote, J, nom)
    controle_structure_catalogue(bc, J, cote)
    BIL[("ref", cote)] = (J, R)

# ---------------------------------------------------------------- premiere execution (premier ordinateur)
PE = os.path.join(DC, "premiere_execution")
for cote in (1, 2):
    print("== premiere execution (premier ordinateur), cote %d" % cote)
    nom = "premiere cote %d" % cote
    if CAND == "P599" and cote == 1:
        J1 = analyse_journal(os.path.join(PE, "cote1_lancement1.log"), 1); J = analyse_journal(os.path.join(PE, "cote1_lancement2.log"), 1)
        for JJ, nn in ((J1, "premiere cote 1, lancement 1"), (J, "premiere cote 1, lancement 2")):
            print("   JVM : %s ; %d fils" % (JJ["jvm"], JJ["fils"]))
            controle_journal_commun(JJ, nn, 1)
            controle("R8 %s : stderr vide" % nn, os.path.getsize(os.path.join(PE, "cote1_lancement%s.err" % nn[-1])) == 0)
        nt = J["nt"]
        controle("R8 lancement 1 : CHECKPOINT nouveau, SELECTION %d/%d, puis arret force (aucun bilan, aucune touche ni erreur)" % (nt, nt),
                 "CHECKPOINT nouveau" in J1["texte"] and ("SELECTION %d/%d ; A_FAIRE %d ; DEJA_AU_CHECKPOINT 0" % (nt, nt, nt)) in J1["lignes"]
                 and "COUVERTURE" not in J1["texte"] and not re.search(r"^(ERREUR|TOUCHE)", J1["texte"], re.M) and J1["shacat"] == J["shacat"])
        avant = os.path.join(PE, "cote1_avant_reprise.ckpt"); ba = open(avant, "rb").read()
        mr = re.search(r"REPRISE : (\d+) taches deja terminees lues dans \S+ \(SHA-256 a la lecture ([0-9a-f]{64})\)", J["texte"])
        nrep = int(mr.group(1))
        controle("R8 lancement 2 : REPRISE de %d recus ; SHA a la lecture = SHA de cote1_avant_reprise.ckpt ; SELECTION %d/%d ; A_FAIRE %d ; DEJA_AU_CHECKPOINT %d"
                 % (nrep, nt, nt, nt - nrep, nrep),
                 hashlib.sha256(ba).hexdigest() == mr.group(2) and ("SELECTION %d/%d ; A_FAIRE %d ; DEJA_AU_CHECKPOINT %d" % (nt, nt, nt - nrep, nrep)) in J["lignes"]
                 and ("EXECUTEES_CE_LANCEMENT %d ; REPRISES_DU_CHECKPOINT %d" % (nt - nrep, nrep)) in J["lignes"] and ("TACHES_TERMINEES %d/%d" % (nt, nt)) in J["lignes"])
        controle_fin(J, "premiere cote 1, lancement 2")
        R = controle_recus(os.path.join(PE, "cote1.ckpt"), J, nom, 1)
        bf = open(os.path.join(PE, "cote1.ckpt"), "rb").read()
        lav = ba.decode("ascii").split("\n")
        controle("R8 reprise : cote1_avant_reprise.ckpt est, octet pour octet, le debut du fichier final ; pas de ligne tronquee", bf.startswith(ba) and ba.endswith(b"\n"))
        iav = [int(x.split("|")[1]) for x in lav[1:-1]]
        iap = [int(x.split("|")[1]) for x in bf[len(ba):].decode("ascii").split("\n")[:-1]]
        controle("R8 reprise : %d indices repris et %d executes ensuite, disjoints, de reunion 0..%d" % (len(iav), len(iap), nt - 1),
                 len(iav) == nrep and len(iap) == nt - nrep and set(iav).isdisjoint(iap) and sorted(iav + iap) == list(range(nt)))
        # rejeu complet des taches reprises
        frj = os.path.join(DC, "rejeu_reprises", "rejeu_cote1.ckpt"); brj = open(frj, "rb").read()
        lrj = brj.decode("ascii").split("\n")
        liste = [int(x) for x in open(os.path.join(DC, "rejeu_reprises", "liste_taches_reprises.txt"), encoding="ascii").read().split()]
        controle("R8 rejeu : la liste des taches rejouees est exactement l'ensemble des %d indices repris" % nrep, sorted(liste) == sorted(iav) and len(set(liste)) == len(liste))
        controle("R8 rejeu : meme en-tete que les recus d'origine (memes parametres, catalogue, entrees, classes)", lrj[0] == lav[0])
        controle("R8 rejeu : les %d recus rejoues sont identiques octet pour octet a ceux d'avant reprise (comparaison par indice)" % nrep,
                 brj.endswith(b"\n") and sorted(lrj[1:-1]) == sorted(lav[1:-1]))
        corps_final = set(R["corps"])
        controle("R8 rejeu : ces %d recus figurent aussi, a l'identique, dans le fichier final" % nrep, all(x in corps_final for x in lrj[1:-1]))
        print("      SHA du fichier de rejeu %s ; SHA du fichier d'avant reprise %s" % (hashlib.sha256(brj).hexdigest(), hashlib.sha256(ba).hexdigest()))
    else:
        J = analyse_journal(os.path.join(PE, "cote%d.log" % cote), cote)
        print("   JVM : %s ; %d fils ; duree imprimee %s s" % (J["jvm"], J["fils"], J["duree"]))
        controle_journal_commun(J, nom, cote)
        controle_lancement_neuf(J, nom)
        controle("R8 %s : stderr vide" % nom, os.path.getsize(os.path.join(PE, "cote%d.err" % cote)) == 0)
        R = controle_recus(os.path.join(PE, "cote%d.ckpt" % cote), J, nom, cote)
    controle("R8 %s : JVM OpenJDK 11.0.16.1 sous Windows" % nom, re.search(r"VM 11\.0\.16\.1 ; Windows", J["jvm"]) is not None)
    controle_catalogue(cote, J, nom)
    controle("R6 %s : memes recus que l'execution de reference (ensembles de lignes egaux)" % nom, sorted(R["corps"]) == sorted(BIL[("ref", cote)][1]["corps"]))
    BIL[("prem", cote)] = (J, R)

# ---------------------------------------------------------------- R9 : coherence et compteurs
print("== R9 coherence")
Us = {k: v[0]["U"] for k, v in BIL.items()}; Hs = [v[0]["hist"] for v in BIL.values()]
controle("R9 meme COMPTE_U (%d) et meme histogramme pour les deux cotes et les deux executions" % Us[("ref", 1)], len(set(Us.values())) == 1 and all(h == Hs[0] for h in Hs))
mx = max(max(max(R["U"]), max(R["NA"]), max(R["NB"])) for _, R in BIL.values())
tot = max(sum(J["noeuds"][:2]) for J, _ in BIL.values())
print("   plus grand compteur d'un recu = %d (< 2^%d) ; plus grand total de noeuds d'une execution = %d (< 2^%d)" % (mx, mx.bit_length(), tot, tot.bit_length()))
controle("R9 (Z9) tous les compteurs des recus et tous les totaux sont < 2^43, loin de 2^63", mx < 2 ** 43 and tot < 2 ** 43)
print("BILAN : %d controles, %d echecs" % (NB[0], NB[1]))
print("FIN_OK" if NB[1] == 0 else "FIN_ECHEC")
sys.exit(0 if NB[1] == 0 else 1)
