import random
from typing import List, Optional, Tuple
from .interface import ISudoku

class DSATURGenerator(ISudoku):
    """
    Générateur de grilles de Sudoku basé sur l'algorithme DSATUR (Degree of Saturation).

    Cette classe génère une grille de Sudoku en remplissant les cases avec des couleurs, 
    en utilisant la stratégie DSATUR, qui choisit la case la plus saturée (ayant le plus de couleurs 
    déjà utilisées dans ses voisins) pour affecter une couleur.

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
        Génère une grille de Sudoku en utilisant l'algorithme DSATUR.

        Retourne :
            List[List[Optional[str]]] : Une grille de Sudoku où chaque case contient une couleur 
                                        ou None si elle est vide. Si la génération échoue, retourne None.
        """
        # Initialisation d'une grille vide (remplie de None)
        grid: List[List[Optional[str]]] = [[None for _ in range(self.size)] for _ in range(self.size)]

        def get_neighbors(row: int, col: int) -> set:
            """
            Récupère tous les voisins (lignes, colonnes et sous-grille) d'une cellule donnée.

            Args :
                row (int) : Indice de la ligne de la cellule.
                col (int) : Indice de la colonne de la cellule.

            Retourne :
                set : Ensemble des voisins sous forme de tuples (r, c), où r et c sont les indices des voisins.
            """
            neighbors = set()
            # Ajoute tous les voisins de la même ligne et colonne
            for i in range(self.size):
                neighbors.add((row, i))
                neighbors.add((i, col))
            
            # Ajoute les voisins dans la sous-grille
            box_size = int(self.size ** 0.5)
            box_row, box_col = (row // box_size) * box_size, (col // box_size) * box_size
            for i in range(box_size):
                for j in range(box_size):
                    neighbors.add((box_row + i, box_col + j))
            
            # Supprime la cellule elle-même des voisins
            neighbors.discard((row, col))
            return neighbors
        
        def get_saturation(cell: Tuple[int, int]) -> int:
            """
            Calcule la saturation d'une cellule (nombre de couleurs déjà utilisées dans ses voisins).

            Args :
                cell (Tuple[int, int]) : Cellule sous forme de tuple (row, col).

            Retourne :
                int : Nombre de couleurs déjà utilisées dans les voisins de la cellule.
            """
            row, col = cell
            # Récupère les couleurs utilisées dans les voisins
            used_colors = set(grid[r][c] for r, c in get_neighbors(row, col) if grid[r][c] is not None)
            return len(used_colors)

        def get_most_saturated_cell() -> Optional[Tuple[int, int]]:
            """
            Récupère la cellule la plus saturée (ayant le plus grand nombre de couleurs dans ses voisins).

            Retourne :
                Optional[Tuple[int, int]] : La cellule la plus saturée sous forme de tuple (row, col).
                                             Retourne None si toutes les cellules sont remplies.
            """
            # Liste des cellules non assignées (qui sont encore vides)
            unassigned_cells = [(r, c) for r in range(self.size) for c in range(self.size) if grid[r][c] is None]
            # Retourne la cellule la plus saturée
            return max(unassigned_cells, key=get_saturation) if unassigned_cells else None

        def assign_color(row: int, col: int) -> Optional[str]:
            """
            Assigne une couleur valide à la cellule (row, col), en évitant les couleurs déjà utilisées par ses voisins.

            Args :
                row (int) : Indice de la ligne.
                col (int) : Indice de la colonne.

            Retourne :
                Optional[str] : La couleur assignée à la cellule, ou None si aucune couleur n'est disponible.
            """
            # Récupère les couleurs déjà utilisées dans les voisins
            used_colors = set(grid[r][c] for r, c in get_neighbors(row, col) if grid[r][c] is not None)
            # Liste des couleurs disponibles (non utilisées par les voisins)
            available_colors = [color for color in self.colors if color not in used_colors]
            return available_colors[0] if available_colors else None

        # Boucle jusqu'à ce qu'il n'y ait plus de cellules non assignées
        while (cell := get_most_saturated_cell()) is not None:
            row, col = cell
            # Assigne une couleur à la cellule la plus saturée
            grid[row][col] = assign_color(row, col)
            if grid[row][col] is None:
                return None  # Échec si aucune couleur n'est disponible pour cette cellule
        
        return grid  # Retourne la grille remplie
