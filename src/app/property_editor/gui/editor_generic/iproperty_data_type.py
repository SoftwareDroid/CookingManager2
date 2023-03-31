from abc import abstractmethod, ABC

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class IPropertyDataType(ABC):
    @abstractmethod
    def create_cell(self, args) -> Gtk.Widget:
        """Creates a Widget, which represent the cell content."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """e.g return type(bool), than is is Property used for every bool"""
        pass

    @abstractmethod
    def set_activ(activ: bool):
        pass

    def set_key(self, key):
        self.key = key

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def signal_change(self):
        pass

    @abstractmethod
    def set_cell_value(self, value):
        pass
