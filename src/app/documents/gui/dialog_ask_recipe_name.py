import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from src.app.documents.logic.i_dokument_manager_logic import IDocumentManagerLogic, ValidationResult
#
from src.localization.programm_config import COLOR_ERROR_TEXT, COLOR_OK_TEXT
from typing import Optional


class RecipeNameDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Choose a recipe name", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY))
        from src.app.documents.logic.dokument_manager_logic import DokumentManagerLogic
        self.document_manager : IDocumentManagerLogic = DokumentManagerLogic.instance()
        self.set_default_size(150, 100)

        box = self.get_content_area()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        hbox = Gtk.HBox(homogeneous=False, spacing=6)

        # The label before th entry
        label = Gtk.Label("Name: ")
        hbox.pack_start(label, True, True, 0)
        self.entry = Gtk.Entry()
        self.entry.connect("changed", self.event_change_entry)
        self.entry.set_text("")
        hbox.pack_start(self.entry, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)
        # Checkbox forced override
        self.check_override = Gtk.CheckButton("Overwrite Recipe")
        self.check_override.connect("toggled", lambda x: self.event_change_entry(None))
        self.check_override.set_active(False)
        vbox.pack_start(self.check_override, True, True, 0)
        # Error label
        self.error_label = Gtk.Label()
        vbox.pack_start(self.error_label, True, True, 0)

        box.add(vbox)
        self.show_all()

        self.event_change_entry(None)

    def is_override_mode(self) -> bool:
        return self.check_override.get_active()

    def get_recipe_name(self) -> str:
        text = self.entry.get_text()
        result = self.document_manager.validate_recipe_key(text, not self.is_override_mode())
        assert result == ValidationResult.OK, " Use this function only the the apply button is pressed"
        return text

    def event_change_entry(self,widget):
        text = self.entry.get_text()
        result = self.document_manager.validate_recipe_key(text, not self.is_override_mode())
        # save_button: Gtk.Button = self.builder.get_object("ButtonDialogSave")
        self.get_widget_for_response(Gtk.ResponseType.APPLY).set_sensitive(result == ValidationResult.OK)
        # save_button.set_sensitive(key_is_valid)
        if result == ValidationResult.ERR_INVALID_CHARS:
            self.error_label.set_markup(
                "<b><span foreground='" + COLOR_ERROR_TEXT + "'>" + "Valid characters are A-Z a-z 0-9 _" + "</span></b>")
        elif result == ValidationResult.ERR_NAME_ALREADY_EXITS:
            self.error_label.set_markup(
                "<b><span foreground='" + COLOR_ERROR_TEXT + "'>" + "The name already exist" + "</span></b>")
        elif result == ValidationResult.ERR_NAME_TO_SHORT:
            self.error_label.set_markup(
                "<b><span foreground='" + COLOR_ERROR_TEXT + "'>" + "Name to short" + "</span></b>")
        elif result == ValidationResult.OK:
            self.error_label.set_markup(
                "<b><span foreground='" + COLOR_OK_TEXT + "'>" + "Name valid" + "</span></b>")
        else:
            assert False, "Unknown Result state"
