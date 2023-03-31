from abc import ABC, abstractmethod
from typing import Tuple, Optional

class IGtkDokumentManager(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def set_window_title(self):
        pass
    @abstractmethod
    def request_new_recipe_name(self) -> Tuple[Optional[str],bool]:
        pass


    @abstractmethod
    def dialog_save_unsaved_changes(self, key: str) -> bool:
        pass