from abc import ABC, abstractmethod
from src.app.share.recipe import Recipe

class GUISignalsViewer(ABC):

    @abstractmethod
    def event_search_for_recipes(self, search_text: str): pass

    # Select as search result an recipe
    @abstractmethod
    def event_select_recipe(self, recipe: Recipe): pass