import random
from .interface import ISudoku

class DSATURGenerator(ISudoku):
    def __init__(self, size=9, colors=None):
        self.size = size
        self.colors = colors if colors else ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "cyan"]
    
    def generate_sudoku(self):
        grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        
        def is_valid(row, col, color, grid):
            """Check if the color can be placed at grid[row][col]."""
            # Check row and column for color conflict
            for i in range(self.size):
                if grid[row][i] == color or grid[i][col] == color:
                    return False

            # Check the 3x3 subgrid for color conflict
            box_size = int(self.size ** 0.5)
            box_row, box_col = (row // box_size) * box_size, (col // box_size) * box_size
            for i in range(box_size):
                for j in range(box_size):
                    if grid[box_row + i][box_col + j] == color:
                        return False
            return True
        
        def calculate_dsat(row, col, grid):
            """Calculate the degree of saturation (DSAT) of a cell."""
            # Set of colors used by neighbors
            used_colors = set()
            for i in range(self.size):
                if grid[row][i] is not None:
                    used_colors.add(grid[row][i])
                if grid[i][col] is not None:
                    used_colors.add(grid[i][col])
            
            box_size = int(self.size ** 0.5)
            box_row, box_col = (row // box_size) * box_size, (col // box_size) * box_size
            for i in range(box_size):
                for j in range(box_size):
                    if grid[box_row + i][box_col + j] is not None:
                        used_colors.add(grid[box_row + i][box_col + j])
            
            return len(used_colors)
        
        def get_most_saturated_cell(grid):
            """Select the cell with the highest DSAT."""
            max_dsat = -1
            best_cell = None
            for row in range(self.size):
                for col in range(self.size):
                    if grid[row][col] is None:
                        dsat = calculate_dsat(row, col, grid)
                        if dsat > max_dsat:
                            max_dsat = dsat
                            best_cell = (row, col)
            return best_cell
        
        # DSATUR coloring algorithm
        while True:
            # Get the most saturated (constrained) cell
            cell = get_most_saturated_cell(grid)
            if cell is None:
                break  # All cells are filled
            
            row, col = cell
            # Try to assign the smallest valid color
            for color in self.colors:
                if is_valid(row, col, color, grid):
                    grid[row][col] = color
                    break
        
        return grid
