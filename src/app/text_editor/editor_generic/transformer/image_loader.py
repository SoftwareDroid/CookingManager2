from typing import Tuple, List, Dict
from src.app.text_editor.editor_generic.i_transformer_range import ITransformerRange

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf, InterpType
from src.localization.programm_config import MAX_IMAGE_SIZE_IN_EDITOR
from src.app.documents.logic.dokument_manager_logic import DokumentManagerLogic, IDocumentManagerLogic
from src.localization.programm_config import KEY_OF_EMPTY_RECIPE


class ImageLoader(ITransformerRange):
    loaded_images: Dict[str, Pixbuf] = {}



    def initialise(self, old_text: str, arg: Tuple[Gtk.TextBuffer, int, int]):
        self.old_text = old_text
        self.arg = arg

    def get_replacement_text(self) -> Tuple[str, List[Tuple[str, int, int]]]:
        file_name = self.old_text

        doc_manager = DokumentManagerLogic.instance()
        current_recipe = doc_manager.get_current_recipe()
        if current_recipe is None:
            current_recipe = KEY_OF_EMPTY_RECIPE

        img_folder: str = doc_manager.get_image_folder_for_recipe(current_recipe)

        arg = self.arg
        # Load Image
        try:
            # We use relative file links
            full_path = img_folder + file_name
            pixbuf = Pixbuf.new_from_file(full_path)
            pixbuf = self.scale_image_if_needed(pixbuf)


            buffer: Gtk.TextBuffer = self.arg[0]

            start_index: int = self.arg[1]
            # Apply img tag to image to make it unchangeable
            insert_it = buffer.get_iter_at_offset(start_index)
            buffer.insert_pixbuf(insert_it, pixbuf)
            # Make the picture path invisible and before the non editable picture
            #return path, [("img",start_index -1, start_index)]

            return file_name, [("invisible",start_index , start_index + len(file_name)),("non_editable",start_index -1, start_index)]
        except gi.repository.GLib.Error as exp:
            return "img2 tag: Failed to load file '" + full_path + "'", []

    def scale_image_if_needed(self,pixbuf):
        scale_factor = 1
        if pixbuf.get_width() > MAX_IMAGE_SIZE_IN_EDITOR[0]:
            tmp = float(MAX_IMAGE_SIZE_IN_EDITOR[0]) / pixbuf.get_width()
            scale_factor = min(scale_factor, tmp)
        if pixbuf.get_height() > MAX_IMAGE_SIZE_IN_EDITOR[1]:
            tmp = float(MAX_IMAGE_SIZE_IN_EDITOR[0]) / pixbuf.get_width()
            scale_factor = min(scale_factor, tmp)

        if scale_factor < 1:
            return pixbuf.scale_simple(pixbuf.get_width() * scale_factor, pixbuf.get_height() * scale_factor,
                                         InterpType.BILINEAR)
        else:
            return pixbuf

    def hide_from_context_menu(self):
        return False

    def get_label(self) -> str:
        return "Image"

    def event_after_replacement(self):
        pass

    def is_deletable(self) -> bool:
        return True
