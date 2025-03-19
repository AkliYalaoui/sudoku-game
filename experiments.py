import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.core  import ColorSudoku

# Paramètres à utiliser dans les tests
sudoku_sizes = [4, 9, 16]  # Liste des tailles de Sudoku pour les tests (4x4, 9x9, 16x16).
algorithms = ["Backtracking", "MRV", "Dsatur", "Knuth"]  # Liste des algorithmes à tester pour la génération de Sudoku.
num_trials = 10  # Nombre d'itérations pour chaque combinaison d'algorithme et de taille de grille.

# Liste pour stocker les résultats des tests
results = []  # Cette liste contiendra les résultats de chaque essai pour chaque taille et chaque algorithme.

# Boucle pour itérer sur chaque taille de grille et chaque algorithme.
for size in sudoku_sizes:  # Itération sur les tailles des grilles (4x4, 9x9, 16x16)
    for algo in algorithms:  # Itération sur les différents algorithmes
        total_time = 0  # Variable pour stocker le temps total pris pour générer les grilles.
        valid_grids = 0  # Variable pour stocker le nombre de grilles générées valides.

        # Effectuer plusieurs essais (num_trials) pour chaque combinaison taille x algorithme.
        for _ in range(num_trials):  # Répéter l'expérience 'num_trials' fois pour chaque combinaison
            start_time = time.time()  # Enregistrement du temps de début avant l'exécution de l'algorithme.
            
            # Création d'un objet ColorSudoku avec la taille et l'algorithme spécifiés
            sudoku = ColorSudoku(size=size, algorithm=algo, test=True)  # Génère la grille de Sudoku avec l'algorithme et la taille donnés.
            
            end_time = time.time()  # Enregistrement du temps de fin après l'exécution de l'algorithme.

            # Vérification si la grille générée est valide (l'algorithme est supposé générer une solution correcte)
            is_valid = sudoku.is_valid_solution()  # Vérifie si la grille générée respecte les règles du Sudoku.

            # Ajout du temps écoulé pour cet essai et du résultat de validité de la grille.
            total_time += (end_time - start_time)  # Ajout du temps pris pour cet essai.
            valid_grids += int(is_valid)  # Si la grille est valide (is_valid=True), on ajoute 1 à valid_grids.

        # Calcul du temps moyen et du taux de validité sur les itérations
        avg_time = total_time / num_trials  # Calcul du temps moyen d'exécution pour cet algorithme et cette taille.
        validity_rate = (valid_grids / num_trials) * 100  # Calcul du taux de validité (en pourcentage).

        # Stockage des résultats dans la liste 'results'
        results.append({
            "Taille": size,  # La taille de la grille (4, 9 ou 16).
            "Algorithme": algo,  # L'algorithme utilisé ("Backtracking", "MRV", "Dsatur", "Knuth").
            "Temps moyen (s)": avg_time,  # Le temps moyen d'exécution pour cette configuration (en secondes).
            "Validité (%)": validity_rate  # Le taux de validité des grilles générées.
        })

# Conversion des résultats en DataFrame Pandas pour faciliter la manipulation des données et la génération de graphiques.
df = pd.DataFrame(results)  # Crée un DataFrame Pandas à partir de la liste de résultats.

# Configuration de style des graphiques pour les rendre plus lisibles.
sns.set(style="whitegrid")  # Utilise le style "whitegrid" pour les graphiques (fond blanc avec une grille).

# Graphique : Temps moyen d'exécution pour chaque combinaison taille x algorithme
plt.figure(figsize=(10, 5))  # Définition de la taille de la figure (largeur=10, hauteur=5).
sns.barplot(x="Taille", y="Temps moyen (s)", hue="Algorithme", data=df, palette="coolwarm")  # Création d'un graphique en barres avec une palette de couleurs "coolwarm".
plt.title("Comparaison des temps d'exécution des algorithmes")  # Titre du graphique.
plt.ylabel("Temps moyen (s)")  # Légende de l'axe Y (temps en secondes).
plt.xlabel("Taille du Sudoku")  # Légende de l'axe X (taille de la grille).
plt.legend(title="Algorithme")  # Légende du graphique indiquant quel algorithme correspond à chaque couleur.
plt.show()  # Affiche le graphique.

# Graphique : Taux de validité des grilles générées pour chaque combinaison taille x algorithme
plt.figure(figsize=(10, 5))  # Définition de la taille de la figure (largeur=10, hauteur=5).
sns.barplot(x="Taille", y="Validité (%)", hue="Algorithme", data=df, palette="viridis")  # Création d'un graphique en barres avec une palette de couleurs "viridis".
plt.title("Comparaison du taux de validité des grilles")  # Titre du graphique.
plt.ylabel("Validité (%)")  # Légende de l'axe Y (taux de validité en pourcentage).
plt.xlabel("Taille du Sudoku")  # Légende de l'axe X (taille de la grille).
plt.legend(title="Algorithme")  # Légende du graphique indiquant quel algorithme correspond à chaque couleur.
plt.ylim(90, 100)  # Limite de l'axe Y (on suppose que tous les taux de validité sont proches de 100%).
plt.show()  # Affiche le graphique.