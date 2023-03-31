from src.gui.share.gtk_helper import GtkHelper
from src.gui.share.gui_generic_interfaces import IGUIViewer
from src.gui.viewer.gui_signals_viewer import GUISignalsViewer
import gi
import logging
from src.app.share.tag_manager import TagManager, DataType
from typing import List, Dict
from src.app.share.recipe import Recipe
from distutils.util import strtobool

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

from src.app.share.engine.i_gui_part import IGUIPart

class GUIViewerGtk(IGUIViewer,IGUIPart):
    def __init__(self):
        self.signals_in: IGUIViewer = self
        self.signals_out: GUISignalsViewer = None

    def initialize(self):
        """IGUI for calling generic gui function and guiSignals for forward massages to the logic"""
        #self.signals_out = gui_signals

        logging.info("Init Gtk Recipe Viewer")
        # Build search result table
        self._setup_search_result()
        # self.debug_setup_list_view()

        # Setup Search
        searchEntry: Gtk.Entry = self.builder.get_object("Search")
        searchEntry.connect("activate", self.on_active_search_entry)
        # Map First Tab
        self._row_key_to_recipe: Dict[str, Recipe] = {}

        # Create all import tags
        #GtkHelper.setup_import_tags(self, "EditorRecipe")

    def _set_info_field(self, message: str, color: str):
        # TODO same as in importer GUI
        message = GtkHelper.escape_string_for_html(message)
        info_field: Gtk.Label = self.builder.get_object("InfoFieldSearch")
        # https://developer.gnome.org/pango/stable/PangoMarkupFormat.html#PangoMarkupFormat
        info_field.set_markup("<b><span foreground='" + color + "'>" + message + "</span></b>")



    def on_active_search_entry(self, widget: Gtk.Entry):
        text: str = widget.get_text()
        self.signals_out.event_search_for_recipes(text)

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text

    def show_rendered_preview(self, text: str, annotations):
        pass

    def show_error(self, message: str):
        self._set_info_field(message, "crimson")

    def show_warning(self, message: str):
        self._set_info_field(message, "orange")

    def show_message(self, message: str):
        self._set_info_field(message, "green")

    @staticmethod
    def _convert_type_to_def_type(data_type: DataType):
        if data_type == DataType.NUMBER:
            return str
        elif data_type == DataType.STRING:
            return str
        elif data_type == DataType.BOOL:
            return bool
        elif data_type == DataType.DURATION:
            return str
        elif data_type == DataType.HIERARCHICAL_BOOL:
            return str
        else:
            assert False, "Define a datatype"

    def _setup_search_result(self):
        def truncate_number(self, number):
            """
            Rounds and truncates a number to one decimal place. Used for all
            float numbers in the data-view. The numbers are saved with full float
            precision.
            """
            number = round(number, 1)
            return number

        table_data_types = []
        table_columns: Gtk.TreeViewColumn = []
        columns = TagManager.get_search_columns()
        assert len(columns) != 0, "No columns defined"
        counter: int = 0
        renderer_text = Gtk.CellRendererText()
        for column in columns:
            tag_name: str = column

            tag = TagManager.get_tag(tag_name)
            display_name = tag.display_name
            assert tag is not None, "Error: Tag not Found " + tag_name
            data_type = tag.data_type

            # Add type for table
            t = GUIViewerGtk._convert_type_to_def_type(data_type)
            table_data_types.append(t)
            # Setup Table column properties
            table_column = Gtk.TreeViewColumn(display_name, renderer_text, text=counter)
            # Set truncate function in case of rendering numbers
            #  if data_type == data_type.NUMBER:
            # table_column.set_cell_data_func(renderer_text, \
            #                            lambda col, cell, model, iter, unused:
            #                          cell.set_property("text", "%g" % float(model.get(iter, 0)[0].replace(",","."))))

            table_columns.append(table_column)
            counter += 1

        # Unpack type arguments
        self._list_store = Gtk.ListStore(*table_data_types)
        # Setup columns
        search_output: Gtk.TreeView = self.builder.get_object("TreeViewSearchOutput")
        for table_column in table_columns:
            search_output.append_column(table_column)

        # Test fill
        # self._list_store.append(["Fedora", "http://fedoraproject.org/", "1"])
        # self._list_store.append(["Slackware", "http://www.slackware.com/", "2"])
        # self._list_store.append(["Sidux", "http://sidux.com/", "2"])
        search_output.set_model(self._list_store)
        select = search_output.get_selection()



        search_output.connect("row-activated", self.select_search_result)

        #select.connect("row-activated", self.select_search_result)

    def select_search_result(self, widget, row, data2):
        row_to_recipe: str = str(list(self._list_store[row]))
        recipe = self._row_key_to_recipe[row_to_recipe]
        self.signals_out.event_select_recipe(recipe)



    def show_search_result(self, recipes: List[Recipe]):
        # Firstly build List store
        # Clear old results
        self._row_key_to_recipe.clear()
        self._list_store.clear()
        for recipe in recipes:
            line = []
            for column in TagManager.get_search_columns():
                tag = TagManager.get_tag(column)
                if recipe.has_tag(column):
                    value_text = str(recipe.get_tag_value(column))
                    if tag.data_type == DataType.BOOL:
                        value = strtobool(value)
                    elif tag.data_type == DataType.STRING or tag.data_type == DataType.DURATION:
                        value = value_text
                    elif tag.data_type == DataType.NUMBER:
                        # Round Number to one digit
                        value = "{:.1f}".format(round(float(value_text), 1))

                    elif tag.data_type == DataType.HIERARCHICAL_BOOL:
                        value = "True"
                    else:
                        assert False, "Not handled search result"
                    line.append(value)
                else:
                    # Set default value if not exist
                    line.append(tag.default_value)
            # Append line
            assert len(TagManager.get_search_columns()) == len(line), " Not all cells set"
            self._list_store.append(line)
            # Save line to recipe in data structure
            self._row_key_to_recipe[str(line)] = recipe



    def debug_setup_list_view(self):
        search_output: Gtk.TreeView = self.builder.get_object("TreeViewSearchOutput")
        # list of tuples for each software, containing the software name, initial release, and main programming languages used
        self.liststore = Gtk.ListStore(str, str)
        self.liststore.append(["Fedora", "http://fedoraproject.org/"])
        self.liststore.append(["Slackware", "http://www.slackware.com/"])
        self.liststore.append(["Sidux", "http://sidux.com/"])
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        search_output.append_column(column_text)
        renderer_editabletext = Gtk.CellRendererText()
        renderer_editabletext.set_property("editable", True)
        column_editabletext = Gtk.TreeViewColumn("Editable Text",
                                                 renderer_editabletext, text=1)
        search_output.append_column(column_editabletext)
        renderer_editabletext.connect("edited", self.text_edited)
        search_output.set_model(self.liststore)
        # TODO click or clicked signal

    def show_rendered_preview(self, text: str, annotations):
        GtkHelper.show_rendered_preview(self,"EditorRecipe",text,annotations)