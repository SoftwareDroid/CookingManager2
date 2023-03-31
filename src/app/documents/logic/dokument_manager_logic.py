from src.app.share.engine.i_logic_part import ILogicPart
from src.app.documents.logic.i_dokument_manager_logic import IDocumentManagerLogic, ValidationResult
from src.app.documents.gui.i_gtk_document_manager import IGtkDokumentManager
from typing import Optional, Set , Dict, Any, Tuple , List
from src.app.share.recipe import Recipe
from src.localization.programm_config import KEY_OF_EMPTY_RECIPE, RECIPE_FOLDER, RECIPES_FILE_EXTENSION, NEW_RECIPE_TEMPLATE_NAME, \
    PROGRAM_NAME, IMG_FOLDER , ASK_UPDATE_RECIPES_BY_IMPORT
from src.localization.my_tags import tags_init
from src.app.property_editor.logic.property_editor_logic import PropertyEditorLogic, IPropertyEditor
from src.app.text_editor.editor_recipes.recipe_editor_logic import RecipeEditorLogic, IRecipeEditorLogic
from src.app.documents.logic.recipe_update import RecipeUpdater, UpdateResult
from src.core.hash import hash_sum_of_file, compare_hashs
import shutil
import os.path
import logging
import json
import re
import datetime
import os.path
from os import path

# Allowed chars in keys (filenames)
key_pattern = re.compile(r"\w+")
# Inverse
inverse_key_pattern = re.compile(r"[^\w]")

from src.localization.programm_config import RECIPE_FOLDER


def validate_recipe_key(key: str) -> bool:
    """Checks if a key has valid format"""
    return key_pattern.match(key) is not None


my_instance = None


