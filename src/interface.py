from abc import ABC, abstractmethod
from typing import List

class ISudoku(ABC):
    @abstractmethod
    def generate_sudoku(self) -> List[List[str | None]]:
        ...
