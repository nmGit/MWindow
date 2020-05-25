from PyQt5.QtWidgets import QVBoxLayout, QFrame

from Elements.MHierarchicalElement import MHierarchicalElement
#from Elements.MContainer import MContainer

class MTab(QFrame, MHierarchicalElement):
    def __init__(self, content):
        super().__init__()
        #self.setContentsMargins(0,0,0,0)
        #self.setStyleSheet("margin-top: 0px")
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(content)
        self.content = content

    def get_content(self):
        return self.content