
from Elements.MWindowManager import MWindowManager

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFontDialog, QFileDialog, QColorDialog
app = QApplication([])

window_manager = MWindowManager()

color_dialog = QColorDialog()

file_dialog = QFileDialog()


font_dialog = QFontDialog()


label = QLabel("Hello, World!")



window_manager.add_window(label, "Hello world")
window_manager.add_window(font_dialog, "Fonts")
window_manager.add_window(file_dialog, "Files")
window_manager.add_window(color_dialog, "Colors")

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