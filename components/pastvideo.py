import datetime
class PastVideo:
    def __init__(self, url, date=datetime.date.today().strftime("%m/%d/%Y")):
        self.date = date
        self.url = url
        
    def get(self):
        '''Returns a tuple of the date and url'''
        return (self.date, self.url)
        
    def __str__(self):
        return f"{self.date} - {self.url}"
    
    def __repr__(self):
        return f"PastVideo(url='{self.url}', date='{self.date}')"
    
    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.url == other.url and self.date == other.date
        else:
            return self == other