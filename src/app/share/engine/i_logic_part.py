from abc import ABC, abstractmethod
from typing import Type, Optional

class ILogicPart(ABC):
    def __init__(self):
        pass

    def get_addon(self,addon_logic_type) -> Optional[object]:
        pass

    @abstractmethod
    def initialize(self):
        pass