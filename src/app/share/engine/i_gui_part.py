from abc import ABC, abstractmethod
from typing import Type, Optional

class IGUIPart(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def initialize(self):
        pass