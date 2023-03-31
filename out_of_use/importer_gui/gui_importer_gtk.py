from src.gui.share.gui_generic_interfaces import IGUI, IGUIImporter
from out_of_use.importer_gui.gui_signals_importer import GUISignalsImporter

from src.gui.share.gtk_helper import GtkHelper
import gi
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GUIImporterGtk(IGUIImporter):
    def init_importer(self, igui: IGUI, builder, gui_signals: GUISignalsImporter):
        """IGUI for calling generic gui function and guiSignals for forward massages to the logic"""
        self._IGUI = igui
        self.builder = builder
        self.gui_signals_importer = gui_signals
        self.show_recipe_import_dialog()

    # Get all text from a GTK-Buffer

    # Forward events
    def press_import_recipe(self, widget):
        self.gui_signals_importer.importer_press_import()

    def event_importer_change_method(self, widget: Gtk.TextBuffer):
        self.gui_signals_importer.importer_change_method(GtkHelper.get_text_from_buffer(widget))

    def event_importer_change_ingredient_list(self, widget: Gtk.TextBuffer):
        self.gui_signals_importer.importer_change_ingredientlist(GtkHelper.get_text_from_buffer(widget))

    def event_importer_change_recipe_name(self, widget: Gtk.Editable):
        self.gui_signals_importer.import_change_recipe_name(widget.get_text())

    def event_importer_preview_render_mode(self, switch, gparam):
        self.gui_signals_importer.importer_change_preview_render_mode(switch.get_active())

    # Show the preview of a recipe
    def show_xml_preview(self, xml: str):
        widget: Gtk.TextView = self.builder.get_object("EditorImportPreview")
        buffer = widget.get_buffer()
        buffer.set_text(xml)

        # Enable import Button
        self.show_message("Valid recipe")
        # import_button = self.builder.get_object("ButtonImport")
        # import_button.set_sensitive(True)

    def get_recipe_name(self) -> str:
        entry = self.builder.get_object("EntryRecipeName")
        return entry.get_text()

    def get_ingredients_list(self) -> str:
        widget: Gtk.TextView = self.builder.get_object("EditorImportIng")
        return GtkHelper.get_text_from_buffer(widget.get_buffer())

    def get_cooking_method(self) -> str:
        widget: Gtk.TextView = self.builder.get_object("EditorImportMethod")
        return GtkHelper.get_text_from_buffer(widget.get_buffer())

    def show_recipe_import_dialog(self):
        logging.info("Show import window")
        window: Gtk.Window = self.builder.get_object("WinImport")
        window.show_all()
        # Create all import tags
        GtkHelper.setup_import_tags(self, "EditorImportPreview")

        # Import Button
        import_button = self.builder.get_object("ButtonImport")
        import_button.connect("clicked", self.press_import_recipe)
        # https://stackoverflow.com/questions/9113717/text-changed-signal-for-text-view-widget-in-gtk3
        editor_ingredients: Gtk.TextView = self.builder.get_object("EditorImportIng")
        editor_ingredients.get_buffer().connect("changed", self.event_importer_change_ingredient_list)

        # Ingredient List
        editor_method: Gtk.TextView = self.builder.get_object("EditorImportMethod")
        editor_method.get_buffer().connect("changed", self.event_importer_change_method)

        # connect to Entry Recipe name
        entry_recipe_name: Gtk.Entry = self.builder.get_object("EntryRecipeName")
        # https://developer.gnome.org/gtk3/unstable/GtkEditable.html#GtkEditable-changed
        entry_recipe_name.connect("changed", self.event_importer_change_recipe_name)

        # Settings toggle render switch
        switch_render_xml = self.builder.get_object("ImportSwitchXMLPreview")
        switch_render_xml.connect("notify::active", self.event_importer_preview_render_mode)
        # Forward default settings
        self.gui_signals_importer.importer_change_preview_render_mode(switch_render_xml.get_active())

        # Disable Button at start.
        import_button = self.builder.get_object("ButtonImport")
        import_button.set_sensitive(False)



    def show_message(self, message: str):
        self._set_info_field(message, "green")
        # Disable Button
        import_button = self.builder.get_object("ButtonImport")
        import_button.set_sensitive(True)

    def show_warning(self, message: str):
        self._set_info_field(message, "yellow")
        # Disable Button
        import_button = self.builder.get_object("ButtonImport")
        import_button.set_sensitive(True)

    def clear_importer(self):
        # Clear Preview
        preview: Gtk.TextView = self.builder.get_object("EditorImportPreview")
        buffer = preview.get_buffer()
        buffer.set_text("")

        # Clear Recipe name
        entryRecipeName: Gtk.Entry = self.builder.get_object("EntryRecipeName")
        entryRecipeName.set_text("")

        # Cooking Method
        widget: Gtk.TextView = self.builder.get_object("EditorImportMethod")
        buffer = widget.get_buffer()
        buffer.set_text("")

        # Ingredient List
        widget: Gtk.TextView = self.builder.get_object("EditorImportIng")
        buffer = widget.get_buffer()
        buffer.set_text("")

        # Disable Button
        import_button = self.builder.get_object("ButtonImport")
        import_button.set_sensitive(False)

    def _set_info_field(self, message: str, color: str):

        info_field: Gtk.Label = self.builder.get_object("InfoField")
        # https://developer.gnome.org/pango/stable/PangoMarkupFormat.html#PangoMarkupFormat
        info_field.set_markup("<b><span foreground='" + color + "'>" + message + "</span></b>")

    def show_error(self, message: str):
        message = GtkHelper.escape_string_for_html(message)
        self._set_info_field(message, "crimson")
        # Disable Button
        import_button = self.builder.get_object("ButtonImport")
        import_button.set_sensitive(False)

    def show_rendered_preview(self, text: str, annotations):
        GtkHelper.show_rendered_preview(self,"EditorImportPreview",text,annotations)
