from src.app.property_editor.gui.editor_generic.property_editor_base import IPropertyDataType

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PropertyDatatypeInt(IPropertyDataType):
    """Creates a cell, with a certain value"""

    def create_cell(self,args) -> Gtk.Widget:
        increment = 1
        adjustment = Gtk.Adjustment(0, args["min"], args["max"], increment, 0, 0)
        self.spin = Gtk.SpinButton()
        self.spin.configure(adjustment, climb_rate=1, digits=0)
        self.spin.connect("value-changed", lambda _: self.signal_change())
        return self.spin

    def signal_change(self):
        pass

    def get_name(self) -> str:
        return type(self).__name__

    def set_cell_value(self, value):
        assert type(value) is int, "Invalid data type."
        self.spin.set_value(value)

    def get_value(self):
        return self.entry.get_value_as_int()

    def set_activ(self, value):
        self.spin.set_sensitive(value)