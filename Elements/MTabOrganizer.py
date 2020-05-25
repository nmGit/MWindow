from PyQt5.QtWidgets import QTabWidget, QWidget
from PyQt5.QtCore import QEvent
from Elements.MHierarchicalElement import MHierarchicalElement
#from Elements.MContainer import MContainer
from Elements.MWindow import MWindow
from Elements.MTab import MTab

class MTabOrganizer(QTabWidget, MHierarchicalElement):
    def __init__(self):
        super().__init__()
        self.tabs = {}
        self.show()

        this_directory = '\\'.join(__file__.split('\\')[0:-1])
        self.setStyleSheet(

            "::pane"
            "{"
            "   border-right: 0.1em solid rgb(100,50,10);"
            "   border-top: 0.2em solid rgb(200,100,20);"
            "   margin-top: -0.2em"
            "}"
            "QTabBar{"
            "   color: rgb(230,230,230);"
            "   margin-top: 0.0em;"
            "}"
            "QTabBar:close-button {"
            "   image: url(../Assets/close-24px.svg);"
            "}"
            "QTabBar:close-button:hover {"
            "   background: rgb(150,50,50);"
            "}"
            "QTabBar::tab{"
            "    font: rgb(255,0,0);"
            "    border-top: 0.15em solid black;    "
            "    border-right: 0.1em solid black;    "
            "    padding-top: 0.3em;"
            "    padding-bottom: 0.3em;"
            "    padding-right: 0.3em;"
            "    padding-left: 0.3em;"
            "    margin-top: 0.2em;"
            "    border-top-left-radius: 4px;"
            "    border-top-right-radius: 4px;"
            "}"
            ""
            "QTabBar::tab:selected{"
            "    border-top: 0.2em solid rgb(200,100,20);    "
            "    border-right: 0.1em solid rgb(100,50,10);    "

            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
            "                                stop: 0 rgb(80, 80, 80),"
            "                                stop: 1 rgb(100,100,100)"
            "                                );"
            "    margin-top: 0.0em;"
            "    margin-left: -0.1em;"
            "    border-top-left-radius: 4px;"
            "    border-top-right-radius: 4px;"
            "}"
            "QTabBar::tab:!selected{"
            "    margin-bottom: 0.2em;"
            "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
            "                                stop: 0 rgb(50, 50, 50),"
            "                                stop: 1 rgb(80,80,80));"
            
       
            "}")
        self.setTabsClosable(True)
        self.tabBar().installEventFilter(self);

    def add_tab(self, widget, title):
        if not type(widget) is MTab:
            raise ValueError("Expected type %s, got type %s", str(MTab), str(type(widget)))


        self.tabs[title] = (self.addTab(widget, title), widget)

        widget.set_parent_he(self)

    def get_tab(self, index):
        for key, value in self.tabs.items():
            if value[0] == index:
                return value[1]

    def eventFilter(self, object, event):

        if event.type() == QEvent.MouseButtonPress or \
                event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.MouseMove:
            print("Got event:", type(event))
            print("it was a mouse event")

            # Ignoring the event will pass it to the parent.
            # Returning false will also pass the event to the children
            # We need to pass the event up the parent because MWindow needs to know about mouse presses
            # We also need to pass the event down the chain because this is what would happen without the event
            # filter and we do not intend to interfere with normal operation of the tabs.
            event.ignore()
        return False

    def remove_tab(self, index):
        self.removeTab(index)
        tab_key = None
        for key, value in self.tabs.items():
            if value[0] == index:
                tab_key = key
        del self.tabs[tab_key]


    def mousePressEvent(self,event):
        print("Tab organizer press")
        event.ignore()