class DokumentManagerLogic(IDocumentManagerLogic, ILogicPart):

    def __init__(self):
        self.signals_in: IDocumentManagerLogic = self
        self.signals_out: IGtkDokumentManager = None
        # Ignore change signals during some operations
        self.lock_ignore_change_signals = True
        # Need saving
        self.dirty_bit = False
        self._all_recipes = {}
        # Load all recipes
        tags_init()
        self.load_all_recipes()
        self.current_recipe_key = None
        # For detecting changes
        self.last_state_properties_editor = None
        self.last_state_text_edtior = None

    def _signal_recipe_changed_callback(self):
        if self.lock_ignore_change_signals:
            return

        if not self.dirty_bit:
            property_editor_state = self.get_addon(PropertyEditorLogic).logic.export_state()
            text_editor_state = self.get_addon(RecipeEditorLogic).logic.export_state()
            if text_editor_state != self.last_state_text_edtior or property_editor_state != self.last_state_properties_editor:
                self.dirty_bit = True
                self.last_state_text_edtior = text_editor_state
                self.last_state_properties_editor = property_editor_state
        # Update window title
        self._update_window_title()

    @staticmethod
    def instance():
        assert my_instance is not None, "Singleton error"
        return my_instance

    def validate_recipe_key(self, key: str, new_key: bool) -> validate_recipe_key:
        if len(key) < 3:
            return ValidationResult.ERR_NAME_TO_SHORT
        file_name = self.convert_key_to_filename(key)
        if new_key and (os.path.exists(file_name) or key.lower() in self._all_recipes or key.lower() == KEY_OF_EMPTY_RECIPE.lower()):
            return ValidationResult.ERR_NAME_ALREADY_EXITS
        """Checks if a key has valid format"""
        if key_pattern.match(key):
            return ValidationResult.OK
        else:
            return ValidationResult.ERR_INVALID_CHARS

    def convert_key_to_filename(_, key: str) -> str:
        """UID for a recipe to filename (not unique)"""
        return RECIPE_FOLDER + key.lower() + "." + RECIPES_FILE_EXTENSION

    def get_image_folder_for_recipe(self, key):
        import os
        cwd = os.getcwd()
        return cwd + "/" + IMG_FOLDER + key.lower() + "/"

    def convert_filename_to_key(_, filename: str) -> str:
        """Filename to recipe UID"""
        # Replace all evil chars
        return inverse_key_pattern.sub("_", filename)

    def initialize(self):
        self.create_empty_recipe()

    def load_all_recipes(self):
        self._load_repository()

    def get_all_recipes(self) -> Set[Recipe]:
        """ Return all recipes as objects"""
        ret = set()
        for x in self._all_recipes:
            ret.add(self._all_recipes[x])
        return ret

    def get_recipe(self, key: str) -> Recipe:
        """ Return a loaded recipe and NONE if not loaded"""
        return self._all_recipes[key]

    def close_current_recipe(self):
        self.current_recipe_key = None
        print("Close current recipe")
        pass

    def clear_img_folder(self, key):
        # Remove Img folder
        error = False
        rm_list = []
        img_folder: str = self.get_image_folder_for_recipe(key)
        if os.path.isdir(img_folder):
            for node in os.listdir(img_folder):
                if node.endswith(".png") or node.endswith(".jpeg") or node.endswith(".svg") or node.endswith(
                        ".bmp") or node.endswith(".gif"):
                    rm_list.append(img_folder + "/" + node)
                else:
                    error = True
            if not error:
                # Remove all images
                for file in rm_list:
                    os.remove(file)
                os.rmdir(img_folder)
            else:
                logging.error("Delete Error: The folder %s contains more than images", img_folder)

    def delete_recipe(self, key: str):
        if key is None:
            return



        # Remove Recipe file
        recipe_file_name: str = self.convert_key_to_filename(key)
        os.remove(recipe_file_name)
        # Remove from memory
        self._all_recipes.pop(key, None)
        # Remove all images
        self.clear_img_folder()

    def get_current_recipe(self) -> Optional[str]:
        return self.current_recipe_key

    def rename_current_recipe(self):
        if self.current_recipe_key is None:
            self.save_current_recipe()
        else:
            new_name: str = self.signals_out.request_new_recipe_name()
            self.copy_recipe(self.current_recipe_key, new_name)
            self.delete_recipe(self.current_recipe_key)

    def copy_recipe(self,old_key: str,new_key: str):
        assert old_key is not None, "Can only copy recipes saved on hdd"
        assert old_key != new_key, "Copy target has to be different as source"
        assert self.has_recipe(old_key), "Copy source doesn't exist"
        assert not self.has_recipe(new_key), "Desitation source already exist"
        # Copy img folder
        img_folder_1 = self.get_image_folder_for_recipe(old_key)
        img_folder_2 = self.get_image_folder_for_recipe(new_key)
        shutil.copytree(img_folder_1, img_folder_2)
        # copy recipe file
        shutil.copyfile(self.convert_key_to_filename(old_key), self.convert_key_to_filename(new_key))

    def rename_recipe(self, current_key: str, new_key: str):
        pass

    def ask_save_question_if_needed(self):
        if self.dirty_bit:
            # If the recipe has no name use the default one
            key_name: str = self.current_recipe_key
            if self.current_recipe_key is None:
                key_name = KEY_OF_EMPTY_RECIPE

            save_changes = self.signals_out.dialog_save_unsaved_changes(key_name)
            if save_changes:
                # Save changes
                self.save_current_recipe()


    def open_recipe(self, key: str):
        self.ask_save_question_if_needed()

        if key == self.current_recipe_key:
            logging.error("Cannot open already opened recipe")
            return
        self.lock_ignore_change_signals = True
        self.dirty_bit = False
        logging.info("Open recipe %s",key)
        # Throw current recipe memory state
        self._all_recipes.pop(key, None)
        # Reparse recipe from filesystem
        self._load_recipe(key)
        # Set current recipe
        self.current_recipe_key = key
        print(self._all_recipes)
        recipe: Recipe = self._all_recipes[key]
        # Get raw states of the recipe
        text_editor_state: Tuple[str, List[Tuple[str, int, int]]] = recipe.method
        property_editor_state: Dict[Any] = recipe.get_all_tags()

        # Load raw states in memory
        property_editor_logic: IPropertyEditor = self.get_addon(PropertyEditorLogic).logic
        property_editor_logic.import_state(property_editor_state)
        text_editor_logic: IRecipeEditorLogic = self.get_addon(RecipeEditorLogic).logic
        # Clear addons past
        text_editor_logic.clear()
        text_editor_logic.import_state(text_editor_state)
        self.lock_ignore_change_signals = False


    def has_recipe(self, key: str) -> bool:
        """Checks if a recipe is loaded"""
        return key in self._all_recipes

    def create_empty_recipe(self):
        self.ask_save_question_if_needed()
        # Ignore change signals
        self.lock_ignore_change_signals = True
        # No changes
        self.dirty_bit = False
        property_editor_logic: IPropertyEditor = self.get_addon(PropertyEditorLogic).logic
        text_editor_logic: IRecipeEditorLogic = self.get_addon(RecipeEditorLogic).logic
        property_editor_logic.load_template(NEW_RECIPE_TEMPLATE_NAME)
        text_editor_logic.clear()
        # We set the recipe name later
        self.current_recipe_key = None

        self.lock_ignore_change_signals = False
        self._update_window_title()


    def _update_window_title(self):
        # If we haven't chosen a file name use the default one of the template
        if self.current_recipe_key is None:
            property_editor_logic: IPropertyEditor = self.get_addon(PropertyEditorLogic).logic
            state = property_editor_logic.export_state()
            assert "name" in state, "name not in state"
            file_name = state["name"]
        else:
            file_name = self.convert_key_to_filename(self.current_recipe_key)
        if self.dirty_bit:
            self.signals_out.set_window_title(PROGRAM_NAME + " – " + file_name + " [changed]")
        else:
            self.signals_out.set_window_title(PROGRAM_NAME + " – " + file_name)

    def save_current_recipe(self):
        if self.current_recipe_key is None:
            name, overwrite = self.signals_out.request_new_recipe_name()
            if name is None:
                logging.info("Abort Saving")
                return
            if overwrite:
                self.delete_recipe(name)
            # Change name of current recipe
            self.current_recipe_key = name

            # Update property editor
            logic_property_editor: IPropertyEditor = self.get_addon(PropertyEditorLogic).logic
            properties_state = logic_property_editor.export_state()
            print("Save recipe name: ", name)
            properties_state["name"] = name
            logic_property_editor.import_state(properties_state)

        self._save_recipe()
        # Update window title
        self.dirty_bit = False
        self._update_window_title()

    def _save_recipe(self):
        logging.info("Save recipe %s ", self.current_recipe_key)
        logic_recipe_editor = self.get_addon(RecipeEditorLogic).logic
        logic_property_editor: IPropertyEditor = self.get_addon(PropertyEditorLogic).logic
        properties_state = logic_property_editor.export_state()
        editor_state = logic_recipe_editor.export_state()
        print("Save Editor: ",editor_state)
        self.last_state_text_edtior = editor_state
        self.last_state_properties_editor = properties_state
        # Get current time
        now = datetime.datetime.now()
        current_time = str(now.strftime("%Y-%m-%d %H:%M"))
        export_data = {}
        export_data["header"] = {"format-version": "2", "time": current_time}
        export_data["body"] = {"properties-state": properties_state, "editor-state": editor_state}
        assert "name" in properties_state, "Every recipe needs a name, which is used as filename."
        file_name = self.convert_key_to_filename(properties_state["name"])
        target_folder = RECIPE_FOLDER
        # Write file
        target_file: str = file_name
        export_data["header"]["filename"] = file_name
        export_data["header"]["sha256_my_tags"] = hash_sum_of_file("src/localization/my_tags.py")
        # Overwrite file if already exits
        with open(target_file, 'w') as f:
            json.dump(export_data, f, indent=4, separators=(',', ': '), sort_keys=True)
            # add trailing newline for POSIX compatibility
            f.write('\n')

    def _load_recipe(self, key: str):
        print("Load: ", key)
        if self.has_recipe(key):
            logging.error("Could not load %s because it is already loaded."
                          "A very similar file might exist in the same folder.", key)
            return
        # Don't load invalid recipes
        if self.validate_recipe_key(key, False) != ValidationResult.OK:
            logging.error("Invalid recipe identifier %s maybe the filename contains invalid characters", key)
            return
        # Parse recipe JSON
        recipe = self._parse_recipe(key)
        # Add recipe to loaded recipe, if there wasn't any error
        if recipe is not None:
            self._all_recipes[key] = recipe
            logging.info("Recipe %s successfully loaded", key)

        else:
            logging.error("Recipe %s not loaded successfully", key)

    def _load_repository(self):
        self.clear_img_folder(KEY_OF_EMPTY_RECIPE)
        self._all_recipes = {}
        import os
        logging.info("Load local recipe repository at " + str(os.getcwd() + "/" + RECIPE_FOLDER))
        for root, dirs, files in os.walk(RECIPE_FOLDER, topdown=False):
            for name in files:
                split_path = name.split(".")
                if len(split_path) == 2 and split_path[1] == RECIPES_FILE_EXTENSION:
                    recipe_key = self.convert_filename_to_key(split_path[0])
                    self._load_recipe(recipe_key.lower())
                else:
                    logging.warning("Invalid file %s in repository %s ", name, RECIPE_FOLDER)

    def _parse_recipe(self, key: str) -> Optional[Recipe]:
        # Get path
        filenname = self.convert_key_to_filename(key)
        with open(filenname) as json_file:
            self.json_data = json.load(json_file)
        update_result = RecipeUpdater.update_recipe(key, self.json_data)

         # Update file if needed
        if update_result == UpdateResult.UPDATED:
            with open(filenname, 'w') as outfile:
                json.dump(self.json_data, outfile, indent=4, separators=(',', ': '), sort_keys=True)
        if update_result != UpdateResult.UPDATE_ABORT:
            return Recipe(key, self.json_data)
        return None


my_instance = DokumentManagerLogic()
