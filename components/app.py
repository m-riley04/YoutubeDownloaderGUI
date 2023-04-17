from .helpers import open_path
from .youtubedownloader import YoutubeDownloader
import os

class App:
    def __init__(self):
        self.downloader = YoutubeDownloader()
    
    def set_extension(self, extension):
        
    
    def open_folder(self, folder=""):
        open_path(fr"{os.getcwd()}\{folder}")
        
    def parse_url(self, url:str):
        if url == "":
            raise ConnectionRefusedError("URL cannot be empty")
        