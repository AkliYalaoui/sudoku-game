import random
from .interface import ISudoku

class MRVGenerator(ISudoku):
    def __init__(self, size=9, colors=None):
        self.size = size
        self.colors = colors if colors else ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "cyan"]
    
    def generate_sudoku(self):
        grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        def is_valid(row, col, color, grid):
            for i in range(self.size):
                if grid[row][i] == color or grid[i][col] == color:
                    return False
            box_size = int(self.size ** 0.5)
            box_row, box_col = (row // box_size) * box_size, (col // box_size) * box_size
            for i in range(box_size):
                for j in range(box_size):
                    if grid[box_row + i][box_col + j] == color:
                        return False
            return True
        
        def get_least_remaining_values_cell(grid):
            min_values = float('inf')
            best_cell = None
            for row in range(self.size):
                for col in range(self.size):
                    if grid[row][col] is None:
                        valid_colors = [color for color in self.colors if is_valid(row, col, color, grid)]
                        if len(valid_colors) < min_values:
                            min_values = len(valid_colors)
                            best_cell = (row, col)
            return best_cell
        
        def solve():
            cell = get_least_remaining_values_cell(grid)
            if cell is None:
                return True
            row, col = cell
            random.shuffle(self.colors)
            for color in self.colors:
                if is_valid(row, col, color, grid):
                    grid[row][col] = color
                    if solve():
                        return True
                    grid[row][col] = None
            return False
        
        solve()
        return grid