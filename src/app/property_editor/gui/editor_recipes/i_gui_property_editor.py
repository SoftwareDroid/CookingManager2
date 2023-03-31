from abc import ABC, abstractmethod
from typing import Dict,Any

class IGUIPropertyEditor(ABC):
    @abstractmethod
    def load_data(self, data: Dict[str, Any]):
        pass

    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def load_template(self, name: str):
        pass

    @abstractmethod
    def set_mode(self,read_only: bool):
        """Make all properties read only"""
        pass

    @abstractmethod
    def import_state(self, state: Dict[str, Any]):
        pass

    @abstractmethod
    def export_state(self) -> Dict[str,Any]:
        pass