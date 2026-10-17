# Balayages certifiés de X₄₉₆₉ et X₄₀₄₉ (15 et 16 octobre 2026)

Addendum, théorème A et § 2.2 (tableau des balayages). Programme : `Rang88CertZ`, avec les classes compilées de `code/certifiant/classes/` de la note. Paramètres : B_A = 1057/200, S = 12.

## Conditions d'exécution

- Machines louées Scaleway POP2-HC-32C-64G, 32 cœurs virtuels, Ubuntu 24.04.
- Chaque côté du critère a été balayé **deux fois, sur deux machines différentes**. Pour X₄₉₆₉, la seconde exécution a tourné sous une autre version de la machine virtuelle Java.
- Chaque exécution :
  - est un lancement unique, avec un point de contrôle neuf et aucune reprise ;
  - rend le code de sortie 0, avec un flux d'erreur vide ;
  - a une couverture complète, sans aucune touche.
- Les reçus des deux exécutions d'un même côté ont la **même empreinte canonique** : SHA-256 des reçus triés par indice, chacun suivi d'un saut de ligne.

## Les exécutions

| Réseau | Côté | Dossier | Tâches | Catalogue (SHA-256, début) | Empreinte canonique des reçus | Contrôles rejoués |
|---|---|---|---|---|---|---|
| X₄₉₆₉ | 1 | `final_P4969_cote1_AMS3` | 97 270 | `6ff951520f324d20…` | `0226b9a51c01ceab49e90822d2b433550e601921e77ded187056bf130f58caf6` | 27/27 |
| X₄₉₆₉ | 1 | `final_P4969_cote1_WAW1_replication` | 97 270 | `6ff951520f324d20…` | `0226b9a51c01ceab49e90822d2b433550e601921e77ded187056bf130f58caf6` | 27/27 |
| X₄₉₆₉ | 2 | `final_P4969_cote2_AMS2` | 140 082 | `94ff3cfa1bcf5f7a…` | `f6a1aecde0370db843c86bb33ccd2eb9cc6688811c93488810f7cf443139e736` | 27/27 |
| X₄₉₆₉ | 2 | `final_P4969_cote2_AMS3_replication` | 140 082 | `94ff3cfa1bcf5f7a…` | `f6a1aecde0370db843c86bb33ccd2eb9cc6688811c93488810f7cf443139e736` | 27/27 |
| X₄₀₄₉ | 1 | `final_P4049_cote1_MIL1` | 77 819 | `370bf006fd701b7c…` | `6334d93e44b7712e1eee274e1b8cfa27f5842c96dc983fe6db695e2e65207455` | 27/27 |
| X₄₀₄₉ | 1 | `final_P4049_cote1_AMS2` | 77 819 | `370bf006fd701b7c…` | `6334d93e44b7712e1eee274e1b8cfa27f5842c96dc983fe6db695e2e65207455` | 27/27 |
| X₄₀₄₉ | 2 | `final_P4049_cote2_MIL1` | 87 731 | `d9dd8b1bb754277e…` | `f95f16b86fd0af5c636fbb9d1516e759caf758a01a7dd98d512545c5b2fda940` | 27/27 |
| X₄₀₄₉ | 2 | `final_P4049_cote2_AMS2_replication` | 87 731 | `d9dd8b1bb754277e…` | `f95f16b86fd0af5c636fbb9d1516e759caf758a01a7dd98d512545c5b2fda940` | 27/27 |
| X_{P₄₆₁σ₂₄(P₄₆₁)} ≅ X₁₃₉ | 1 | `final_P461s24_AMS3` | 73 244 | `0189bac379e039fb…` | `11188cb782be415e2a15cfc598b04f1f9d9cac0eef0917260ceb284c4a658108` | 27/27 |
| X_{P₄₆₁σ₂₄(P₄₆₁)} ≅ X₁₃₉ | 2 | `final_P461s24_AMS3` | 73 359 | `388a5734bb6ce7e5…` | `b2682b9db29c6b66a0fac838791397dd73d7809b0e131006ef607e36708ad222` | 27/27 |

Les deux côtés d'un même réseau donnent le même nombre total de vecteurs courts |U| :
- 1 544 898 536 pour X₄₉₆₉ ;
- 1 257 946 084 pour X₄₀₄₉ ;
- 143 529 602 pour X_{P₄₆₁σ₂₄(P₄₆₁)}.

La dernière ligne du tableau est le contre-audit de dépendance aux coordonnées (addendum, § 3). L'idéal P₄₆₁σ₂₄(P₄₆₁), avec P₄₆₁ = (461, ζ − 5), est dans l'orbite de P₁₃₉ ; son réseau est donc isométrique à X₁₃₉.

## Rejouer un contrôle

```
tar xzf final_P4969_cote1_AMS3/run_P4969_cote1_AMS3.tar.gz
python3 -I controle_execution.py run_P4969_cote1 1 97270 <SHA-256 complet du catalogue>
```

- Le SHA-256 complet du catalogue est la ligne `CATALOGUE_SHA256` du journal `run_*/cote*.stdout.log` de l'archive.
- Le contrôleur le recalcule sur le fichier `.taches` et le compare aux reçus.
- Sortie attendue : `BILAN : 27 controles, 0 echecs`, puis `CONTROLE_OK`.
- Les contrôles E1 à E6 sont décrits en tête de `controle_execution.py`.

Ces 10 contrôles ont été rejoués sur les archives publiées le 17 octobre 2026, après décompression dans un dossier neuf : 27 contrôles et aucun échec pour chacun.

## Contenu de chaque dossier

- `run_*.tar.gz` : l'exécution complète. On y trouve les journaux stdout et stderr, le code de sortie, les reçus (`cote*.ckpt`), le catalogue (`cote*.taches`), le journal de chaînage et l'autotest de la machine.
- `CONTROLE_EXECUTION*.txt` : le contrôle fait au rapatriement. Le contrôle E7, facultatif, y compare les reçus à des exécutions partielles de deux postes de l'auteur, qui ne sont pas publiées ; il ne sert pas au théorème.
- `SHA256SUMS*.txt` : empreintes au rapatriement.
- Journaux de lancement, de surveillance et d'extinction des machines.

`journal_avancement.txt` contient les relevés d'avancement pris pendant les calculs.
