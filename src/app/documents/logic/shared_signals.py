from typing import Callable
from src.app.documents.logic.dokument_manager_logic import DokumentManagerLogic
# This signals are in a separate file for preventing include circles
# This output of this signals is received from the document manager logic
recipe_changed_editor = lambda: DokumentManagerLogic.instance()._signal_recipe_changed_callback()
recipe_changed_properties = lambda: DokumentManagerLogic.instance()._signal_recipe_changed_callback()