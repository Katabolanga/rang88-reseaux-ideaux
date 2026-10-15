# Fichier externe : la matrice de Gram de L₀ (R. Sakamoto)

Deux vérifications (`code/verification/verifier_H_L0.py`, `code/verification/verifier_conformite_article.py`) lisent la matrice de Gram du réseau L₀ publiée par R. Sakamoto. **Ce fichier n'est pas redistribué ici.** Pour rejouer ces deux vérifications :

1. Télécharger soi-même le fichier `data/L0/integer_input.txt` du dépôt public
   <https://github.com/RyotaroSakamoto0113/rank-88-extremal-lattice-computations>, **révision `628ce2a7`** (`628ce2a7ac23acf8d4c295677e4310c9ec5b21d9`), par exemple :
   `https://raw.githubusercontent.com/RyotaroSakamoto0113/rank-88-extremal-lattice-computations/628ce2a7ac23acf8d4c295677e4310c9ec5b21d9/data/L0/integer_input.txt`
2. Le placer ici, sous le nom `externe/integer_input.txt`.
3. Contrôler son empreinte : SHA-256 attendu
   `68af477caf3f6d6a8980c40f234bcb47c0bac6caf3582c1757280cb64457631f` (51 284 octets).

Les deux scripts recalculent cette empreinte **avant toute lecture du contenu** et s'arrêtent si elle diffère. Le fichier est ensuite lu comme du texte : seuls des entiers sont acceptés (« 88 », puis trois matrices 88 × 88 : la Gram G de L₀, puis deux matrices M5 et M23), et rien n'est exécuté. Aucun code du dépôt de Sakamoto n'est utilisé.

Le fichier `externe/integer_input.txt` est exclu du suivi de version (`.gitignore`) et de `SHA256SUMS.txt`.
