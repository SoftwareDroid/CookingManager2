# For Interfaces See https://www.youtube.com/watch?v=Nyn2dylpPDE
from abc import ABCMeta, abstractmethod, ABC
from typing import List
from src.app.share.recipe import Recipe

class IGUIImporter(ABC):
    def init(self):
        super().__init__()

    @abstractmethod
    def get_ingredients_list(self) -> str: pass

    @abstractmethod
    def show_error(self, message: str): pass

    # Show the preview of a recipe
    @abstractmethod
    def show_xml_preview(self, xml: str): pass

    # Renders the output similar to pdf in the window
    @abstractmethod
    def show_rendered_preview(self, text: str, annotations): pass

    @abstractmethod
    def get_recipe_name(self) -> str: pass

    # get the content of the cooking method text field
    @abstractmethod
    def get_cooking_method(self) -> str: pass

    # Clear all input fields
    @abstractmethod
    def clear_importer(self): pass


class IGUIViewer(ABC):
    def init(self):
        super().__init__()

    # Shows a error
    @abstractmethod
    def show_error(self, message: str): pass

    @abstractmethod
    def show_warning(self, message: str): pass

    # Shows a message
    @abstractmethod
    def show_message(self, message: str): pass

    # Show a search result
    @abstractmethod
    def show_search_result(self, recipes: List[Recipe]): pass

    @abstractmethod
    def show_rendered_preview(self, text: str, annotations): pass

