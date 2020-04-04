from Elements.MWindowManager import MWindowManager

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFontDialog, QFileDialog, QColorDialog
app = QApplication([])

window_manager = MWindowManager()

color_dialog = QColorDialog()

file_dialog = QFileDialog()


font_dialog = QFontDialog()


label = QLabel("Hello, World!")



window_manager.add_window(label)
window_manager.add_window(font_dialog)
window_manager.add_window(file_dialog)
window_manager.add_window(color_dialog)


window_manager.show()

font_dialog.show()
file_dialog.show()
label.show()

app.exec_()