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
        self._goIcon            = QIcon("components/icons/play.png")
        
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
        self.btn_go.setIcon(self._goIcon)
        self.btn_go.setIconSize(QSize(16, 16))
        self.image_logo.setPixmap(self._appLogo)
        
        #-- Other
        self.entry_url.editingFinished.connect(self.typed_url)
        self.list_streams.itemDoubleClicked.connect(self.click_stream)
        
    def _initialize_pages(self):
        # Set First Pages
        self.stack_pages.setCurrentWidget(self.page_home)
        
        # Set Sub-Pages
        self.stack_subpages.setCurrentWidget(self.subpage_logo)
        
    def _initialize_video_preview(self):
        for i in range(5):
            try:
                thumbnail   = QPixmap()
                thumbnail.loadFromData(self.app.get_thumbnail_url())
                videoURL    = self.app.get_url()
                title       = self.app.get_title()
                channel     = self.app.get_channel()
                channelURL  = self.app.get_channel_url()
                duration    = self.app.get_duration()
            except:
                print(f"Error when initializing video preview (try #{i+1})")
                self.stack_subpages.setCurrentWidget(self.subpage_error)
            else:
                self.image_videoThumbnail.setPixmap(thumbnail)
                self.label_videoTitle.setText(title)
                self.label_videoChannel.setText(channel)
                self.label_videoDuration.setText(duration)
                return
        
        
        #error = QMessageBox()
        #error.setWindowTitle("ERROR")
        #error.setText("There was an error when trying to retrieve the video's data. Please try again.")
        #error.exec()
        
        
    
    #-- Populating/Clearing
    def clear_fields(self, parent):
        '''Clears the parent's entry forms and lists'''
        children = [parent.findChildren(QLineEdit), parent.findChildren(QTextEdit)]
        
        for widget in children:
            for child in widget:
                try:
                    child.clear()
                except:
                    pass
                
    def clear_images(self, parent):
        children = [parent.findChildren(QLabel)]
        for widget in children:
            for child in widget:
                try:
                    child.setPixmap()
                except:
                    pass
                
    def populate_list(self, list, data):
        for i, value in enumerate(data):
            list.addItem(value)
    
    '''
    =======================
        Widget Commands
    =======================
    '''
    #-- Buttons
    def click_home(self):
        self.clear_fields(self.page_home)
        self.stack_pages.setCurrentWidget(self.page_home)
        self.stack_subpages.setCurrentWidget(self.subpage_logo)
    
    def click_history(self):
        self.stack_pages.setCurrentWidget(self.page_history)
    
    def click_settings(self):
        pass
    
    def click_go(self):
        self.clear_fields(self.frame_video)
        self.clear_images(self.frame_video)
        try:
            url = self.entry_url.text()
            self.app.parse_url(url=url)
        except ConnectionRefusedError:
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("The URL slot cannot be empty!")
            error.exec()
        except ValueError:
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("Please enter a valid URL!")
            error.exec()
        except:
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("An unexpected error has occurred. Please try again.")
            error.exec()
        else:
            self.populate_list(self.list_streams, [])
            self.stack_pages.setCurrentWidget(self.page_streams)
            
            
    
    def click_media(self):
        self.app.open_folder(folder="media")
    
    def click_stream(self):
        pass
    
    def click_video(self):
        pass
    
    # Text Fields
    def typed_url(self):
        try:
            url = self.entry_url.text()
            self.app.parse_url(url=url)
        except ConnectionRefusedError:
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("The URL slot cannot be empty!")
            error.exec()
        except ValueError:
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("Please enter a valid URL!")
            error.exec()
        except:
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("An unexpected error has occurred. Please try again.")
            error.exec()
        else:
            self._initialize_video_preview()
            self.stack_subpages.setCurrentWidget(self.subpage_video)