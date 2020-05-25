from PyQt5.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from Elements.MHeaderBar import MHeaderBar
from Elements.MHierarchicalElement import MHierarchicalElement
#from Elements.MContainer import MContainer

class MWindow(QFrame, MHierarchicalElement):

    def __init__(self, content, title):
        super().__init__()

        # if not (type(content) is MContainer):
        #     raise TypeError("Expected type %s, got %s" % (str(MContainer), type(content)))
        self.content = content
        content.setMouseTracking(True)
        self.setObjectName("main_m_window_frame")
        # Construct top-level window elements

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)

        self.header_frame = MHeaderBar(self)
        self.header_frame.setTitle(title)

        self.main_layout.addWidget(self.header_frame)
        self.main_layout.addStretch(0)
        self.main_layout.addWidget(self.content)
        self.main_layout.setStretchFactor(self.content, 1)

        self.show()

        self.setStyleSheet(self.styleSheet() + "QFrame#main_m_window_frame{border: 2px solid black}\r\n"
                                               "QFrame#main_m_window_frame{background-color:rgb(120,120,130)}")

        self.drop_region_top_frame = QFrame(self)
        self.drop_region_left_frame = QFrame(self)
        self.drop_region_right_frame = QFrame(self)
        self.drop_region_bottom_frame = QFrame(self)
        self.drop_region_onto_frame = QFrame(self)

        self.drop_region_stylesheet = "background-color: rgba(50, 50, 150, 0);"
        self.drop_region_focused_stylesheet = "background-color: rgba(50, 50, 80, 100);" \
                                 "border: 2px solid grey"

        self.drop_region_top_frame.setStyleSheet(self.drop_region_stylesheet)
        self.drop_region_left_frame.setStyleSheet(self.drop_region_stylesheet)
        self.drop_region_right_frame.setStyleSheet(self.drop_region_stylesheet)
        self.drop_region_bottom_frame.setStyleSheet(self.drop_region_stylesheet)
        self.drop_region_onto_frame.setStyleSheet(self.drop_region_stylesheet)

        self.drop_regions = {"top": self.drop_region_top_frame,
                             "left": self.drop_region_left_frame,
                             "right": self.drop_region_right_frame,
                             "bottom": self.drop_region_bottom_frame,
                             "onto": self.drop_region_onto_frame}
        self.setMinimumHeight(24)
        self.setMinimumWidth(128)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.uid = None

    def get_content(self):
        return self.content

    def set_title(self, title):
        self.header_frame.setTitle(title)

    def get_title(self):
        return self.header_frame.getTitle()

    def show_drop_regions(self):
        window_geometry = self.geometry()

        self.drop_region_top_frame.setGeometry(
            0,
            0,
            window_geometry.width(),
            window_geometry.height()/5
        )

        self.drop_region_left_frame.setGeometry(
            0,
            0,
            window_geometry.width()/5,
            window_geometry.height()
        )

        self.drop_region_right_frame.setGeometry(
            4 * window_geometry.width() / 5,
            0,
            window_geometry.width()/5,
            window_geometry.height()
        )

        self.drop_region_bottom_frame.setGeometry(
            0,
            4 * window_geometry.height() / 5,
            window_geometry.width(),
            window_geometry.height() / 5
        )

        self.drop_region_onto_frame.setGeometry(
            1 * window_geometry.width() / 3,
            1 * window_geometry.height() / 3,
            window_geometry.width() / 3,
            window_geometry.height() / 3
        )

        self.drop_region_top_frame.show()
        self.drop_region_left_frame.show()
        self.drop_region_right_frame.show()
        self.drop_region_bottom_frame.show()
        self.drop_region_onto_frame.show()

        self.drop_region_top_frame.raise_()
        self.drop_region_top_frame.updateGeometry()

    def hide_drop_regions(self):
        #print("hiding drop regions of", str(self))
        for child in self.child_containers:
            child.hide_drop_regions()
        self.drop_region_top_frame.hide()
        self.drop_region_left_frame.hide()
        self.drop_region_right_frame.hide()
        self.drop_region_bottom_frame.hide()
        self.drop_region_onto_frame.hide()

    def over_drop_regions(self, pos):

        if self.drop_region_top_frame.geometry().contains(self.mapFromGlobal(pos)):
            return self.drop_region_top_frame
        elif self.drop_region_left_frame.geometry().contains(self.mapFromGlobal(pos)):
            return self.drop_region_left_frame
        elif self.drop_region_right_frame.geometry().contains(self.mapFromGlobal(pos)):
            return self.drop_region_right_frame
        elif self.drop_region_bottom_frame.geometry().contains(self.mapFromGlobal(pos)):
            return self.drop_region_bottom_frame
        elif self.drop_region_onto_frame.geometry().contains(self.mapFromGlobal(pos)):
            return self.drop_region_onto_frame
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



    def __str__(self):
        return self.get_title()