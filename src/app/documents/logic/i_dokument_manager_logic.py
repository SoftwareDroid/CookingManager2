from src.app.share.recipe import Recipe
from abc import ABC, abstractmethod

from typing import Optional, Set

from enum import Enum  # for enum34, or the stdlib version

class ValidationResult(Enum):
    """OK = The Name can used as a new recipe name"""
    OK, ERR_NAME_ALREADY_EXITS, ERR_NAME_TO_SHORT, ERR_INVALID_CHARS = range(4)

class IDocumentManagerLogic(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def validate_recipe_key(self, key: str, new_key: bool) -> ValidationResult:
        """ If new key. The file the corresponding file is checked if exist"""
        pass

    @abstractmethod
    def convert_filename_to_key(_,filename: str) -> str:
        pass

    @abstractmethod
    def convert_key_to_filename(_, key: str) -> str:
        pass

    @abstractmethod
    def rename_current_recipe(self):
        pass

    @abstractmethod
    def load_all_recipes(self):
        pass

    @abstractmethod
    def save_current_recipe(self):
        pass

    @abstractmethod
    def close_current_recipe(self):
        """Clears the GUI"""
        pass

    @abstractmethod
    def delete_recipe(self, key: str):
        """Deletes a recipe from the filesystem"""
        pass

    @abstractmethod
    def ask_save_question_if_needed(self):
        """If there are unsaved changes ask for saving them"""
        pass

    @abstractmethod
    def get_current_recipe(self) -> Optional[str]:
        """The key of currently loaded recipe. None if none is loaded."""
        pass

    @abstractmethod
    def rename_recipe(self, current_key: str, new_key: str):
        pass

    @abstractmethod
    def open_recipe(self, key: str):
        """load a recipe in the GUI"""
        pass

    @abstractmethod
    def has_recipe(self, key: str) -> bool:
        pass

    @abstractmethod
    def create_empty_recipe(self):
        pass

    @abstractmethod
    def get_all_recipes(self) -> Set[Recipe]:
        pass