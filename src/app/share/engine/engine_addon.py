from abc import ABCMeta, abstractmethod, ABC
from src.app.share.engine.i_logic_part import ILogicPart
from src.app.share.engine.i_gui_part import IGUIPart

class EngineAddon(ABC):
    def __init__(self, logic, gui):
        self.logic = logic
        self.gui = gui

    def init_gtk_gui(self, builder):
        # Set Properties in gui
        self.gui.builder = builder


    def connect_logic_and_gui(self):
        # Connect logic -> gui
        assert self.gui.signals_in is not None, "GUI: Missing Signals Signals should always point to self" + self.gui
        assert self.logic.signals_in is not None, "Logic: Missing Signals Signals should always point to self"
        assert isinstance(self.logic, ILogicPart), " The logic of the addon doesn't implement ILogicPart " + str(self.logic)
        assert isinstance(self.gui,IGUIPart), " The gui of the addon doesn't implement IGUIPart " + str(self.gui)
        self.logic.signals_out = self.gui.signals_in
        self.gui.signals_out = self.logic.signals_in
        self.gui.initialize()

