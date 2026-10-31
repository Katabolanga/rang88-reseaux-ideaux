# -*- coding: utf-8 -*-
"""verifier_jumeau_P461s91.py -- controle documentaire, en lecture seule, des recus du balayage de X(P461 sigma_91) (Crapaud08, V2,
19-20 oct. 2026) contre les recus COMPLETS publies de son jumeau de recollement P461 sigma_24 (Scaleway AMS3, 16 oct. 2026, depot
public v1.1, calcul_externe_resultats_20261015/final_P461s24_AMS3/run_P461s24_coteN.tar.gz).  Claude, 30 oct. 2026.

Les deux ideaux ont les MEMES fichiers du cote court (coteN_A.gram, coteN_B.gram, coteN_meta.txt identiques a l'octet) et le
meme catalogue de taches ; seul le recollement coteN_T.mat differe.  Le cote court d'une tache (U, CVP, NA, HIST) ne depend pas
du recollement ; la fibre (NB, TOUCHES) en depend.  Ce script verifie, tache par tache :
  J0  archive du jumeau : SHA-256 = valeur de SHA256SUMS_RAPATRIEMENT.txt du depot ; SHA du ckpt = CHECKPOINT_SHA256 de bilan_P461s24.txt ;
  J1  en-tetes : meme total, meme catalogue, parametres identiques ; empreinte 'entrees' differente (T differe) ;
  J2  memes indices, permutation complete de 0..total-1, recus au format strict ;
  J3  pour CHAQUE tache : U, CVP, NA et HIST identiques ; TOUCHES = 0 des deux cotes ; on compte les NB egaux (information) ;
  J4  (cote 1, si le seed est donne) les 2 089 recus herites du lancement interrompu (seed_inputs/cote1.ckpt) : en-tete identique,
      chaque ligne identique a la ligne finale de meme indice ; parmi eux, ceux qui figurent dans la reference E7 (filtre du 17 oct.)
      et ceux qui n'y figurent pas ; J3 restreint a ces derniers.
Portee : constat documentaire.  J3 recoupe, sur une autre machine et un autre lancement, la partie COURTE de chaque tache ; il ne dit
rien de la fibre (NB, recherche des touches), qui est la partie propre a P461 sigma_91 et n'est PAS repliquee.
Usage : python3 -I verifier_jumeau_P461s91.py <cote> <ckpt P461s91> <tar.gz P461s24> <SHA256SUMS_RAPATRIEMENT.txt> <bilan_P461s24.txt> [<seed.ckpt> <ref_E7.ckpt>]"""
import sys, os, re, hashlib, tarfile

RX = re.compile(r"^T\|(0|[1-9]\d*)\|U=(\d+)\|CVP=(\d+)\|NA=(\d+)\|NB=(\d+)\|TOUCHES=(\d+)\|HIST=((?:\d+:\d+(?:,\d+:\d+)*)?)\|FIN$")
NB = [0, 0]
def controle(nom, c):
    NB[0] += 1; NB[1] += (not c); print(("OK    " if c else "ECHEC ") + nom); sys.stdout.flush()
def sha_b(b): return hashlib.sha256(b).hexdigest()
def lire(brut):
    l = brut.decode("ascii").split("\n")
    assert l[-1] == "", "derniere ligne incomplete"
    ent, corps = l[0], l[1:-1]
    d = {}; ok = True
    for x in corps:
        m = RX.match(x)
        if not m: ok = False; continue
        d[int(m.group(1))] = (m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7), x)
    return ent, d, ok, len(corps)
def champs(ent):
    return dict(kv.split("=", 1) for kv in ent.split("|")[1:])

if len(sys.argv) not in (6, 8): raise SystemExit(__doc__)
S = int(sys.argv[1]); F91, TGZ, SUMS, BIL = sys.argv[2:6]
print("source : %s SHA-256 %s" % (os.path.basename(__file__), sha_b(open(os.path.abspath(__file__), "rb").read())))
print("cote %d ; P461s91 : %s ; jumeau P461s24 : %s" % (S, F91, TGZ))
# J0
htgz = sha_b(open(TGZ, "rb").read())
attendu = {}
for x in open(SUMS, encoding="ascii"):
    if x.strip(): h, n = x.split(); attendu[os.path.basename(n.lstrip("*"))] = h
controle("J0 SHA-256 de %s = %s... (SHA256SUMS_RAPATRIEMENT.txt du depot)" % (os.path.basename(TGZ), htgz[:16]), attendu.get(os.path.basename(TGZ)) == htgz)
with tarfile.open(TGZ, "r:gz") as t:
    m = t.getmember("run_P461s24_cote%d/cote%d.ckpt" % (S, S))
    b24 = t.extractfile(m).read()
