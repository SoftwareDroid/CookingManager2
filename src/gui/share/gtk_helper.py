import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
import logging


class GtkHelper:
    @staticmethod
    def get_text_from_buffer(buffer: Gtk.TextBuffer) -> str:
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        return buffer.get_text(start_iter, end_iter, True)

    @staticmethod
    def escape_string_for_html(text: str) -> str:
        text = text.replace(r"\"", "&quot;")
        text = text.replace("'", "&#39;")
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text.replace(">", "&gt;")
        return text

        """Showed annotated text as recipe preview"""

    # Creates all tags which can be used by the using of annotated text
    @staticmethod
    def setup_import_tags(self, editor_name):
        # See https://developer.gnome.org/pygtk/stable/class-gtkcellrenderertext.html for all tag properties
        widget: Gtk.TextView = self.builder.get_object(editor_name)
        buffer = widget.get_buffer()
        self.import_error_tag = buffer.create_tag("error_red", foreground="red", weight=Pango.Weight.BOLD)

        self.recipe_tags = {}

        self.recipe_tags["b"] = buffer.create_tag("b",weight=Pango.Weight.BOLD)
        self.recipe_tags["i"] = buffer.create_tag("i",style=Pango.Style.ITALIC)
        self.recipe_tags["u"] = buffer.create_tag("u",underline=Pango.Underline.SINGLE)
        # headlines h1 to h4
        self.recipe_tags["h1"] = buffer.create_tag("h1",scale=1.5, weight=Pango.Weight.BOLD, foreground="slategray")
        self.recipe_tags["h2"] = buffer.create_tag("h2",scale=1.25, weight=Pango.Weight.BOLD, foreground="slategray")
        self.recipe_tags["h3"] = buffer.create_tag("h3",scale=1.1, weight=Pango.Weight.BOLD)
        self.recipe_tags["h4"] = buffer.create_tag("h4",scale=1, weight=Pango.Weight.BOLD)
        # Special tags
        # app:start_recipe -> Heading
        # Colors are defined under: https://drafts.csswg.org/css-color/#named-colors
        self.recipe_tags["app:start_recipe"] = buffer.create_tag("app:start_recipe",scale=2.0, weight=Pango.Weight.BOLD,
                                                                 foreground="royalblue")
        self.recipe_tags["app:start_ingredients"] = buffer.create_tag("app:start_ingredients",scale=1.25, weight=Pango.Weight.BOLD,
                                                                      foreground="royalblue")
        self.recipe_tags["app:start_method"] = buffer.create_tag("app:start_method",scale=1.25, weight=Pango.Weight.BOLD,
                                                                 foreground="royalblue")
        self.recipe_tags["app:error"] = buffer.create_tag("app:error",weight=Pango.Weight.BOLD, foreground="crimson")

        #Only a dummy entry don't edit
        self.recipe_tags["StarText"] = buffer.create_tag("StarText", background="gray", foreground="crimson",editable=False)
        self.recipe_tags["img"] = buffer.create_tag("img",foreground="crimson",editable=False)

        for x in self.recipe_tags:
            assert x == self.recipe_tags[x].props.name

    @staticmethod
    def show_rendered_preview(self, editor_name,text: str, annotations):
        """Showed annotated text as recipe preview"""

        def apply_tag(rule, text_buffer: Gtk.TextBuffer):
            if rule["tag"] not in self.recipe_tags:
                logging.warning("Could not apply tag " + rule["tag"] + " (error: tag not defined)")
                return
            start_iter = text_buffer.get_iter_at_offset(rule["begin"])
            # Add 1 because end isn't included
            end_iter = text_buffer.get_iter_at_offset(rule["end"] + 1)
            text_buffer.apply_tag(self.recipe_tags[rule["tag"]], start_iter, end_iter)

        widget: Gtk.TextView = self.builder.get_object(editor_name)
        buffer: Gtk.TextBuffer = widget.get_buffer()
        buffer.set_text(text)
        # Apply all tags
        for annotation in annotations:
            apply_tag(annotation, buffer)

        # Enable Import Button
        self.show_message("Valid recipe")
        # import_button = self.builder.get_object("ButtonImport")
        # import_button.set_sensitive(True)