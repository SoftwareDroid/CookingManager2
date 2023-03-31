from enum import Enum  # for enum34, or the stdlib version
import logging
from typing import Optional, Set, List, Tuple
from src.localization.programm_config import KEY_OF_EMPTY_RECIPE


class DataType(Enum):
    """ NUMBER ist a Integer or Floating Point Number (supports operators e.g. smaller)
    STRING is an arbitrary text
    BOOL Only True or False
    VOID None Value
    TIME Number + Duration_prefix e.g 5h or 10min (supports operators e.g. smaller)
    Path is a hierarchical string e.g Asian/Indian
    """
    NUMBER, STRING, BOOL, HIERARCHICAL_BOOL, DURATION = range(5)


def get_all_children_recursively(tag) -> Set:
    ret = set()
    for c in tag.children:
        ret = ret.union(get_all_children_recursively(TagManager.get_tag(c)))
    return ret

class Tag:
    """Settings for tag. Every used tag need these settings"""

    def __init__(self, name: str, kargs):
        # Data type
        assert "data_type" in kargs, "Every tag needs a data type " + name
        self._data_type = kargs.get("data_type", DataType.HIERARCHICAL_BOOL)
        # A unique id for the tag
        self._name = name
        # A Shortcut which helps in the search field e.g -v for vegetarian
        self._search_shortcut = kargs.get("search_shortcut", None)
        # The color of the tag
        self._color = kargs.get("color", None)
        # parent tags define a subset here, which is used in the search
        self._children = kargs.get("children", list())
        # Display name
        assert "display_name" in kargs, "No display name set for tag " + name
        self._display_name = kargs.get("display_name", None)
        assert "render_priority" in kargs, "No render_priority defined in " + name
        self._render_priority = kargs.get("render_priority", None)
        self._data_type_args = kargs.get("data_type_args", {})
        # Default value
        assert "default_value" in kargs, "No default value set for tag " + name
        self._default_value = kargs.get("default_value", None)
        # Is a keyword tag
        self._keyword = kargs.get("_is_keyword", False)

        self._parent = None
        # Check for options, which are no longer used
        assert "parent" not in kargs, "The parent parameter is set automatically. Don't set in manually. " + name

        # Read only options
        self._read_only = kargs.get("read_only", kargs.get("read_only", False))

    @property
    def read_only(self):
        return self._read_only

    @property
    def data_type_args(self):
        return self._data_type_args

    @property
    def render_priority(self) -> Optional[int]:
        """If None is set. Then the property should not be rendered"""
        return self._render_priority

    @property
    def keyword(self) -> bool:
        return self._keyword

    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def default_value(self):
        """Return type depends of data type"""
        return self._default_value

    @property
    def data_type(self) -> DataType:
        return self._data_type

    @property
    def render_priority(self) -> Optional[int]:
        return self._render_priority

    @property
    def name(self) -> str:
        return self._name

    @property
    def search_shortcut(self) -> Optional[str]:
        return self._search_shortcut

    @property
    def color(self) -> str:
        return self._color

    @property
    def children(self) -> Set[str]:
        return self._children

    @property
    def parent(self):
        return self._parent


