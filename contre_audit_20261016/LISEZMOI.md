# Contre-audit du 16 octobre 2026 (addendum, § 3)

Ce dossier est l'attaque délibérée de la chaîne certifiante, menée le 16 octobre 2026. Il contient les bilans et les scripts.

| Pièce | Contenu |
|---|---|
| `C1_C4_BILAN.md` | bilan d'ensemble des quatre attaques |
| `C1_controle_generique.sh`, `C1_GROUPE_TEMOIN_RESULTATS.txt` | C1 : le contrôle générique et le groupe témoin |
| `C2_MUTATIONS_BILAN.md`, `RESULTATS_MUTATIONS.txt` | C2 : huit mutations de la source, chacune d'une seule substitution, passées contre trois tests |
| `C3_BILAN.md` | C3 : prédiction des touches à partir de témoins connus de norme 6 et de leurs rotations, par un script GP qui ne lit aucune sortie du programme ; puis rejeu des seules tâches concernées |
| `C4_compte_U_P139_qfminim.gp/.log`, `C4b_compte_U_P139_complet*.gp/.log`, `C4b_enveloppe_execution.txt` | C4 : comptes indépendants de vecteurs courts sur X₁₃₉ |

## Pièces à venir

Ces pièces ne sont pas dans les versions 1.1 et 1.2 du dépôt : elles sont trop lourdes en l'état, surtout à cause des catalogues de tâches régénérables, et une partie de leurs fichiers contient des chemins absolus du poste de l'auteur. Elles sont prévues pour une version ultérieure (1.3), allégées.
- `mut/`, environ 100 Mo : les sources des huit mutants et leurs exécutions.
- `C3/`, environ 164 Mo : les exécutions de prédiction et de rejeu.

## Chemins absolus

Quatre scripts contiennent, sur une seule ligne d'affectation, un chemin absolu du poste de l'auteur :
- `C1_controle_generique.sh`, ligne 11 (`FBNFP=…`) ;
- `C4_compte_U_P139_qfminim.gp`, ligne 8 ;
- `C4b_compte_U_P139_complet.gp`, ligne 8 ;
- `C4b_compte_U_P139_complet_v2.gp`, ligne 11.

Ces scripts sont publiés à l'identique des versions exécutées. Avant de les relancer, remplacer ce chemin par celui du fichier correspondant de ce dépôt.
