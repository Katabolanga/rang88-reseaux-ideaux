# Reproduire

Toutes les commandes se lancent **depuis la racine du dépôt**, entrée standard vide (`< /dev/null`). Logiciels utilisés pour les sorties de `verification/RESULTATS.md` : Python 3.11.5 (bibliothèque standard seulement ; Python ≥ 3.9 suffit), PARI/GP 2.15.4, OpenJDK 11.0.16.1 (javac et java). Toujours lancer Python en mode isolé (`-I`). Sous Windows, placer le dépôt dans un chemin court (moins de 100 caractères environ) : PARI/GP et Python refusent les chemins de plus de 260 caractères.

## 1. Rapide : toutes les vérifications exactes (environ 4 min)

```sh
PY=python3 GP=gp sh code/verification/tout_verifier.sh
```

Le script lance, dans l'ordre, les commandes ci-dessous et s'arrête sur un bilan global (`TOUTES LES VERIFICATIONS : code 0`). Durées mesurées sur un portable (Ryzen 7 5700U) :

| Commande | Ce qui est vérifié | Durée |
|---|---|---|
| `python -I code/verification/verifier_sha256.py` | empreinte de chaque fichier (`SHA256SUMS.txt`) | 1 s |
| `python -I code/verification/verifier_corps.py` | Pm, β₀ ≫ 0, β₀𝔇 = O⁺, Gram de H | 1 s |
| `gp -q -D parisize=400000000 code/verification/hmoins115.gp < /dev/null` | h⁻(115) et trois valeurs de contrôle | 1 s |
| `gp -q -D parisize=400000000 code/verification/caracteres115.gp < /dev/null` | caractères, noyaux, 508 463 orbites | 1 s |
| `python -I code/verification/verifier_hmoins_caracteres.py` | second calcul, indépendant, des deux précédents | 1 s |
| `python -I code/verification/verifier_H_L0.py` | H ≅ L₀ (exige `externe/integer_input.txt`) | 5 s |
| `python -I code/verification/verifier_conformite_article.py` | Q G_art Qᵀ = G (exige `externe/integer_input.txt`) | 3 s |
| `gp -q -D parisize=400000000 code/verification/verifier_temoins.gp < /dev/null` | huit témoins de norme 6 | 10 s |
| `python -I code/verification/verifier_temoins.py` | les mêmes, sans PARI/GP, et les trois décompositions du § 6.1 | 1 min |
| `python -I code/verification/verifier_raccord.py P139` (puis `P599`) | raccord géométrique, vecteur de norme 8 | 1 min chacun |
| `python -I code/verification/verifier_recus.py P139` (puis `P599`) | reçus, journaux, catalogues, empreintes canoniques, reprise et rejeu de P₅₉₉ | 5 à 10 s chacun |
| `python -I code/verification/verifier_classe_P139.py` (puis `_P599`) | certificats de classe dans K₂₂ | 10 s chacun |

Sans le fichier de R. Sakamoto, les deux vérifications qui le lisent sont sautées (voir `externe/LISEZMOI.md`).

## 2. Quelques minutes : sous GRH et préparation des entrées

```sh
gp -q -D parisize=800000000 code/sous_grh/localiser_classes.gp < /dev/null     # environ 1 min 20 s (bnfinit en degré 44)
GP=gp sh code/preparation/preparer.sh                                          # environ 1 min 30 s
```

