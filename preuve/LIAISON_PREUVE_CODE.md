# Liaison entre la preuve de non-omission et le code

Ce document relie chaque étape de `PREUVE_NON_OMISSION.md` aux lignes du source `code/certifiant/Rang88CertZ.java` (SHA-256 `9e467c750470301ec0612c087b84636da6b46538a0fe33458970af6cb97bc3c5`, 521 lignes), puis chaque prémisse du corollaire 5.2 de la note au contrôle qui la vérifie sur les exécutions publiées. Les numéros de ligne sont ceux de ce fichier ; le source n'a pas été modifié pour ce dépôt (son en-tête, lignes 12 à 33, est d'origine).

## 1. Lemmes et lignes du source

| Lemme | Lignes | Élément du source | Ce qu'il faut y lire |
|---|---|---|---|
| L1 | 104–153 | `FormeZ(long[][] G)` | pivots exacts d_i (114–118), refus d'un pivot ≤ 0 (117), q_ij exacts (121–124), contrôle final exact de G_ij = Σ d_k q_ki q_kj (134–138) |
| L2 | 58–70 | `cmpDoubleRat`, `encadre` | les boucles ne s'arrêtent que sur une comparaison exacte en `BigDecimal` ; `dL[i] = encadre(...)[0]` (119), refus de dL ≤ 0 (120) |
| L3 | 72–83 | `dn`, `up` | voisin par motif binaire pour x > 0 fini, refus des valeurs non finies |
| Z1 | 125–130 | `qI[i][j]` dans `FormeZ` | plancher exact de 2ᶠ q_ij, contrôlé par `fl·den ≤ num < (fl+1)·den` (129) |
| Z2 | 170–195, 225–230 | `absW`, `cS`, `top`, `raz` (182), `fixe` (183), `descend` (185–190), `verifie` (191–195) ; mise à jour de `top[i-1]` (228) | invariant (K) ; recalcul exact optionnel par `-Dverif=1` (201) |
| Z3 | 313 ; 258–260 | `bornAU = encadre(DA·BAnum, BAden)[1]` ; `N` exact et `eB.borneU = up(up((double) N) / DA_D)` | majorants des budgets court et fibre |
| Z4 | 84–93 ; 202–212 | `plancherDiv` ; `reste`, `r`, `rs`, `H`, `C`, `yhi`, `ylo` | plage entière ; refus `rs ≥ 2⁶²` (206) |
| Z5 | 202–203 ; 217–222 | `reste < 0` ; `delta`, `dd`, `PL2`, `garde` | minorant certifié et coupe sûre |
| Z6 | 211 ; 248 | `signe && zeroDessus` ; `la <= 0` | normalisation de signe, exclusion de u = 0 |
| Z7 | 199 ; 315–323 ; 290–299 | branche `gen` de `rec` ; `catalogue` ; `Travail.executer` | émission des tâches ; exception si une feuille est atteinte pendant la génération (319) ; réinstallation du préfixe |
| Z8 | 244–266 ; 267–288 | `feuilleA` ; `feuilleB` | tests exacts de 𝒰 (248–249) ; recalcul de w en `BigInteger` et test exact de 𝒯 (270–281) ; comptage et écriture de la touche (282–287) |
| Z9 | 362–366 ; méthodes `…Exact` | `main` : toute exception donne le code 2 | refus de domaine : 42, 206, 216, 307 |
| Z10 | 332–360 ; 395–399 ; 419–449 ; 458–498 ; 500–519 | `ecrireCkpt`, `ecrireTouche`, `ligneResultat`, `lireResultat` ; lien entrées/classes ; relecture ; exécution ; bilan | voir § 2 |

## 2. Le corollaire 5.2 (absence de touche) dans le code

