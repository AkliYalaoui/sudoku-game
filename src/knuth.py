import random
from typing import List, Optional
from .interface import ISudoku

class DLXNode:
    """
    Représente un noeud dans la structure de données utilisée pour l'algorithme DLX (Dancing Links).

    Attributs :
        row (Optional[int]) : Numéro de la ligne associée à ce noeud.
        col (Optional[int]) : Numéro de la colonne associée à ce noeud.
        up (DLXNode) : Référence au noeud au-dessus dans la colonne.
        down (DLXNode) : Référence au noeud en dessous dans la colonne.
        left (DLXNode) : Référence au noeud à gauche dans la ligne.
        right (DLXNode) : Référence au noeud à droite dans la ligne.
        column (Optional[DLXNode]) : Référence à la colonne à laquelle ce noeud appartient.
        size (int) : Taille de la colonne (nombre de noeuds dans cette colonne).
    """
    def __init__(self, row: Optional[int] = None, col: Optional[int] = None, 
                 up: Optional['DLXNode'] = None, down: Optional['DLXNode'] = None,
                 left: Optional['DLXNode'] = None, right: Optional['DLXNode'] = None,
                 column: Optional['DLXNode'] = None):
        self.row = row
        self.col = col
        self.up = up or self  # Si pas de noeud au-dessus, on se réfère à soi-même (circularité)
        self.down = down or self  # Si pas de noeud en dessous, on se réfère à soi-même
        self.left = left or self  # Idem pour le gauche
        self.right = right or self  # Idem pour la droite
        self.column = column  # La colonne à laquelle ce noeud appartient
        self.size = 0  # Initialisation de la taille de la colonne


class DLX:
    """
    Implémentation de l'algorithme DLX (Dancing Links), utilisé pour résoudre des problèmes d'Exact Cover.

    Attributs :
        header (DLXNode) : Noeud représentant l'entête de la structure DLX.
        nodes (List[DLXNode]) : Liste de tous les noeuds de la structure DLX.
        solution (List[int]) : Liste des solutions trouvées.
    """
    def __init__(self, matrix: List[List[int]]):
        """
        Initialise la structure DLX à partir d'une matrice d'entrée.

        Args :
            matrix (List[List[int]]) : Matrice représentant les contraintes du problème.
        """
        self.header = DLXNode()  # Noeud d'entête
        self.nodes = []  # Liste des noeuds de la matrice
        self.solution = []  # Liste pour stocker la solution
        self.build_linked_matrix(matrix)  # Construction de la matrice liée

    def build_linked_matrix(self, matrix: List[List[int]]) -> None:
        """
        Convertit la matrice d'entrée en une structure de noeuds reliés.

        Args :
            matrix (List[List[int]]) : Matrice représentant les contraintes du problème.
        """
        # Création des colonnes de la structure DLX
        columns = [DLXNode(col=i) for i in range(len(matrix[0]))]
        
        # Relier les colonnes entre elles
        self.header.right = columns[0]
        columns[0].left = self.header
        for i in range(1, len(columns)):
            columns[i - 1].right = columns[i]
            columns[i].left = columns[i - 1]
        columns[-1].right = self.header
        self.header.left = columns[-1]
        
        # Créer les noeuds correspondant aux éléments de la matrice
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

    def cover(self, column: DLXNode) -> None:
        """
        Cache une colonne et ses noeuds associés (opération de couverture).

        Args :
            column (DLXNode) : Colonne à couvrir.
        """
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

    def uncover(self, column: DLXNode) -> None:
        """
        Découvre une colonne et ses noeuds associés (opération inverse de la couverture).

        Args :
            column (DLXNode) : Colonne à découvrir.
        """
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

    def search(self) -> bool:
        """
        Recherche la solution en utilisant l'algorithme de backtracking DLX.

        Retourne :
            bool : True si une solution est trouvée, sinon False.
        """
        # Si la structure est vide (toutes les colonnes sont couvertes), c'est une solution
        if self.header.right == self.header:
            return True
        
        # Sélectionne la colonne avec le moins de noeuds
        column = self.header.right
        self.cover(column)
        node = column.down
        
        # Parcours les noeuds de la colonne
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
    """
    Générateur de Sudoku utilisant l'algorithme DLX (Dancing Links) pour résoudre le problème d'Exact Cover.

    Cette classe résout un Sudoku en représentant le problème avec une matrice d'Exact Cover et 
    en utilisant l'algorithme DLX pour trouver une solution.

    Attributs :
        size (int) : Taille de la grille (par défaut 9x9).
        colors (List[str]) : Liste des couleurs utilisées pour remplir la grille.
    """
    def __init__(self, size: int = 9, colors: Optional[List[str]] = None) -> None:
        """
        Initialise le générateur de Sudoku.

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
        Génère une grille de Sudoku en résolvant un problème d'Exact Cover avec l'algorithme DLX.

        Retourne :
            List[List[Optional[str]]] : Une grille de Sudoku remplie avec des couleurs ou None.
        """
        matrix = self.create_exact_cover_matrix()  # Créer la matrice d'Exact Cover
        dlx = DLX(matrix)  # Créer une instance de DLX avec la matrice
        dlx.search()  # Résoudre le problème avec la méthode search de DLX
        return self.build_grid_from_solution(dlx.solution)  # Construire la grille à partir de la solution trouvée

    def create_exact_cover_matrix(self) -> List[List[int]]:
        """
        Crée la matrice d'Exact Cover représentant les contraintes du Sudoku.

        Retourne :
            List[List[int]] : La matrice d'Exact Cover pour le Sudoku.
        """
        size = self.size
        num_constraints = 4 * size * size  # Nombre de contraintes : cellule, ligne, colonne et bloc
        matrix = [[0] * num_constraints for _ in range(size * size * size)]  # Matrice vide
        
        box_size = int(size ** 0.5)  # Calcul dynamique de la taille du bloc
        
        # Remplir la matrice avec les contraintes
        for row in range(size):
            for col in range(size):
                for num in range(size):
                    index = (row * size + col) * size + num
                    matrix[index][row * size + col] = 1  # Contrainte sur la cellule
                    matrix[index][size * size + row * size + num] = 1  # Contrainte sur la ligne
                    matrix[index][2 * size * size + col * size + num] = 1  # Contrainte sur la colonne
                    box = (row // box_size) * box_size + (col // box_size)  # Calcul du bloc
                    matrix[index][3 * size * size + box * size + num] = 1  # Contrainte sur le bloc
        return matrix

    def build_grid_from_solution(self, solution: List[int]) -> List[List[Optional[str]]]:
        """
        Construit une grille de Sudoku à partir de la solution trouvée par l'algorithme DLX.

        Args :
            solution (List[int]) : Solution sous forme de liste de positions.

        Retourne :
            List[List[Optional[str]]] : La grille de Sudoku remplie avec des couleurs.
        """
        grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        for entry in solution:
            row = entry // (self.size * self.size)
            col = (entry // self.size) % self.size
            num = entry % self.size
            grid[row][col] = self.colors[num]  # Remplir la grille avec les couleurs correspondantes
        return grid
