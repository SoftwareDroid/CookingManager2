from typing import Tuple, List, Dict
from src.app.text_editor.editor_generic.i_transformer_range import ITransformerRange

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TransformerHeading2(ITransformerRange):

    def initialise(self, old_text: str, arg: Tuple[Gtk.TextBuffer, int, int]):
        self.old_text = old_text
        self.arg = arg

    def get_replacement_text(self) -> Tuple[str, List[Tuple[str, int, int]]]:
        return self.old_text,[]

    def hide_from_context_menu(self):
        return False

    def get_label(self) -> str:
        return "Format Heading 1"

    def event_after_replacement(self):
        pass

    def is_deletable(self) -> bool:
        return True
