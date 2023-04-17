from .helpers import open_path
import os

class App:
    def __init__(self):
        pass
    
    def open_folder(self, folder=""):
        open_path(fr"{os.getcwd()}\{folder}")
        
    def parse_url(self, url:str):
        if url == "":
            raise ConnectionRefusedError("URL cannot be empty")
        