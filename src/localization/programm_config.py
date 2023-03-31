from typing import Tuple

# Ask the question if recipes with other localation files needs to be updated by import
ASK_UPDATE_RECIPES_BY_IMPORT: bool = True

COLOR_ERROR_TEXT: str = "crimson"
COLOR_OK_TEXT: str = "green"

# The name of program which is showed in title bar
PROGRAM_NAME = "CookingManager"

# The used template with default key value pairs of a new recipe
NEW_RECIPE_TEMPLATE_NAME: str = "default"

KEY_OF_EMPTY_RECIPE = "untitled"

IMG_FOLDER: str = "content/img/"
# The path for saving json recipes
RECIPE_FOLDER: str = "content/recipes/"
RECIPES_FILE_EXTENSION: str = "json"
# How much can you press srg+z in the editor
EDITOR_NUMBER_OF_RETURN_STEPS: int = 150
# Every image which is bigger than this size is scaled down automatically
MAX_IMAGE_SIZE_IN_EDITOR: Tuple[int,int] = (400, 400)