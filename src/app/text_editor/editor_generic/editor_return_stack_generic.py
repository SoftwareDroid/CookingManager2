from abc import abstractmethod, ABC

from typing import Tuple, Sequence, List


class ReturnStack:
    class IReturnable(ABC):
        @abstractmethod
        def export_state(self) -> Tuple[str, Sequence[Tuple[str, int, int]]]: pass

        @abstractmethod
        def import_state(self, state: Tuple[str, Sequence[Tuple[str, int, int]]]): pass

    def __init__(self, max_return_steps: int, editor: IReturnable):
        self._max_return_steps: int = max_return_steps
        self._editor = editor
        self._stack: List[Tuple[str, Sequence[Tuple[str, int, int]]]] = []
        # Init stack pointer
        self._stack_pointer = -1
        assert self._max_return_steps >= 0 and self._max_return_steps <= 1024, "Invalid return step number"

    def do_button(self):
        assert self.can_do(), "Do action is not possible"
        # Move stack pointer
        self._stack_pointer += 1
        # Recover state
        self._editor.import_state(self._stack[self._stack_pointer])

    def can_do(self):
        return self._stack_pointer < (len(self._stack) - 1)

    def can_undo(self):
        return self._stack_pointer > 0

    def undo_button(self):
        assert self.can_undo(), "Undo action is not possible"
        # Move stack pointer
        self._stack_pointer -= 1
        # Recover state
        self._editor.import_state(self._stack[self._stack_pointer])

    def do_action(self):
        front: int = len(self._stack) - 1
        state = self._editor.export_state()

        if self._stack_pointer != front:
            # Throw away actions, if we override such in the past
            self._stack = self._stack[:self._stack_pointer + 1]
            assert self._stack_pointer == (len(self._stack) - 1), "Invalid Stack Pointer "

        self._stack.append(state)
        self._stack_pointer += 1

        if len(self._stack) > self._max_return_steps:
            self._stack.pop(0)
            self._stack_pointer -= 1

        assert self._stack_pointer < len(self._stack),"Invalid Stack Pointer"
        assert self._stack_pointer >= 0, "Invalid Stack Pointer"