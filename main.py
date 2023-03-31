from src.app.share.engine.main_engine import MainEngine
from src.app.share.engine.engine_addon import EngineAddon
# Searcher Addon
from src.app.viewer.logic_viewer import LogicViewer
from src.gui.viewer.gui_viewer_gtk import GUIViewerGtk
# Property Editor Addon
from src.app.property_editor.logic.property_editor_logic import PropertyEditorLogic
from src.app.property_editor.gui.editor_recipes.gtk_property_editor_recipes import GtkPropertyEditorRecipes
# Menu Addon
from src.app.menu.logic.menu_logic import MenuLogic
from src.app.menu.gui.gtk_menu import GtkMenu
# Recipe Text Editor
from src.app.text_editor.editor_recipes.recipe_editor_gtk import RecipeEditorGtk
from src.app.text_editor.editor_recipes.recipe_editor_logic import RecipeEditorLogic
# Document Manager
from src.app.documents.gui.gtk_dokument_manager import GtkDokumentManager
from src.app.documents.logic.dokument_manager_logic import DokumentManagerLogic


import sys

import logging

# Clear logfile before start
with open('log_file.log', 'w'):
    pass
logging.basicConfig(filename='log_file.log', level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

if sys.version_info < (3, 0):
    logging.error("Use Python3 for this app")
else:
    main_engine = MainEngine()
    # Create Addons
    document_manager_addon = EngineAddon(DokumentManagerLogic.instance(), GtkDokumentManager())
    searcher_addon = EngineAddon(LogicViewer(), GUIViewerGtk())
    property_editor_addon = EngineAddon(PropertyEditorLogic(), GtkPropertyEditorRecipes())
    menu_addon = EngineAddon(MenuLogic(), GtkMenu())
    recipe_text_editor_addon = EngineAddon(RecipeEditorLogic(), RecipeEditorGtk())
    # Add addons
    main_engine.add_addon(document_manager_addon)
    main_engine.add_addon(recipe_text_editor_addon)
    main_engine.add_addon(searcher_addon)
    main_engine.add_addon(property_editor_addon)
    main_engine.add_addon(menu_addon)
    # Start program
    main_engine.run()
