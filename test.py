import unittest
from src.backtracking import BacktrackingGenerator
from src.mrv import MRVGenerator
from src.dsatur import DSATURGenerator
from src.knuth import DLXSudokuGenerator

class TestColorSudoku(unittest.TestCase):
    def is_valid_sudoku(self, grid, size):
        """Check if the Sudoku grid is valid (no conflicts in rows, columns, or subgrids)."""
        # Check rows and columns for conflicts
        for r in range(size):
            row_colors = set()
            col_colors = set()
            for c in range(size):
                if grid[r][c] is not None:
                    if grid[r][c] in row_colors:
                        return False
                    row_colors.add(grid[r][c])
                if grid[c][r] is not None:
                    if grid[c][r] in col_colors:
                        return False
                    col_colors.add(grid[c][r])

        # Check subgrids for conflicts
        box_size = int(size ** 0.5)
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
        """Test Backtracking Sudoku generation algorithm."""
        for size in [4,9,16]:
            generator = BacktrackingGenerator(size=size)
            grid = generator.generate_sudoku()
            self.assertTrue(self.is_valid_sudoku(grid, size), f"Backtracking algorithm with size {size} generated an invalid Sudoku grid.")

            for row in grid:
                for cell in row:
                    self.assertIsNotNone(cell, f"Cell {row, grid.index(row)} is uncolored in Backtracking algorithm with size {size}.")

    def test_mrv_generator(self):
        """Test Greedy Sudoku generation algorithm."""
        for size in [4,9]:
            generator = MRVGenerator(size=size)
            grid = generator.generate_sudoku()
            self.assertTrue(self.is_valid_sudoku(grid, size), f"MRV algorithm with size {size} generated an invalid Sudoku grid.")

            for row in grid:
                for cell in row:
                    self.assertIsNotNone(cell, f"Cell {row, grid.index(row)} is uncolored in MRV algorithm with size {size}.")

    def test_dsatur_generator(self):
        """Test DSATUR Sudoku generation algorithm."""
        for size in [4,9]:
            generator = DSATURGenerator(size=size)
            grid = generator.generate_sudoku()
            self.assertTrue(self.is_valid_sudoku(grid, size), f"DSATUR algorithm with size {size} generated an invalid Sudoku grid.")

            for row in grid:
                for cell in row:
                    self.assertIsNotNone(cell, f"Cell {row, grid.index(row)} is uncolored in DSATUR algorithm with size {size}.")

    def test_knuth_generator(self):
        """Test KNUTH Sudoku generation algorithm."""
        for size in [4,9,16]:
            generator = DLXSudokuGenerator(size=size)
            grid = generator.generate_sudoku()
            self.assertTrue(self.is_valid_sudoku(grid, size), f"KNUTH algorithm with size {size} generated an invalid Sudoku grid.")

            for row in grid:
                for cell in row:
                    self.assertIsNotNone(cell, f"Cell {row, grid.index(row)} is uncolored in KNUTH algorithm with size {size}.")

if __name__ == "__main__":
    unittest.main()
