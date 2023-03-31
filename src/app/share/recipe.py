from typing import Sequence, Optional, Any
import logging
# Own imports
from src.app.share.tag_manager import TagManager
#from src.app.documents.logic.dokument_manager_logic import DokumentManagerLogic, IDocumentManagerLogic
from typing import Tuple, List
from src.localization.units import Unit
from src.core.hash import hash_sum_of_file
from fpdf import FPDF, HTMLMixin


class MyFPDF(FPDF, HTMLMixin):
    pass


class Ingredient:
    """ A ingredient consist of a name and a factor with a unit e.g. 2 T Salt"""

    def __init__(self, name: str, unit: Optional[str], amount: float):
        """
        :type amount: object
        """
        self._name = name
        self._unit = unit
        self._amount = amount

    @property
    def name(self):
        """Name of the ingredient"""
        return self._name

    @property
    def amount(self):
        """Ingredient factor"""
        return self._amount

    @property
    def unit(self):
        """NONE if not set"""
        return self._unit

    def as_readable_string(self) -> str:
        # Build unit a string
        unit_str = ""
        if self.unit is not None:
            unit_str = Unit.get_unit(self.unit).to_str(self.amount)
        else:
            unit_str = " "
        # Omit amount if not set
        amount_str = str(self.amount)
        if self.amount is None:
            amount_str = ""
        result = amount_str + unit_str + self.name
        # Trim away leading and following spaces
        return result.strip()


class Recipe:
    """The representation of recipe (only data)
    Only the display name, file-format are mandatory entries in the file"""

    def __init__(self, key: str, json_data):
        self._tags = {}
        self._ingredients = []
        # Save unique id
        self._key = key
        self._parse_json(json_data)

    def _parse_json(self, json_data):
        # Parse Header
        header = json_data["header"]
        assert header['format-version'] == "2", " Wrong format of recipe file"
        hash_of_my_tags = hash_sum_of_file("src/localization/my_tags.py")
        if header['sha256_my_tags'] != hash_of_my_tags:
            logging.warning("Another src/localization/my_tags.py file was used for the recipe %s ", self._key)
        if self.key not in header['filename']:
            logging.warning("The file name of %s didn't match with entry in the header", self._key)
        # Parse Body
        body = json_data["body"]
        self._method = body["editor-state"]
        self._tags = body["properties-state"]



    @property
    def method(self) -> Tuple[str, List[Tuple[str, int, int]]]:
        """Returns the cooking method (plaintext, list of annotations)
        annotation = (tag_name, start, end)"""
        return self._method

    @property
    def ingredients(self) -> Sequence[Ingredient]:
        """Returns a list of ingredients for the recipe"""
        return self._ingredients

    @property
    def name(self) -> str:
        """The displayed name of the recipe"""
        return self._name

    @property
    def key(self) -> str:
        """A unique id for the recipe"""
        return self._key

    def get_tag_value(self, name: str) -> Any:
        """The tags are only saved as simple strings"""
        if name in self._tags:
            return self._tags[name]
        return None

    def has_tag(self, name: str) -> bool:
        return name in self._tags

    def get_all_tags(self):
        return self._tags

    def has_tag(self, name: str) -> bool:
        """Checks if a tag is set in the recipe"""
        return name in self._tags
