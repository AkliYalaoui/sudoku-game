import random
from .interface import ISudoku

class BacktrackingGenerator(ISudoku):
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
        
        def solve(row=0, col=0):
            if row == self.size:
                return True
            if col == self.size:
                return solve(row + 1, 0)
            random.shuffle(self.colors)
            for color in self.colors:
                if is_valid(row, col, color, grid):
                    grid[row][col] = color
                    if solve(row, col + 1):
                        return True
                    grid[row][col] = None
            return False
        
        solve()
        return grid
