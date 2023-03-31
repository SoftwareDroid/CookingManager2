import logging
import gi
from src.app.menu.gui.i_gtk_menu import IGtkMenu
from src.app.menu.logic.i_menu_logic import IMenuLogic
from src.app.share.engine.i_gui_part import IGUIPart
from src.app.documents.gui.dialog_select_recipe_file import DialogSelectRecipeFile
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GtkMenu(IGtkMenu, IGUIPart):
    def __init__(self):
        self.signals_in: IGtkMenu = self
        self.signals_out: IMenuLogic = None

    def initialize(self):
            save_item = self.builder.get_object("MenuSaveItem")
            save_item.connect("activate",lambda _: self.signals_out.event_save())
            self.builder.get_object("MenuRename").connect("activate", lambda _: self.signals_out.event_file_new())
            self.builder.get_object("MenuFileNew").connect("activate",lambda _: self.signals_out.event_file_new())
            self.builder.get_object("MenuFileOpen").connect("activate",self.event_file_open)

    def event_file_open(self,_):
        key = DialogSelectRecipeFile.select_recipe()
        if key is not None:
            self.signals_out.event_file_open(key)

    def show_error_dialog(self,title: str,message: str):
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, title)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()