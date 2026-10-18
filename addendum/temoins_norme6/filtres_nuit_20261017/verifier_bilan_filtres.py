# -*- coding: utf-8 -*-
"""verifier_bilan_filtres.py -- controle, en LECTURE SEULE, du bilan des 21 filtres de la nuit du 16 au 17 octobre 2026
(addendum, par. 4.5, tableau 4).  Bibliotheque standard seulement ; aucun fichier n'est ecrit.

Ce script refait le calcul du generateur qui a produit les tableaux de l'addendum (tableau_filtres.py, 17 octobre 2026,
non publie : il ecrivait dans un dossier du poste de l'auteur), a partir des seules pieces de ce dossier, et compare :
  F1  l'audit de reference AUDIT_REJETS_20261017_044917.txt a l'empreinte SHA-256 citee en tete de addendum/comptes_filtres.tex
      et de addendum/couts_recensement.tex ; il compte 4 rejets, tous « REJET DEMONTRE », et se termine par
      AUDIT_TOUS_REJETS_VALIDES ;
  F2  BILAN_FILTRES.txt contient 21 filtres distincts : 4 rejets (ceux de l'audit) et 17 survivants partiels ;
  F3  pour chaque filtre, les deux journaux, codes de sortie et fichiers de recus de executions/ sont presents ; un fichier
      de touches existe pour le cote de chaque rejet et pour lui seul ; la ligne TOUCHE du journal Java est celle du fichier
      de touches et celle du bilan (energies) ;
  F4  les lignes du tableau 4 recalculees (heure, anneau, ideal, verdict, millions de projections courtes = somme des champs
      U= des recus des deux cotes, duree, energies) sont identiques, octet pour octet, a addendum/tableau_filtres_fr.tex et
      addendum/tableau_filtres_en.tex ;
  F5  les macros de comptes (21 filtres, 4 rejets, 17 survivants, par anneau, projections extremes des survivants, queues
      binomiales de l'heuristique) sont identiques, octet pour octet, a addendum/comptes_filtres.tex.
Statut : les rejets sont demontres par leurs temoins (../verifier_temoins_norme6.gp et .py) ; ce script ne controle que la
coherence du bilan, des journaux et des tableaux.  Les survivants partiels sont constates : un filtre arrete ne prouve rien.
Usage (depuis la racine du depot) :  python3 -I addendum/temoins_norme6/filtres_nuit_20261017/verifier_bilan_filtres.py"""
import hashlib, os, re, sys
from math import comb
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

ICI = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(ICI, "executions")
ADD = os.path.normpath(os.path.join(ICI, "..", ".."))
AUDIT = "AUDIT_REJETS_20261017_044917.txt"
NB = [0, 0]
def chk(c, s):
    NB[0] += 1; NB[1] += bool(c)
    print("%s %s" % ("OK   " if c else "ECHEC", s)); sys.stdout.flush()
    return bool(c)
def lire(f, mode="r"):
    return open(f, "rb").read() if mode == "rb" else open(f, encoding="utf-8", errors="replace").read()

# F1 : audit de reference
octets = lire(os.path.join(ICI, AUDIT), "rb"); sha = hashlib.sha256(octets).hexdigest()
entetes = [lire(os.path.join(ADD, f)).splitlines()[0] for f in ("comptes_filtres.tex", "couts_recensement.tex")]
valides = {}
for l in octets.decode("utf-8").splitlines():
    if l.startswith("#") or l.startswith("BILAN") or l.startswith("AUDIT_"): continue
    ch = [c.strip() for c in l.split("|")]
    if len(ch) < 7: continue
    valides[ch[0]] = (ch[1] == "0" and ch[2] == "TEMOIN_NORME6_OK" and ch[3] == "1" and ch[4].isdigit() and int(ch[4]) >= 1
                      and ch[5] == "0" and ch[6].startswith("REJET DEMONTRE"))
chk(all(("audit de reference %s (sha256 %s)" % (AUDIT, sha)) in e for e in entetes) and len(valides) == 4 and all(valides.values())
    and octets.decode("utf-8").rstrip("\n").endswith("AUDIT_TOUS_REJETS_VALIDES"),
    "F1 : audit de reference %s, SHA-256 %s, cite par comptes_filtres.tex et couts_recensement.tex ; 4 rejets demontres" % (AUDIT, sha))

