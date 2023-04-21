import pytube as pt

class YoutubeDownloader:
    def __init__(self):
        self._youtube           = None
        self._url               = None
        self._filtersEnabled    = False
        self._splitChannels     = False
        self._onlyOne           = False
        self._chosenType        = False
        self._extension         = None
        self._format            = None
        self._streams           = None
        self._downloads         = []
        
    def set_video(self, url):
        '''Sets the video to search for'''
        try:
            self._url = url
            self._youtube = pt.YouTube(url=url)
        except:
            raise ValueError("Invalid URL.")
        
    def set_extension(self, extension:str):
        '''Sets the filtered extension'''
        self._extension = extension
        
    def set_format(self, format):
        '''Sets the filtered format'''
        self._format = format
        
    def set_splitChannels(self, splitChannels:bool):
        '''Sets the filtered channel'''
        self._splitChannels = splitChannels
        
    def get_url(self):
        return self._url
        
    def get_thumbnail_url(self):
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.thumbnail_url
    
    def get_title(self):
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.title
    
    def get_description(self):
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.description
    
    def get_channel(self):
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.author
    
    def get_channel_url(self):
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.channel_url
    
    def get_duration(self) -> int:
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.length
    
    def get_publish_date(self):
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.publish_date
    
    def get_rating(self):
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.rating
    
    def get_views(self):
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.views
    
    def get_keywords(self):
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.keywords
    
    def get_avaliability(self):
        try:
            return self._youtube.check_availability()
        except:
            pass
    
    def get_info(self):
        if self._youtube == None:
            raise ValueError("Video not set.")
        return self._youtube.vid_info
    
    def initialize_yt(self, url):
        '''Attempts to create the Youtube object with the passed URL. If it URL is not valid, it raises a ValueError. Otherwise, it returns the Youtube object.'''
        try:
            self._youtube = pt.YouTube(url=url)
        except:
            raise ValueError("Invalid URL.")
        else:
            return self._youtube
        
    def initialize_directory(self, outputPath):
        '''Takes an output path for the downloaded videos. Returns the output path.'''
        self._output = outputPath
        return self._output
    
    def get_filtered_streams(self):
        self._streams = self._youtube.streams.filter()
        return self._streams
    
    def get_stream(self, itag:int):
        return self._streams.get_by_itag(itag)
    
    def download_stream(self, stream:pt.Stream, outputPath:str):
        return stream.download(output_path=outputPath)

    def try_filters(self, filtersEnabled:bool, splitChannels:bool, extension:str, chosenType:bool, maxAttempts=3):
        '''Takes in a boolean for filters enabled, split channels, chosen type, and a string for the extension. Returns a Stream object.'''
        for i in range(maxAttempts):
            try:
                if filtersEnabled:
                    if splitChannels:
                        return self._youtube.streams.filter(progressive=not splitChannels, adaptive=splitChannels, file_extension=extension, only_audio=chosenType, only_video=not chosenType)
                    else:
                        return self._youtube.streams.filter(progressive=not splitChannels, adaptive=splitChannels, file_extension=extension)
                else:
                    return self._youtube.streams.filter()
            except:
                print(f"ERROR: returning YouTube stream filter. Retrying... (Attempt #{i+1})")
        
        # If it does not return in time...
        raise RuntimeError("ERROR: YouTube stream filter did not return in time.")

    def create_download_list(self, streams, maxAttempts=3):
        '''Returns a list of all possible YouTube downloads'''
        count = 0
        for retry in range(maxAttempts):
            try:
                options = {}
                for i, stream in enumerate(streams):
                    options[str(i+1)] = stream.itag
                    if stream.type == "video":
                        print(f"{i+1}) Type: {stream.type} - Extension: {stream.subtype} - Resolution: {stream.resolution} - FPS: {stream.fps} - Video Codec: {stream.video_codec} - Audio Codec: {stream.audio_codec}")
                    else:
                        print(f"{i+1}) Type: {stream.type} - Extension: {stream.subtype} - Bitrate: {stream.abr} - Audio Codec: {stream.audio_codec}")
                    count = i
                if count == 0:
                    print("RESULTS: No downloads were found matching that filter.")
                    break
            except:
                print(f"ERROR: There was an error creating the downloads list. Retrying... (Attempt #{retry+1})")
            else:
                return options
            
    def select_download(self, downloads):
        '''Takes a list of downloads and prompts the user to choose one of them. Returns a Stream.'''
        chosen = ""
        while True:
            try:
                print("Select a file to download:")
                while chosen not in downloads.keys():
                    chosen = input(">> ")
                    if chosen not in downloads.keys():
                        print(f"ERROR: No download found for #{chosen}. Please restart the program.")
            except:
                print("ERROR: There was an issue selecting the download. Please restart the program.")
            else:
                return self._youtube.streams.get_by_itag(downloads[chosen])
            
    def try_download(self, stream, maxAttempts=3):
        '''Tries to download the passed Stream for a certain amount of times. If it exceeds those tries, it exits.'''
        count = 0
        while True:
            if count > maxAttempts:
                print("Cannot download file. Please try another download.")
                self.try_download(self.select_download(self._downloads))
            try:
                stream.download(output_path=self._output)
            except:
                count += 1
                print(f"ERROR: There was an error downloading the file. Retrying... (attempt #{count})")
            else:
                print("Finished downloading!")
                break
    
    def convert_to_timestamp(self, seconds):
        '''Return a formatted timestamp of a given number of seconds.'''
        from math import floor

        minutes = floor(seconds/60)
        remainingSeconds = seconds & 60
        return f"{minutes}:{remainingSeconds}"

    def run(self):
        '''Starts the downloader and prompts.'''
        
        # Show video selected
        print(f"Video Selected: '{self._youtube.title}' by {self._youtube.author} ({self.convert_to_timestamp(self._youtube.length)})")

        try:
            # Prompts
            self._filtersEnabled = self.prompt_filters()
            if self._filtersEnabled:
                self._splitChannels = self.prompt_channels()
                self._extension = self.prompt_extension()

            # Gathers filtered streams and downloads
            self._streams = self.try_filters(self._filtersEnabled, self._splitChannels, self._extension, self._chosenType)
            self._downloads = self.create_download_list(self._streams)

            # Attempts to download
            if self._downloads != None:
                self.try_download(self.select_download(self._downloads))

        except:
            print("ERROR: An unknown error has occurred in the process. Please restart the program and try again.")