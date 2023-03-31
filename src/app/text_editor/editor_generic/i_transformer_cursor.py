from abc import abstractmethod
from src.app.text_editor.editor_generic.i_transform_tag import ITagTransform
from typing import Tuple,Sequence

class ITransformerCursor(ITagTransform):
    @abstractmethod
    def apply(self,cursor_pos:int, buffer) -> Tuple[str, str]:
        """return [insert_text,apply_tag]"""
        pass
