from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QAction, QPixmap
from .app import App

class Window(QMainWindow):
    '''GUI of the application'''
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("components/elements/layout.ui", self)
        
        # Initialize Icons
        self._appIcon           = QIcon("components/icons/icon.ico")
        self._appLogo           = QPixmap("components/icons/logo.png")
        self._mediaIcon         = QIcon("components/icons/media.png")
        
        # Window Attributes
        self.setWindowTitle("YoutubeDownloader")
        self.setWindowIcon(self._appIcon)
        self.setFixedSize(1051, 779)
        
        # Import Stylesheet
        with open("components/elements/stylesheet.qss", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())
        
        # Set app
        self.app = App()
        
        # Initialize Widgets
        self._initialize_widgets()
        self._initialize_pages()
        
        # Show Window
        self.show()
    
    def _initialize_widgets(self):
        '''Initializes the app's widgets'''
        #-- Navigation Buttons
        self.btn_home.clicked.connect(self.click_home)
        self.btn_history.clicked.connect(self.click_history)
        self.btn_media.clicked.connect(self.click_media)
        self.btn_media.setIcon(self._mediaIcon)
        self.btn_media.setIconSize(QSize(16, 16))
        
        #-- Home Buttons
        self.btn_go.clicked.connect(self.click_go)
        self.image_logo.setPixmap(self._appLogo)
        
    def _initialize_pages(self):
        # Set First Pages
        self.stack_pages.setCurrentWidget(self.page_home)
        
        # Set Sub-Pages
        self.stack_subpages.setCurrentWidget(self.subpage_logo)
    
    def _reset_page_forms(self, page):
        '''Clears the page's entry forms and lists'''
        children = [page.findChildren(QLineEdit), page.findChildren(QListWidget), page.findChildren(QTextEdit)]
        
        for widget in children:
            for child in widget:
                try:
                    child.clear()
                except:
                    pass
    
    #-- Widget Commands
    def click_home(self):
        self.stack_pages.setCurrentWidget(self.page_home)
    
    def click_history(self):
        self.stack_pages.setCurrentWidget(self.page_history)
    
    def click_settings(self):
        pass
    
    def click_go(self):
        try:
            url = self.entry_url.text()
            self.app.parse_url(url=url)
        except ConnectionRefusedError:
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("The URL slot cannot be empty!")
            error.exec()
    
    def click_media(self):
        self.app.open_folder(folder="media")