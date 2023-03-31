import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from src.app.share.engine.main_engine import GUIGTK
from src.localization.programm_config import RECIPES_FILE_EXTENSION , RECIPE_FOLDER
from typing import Optional
import os
import logging
from src.app.documents.logic.i_dokument_manager_logic import IDocumentManagerLogic, ValidationResult
from src.app.documents.logic.dokument_manager_logic import DokumentManagerLogic
from src.localization.programm_config import COLOR_ERROR_TEXT, COLOR_OK_TEXT

class DialogSelectRecipeFile:

    @staticmethod
    def select_recipe() -> Optional[str]:
        """Return recipe key"""
        dialog = Gtk.FileChooserDialog("Please choose a recipe file", GUIGTK.window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        DialogSelectRecipeFile.add_filters(dialog)
        # Set Folder where all recipe are stored
        dialog.set_current_folder(RECIPE_FOLDER)
        dialog.connect("current-folder-changed", DialogSelectRecipeFile.current_folder_changed)
        response = dialog.run()
        ret = None
        if response == Gtk.ResponseType.OK:
            ret = os.path.splitext(os.path.basename(dialog.get_filename()))[0]
        elif response == Gtk.ResponseType.CANCEL:
            logging.info("Cancel file chooser dialog")
            ret = None

        dialog.destroy()
        return ret

    @staticmethod
    def current_folder_changed(dialog):
        should_path = os.getcwd() + "/" + RECIPE_FOLDER[:-1]
        if dialog.get_current_folder() != should_path:
            dialog.set_current_folder(should_path)
            logging.error("Only recipes in this folder can be selected")
        #print("A: " + cwd)
        #print("B" + dialog.get_current_folder())

    @staticmethod
    def add_filters(dialog):
        filter_any = Gtk.FileFilter()
        filter_any.set_name("JSON Recipes")
        filter_any.add_pattern("*." + RECIPES_FILE_EXTENSION)
        dialog.add_filter(filter_any)