Le premier imprime la classe de N_{L/K}(P) dans Cl(Q(√−23)) (certifié), Cl(K₂₂) et Cl(K₄₄) (sous GRH) pour les quatorze idéaux des tableaux 2 et 3. Le second refait `bnfinit` de Q(ζ₁₁₅)⁺ (sous GRH ; il ne sert qu'à trouver ν), régénère dans `sortie_preparation/` les onze fichiers d'entrée de P₁₃₉ et de P₅₉₉ et les compare octet pour octet à `data/P*/entrees/` (attendu : 22 lignes `IDENTIQUE`). Il écrit `sortie_preparation/` et, parfois, `gp_history.txt` (tous deux ignorés par `.gitignore`).

## 3. La note

```sh
cd article && pdflatex rang88.tex && pdflatex rang88.tex && pdflatex rang88.tex
```

La note se compile avec pdfLaTeX, en trois passes (références croisées et signets) ; paquets : `inputenc`, `fontenc`, `lmodern`, `babel` (français, anglais), `amsart` et ses compagnons, `geometry`, `booktabs`, `enumitem`, `microtype`, `xcolor`, `hyperref`, `xurl`, `array`.

## 4. Essais courts du programme certifiant (Java, quelques secondes chacun)

Ces essais ne relancent aucun balayage complet ; ils écrivent dans un répertoire temporaire choisi par l'utilisateur (`$T` ci-dessous).

```sh
T=$(mktemp -d)        # ou tout répertoire neuf et court
# (a) recompilation : les 8 classes doivent être identiques octet pour octet à code/certifiant/classes/ (même JDK 11.0.16.1)
javac -d "$T/recomp" code/certifiant/Rang88CertZ.java code/certifiant/TestCertZ.java
for f in "$T"/recomp/*.class; do cmp "$f" "code/certifiant/classes/$(basename "$f")" && echo "identique $(basename "$f")"; done

# (b) harnais : comparaison à une recherche exhaustive en entiers sur 300 formes aléatoires (environ 25 s)
java -Xmx1g -Dverif=1 -cp code/certifiant/classes TestCertZ 1 300

# (c) validation sur l'idéal rejeté P461, seuil 7/2, découpage D = 6 : attendu 697 u, 2 touches de norme 6
mkdir -p "$T/val461/java_P461" && cp data/validation/P461/cote1_* "$T/val461/java_P461/"
(cd "$T/val461" && java -Xmx2g -cp "$OLDPWD/code/certifiant/classes" Rang88CertZ run java_P461/cote1 7 2 12 6 6)

# (d) le lanceur, sur le même cas, avec les paramètres de production (arrêt à la première touche) :
BA_NUM=7 BA_DEN=2 sh code/certifiant/rejouer_cote.sh validation/P461 1 "$T/P461_7_2" 4
#     attendu : TOTAL_TOUCHES 1, COUVERTURE_PARTIELLE, et un fichier cote1.ckpt.touches

# (e) catalogues seuls (mode « taches », aucune certification), 2 s par côté : identiques à data/P*/cote*.taches
mkdir -p "$T/cat/java_P139" && cp data/P139/entrees/cote*_* "$T/cat/java_P139/"
(cd "$T/cat" && java -Xmx2g -DDmax=16 -Dseuil=0.2 -Dcat=P139.cote1.taches -cp "$OLDPWD/code/certifiant/classes" \
   Rang88CertZ taches java_P139/cote1 1057 200 12 6 6 && cmp P139.cote1.taches "$OLDPWD/data/P139/cote1.taches")

# (f) quelques tâches isolées, rejouées dans un fichier de reçus neuf : leurs reçus sont identiques à ceux publiés
echo "15730 29320 4426 7055 14107 32661" > "$T/cat/liste.txt"
(cd "$T/cat" && java -Xmx2g -DDmax=16 -Dseuil=0.2 -Dckpt=essai.ckpt -Dliste=liste.txt -cp "$OLDPWD/code/certifiant/classes" \
   Rang88CertZ run java_P139/cote1 1057 200 12 6 6)
#     puis comparer chaque ligne de $T/cat/essai.ckpt à la ligne de même indice de data/P139/replication/cote1.ckpt
```

## 5. Long : refaire un balayage certifiant (plusieurs heures par côté ; non fait pour ce dépôt)

```sh
sh code/certifiant/rejouer_cote.sh P139 1 /un/repertoire/neuf 8      # puis P139 2, P599 1, P599 2
python -I code/verification/empreinte_canonique.py /un/repertoire/neuf/cote1.ckpt
```

Le lanceur copie les quatre fichiers d'entrée dans `<répertoire>/java_<C>/` et exécute, depuis ce répertoire, exactement l'invocation des exécutions publiées :

```
java -Xmx2g -DstopTouche=1 -Dveille=600 -DDmax=16 -Dseuil=0.2 -Dckpt=coteN.ckpt -Dcat=coteN.taches \
     -cp <dépôt>/code/certifiant/classes Rang88CertZ run java_<C>/coteN 1057 200 12 <fils> 6
```

Il refuse un répertoire qui contient déjà `coteN.ckpt` : **un fichier de reçus existant serait relu et les tâches correspondantes ne seraient pas rejouées** (réserve Z10). Il n'efface rien. Le nombre de fils ne change pas les reçus ; une réplication doit redonner, à l'octet près, l'empreinte canonique publiée : P₁₃₉ `c99dcf87db02e6b51f448cdb3e51da1f8b0ee4bd782b6b0e78d686bed5575122` (côté 1), `8ab1f40a48c416dd4eab8dde92d0c5866a6ca1951b5edd5d579c5f2ee0bedaf7` (côté 2) ; P₅₉₉ `f3cf379ad157b1595f9ad96c38d3734a920ea24de3afc5d12dfa617bb3e42689` (côté 1), `b9c93a83d2b370fad5de5b3d0edc317718ebe4900960642ef98f72c219458ef6` (côté 2). Elle doit aussi se terminer avec le code 0, la ligne `COUVERTURE_COMPLETE`, et sans fichier `coteN.ckpt.touches`.

Durées des exécutions publiées :

| Exécution | P₁₃₉ côté 1 | P₁₃₉ côté 2 | P₅₉₉ côté 1 | P₅₉₉ côté 2 |
|---|---|---|---|---|
| tâches | 48 227 | 61 174 | 59 255 | 74 398 |
| premier ordinateur (Windows, OpenJDK 11.0.16.1) | 14 562 s, 6 fils | 15 856 s, 6 fils | deux lancements : 6 fils, arrêt forcé après environ 20 350 s ; puis 19 765 s, 10 fils | 34 114 s, 10 fils |
| second ordinateur (Linux, OpenJDK 21.0.12.1), **référence** | 12 539 s, 8 fils | 13 648 s, 8 fils | 26 212 s, 14 fils | 25 956 s, 14 fils |

`COMPTE_U` imprimé : 42 957 972 (P₁₃₉, deux côtés), 185 794 630 (P₅₉₉, deux côtés). Mémoire : `-Xmx2g` (1,5 Go sur le second ordinateur pour P₁₃₉).

## 6. Lignes de bilan des journaux non inclus

Le journal du **rejeu complet des 21 459 tâches reprises** de P₅₉₉ côté 1 (premier ordinateur, OpenJDK 11.0.16.1, 10 fils ; option `-Dliste` avec `data/P599/rejeu_reprises/liste_taches_reprises.txt`, fichier de reçus neuf) n'est pas inclus, parce qu'il imprime des chemins propres au poste de travail. Ses lignes de bilan, recopiées telles quelles (chemins remplacés par `<chemin>`) :

```
CATALOGUE_SHA256 b9ff8375cdbb906a78daf01c07ae523b76165fa73ff34a3fcadba3b0ce130155 ; TOTAL_TACHES 59255
CHECKPOINT nouveau : <chemin>
SELECTION 21459/59255 ; A_FAIRE 21459 ; DEJA_AU_CHECKPOINT 0
CHECKPOINT_SHA256 ba14ba4fb3ed7e321d5e111fd125ec3ade6e9c033791ee6d2c1b191b30890cc9 ; <chemin>
EXECUTEES_CE_LANCEMENT 21459 ; REPRISES_DU_CHECKPOINT 0
TACHES_TERMINEES 21459/59255
COMPTE_U (au signe pres, energie courte <= 1057/200) 77265913 ; histogramme …
NOEUDS court 65513228269 ; fibre 1327406509299 ; CVP 77265913
TOTAL_TOUCHES 0
COUVERTURE_PARTIELLE 21459/59255 : AUCUNE CONCLUSION GLOBALE
FIN [14564 s]
```

La couverture est partielle par construction (seules les tâches reprises sont rejouées). Le fichier de reçus de ce rejeu est inclus (`data/P599/rejeu_reprises/rejeu_cote1.ckpt`, SHA-256 `ba14ba4f…0cc9`, égal à la ligne `CHECKPOINT_SHA256` ci-dessus) et comparé exactement par `verifier_recus.py P599` (contrôles R8).

Les journaux des quatre exécutions de référence et des exécutions du premier ordinateur sont inclus (`data/P*/replication/*.stdout.log`, `data/P*/premiere_execution/*.log`) ; leurs lignes `SELECTION`, `EXECUTEES_CE_LANCEMENT`, `TOTAL_TOUCHES`, `COUVERTURE_COMPLETE` et `CATALOGUE` sont contrôlées par `verifier_recus.py` et citées dans `verification/RESULTATS.md`. Les scripts qui ont enchaîné les lancements sur chaque ordinateur et les relevés d'environnement du second ordinateur ne sont pas inclus.
