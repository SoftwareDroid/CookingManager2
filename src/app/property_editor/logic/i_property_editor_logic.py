from abc import ABC, abstractmethod
from typing import Dict, Any

class IPropertyEditor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def export_state(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def import_state(self, state: Dict[str, Any]):
        pass

    @abstractmethod
    def load_template(self, name: str):
        pass