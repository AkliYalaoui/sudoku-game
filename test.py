import unittest
from typing import List
from src.backtracking import BacktrackingGenerator
from src.mrv import MRVGenerator
from src.dsatur import DSATURGenerator
from src.knuth import DLXSudokuGenerator

class TestColorSudoku(unittest.TestCase):
    """
    Classe de test pour vérifier les générateurs de Sudoku coloré utilisant différents algorithmes.
    Cette classe teste si les générateurs produisent des grilles valides, sans conflits dans les lignes,
    les colonnes et les sous-grilles.
    """

    def generate_colors(self, size) -> List[str]:
        """
        Génère une liste de couleurs basée sur la taille du Sudoku (rank). Par défaut, elle utilise une liste
        pré-définie de couleurs et limite la taille de cette liste en fonction du rang (ex. 3x3 ou 4x4).
        
        Returns:
            List[str]: Liste de couleurs.
        """
        base_colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "cyan", "lime", "teal", "magenta", "gold", "silver", "navy", "maroon"]
        return base_colors[:size]  # Limite les couleurs à la taille de la grille (par exemple, 9 couleurs pour un Sudoku 9x9).

    def is_valid_sudoku(self, grid, size):
        """
        Vérifie si une grille de Sudoku est valide. Cette fonction vérifie les conflits dans les lignes,
        les colonnes et les sous-grilles (les "boîtes" dans un Sudoku).

        Args :
            grid (List[List[Optional[str]]]) : Grille du Sudoku à tester.
            size (int) : Taille de la grille (par exemple, 9 pour un Sudoku standard).

        Retourne :
            bool : True si la grille est valide, False sinon.
        """
        # Vérification des conflits dans les lignes et les colonnes
        for r in range(size):
            row_colors = set()
            col_colors = set()
            for c in range(size):
                # Vérification des conflits dans la ligne
                if grid[r][c] is not None:
                    if grid[r][c] in row_colors:
                        return False
                    row_colors.add(grid[r][c])
                # Vérification des conflits dans la colonne
                if grid[c][r] is not None:
                    if grid[c][r] in col_colors:
                        return False
                    col_colors.add(grid[c][r])

        # Vérification des conflits dans les sous-grilles (boîtes)
        box_size = int(size ** 0.5)  # Taille de chaque boîte (par exemple 3x3 pour un Sudoku 9x9)
        for box_r in range(0, size, box_size):
            for box_c in range(0, size, box_size):
                box_colors = set()
                for i in range(box_size):
                    for j in range(box_size):
                        r, c = box_r + i, box_c + j
                        if grid[r][c] is not None:
                            if grid[r][c] in box_colors:
                                return False
                            box_colors.add(grid[r][c])
        return True

    def test_backtracking_generator(self):
        """Test du générateur de Sudoku utilisant l'algorithme de Backtracking."""
        for size in [4,9, 16]:
            colors = self.generate_colors(size)
            generator = BacktrackingGenerator(size=size, colors=colors)
            grid = generator.generate_sudoku()  # Génère une grille de Sudoku
            # Vérifie si la grille générée est valide
            self.assertTrue(self.is_valid_sudoku(grid, size), f"Backtracking algorithm with size {size} generated an invalid Sudoku grid.")

            # Vérifie si toutes les cellules sont colorées (aucune cellule vide)
            for row in grid:
                for cell in row:
                    self.assertIsNotNone(cell, f"Cell {row, grid.index(row)} is uncolored in Backtracking algorithm with size {size}.")

    def test_mrv_generator(self):
        """Test du générateur de Sudoku utilisant l'algorithme MRV (Minimum Remaining Values)."""
        for size in [4,9, 16]:
            colors = self.generate_colors(size)
            generator = MRVGenerator(size=size, colors=colors)
            grid = generator.generate_sudoku()
            self.assertTrue(self.is_valid_sudoku(grid, size), f"MRV algorithm with size {size} generated an invalid Sudoku grid.")

            # Vérifie que chaque cellule est colorée
            for row in grid:
                for cell in row:
                    self.assertIsNotNone(cell, f"Cell {row, grid.index(row)} is uncolored in MRV algorithm with size {size}.")

    def test_dsatur_generator(self):
        """Test du générateur de Sudoku utilisant l'algorithme DSATUR (Degree of Saturation)."""
        for size in [4,9]:
            colors = self.generate_colors(size)
            generator = DSATURGenerator(size=size, colors=colors)
            grid = generator.generate_sudoku()
            self.assertTrue(self.is_valid_sudoku(grid, size), f"DSATUR algorithm with size {size} generated an invalid Sudoku grid.")

            # Vérifie que chaque cellule est colorée
            for row in grid:
                for cell in row:
                    self.assertIsNotNone(cell, f"Cell {row, grid.index(row)} is uncolored in DSATUR algorithm with size {size}.")

    def test_knuth_generator(self):
        """Test du générateur de Sudoku utilisant l'algorithme de Knuth (DLX - Dancing Links)."""
        for size in [4,9,16]:
            colors = self.generate_colors(size)
            generator = DLXSudokuGenerator(size=size, colors=colors)
            grid = generator.generate_sudoku()
            self.assertTrue(self.is_valid_sudoku(grid, size), f"KNUTH algorithm with size {size} generated an invalid Sudoku grid.")

            # Vérifie que chaque cellule est colorée
            for row in grid:
                for cell in row:
                    self.assertIsNotNone(cell, f"Cell {row, grid.index(row)} is uncolored in KNUTH algorithm with size {size}.")

# Permet d'exécuter les tests lorsque ce fichier est exécuté en tant que script.
if __name__ == "__main__":
    unittest.main()
