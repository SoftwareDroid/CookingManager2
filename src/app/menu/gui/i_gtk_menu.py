from abc import ABC, abstractmethod


class IGtkMenu(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def show_error_dialog(self, title: str, message: str):
        pass
