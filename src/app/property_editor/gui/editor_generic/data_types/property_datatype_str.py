from src.app.property_editor.gui.editor_generic.property_editor_base import IPropertyDataType

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PropertyDatatypeStr(IPropertyDataType):
    """Creates a cell, with a certain value"""

    def create_cell(self, args) -> Gtk.Widget:
        self.entry = Gtk.Entry()
        self.entry.connect("changed", lambda _: self.signal_change())
        return self.entry

    def signal_change(self):
        pass

    def get_name(self):
        return type(self).__name__

    def set_cell_value(self, value):
        assert type(value) is str, "Invalid data type."
        self.entry.set_text(value)

    def get_value(self):
        return self.entry.get_text()

    def set_activ(self, value):
        self.entry.set_sensitive(value)
