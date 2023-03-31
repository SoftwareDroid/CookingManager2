from abc import ABC, abstractmethod
from typing import Tuple, Sequence

class IRecipeEditorLogic(ABC):
    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def import_state(self, state: Tuple[str, Sequence[Tuple[str, int, int]]]):
        pass

    @abstractmethod
    def export_state(self) -> Tuple[str, Sequence[Tuple[str, int, int]]]:
        pass

    @abstractmethod
    def get_recipe_name(self) -> str:
        pass