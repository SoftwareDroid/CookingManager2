from src.app.property_editor.gui.editor_generic.property_editor_base import IPropertyDataType

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PropertyDatatypeBoolean(IPropertyDataType):
    """Creates a cell, with a certain value"""

    def create_cell(self, args) -> Gtk.Widget:
        self.check_button = Gtk.CheckButton()
        self.check_button.connect("toggled", lambda _: self.signal_change())
        return self.check_button

    def get_name(self) -> str:
        return type(self).__name__

    def set_cell_value(self, value):
        assert type(value) is bool, "Invalid data type." + value
        self.check_button.set_active(value)

    def get_value(self):
        return self.check_button.get_active()

    def signal_change(self):
        pass

    def set_activ(self,value):
        self.check_button.set_sensitive(value)
