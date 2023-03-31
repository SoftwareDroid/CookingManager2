from src.gui.viewer.gui_signals_viewer import GUISignalsViewer
from src.app.share.recipe import Recipe
from src.app.viewer.search import Searcher
from src.gui.viewer.gui_viewer_gtk import IGUIViewer
from src.app.share.engine.i_logic_part import ILogicPart
from src.app.documents.logic.dokument_manager_logic import DokumentManagerLogic, IDocumentManagerLogic
import logging




class LogicViewer(GUISignalsViewer, ILogicPart):
    def __init__(self):
        self._repository: IDocumentManagerLogic = DokumentManagerLogic.instance()
        self._searcher = Searcher(self._repository)
        self.signals_in: GUISignalsViewer = self
        self.signals_out: IGUIViewer = None
        logging.getLogger().setLevel(logging.DEBUG)

    def initialize(self):
        logging.info("Call event_gui_init_finished in LogicViewer")


    def event_search_for_recipes(self, search_text: str):
        logging.getLogger().info("Start search query for %s", search_text)
        try:
            result = self._searcher.search(search_text)
            self.signals_out.show_search_result(result)
            self.signals_out.show_message("Search successful")
        except Exception as exp:
            self.signals_out.show_error(str(exp))

    def event_select_recipe(self, recipe: Recipe):
        annotated_text = recipe.to_annotated_text()
        self.signals_out.show_rendered_preview(annotated_text[0], annotated_text[1])