from out_of_use.importer_gui.gui_signals_importer import GUISignalsImporter
from src.gui.share.gui_generic_interfaces import IGUIImporter
from src.app.text_editor.editor_recipes.ingredient_parser import create_xml_recipe, xml_to_str,is_wellformed_xml
from src.app.share.recipe_repository import myRepository
from src.app.share.recipe import Recipe
import logging


# Beachte der Import muss richtig sein

class LogicImporter(GUISignalsImporter):
    def __init__(self,igui : IGUIImporter):
        assert igui != None, "IGUI not set"
        self.igui = igui
        self._repository = myRepository

    def import_change_recipe_name(self, name: str):
        # normalize the recipe name
        key = self._repository.convert_filename_to_key(name)
        #logging.info("Check Recipe name %s",key)
        # Forbid the creation of already existing recipes
        if self._repository.has_recipe(key):
            self.igui.show_error("Recipe name already exist.")
        else:
            self._calc_recipe_preview()

    def event_gui_init_finished(self):
        pass
        # NOTE ONLY DEBUG CODE
        # self._debug_load_recipe()

