import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from src.app.share.engine.main_engine import GUIGTK
class DialogYesNo(Gtk.Dialog):

    def __init__(self, title: str, question: str):
        Gtk.Dialog.__init__(self, title, GUIGTK.window, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        label = Gtk.Label(question)

        box = self.get_content_area()
        box.add(label)
        self.show_all()

