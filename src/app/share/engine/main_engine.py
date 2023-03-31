import logging
from src.app.share.engine.engine_addon import EngineAddon
from src.gui.share.gui_share import GUIGTK
from typing import Type

class MainEngine:
    def __init__(self):
        self.gui = GUIGTK()
        self.addons = {}

    def add_addon(self, addon: EngineAddon):
        addon.init_gtk_gui(self.gui.builder)
        addon.connect_logic_and_gui()
        self.addons[type(addon.logic)] = addon
        addon.logic.get_addon = self.get_addon

    def get_addon(self, logic: Type):
        return self.addons[logic]


    def init_after_gui_run(self):
        for addon_key in self.addons:
            self.addons[addon_key].logic.initialize()


    def run(self):
        logging.info("Start main Engine")
        self.gui.run(self.init_after_gui_run)


# ADDON.signals_in is a reference normally set to self for receiving incoming signals
# ADDON.signals_out is a reference for sending signals. This reference is set automatically.
# Logic has access to get_addon function