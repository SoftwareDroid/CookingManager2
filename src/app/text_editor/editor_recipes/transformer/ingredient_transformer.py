from typing import Tuple, List, Dict
from src.app.text_editor.editor_generic.i_transformer_range import ITransformerRange
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from src.app.text_editor.editor_recipes.ingredient_parser import ingredient_list_to_normalized_text,text_to_ingredient_list

class IngredientTransformer(ITransformerRange):
    def initialise(self, old_text: str, arg: Tuple[Gtk.TextBuffer, int, int]):
        self.old_text = old_text
        self.arg = arg

    def get_replacement_text(self) -> Tuple[str, List[Tuple[str, int, int]]]:
        ingredients = text_to_ingredient_list(self.old_text)
        text: str = ingredient_list_to_normalized_text(ingredients)
        return (text,[])

    def hide_from_context_menu(self):
        return False

    def event_after_replacement(self):
        pass

    def get_label(self) -> str:
        return "Format Ingredients"

    def is_deletable(self) -> bool:
        return True