# Contre-audit, expérience C2 : mutations du programme certifiant (16 octobre 2026, 9 h 09 – 9 h 22)

*Claude. Sources : `mut/mutations.py` (génération), `mut/mutations.sh` (batterie), `mut/RESULTATS_MUTATIONS.txt`, journaux `mut/M*/t*.log`. Le source de référence `Rang88CertZ.java` (SHA-256 9e467c75…) n'est pas modifié ; chaque mutant est une copie avec une seule substitution exacte.*

**Batterie** :
- T1 : TestCertZ 1 300 (910 contrôles) ;
- T2 : validation P₄₆₁ (697 u, 2 touches, couverture 3658/3658) ;
- T3 : rejeu des 12 tâches de contrôle de P₄₉₆₉, côté 1, avec des reçus identiques à l'octet à ceux du poste d'Ivan.

| Mutant | Faute injectée | T1 | T2 | T3 | Verdict |
|---|---|---|---|---|---|
| M0 | aucune (témoin recompilé) | ok | ok | ok | passe (attendu) |
| M1 | test de feuille sans égalité (`> 0` → `>= 0`) | ÉCHEC | ÉCHEC (0 touche) | ok | **tué** |
| M2 | élagage dès que le budget restant vaut 0 | ok | ok | ok | survit |
| M3 | arrondi extérieur supprimé sur le budget restant | ok | ok | ok | survit |
| M4 | plage entière rétrécie d'une unité (2⁻⁴⁰ en virgule fixe) | ok | ok | ok | survit |
| M5 | arrondi extérieur supprimé sur le rayon | ok | ok | ok | survit |
| M6 | budget de fibre diminué d'un cran | ÉCHEC | ÉCHEC (0 touche) | ÉCHEC | **tué** |
| M7 | vecteur nul non exclu au dernier niveau | ok | ok | ok | survit, mais sans effet : le vecteur nul est exclu une seconde fois à la feuille (`if (la <= 0) return;`, ligne 248) |
| M8 | autre convention de signe (symétrie u ↦ −u) | ÉCHEC | ok | ÉCHEC | **tué**. Prévu « équivalent » : les tests contrôlent la convention exacte, pas seulement les comptes |

## Lecture

- **Les fautes qui feraient manquer des vecteurs dans les cas ordinaires sont détectées** : M1 et M6, qui perdent les deux touches de P₄₆₁ ; et M8, un changement de convention.
- **Les fautes de frontière exacte ou d'arrondi (M2 à M5) ne sont pas détectables par des tests finis de ce type.** Elles n'agissent que si une énergie tombe exactement sur un budget, ou à moins d'un ulp ou de 2⁻⁴⁰ près. **Sur ces points, la correction repose uniquement sur la preuve de non-omission** (lemmes Z3, Z4 et Z5, arrondi extérieur L3, modèle M1). C'est la cible prioritaire de l'audit d'Astra.
- **Renforcements possibles des tests.** Ils ne remplacent pas la preuve.
  - Formes et bornes **égales à des normes atteintes**, avec des coordonnées finales nulles, pour exercer l'égalité aux niveaux intermédiaires (M2).
  - Formes mal conditionnées et bornes placées sur des frontières de représentation des `double`, pour M3 et M5.
  - Contrôle croisé par un énumérateur entièrement exact sur des formes de dimension 8 à 16.
