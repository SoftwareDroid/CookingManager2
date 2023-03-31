import logging
import gi
from src.app.documents.gui.i_gtk_document_manager import IGtkDokumentManager
from src.app.documents.logic.i_dokument_manager_logic import IDocumentManagerLogic
from src.app.share.engine.main_engine import GUIGTK
from src.app.share.engine.i_gui_part import IGUIPart
from src.app.documents.gui.dialog_ask_recipe_name import RecipeNameDialog
from src.app.documents.gui.dialog_yes_no import DialogYesNo
from typing import Optional, Tuple

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GtkDokumentManager(IGtkDokumentManager, IGUIPart):
    def __init__(self):
        self.signals_in: IGtkDokumentManager = self
        self.signals_out: IDocumentManagerLogic = None

    def initialize(self):
        pass

    def set_window_title(self, title: str):
        window: Gtk.ApplicationWindow = self.builder.get_object("WinMain")
        window.set_title(title)

    def request_new_recipe_name(self) -> Tuple[Optional[str], bool]:
        dialog = RecipeNameDialog(GUIGTK.window)
        response = dialog.run()
        ret = None
        if response == Gtk.ResponseType.APPLY:
            ret = dialog.get_recipe_name()
        overwrite: bool = dialog.is_override_mode()
        dialog.destroy()
        return ret, overwrite

    @staticmethod
    def dialog_update_recipe(key: str) -> Tuple[bool,bool]:
        title: str = "Import Error"
        question: str = "The recipe " + key + " was created with other tags. Only updated recipes can be imported." \
                                              "Do you wish to update the recipe?"
        dialog = DialogYesNo(title, question)
        response = dialog.run()

        ret = False
        if response == Gtk.ResponseType.OK:
            ret = True
        elif response == Gtk.ResponseType.CANCEL:
            ret = False
        dialog.destroy()
        return ret

    def dialog_save_unsaved_changes(self, key) -> bool:
        title: str = "Unsaved changes"
        question: str = "You have unsaved changes made to " + key + " which will be lost if you proceed. Do you wish to save them first?"
        dialog = DialogYesNo(title, question)
        response = dialog.run()

        ret = False
        if response == Gtk.ResponseType.OK:
            ret = True
        elif response == Gtk.ResponseType.CANCEL:
            ret = False
        dialog.destroy()
        return ret
