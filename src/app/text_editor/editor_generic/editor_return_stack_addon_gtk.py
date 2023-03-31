from src.app.text_editor.editor_generic.editor_return_stack_generic import ReturnStack
from typing import Tuple, Sequence
from src.localization.programm_config import EDITOR_NUMBER_OF_RETURN_STEPS

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class EditorReturnStackAddonGtk(ReturnStack.IReturnable):
    """enables to reverse actions"""

    def __init__(self, editor):
        self._editor = editor
        self._builder = self._editor.builder

        self.name_button_redo = "MenuRedo"
        self.name_button_undo = "MenuUndo"
        self.name_click_signal = "activate"

        # Setup do and undo stack
        do_button = self._builder.get_object(self.name_button_redo)
        do_button.connect(self.name_click_signal, self._press_do_button)
        undo_button = self._builder.get_object(self.name_button_undo)
        undo_button.connect(self.name_click_signal, self._press_undo_button)
        self._return_stack = ReturnStack(EDITOR_NUMBER_OF_RETURN_STEPS, self)
        self._update_return_stack_buttons()
        self._return_stack.do_action()

        # Connect to buffer modified signal
        text_buffer: Gtk.TextBuffer = self._builder.get_object(editor.editor_name).get_buffer()
        text_buffer.connect("end-user-action", self._on_end_user_action)

    def clear(self):
        # Throw away old Return stack and create a new one
        self._return_stack = ReturnStack(EDITOR_NUMBER_OF_RETURN_STEPS, self)
        self._update_return_stack_buttons()
        self._return_stack.do_action()

    def do_action(self):
        # Update return stack
        self._return_stack.do_action()
        self._update_return_stack_buttons()

    def _on_end_user_action(self, widget):
        self.do_action()

    def export_state(self) -> Tuple[str, Sequence[Tuple[str, int, int]]]:
        """Forward method call"""
        return self._editor.export_state()

    def import_state(self, state: Tuple[str, Sequence[Tuple[str, int, int]]]):
        """Forward method call"""
        self._editor.import_state(state)

    def _update_return_stack_buttons(self):
        do_button = self._builder.get_object(self.name_button_redo)
        do_button.set_sensitive(self._return_stack.can_do())
        undo_button = self._builder.get_object(self.name_button_undo)
        undo_button.set_sensitive(self._return_stack.can_undo())

    def _press_do_button(self, widget):
        if self._return_stack.can_do():
            self._return_stack.do_button()
            self._update_return_stack_buttons()

    def _press_undo_button(self, widget):
        if self._return_stack.can_undo():
            self._return_stack.undo_button()
            self._update_return_stack_buttons()
