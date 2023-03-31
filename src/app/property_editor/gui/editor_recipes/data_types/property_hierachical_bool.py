from src.app.property_editor.gui.editor_generic.property_editor_base import IPropertyDataType

from typing import Callable, List, Optional, Dict

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PropertyHierachicalBool(IPropertyDataType):
    def create_cell(self, args) -> Gtk.Widget:
        self.tree_store = Gtk.TreeStore(str, bool)
        self.treeview = Gtk.TreeView.new_with_model(self.tree_store)
        # Setup columns
        self.toggle_renderer = Gtk.CellRendererToggle()
        for i, column_title in enumerate(["Name", "Set"]):
            column = None
            if i == 0:
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            elif i == 1:
                self.toggle_renderer.set_activatable(False)
                self.toggle_renderer.connect("toggled", self.on_toggled)
                column = Gtk.TreeViewColumn(column_title, self.toggle_renderer,active=1)

            self.treeview.append_column(column)
        # We don't need headers
        self.treeview.set_headers_visible(False)
        self.treeview.set_enable_search(True)
        assert "key" in args," Key not defined"
        self.key: str = args["key"]
        self.get_children: Callable[[str], List[(str)]] = args.get("get_children", None)
        self.get_parent: Callable[[str], Optional[str]] = args.get("get_parent", None)
        self.get_display_name: Callable[[str],str] = args.get("get_display_name", None)


        assert self.get_children is not None, "get_children Function for HierachicalBool not defined"
        assert self.get_parent is not None, "get_children Function for HierachicalBool not defined"
        assert self.get_display_name is not None, "get_display_name Function for HierachicalBool not defined"
        self.setup_tree()
        return self.treeview

    def signal_change(self):
        pass


    def on_toggled(self, widget, path):
        """If a child is set to TRUE set the parent also to TRUE"""
        self.signal_change()
        def activate_parent(key,toggle):
            path = self.key_to_path[key]
            # Toggle current Value
            current_value = self.tree_store[path][1]
            if toggle:
                self.tree_store[path][1] = not current_value
            else:
                self.tree_store[path][1] = True
            # Toggle Parent if we set to True
            if not current_value or not toggle:
                parent = self.get_parent(key)
                if parent is not None:
                    activate_parent(parent, False)

        def deactivate_childs(key,set_to_false):
            path = self.key_to_path[key]
            if set_to_false:
                self.tree_store[path][1] = False
            current_value = self.tree_store[path][1]
            if not current_value:
                for child in self.get_children(key):
                    deactivate_childs(child,True)

        activate_parent(self.path_to_key[path], True)
        deactivate_childs(self.path_to_key[path], False)

    def setup_tree(self):
        """Creates the tree but the values are set later"""
        assert self.get_parent(self.key) is None, "Trees can only build for root attributes. Set Child Values in Parent Tag"
        self.row_iters = {}
        self.path_to_key = {}
        self.key_to_path = {}
        def create_tree(key):

            is_root: bool = (self.get_parent(key) is None)
            if is_root:
                # None is a root iterator
                it = None
            else:
                parent = self.get_parent(key)
                assert parent in self.row_iters, "Parent has to be created before child parent: " + parent
                it = self.row_iters[parent]
            display_name = self.get_display_name(key)
            # Create Entry
            assert display_name not in self.row_iters and key not in self.row_iters," Use Unique names"
            self.row_iters[key] = self.tree_store.append(it, [display_name, False])
            path = self.tree_store.get_path(self.row_iters[key])
            self.path_to_key[str(path)] = key
            self.key_to_path[key] = path
            for children in self.get_children(key):
                create_tree(children)

        create_tree(self.key)



    def get_name(self) -> str:
        return type(self).__name__

    def set_cell_value(self, values: Dict[str, bool]):
        assert type(values) is not bool, "Wrong default type"
        for key in values:
            path = self.key_to_path[key]
            current_value = self.tree_store[path][1]
            # Toggle the value so that we can use the toggle function to activate the parent recursivly
            self.tree_store[path][1] = not values[key]
            self.on_toggled(self.treeview, str(path))

    def get_value(self) -> Dict[str, bool]:
        ret = {}
        for key in self.key_to_path:
            current_value = self.tree_store[self.key_to_path[key]][1]
            ret[key] = current_value
        return ret

    def set_activ(self, value):
        self.toggle_renderer.set_activatable(value)
        pass