# F2 : bilan
lignes = [l.rstrip("\n") for l in lire(os.path.join(ICI, "BILAN_FILTRES.txt")).splitlines() if l.strip() and not l.startswith("#")]
noms = [[c.strip() for c in l.split(" | ")][1] for l in lignes]
rej = [n for n, l in zip(noms, lignes) if [c.strip() for c in l.split(" | ")][3].startswith("REJETE")]
sur = [n for n, l in zip(noms, lignes) if [c.strip() for c in l.split(" | ")][3].startswith("SURVIVANT")]
chk(len(lignes) == 21 and len(set(noms)) == 21 and len(rej) == 4 and len(sur) == 17 and set(rej) == set(valides),
    "F2 : BILAN_FILTRES.txt : 21 filtres distincts, 4 rejets (ceux de l'audit), 17 survivants partiels")

# F3 : executions
def projections(nom, c):
    s = 0
    for l in lire(os.path.join(EXE, "%s_c%d.ckpt" % (nom, c))).splitlines():
        if l.startswith("T|"):
            mm = re.search(r"\|U=(\d+)\|", l)
            if mm: s += int(mm.group(1))
    return s
ok3 = True; pb = []
for nom, l in zip(noms, lignes):
    details = [c.strip() for c in l.split(" | ")][4]
    for c in (1, 2):
        for ext in (".log", ".exit", ".ckpt"):
            if not os.path.exists(os.path.join(EXE, "%s_c%d%s" % (nom, c, ext))): ok3 = False; pb.append("%s_c%d%s absent" % (nom, c, ext))
    cotes_touche = [c for c in (1, 2) if os.path.exists(os.path.join(EXE, "%s_c%d.ckpt.touches" % (nom, c)))]
    if nom in rej:
        mm = re.search(r"cote (\d) : [^;]*TOUCHE (court=\S+ fibre\(num\)=\S+)", details)
        if not mm or cotes_touche != [int(mm.group(1))]: ok3 = False; pb.append("%s : cote de la touche" % nom); continue
        c = int(mm.group(1))
        tou = lire(os.path.join(EXE, "%s_c%d.ckpt.touches" % (nom, c))).strip().splitlines()
        jl = [x.strip() for x in lire(os.path.join(EXE, "%s_c%d.log" % (nom, c))).splitlines() if x.startswith("TOUCHE ")]
        if len(tou) != 1 or jl != [tou[0].strip()] or not tou[0].startswith("TOUCHE " + mm.group(2) + " "):
            ok3 = False; pb.append("%s : ligne TOUCHE" % nom)
    elif cotes_touche:
        ok3 = False; pb.append("%s : fichier de touches pour un survivant" % nom)
chk(ok3, "F3 : 42 journaux, codes de sortie et fichiers de recus ; touches des 4 rejets concordantes (journal, fichier, bilan)%s" % ("" if ok3 else " : " + "; ".join(pb)))

# F4 : lignes du tableau 4 (meme calcul que tableau_filtres.py)
def ideal_tex(nom):
    mm = re.match(r"P(\d+)(s24)?$", nom); p = mm.group(1)
    return r"$P_{%s}\sigma_{24}(P_{%s})$" % (p, p) if mm.group(2) else r"$P_{%s}$" % p
EN, FR = [], []
for l in lignes:
    ch = [c.strip() for c in l.split(" | ")]
    nom, orb, verdict, details = ch[1], ch[2], ch[3], ch[4]
    h = int(re.search(r"h(\d+)", orb).group(1)); ext = orb.startswith("{331}")
    duree = int(re.search(r"(\d+) s ;", details).group(1))
    proj = projections(nom, 1) + projections(nom, 2)
    if verdict.startswith("REJETE"):
        valide = valides.get(nom, False)
        mm = re.search(r"cote (\d) : [^;]*TOUCHE court=(\d+)/(\d+) fibre\(num\)=(\d+)/\(1\*(\d+)\^2\)", details)
        c, a, da, b, d = mm.groups()
        en = ("rejected (side %s)" % c) if valide else "hit, check pending"
        fr = ("rejeté (côté %s)" % c) if valide else "touche à vérifier"
        energ = r"\rule[-1.6ex]{0pt}{4.4ex}$\frac{%s}{%s}+\frac{%s}{%s^2}$" % (a, da, b, d)
    elif verdict.startswith("SURVIVANT"):
        en, fr, energ = "partial survivor", "survivant partiel", ""
    else:
        en, fr, energ = "to be examined", "à examiner", ""
    mio = "%.1f" % (proj / 1e6)
    EN.append(r"$%d$ & %s & %s & %s & $%s$ & $%d$ & %s \\" % (h, "outer" if ext else "inner", ideal_tex(nom), en, mio, duree, energ))
    FR.append(r"$%d$ & %s & %s & %s & $%s$ & $%d$ & %s \\" % (h, "ext." if ext else "int.", ideal_tex(nom), fr, mio.replace(".", "{,}"), duree, energ))
