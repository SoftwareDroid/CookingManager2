from src.app.property_editor.gui.editor_generic.property_editor_base import IPropertyDataType

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class PropertyDatatypeCombobox(IPropertyDataType):
    """Creates a cell, with a certain value"""

    def create_cell(self, args) -> Gtk.Widget:
        self.entry = Gtk.ComboBoxText.new()
        assert "items" in args, "No items for combobox specified"
        assert len(args["items"]) > 1 , "No items for combobox specified"
        self.name_to_id = {}
        counter = 0
        for item in args["items"]:
            self.entry.append_text(item)
            self.name_to_id[item] = counter
            counter += 1
        # Set default item
        self.entry.set_active(0)
        self.entry.connect("changed", lambda _: self.signal_change())
        return self.entry

    def signal_change(self):
        pass

    def get_name(self):
        return type(self).__name__

    def set_cell_value(self, value):
        assert type(value) is str, "Invalid data type."
        assert value in self.name_to_id, "Item does not exist in combobo"
        self.entry.set_active(self.name_to_id[value])

    def get_value(self):
        return self.entry.get_active_text()

    def set_activ(self, value):
        self.entry.set_sensitive(value)
