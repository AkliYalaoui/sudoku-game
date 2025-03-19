import random
from typing import Optional, List
from .backtracking import BacktrackingGenerator
from .mrv import MRVGenerator
from .dsatur import DSATURGenerator
from .knuth import DLXSudokuGenerator


class ColorSudoku:
    """
    Classe représentant un générateur de Sudoku coloré. Elle permet de créer un Sudoku avec des couleurs 
    et de résoudre le puzzle en utilisant différents algorithmes de génération.
    
    Attributes:
        size (int): La taille du Sudoku (ex : 9 pour un Sudoku classique 9x9).
        rank (int): Le rang de la grille (calculé comme la racine carrée de la taille).
        colors (List[str]): Liste des couleurs utilisées dans le Sudoku.
        algorithm (str): L'algorithme utilisé pour générer la grille de Sudoku ("Backtracking", "MRV", "Dsatur", "Knuth").
        grid (List[List[Optional[str]]]): La grille actuelle du Sudoku avec les couleurs.
        solution (List[List[str]]): La solution complète du Sudoku (avant d'enlever des couleurs pour rendre le puzzle).
    
    Methods:
        __init__(self, size=9, algorithm="Backtracking", colors=None, test=False): Initialisation du générateur de Sudoku.
        generate_colors(self) -> List[str]: Génère une liste de couleurs pour le Sudoku.
        generate_sudoku(self) -> List[List[Optional[str]]]: Génère la grille du Sudoku selon l'algorithme sélectionné.
        remove_colors(self, remove_count: int): Retire un nombre spécifié de couleurs de la grille pour créer un puzzle.
        is_valid_solution(self) -> bool: Vérifie si la grille actuelle est une solution valide.
        is_valid_placement(self, row: int, col: int, color: str) -> bool: Vérifie si une couleur peut être placée dans une cellule donnée.
        set_user_color(self, row: int, col: int, color: str): Définit la couleur d'une cellule spécifiée par l'utilisateur.
        reveal_solution(self): Révèle la solution complète du Sudoku.
    """

    def __init__(self, size: int = 9, algorithm: str = "Backtracking", colors: Optional[List[str]] = None, test: bool = False):
        """
        Initialise un générateur de Sudoku coloré avec la taille spécifiée, l'algorithme de génération choisi,
        et une liste optionnelle de couleurs. Si `test` est False, des couleurs seront retirées pour créer un puzzle.
        
        Args:
            size (int): La taille du Sudoku (par défaut 9 pour une grille 9x9).
            algorithm (str): L'algorithme de génération du Sudoku (par défaut "Backtracking").
            colors (List[str], optionnel): Liste des couleurs à utiliser. Si None, une liste par défaut est générée.
            test (bool): Si True, ne supprime pas les couleurs de la grille (utilisé pour les tests).
        """
        self.size = size
        self.rank = int(size ** 0.5)  # Rang de la grille, c'est la racine carrée de la taille.
        self.colors = self.generate_colors()  # Génère les couleurs à utiliser pour le Sudoku.
        self.algorithm = algorithm  # Algorithme de génération de Sudoku sélectionné.
        self.grid = self.generate_sudoku()  # Génère la grille du Sudoku.
        self.solution = [row[:] for row in self.grid]  # Crée une copie de la grille générée pour la solution complète.
        if not test: 
            remove_count = int(.60 * size ** 2)  # Retirer 60% des cellules pour créer un puzzle.
            self.remove_colors(remove_count)

    def generate_colors(self) -> List[str]:
        """
        Génère une liste de couleurs basée sur la taille du Sudoku (rank). Par défaut, elle utilise une liste
        pré-définie de couleurs et limite la taille de cette liste en fonction du rang (ex. 3x3 ou 4x4).
        
        Returns:
            List[str]: Liste de couleurs.
        """
        base_colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "cyan", "lime", "teal", "magenta", "gold", "silver", "navy", "maroon"]
        return base_colors[:self.rank ** 2]  # Limite les couleurs à la taille de la grille (par exemple, 9 couleurs pour un Sudoku 9x9).

    def generate_sudoku(self) -> List[List[Optional[str]]]:
        """
        Génère la grille de Sudoku en fonction de l'algorithme choisi pour la génération (Backtracking, MRV, DSATUR, Knuth).
        
        Returns:
            List[List[Optional[str]]]: La grille de Sudoku générée avec les couleurs.
        """
        # Sélectionne et utilise l'algorithme de génération de Sudoku approprié
        if self.algorithm == "Backtracking":
            generator = BacktrackingGenerator(self.size, self.colors)
        elif self.algorithm == "MRV":
            generator = MRVGenerator(self.size, self.colors)
        elif self.algorithm == "Dsatur":
            generator = DSATURGenerator(self.size, self.colors)
        elif self.algorithm == "Knuth":
            generator = DLXSudokuGenerator(self.size, self.colors)
        else:
            raise ValueError("Unknown algorithm selected!")  # Lève une erreur si un algorithme inconnu est fourni.
        
        return generator.generate_sudoku()  # Génère et retourne la grille de Sudoku avec l'algorithme choisi.

    def remove_colors(self, remove_count: int):
        """
        Retire un certain nombre de couleurs de la grille pour créer un puzzle à partir de la solution complète.
        
        Args:
            remove_count (int): Le nombre de cellules à retirer de la grille pour créer un puzzle.
        """
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]  # Crée une liste de toutes les cellules (r, c).
        random.shuffle(cells)  # Mélange les cellules pour enlever les couleurs de manière aléatoire.
        for _ in range(remove_count):
            if cells:
                r, c = cells.pop()  # Retire une cellule de la liste et l'enlève de la grille.
                self.grid[r][c] = None  # Enlève la couleur de la cellule pour créer un puzzle.

    def is_valid_solution(self) -> bool:
        """
        Vérifie si la grille actuelle est une solution valide. Toutes les cellules doivent être remplies et valides.
        
        Returns:
            bool: True si la grille est une solution valide, sinon False.
        """
        for r in range(self.size):
            for c in range(self.size):
                color = self.grid[r][c]
                if color is None:  # Si la cellule est vide, ce n'est pas une solution valide.
                    return False
                if not self.is_valid_placement(r, c, color):  # Vérifie si la couleur placée est valide.
                    return False
        return True  # Si toutes les cellules sont valides, la solution est valide.

    def is_valid_placement(self, row: int, col: int, color: str) -> bool:
        """
        Vérifie si une couleur peut être placée à une position donnée (ligne, colonne) dans la grille.
        
        Args:
            row (int): Indice de la ligne de la cellule.
            col (int): Indice de la colonne de la cellule.
            color (str): La couleur à vérifier.
        
        Returns:
            bool: True si le placement est valide, sinon False.
        """
        # Vérifie si la couleur est déjà présente dans la même ligne ou colonne
        for i in range(self.size):
            if i != col and self.grid[row][i] == color:
                return False  # La couleur est déjà présente dans la ligne.
            if i != row and self.grid[i][col] == color:
                return False  # La couleur est déjà présente dans la colonne.

        # Vérifie si la couleur est déjà présente dans la même boîte (sous-grille)
        box_size = self.rank  # Le "rank" est la racine carrée de la taille de la grille (3 pour 9x9).
        box_row, box_col = (row // box_size) * box_size, (col // box_size) * box_size
        for i in range(box_size):
            for j in range(box_size):
                r, c = box_row + i, box_col + j
                if (r, c) != (row, col) and self.grid[r][c] == color:
                    return False  # La couleur est déjà présente dans la boîte.
        return True  # Si aucun conflit, le placement est valide.

    def set_user_color(self, row: int, col: int, color: str):
        """
        Permet à l'utilisateur de définir une couleur dans une cellule spécifique, si la cellule est vide.
        
        Args:
            row (int): L'indice de la ligne de la cellule.
            col (int): L'indice de la colonne de la cellule.
            color (str): La couleur à attribuer à la cellule.
        """
        if self.grid[row][col] is None:  # Si la cellule est vide
            self.grid[row][col] = color  # Affecte la couleur à la cellule.

    def reveal_solution(self):
        """
        Révèle la solution complète du Sudoku (annule les couleurs retirées pour le puzzle).
        """
        self.grid = [row[:] for row in self.solution]  # Remplace la grille actuelle par la solution complète.