class TagManager:
    _bool_need_init = True
    _all_tags = {}
    # Includes all tags begin with app:
    _reserved_keywords = {"format-version", "root", "name", "tags", "header", "ingredients", "ingredient", "method",
                          "random", "all",
                          "b", "i", "u", "h1", "h2", "h3", "h4"}
    _search_shortcuts = set()

    _search_columns: List[str] = []

    @staticmethod
    def need_init() -> bool:
        return TagManager._bool_need_init

    @staticmethod
    def init_complete():
        assert TagManager._bool_need_init, "You should not call this method twice."
        TagManager._bool_need_init = False

    @staticmethod
    def is_tag_name_a_keyword(name: str) -> bool:
        return name in TagManager._reserved_keywords

    @staticmethod
    def set_search_columns(search_columns: List[str]):
        assert len(search_columns) > 0, "To few columns"
        # Validate all columns
        for entry in search_columns:
            tag_name: str = entry
            if tag_name != "name":
                assert tag_name in TagManager._all_tags, "Unknown tag for table heading"
        # Set columns
        TagManager._search_columns = search_columns
        # Create default tag name
        # Its read only use the rename in the menu to change it
        TagManager._create_keyword_tag("name", data_type=DataType.STRING,
                                       display_name="Name", default_value=KEY_OF_EMPTY_RECIPE, render_priority=0, read_only=True)
        # The all tag is set in every recipe
        TagManager._create_keyword_tag("all", data_type=DataType.HIERARCHICAL_BOOL,
                                       display_name="", default_value=False, render_priority=None)
        TagManager._create_keyword_tag("random", data_type=DataType.NUMBER,
                                       display_name="", default_value=False, render_priority=None)
        # For search in the ingredient list
        TagManager._create_keyword_tag("ingredient", data_type=DataType.STRING,
                                       display_name="", default_value="", render_priority=None)

    @staticmethod
    def get_search_columns() -> List[Tuple[str, str, str]]:
        """Tag name -> display name, default_value (if tag is not set)"""
        assert not TagManager._bool_need_init, " Strong state."
        return TagManager._search_columns

    @staticmethod
    def is_valid_tag_name(name: str) -> bool:
        # If reserved keyword or has the app prefix than is the tag not valid
        if name in TagManager._reserved_keywords or name.startswith("app:"):
            logging.error("tag name is a reserved keyword %s", name)
            return False
        if name in TagManager._all_tags or name in TagManager._search_shortcuts:
            logging.error("tag already defined %s", name)
            return False
        return True

    @staticmethod
    def get_tag(name: str) -> Optional[Tag]:
        #assert not TagManager._bool_need_init, " Strong state: " + str(TagManager.need_init())
        return TagManager._all_tags.get(name, None)

    @staticmethod
    def get_all_tags() -> Set[str]:
        """Get all tags without search shortcuts"""
        #assert not TagManager._bool_need_init, " Strong state: " + str(TagManager.need_init())
        assert len(TagManager._all_tags) != 0, "No Tags defined"
        return set(TagManager._all_tags.keys()).difference(TagManager._search_shortcuts)

    @staticmethod
    def create_tag(name: str, **kargs):
        assert TagManager._bool_need_init," Wrong state."
        assert "_is_keyword" not in kargs, "The end user should not define own keyword tags"
        # Create tag
        tag: Tag = Tag(name, kargs)
        # Check if name are valid
        # print(tag.name," ",tag.search_shortcut)
        assert TagManager.is_valid_tag_name(tag.name), "Tag name is not valid " + name

        if tag.search_shortcut:
            assert TagManager.is_valid_tag_name(tag.search_shortcut), "Search shortcut for " + name + " is not valid"
            # Save tag also as search shortcut
            TagManager._all_tags[tag.search_shortcut] = tag
        # Add Tag and search shortcut if defined
        logging.info("Create Tag: %s", tag.name)
        TagManager._all_tags[tag.name] = tag
        if tag.search_shortcut is not None:
            TagManager._search_shortcuts.add(tag.search_shortcut)

    @staticmethod
    def _create_keyword_tag(name: str, **kargs):
        """Never use a user this function for creating tags"""
        assert TagManager._bool_need_init, " Strong state: " + str(TagManager.need_init())
        kargs["_is_keyword"] = True
        assert "_is_keyword" in kargs, "Not a keyword tag"
        # Create tag
        tag: Tag = Tag(name, kargs)

        # Add Tag and search shortcut if defined
        TagManager._all_tags[tag.name] = tag
        if tag.search_shortcut is not None:
            TagManager._search_shortcuts.add(tag.search_shortcut)

    @staticmethod
    def create_parent_edges():
        assert TagManager._bool_need_init, " Strong state: " + str(TagManager.need_init())
        # Sort by render priority
        def sort_by_render_priority(key):
            tag = TagManager.get_tag(key)
            assert tag is not None, "Invalid tag: " + key
            if tag.render_priority is None:
                return 100000
            else:
                return tag.render_priority

        for tag_name in TagManager.get_all_tags():
            tag = TagManager.get_tag(tag_name)
            tag._children = sorted(tag.children, key=sort_by_render_priority, reverse=False)
            for children in tag.children:
                # Add parent edges
                TagManager.get_tag(children)._parent = tag_name

    @staticmethod
    def auto_fill_void_tag_args():
        assert TagManager._bool_need_init, " Strong state: " + str(TagManager.need_init())
        def get_display_name(name):
            return TagManager.get_tag(name).display_name

        def get_children(name: str):
            return TagManager.get_tag(name).children

        def get_parent(name: str):
            return TagManager.get_tag(name).parent

        for tag_name in TagManager.get_all_tags():
            tag: Tag = TagManager.get_tag(tag_name)
            if tag.data_type == DataType.HIERARCHICAL_BOOL:
                tag.data_type_args["key"] = tag.name
                tag.data_type_args["get_parent"] = get_parent
                tag.data_type_args["get_children"] = get_children
                tag.data_type_args["get_display_name"] = get_display_name
