from pyleri import Choice
from pyleri import Grammar
from pyleri import Keyword
from pyleri import Regex
from pyleri import Repeat
from pyleri import Sequence
from pyleri import Optional
from pyleri import Token
from typing import Optional as TypeOpt  # Rename Optional because it is always defined
from src.app.share.pyleri_tree import view_parse_tree
import xml.etree.ElementTree as ET
from typing import List,Tuple
from typing import Sequence as SequenceType
from src.app.share.recipe import Ingredient


# Returns properties of a node object as a dictionary:


##Key Value Paare Name, Type, Rating, Cuisine, Tags, has_tried, duration

# Create a Grammar Class to define your language
class MyGrammar(Grammar):
    # Verschiedne Zahlen darstellungen
    t_float = Regex("\d*\.\d+|\d+")
    t_fraction = Regex("\d+/\d+")
    # Nach einer Zhal folgt optional ein Whitspace
    Number = Choice(t_float, t_fraction)
    # Imperiale und metrische Einheiten dies müssen Keywords sein damit sie erkannt werden (vorrang)
    UnitCup = Sequence(Choice(Keyword("c"), Keyword("cups")), Regex(r"\.?"))
    # EL german = Esslöfel
    UnitTbs = Sequence(
        Choice(Keyword("T"), Keyword("tablespoons"), Keyword("tbsp"), Keyword("tbsps"), Keyword("Tb"), Keyword("EL")),
        Regex(r"\.?"))
    # TL german = Teelöfel
    UnitTsp = Choice(Keyword("t"), Keyword("teaspoons"), Keyword("tsp"), Keyword("TL"))
    UnitInch = Choice(Keyword("inch"), Keyword("in"), Token("''"))
    UnitCm = Keyword("cm")
    UnitGram = Keyword("g")
    UnitKg = Choice(Keyword("Kg"), Keyword("kg"))
    UnitLiter = Choice(Keyword("l"), Keyword("liter"))
    UnitMilliLiter = Choice(Keyword("ml"))
    # Nach jeder Einheit muss ein Whitespace folgen
    Unit = Choice(UnitCup, UnitTbs, UnitTsp, UnitInch, UnitCm, UnitGram, UnitKg, UnitLiter, UnitMilliLiter)
    # Zutat darf nicht mit einer Zahl beginnen und darf sich nicht über mehrere Zeilen erstecken
    IngredientName = Regex(r'[^\n0-9][^\n]*')
    # Ein Zeile pro Zutat hat eine Zahl und Einheit als Optionale Bestandteile
    IngredientLine = Sequence(Optional(Number), Optional(Unit), IngredientName)

    # Eine Menge aus Zutatenzeilen
    START = Repeat(IngredientLine, mi=1)


my_grammar = MyGrammar()


def ingredient_list_to_normalized_text(ingredients:  List[Ingredient]) -> str:
    text: str = ""
    for ingredient in ingredients:
        text += ingredient.as_readable_string() + "\n"
    # Remove last new line in string
    return text[:-1]

def text_to_ingredient_list(text: str) -> List[Ingredient]:
    res = my_grammar.parse(text)
    # Parsen ist Fehlgeschlagen gebe None zurück.

    if not res.is_valid:
        return None
    # Wandele die parse tree erst mal in einen normal Python Datenstrutkur um
    tree = view_parse_tree(res)
    def interpret_ingredient(line, root: List[Ingredient]):
        children = line["children"]
        # Die letzte Variable jeder Produktion ist immer der Zutatenname
        ingredient_name: str = children[len(children) - 1]["string"]
        unit_name = None
        factor_name = None
        if len(children) > 1:
            for n in range(0, len(children) - 1):
                # Interpret Unit and Factor
                tmp = interpret_unit(children[n]["children"][0])
                if tmp is not None:
                    unit_name = tmp
                tmp = interpret_ingredient_factor(children[n]["children"][0])
                if tmp is not None:
                    factor_name = tmp

                # Append Ingredient
        root.append(Ingredient(ingredient_name,unit_name,factor_name))
    def interpret_unit(unit_tag) -> str:
        if unit_tag["name"] != "Unit":
            return
        unit_as_str = unit_tag["children"][0]["name"]
        return unit_as_str

    def interpret_ingredient_factor(factor_tree) -> str:
        if factor_tree["name"] != "Number":
            return None
        return factor_tree["string"]

    def interpret_start_symbol(full_tree, root: List[Ingredient]):
        assert full_tree["name"] == "START", "Not the start symobl at tree root"
        for line in full_tree["children"]:
            interpret_ingredient(line, root)
        return root

    return interpret_start_symbol(tree,[])


