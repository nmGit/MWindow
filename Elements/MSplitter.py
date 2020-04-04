from PyQt5.QtGui import QDrag, QCursor
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QToolButton, QSplitter
from Elements.MHeaderBar import MHeaderBar
class MSplitWindow(QFrame):


    def __init__(self, parent = None):
        super().__init__(parent)
        self.setObjectName("main_frame")
        # Construct top-level window elements
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_splitter = QSplitter()
        self.main_splitter.show()
        self.main_layout.setContentsMargins(0, 0, 0, 0)


        self.header_frame = MHeaderBar(self)

        self.main_layout.addWidget(self.header_frame)
        self.main_layout.addWidget(self.main_splitter)
        self.show()

        self.setStyleSheet(self.styleSheet() + "QFrame#main_frame{border: 2px solid green}\r\n"
                                               "QFrame#main_frame{background-color:rgb(200,200,200)}")
        self.setMinimumSize(1000,1000)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    def add_content(self, content):
        self.main_splitter.addWidget(content)

