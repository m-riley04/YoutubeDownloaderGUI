from .pastvideo import PastVideo
import os

class VideoHistory:
    def __init__(self):
        self.history = []
        
        self._load()
        
    def add(self, videoURL:str):
        self.history.append(PastVideo(url=videoURL))
        self._save()
        
    def get(self):
        self._load()
        return self.history
    
    def clear(self):
        self.history = []
        file = open(f"{os.getcwd()}/user_data/history.txt", "w")
        file.close()
            
    def _save(self):
        file = open(f"{os.getcwd()}/user_data/history.txt", "w")
        for video in self.history:
            file.write(f"{video.url}\t{video.date}\n")
        file.close()
            
    def _load(self):
        _temp = []
        if os.path.exists(f"{os.getcwd()}/user_data/history.txt"):
            with open(f"{os.getcwd()}/user_data/history.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    line = line.split("\t")
                    _temp.append(PastVideo(url=line[0], date=line[1]))
                file.close()
        self.history = _temp