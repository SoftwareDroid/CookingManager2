from src.app.text_editor.editor_generic.editor_return_stack_addon_gtk import EditorReturnStackAddonGtk
from src.app.text_editor.editor_recipes.recipe_tag_manager_addon import RecipeTagManagerAddon
from src.app.text_editor.editor_generic.simple_text_editor import Editor
from src.app.share.engine.i_gui_part import IGUIPart
from src.app.text_editor.editor_recipes.i_recipe_editor_gtk import IRecipeEditorGtk
from src.app.text_editor.editor_recipes.i_recipe_editor_logic import IRecipeEditorLogic
from src.app.documents.logic.shared_signals import recipe_changed_editor
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class RecipeEditorGtk(Editor, IGUIPart, IRecipeEditorGtk):
    def __init__(self):
        self.signals_in: IRecipeEditorGtk = self
        self.signals_out: IRecipeEditorLogic = None
        # Fix warnings
        self.addons = {}
        self.editor_name = None

    def get_recipe_name(self) -> str:
        return self.signals_out.get_recipe_name()

    def initialize(self):
        self.editor_name = "RecipeTextEditor"
        self.builder.get_object(self.editor_name).get_buffer().connect("changed", lambda _: recipe_changed_editor())
        self.init_addons()

    def apply_tag(self, name: str, start: int, end: int) -> int:
        return self.addons["tag_manager"].apply_tag(name,start,end)

    def import_state_callback(self):
        self.addons["tag_manager"].clear()

    def clear(self):
        # Clear all text
        text_editor = self.builder.get_object(self.editor_name)
        buffer = text_editor.get_buffer()
        buffer.set_text("")
        # Clear all tags
        self.addons["tag_manager"].clear()
        # Reset return stack
        self.addons["return_stack"].clear()

    def init_addons(self):
        self.addons["return_stack"] = EditorReturnStackAddonGtk(self)
        self.addons["tag_manager"] = RecipeTagManagerAddon(self)
        # Toggle of a tag, is counted as a user action.
        self.addons["tag_manager"].connect_toggle_tag_callback(lambda: self.addons["return_stack"].do_action())