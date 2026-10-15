# -*- coding: utf-8 -*-
"""empreinte_canonique.py -- empreinte canonique d'un fichier de recus de Rang88CertZ : lignes de recu (apres l'en-tete),
triees par indice numerique, chacune suivie de LF, puis SHA-256.  Valeurs publiees (note, par. 6.2) :
  P139 cote 1 c99dcf87db02e6b51f448cdb3e51da1f8b0ee4bd782b6b0e78d686bed5575122   P139 cote 2 8ab1f40a48c416dd4eab8dde92d0c5866a6ca1951b5edd5d579c5f2ee0bedaf7
  P599 cote 1 f3cf379ad157b1595f9ad96c38d3734a920ea24de3afc5d12dfa617bb3e42689   P599 cote 2 b9c93a83d2b370fad5de5b3d0edc317718ebe4900960642ef98f72c219458ef6
Usage : python -I code/verification/empreinte_canonique.py <fichier.ckpt> [...]"""
import sys, hashlib, re
RX = re.compile(r"^T\|(0|[1-9]\d*)\|U=\d+\|CVP=\d+\|NA=\d+\|NB=\d+\|TOUCHES=\d+\|HIST=(?:\d+:\d+(?:,\d+:\d+)*)?\|FIN$")
for f in sys.argv[1:]:
    brut = open(f, "rb").read()
    if not brut.endswith(b"\n"): print("%s : derniere ligne incomplete" % f)
    l = brut.decode("ascii").split("\n")[:-1]
    corps = l[1:]
    assert all(RX.match(x) for x in corps), "ligne de recu mal formee"
    idx = sorted(int(x.split("|")[1]) for x in corps)
    complet = idx == list(range(len(idx)))
    tot = re.search(r"\|total=(\d+)\|", l[0])
    h = hashlib.sha256("".join(x + "\n" for x in sorted(corps, key=lambda x: int(x.split("|")[1]))).encode("ascii")).hexdigest()
    touches = sum(int(re.search(r"TOUCHES=(\d+)", x).group(1)) for x in corps)
    print("%s : %d recus (total annonce %s, indices %s) ; touches %d ; empreinte canonique %s"
          % (f, len(corps), tot.group(1) if tot else "?", "0..n-1 complets" if complet else "INCOMPLETS", touches, h))