bil = open(BIL, encoding="ascii").read()
ck = re.findall(r"^CHECKPOINT_SHA256 ([0-9a-f]{64}) ; run_P461s24_cote%d/cote%d.ckpt$" % (S, S), bil, re.M)
controle("J0 SHA-256 du ckpt du jumeau (lu dans l'archive, sans extraction sur disque) = CHECKPOINT_SHA256 de bilan_P461s24.txt (%s...)" % sha_b(b24)[:16],
         len(ck) == 1 and ck[0] == sha_b(b24))
b91 = open(F91, "rb").read()
print("      SHA-256 des recus P461s91 cote %d : %s" % (S, sha_b(b91)))
e91, d91, ok91, n91 = lire(b91); e24, d24, ok24, n24 = lire(b24)
c91, c24 = champs(e91), champs(e24)
# J1
memes = all(c91.get(k) == c24.get(k) for k in ("mode", "n", "BA", "S", "DA", "DB", "d", "F", "D", "Dmax", "seuil", "total", "catalogue", "classes"))
controle("J1 en-tetes : memes parametres, total %s, catalogue %s..., classes %s..." % (c91.get("total"), c91.get("catalogue", "")[:16], c91.get("classes", "")[:16]), memes)
controle("J1 en-tetes : empreintes 'entrees' differentes (recollement T different) : %s... / %s..." % (c91.get("entrees", "")[:16], c24.get("entrees", "")[:16]),
         c91.get("entrees") != c24.get("entrees"))
# J2
tot = int(c91["total"])
controle("J2 recus au format strict : %d (P461s91) et %d (P461s24) lignes" % (n91, n24), ok91 and ok24 and n91 == len(d91) == tot and n24 == len(d24) == tot)
controle("J2 memes indices, permutation de 0..%d" % (tot - 1), sorted(d91) == list(range(tot)) == sorted(d24))
# J3
diff_court = [i for i in d91 if i in d24 and (d91[i][0], d91[i][1], d91[i][2], d91[i][5]) != (d24[i][0], d24[i][1], d24[i][2], d24[i][5])]
nb_eg = sum(1 for i in d91 if i in d24 and d91[i][3] == d24[i][3])
controle("J3 cote court identique tache par tache (U, CVP, NA, HIST) : %d taches, %d differences" % (len(d91), len(diff_court)), not diff_court and len(d91) == tot)
controle("J3 TOUCHES = 0 dans chaque recu des deux reseaux", all(v[4] == "0" for v in d91.values()) and all(v[4] == "0" for v in d24.values()))
sU = sum(int(v[0]) for v in d91.values())
print("      information : somme des U = %d ; NB egal pour %d taches sur %d (la fibre depend du recollement)" % (sU, nb_eg, tot))
# J4
if len(sys.argv) == 8:
    bs = open(sys.argv[6], "rb").read(); es, ds, oks, ns = lire(bs)
    print("      seed : %s ; SHA-256 %s" % (sys.argv[6], sha_b(bs)))
    controle("J4 seed : en-tete identique a celui des recus finaux", es == e91)
    controle("J4 seed : %d recus au format strict, indices distincts" % ns, oks and ns == len(ds))
    controle("J4 seed : chaque recu herite est identique a la ligne finale de meme indice", all(i in d91 and d91[i][6] == ds[i][6] for i in ds))
    ref = {}
    for x in open(sys.argv[7], encoding="ascii"):
        if x.startswith("T|"): ref[int(x.split("|")[1])] = x.rstrip("\r\n")
    dans = [i for i in ds if i in ref]; hors = [i for i in ds if i not in ref]
    controle("J4 parmi les %d herites : %d dans la reference E7 (identiques : %d), %d hors de E7" % (len(ds), len(dans), sum(1 for i in dans if ref[i] == ds[i][6]), len(hors)),
             all(ref[i] == ds[i][6] for i in dans))
    controle("J4 les %d herites hors de E7 ont un cote court (U, CVP, NA, HIST) identique a celui du jumeau" % len(hors),
             all((d91[i][0], d91[i][1], d91[i][2], d91[i][5]) == (d24[i][0], d24[i][1], d24[i][2], d24[i][5]) for i in hors))
print("BILAN : %d controles, %d echecs" % (NB[0], NB[1]))
print("JUMEAU_COURT_IDENTIQUE" if NB[1] == 0 else "JUMEAU_ECHEC")
sys.exit(0 if NB[1] == 0 else 1)
