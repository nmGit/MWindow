from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QToolButton
from Elements.MHeaderBar import MHeaderBar

class MWindow(QFrame):

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.setObjectName("main_frame")
        # Construct top-level window elements

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)

        self.header_frame = MHeaderBar(self)

        self.main_layout.addWidget(self.header_frame)
        self.main_layout.addStretch(0)
        self.main_layout.addWidget(self.widget)

        self.show()

        self.setStyleSheet(self.styleSheet() + "QFrame#main_frame{border: 2px solid black}\r\n"
                                               "QFrame#main_frame{background-color:rgb(200,200,200)}")

        self.child_windows = []
        self.parent_window = None

        self.drop_region_top_frame = QFrame(self)
        self.drop_region_left_frame = QFrame(self)
        self.drop_region_right_frame = QFrame(self)
        self.drop_region_bottom_frame = QFrame(self)

        self.drop_region_stylesheet = "background-color: rgba(50, 50, 150, 100);" \
                                 "border: 2px solid blue"
        self.drop_region_focused_stylesheet = "background-color: rgba(50, 150, 50, 100);" \
                                 "border: 2px solid blue"

        self.drop_region_top_frame.setStyleSheet(self.drop_region_stylesheet)
        self.drop_region_left_frame.setStyleSheet(self.drop_region_stylesheet)
        self.drop_region_right_frame.setStyleSheet(self.drop_region_stylesheet)
        self.drop_region_bottom_frame.setStyleSheet(self.drop_region_stylesheet)

        self.drop_regions = {"top" : self.drop_region_top_frame,
                             "left" : self.drop_region_left_frame,
                             "right" : self.drop_region_right_frame,
                             "bottom" : self.drop_region_bottom_frame}

    def get_content(self):
        return self.widget

    def get_parent_window(self):
        return self.parent_window

    def get_child_windows(self):
        return self.child_windows

    def set_parent_window(self, new_parent_window):
        # Remove self from old parent
        if self.parent_window is not None:
            self.parent_window._remove_child_window(self)

        # Add self to new parent
        if(new_parent_window is not None):
            new_parent_window._add_child_window(self)

        # Set local reference to parent
        self.parent_window = new_parent_window

    def show_drop_regions(self):
        window_geometry = self.geometry()

        self.drop_region_top_frame.setGeometry(
            window_geometry.width()/3,
            0,
            window_geometry.width()/3,
            window_geometry.height()/5
        )

        self.drop_region_left_frame.setGeometry(
            0,
            window_geometry.height()/3,
            window_geometry.width()/5,
            window_geometry.height()/3
        )

        self.drop_region_right_frame.setGeometry(
            4 * window_geometry.width() / 5,
            window_geometry.height()/3,
            window_geometry.width()/5,
            window_geometry.height()/3
        )

        self.drop_region_bottom_frame.setGeometry(
            window_geometry.width() / 3,
            4 * window_geometry.height() / 5,
            window_geometry.width() / 3,
            window_geometry.height() / 5
        )

        self.drop_region_top_frame.show()
        self.drop_region_left_frame.show()
        self.drop_region_right_frame.show()
        self.drop_region_bottom_frame.show()

        self.drop_region_top_frame.raise_()
        self.drop_region_top_frame.updateGeometry()

    def hide_drop_regions(self):
        self.drop_region_top_frame.hide()
        self.drop_region_left_frame.hide()
        self.drop_region_right_frame.hide()
        self.drop_region_bottom_frame.hide()

    def over_drop_regions(self, pos):

        if self.drop_region_top_frame.geometry().contains(self.mapFromGlobal(pos)):
            return self.drop_region_top_frame
        elif self.drop_region_left_frame.geometry().contains(self.mapFromGlobal(pos)):
            return self.drop_region_left_frame
        elif self.drop_region_right_frame.geometry().contains(self.mapFromGlobal(pos)):
            return self.drop_region_right_frame
        elif self.drop_region_bottom_frame.geometry().contains(self.mapFromGlobal(pos)):
            return self.drop_region_bottom_frame
        else:
            return None

    def focus_drop_region(self, pos):
        active_region = self.over_drop_regions(pos)
        for drop_region in self.drop_regions.values():
            if drop_region is active_region:
                drop_region.setStyleSheet(self.drop_region_focused_stylesheet)
            else:
                drop_region.setStyleSheet(self.drop_region_stylesheet)


    def get_drop_region(self, key):
        return self.drop_regions[key]

    def _remove_child_window(self, child_window):
        self.child_windows.remove(child_window)

    def _add_child_window(self, child_window):
        self.child_windows.append(child_window)