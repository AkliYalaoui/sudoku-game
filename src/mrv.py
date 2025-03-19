import random
from typing import List, Optional, Tuple
from .interface import ISudoku

class MRVGenerator(ISudoku):
    """
    Générateur de grilles de Sudoku basé sur l'algorithme MRV (Minimum Remaining Values).

    Cette classe génère une grille de Sudoku en remplissant les cases en suivant la stratégie MRV,
    qui consiste à remplir la cellule ayant le moins de valeurs possibles (en fonction des couleurs disponibles).
    
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
        Génère une grille de Sudoku en utilisant l'algorithme MRV (Minimum Remaining Values).

        Retourne :
            List[List[Optional[str]]] : Une grille de Sudoku où chaque case contient une couleur 
                                        ou None si elle est vide. Si la génération échoue, retourne None.
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

        def get_least_remaining_values_cell(grid: List[List[Optional[str]]]) -> Optional[Tuple[int, int]]:
            """
            Trouve la cellule avec le moins de valeurs possibles disponibles (stratégie MRV).

            Args :
                grid (List[List[Optional[str]]]) : Grille actuelle du Sudoku.

            Retourne :
                Optional[Tuple[int, int]] : La cellule avec le moins de valeurs possibles (ligne, colonne).
                                            Retourne None si toutes les cellules sont remplies.
            """
            min_values = float('inf')  # Initialiser le minimum des valeurs restantes
            best_cell = None  # Cellule avec le moins de valeurs possibles
            for row in range(self.size):
                for col in range(self.size):
                    if grid[row][col] is None:  # Si la cellule est vide
                        valid_colors = [color for color in self.colors if is_valid(row, col, color, grid)]
                        if len(valid_colors) < min_values:
                            min_values = len(valid_colors)
                            best_cell = (row, col)
            return best_cell

        def solve() -> bool:
            """
            Remplit la grille en utilisant un algorithme de backtracking avec MRV.

            Retourne :
                bool : True si la grille est remplie avec succès, sinon False.
            """
            # Trouve la cellule avec le moins de valeurs possibles (MRV)
            cell = get_least_remaining_values_cell(grid)
            if cell is None:  # Si toutes les cellules sont remplies
                return True
            
            row, col = cell
            random.shuffle(self.colors)  # Mélange les couleurs pour varier les solutions

            # Essayer chaque couleur valide pour cette cellule
            for color in self.colors:
                if is_valid(row, col, color, grid):
                    grid[row][col] = color  # Assigner la couleur
                    if solve():  # Appel récursif pour la prochaine cellule
                        return True
                    grid[row][col] = None  # Backtracking si aucune solution n'a été trouvée

            return False  # Si aucune couleur ne fonctionne, retour à l'état précédent

        solve()  # Démarrer la résolution
        return grid  # Retourne la grille remplie
