from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QToolButton, QSplitter, QLabel
from PyQt5.QtGui import QPixmap, QIcon



class MHeaderBar(QFrame):
    def __init__(self, window):
        super().__init__()
        self.header_layout = QHBoxLayout()
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("header_frame")
        self.setStyleSheet("#header_frame{"
                           "    border-bottom: 2px solid black;"
                           "    background-color: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 rgb(50,50,50), stop:1 rgb(100,100,100))"
                           "}")
        # Construct header bar
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.header_layout)

        self.title_label = QLabel()
        self.title_label.setStyleSheet(".QLabel{"
                                       "    font: bold System;"
                                       "    font-size: 18px; "
                                       "    color: rgb(220,220,220);"
                                       "}")
        self.title_label.setMouseTracking(True)

        self.header_layout.addWidget(self.title_label)

        self.header_layout.addStretch(3)

        self.minimize_button = QPushButton()
        self.minimize_button.setFlat(True)
        minimize_pixmap = QPixmap("../Assets/minimize-24px.svg");
        minimize_icon = QIcon(minimize_pixmap)
        self.minimize_button.setStyleSheet(".QPushButton{background-color: rgb(150,150,50)}")
        self.minimize_button.setIcon(minimize_icon)
        self.header_layout.addWidget(self.minimize_button)

        self.fullscreen_button = QPushButton()
        self.fullscreen_button.setFlat(True)
        fullscreen_pixmap = QPixmap("../Assets/fullscreen-24px.svg");
        fullscreen_icon = QIcon(fullscreen_pixmap);
        self.fullscreen_button.setStyleSheet(".QPushButton{background-color: rgb(50,150,50)}")
        self.fullscreen_button.setIcon(fullscreen_icon)
        self.header_layout.addWidget(self.fullscreen_button)


        self.exit_button = QPushButton()
        self.exit_button.setFlat(True)
        close_pixmap = QPixmap("../Assets/close-24px.svg");
        exit_icon = QIcon(close_pixmap);
        self.exit_button.setStyleSheet(".QPushButton{background-color: rgb(150,50,50)}")
        self.exit_button.setIcon(exit_icon)
        self.header_layout.addWidget(self.exit_button)

        self.setMinimumHeight(24)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        self.exit_button.show()
        self.show()
        self.window = window

        self.setMouseTracking(True)
        # Create drag handler

    def getWindow(self):
        return self.window

    def setTitle(self, title):
        self.title_label.setText(title)

    def getTitle(self):
        return self.title_label.text()

    def mousePressEvent(self, event):
        self.setStyleSheet("#header_frame{"
                           "    border-bottom: 2px solid black;"
                           "    background-color: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 rgb(50,50,50), stop:1 rgb(200,200,200))"
                           "}")
        event.ignore()

    def mouseReleaseEvent(self, event):
        self.setStyleSheet("#header_frame{"
                           "    border-bottom: 2px solid black;"
                           "    background-color: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 rgb(50,50,50), stop:1 rgb(100,100,100))"
                           "}")
        event.ignore()