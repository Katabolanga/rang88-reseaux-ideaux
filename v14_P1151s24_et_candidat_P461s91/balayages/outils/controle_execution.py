# -*- coding: utf-8 -*-
"""controle_execution.py -- controle exact, en lecture seule, d'une execution TERMINEE de Rang88CertZ rapatriee d'une
machine louee (Claude, 16 octobre 2026).  Independant de bilan.sh et d'empreinte_canonique.py (lecture et sommes refaites ici).

Usage : python3 -I controle_execution.py <repertoire run_<C>_cote<s>> <s> <nombre_de_taches> <SHA du catalogue attendu> [ref.ckpt ...]

E1 journal : un seul lancement (le plus recent), CHECKPOINT nouveau, SELECTION nt/nt, DEJA_AU_CHECKPOINT 0,
   EXECUTEES_CE_LANCEMENT nt, REPRISES 0, TACHES_TERMINEES nt/nt, TOTAL_TOUCHES 0, COUVERTURE_COMPLETE nt/nt, FIN ;
   aucune ligne ERREUR / TOUCHE / ARRET / REPRISE ; code de sortie 0 ; stderr vide ;
E2 catalogue : SHA du fichier .taches = CATALOGUE_SHA256 du journal = champ catalogue de l'en-tete des recus = valeur attendue ;
E3 recus : nt lignes au format strict, indices = permutation de 0..nt-1, TOUCHES = 0 partout ;
E4 sommes des recus = totaux du journal (COMPTE_U, CVP, NOEUDS court = somme des NA + noeuds de generation, fibre) ;
   somme des HIST = histogramme du journal ; recu par recu : CVP = U, somme de HIST = U, NA >= 1 (comme verifier_recus.py, R4) ;
E5 SHA du fichier de recus = CHECKPOINT_SHA256 du journal ; aucun fichier .touches ;
E6 empreinte canonique (recus tries par indice, chacun suivi de LF, SHA-256), calculee de deux facons ;
E7 (facultatif) comparaison tache par tache aux recus de reference fournis (taches communes, egalite a l'octet)."""
import sys, os, re, hashlib, glob

def sha(f):
    return hashlib.sha256(open(f, "rb").read()).hexdigest()

if len(sys.argv) < 5:
    raise SystemExit(__doc__)
D, S, NT, CAT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
REFS = sys.argv[5:]
NB = [0, 0]
def controle(nom, cond):
    NB[0] += 1
    if not cond:
        NB[1] += 1
    print(("OK    " if cond else "ECHEC ") + nom)

# ---- E1 journal
logs = sorted(glob.glob(os.path.join(D, "cote%d_*.stdout.log" % S)))
controle("E1 un seul journal de lancement (%d trouve(s))" % len(logs), len(logs) == 1)
L = logs[-1]
J = open(L, "rb").read().decode("ascii", "replace").replace("\r\n", "\n")
def un(rx):
    m = re.findall(rx, J, re.M)
    return m[0] if len(m) == 1 else None
controle("E1 CHECKPOINT nouveau", un(r"^CHECKPOINT nouveau : ") is not None)
controle("E1 SELECTION %d/%d ; A_FAIRE %d ; DEJA_AU_CHECKPOINT 0" % (NT, NT, NT), un(r"^SELECTION %d/%d ; A_FAIRE %d ; DEJA_AU_CHECKPOINT 0$" % (NT, NT, NT)) is not None)
controle("E1 EXECUTEES_CE_LANCEMENT %d ; REPRISES_DU_CHECKPOINT 0" % NT, un(r"^EXECUTEES_CE_LANCEMENT %d ; REPRISES_DU_CHECKPOINT 0$" % NT) is not None)
controle("E1 TACHES_TERMINEES %d/%d" % (NT, NT), un(r"^TACHES_TERMINEES %d/%d$" % (NT, NT)) is not None)
controle("E1 TOTAL_TOUCHES 0", un(r"^TOTAL_TOUCHES 0$") is not None)
controle("E1 COUVERTURE_COMPLETE %d/%d" % (NT, NT), un(r"^COUVERTURE_COMPLETE %d/%d ; CATALOGUE [0-9a-f]{64}$" % (NT, NT)) is not None)
controle("E1 ligne FIN", un(r"^FIN \[\d+ s\]$") is not None)
controle("E1 aucune ligne ERREUR / TOUCHE / ARRET / REPRISE / Exception",
         not re.search(r"^(ERREUR|TOUCHE|ARRET|REPRISE)|Exception", J, re.M))
ex = L.replace(".stdout.log", ".java.exit"); se = L.replace(".stdout.log", ".stderr.log")
controle("E1 code de sortie 0", os.path.exists(ex) and open(ex).read().strip() == "0")
controle("E1 stderr vide", os.path.exists(se) and os.path.getsize(se) == 0)

# ---- E2 catalogue
fcat = os.path.join(D, "cote%d.taches" % S)
hcat = sha(fcat)
jcat = re.search(r"^CATALOGUE_SHA256 ([0-9a-f]{64}) ; TOTAL_TACHES (\d+)$", J, re.M)
fck = os.path.join(D, "cote%d.ckpt" % S)
brut = open(fck, "rb").read()
lignes = brut.decode("ascii").split("\n")
entete = lignes[0]
controle("E2 SHA du catalogue = valeur attendue %s..." % CAT[:8], hcat == CAT)
controle("E2 CATALOGUE_SHA256 du journal = SHA du fichier ; TOTAL_TACHES %d" % NT, jcat is not None and jcat.group(1) == hcat and int(jcat.group(2)) == NT)
controle("E2 en-tete des recus : catalogue et total", ("|catalogue=%s|" % hcat) in entete and ("|total=%d|" % NT) in entete)

