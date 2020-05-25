from PyQt5.QtWidgets import QFrame, QVBoxLayout, QSizePolicy, QSplitter
from PyQt5.QtCore import Qt
from Elements.MHierarchicalElement import MHierarchicalElement
#from Elements.MContainer import MContainer
from Elements.MWindow import MWindow

class MSplitter(QFrame, MHierarchicalElement):

    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'

    def __init__(self, parent_window):
        super().__init__()
        self.setObjectName("main_frame")

        # Construct top-level window elements
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.parent_container = None

        #self.set_parent_he(parent_window)

        self.main_splitter = QSplitter()
        self.main_splitter.setObjectName("main_splitter")
        self.main_splitter.show()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        #self.header_frame = MHeaderBar(self)

        #self.main_layout.addWidget(self.header_frame)
        self.content = self.main_splitter
        self.main_layout.addWidget(self.main_splitter)
        self.show()

        self.setStyleSheet(self.styleSheet() + "QFrame#main_frame{background-color:rgb(200,200,200)}\r\n"
                                               "QSplitter::handle#main_splitter"
                                               "{"
                                               "    border: 2px solid rgb(50,50,50);"
                                               "    background-color:rgb(100,100,100)"
                                               "}"
                                               "QSplitter::handle:pressed#main_splitter"
                                               "{"
                                               "    border: 2px solid rgb(100,100,100);"
                                               "    background-color:rgb(200,100,20)"
                                               "}"
                           )

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.orientation = None

    def set_sizes(self, one, two):
        self.main_splitter.setSizes([one, two])

    def get_sizes(self):
        return self.main_splitter.sizes()

    def add_content(self, container, location = None):

        # if not (type(container) is MContainer):
        #     raise TypeError("Expected type %s, got %s" % (str(MWindow), type(container)))

        if location is None:
            self.main_splitter.addWidget(container)

        elif location is "top":
            self.main_splitter.setOrientation(Qt.Vertical)
            self.main_splitter.insertWidget(0, container)
            self.orientation = self.VERTICAL

        elif location is "left":
            self.main_splitter.setOrientation(Qt.Horizontal)
            self.main_splitter.insertWidget(0, container)
            self.orientation = self.HORIZONTAL

        elif location is "right":
            self.main_splitter.setOrientation(Qt.Horizontal)
            self.main_splitter.insertWidget(1, container)
            self.orientation = self.HORIZONTAL

        elif location is "bottom":
            self.main_splitter.setOrientation(Qt.Vertical)
            self.main_splitter.insertWidget(1, container)
            self.orientation = self.VERTICAL

        container.set_parent_he(self.get_parent_he())
        self.updateGeometry()

    def get_orientation(self):
        return self.orientation

    def get_position(self):
        return self.main_splitter.sizes()

    def get_num_widgets(self):
        return self.main_splitter.count()

    def get_item_at(self, index):
        return self.main_splitter.widget(index)
    #
    # def get_parent_container(self):
    #     return self.parent_container
    #
    # def set_parent_container(self, win):
    #
    #     if type(win) is MWindow or win is None:
    #
    #         # Remove self from old parent
    #         if self.parent_container is not None:
    #             self.parent_container._remove_child_container(self)
    #
    #         # Add self to new parent
    #         if (win is not None):
    #             win._add_child_container(self)
    #
    #         # Set local reference to parent
    #         self.parent_container = win
    #
    #     else:
    #         raise TypeError("Parent window must be type %s, not %s" % (str(type(MWindow)), str(type(win))))

    def show_drop_regions(self):
        pass
    def hide_drop_regions(self):
        pass
