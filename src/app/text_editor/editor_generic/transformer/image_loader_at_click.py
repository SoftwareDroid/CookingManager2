from src.app.text_editor.editor_generic.i_transformer_cursor import ITransformerCursor
import os
from src.core.file_names import create_ok_filename, is_fillname_ok
from shutil import copyfile
import logging
from typing import Callable
from src.localization.programm_config import IMG_FOLDER
import gi
from src.app.share.engine.main_engine import GUIGTK
from typing import Tuple
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from src.core.hash import compare_hashs

class ImageLoaderAtClick(ITransformerCursor):

    def __init__(self, editor):
        # We need the editor to access the recipe name
        self._editor = editor

    def apply(self, cursor_pos: int, buffer: Gtk.TextBuffer) -> Tuple[str, str]:
        file_name = self.get_filename()
        if file_name is not None:
            new_file_name = self.copy_file_to_img_folder(file_name)
            print("BBBBBBBBBBBBBB")
            return new_file_name, "img"
        return "", None

    def copy_file_to_img_folder(self,file_name):
        # Remove forbidden chars
        base = os.path.basename(file_name)
        parts = os.path.splitext(base)
        new_file_name = create_ok_filename(parts[0]) + parts[1]
        # Set new target folder
        my_recipe_folder: str = self._editor.get_recipe_name() + "/"
        target_folder = IMG_FOLDER + my_recipe_folder
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            logging.info("Create folder: " + target_folder)
        # Copy file to target folder
        target_file: str = target_folder + new_file_name

        if os.path.exists(target_file) and not compare_hashs(file_name, target_file):
            logging.warning("Selected file has same new file name as " + target_file + " but not the same hash sum.")

        copyfile(file_name, target_file)
        # Insert Text with tag
        return new_file_name

    def get_filename(self):
        ret = None
        dialog = Gtk.FileChooserDialog("Please choose a file", GUIGTK.window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_file_filter(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            ret = dialog.get_filename()
        dialog.destroy()
        return ret

    def get_label(self) -> str:
        return "Image"

    def hide_from_context_menu(self):
        return False

    def add_file_filter(self, dialog):

        filterPng = Gtk.FileFilter()
        filterPng.set_name("PNG file format")
        filterPng.add_pattern("*.png")
        dialog.add_filter(filterPng)

        filterJPG = Gtk.FileFilter()
        filterJPG.set_name("JPG file format")
        filterJPG.add_pattern("*.jpeg")
        dialog.add_filter(filterJPG)

        filterBMP = Gtk.FileFilter()
        filterBMP.set_name("BMP file format")
        filterBMP.add_pattern("*.bmp")
        dialog.add_filter(filterBMP)

        filterSVG = Gtk.FileFilter()
        filterSVG.set_name("SVG file format")
        filterSVG.add_pattern("*.svg")
        dialog.add_filter(filterSVG)

        filterGIF = Gtk.FileFilter()
        filterGIF.set_name("GIF file format")
        filterGIF.add_pattern("*.gif")
        dialog.add_filter(filterGIF)