| Étape de la preuve (`PREUVE_NON_OMISSION.md`, § 5 bis) | Lignes | Code |
|---|---|---|
| Fichier de reprise neuf : aucun reçu relu | 423–447 | si le fichier n'existe pas ou est vide, branche `else` : création, écriture de l'en-tête, impression de « CHECKPOINT nouveau » (446) ; `repris` reste à 0 |
| Fichier de touche voisin du fichier de reprise | 448 | `touchesFichier = ckpt + ".touches"` |
| Toute feuille admissible écrit une touche, sans condition sur un compteur | 281–287, 338–344 | après le test exact (281), `C.touches++` puis, hors récepteur de test, `ecrireTouche(txt)` : ouverture en `CREATE, WRITE, APPEND`, écriture, `force` ; une `IOException` devient `UncheckedIOException` |
| Pas de récepteur de test en exécution normale | 157–158, 284 | `recepteur` vaut `null` sauf dans le harnais `TestCertZ` |
| Une exception d'une tâche remonte au code de sortie 2 | 465–476, 489–493, 362–366 | chaque tâche est un `Future` ; `fs.get(i).get()` relance l'exception ; `main` la capte et rend 2 |
| Le reçu n'est écrit qu'après l'exécution complète de la tâche | 471–472, 334–337 | `executer` puis `ecrireCkpt(ligneResultat(t, c))`, écrit et forcé sur disque |
| `COUVERTURE_COMPLETE` seulement si toutes les tâches ont un résultat | 500–517 | `couvertes == nt` ; avec un fichier neuf, ces résultats viennent tous de ce lancement (`res[t]` rempli en 490–492) |
| Arrêt sur touche (`-DstopTouche=1`) sans fausse conclusion | 469, 474, 491, 497 | une tâche sautée n'a pas de résultat : la couverture devient partielle |

## 3. Les prémisses, vérifiées sur les exécutions publiées

Pour chacune des quatre exécutions de référence (second ordinateur ; P₁₃₉ et P₅₉₉, côtés 1 et 2), `code/verification/verifier_recus.py` contrôle :

| Prémisse | Contrôle |
|---|---|
| mode `run`, paramètres BA = 1057/200, S = 12, F = 40, D = 6, Dmax = 16, seuil = 0,2 | R3 (ligne d'en-tête du journal) et R4 (en-tête du fichier de reçus) |
| classes et entrées : celles du dépôt | R1 (empreintes des sept classes imprimées par l'exécution = fichiers de `code/certifiant/classes/`), R2 (quatre fichiers d'entrée), LIEN recalculé |
| fichier de reprise neuf, aucune reprise | R3 : « CHECKPOINT nouveau », `SELECTION nt/nt ; A_FAIRE nt ; DEJA_AU_CHECKPOINT 0`, `EXECUTEES_CE_LANCEMENT nt ; REPRISES_DU_CHECKPOINT 0`, aucune ligne `REPRISE` |
| code de sortie 0, `COUVERTURE_COMPLETE`, aucune erreur | R3 : `cote*.java.exit` = 0 ; une ligne `COUVERTURE_COMPLETE nt/nt` ; `FIN` ; aucune ligne `ERREUR`, `TOUCHE`, `ARRET` ; stderr sans exception |
| aucun fichier de touche | R7 : inventaire complet du répertoire de sortie, relevé après la fin du calcul (`data/<C>/replication/INVENTAIRE_SORTIE.txt`) |
| les reçus sont ceux de cette exécution | R4 : SHA du fichier = `CHECKPOINT_SHA256` imprimé ; nt lignes au format, indices = permutation de 0..nt−1 ; sommes = totaux du journal |
| reçus identiques entre les deux ordinateurs | R6 : empreinte canonique égale aux valeurs publiées, pour les deux exécutions de chaque côté |

Ces contrôles portent sur les fichiers ; ils supposent H3 (les journaux sont la sortie authentique des exécutions). Le raccord entre les fichiers d'entrée et le réseau est contrôlé à part (`verifier_raccord.py`), et le critère (note, th. 4.6) fait le reste de la composition (note, th. 6.11).
