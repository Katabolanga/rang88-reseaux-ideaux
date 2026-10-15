# -*- coding: utf-8 -*-
"""verifier_sha256.py -- controle l'empreinte SHA-256 de chaque fichier du depot listee dans SHA256SUMS.txt (format
sha256sum : empreinte, deux espaces, chemin relatif), et signale les fichiers presents qui n'y figurent pas.
Usage (depuis la racine du depot) : python -I code/verification/verifier_sha256.py"""
import os, sys, hashlib
RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
IGNORES = {"SHA256SUMS.txt", "externe/integer_input.txt"}
attendu = {}
for l in open(os.path.join(RACINE, "SHA256SUMS.txt"), encoding="ascii"):
    if l.strip():
        h, chemin = l.rstrip("\n").split("  ", 1); attendu[chemin] = h
ok = ko = 0
for chemin, h in sorted(attendu.items()):
    f = os.path.join(RACINE, *chemin.split("/"))
    if not os.path.isfile(f): print("ABSENT  ", chemin); ko += 1; continue
    hh = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): hh.update(b)
    if hh.hexdigest() == h: ok += 1
    else: print("DIFFERENT", chemin); ko += 1
presents = set()
for d, _, fs in os.walk(RACINE):
    if os.path.basename(d) == ".git" or os.sep + ".git" + os.sep in d + os.sep: continue
    for x in fs:
        r = os.path.relpath(os.path.join(d, x), RACINE).replace(os.sep, "/")
        if r not in IGNORES and not r.startswith(".git/"): presents.add(r)
hors = sorted(presents - set(attendu))
for r in hors: print("NON LISTE", r)
print("BILAN : %d fichiers conformes, %d absents ou differents, %d fichiers non listes" % (ok, ko, len(hors)))
sys.exit(0 if ko == 0 and not hors else 1)
