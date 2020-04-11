
from Elements.MWindowManager import MWindowManager
from Widgets.DictionaryViewer import DicionaryViewer

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFontDialog, QFileDialog, QColorDialog

def refresh_win_heirarchy():
    win_hierarchy_viewer.fill_widget(window_manager.get_window_hierarchy())


app = QApplication([])

window_manager = MWindowManager()

color_dialog = QColorDialog()

file_dialog = QFileDialog()

win_hierarchy_viewer = DicionaryViewer()
window_manager.window_hierarchy_updated_sig.connect(refresh_win_heirarchy)

font_dialog = QFontDialog()


label = QLabel("Hello, World!")



window_manager.add_window(label, "Hello world")
window_manager.add_window(font_dialog, "Fonts")
window_manager.add_window(file_dialog, "Files")
window_manager.add_window(color_dialog, "Colors")
window_manager.add_window(win_hierarchy_viewer, "Window Hierarchy")

window_manager.show()

font_dialog.show()
file_dialog.show()
label.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":

    import sys
    sys.excepthook = except_hook

app.exec_()