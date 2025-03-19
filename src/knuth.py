import random
from .interface import ISudoku

class DLXNode:
    def __init__(self, row=None, col=None, up=None, down=None, left=None, right=None, column=None):
        self.row = row
        self.col = col
        self.up = up or self
        self.down = down or self
        self.left = left or self
        self.right = right or self
        self.column = column
        self.size = 0

class DLX:
    def __init__(self, matrix):
        self.header = DLXNode()
        self.nodes = []
        self.solution = []
        self.build_linked_matrix(matrix)

    def build_linked_matrix(self, matrix):
        columns = [DLXNode(col=i) for i in range(len(matrix[0]))]
        self.header.right = columns[0]
        columns[0].left = self.header
        
        for i in range(1, len(columns)):
            columns[i - 1].right = columns[i]
            columns[i].left = columns[i - 1]
        
        columns[-1].right = self.header
        self.header.left = columns[-1]
        
        for row in range(len(matrix)):
            first = None
            for col in range(len(matrix[row])):
                if matrix[row][col]:
                    node = DLXNode(row=row, col=col, column=columns[col])
                    columns[col].size += 1
                    if first is None:
                        first = node
                    else:
                        node.left = first.left
                        node.right = first
                        first.left.right = node
                        first.left = node
                    
                    columns[col].up.down = node
                    node.up = columns[col].up
                    node.down = columns[col]
                    columns[col].up = node
                    self.nodes.append(node)

    def cover(self, column):
        column.right.left = column.left
        column.left.right = column.right
        node = column.down
        while node != column:
            right_node = node.right
            while right_node != node:
                right_node.down.up = right_node.up
                right_node.up.down = right_node.down
                right_node.column.size -= 1
                right_node = right_node.right
            node = node.down

    def uncover(self, column):
        node = column.up
        while node != column:
            left_node = node.left
            while left_node != node:
                left_node.column.size += 1
                left_node.down.up = left_node
                left_node.up.down = left_node
                left_node = left_node.left
            node = node.up
        column.right.left = column
        column.left.right = column

    def search(self):
        if self.header.right == self.header:
            return True
        
        column = self.header.right
        self.cover(column)
        node = column.down
        
        while node != column:
            self.solution.append(node.row)
            right_node = node.right
            while right_node != node:
                self.cover(right_node.column)
                right_node = right_node.right
            
            if self.search():
                return True
            
            self.solution.pop()
            left_node = node.left
            while left_node != node:
                self.uncover(left_node.column)
                left_node = left_node.left
            node = node.down
        
        self.uncover(column)
        return False

class DLXSudokuGenerator(ISudoku):
    def __init__(self, size=9, colors=None):
        self.size = size
        self.colors = colors if colors else ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "cyan"]
    
    def generate_sudoku(self):
        matrix = self.create_exact_cover_matrix()
        dlx = DLX(matrix)
        dlx.search()
        return self.build_grid_from_solution(dlx.solution)

    def create_exact_cover_matrix(self):
        size = self.size
        num_constraints = 4 * size * size
        matrix = [[0] * num_constraints for _ in range(size * size * size)]
        
        box_size = int(size ** 0.5)  # Dynamically calculate box size
        
        for row in range(size):
            for col in range(size):
                for num in range(size):
                    index = (row * size + col) * size + num
                    matrix[index][row * size + col] = 1  # Cell constraint
                    matrix[index][size * size + row * size + num] = 1  # Row constraint
                    matrix[index][2 * size * size + col * size + num] = 1  # Column constraint
                    box = (row // box_size) * box_size + (col // box_size)  # Fix: dynamic box calculation
                    matrix[index][3 * size * size + box * size + num] = 1  # Box constraint
        return matrix


    def build_grid_from_solution(self, solution):
        grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        for entry in solution:
            row = entry // (self.size * self.size)
            col = (entry // self.size) % self.size
            num = entry % self.size
            grid[row][col] = self.colors[num]
        return grid
