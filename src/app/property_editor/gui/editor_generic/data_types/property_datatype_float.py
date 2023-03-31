from src.app.property_editor.gui.editor_generic.property_editor_base import IPropertyDataType

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PropertyDatatypeFloat(IPropertyDataType):
    """Creates a cell, with a certain value"""

    def create_cell(self, args) -> Gtk.Widget:
        adjustment = Gtk.Adjustment(0, args["min"], args["max"], args.get("inc",1), 0, 0)
        self.spin = Gtk.SpinButton()
        self.spin.configure(adjustment, climb_rate=1, digits=args.get("digits",2))
        self.spin.connect("value-changed", lambda _: self.signal_change())
        return self.spin

    def get_name(self) -> str:
        return type(self).__name__

    def signal_change(self):
        pass

    def set_cell_value(self, value):
        value = float(value)
        assert type(value) is float, "Invalid data type."
        self.spin.set_value(value)

    def get_value(self):
        return self.spin.get_value()

    def set_activ(self, value):
        self.spin.set_sensitive(value)