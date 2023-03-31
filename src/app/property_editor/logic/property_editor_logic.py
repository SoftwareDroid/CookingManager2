from src.app.property_editor.logic.i_property_editor_logic import IPropertyEditor
from src.app.property_editor.gui.editor_recipes.i_gui_property_editor import IGUIPropertyEditor
from src.app.share.tag_manager import TagManager
from src.localization.my_tags import tags_init
from typing import Dict, Any
from src.app.share.engine.i_logic_part import ILogicPart

class PropertyEditorLogic(IPropertyEditor,ILogicPart):
    def __init__(self):
        self.signals_in: IPropertyEditor = self
        self.signals_out: IGUIPropertyEditor = None

    def initialize(self):
        if TagManager.need_init():
            tags_init()

        #self.signals_out.load_template("default")

    def export_state(self) -> Dict[str, Any]:
        # Forward method call
        return self.signals_out.export_state()

    def import_state(self, state: Dict[str, Any]):
        # Forward method call
        self.signals_out.import_state(state)

    def load_template(self, name: str):
        """Use this as a clear operation"""
        self.signals_out.load_template(name)
