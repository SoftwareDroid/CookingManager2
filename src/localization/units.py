# Singular, Plural, Name, Space after number
from typing import Optional
import logging

class Unit:
    _all_units = {}
    """Properties of a unit"""

    def __init__(self, key, **kwargs):
        self.key = key
        self.singular = kwargs["singular"]
        self.plural = self.singular
        # Use only singular if no plural is defined
        if "plural" in kwargs:
            self.plural = kwargs["plural"]
        # Default need space
        self.need_space = True
        if "need_space" in kwargs:
            self.need_space = kwargs["need_space"]
        # Register unit
        Unit._register_uint(self)

    def to_str(self, amount: Optional[float]) -> str:
        """Combines a unit with a number to a string"""
        name = ""
        try:
            from fractions import Fraction
            if amount is None or Fraction(amount) <= 1.0:
                name = self.singular
            else:
                name = self.plural
        except ZeroDivisionError:
            # Show a error in the output
            name = "<app:error>Division by Zero</app:error>"
        # Space
        space = ""
        if self.need_space:
            space = " "

        # Append number
        if amount is not None:
            name = space + name

        return name + " "

    @staticmethod
    def get_unit(key):
        assert key in Unit._all_units, "Error undefined unit"
        return Unit._all_units[key]

    @staticmethod
    def _register_uint(self):
        assert self.key not in Unit._all_units, "Unit already defined " + self.key
        Unit._all_units[self.key] = self


# Lets define some Units. Have to match the units in the ingredient parser
unit_cup = Unit("UnitCup", singular="cup", plural="cups", need_space=True)
unit_tbs = Unit("UnitTbs", singular="tbsp", plural="tbsps", need_space=True)
unit_teaspoon = Unit("UnitTsp", singular="tsp", plural="tsps", need_space=True)
unit_inch = Unit("UnitInch", singular="inch", need_space=True)
unit_cm = Unit("UnitCm", singular="cm", need_space=False)
unit_kg = Unit("UnitKg", singular="kg", need_space=False)
unit_gram = Unit("UnitGram", singular="g", need_space=False)
unit_ml = Unit("UnitMilliLiter", singular="ml", need_space=False)
