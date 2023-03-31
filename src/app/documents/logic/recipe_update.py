from enum import Enum  # for enum34, or the stdlib version
from typing import Dict,Any
import logging
from src.core.hash import hash_sum_of_file
from src.localization.programm_config import ASK_UPDATE_RECIPES_BY_IMPORT
from src.app.documents.gui.gtk_dokument_manager import GtkDokumentManager
from src.app.share.tag_manager import TagManager, Tag , DataType, get_all_children_recursively

class UpdateResult(Enum):
    UPDATE_ABORT, UPDATED, NEED_NO_UPDATE = range(3)

class RecipeUpdater:
    _hash_of_my_tags = None

    @staticmethod
    def _init():
        if RecipeUpdater._hash_of_my_tags is None:
            RecipeUpdater._hash_of_my_tags = hash_sum_of_file("src/localization/my_tags.py")
    @staticmethod
    def _update_json_data(json_data):
        header = json_data["header"]
        # Update hash
        header['sha256_my_tags'] = RecipeUpdater._hash_of_my_tags
        tags: Dict[Any] = json_data["body"]["properties-state"]
        for tag_name in list(tags.keys()):
            tag: Tag = TagManager.get_tag(tag_name)
            print(tag)
            # If a tag isn't defined delete them
            if tag is None:
                del tags[tag_name]

            # Fix Hierarchical bool
            if tag.data_type == DataType.HIERARCHICAL_BOOL:
                # Add missing children
                for should_child in get_all_children_recursively(tag):
                    if should_child not in tags[tag_name]:
                        tags[tag_name][should_child] = TagManager.get_tag(should_child).default_value
                # Remove children which are not found
                for child in list(tags[tag_name].keys()):
                    if child not in get_all_children_recursively(tag):
                        del tags[tag_name][child]
        # Set default values of not hierarchical bools
        for tag_name in TagManager.get_all_tags():
            if tag_name not in tags:
                tags[tag_name] = TagManager.get_tag(tag_name).default_value


    @staticmethod
    def update_recipe(key: str, json_data) -> UpdateResult:
        """Return True if case of update"""
        RecipeUpdater._init()
        header = json_data["header"]
        if header['format-version'] != "2":
            logging.error("Wrong recipe file format got %s expected",header['format-version'],"2")
            return UpdateResult.UPDATE_ABORT

        if header['sha256_my_tags'] != RecipeUpdater._hash_of_my_tags:
            if ASK_UPDATE_RECIPES_BY_IMPORT:
                # We don't have access to out signals so we use the gui in this way
                answer = GtkDokumentManager.dialog_update_recipe(key)
                if not answer:
                    logging.info("Abort importing recipe %s ", key)
                    return UpdateResult.UPDATE_ABORT
            RecipeUpdater._update_json_data(json_data)
            return UpdateResult.UPDATED
        else:
            return UpdateResult.NEED_NO_UPDATE
