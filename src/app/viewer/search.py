from src.app.documents.logic.dokument_manager_logic import DokumentManagerLogic, IDocumentManagerLogic, Recipe
from src.app.share.pyleri_tree import view_parse_tree
from typing import Set, Tuple
from multiprocessing import Pool
from enum import Enum
from src.app.share.tag_manager import TagManager, Tag, DataType
from typing import List
from typing import Tuple as TupleType
from src.app.viewer.searcher_grammar import _SearchGrammar
from distutils.util import strtobool
import logging
from src.app.viewer.tag_search import _Match, _search_with_recipe_name, _search_with_ingredients, \
    _number_tag_search, _duration_tag_search, _string_tag_search, _tag_void_search, bool_tag_search, \
    DEFAULT_BOOL_OPERATION, _search_random_recipe

import re


# Init all own tags
# tags_init()


class _CombineSearchResults(Enum):
    AND = 0
    OR = 1
    OR_NOT = 2
    AND_NOT = 3


class Searcher:
    def __init__(self, respository: IDocumentManagerLogic):
        # Set global variable for pool package
        global source
        source = respository
        # Create a thread pool
        self._pool = Pool()
        self._source: IDocumentManagerLogic = respository
        self._simple_search_regex = re.compile(r'[^\"\':]+$')
        self._grammar = _SearchGrammar()

    def _try_simplified_search(self, query: str) -> str:
        if self._simple_search_regex.match(query) is not None:
            return f"name: '{query}' or ingredient: '{query}'"
        else:
            # Its not a simple search try advanced
            return query

    """ For a search in a recipe respository"""

    def search(self, query: str) -> TupleType[List[Recipe]]:
        """Returns a list of recipe of keys for a query and a string which indicates errors"""
        # Try a simpler search form without colon or quotes in name and ingredients
        query2 = self._try_simplified_search(query)
        import json
        result = self._grammar.parse(query2)
        if result.is_valid:
            tree = view_parse_tree(result)
            result = self._parse_start_symbol(tree)
            # Filter no hits out and sort result
            return [x[0] for x in Searcher._sort_search_result(result) if x[1] != _Match.NO_MATCH]
        else:
            logging.warning("Could not parse search query: " + query2)
            # Show query if input is changed
            if query != query2:
                raise Exception("Query {} is NOT valid. After {}".format(query,
                                                                         result.tree.string[:result.pos]))
            else:
                raise Exception('Query is NOT valid. After "{}"'.format(
                    result.tree.string[:result.pos]))

    @staticmethod
    def _sort_search_result(result: List[Tuple[Recipe, _Match]]) -> List[Tuple[Recipe, _Match]]:
        def _order_by_match(arg: Tuple[Recipe, _Match]):
            # Sort by match and name of the recipe
            assert len(arg) == 2, "Wrong Parameter"
            return arg[1].value, arg[0].name

        # Sort descending higher matches shall be at front
        result.sort(key=_order_by_match, reverse=True)
        return result

    def _parse_start_symbol(self, node):

        repeat_node = node
        assert repeat_node["element"] == "Repeat", "Wrong grammar assumption."
        first_op_part = True
        for op_part in repeat_node["children"]:
            if first_op_part:
                first_op_part = False
                current_result, _ = self._process_optional_part(op_part)
            else:
                # Start a search with a tag
                search_result, bool_op = self._process_optional_part(op_part)
                # Combine result with previous result
                current_result = self._combine_search_results(current_result, search_result, bool_op)
        return current_result

    @staticmethod
    def _extract_from_quoted_string(text: str) -> str:
        # A text with length one is never a quoted string
        assert len(text) >= 2, "not a quoted string"
        assert text[0] == text[-1] and (text[0] == '"' or text[0] == "'"), "not a quoted string"

        if len(text) == 2:
            return ""
        elif len(text) == 3:
            return text[1]
        else:
            # Remove first and last char
            return text[1:len(text) - 1]

    def _process_first_part(self, node):
        # The first part consist only of the string
        assert node["name"] == "first_part", "Grammar Error"
        node = node["children"][0]
        # Extract search string
        if node["name"] == "word_without_quotes":
            search_text = node["string"]
        else:
            search_text = Searcher._extract_from_quoted_string(node["children"][0]["string"])

        # Examine all recipe names
        all_recipes: Set[Recipe] = self._source.get_all_recipes()
        work = zip([search_text] * len(all_recipes), all_recipes)
        name_search_result = self._pool.map(_search_with_recipe_name, work)
        # Refill work and search in ingredients
        work = zip([search_text] * len(all_recipes), all_recipes)
        ingredient_search_result = self._pool.map(_search_with_ingredients, work)

        # Search for tag
        result = Searcher._combine_search_results(name_search_result, ingredient_search_result, DEFAULT_BOOL_OPERATION)
        return result

    @staticmethod
    def _combine_search_results(result1: List[Tuple[Recipe, _Match]], result2: List[Tuple[Recipe, _Match]],
                                method: str) -> List[Tuple[Recipe, _Match]]:
        """ Combine two result lists with a boolean operation"""
        ret = []
        # Map recipe key to (recipe, search_result)

        if len(result1) != len(result2):
            raise Exception("Omit partial search result")

        for n in range(len(result1)):
            assert result1[n][0].key == result2[n][0].key, "Cannot combine results list because no match."
            match1: _Match = result1[n][1].value
            match2: _Match = result2[n][1].value

            # Use Python boolean logic to determine the result
            if method == "or":
                has_result = (bool(match1) or bool(match2))
            elif method == "and":
                has_result = (bool(match1) and bool(match2))
            elif method == "and not":
                has_result = (bool(match1) and not bool(match2))
            elif method == "or not":
                has_result = (bool(match1) or not bool(match2))
            else:
                assert False, "Invalid method for combining results."

            if has_result:
                # Take better result if there
                ret.append((result1[n][0], _Match(max(match1, match2))))
            else:
                ret.append((result1[n][0], _Match.NO_MATCH))
        return ret

    @staticmethod
    def _get_tag_value_inner_node(value):
        """Get Node with the value"""
        if value is None:
            return None
        else:
            # Navigate optional tag
            part_value = value["children"][0]
            # Get Node with the concrete value
            inner_node = part_value["children"][0]
            return inner_node

    def _parse_tag_with_value(self, tag: Tag, value) -> List[Tuple[Recipe, _Match]]:
        """ Executes a search with a single tag"""

        # Check for correct data type
        data_type = Searcher._get_tag_value_inner_node(value)
        if tag.data_type == DataType.HIERARCHICAL_BOOL:
            result = self._search_void_tag(tag, data_type)
        elif data_type["name"] == "value_number":
            result = self._search_number_tag(tag, data_type)
        elif data_type["name"] == "value_boolean":
            result = self._search_bool_tag(tag, data_type)
        elif data_type["name"] == "value_duration":
            result = self._search_duration_tag(tag, data_type)
        elif data_type["name"] == "string":
            result = self._search_string_tag(tag, data_type)
        else:
            # Change grammar in case of error
            assert False, "Grammar Error: not handled tag data type in search."

        return result

    def _search_string_tag(self, tag: Tag, value) -> List[Tuple[Recipe, _Match]]:
        if tag.data_type != DataType.STRING:
            raise Exception(
                "Invalid data type for tag '{}' should be a quoted string e.g {}: 'warm'".format(tag.name, tag.name))

        search_value: str = Searcher._extract_from_quoted_string(value["string"])
        # Start search
        all_recipes: Set[Recipe] = self._source.get_all_recipes()
        # Handle ingredient tag
        if tag.keyword and tag.name == "ingredient":
            work = zip([search_value] * len(all_recipes), all_recipes)
            string_search_result = self._pool.map(_search_with_ingredients, work)
        else:
            work = zip([tag.name] * len(all_recipes), all_recipes, [search_value] * len(all_recipes))
            string_search_result = self._pool.map(_string_tag_search, work)
        return string_search_result

    @staticmethod
    def _extract_number_and_operator(value):
        """Extract the value and number from a tag"""
        # Extract operator and number
        if len(value["children"]) == 2:
            operator = value["children"][0]["string"]
            number = float(value["children"][1]["string"])
        else:
            # Default operator if none is used
            operator = "="
            # No operator defined so number is first child
            number = float(value["children"][0]["string"])
        return operator, number

    def _search_duration_tag(self, tag: Tag, value) -> List[Tuple[Recipe, _Match]]:
        if tag.data_type != DataType.DURATION:
            raise Exception("Expected something like < 2 h after {}:".format(tag.name))

        comparator, number = Searcher._extract_number_and_operator(value["children"][0])
        time_unit = value["children"][1]["children"][0]["name"]
        # Start search
        all_recipes: Set[Recipe] = self._source.get_all_recipes()
        work = zip([tag.name] * len(all_recipes), all_recipes, [(comparator, number, time_unit)] * len(all_recipes))
        duration_search_result = self._pool.map(_duration_tag_search, work)
        return duration_search_result

    def _search_number_tag(self, tag: Tag, value) -> List[Tuple[Recipe, _Match]]:
        """Search for a tag of type float"""
        if tag.data_type != DataType.NUMBER:
            raise Exception("Expected a number after {}:".format(tag.name))

        comparator, number = Searcher._extract_number_and_operator(value)

        all_recipes: Set[Recipe] = self._source.get_all_recipes()
        if tag.keyword and tag.name == "random":
            from random import sample
            # Build a set of unique recipe keys
            random_recipe_keys: Set[str] = {x.key for x in sample(all_recipes, int(number))}
            work = zip(all_recipes, [random_recipe_keys] * len(all_recipes))
            number_search_result = self._pool.map(_search_random_recipe, work)
        # Start search
        else:
            work = zip([tag.name] * len(all_recipes), all_recipes, [(comparator, number)] * len(all_recipes))
            number_search_result = self._pool.map(_number_tag_search, work)
        return number_search_result

    def _search_void_tag(self, tag: Tag, value) -> List[Tuple[Recipe, _Match]]:
        """Search for a tag of type VOID"""
        if value is not None or tag.data_type != DataType.HIERARCHICAL_BOOL:
            raise Exception("Expected no value after {}:".format(tag.name))
        else:
            all_recipes: Set[Recipe] = self._source.get_all_recipes()
            work = zip([tag.name] * len(all_recipes), all_recipes)
            void_search_result = self._pool.map(_tag_void_search, work)
            return void_search_result

    def _search_bool_tag(self, tag: Tag, value) -> List[Recipe]:
        """Search for a tag of type boolean"""
        if tag.data_type != DataType.BOOL:
            raise Exception("Expected a boolean after {}:".format(tag.name))

        # Extract bool from search query
        search_bool: bool = bool(strtobool(value["string"]))
        # Start search
        all_recipes: Set[Recipe] = self._source.get_all_recipes()
        work = zip([tag.name] * len(all_recipes), all_recipes, [search_bool] * len(all_recipes))
        bool_search_result = self._pool.map(bool_tag_search, work)
        return bool_search_result

    def _process_optional_part(self, node) -> Tuple[List[Tuple[Recipe, _Match]], str]:
        """Returns search result, Boolean operation"""
        # Get Bool Operation if there

        bool_operation: str = DEFAULT_BOOL_OPERATION
        index_of_identifier = 0
        # There have to be a least one node
        start_node = node["children"][0]

        # Found the optional bool node
        if start_node["element"] == "Optional":
            bool_operation = start_node["string"]
            # Identifier node is at the next position
            index_of_identifier = 1
        # Parse Identifier and omit the colon at the end
        tag_idenifier: str = node["children"][index_of_identifier]["string"][:-1]
        tag = TagManager.get_tag(tag_idenifier)
        # Check if tag is defined
        if tag is None:
            raise Exception("Unknown tag: {}".format(tag_idenifier))

        # Get optional value
        if len(node["children"]) == index_of_identifier + 2:
            value_node = node["children"][index_of_identifier + 1]
        else:
            value_node = None

        # Parse Tag
        return self._parse_tag_with_value(tag, value_node), bool_operation
