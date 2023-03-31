from typing import Dict, Any, List, Tuple, Optional
from abc import abstractmethod, ABC
from src.app.property_editor.gui.editor_generic.iproperty_data_type import IPropertyDataType
import copy
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class KeyInfo:
    def __init__(self, display_name: str, read_only: bool, data_type: str, args, render_priority : Optional[int]):
        self.display_name = display_name
        self.read_only = read_only
        self.data_type = data_type
        # Value is set later
        self.value = None
        self.args = args
        self._render_priority = render_priority

    @property
    def render_priority(self):
        return self._render_priority

    def set_value(self, value):
        self.value = value


class PropertyEditorBase(ABC):
    def __init__(self):


        self._data_types_to_properties: Dict[str, IPropertyDataType] = {}
        # row -> Property
        self._cell_renderers: Dict[int, IPropertyDataType] = {}
        #self.list_box_name = "PropertyList"

    def get_data(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = {}
        for row in self._cell_renderers:
            entry: IPropertyDataType = self._cell_renderers[row]
            ret[entry.key] = entry.get_value()
        return ret
    def _sort_data_for_loading(self, data: Dict[str, Any]) -> List[Tuple[str, Any]]:
        """Sort the Properties after name"""
        ret = []
        for key in data:
            # Exclude Attributes which should not be rendered
            key_info: KeyInfo = self.get_key_infos(key)
            if key_info.render_priority is not None:
                # Save key, value because it is needed during init
                key_info.set_value(data[key])
                ret.append((key, key_info))
        # Sort by key
        ret.sort(key=lambda e: e[1].render_priority, reverse=False)
        return ret

    def clear(self):
        """Removes all Children"""
        list_box = self.builder.get_object(self.list_box_name)
        assert list_box is not None, "Property Editor Anchor does not exist (Wrong anchor id). " + self.list_box_name
        children = [x for x in list_box.get_children()]
        for child in children:
            list_box.remove(child)

    def _create_header(self):

        list_box = self.builder.get_object(self.list_box_name)
        # Add Header
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("", xalign=0)
        label.set_markup("<b>Property</b>")
        label2 = Gtk.Label("", xalign=0)
        label2.set_markup("<b>Value</b>")
        hbox.pack_start(label, True, True, 0)
        # Expand, fill, padding
        hbox.pack_start(label2, True, True, 0)
        row.set_selectable(False)
        list_box.add(row)

    @abstractmethod
    def _some_entry_changed(self):
        pass

    def load_data(self, data: Dict[str, Any]):

        self.clear()
        self._create_header()

        # 6.3. ListBox seems the best fit
        list_box = self.builder.get_object(self.list_box_name)
        assert list_box is not None, "ListBox for Property Editor not found."
        row_counter = 0
        for map_key, key_info in self._sort_data_for_loading(data):
            # Create Row
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            row.add(hbox)
            label = Gtk.Label(key_info.display_name, xalign=0)
            t = key_info.data_type
            assert t in self._data_types_to_properties, "Forgot to register data type: " + str(key_info.data_type)
            property_copy: IPropertyDataType = copy.copy(self._data_types_to_properties[t])
            # We need the map key for later export
            property_copy.set_key(map_key)

            # Redrict all entry changes to one method
            property_copy.signal_change = self._some_entry_changed

            # Save property for further use
            self._cell_renderers[row_counter] = property_copy
            # Create cell with arguments
            widget: Gtk.Widget = property_copy.create_cell(key_info.args)
            self.update_property(key_info, property_copy)

            hbox.pack_start(label, True, True, 0)
            # Expand, fill, padding
            hbox.pack_start(widget, False, True, 0)
            list_box.add(row)
            row_counter += 1
        self.builder.get_object(self.list_box_name).show_all()
    def update_property(self, key_info: KeyInfo, property: IPropertyDataType):
        property.set_activ(not key_info.read_only)
        property.set_cell_value(key_info.value)

    def register_data_type(self, date_type: IPropertyDataType):
        assert isinstance(date_type, IPropertyDataType), "No valid property representation."
        type_name = date_type.get_name()
        assert type_name not in self._data_types_to_properties, "A property for this data type is already defined."
        self._data_types_to_properties[type_name] = date_type

    @abstractmethod
    def get_key_infos(self, key: str) -> KeyInfo:
        pass
