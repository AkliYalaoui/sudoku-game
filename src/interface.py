from abc import ABC, abstractmethod
from typing import List, Optional

class ISudoku(ABC):
    """
    Interface abstraite pour la génération d'une grille de Sudoku.
    
    Cette classe définit une méthode abstraite `generate_sudoku` que toute 
    classe implémentant cette interface devra définir.
    """

    @abstractmethod
    def generate_sudoku(self) -> List[List[Optional[str]]]:
        """
        Génère une grille de Sudoku.

        Retourne :
            List[List[Optional[str]]]: Une matrice n^2xn^2 représentant la grille de Sudoku.
            Chaque case peut contenir une couleur ou être None (case vide).
        """
        ...
