#!/usr/bin/env python3
"""compare_recus.py -- compare deux fichiers de recus Rang88CertZ (lignes T|indice|...|FIN), tache par tache.

Usage : python3 compare_recus.py NOUVEAU.ckpt REFERENCE.ckpt [--tout]
  Sans --tout : chaque tache du NOUVEAU fichier doit figurer dans la REFERENCE avec une ligne identique a l'octet.
  Avec --tout : on compare seulement les taches communes (le nouveau fichier peut en contenir d'autres).
Code de sortie 0 si aucune difference ; 1 sinon.
"""
import sys


def recus(path):
    d = {}
    with open(path, encoding="ascii") as f:
        for line in f:
            if line.startswith("T|"):
                d[int(line.split("|")[1])] = line.rstrip("\r\n")
    return d


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    a, b = recus(argv[1]), recus(argv[2])
    tout = "--tout" in argv
    communs = sorted(set(a) & set(b))
    diff = [i for i in communs if a[i] != b[i]]
    absents = [] if tout else sorted(set(a) - set(b))
    print("recus nouveaux : %d ; reference : %d ; communs : %d ; differents : %d ; absents de la reference : %d"
          % (len(a), len(b), len(communs), len(diff), len(absents)))
    for i in diff[:5]:
        print("DIFFERENCE tache %d :\n  nouveau   %s\n  reference %s" % (i, a[i], b[i]))
    ok = bool(communs) and not diff and not absents
    print("COMPARAISON_OK" if ok else "COMPARAISON_ECHEC")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
