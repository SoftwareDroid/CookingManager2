from src.gui.share.gtk_helper import GtkHelper
from typing import Dict, Tuple, Sequence
from abc import ABC,abstractmethod
from typing import Set
from abc import abstractmethod, ABC

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Editor(ABC):
    """Contains only base functionality such as import, exporting text and ad-don integration"""

    def on_export(self, _):
        self.import_state(self.export_state)

    @abstractmethod
    def import_state_callback(self):
        pass

    def import_state(self, state: Tuple[str, Sequence[Tuple[str, int, int]]]):
        """Import a state which is exported via export_state"""
        self.import_state_callback()

        text: str = state[0]
        annotations: Sequence[Tuple[str, int, int]] = state[1]
        text_editor = self.builder.get_object(self.editor_name)
        buffer = text_editor.get_buffer()
        # Set full text
        buffer.set_text(text)
        # Apply annotations
        for annotation in annotations:
            start = buffer.get_iter_at_offset(annotation[1])
            end = buffer.get_iter_at_offset(annotation[2])
            tagname: str = annotation[0]
            assert len(tagname) > 0, "Invalid tag name"
            buffer.apply_tag_by_name(tagname, start, end)
            buffer.apply_tag_by_name(":start_tag:" + tagname,buffer.get_iter_at_offset(annotation[1]),buffer.get_iter_at_offset(annotation[1] + 1))
            buffer.apply_tag_by_name(":end_tag:" + tagname, buffer.get_iter_at_offset(annotation[2]),
                                     buffer.get_iter_at_offset(annotation[2] + 1))
        # Sort annonations from begin
        offset: int = 0
        for annotation in sorted(annotations, key=lambda x: x[1]):
            old_len: int = annotation[2] - annotation[1]
            new_len: int = self.apply_tag(annotation[0], annotation[1] + offset, annotation[2])
            diff_len: int = old_len - new_len
            offset -= diff_len

    @abstractmethod
    def apply_tag(self,name: str,start: int, end :int) -> int:
        """Retuns new size"""
        pass

    def get_all_text(self):
        """Return all text without annotations"""
        text_editor = self.builder.get_object(self.editor_name)
        buffer = text_editor.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        all_text = buffer.get_text(start_iter, end_iter, True)

        return all_text

    def export_state(self) -> Tuple[str, Sequence[Tuple[str, int, int]]]:
        text_editor = self.builder.get_object(self.editor_name)
        buffer = text_editor.get_buffer()
        all_text = self.get_all_text()
        tag_searcher_cache: Dict = {}
        exported_tags: Sequence[Tuple[str, int, int]] = []
        for n in range(len(all_text)):
            it: Gtk.TextIter = buffer.get_iter_at_offset(n)
            tag_set: Set[str] = {tag.props.name for tag in it.get_tags()}
            for tag_name in tag_set:
                if not tag_name.startswith(":"):
                    if ":start_tag:" + tag_name in tag_set:
                        # Start one to k new tags
                            tag_searcher_cache[tag_name] = n
                    if ":end_tag:" + tag_name in tag_set:
                        exported_tags.append((tag_name, tag_searcher_cache[tag_name], n + 1))
                        del tag_searcher_cache[tag_name]

        # assert len(tag_searcher_cache) == 0, "Tags found without proper start and ending" + str(tag_searcher_cache)
        return all_text, exported_tags

    def export_state2(self) -> Tuple[str, Sequence[Tuple[str, int, int]]]:
        # Init
        text_editor = self.builder.get_object(self.editor_name)
        buffer = text_editor.get_buffer()
        all_text = self.get_all_text()
        tag_searcher_cache: Dict = {}
        exported_tags: Sequence[Tuple[str, int, int]] = []
        for n in range(len(all_text)):
            it: Gtk.TextIter = buffer.get_iter_at_offset(n)
            for tag in it.get_tags():
                name: str = tag.props.name
                # start new tag
                if name not in tag_searcher_cache:
                    #print("Start new tag at pos: ", n, "tag: ",name)
                    tag_searcher_cache[name] = (n, n + 1)
                    continue
                else:
                    begin_of_tag = tag_searcher_cache[name][0]
                    end_of_tag = tag_searcher_cache[name][1]
                    # tag continue
                    if n == end_of_tag:
                        #print("tag continue: ",name, " pos ",n)
                        tag_searcher_cache[name] = (begin_of_tag, end_of_tag + 1)

            # No tag continue
            for name in list(tag_searcher_cache):
                begin_of_tag = tag_searcher_cache[name][0]
                end_of_tag = tag_searcher_cache[name][1]
                if (end_of_tag - 1) != n:
                    exported_tags.append((name, begin_of_tag, end_of_tag))
                    #print("Stop tag: ",name," ", n)
                    del tag_searcher_cache[name]
        # Export all tag, which stop at the last char
        for name in list(tag_searcher_cache):
            begin_of_tag = tag_searcher_cache[name][0]
            end_of_tag = tag_searcher_cache[name][1]
            exported_tags.append((name, begin_of_tag, end_of_tag))

        return all_text, exported_tags