from .helpers import open_path
from .youtubedownloader import YoutubeDownloader
from .videohistory import VideoHistory

import os, requests

class App:
    def __init__(self):
        self.downloader = YoutubeDownloader()
        self.history = VideoHistory()
    
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
    
    def get_streams(self, i=0):
        return self.downloader.get_filtered_streams()
    
    def download_video(self, itag:int, path:str=f"{os.getcwd()}/media"):
        return self.downloader.download_stream(self.downloader.get_stream(itag=itag), path)
    
    def clear_history(self):
        return self.history.clear()
        
    def get_history(self):
        return self.history.get()
    
    def add_to_history(self, url:str):
        return self.history.add(url)
    
    def open_folder(self, folder=""):
        '''Opens a folder at a specific path'''
        folder = fr"{folder}"
        open_path(fr"{os.getcwd()}\{folder}")
        
    def parse_url(self, url:str):
        '''Parses a url into the YoutubeDownloader class'''
        if url == "":
            raise ConnectionRefusedError("URL cannot be empty")
        
        self.downloader.set_video(url=url)
        