from PyQt5.QtGui import QDrag, QCursor
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QToolButton, QSplitter
from PyQt5.QtCore import Qt
from . MHeaderBar import MHeaderBar
class MSplitter(QFrame):


    def __init__(self, parent = None):
        super().__init__(parent)
        self.setObjectName("main_frame")

        # Construct top-level window elements
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_splitter = QSplitter()
        self.main_splitter.setObjectName("main_splitter")
        self.main_splitter.show()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        #self.header_frame = MHeaderBar(self)

        #self.main_layout.addWidget(self.header_frame)
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
                                               "    background-color:rgb(50,50,50)"
                                               "}"
                           )

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)


    def add_content(self, content, location = None):
        if location is None:
            self.main_splitter.addWidget(content)

        elif location is "top":
            self.main_splitter.setOrientation(Qt.Vertical)
            self.main_splitter.insertWidget(0, content)

        elif location is "left":
            self.main_splitter.setOrientation(Qt.Horizontal)
            self.main_splitter.insertWidget(0, content)

        elif location is "right":
            self.main_splitter.setOrientation(Qt.Horizontal)
            self.main_splitter.insertWidget(1, content)

        elif location is "bottom":
            self.main_splitter.setOrientation(Qt.Vertical)
            self.main_splitter.insertWidget(1, content)

        self.updateGeometry()

    def get_num_widgets(self):
        return self.main_splitter.count()



