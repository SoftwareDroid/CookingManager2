from typing import Tuple,Set
from src.app.share.recipe import Recipe
from similarity.levenshtein import Levenshtein
from src.app.share.tag_manager import TagManager
from enum import Enum
import operator
from distutils.util import strtobool

ALLOWED_WORD_DISTANCE_BY_SEARCH = 3
DEFAULT_BOOL_OPERATION = "and"


# Have to be NULL
class _Match(Enum):
    """ Different matches are used later to order the result."""
    NO_MATCH = 0
    INGREDIENT_MATCH = 1
    TAG_MATCH = 2  # A Searched Tag was found
    TAG_VOID_MATCH = 3  # A searched tag of data type void was found
    NAME_MATCH = 4
assert _Match.NO_MATCH.value == 0, "Match.NO_MATCH.value has to be null to interpreting as boolean"

def _search_random_recipe(arg: Tuple[Recipe,Set[str]]):
    recipe: Recipe = arg[0]
    random_set: Set[str] = arg[1]
    if recipe.key in random_set:
        return recipe, _Match.TAG_MATCH
    else:
        return recipe, _Match.NO_MATCH

# Search queries
def _search_with_recipe_name(arg: Tuple[str, Recipe]):
    """ Check if a recipe name match to a search string
    arg[0] = search string arg[1] recipe object"""
    search: str = arg[0]
    recipe: Recipe = arg[1]
    # Check word distance
    levenshtein = Levenshtein()
    # if search is a suffix or distance between them is under a threshold ALLOWED_WORD_DISTANCE_BY_SEARCH
    if search in recipe.name or levenshtein.distance(search, recipe.name) <= ALLOWED_WORD_DISTANCE_BY_SEARCH:
        return recipe, _Match.NAME_MATCH
    else:
        return recipe, _Match.NO_MATCH


def _search_with_ingredients(arg: Tuple[str, Recipe]):
    """Search if a recipe has a certain ingredient"""
    search: str = arg[0]
    recipe: Recipe = arg[1]
    # Check word distance
    for ingredient in recipe.ingredients:
        if search in ingredient.name:
            return recipe, _Match.INGREDIENT_MATCH
    return recipe, _Match.NO_MATCH


def _tag_void_search(arg: Tuple[str, Recipe]):
    """Check if a recipe has a certain tag and search recursively in children"""
    search: str = arg[0]
    recipe: Recipe = arg[1]
    if recipe.has_tag(search):
        return recipe, _Match.TAG_VOID_MATCH
    else:
        for child_tag in TagManager.get_tag(search).children:
            # search recursive further
            child_result = _tag_void_search((child_tag, recipe))
            if child_result[1] != _Match.NO_MATCH:
                return child_result
        return recipe, _Match.NO_MATCH


def _string_tag_search(arg: Tuple[str, Recipe, str]):
    search_tag: str = arg[0]
    recipe: Recipe = arg[1]
    str_search: str = arg[2]
    # Check
    if recipe.has_tag(search_tag):
        if str_search.lower() in recipe.get_tag_value(search_tag).lower():
            return recipe, _Match.TAG_MATCH
    # else:
    #    if str_search.lower() in str(TagManager.get_tag(search_tag).default_value).lower():
    #       return recipe, _Match.TAG_MATCH
    return recipe, _Match.NO_MATCH


def _duration_to_seconds(number: float, time_suffix: str) -> float:
    seconds_per_unit = {"s": 1, "m": 60, "min": 60, "h": 3600, "hour": 3600, "hours": 3600, "d": 86400, "w": 604800}
    assert time_suffix in seconds_per_unit, "Time suffix not found. Grammar changed? " + str(time_suffix)
    return seconds_per_unit[time_suffix] * number


def _duration_tag_search(arg: Tuple[str, Recipe, Tuple[str, float, str]]):
    def token_name_to_time_suffix(token_name):
        transformer = {"token_day": "d", "token_hour": "h", "token_min": "m"}
        assert token_name in transformer, "Unknown Token " + str(token_name)
        return transformer[token_name]

    assert len(arg) == 3, "Wrong using of _duration_tag_search"
    assert len(arg[2]) == 3, "Wrong using of _duration_tag_search"
    search_tag: str = arg[0]
    recipe: Recipe = arg[1]
    current_operator: str = arg[2][0]
    number: float = float(arg[2][1])
    search_time_unit: str = token_name_to_time_suffix(str(arg[2][2]))
    # Search time in seconds
    search_time_in_seconds: float = _duration_to_seconds(number, search_time_unit)
    # Check
    if recipe.has_tag(search_tag):
        tmp = recipe.get_tag_value(search_tag).split()
        assert len(tmp) == 2, "Grammar changed? Could to extract time suffix and number"
        current_number = float(tmp[0])
        current_time_unit: str = tmp[1]
        # Time in seconds
        current_time_in_sec: float = _duration_to_seconds(current_number, current_time_unit)
        op_dict = {'<': operator.lt,
                   '>': operator.gt,
                   '=': operator.eq,
                   '!=': operator.ne,
                   '<=': operator.le,
                   '>=': operator.ge,
                   }
        assert current_operator in op_dict, "Grammar Error: Unknown relational operator: " + str(current_operator)
        if op_dict[current_operator](current_time_in_sec, search_time_in_seconds):
            return recipe, _Match.TAG_MATCH
    return recipe, _Match.NO_MATCH


def _number_tag_search(arg: Tuple[str, Recipe, Tuple[str, float]]):
    assert len(arg) == 3, "Parameter Error: _number_tag_search"
    assert len(arg[2]) == 2, "Parameter Error: _number_tag_search"
    search_tag: str = arg[0]
    recipe: Recipe = arg[1]
    current_operator: str = arg[2][0]
    number: float = float(arg[2][1])
    # Check
    if recipe.has_tag(search_tag):
        op_dict = {'<': operator.lt,
                   '>': operator.gt,
                   '=': operator.eq,
                   '!=': operator.ne,
                   '<=': operator.le,
                   '>=': operator.ge,
                   }
        assert current_operator in op_dict, "Grammar Error: Unknown relational operator: " + str(current_operator)
        current_number: float = float(recipe.get_tag_value(search_tag))
        if op_dict[current_operator](current_number, number):
            return recipe, _Match.TAG_MATCH
    return recipe, _Match.NO_MATCH


def bool_tag_search(arg: Tuple[str, Recipe, bool]):
    """Checks if a recipe has a tag with a certain boolean value"""
    assert len(arg) == 3, "Parameter Error: bool_tag_search"
    search_value: bool = arg[2]
    recipe: Recipe = arg[1]
    search_tag: str = arg[0]
    # Check
    if recipe.has_tag(search_tag):
        # Convert tag text to boolean
        recipe_value: bool = bool(strtobool(recipe.get_tag_value(search_tag)))
        if recipe_value == search_value:
            return recipe, _Match.TAG_MATCH
    return recipe, _Match.NO_MATCH