# ---- E3 recus
controle("E3 fichier de recus termine par LF", brut.endswith(b"\n"))
corps = lignes[1:-1]
RX = re.compile(r"^T\|(0|[1-9]\d*)\|U=(\d+)\|CVP=(\d+)\|NA=(\d+)\|NB=(\d+)\|TOUCHES=(\d+)\|HIST=((?:\d+:\d+(?:,\d+:\d+)*)?)\|FIN$")
ms = [RX.match(x) for x in corps]
controle("E3 %d lignes de recu au format strict (%d lues)" % (NT, len(corps)), len(corps) == NT and all(ms))
idx = [int(m.group(1)) for m in ms if m]
controle("E3 indices = permutation de 0..%d" % (NT - 1), sorted(idx) == list(range(NT)))
controle("E3 TOUCHES = 0 dans chaque recu", all(m and m.group(6) == "0" for m in ms))

# ---- E4 sommes
sU = sum(int(m.group(2)) for m in ms); sC = sum(int(m.group(3)) for m in ms)
sA = sum(int(m.group(4)) for m in ms); sB = sum(int(m.group(5)) for m in ms)
cu = re.search(r"^COMPTE_U \(au signe pres, energie courte <= [0-9/]+\) (\d+) ; histogramme (.*)$", J, re.M)
no = re.search(r"^NOEUDS court (\d+) ; fibre (\d+) ; CVP (\d+)$", J, re.M)
controle("E4 somme des U = COMPTE_U du journal (%d)" % sU, cu is not None and int(cu.group(1)) == sU)
controle("E4 somme des CVP = CVP du journal (%d)" % sC, no is not None and int(no.group(3)) == sC)
ng = re.search(r"\((\d+) noeuds de generation\)", J)    # le journal imprime NOEUDS court = somme des NA + noeuds de generation du catalogue (source, l. 515)
controle("E4 somme des NA + %s noeuds de generation = NOEUDS court (%d)" % (ng.group(1) if ng else "?", sA), no is not None and ng is not None and int(no.group(1)) == sA + int(ng.group(1)))
def hsum(m):
    return sum(int(kv.split(":")[1]) for kv in m.group(7).split(",")) if m.group(7) else 0
controle("E4 chaque recu : CVP = U, somme de HIST = U, NA >= 1", all(m and m.group(3) == m.group(2) and hsum(m) == int(m.group(2)) and int(m.group(4)) >= 1 for m in ms))
controle("E4 somme des NB = NOEUDS fibre (%d)" % sB, no is not None and int(no.group(2)) == sB)
H = {}
for m in ms:
    if m and m.group(7):
        for kv in m.group(7).split(","):
            k, v = kv.split(":"); H[int(k)] = H.get(int(k), 0) + int(v)
HJ = {}
if cu:
    for a, b, v in re.findall(r"\[(\d+\.\d),(\d+\.\d)\):(\d+)", cu.group(2)):
        HJ[int(round(float(a) * 10))] = int(v)
controle("E4 somme des HIST des recus = histogramme du journal (%d cases) ; total HIST = somme des U" % len(HJ), H == HJ and sum(H.values()) == sU)

# ---- E5 fichier de recus et touches
jck = re.search(r"^CHECKPOINT_SHA256 ([0-9a-f]{64}) ; ", J, re.M)
controle("E5 SHA du fichier de recus = CHECKPOINT_SHA256 du journal", jck is not None and jck.group(1) == hashlib.sha256(brut).hexdigest())
controle("E5 aucun fichier .touches dans le repertoire", not glob.glob(os.path.join(D, "*.touches")))

# ---- E6 empreinte canonique, deux facons
tri = sorted(corps, key=lambda x: int(x.split("|")[1]))
h1 = hashlib.sha256("".join(x + "\n" for x in tri).encode("ascii")).hexdigest()
par = {int(x.split("|")[1]): x for x in corps}
g = hashlib.sha256()
for i in range(NT):
    g.update(par[i].encode("ascii")); g.update(b"\n")
h2 = g.hexdigest()
controle("E6 empreinte canonique (deux calculs) %s" % h1, h1 == h2)

# ---- E7 references
for r in REFS:
    ref = {}
    for x in open(r, encoding="ascii"):
        if x.startswith("T|"):
            ref[int(x.split("|")[1])] = x.rstrip("\r\n")
    com = sorted(set(ref) & set(par))
    dif = [i for i in com if ref[i] != par[i]]
    controle("E7 reference %s : %d recus communs, %d differents" % (os.path.basename(r), len(com), len(dif)), com and not dif)

print("BILAN : %d controles, %d echecs ; |U| = %d ; empreinte canonique %s" % (NB[0], NB[1], sU, h1))
print("CONTROLE_OK" if NB[1] == 0 else "CONTROLE_ECHEC")
sys.exit(0 if NB[1] == 0 else 1)