ten = "\\newcommand{\\lignesfiltresen}{%\n" + "\n".join(EN) + "\n}\n"
tfr = "\\newcommand{\\lignesfiltresfr}{%\n" + "\n".join(FR) + "\n}\n"
chk(ten == lire(os.path.join(ADD, "tableau_filtres_en.tex")), "F4 : 21 lignes recalculees = addendum/tableau_filtres_en.tex (octet pour octet)")
chk(tfr == lire(os.path.join(ADD, "tableau_filtres_fr.tex")), "F4 : 21 lignes recalculees = addendum/tableau_filtres_fr.tex (octet pour octet)")

# F5 : macros de comptes
nrej = sum(1 for l in EN if "rejected" in l); nsur = sum(1 for l in EN if "partial survivor" in l)
nfi = sum(1 for l in EN if "& inner &" in l); nfe = sum(1 for l in EN if "& outer &" in l)
nri = sum(1 for l in EN if "& inner &" in l and "rejected" in l); nre = sum(1 for l in EN if "& outer &" in l and "rejected" in l)
nsi = sum(1 for l in EN if "& inner &" in l and "partial survivor" in l); nse = sum(1 for l in EN if "& outer &" in l and "partial survivor" in l)
projs = [float(re.search(r"& \$([0-9.]+)\$ & \$\d+\$", l).group(1)) for l in EN if "partial survivor" in l]
pmin, pmax = min(projs), max(projs)
mac = [r"\newcommand{\nfiltres}{%d}" % len(EN), r"\newcommand{\nrejets}{%d}" % nrej, r"\newcommand{\nsurv}{%d}" % nsur,
       r"\newcommand{\nfiltint}{%d}" % nfi, r"\newcommand{\nrejint}{%d}" % nri, r"\newcommand{\nfiltext}{%d}" % nfe,
       r"\newcommand{\nrejext}{%d}" % nre, r"\newcommand{\nsurvint}{%d}" % nsi, r"\newcommand{\nsurvext}{%d}" % nse,
       r"\newcommand{\projmin}{%.1f}" % pmin, r"\newcommand{\projmax}{%.1f}" % pmax,
       r"\newcommand{\projminfr}{%s}" % ("%.1f" % pmin).replace(".", "{,}"), r"\newcommand{\projmaxfr}{%s}" % ("%.1f" % pmax).replace(".", "{,}")]
queue = lambda n, k, p: sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k + 1))
pint, pext = 100 * queue(nfi, nri, 1 - 0.0441 ** 0.5), 100 * queue(nfe, nre, 1 - 0.0441 ** 0.25)
mac += [r"\newcommand{\probint}{%.1f}" % pint, r"\newcommand{\probext}{%.1f}" % pext,
        r"\newcommand{\probintfr}{%s}" % ("%.1f" % pint).replace(".", "{,}"), r"\newcommand{\probextfr}{%s}" % ("%.1f" % pext).replace(".", "{,}")]
tmac = "%% genere par tableau_filtres.py ; audit de reference %s (sha256 %s)\n" % (AUDIT, sha) + "\n".join(mac) + "\n"
chk(tmac == lire(os.path.join(ADD, "comptes_filtres.tex")) and (len(EN), nrej, nsur, nfi, nri, nfe, nre) == (21, 4, 17, 10, 3, 11, 1),
    "F5 : macros recalculees = addendum/comptes_filtres.tex (21 filtres ; 4 rejets, 3 int. et 1 ext. ; 17 survivants ; projections %.1f a %.1f millions)" % (pmin, pmax))
print("BILAN : %d controles (attendus 6), %d echecs" % (NB[0], NB[0] - NB[1]))
verdict = NB[0] == 6 and NB[1] == 6
print("BILAN_FILTRES_CONFORME" if verdict else "BILAN_FILTRES_ECHEC")
sys.exit(0 if verdict else 1)
