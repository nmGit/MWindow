from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint, pyqtSignal
from PyQt5.QtCore import Qt

from Elements.MWindow import MWindow
from Elements.MSplitter import MSplitter
from Elements.MHeaderBar import MHeaderBar
from Elements.MContainer import MContainer

import json

import pprint
pp = pprint.PrettyPrinter(indent=2, width=1)

class MWindowManager(QtWidgets.QFrame, MContainer):

    window_hierarchy_updated_sig = pyqtSignal()

    resize_regions = {"none": 0, "top": 1, "bottom": 2, "left": 3, "right": 4, "top-left": 5, "top-right": 6,
                      "bottom-left": 7, "bottom-right": 8}

    def __init__(self):
        super().__init__()
        self.setObjectName("win_manage")
        self.setStyleSheet(self.styleSheet() + "QFrame#win_manage{background: rgb(50,50, 50)}")
        self.process_move = False
        self.child_containers = []
        self.move_offset = QPoint(0,0)
        self.window = None
        self.setMouseTracking(True)
        self.resize_dimension = self.resize_regions["none"]
        self.window_hierarchy = {}
        self.uid = 0

    def get_uid(self):
        return self.uid

    def serialize(self):
        self.dump_to_dictionary()


    def add_window(self, widget, title, uid = None):
        win = MWindow(widget, title)
        win.setParent(self)
        win.set_parent_container(self)
        win.setMouseTracking(True)
        win.show()
        win.move(0, 0)

        if type(widget) is MSplitter:
            widget.set_parent_container(win)

        if self._validate_uid(uid):
            win.set_uid(uid)
        else:
            uid = self._generate_window_uid()
            win.set_uid(uid)
        return win

    def remove_window(self, window):
        self.child_containers.remove(window)
        window.deleteLater()

    def get_title(self):
        return "Main window"

    def serialize(self):
        self.construct_window_hierarcy()
        dict_ = self.get_window_hierarchy()
        ser_data = json.dumps(dict_, indent=4)
        return ser_data

    def deserialize(self, ser_str, item_dict):
        try:
            if ser_str != '':
                dict_ = json.loads(ser_str)
            else:
                dict_ = {}
        except json.decoder.JSONDecodeError as e:
            print("Could not decode window manager data. The data may be corrupt")
            print(e)
            dict_ = {}


        if "MainWindow" in dict_.keys():

            self._reconstruct_window(self, dict_["MainWindow"]["windows"], item_dict)
            try:
                self.setGeometry(dict_["MainWindow"]["position"][0],
                                 dict_["MainWindow"]["position"][1],
                                 dict_["MainWindow"]["size"][0],
                                 dict_["MainWindow"]["size"][1])
            except KeyError as e:
                print("Could not find top-level position and size information. The data may have been corrupted")
                print(e)

        else:
            for key, value in item_dict.items():
                self.add_window(value[0], value[1], int(key))



    def _reconstruct_window(self, parent, ser_data, item_dict):
        def _place_window(location, value):
            uid = value[list(value.keys())[0]]['uid']
            position = value[list(value.keys())[0]]['position']
            size = value[list(value.keys())[0]]['position']
            content = item_dict[uid]
            win = MWindow(content[0], content[1])
            win.set_uid(uid)
            win.setGeometry(position[0], position[1], size[0], size[1])
            parent.add_content(win, location)

        def _place_splitter(parent, location):
            split = MSplitter(parent.get_parent_container())
            parent.add_content(split, location)
            self._reconstruct_window(split, value["splitter"], item_dict)
            split.set_sizes(*value["splitter"]["sizes"])


        for key, value in ser_data.items():
            # This a base case.
            # If we have reached a leaf then don't try to traverse the tree any further
            if type(value) is not dict:
                continue

            # Get the UID of the window that we are about to create. The UIDs of windows *must* remain
            # consistent, as uid are keyed on by the application to determine which window goes where.
            # it is up to the application to save the UIDs of its gui elements
            uid = value.get('uid', None)

            # If a UID has been found and the parent isn't a splitter, then create the window
            # if the parent is a splitter then there are a few extra steps to place the contents within the splitter
            # at the correct location

            # With the way this is set up, the next two if statements will only pass iff the parent is a floating window
            # container. That's important because it allows the add_window call
            if type(parent) is not MSplitter and uid:

                # Fetch a reference to the gui data (e.g. QWidget) that is going to be placed
                content = item_dict.get(uid, None)

                # Ensure that the key (uid) was valid
                # Ensure that we are not going to try to place a splitter. Doing so requires different steps.
                if content and "splitter" not in value.keys():
                    win = parent.add_window(content[0], key, uid)
                    win.setGeometry(value["position"][0], value["position"][1],
                                    value["size"][0], value["size"][1]
                                    )

                # Otherwise, if we are placing a splitter (which is an MContainer) then we have to make a recursive
                # call that will take care of placing all children inside of the splitter.
                elif type(value) is dict and "splitter" in value.keys():

                    # Create a blank splitter and add it to the parent
                    split = MSplitter(None)
                    win = parent.add_window(split, key, value["uid"])
                    split.set_parent_container(win)

                    self._reconstruct_window(split, ser_data[key]["splitter"], item_dict)
                    #self._reconstruct_window(split, ser_data[key]["splitter"], item_dict)
                    split.set_sizes(*value["splitter"]["sizes"])

                    win.setGeometry(value['position'][0], value['position'][1], value['size'][0], value['size'][1])
                    win.set_uid(None)

            elif type(parent) is MSplitter:
                if ser_data["orientation"] == MSplitter.VERTICAL:
                    if "splitter" in value.keys() and key == "top or left":
                        _place_splitter(parent, "top")
                    elif key == "top or left":
                        _place_window('top', value)

                    if "splitter" in value.keys() and key == "bottom or right":
                        _place_splitter(parent, "bottom")
                    elif key == "bottom or right":
                        _place_window('bottom', value)

                if ser_data["orientation"] == MSplitter.HORIZONTAL:
                    if "splitter" in value.keys() and key == "top or left":
                        _place_splitter(parent, "left")
                    elif key == "top or left":
                        _place_window('left', value)

                    if "splitter" in value.keys() and key == "bottom or right":
                        _place_splitter(parent, "right")
                    elif key == "bottom or right":
                        _place_window('right', value)

                #parent.add_content()
    def get_window_hierarchy(self):
        return self.window_hierarchy

    def construct_window_hierarcy(self):
        self.window_hierarchy = {}
        self.window_hierarchy["MainWindow"] = {}
        self.window_hierarchy["MainWindow"]["windows"] = {}
        #for win in self.child_windows:
        self._add_children_to_dict(self.window_hierarchy["MainWindow"]["windows"], self)
        self.window_hierarchy["MainWindow"]["position"] = (self.x(), self.y())
        self.window_hierarchy["MainWindow"]["size"] = (self.width(), self.height())
        self.window_hierarchy_updated_sig.emit()

    def _generate_window_uid(self):
        next_uid = 1
        illegal_uids = [0] # 0 is reserved for the main window
        for win in self.child_containers:
            illegal_uids.append(win.get_uid())

        while next_uid in illegal_uids:
            next_uid += 1

        return next_uid

    def _validate_uid(self, uid):
        if uid == None:
            return False

        illegal_uids = []
        for win in self.child_containers:
            illegal_uids.append(win.get_uid())
        if uid in illegal_uids:
            return False
        else:
            return True
    # def get_child_windows(self):
    #     return self.child_containers

    def get_content(self):
        return self.child_containers

    def _add_children_to_dict(self, dict_, parent):
        # pp.pprint(self.window_hierarchy)
        item_to_index = parent
        if type(parent) is MWindow and type(parent.get_content()) is MSplitter:
            item_to_index = parent.get_content()

        if type(item_to_index) is MSplitter:
            #dict_ = {"position": (parent.x(), parent.y()),
            #                     "size": (parent.width(), parent.height()),
            #                     "uid": parent.get_uid()}

            splitter = item_to_index
            parent_key = None

            if type(parent) is MWindow:
                parent_key = str(parent)
                dict_ = dict_[parent_key]
            elif type(parent) is MSplitter:
                pass

            dict_["splitter"] = {}
            # dict_[str(child)]["splitter"]["position"] = splitter.get_position()

            dict_["splitter"] = {}
            content_1 = splitter.get_item_at(0)
            content_2 = splitter.get_item_at(1)
            dict_["splitter"]["top or left"] = {}
            dict_["splitter"]["bottom or right"] = {}
            if content_1:
                self._add_children_to_dict(dict_["splitter"]["top or left"], content_1)
            if content_2:
                self._add_children_to_dict(dict_["splitter"]["bottom or right"], content_2)
            dict_["splitter"]["orientation"] = splitter.get_orientation()
            dict_["splitter"]["sizes"] = splitter.get_sizes()
        else:
            children = parent.get_child_container()
            if len(children) == 0:
                dict_[str(parent)] = {}
                dict_[str(parent)]["position"] = (parent.x(), parent.y())
                dict_[str(parent)]["size"] = (parent.width(), parent.height())
                dict_[str(parent)]["uid"] = parent.get_uid()
            else:
                for child in children:
                    dict_[str(child)] = {"position": (child.x(), child.y()),
                                         "size": (child.width(), child.height()),
                                         "uid": child.get_uid()}

                    self._add_children_to_dict(dict_, child)

            #else:
            #    self._add_children_to_dict(dict_[str(child)]["splitter"], child)


    def decouple(self, win, width = None, height = None):
        orig_position = win.mapToGlobal(win.pos())


        old_parent = win.get_parent_container()



        win.setParent(self)
        win.set_parent_container(self)

        # Take the global position from the window and map it to coordinates of the main window
        # Then move the window to that position
        orig_position_mapped_to_main_window = self.mapFromGlobal(orig_position)

        if(width is not None and height is not None):
            win.setGeometry(orig_position_mapped_to_main_window.x(),
                            orig_position_mapped_to_main_window.y(),
                            width,
                            height)
        else:
            win.move(orig_position_mapped_to_main_window)

        win.updateGeometry()
        children_windows = [child for child in old_parent.get_child_container() if type(child) is MWindow]
        children_elements = [child for child in old_parent.get_child_container() if type(child) is MWindow]

        if(len(children_windows) == 1):
            orig_width = children_windows[0].width()
            orig_height = children_windows[0].height()
            self.decouple(children_windows[0], orig_width, orig_height)
            #print("Deleting", old_parent.get_title())
            #self.remove_window(old_parent)
        else:
            pass
            other_content = old_parent.get_content()
            if(len(children_windows) >= 2):
                new_title = ''
                for window in children_windows:
                    new_title = new_title + str(window) + ","
                new_window = self.add_window(other_content, new_title)
                for window in children_elements:
                    window.set_parent_container(new_window)
            #print("deleting", old_parent)
            old_parent.setStyleSheet("background-color:purple")
            self.remove_window(old_parent)

        #old_parent.setParent(None)

        win.show()
        return win

    def join_windows_in_splitter(self, win1, win2, location):
        # If the destination window already contains a splitter
        if type(win1.get_content()) is MSplitter:
            print("You dropped a window on a splitter")
            # Take out the existing splitter and its contents
            existing_splitter = win1.get_content()
            print("Content", existing_splitter)
            existing_windows = [child for child in win1.get_child_container()]
            print("Existing windows", [str(win) for win in existing_windows])
            new_splitter = MSplitter(None)

            # Create a new window with the new splitter
            new_window = self.add_window(new_splitter, "%s, %s" % (win1.get_title(), win2.get_title()))

            # Add the existing splitter to the new splitter as a child
            new_splitter.add_content(existing_splitter)

            # Add the new widget to the new splitter at the specified location
            new_splitter.add_content(win2, location)

            # Now we need to re-parent all existing windows as well as the one that was dragged in
            for window in existing_windows:
                window.set_parent_container(new_window)
            win2.set_parent_container(new_window)

            # Delete win2 and win1. Their contents has been removed and combined in a new window
            print("Deleting", win1.get_title())
            self.remove_window(win1)

        elif type(win2.get_content()) is MSplitter:
            print("You dropped a splitter on a window")
            # Take out the existing splitter and its contents
            existing_splitter = win2.get_content()
            # Create a copy because we need to modify the list
            existing_windows = [child for child in win2.get_child_container()]

            new_splitter = MSplitter(None)

            # Create a new window with the new splitter
            new_window = self.add_window(new_splitter, "%s, %s" % (win1.get_title(), win2.get_title()))

            # Add the existing splitter to the new splitter as a child
            new_splitter.add_content(existing_splitter)

            # Add the new widget to the new splitter at the specified location
            new_splitter.add_content(win1, location)


            # Now we need to re-parent all existing windows as well as the one that was dragged in
            for window in existing_windows:
                window.set_parent_container(new_window)
            win1.set_parent_container(new_window)

            # Delete win2 and win1. Their contents has been removed and combined in a new window
            print("Deleting", win2.get_title())
            self.remove_window(win2)

        else:
            new_splitter = MSplitter(None)

            new_win = self.add_window(new_splitter, "%s, %s" % (win1.get_title(), win2.get_title()))

            new_splitter.add_content(win2)
            new_splitter.add_content(win1, location)


            win1.set_parent_container(new_win)
            win2.set_parent_container(new_win)



    def mouse_is_over_resize_region(self, pos):
        child = self.childAt(self.mapFromGlobal(pos))
        # print(child)
        if child is None:
            return self.resize_regions["none"]

        if type(child) is MHeaderBar:
            child = child.getWindow()
        if type(child) is MWindow:

            x = child.mapFromGlobal(pos).x()
            y = child.mapFromGlobal(pos).y()
            width = child.width()
            height = child.height()
            margin = 8

            if y < margin and x < margin:
                return self.resize_regions["top-left"]
            elif y > height - margin and x > width - margin:
                return self.resize_regions["bottom-right"]
            elif y > height - margin and x < margin:
                return self.resize_regions["bottom-left"]
            elif y < margin and x > width - margin:
                return self.resize_regions["top-right"]
            elif x < margin:
                return self.resize_regions["left"]
            elif x > width - margin:
                return self.resize_regions["right"]
            elif y < margin:
                return self.resize_regions["top"]
            elif y > height - margin:
                return self.resize_regions["bottom"]
            else:
                return self.resize_regions["none"]

    def update_cursor_shape(self, pos):
        '''
        Takes a global coordinate and makes the cursor the correct shape
        '''
        self.setCursor(Qt.ArrowCursor)
        child = self.childAt(self.mapFromGlobal(pos))
        #print(child)
        if child is None:
            self.setCursor(Qt.ArrowCursor)

            return
        region = self.mouse_is_over_resize_region(pos)

        if region is self.resize_regions["top-left"]:
            self.setCursor(Qt.SizeFDiagCursor)
        elif region is self.resize_regions["bottom-right"]:
            self.setCursor(Qt.SizeFDiagCursor)
        elif region is self.resize_regions["bottom-left"]:
            self.setCursor(Qt.SizeBDiagCursor)
        elif region is self.resize_regions["top-right"]:
            self.setCursor(Qt.SizeBDiagCursor)


        elif region is self.resize_regions["left"]:
            self.setCursor(Qt.SizeHorCursor)
        elif region is self.resize_regions["right"]:
            self.setCursor(Qt.SizeHorCursor)


        elif region is self.resize_regions["top"]:
            self.setCursor(Qt.SizeVerCursor)
        elif region is self.resize_regions["bottom"]:
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def move_window_dimension_to(self, window, dimension, pos):
        old_geometry = window.geometry()
        pos_mapped_to_main = self.mapFromGlobal(pos)

        if dimension is self.resize_regions["top-left"]:
            window.setGeometry(old_geometry.x() + self.mapFromGlobal(pos).x() - old_geometry.x(),
                               old_geometry.y() + self.mapFromGlobal(pos).y() - old_geometry.y(),
                               old_geometry.width() - (self.mapFromGlobal(pos).x() - old_geometry.x()),
                               old_geometry.height() - (self.mapFromGlobal(pos).y() - old_geometry.y())
                               )
            window.updateGeometry()

        elif dimension is self.resize_regions["bottom-right"]:
            window.setGeometry(old_geometry.x(),
                               old_geometry.y(),
                               self.mapFromGlobal(pos).x() - old_geometry.x(),
                               self.mapFromGlobal(pos).y() - old_geometry.y()
                               )
            window.updateGeometry()

        elif dimension is self.resize_regions["bottom-left"]:
            window.setGeometry(self.mapFromGlobal(pos).x(),
                               old_geometry.y(),
                               old_geometry.width() - (self.mapFromGlobal(pos).x() - old_geometry.x()),
                               self.mapFromGlobal(pos).y() - old_geometry.y()
                               )
            window.updateGeometry()

        elif dimension is self.resize_regions["top-right"]:
            window.setGeometry(old_geometry.x(),
                               self.mapFromGlobal(pos).y(),
                               self.mapFromGlobal(pos).x() - old_geometry.x(),
                               old_geometry.height() - (self.mapFromGlobal(pos).y() - old_geometry.y()),
                               )
            window.updateGeometry()

        elif dimension is self.resize_regions["left"]:
            window.setGeometry(old_geometry.x() + (self.mapFromGlobal(pos).x() - old_geometry.x()),
                               old_geometry.y(),
                               old_geometry.width() - (self.mapFromGlobal(pos).x() - old_geometry.x()),
                               old_geometry.height(),
                               )
            window.updateGeometry()

        elif dimension is self.resize_regions["right"]:
            window.setGeometry(old_geometry.x(),
                               old_geometry.y(),
                               self.mapFromGlobal(pos).x() - old_geometry.x(),
                               old_geometry.height(),
                               )
            window.updateGeometry()

        elif dimension is self.resize_regions["top"]:
            window.setGeometry(old_geometry.x(),
                               self.mapFromGlobal(pos).y(),
                               old_geometry.width(),
                               old_geometry.height() - (self.mapFromGlobal(pos).y() - old_geometry.y()),
                               )
            window.updateGeometry()

        elif dimension is self.resize_regions["bottom"]:
            window.setGeometry(old_geometry.x(),
                               old_geometry.y(),
                               old_geometry.width(),
                               self.mapFromGlobal(pos).y() - old_geometry.y(),
                               )
            window.updateGeometry()

        else:
            self.setCursor(Qt.ArrowCursor)

        if dimension != self.resize_regions["none"]:
             content_rect = window.get_content().geometry()
             window_rect = window.geometry()
             content_rect.setHeight(window_rect.height())
             content_rect.setWidth(window_rect.width())
             #window.setGeometry(window_rect)

    def high_z_child_window_at(self, pos):
        highest_z_win = None
        for win in self.child_containers:
            if win.geometry().contains(win.mapFromGlobal(pos)):
                return win

    def mousePressEvent(self, event):
        #print("You clicked!")
        child = self.childAt(self.mapFromGlobal(event.globalPos()))
        if child:

            #child.raise_()
            win = self.high_z_child_window_at(event.globalPos())
            if win:
                win.raise_()
            print("You clicked on my child", child)
            # Test to see if we are resizing a window
            x = child.mapFromGlobal(event.globalPos()).x()
            y = child.mapFromGlobal(event.globalPos()).y()
            resize_region = self.mouse_is_over_resize_region(event.globalPos())
            print("Resize dimension:", resize_region)
            if resize_region:
                self.resize_dimension = resize_region
                if type(child) is MHeaderBar:
                    self.window = child.getWindow()
                elif type(child) is MWindow:
                    self.window = child

            # Test to see if we are clicking on the header bar (window drag)
            elif type(child) is MHeaderBar:
                print("You clicked on my header")
                self.process_move = True
                self.window = child.getWindow()

                # Decouple the window we are moving if it is embedded in another layout
                if self.window.parent() is not self:
                    global_pos = event.globalPos()
                    offset_pos = self.window.mapFromGlobal(global_pos)
                    self.decouple(self.window)
                    # Move the window in the domain fo the main window
                    self.window.move(self.mapFromGlobal(global_pos))
                self.move_offset = event.globalPos() - self.mapToGlobal(self.window.pos())
                event.accept()
            # Test to see if we are just clicking on a window

        else:
            event.accept()
            return

    def mouseReleaseEvent(self, event):
        # print("You released!")
        self.process_move = False
        self.resize_dimension = self.resize_regions["none"]
       # self.resize_dimension = self.resize_regions["none"]
        # Figure out if we are above another window
        for child in self.children():
            if self.window is not child:
                if child.geometry().contains(self.mapFromGlobal(event.globalPos())):
                    drop_region = child.over_drop_regions(event.globalPos())
                    if drop_region is child.get_drop_region("top"):
                        self.join_windows_in_splitter(self.window, child, "top")
                    if drop_region is child.get_drop_region("left"):
                        self.join_windows_in_splitter(self.window, child, "left")
                    if drop_region is child.get_drop_region("right"):
                        self.join_windows_in_splitter(self.window, child, "right")
                    if drop_region is child.get_drop_region("bottom"):
                        self.join_windows_in_splitter(self.window, child, "bottom")
                    print("You dropped a child on another child!")
                    break
            self._defocus_all_drop_regions()
        self.construct_window_hierarcy()

        event.accept()

    def mouseMoveEvent(self, event):
        #print("Mouse is moving!")
        if self.resize_dimension:
            self.move_window_dimension_to(self.window, self.resize_dimension, event.globalPos())

        elif self.process_move:
            #print("Mouse is moving!")
            self.window.move(event.pos() - self.move_offset)

            for child in self.children():
                if self.window is not child and type(child) is MWindow:
                    if child.geometry().contains(event.pos()):
                        child.show_drop_regions()
                        child.focus_drop_region(event.globalPos())
                    else:
                        child.hide_drop_regions()
        else:
            self.update_cursor_shape(event.globalPos())
    #
    # def get_child_windows(self):
    #     return self.child_containers
    #
    # def _remove_child_container(self, child_container):
    #     self.child_containers.remove(child_container)
    #
    # def _add_child_container(self, child_container):
    #     self.child_containers.append(child_container)

    def _defocus_all_drop_regions(self):
        for child in self.children():
            if type(child) is MWindow:
                child.hide_drop_regions()

    def __str__(self):
        return "Main Window"