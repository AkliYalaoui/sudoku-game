# Projet Sudoku des Couleurs

Le **Sudoku des Couleurs** est une variation du traditionnel jeu de Sudoku où les chiffres sont remplacés par des couleurs. Ce projet permet à l'utilisateur de résoudre des puzzles de Sudoku colorés en utilisant différentes stratégies d'algorithmes de génération de grilles. L'utilisateur peut choisir parmi plusieurs algorithmes et interagir avec le puzzle pour colorier les cases.

## Fonctionnalités principales

- **Sélection de la taille de la grille** : Vous pouvez choisir entre trois tailles de grille (4x4, 9x9, 16x16) en fonction de la "rank" (2, 3 ou 4).
- **Algorithmes de génération** : Le Sudoku est généré selon plusieurs algorithmes, notamment :
  - **Backtracking** : Algorithme de retour sur trace.
  - **MRV (Minimum Remaining Values)** : Une heuristique pour les problèmes de satisfaction de contraintes.
  - **DSATUR (Degree of Saturation)** : Utilise le degré de saturation pour la génération de la grille.
  - **Knuth (DLX)** : Utilise l'algorithme de Knuth pour la génération de la grille.
- **Interaction avec la grille** : L'utilisateur peut sélectionner une couleur et cliquer sur une case vide pour la colorier.
- **Vérification de la solution** : Après avoir rempli la grille, l'utilisateur peut vérifier si la solution respecte les règles du Sudoku des couleurs.
- **Affichage de la solution** : L'utilisateur peut afficher la solution complète du puzzle généré.
- **Recommencement de la partie** : L'utilisateur peut recommencer une nouvelle partie avec un puzzle généré aléatoirement.

## Technologies utilisées

- **Streamlit** : Utilisé pour créer l'interface interactive du Sudoku des couleurs.
- **Python** : Langage de programmation pour la logique du jeu et la génération des grilles.
- **Pandas** : Utilisé pour manipuler et organiser les résultats de performance.
- **Matplotlib et Seaborn** : Utilisés pour afficher des graphiques de comparaison des performances des différents algorithmes.
  
## Exécutez 
Assurez-vous que vous avez Streamlit, Pandas, Matplotlib, et Seaborn installés dans votre environnement.

```bash
streamlit run app.py

