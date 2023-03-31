from typing import Tuple, List, Dict, Set
from src.app.text_editor.editor_generic.i_transform_tag import ITagTransform
from abc import abstractmethod, ABC
from src.app.text_editor.editor_generic.i_transformer_range import ITransformerRange
from src.app.text_editor.editor_generic.i_transformer_cursor import ITransformerCursor

import gi
from typing import Callable

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class TagSupportAddonGTK(ABC):
    """Do not use this class directly inherit and override the three methods"""

    @abstractmethod
    def setup_my_transformer(self):
        """Creates all advanced transformer tags"""
        pass

    @abstractmethod
    def define_all_tags(self):
        """Defines all normal tags"""
        pass

    @abstractmethod
    def init_buttons(self):
        """Connects a button with a tag"""

    def get_recipe_name(self) -> str:
        return self.editor.get_recipe_name()

    def clear(self):
        # Throw away replacements
        self._transformer_to_old_replacement: Dict[str, List[Tuple[Gtk.TextMark, str]]] = {}

    def __init__(self, editor):
        # TODO 1. Tags dürfen nur auf editierbaren Text anbewendet werden
        # TODO 2. nicht Transformer werden über Buttons gesteuert
        # TODO 3. Transfomer werden über das Kontextmenü gesteuert
        # TODO 4. Transformer werden id technisch durchnummieriert um verschmlezungen zu verhindern
        # TODO 5. Es wird unschieben zwischen Tranformer, welche auf ranges von texten und welche an der CUrsor Postion angewerndet werden
        # assert False, "beachte 5"
        self._transformer: Dict[str, ITagTransform] = {}
        self._transformer_to_old_replacement: Dict[str, List[Tuple[Gtk.TextMark, str]]] = {}
        # Disable Transformers to prevent an apply tag recursion
        # Since nesting of is prohibited, this is not a restriction
        self.callback_toggle_tag = None
        # Copy Variables
        self.editor_name = editor.editor_name
        self.builder = editor.builder
        # text_buffer.connect("apply_tag",self._on_apply_tag)
        # Setup Tag merge preventing
        self.editor = editor
        self._last_state = None
        self._last_text = ""
        # Call methods in child class
        self.define_all_tags()
        self.init_buttons()
        self.setup_my_transformer()

        # Connect for user action and text selecting

        # text_buffer.connect("mark-set", self._on_mark_set)
        #        text_buffer.connect("end-user-action", self._on_end_user_action)

        # Update GUI
        #        self._update_transform_buttons()

        # Mouse context menu
        self.builder.get_object(self.editor_name).connect("populate_popup", self.fill_mouse_context_menu)

    def is_range_editable(self, start: Gtk.TextIter, end: Gtk.TextIter):
        """Checks if a range is editable"""
        text_editor = self.builder.get_object(self.editor_name)
        buffer = text_editor.get_buffer()
        offset_begin = start.get_offset()
        offset_end = end.get_offset()
        default_editable = True
        for n in range(offset_begin, offset_end):
            it: Gtk.TextIter = buffer.get_iter_at_offset(n)
            if not it.can_insert(default_editable):
                return False
        return True

    def event_execute_click_transformer(self, cursor_pos, transformer):
        # Get buffer
        text_buffer = self.builder.get_object(self.editor_name).get_buffer()
        text, tag = transformer.apply(cursor_pos, text_buffer)
        # Abort, if we selected no image
        if text is None or tag is None:
            return
        text_buffer.insert_at_cursor(text)
        start_it = text_buffer.get_iter_at_offset(cursor_pos)
        end_it = text_buffer.get_iter_at_offset(cursor_pos + len(text))
        # print("event_rm_execute_click_transformer", self.recipe_tags)
        self._on_apply_tag(None, self.recipe_tags[tag], start_it, end_it)

    def context_menu_add_range_transformer_apply(self, parent_menu, parent_parent_menu, bounds, tag_name):
        transformer: ITagTransform = self._transformer[tag_name]
        has_selection: bool = len(bounds) != 0
        if isinstance(transformer, ITransformerRange) and has_selection:
            start, end = bounds
            if self.is_range_editable(start, end):
                menu_item = Gtk.MenuItem(transformer.get_label())
                menu_item.show()
                parent_parent_menu.show()
                assert tag_name != "img_cursor", "Logic Error"
                # print("Create Range: ", tag_name)
                tag: Gtk.TextTag = self.recipe_tags[tag_name]
                menu_item.connect("activate", lambda widget: self._on_apply_tag(None, tag, start, end))
                parent_menu.append(menu_item)

    def search_tag_range(self, start_offset, tagname) -> Tuple[int, int]:
        text_buffer = self.builder.get_object(self.editor_name).get_buffer()
        states = self.editor.export_state()
        nearest_end = None
        for tag in states[1]:
            tag_name = tag[0]
            start = tag[1]
            end = tag[2]
            if tag_name == tagname and start_offset >= start and start_offset < end:
                return start, end
        return None


    def _is_transformer_tag(self, tag: Gtk.TextTag):
        tag_name: str = tag.props.name
        return tag_name in self._transformer

    def _on_remove_tag(self, _, tag, start, end):
        """Callback function applied when a tag is removed"""
        tag_name: str = tag.props.name
        if self._is_transformer_tag(tag):
            text_editor = self.builder.get_object(self.editor_name)
            buffer = text_editor.get_buffer()
            offset_begin = start.get_offset()
            offset_end = end.get_offset()
            transform_cache = self._transformer_to_old_replacement[tag_name]
            for entry_index, entry in enumerate(transform_cache[:]):
                mark = entry[0]
                mark_iter = buffer.get_iter_at_mark(mark)
                offset_marker = mark_iter.get_offset()
                offset_remove = start.get_offset()
                if offset_marker == offset_remove:
                    old_text = entry[1]
                    # Remove end marker
                    buffer.remove_tag_by_name(":start_tag:" + tag_name, buffer.get_iter_at_offset(offset_begin),
                                              buffer.get_iter_at_offset(offset_begin + 1))
                    buffer.remove_tag_by_name(":end_tag:" + tag_name, buffer.get_iter_at_offset(offset_end),
                                              buffer.get_iter_at_offset(offset_end + 1))
                    # Delete Old Text
                    buffer.delete(start, end)
                    # Get new iterator because iterator is invalid after calling delete
                    start = buffer.get_iter_at_mark(mark)
                    buffer.insert(start, old_text)
                    del transform_cache[entry_index]
                    return

    def event_rm_execute_click_transformer(self, range, tag_name):
        start_offset = range[0]
        end_offset = range[1]
        text_buffer = self.builder.get_object(self.editor_name).get_buffer()
        # Get buffer
        tag = self.recipe_tags[tag_name]
        self._on_remove_tag(None, tag, text_buffer.get_iter_at_offset(start_offset),
                            text_buffer.get_iter_at_offset(end_offset))

    def context_menu_remove_range_transformer(self, context_menu, parent_menu, parent_parent_menu, cursor_pos,
                                              tag_name):
        # text_buffer = self.builder.get_object(self.editor_name).get_buffer()
        transformer: ITagTransform = self._transformer[tag_name]
        if isinstance(transformer, ITransformerRange):
            tag_range = self.search_tag_range(cursor_pos, tag_name)
            if tag_range is not None:
                menu_item = Gtk.MenuItem("Remove: " + transformer.get_label())
                # parent_parent_menu.show()
                menu_item.show()
                menu_item.connect("activate",
                                  lambda widget: self.event_rm_execute_click_transformer(tag_range, tag_name))
                context_menu.append(menu_item)

    def context_menu_add_cursor_transformer_apply(self, parent_menu, parent_parent_menu, cursor_pos, tag_name):
        # Get buffer
        text_buffer = self.builder.get_object(self.editor_name).get_buffer()
        transformer: ITagTransform = self._transformer[tag_name]
        if isinstance(transformer, ITransformerCursor):
            cursor_it: Gtk.TextIter = text_buffer.get_iter_at_offset(cursor_pos)
            if cursor_it.can_insert(True):
                menu_item = Gtk.MenuItem("Add " + transformer.get_label())
                parent_parent_menu.show()
                menu_item.show()
                menu_item.connect("activate",
                                  lambda widget: self.event_execute_click_transformer(cursor_pos, transformer))
                parent_menu.add(menu_item)

    def context_menu_remove_img(self, sub_menu_cursor, tmp_cursor, cursor_pos, tag_name):
        assert "img" not in self._transformer[tag_name], "No Image tag"



    def fill_mouse_context_menu(self, _: Gtk.TextView, menu: Gtk.Widget):
        # Get buffer
        text_buffer = self.builder.get_object(self.editor_name).get_buffer()
        # The position of the mouse cursor
        cursor_pos: int = text_buffer.props.cursor_position
        bounds = text_buffer.get_selection_bounds()

        # Create submenu range
        tmp_range = Gtk.MenuItem("On Selection")
        menu.append(tmp_range)
        sub_menu_range = Gtk.Menu()
        tmp_range.set_submenu(sub_menu_range)

        # Create Submenu at cursor
        tmp_cursor = Gtk.MenuItem("At Cursor")
        menu.append(tmp_cursor)
        sub_menu_cursor = Gtk.Menu()
        tmp_cursor.set_submenu(sub_menu_cursor)

        for tag_name in self._transformer:
            transformer: ITagTransform = self._transformer[tag_name]
            if transformer.hide_from_context_menu():
                continue
            self.context_menu_add_range_transformer_apply(sub_menu_range, tmp_range, bounds, tag_name)
            self.context_menu_add_cursor_transformer_apply(sub_menu_cursor, tmp_cursor, cursor_pos, tag_name)
            # Add Option for removing tags
            self.context_menu_remove_range_transformer(menu, sub_menu_range, tmp_range, cursor_pos, tag_name)
        #
        context_menu_remove_img(sub_menu_cursor, tmp_cursor, cursor_pos,"img")

    def apply_tag(self, name: str, start: int, end: int) -> int:
        tag: Gtk.TextTag = self.recipe_tags[name]
        text_buffer = self.builder.get_object(self.editor_name).get_buffer()
        start_it = text_buffer.get_iter_at_offset(start)
        end_it = text_buffer.get_iter_at_offset(end)
        return self._on_apply_tag(None, tag, start_it, end_it)

    def _on_apply_tag(self, widget, tag, start, end):
        """Callback function, called when a tag is applied"""

        offset_begin = start.get_offset()
        offset_end = end.get_offset()
        # offset_end = end.get_offset()
        tag_name: str = tag.props.name
        # print("_on_apply_tag ", tag_name)
        if tag_name in self._transformer:
            # Extract old text
            text_editor = self.builder.get_object(self.editor_name)
            buffer = text_editor.get_buffer()
            old_text = buffer.get_text(buffer.get_iter_at_offset(offset_begin), buffer.get_iter_at_offset(offset_end),
                                       True)
            transformer: ITransformerRange = self._transformer[tag_name]

            # Check data type and prevent endless recursion
            if not isinstance(transformer, ITransformerRange):
                return offset_end - offset_begin
            # Delete old text
            # print("Delete from: ",offset_begin," To: ", offset_end)
            buffer.delete(buffer.get_iter_at_offset(offset_begin), buffer.get_iter_at_offset(offset_end))
            # Transform text
            optional_arg = (buffer, offset_begin, offset_end)
            transformer.initialise(old_text, optional_arg)
            # Get Text Mark this is the address of the selection
            mark = buffer.create_mark(None, buffer.get_iter_at_offset(offset_begin), True)
            # Insert New Text
            new_text, new_tags = transformer.get_replacement_text()
            # print("Insert at ",offset_begin," text ",new_text," tag name",tag_name)
            buffer.insert_with_tags_by_name(buffer.get_iter_at_offset(offset_begin), new_text, tag_name)
            buffer.apply_tag_by_name(":start_tag:" + tag_name, buffer.get_iter_at_offset(offset_begin),
                                     buffer.get_iter_at_offset(offset_begin + 1))
            end_range = offset_begin + len(new_text)
            # print("End Tag at pos: ", end_range, "offset Begin ",offset_begin," Len(Text)",new_text, " leen",len(new_text))
            buffer.apply_tag_by_name(":end_tag:" + tag_name, buffer.get_iter_at_offset(end_range - 1),
                                     buffer.get_iter_at_offset(end_range))

            # Apply additional tags if needed
            for new_tag in new_tags:
                buffer.apply_tag_by_name(new_tag[0], buffer.get_iter_at_offset(new_tag[1]),
                                         buffer.get_iter_at_offset(new_tag[2]))
            transformer.event_after_replacement()
            # Save old text for later recovery
            if tag_name not in self._transformer_to_old_replacement:
                self._transformer_to_old_replacement[tag_name] = []
            self._transformer_to_old_replacement[tag_name].append((mark, old_text))
            # Add one because offset_end - offset_begin si default an len of new text si one smaller
            return len(new_text) + 1

    def connect_toggle_tag_callback(self, func: Callable):
        self.callback_toggle_tag = func

    def clear(self):
        pass

    def insert_tag_at_cursor_pos(self, text: str, tag_name: str):
        pass

    def _on_mark_set(self, widget: Gtk.TextBuffer, location, mark):
        """Callback when we select Text"""
        pass

    def _prevent_transform_tag_merging(self):
        pass

    #

    def register_tag_transformer(self, tag_name: str, transformer: ITagTransform):
        assert isinstance(transformer, ITransformerRange) or isinstance(transformer,
                                                                        ITransformerCursor), "Only transformer are allowed. Does argument inherits from "
        self._transformer[tag_name] = transformer
