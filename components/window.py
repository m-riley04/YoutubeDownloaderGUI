from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QAction, QPixmap
from time import sleep
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
        
        # Temp Variables
        self._itags = []
        self._selectedRow = 0
        self._urls = []
        
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
        self.table_streams.itemClicked.connect(self.click_stream)
        self.table_streams.itemDoubleClicked.connect(self.click_stream)
        self.table_history.itemClicked.connect(self.click_historyItem)
        self.btn_save.clicked.connect(self.click_save)
        self.btn_saveToFolder.clicked.connect(self.click_saveToFolder)
        self.btn_clearHistory.clicked.connect(self.click_clearHistory)
        self.btn_loadURL.clicked.connect(self.click_loadURL)
        
    def _initialize_pages(self):
        # Set First Pages
        self.stack_pages.setCurrentWidget(self.page_home)
        
        # Set Sub-Pages
        self.stack_subpages.setCurrentWidget(self.subpage_logo)
        
    def _initialize_video_preview(self):
        for i in range(5):
            try:
                thumbnail   = QPixmap("")
                thumbnail.loadFromData(self.app.get_thumbnail_url())
                videoURL    = self.app.get_url()
                title       = self.app.get_title()
                channel     = self.app.get_channel()
                channelURL  = self.app.get_channel_url()
                duration    = self.app.get_duration()
            except:
                print(f"Error when initializing video preview (try #{i+1})")
                self.image_videoThumbnail.setPixmap()
                self.label_videoTitle.setText("Title")
                self.label_videoChannel.setText("Channel")
                self.label_videoDuration.setText("Duration")
            else:
                self.image_videoThumbnail.setPixmap(thumbnail)
                self.label_videoTitle.setText(title)
                self.label_videoChannel.setText(channel)
                self.label_videoDuration.setText(duration)
                return
        
    def _initialize_history(self):
        pass
        
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
                    child.setPixmap(QPixmap())
                except:
                    pass
                
    def populate_list(self, list, data):
        for i, value in enumerate(data):
            list.addItem(str(value))
            
    def populate_downloads(self, table, data, i=0):
        # Remove all previous downloads
        for i, tag in enumerate(self._itags):
            table.removeRow(0)
        self._itags = []
        table.clearContents()
        
        # Load new downloads
        try:
            for row, value in enumerate(data):
                format = "Any"
                extension = value.subtype
                bitrate = value.bitrate
                size = value.filesize_mb
                resolution = value.resolution
                audioCodec = value.audio_codec
                videoCodec = value.video_codec
                itag = value.itag
                videoProps = [format, extension, bitrate, size, resolution, audioCodec, videoCodec, itag]
                
                self._itags.append(int(itag))
                table.insertRow(row)
                
                # Set each cell's value
                for col, prop in enumerate(videoProps):
                    table.setItem(row, col, QTableWidgetItem(str(prop)))
        except:
            print(f"ERROR: Streams were unable to generate. Trying again... (#{i+1})")
            if i < 20:
                self.populate_downloads(list, data, i+1)
            else:
                error = QMessageBox()
                error.setWindowTitle("ERROR")
                error.setText("Unable to generate streams. Please try again.")
                error.exec()
            
    def populate_history(self, table, data):
        # Remove all previous histories
        for i, url in enumerate(self._urls):
            table.removeRow(0)
        self._urls = []
        table.clearContents()
            
        # Load new histories
        for row, value in enumerate(data):
            self._urls.append(value.url)
            table.insertRow(row)
            
            videoProps = [value.date, value.url]
            # Set each cell's value
            for col, prop in enumerate(videoProps):
                table.setItem(row, col, QTableWidgetItem(prop))
        
    '''
    =======================
        Widget Commands
    =======================
    '''
    #-- Buttons
    def navigate(self, stack, page):
        stack.setCurrentWidget(page)
    
    def click_home(self):
        self.clear_fields(self.page_home)
        self.navigate(self.stack_pages, self.page_home)
        self.navigate(self.stack_subpages, self.subpage_logo)
    
    def click_history(self):
        self.populate_history(self.table_history, self.app.get_history())
        if self.table_history.selectedItems() == []:
            self.btn_loadURL.setEnabled(False)
        self.navigate(self.stack_pages, self.page_history)
    
    def click_settings(self):
        self.navigate(self.stack_pages, self.page_settings)
    
    def click_go(self, __i=0):
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
            if __i < 5:
                sleep(1)
                return self.click_go(__i+1)
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("An unexpected error has occurred. Please try again.")
            error.exec()
            
        else:
            try:
                self.populate_downloads(self.table_streams, self.app.get_streams())
                self.app.add_to_history(url)
            except:
                error = QMessageBox()
                error.setWindowTitle("ERROR")
                error.setText("Unable to generate streams. Please try again.")
                error.exec()
            else:
                self._initialize_video_preview()
                self.navigate(self.stack_pages, self.page_streams)
            
    def click_media(self):
        self.app.open_folder(folder="media")
    
    def click_stream(self):
        self._selectedRow = self.table_streams.currentRow()
    
    def click_column(self):
        pass
    
    def click_save(self):
        try:
            self.app.download_video(self._itags[self._selectedRow])
        except:
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("The download could not be completed. Please try again.")
            error.exec()
        else:
            message = QMessageBox()
            message.setWindowTitle("Success!")
            message.setText("The file has been successfully downloaded to your selected media folder!")
            message.exec()
            
    def click_saveToFolder(self):
        try:
            self.app.download_video(self._itags[self._selectedRow], QFileDialog.getExistingDirectory(self, "Select a folder"))
        except:
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("The download could not be completed. Please try again.")
            error.exec()
        else:
            message = QMessageBox()
            message.setWindowTitle("Success!")
            message.setText("The file has been successfully downloaded to your selected folder!")
            message.exec()
    
    def click_clearHistory(self):
        for i, url in enumerate(self._urls):
            self.table_history.removeRow(0)
        self._urls = []
        self.table_history.clearContents()
        self.app.clear_history()
    
    def click_loadURL(self, __i=0):
        try:
            url = self._urls[self.table_history.selectedItems()[0].row()]
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
            if __i < 5:
                sleep(1)
                return self.click_loadURL(__i+1)
            error = QMessageBox()
            error.setWindowTitle("ERROR")
            error.setText("An unexpected error has occurred. Please try again.")
            error.exec()
        else:
            try:
                self.app.add_to_history(url)
                self.populate_downloads(self.table_streams, self.app.get_streams())
            except:
                error = QMessageBox()
                error.setWindowTitle("ERROR")
                error.setText("Unable to generate streams. Please try again.")
                error.exec()
            else:
                self._initialize_video_preview()
                self.navigate(self.stack_pages, self.page_streams)
                
    def click_historyItem(self):
        self.btn_loadURL.setEnabled(True)
    
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