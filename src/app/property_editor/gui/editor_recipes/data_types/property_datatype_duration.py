from src.app.property_editor.gui.editor_generic.property_editor_base import IPropertyDataType

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PropertyDatatypeDuration(IPropertyDataType):
    def create_cell(self, args) -> Gtk.Widget:
        self.unit_entry = Gtk.ComboBoxText.new()

        self.name_to_id = {}
        counter = 0
        for item in ["s", "min", "h", "d"]:
            self.unit_entry.append_text(item)
            self.name_to_id[item] = counter
            counter += 1
        # Set default item
        self.unit_entry.set_active(0)
        # Spin Button for the number
        adjustment = Gtk.Adjustment(0, 0, 9999, 1, 0, 0)
        self.spin = Gtk.SpinButton()
        self.spin.configure(adjustment, climb_rate=1, digits=1)
        # Box for two Inputs
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)

        # Expand, fill, padding
        self.hbox.pack_start(self.spin, True, False, 0)
        self.hbox.pack_start(self.unit_entry, True, False, 0)
        self.spin.connect("value-changed", lambda _: self.signal_change())
        self.unit_entry.connect("changed", lambda _: self.signal_change())
        return self.hbox

    def signal_change(self):
        pass


    def get_name(self) -> str:
        return type(self).__name__

    def set_cell_value(self, value: str):
        assert type(value) is str, "Invalid data type."
        words = value.split(" ")
        assert len(words) == 2, "Invalid format duration"
        try:
            number = float(words[0].replace(",", "."))
            self.spin.set_value(number)
        except ValueError:
            assert False, "Invalid format duration"
        unit = words[1]
        assert unit in self.name_to_id,"Invalid format (Unit)" + unit
        self.unit_entry.set_active(self.name_to_id[unit])

    def get_value(self) -> str:

        return str(self.spin.get_value()) + " " + self.unit_entry.get_active_text()

    def set_activ(self, value):
        self.spin.set_editable(value)
        self.unit_entry.set_sensitive(value)