# from PyQt5.QtWidgets import QFrame, QVBoxLayout
#
# from Elements.MHierarchicalElement import MHierarchicalElement
#
# class MContainer(QFrame):
#     def __init__(self, contents):
#         super().__init__()
#         self.contents = contents
#         self.main_layout = QVBoxLayout()
#         self.setLayout(self.main_layout)
#         self.main_layout.addWidget(contents)
#
#         self.main_layout.setContentsMargins(0, 0, 0, 0)
#         self.setStyleSheet(".QFrame{border: 0};")
#
#         self.uid = None
#
#     def get_content(self, *args):
#         return self.contents
#
#     def set_uid(self, uid):
#         self.uid = uid
#
#     def get_uid(self):
#         return self.uid