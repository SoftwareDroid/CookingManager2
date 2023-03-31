# Interface welches die GUI Methoden vorschreibt
from abc import abstractmethod, ABC

class ITagTransform(ABC):
    @abstractmethod
    def get_label(self) -> str: pass

    @abstractmethod
    def hide_from_context_menu(self):
        pass