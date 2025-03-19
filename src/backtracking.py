import random
from typing import List, Optional
from .interface import ISudoku

class BacktrackingGenerator(ISudoku):
    """
    Générateur de grilles de Sudoku basé sur l'algorithme de backtracking.

    Cette classe génère une grille de Sudoku en remplissant les cases avec des couleurs 
    en respectant les règles de non-répétition dans les lignes, colonnes et sous-grilles.

    Attributs :
        size (int) : Taille de la grille (par défaut 9x9).
        colors (List[str]) : Liste des couleurs utilisées pour remplir la grille.
    """

    def __init__(self, size: int = 9, colors: Optional[List[str]] = None) -> None:
        """
        Initialise le générateur de Sudoku avec une taille et une liste de couleurs.

        Args :
            size (int) : Taille de la grille (doit être un carré parfait, ex: 9 pour un Sudoku standard).
            colors (Optional[List[str]]) : Liste des couleurs disponibles pour le remplissage. 
                                           Si None, une liste par défaut est utilisée.
        """
        self.size = size
        self.colors = colors if colors else [
            "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "cyan"
        ]

    def generate_sudoku(self) -> List[List[Optional[str]]]:
        """
        Génère une grille de Sudoku en utilisant un algorithme de backtracking.

        Retourne :
            List[List[Optional[str]]] : Une grille de Sudoku où chaque case contient une couleur 
                                        ou None si elle est vide.
        """
        # Initialisation d'une grille vide (remplie de None)
        grid: List[List[Optional[str]]] = [[None for _ in range(self.size)] for _ in range(self.size)]

        def is_valid(row: int, col: int, color: str, grid: List[List[Optional[str]]]) -> bool:
            """
            Vérifie si une couleur peut être placée à la position (row, col) en respectant les règles du Sudoku.

            Args :
                row (int) : Indice de la ligne.
                col (int) : Indice de la colonne.
                color (str) : Couleur à placer.
                grid (List[List[Optional[str]]]) : Grille actuelle du Sudoku.

            Retourne :
                bool : True si la couleur peut être placée, sinon False.
            """
            # Vérification de la ligne et de la colonne
            for i in range(self.size):
                if grid[row][i] == color or grid[i][col] == color:
                    return False

            # Vérification du sous-groupe (bloc)
            box_size = int(self.size ** 0.5)  # Taille du bloc
            box_row, box_col = (row // box_size) * box_size, (col // box_size) * box_size
            
            for i in range(box_size):
                for j in range(box_size):
                    if grid[box_row + i][box_col + j] == color:
                        return False
            
            return True

        def solve(row: int = 0, col: int = 0) -> bool:
            """
            Remplit la grille en utilisant un algorithme de backtracking.

            Args :
                row (int) : Indice de la ligne actuelle.
                col (int) : Indice de la colonne actuelle.

            Retourne :
                bool : True si la grille est remplie avec succès, sinon False.
            """
            if row == self.size:  # Si on a atteint la fin de la grille, le Sudoku est valide
                return True

            if col == self.size:  # Passer à la ligne suivante si on atteint la fin d'une ligne
                return solve(row + 1, 0)

            random.shuffle(self.colors)  # Mélanger les couleurs pour varier les solutions

            for color in self.colors:
                if is_valid(row, col, color, grid):  # Vérifier si la couleur est valide
                    grid[row][col] = color  # Placer la couleur
                    
                    if solve(row, col + 1):  # Passer à la prochaine case
                        return True
                    
                    grid[row][col] = None  # Annuler le placement en cas d'impasse (backtracking)

            return False  # Aucune solution trouvée pour cette case

        solve()  # Démarrer la résolution
        return grid  # Retourner la grille remplie
