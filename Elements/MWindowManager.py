from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint
from Management.MWindow import MWindow
from Elements.MSplitter import MSplitter
from Elements.MHeaderBar import MHeaderBar


class MWindowManager(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("win_manage")
        self.setStyleSheet(self.styleSheet() + "QFrame#win_manage{background: rgb(50,50, 50)}")
        self.process_move = False
        self.child_windows = []
        self.move_offset = QPoint(0,0)
        self.window = None

    def add_window(self, widget):
        win = MWindow(widget)
        win.setParent(self)
        win.set_parent_window(self)
        win.show()
        return win

    def decouple(self, win):
        orig_position = win.mapToGlobal(win.pos())

        old_parent = win.get_parent_window()
        win.setParent(self)
        win.set_parent_window(self)
        win.move(orig_position)

        children_windows = old_parent.get_child_windows()

        #if(len(children_windows) == 1):
         #   self.decouple(children_windows[0])
        #old_parent.setParent(None)
        old_parent.setStyleSheet("background-color:purple")
        old_parent.deleteLater()

        win.show()

    def join_windows_in_splitter(self, win1, win2, location):
        # If the destination window already contains a splitter
        if type(win1.get_content()) is MSplitter:
            # Take out the existing splitter and its contents
            existing_splitter = win1.get_content()
            new_splitter = MSplitter()

            # Add the existing splitter to the new splitter as a child
            new_splitter.add_content(existing_splitter)

            # Add the new widget to the new splitter at the specified location
            new_splitter.add_content(win2, location)

            # Create a new window with the new splitter
            self.add_window(new_splitter)

            # Delete win2 and win1. Their contents has been removed and combined in a new window
            win1.deleteLater()

        elif type(win2.get_content()) is MSplitter:
            # Take out the existing splitter and its contents
            existing_splitter = win2.get_content()
            new_splitter = MSplitter()



            # Add the existing splitter to the new splitter as a child
            new_splitter.add_content(existing_splitter)

            # Add the new widget to the new splitter at the specified location
            new_splitter.add_content(win1, location)

            # Create a new window with the new splitter
            self.add_window(new_splitter)

            # Delete win2 and win1. Their contents has been removed and combined in a new window
            win2.deleteLater()

        else:
            new_splitter = MSplitter(self)

            new_splitter.add_content(win2)
            new_splitter.add_content(win1, location)

            new_win = self.add_window(new_splitter)

            win1.set_parent_window(new_win)
            win2.set_parent_window(new_win)

    def mousePressEvent(self, event):
        # print("You clicked!")
        child = self.childAt(event.pos())
        if child:
            print("You clicked on my child")
            if type(child) is MHeaderBar:
                child.getWindow().raise_()

                # print("You clicked on my header")
                self.process_move = True
                self.window = child.getWindow()

                # Decouple the window we are moving if it is embedded in another layout
                if self.window.parent() is not self:
                    global_pos = event.pos()
                    offset_pos = self.window.mapFromGlobal(global_pos)
                    self.decouple(self.window)

                    self.window.move(global_pos - offset_pos)
                self.move_offset = event.pos() - self.window.pos()
                event.accept()
            else:
                child.raise_()
        else:
            event.accept()
            return

    def mouseReleaseEvent(self, event):
        # print("You released!")
        self.process_move = False

        # Figure out if we are above another window
        for child in self.children():
            if self.window is not child:
                if child.geometry().contains(event.pos()):
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
        event.accept()

    def mouseMoveEvent(self, event):
        if self.process_move:
            self.window.move(event.pos() - self.move_offset)

            for child in self.children():
                if self.window is not child and type(child) is MWindow:
                    if child.geometry().contains(event.pos()):
                        child.show_drop_regions()
                        child.focus_drop_region(event.globalPos())
                    else:
                        child.hide_drop_regions()


            event.accept()

    def _remove_child_window(self, child_window):
        self.child_windows.remove(child_window)

    def _add_child_window(self, child_window):
        self.child_windows.append(child_window)

    def _defocus_all_drop_regions(self):
        for child in self.children():
            if self.window is not child and type(child) is MWindow:
                child.hide_drop_regions()