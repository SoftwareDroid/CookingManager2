from abc import ABC, abstractmethod

class GUISignalsImporter(ABC):

    def __init__(self, igui):
        self.igui = igui
        super().__init__()

    @abstractmethod
    def import_change_recipe_name(self, name: str): pass

    @abstractmethod
    def importer_press_import(self): pass

    @abstractmethod
    def importer_change_method(self, text: str): pass

    @abstractmethod
    def importer_change_ingredientlist(self, text: str): pass

    # Render alternately the recipe in normal oder as xml
    @abstractmethod
    def importer_change_preview_render_mode(self, xml_mode: bool): pass

    @abstractmethod
    def event_gui_init_finished(self): pass