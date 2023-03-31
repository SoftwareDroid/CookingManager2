from src.app.text_editor.editor_generic.tag_support_addon_gtk import TagSupportAddonGTK
from src.app.text_editor.editor_generic.i_transform_tag import ITagTransform
from typing import Tuple,Sequence, Dict
from src.app.text_editor.editor_generic.transformer.image_loader import ImageLoader
from src.app.text_editor.editor_recipes.transformer.ingredient_transformer import IngredientTransformer
from src.app.text_editor.editor_generic.transformer.image_loader_at_click import ImageLoaderAtClick
from src.app.text_editor.editor_generic.transformer.transformer_bold_text import TransformerBoldText
from src.app.text_editor.editor_generic.transformer.transformder_underline_text import TransformerUnderlineText
from src.app.text_editor.editor_generic.transformer.transformer_italic_text import TransformerItalicText
from src.app.text_editor.editor_generic.transformer.transformer_heading1 import TransformerHeading1
from src.app.text_editor.editor_generic.transformer.transformer_heading2 import TransformerHeading2

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

class RecipeTagManagerAddon(TagSupportAddonGTK):
    def __init__(self,editor):
        TagSupportAddonGTK.__init__(self,editor)

    def get_recipe_name(self) -> str:
        return TagSupportAddonGTK.get_recipe_name(self)

    def clear(self):
        TagSupportAddonGTK.clear(self)


    def setup_my_transformer(self):
        #class StarTransformer(ITagTransform):
        #    def initialise(self, old_text: str, _):
        #        self.old_text = old_text

        #    def get_replacement_text(self) -> Tuple[str, Sequence[Tuple[str, int, int]]]:
        #        return self.old_text.upper(), []

        #    def event_after_replacement(self):
        #        pass

        img_loader = ImageLoader()
        self.register_tag_transformer("img", img_loader)
        self.register_tag_transformer("ingredients", IngredientTransformer())
        self.register_tag_transformer("img_cursor", ImageLoaderAtClick(self))
        self.register_tag_transformer("b", TransformerBoldText())
        self.register_tag_transformer("u", TransformerUnderlineText())
        self.register_tag_transformer("i", TransformerItalicText())
        self.register_tag_transformer("h1", TransformerHeading1())
        self.register_tag_transformer("h2", TransformerHeading2())

        # self.register_tag_transformer("StarText", StarTransformer())

    # Creates all tags which can be used by the using of annotated text
    def define_all_tags(self):
        # See https://developer.gnome.org/pygtk/stable/class-gtkcellrenderertext.html for all tag properties
        widget: Gtk.TextView = self.builder.get_object(self.editor_name)
        buffer = widget.get_buffer()
        # Tags which are always needed
        buffer.create_tag("non_editable",editable=False)
        buffer.create_tag("invisible", invisible=True, editable=False)


        self.recipe_tags = {}
        self.recipe_tags["b"] = buffer.create_tag("b", weight=Pango.Weight.BOLD,
                                                         editable=False)
        self.recipe_tags["i"] = buffer.create_tag("i", style=Pango.Style.ITALIC,
                                                         editable=False)
        self.recipe_tags["u"] = buffer.create_tag("u", underline=Pango.Underline.SINGLE,
                                                         editable=False)
        # headlines h1 to h4
        self.recipe_tags["h1"] = buffer.create_tag("h1", scale=1.5, editable=False, weight=Pango.Weight.BOLD, foreground="royalblue")
        self.recipe_tags["h2"] = buffer.create_tag("h2", scale=1.25, editable=False, weight=Pango.Weight.BOLD, foreground="royalblue")

        #self.recipe_tags["app:error"] = buffer.create_tag("app:error", weight=Pango.Weight.BOLD, foreground="crimson")
        # Only a dummy entry don't edit
        #self.recipe_tags["StarText"] = buffer.create_tag("StarText", background="gray", foreground="crimson",
        #                                                 editable=False)

        self.recipe_tags["img"] = buffer.create_tag("img", foreground="crimson", editable=False)
        self.recipe_tags["ingredients"] = buffer.create_tag("ingredients", background="gray", editable=False)

        for tag in list(self.recipe_tags):
            self.recipe_tags[":start_tag:" + tag] = buffer.create_tag(":start_tag:" + tag)
            self.recipe_tags[":end_tag:" + tag] = buffer.create_tag(":end_tag:" + tag)




        # self.recipe_tags["h3"] = buffer.create_tag("h3", scale=1.1, weight=Pango.Weight.BOLD)
        # self.recipe_tags["h4"] = buffer.create_tag("h4", scale=1, weight=Pango.Weight.BOLD)
        # Special tags
        # app:start_recipe -> Heading
        # Colors are defined under: https://drafts.csswg.org/css-color/#named-colors
        # self.recipe_tags["app:start_recipe"] = buffer.create_tag("app:start_recipe", scale=2.0,
        #                                                         weight=Pango.Weight.BOLD,
        #                                                         foreground="royalblue")
        # self.recipe_tags["app:start_ingredients"] = buffer.create_tag("app:start_ingredients", scale=1.25,
        #                                                              weight=Pango.Weight.BOLD,
        #                                                              foreground="royalblue")
        # self.recipe_tags["app:start_method"] = buffer.create_tag("app:start_method", scale=1.25,
        #                                                         weight=Pango.Weight.BOLD,
        #                                                         foreground="royalblue")


    def init_buttons(self):
        pass
        #self._tag_name_to_button_id: Dict[str, str] = {}
        # Connect to Buttons
        #self.init_tag_apply_button("ButtonBold", "b")
        #self.init_tag_apply_button("ButtonItalic", "i")
        #self.init_tag_apply_button("ButtonUnderline", "u")
        #self.init_tag_apply_button("ButtonIngredients", "ingredients")

        # self.init_tag_apply_button("ButtonStarText", "StarText")
        #self.init_tag_apply_button("ButtonImg", "img")