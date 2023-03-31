from abc import abstractmethod
from src.app.text_editor.editor_generic.i_transform_tag import ITagTransform
from typing import Tuple,Sequence
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ITransformerRange(ITagTransform):
    @abstractmethod
    def initialise(self, old_text: str, arg: Tuple[Gtk.TextBuffer, int, int]):
        """
        :param old_text: the text, which can be changed
        :param arg: access to the buffer and the begin and end index of old_text in the buffer
        """
        pass

    @abstractmethod
    def get_replacement_text(self) -> Tuple[str,Sequence[Tuple[str,int,int]]]:
        """
        :return: replacement_string, Sequence of tags, which are applied after the replacement
        """
        pass

    @abstractmethod
    def event_after_replacement(self): pass