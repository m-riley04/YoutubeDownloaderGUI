from .helpers import open_path
from .youtubedownloader import YoutubeDownloader
import os, requests

class App:
    def __init__(self):
        self.downloader = YoutubeDownloader()
    
    def set_extension(self, extension):
        '''Sets the extension of the Youtube filter'''
        self.downloader.set_extension(extension=extension)
        
    def set_format(self, format):
        '''Sets the format of the Youtube filter'''
        self.downloader.set_format(format=format)
    
    def get_info(self):
        return self.downloader.get_info()
        
    def get_thumbnail_url(self):
        return requests.get(self.downloader.get_thumbnail_url()).content
    
    def get_url(self):
        return self.downloader.get_url()
    
    def get_title(self):
        return self.downloader.get_title()
    
    def get_description(self):
        return self.downloader.get_description()
    
    def get_channel(self):
        return self.downloader.get_channel()
    
    def get_channel_url(self):
        return self.downloader.get_channel_url()
    
    def get_duration(self):
        return str(self.downloader.get_duration())
    
    def get_filesize(self):
        return self.downloader.get_filesize()
    
    def open_folder(self, folder=""):
        '''Opens a folder at a specific path'''
        folder = fr"{folder}"
        open_path(fr"{os.getcwd()}\{folder}")
        
    def parse_url(self, url:str):
        '''Parses a url into the YoutubeDownloader class'''
        if url == "":
            raise ConnectionRefusedError("URL cannot be empty")
        
        self.downloader.set_video(url=url)
        