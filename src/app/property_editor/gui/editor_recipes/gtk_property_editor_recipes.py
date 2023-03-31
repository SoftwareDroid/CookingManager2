from src.app.property_editor.gui.editor_generic.property_editor_base import PropertyEditorBase, KeyInfo
from src.app.property_editor.gui.editor_generic.data_types.property_datatype_boolean import \
    PropertyDatatypeBoolean
from src.app.property_editor.gui.editor_generic.data_types.property_datatype_str import PropertyDatatypeStr
from src.app.property_editor.gui.editor_generic.data_types.property_datatype_int import PropertyDatatypeInt
from src.app.property_editor.gui.editor_generic.data_types.property_datatype_float import PropertyDatatypeFloat
from src.app.property_editor.gui.editor_generic.data_types.property_datatype_combobox import \
    PropertyDatatypeCombobox
from src.app.property_editor.gui.editor_recipes.data_types.property_datatype_duration import \
    PropertyDatatypeDuration
from src.app.property_editor.gui.editor_recipes.data_types.property_hierachical_bool import \
    PropertyHierachicalBool

from typing import Dict, Any
from src.app.share.tag_manager import TagManager, DataType

from src.app.property_editor.gui.editor_recipes.i_gui_property_editor import IGUIPropertyEditor
from src.app.property_editor.logic.i_property_editor_logic import IPropertyEditor
from src.app.share.engine.i_gui_part import IGUIPart
from src.app.documents.logic.shared_signals import recipe_changed_properties
import logging
import gi

gi.require_version('Gtk', '3.0')


class GtkPropertyEditorRecipes(PropertyEditorBase,IGUIPropertyEditor, IGUIPart):
    def __init__(self):
        PropertyEditorBase.__init__(self)
        self.signals_in: IGUIPropertyEditor = self
        self.signals_out: IPropertyEditor = None
        self.list_box_name = "RecipePropertyEditor"
        # self.debug_build_table()
        self._register_data_types()
        # Run GUI
        #self.window.show_all()
        #Gtk.main()

    def _some_entry_changed(self):
        # Forward signal
        if recipe_changed_properties is not None:
            recipe_changed_properties()

    def export_state(self) -> Dict[str, Any]:
        return self.get_data()

    def import_state(self, state: Dict[str, Any]):
        self.load_data(state)

    def initialize(self):
        recipe = self._create_empty_recipe()
        self.load_data(recipe)

    def load_template(self, name: str):
        assert name == "default", "Not supported template"
        recipe = self._create_empty_recipe()
        self.load_data(recipe)

    def set_mode(self, read_only: bool):
        assert False, "Not yet implemented"

    def _register_data_types(self):
        self.register_data_type(PropertyDatatypeBoolean())
        self.register_data_type(PropertyDatatypeStr())
        self.register_data_type(PropertyDatatypeInt())
        self.register_data_type(PropertyDatatypeFloat())
        self.register_data_type(PropertyDatatypeCombobox())
        self.register_data_type(PropertyDatatypeDuration())
        self.register_data_type(PropertyHierachicalBool())

    def _create_empty_recipe(self) -> Dict[str, Any]:
        data = {}
        for tag_name in TagManager.get_all_tags():
            tag = TagManager.get_tag(tag_name)
            # Remove hierarchical none root tags
            if tag.parent is None:
                data[tag_name] = tag.default_value

        return data

    def _get_data_type_name(self, type: DataType) -> str:
        switcher = {
            DataType.STRING: PropertyDatatypeStr().get_name(),
            DataType.NUMBER: PropertyDatatypeFloat().get_name(),
            DataType.DURATION: PropertyDatatypeDuration().get_name(),
            DataType.HIERARCHICAL_BOOL: PropertyHierachicalBool().get_name(),
            DataType.BOOL: PropertyDatatypeBoolean().get_name(),
        }
        return switcher.get(type, "Type not found _get_data_type_name")

    def get_key_infos(self, key: str) -> KeyInfo:
        tag_info = TagManager.get_tag(key)
        render_priority = tag_info.render_priority
        display_name = tag_info.display_name
        read_only = tag_info.read_only
        data_type_args = tag_info.data_type_args
        data_type = self._get_data_type_name(tag_info.data_type)
        return KeyInfo(display_name, read_only, data_type, data_type_args, render_priority)

    # Create Editor for testing


# TODO Remove me debug code
#tags_init()
#editor = GtkPropertyEditorRecipes()
