from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QAction, QPixmap
from .app import App

class Window(QMainWindow):
    '''GUI of the application'''
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("components/elements/layout.ui", self)
        
        # Window Attributes
        APP_ICON = QIcon("components/icons/icon.ico")
        self.setWindowTitle("YoutubeDownloader")
        self.setWindowIcon(APP_ICON)
        
        # Import Stylesheet
        with open("components/elements/stylesheet.qss", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())
        
        # Set app
        self.app = App()
        
        # Show Window
        self.show()