from src.app.text_editor.editor_recipes.i_recipe_editor_logic import IRecipeEditorLogic
from src.app.text_editor.editor_recipes.i_recipe_editor_gtk import IRecipeEditorGtk
from src.app.share.engine.i_logic_part import ILogicPart
from typing import Tuple, Sequence
from src.app.property_editor.logic.property_editor_logic import PropertyEditorLogic
from src.core.file_names import create_ok_filename

class RecipeEditorLogic(IRecipeEditorLogic, ILogicPart):
    def __init__(self):
        self.signals_in: IRecipeEditorLogic = self
        self.signals_out: IRecipeEditorGtk = None

    def initialize(self):
        pass

    def get_recipe_name(self) -> str:
        logic_property_editor = self.get_addon(PropertyEditorLogic).logic
        properties_state = logic_property_editor.export_state()
        file_name = create_ok_filename(properties_state["name"])
        return file_name

    def clear(self):
        # Forward method call
        self.signals_out.clear()

    def import_state(self, state: Tuple[str, Sequence[Tuple[str, int, int]]]):
        # Forward method call
        self.signals_out.import_state(state)

    def export_state(self) -> Tuple[str, Sequence[Tuple[str, int, int]]]:
        # Forward method call
        return self.signals_out.export_state()
