from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

class DicionaryViewer(QTreeWidget):
    def __init__(self):
        super().__init__()

    def fill_item(self, item, value):
        item.setExpanded(True)
        if type(value) is dict:
            for key, val in sorted(value.items()):
                child = QTreeWidgetItem()
                child.setText(0, str(key))
                item.addChild(child)
                self.fill_item(child, val)
        elif type(value) is list:
            for val in value:
                child = QTreeWidgetItem()
                item.addChild(child)
                if type(val) is dict:
                    child.setText(0, '[dict]')
                    self.fill_item(child, val)
                elif type(val) is list:
                    child.setText(0, '[list]')
                    self.fill_item(child, val)
                else:
                    child.setText(0, str(val))
                child.setExpanded(True)
        else:
            child = QTreeWidgetItem()
            child.setText(0, str(value))
            item.addChild(child)

    def fill_widget(self, value):
        self.clear()
        self.fill_item(self.invisibleRootItem(), value)