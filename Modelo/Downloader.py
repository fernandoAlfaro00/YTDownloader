from  pytube import YouTube
from PyQt5 import QtWidgets , QtGui 
from PyQt5.QtCore  import QThread , pyqtSignal 
import os 
class Downloader(QThread):
    processSignal = pyqtSignal(float)
   
    def __init__(self, parent=None):
        super(Downloader, self).__init__(parent=parent)
        self.path = None
        self.url = None
        self.video = None
        self.stream = None

    def download_video(self, url, path):
        self.path = path
        self.url = url
        self.start()

    def run(self):
        self.video = YouTube(self.url)
        self.video.register_on_progress_callback(self.return_progress)
    
    def set_stream(self,itag):

        self.stream =  self.video.streams.get_by_itag(itag)

        
    def download(self):

        self.stream.download(self.path)

    def return_progress(self, stream, chunk, bytes_remaining):
        percentage = 1 - bytes_remaining / self.stream.filesize
        self.processSignal.emit(percentage)

    def list_stream(self):
        
        self.esperar()

        return self.video.streams.all()

    def get_title(self):
        
        return self.video.title

    def esperar(self):

        self.start()
        if self.video is None:

            print("espere por favor")
            os.system("cls")
            self.esperar()
           
