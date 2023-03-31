from abc import ABC, abstractmethod

class IMenuLogic(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def event_save(self):
        pass

    @abstractmethod
    def event_file_open(self, path: str):
        pass

    @abstractmethod
    def event_file_new(self):
        pass

    @abstractmethod
    def event_rename_current_recipe(self):
        pass