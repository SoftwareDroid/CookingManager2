from src.gui.viewer.gui_signals_viewer import GUISignalsViewer
from src.gui.viewer.gui_viewer_gtk import GUIViewerGtk

import logging
# from ..grammar.interpreter import GrammarInterpreter
# See https://python-gtk-3-tutorial.readthedocs.io/en/latest/textview.html
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Connects GTK with the logic. Doesn't contain any business logic.
class GUIGTK:
    window = None
    def __init__(self):
        logging.info("Create GTK GUI")
        builder: Gtk.Builder = Gtk.Builder()
        builder.add_from_file("gui.glade")
        # builder.connect_signals(Handler())
        # Get Access to Builder in every single method
        self.builder = builder

        #self.viewer = GUIViewerGtk()
        #self.importer = GUIImporterGtk()

    def destory_event(self,_):
        from src.app.documents.logic.dokument_manager_logic import DokumentManagerLogic
        DokumentManagerLogic.instance().ask_save_question_if_needed()
        Gtk.main_quit()


    def run(self,callback_func):
        #self.gui_signals_importer = gui_signals_importer
        #self.gui_signals_viewer = gui_signals_viewer
        #logging.info("Initialize GUI")

        # Init importer and viewer
        #self.viewer.init_viewer(self, builder, gui_signals_viewer)

        # Init main window
        GUIGTK.window = self.builder.get_object("WinMain")
        GUIGTK.window.connect("destroy",self.destory_event )

        GUIGTK.window: Gtk.ApplicationWindow = GUIGTK.window
        #self._import_win: Gtk.ApplicationWindow = self.builder.get_object("WinImport")
        # Forward init finished
        callback_func()
        # Show the first window
        GUIGTK.window.show_all()

        Gtk.main()
