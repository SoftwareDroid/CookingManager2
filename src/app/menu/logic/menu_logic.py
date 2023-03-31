from src.app.menu.logic.i_menu_logic import IMenuLogic
from src.app.menu.gui.i_gtk_menu import IGtkMenu
import logging
from src.app.share.engine.i_logic_part import ILogicPart
from src.app.documents.logic.dokument_manager_logic import IDocumentManagerLogic, DokumentManagerLogic
import os


class MenuLogic(IMenuLogic, ILogicPart):
    def __init__(self):
        self.signals_in: IMenuLogic = self
        self.signals_out: IGtkMenu = None

    def initialize(self):
        pass

    def event_save(self):
        document_manager: IDocumentManagerLogic = self.get_addon(DokumentManagerLogic).logic
        document_manager.save_current_recipe()

    def event_file_open(self,key: str):
        if key is not None:
            DokumentManagerLogic.instance().open_recipe(key)

    def event_file_new(self):
        DokumentManagerLogic.instance().create_empty_recipe()

    def event_rename_current_recipe(self):
        DokumentManagerLogic.instance().rename_current_recipe()
