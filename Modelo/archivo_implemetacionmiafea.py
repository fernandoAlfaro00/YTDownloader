from  pytube import YouTube

class DownLoader(QThread):

    
    def __init__(self,url):
        super(DownLoader,self).__init__()
        self.URL_VIDEO = url
        progressSignal = pyqtSignal()



    def run(self):
        self.video = Video(self.URL_VIDEO)
        
        self.video.download_file()

        print("-----------------------------")



class Video(object):
    
    


    
    def __init__(self, url):
        
        self.file_size = None

        self.URL_VIDEO =  str(url)

        self.percent =  0 

        self.video = YouTube(url, on_progress_callback=self.progress_Check)
        #self.video = YouTube(url)

        self.title  =  self.video.title  
        
        self.video_type  =   self.video.streams.filter(progressive= True, file_extension="mp4").first()

        self.file_size =   self.video_type.filesize

    def get_title(self):

        return self.title

    def progress_Check(self,stream = None, chunk = None, bytes_remaining = None):

        self.percent  = (100*(self.file_size-bytes_remaining))/self.file_size  
        format_string = "{:00.0f}% downloaded".format(self.percent)

        return format_string
    
    def download_file(self):

        self.video_type.download()

    def get_percent(self):
        
        return  self.percent