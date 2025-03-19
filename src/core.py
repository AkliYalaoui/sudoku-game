import random
from .backtracking import BacktrackingGenerator
from .mrv import MRVGenerator
from .dsatur import DSATURGenerator
from.knuth import DLXSudokuGenerator


class ColorSudoku:
    def __init__(self, size=9, algorithm="Backtracking", colors=None):
        self.size = size
        self.rank = int(size ** 0.5)  # Rank of the grid
        self.colors =  self.generate_colors()
        self.algorithm = algorithm
        self.grid = self.generate_sudoku()
        self.solution = [row[:] for row in self.grid]
        remove_count = int(.60*size**2)
        self.remove_colors(remove_count)

    def generate_colors(self):
        base_colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "cyan", "lime", "teal", "magenta", "gold", "silver", "navy", "maroon"]
        return base_colors[:self.rank**2]

    def generate_sudoku(self):
        """Generates the sudoku puzzle based on the selected algorithm."""
        if self.algorithm == "Backtracking":
            generator = BacktrackingGenerator(self.size, self.colors)
        elif self.algorithm == "MRV":
            generator = MRVGenerator(self.size, self.colors)
        elif self.algorithm == "Dsatur":
            generator = DSATURGenerator(self.size, self.colors)
        elif self.algorithm == "Knuth":
            generator = DLXSudokuGenerator(self.size, self.colors)
        else:
            raise ValueError("Unknown algorithm selected!")
        
        return generator.generate_sudoku()

    def remove_colors(self, remove_count):
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(cells)
        for _ in range(remove_count):
            if cells:
                r, c = cells.pop()
                self.grid[r][c] = None
    
    def is_valid_solution(self):
        for r in range(self.size):
            for c in range(self.size):
                color = self.grid[r][c]
                if color is None:
                    return False
                if not self.is_valid_placement(r, c, color):
                    return False
        return True
    
    def is_valid_placement(self, row, col, color):
        for i in range(self.size):
            if i != col and self.grid[row][i] == color:
                return False
            if i != row and self.grid[i][col] == color:
                return False
        box_size = self.rank
        box_row, box_col = (row // box_size) * box_size, (col // box_size) * box_size
        for i in range(box_size):
            for j in range(box_size):
                r, c = box_row + i, box_col + j
                if (r, c) != (row, col) and self.grid[r][c] == color:
                    return False
        return True
    
    def set_user_color(self, row, col, color):
        if self.grid[row][col] is None:
            self.grid[row][col] = color
    
    def reveal_solution(self):
        self.grid = [row[:] for row in self.solution]