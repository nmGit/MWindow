
from Management.MWindowManager import MWindowManager
from Widgets.DictionaryViewer import DicionaryViewer
import atexit
from PyQt5.QtWidgets import QApplication, QLabel, QFontDialog, QFileDialog, QColorDialog


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



#window_manager.add_window(label, "Hello world")
#window_manager.add_window(font_dialog, "Fonts")
#window_manager.add_window(file_dialog, "Files")
#indow_manager.add_window(color_dialog, "Colors")
#indow_manager.add_window(win_hierarchy_viewer, "Window Hierarchy")

item_dict = {
             1: (label, "Hello world"),
             2: (font_dialog, "Fonts"),
             3: (file_dialog, "Files"),
             4: (color_dialog, "Colors"),
             5: (win_hierarchy_viewer, "Window Hierarchy")}

window_manager.show()

font_dialog.show()
file_dialog.show()
label.show()


def hello():
    print("Hello!")
    f = open("ui.txt", "r")
    ser_data = f.read()
    print(ser_data)
    f.close()

    window_manager.deserialize(ser_data, item_dict)

@atexit.register
def goodbye():
    win_serial = window_manager.serialize()
    f = open("ui.txt", "w")
    f.truncate()
    f.write(str(win_serial))
    f.close()
    print("Bye!")

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":

    import sys
    sys.excepthook = except_hook

hello()
app.exec_()