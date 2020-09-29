from PyQt5 import QtWidgets , QtGui 
from PyQt5.QtCore  import QThread , pyqtSignal 
from .design  import Ui_MainWindow  
from Modelo.Downloader import Downloader
from .dialogo import Ui_Dialog
import  sys 
import time



    

class Dialog(QtWidgets.QDialog):

    def __init__(self):
        super(Dialog,self).__init__()
        
        
        self.ui =  Ui_Dialog()
        
        self.ui.setupUi(self)
        #botones
        #boton aceptar
        self.ui.pushAceptar.clicked.connect(self.cerrar)
        self.ui.pushCancelar.clicked.connect(self.cerrar)

        #tabla de listado de formato
        self.ui.tableFormato.setRowCount(1)
        self.ui.tableFormato.setColumnCount(6)
        self.ui.tableFormato.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.tableFormato.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.tableFormato.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.tableFormato.cellClicked.connect(self.seleccionar_itag)
        self.itag =  None

            
        


    
    def lista_formato(self,streams):
        
     
        rows = 0          
        for stream in  streams:
            self.itag  = QtWidgets.QTableWidgetItem(str(stream.itag))
            self.resolution  = QtWidgets.QTableWidgetItem(stream.resolution)
            self.type  = QtWidgets.QTableWidgetItem(stream.type)
            self.mime_type  = QtWidgets.QTableWidgetItem(stream.mime_type)
           
            self.ui.tableFormato.setItem(rows,0, self.itag)
            self.ui.tableFormato.setItem(rows,1, self.resolution)
            self.ui.tableFormato.setItem(rows,2, self.type)
            self.ui.tableFormato.setItem(rows,3, self.mime_type)
            
            
            

            rows  =  rows +1 
            print(stream)
            self.ui.tableFormato.insertRow(rows)
        

    def seleccionar_itag(self):
        
        self.itag  = self.ui.tableFormato.selectedIndexes()[0].data()
    
        print(self.itag)

    def dar_itag(self):

        return self.itag

    def cerrar(self):

        self.close()



class Window(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Window,self).__init__()

        
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)

        self.ui.pushDescargar.clicked.connect(self.descargar_video)
    
        
        self.ui.tableDescargas.setRowCount(3)

        self.ui.tableDescargas.setColumnCount(3)
        nombreColumnas = ("Titulo", "Descripcion", "Descarga")
        # Establecer las etiquetas de encabezado horizontal usando etiquetas
        self.ui.tableDescargas.setHorizontalHeaderLabels(nombreColumnas)
        self.ui.tableDescargas.setWordWrap(True)
        self.ui.tableDescargas.horizontalHeader().setStretchLastSection(True)
        self.ui.tableDescargas.insertRow(3)
        self.thread   =  Downloader()

        
        
  
    
    def  descargar_video(self):
        
        #url =  self.ui.texUrl.toPlainText()
        url =  "https://www.youtube.com/watch?v=PHaJz21v8Xs"
        path  =  "C:/Users/Akira/Downloads"
        self.thread.download_video(url,path)
        itag =  self.open_wformat()
        if itag is not None:
            self.thread.set_stream(itag)
            self.agregar_fila()
            self.thread.download()

            print(itag)
            
        
        
    def open_wformat(self):
        dialog  = Dialog()
        dialog.setModal(True)
        
        dialog.lista_formato(self.thread.list_stream())
      
        dialog.show()

        dialog.exec()
        return  dialog.dar_itag()

    def agregar_fila(self):
        
        self.progress_bar  = QtWidgets.QTableWidgetItem("")
        self.cell_nombre  = QtWidgets.QTableWidgetItem("")
        self.cell_url    =  QtWidgets.QTableWidgetItem("")
        
        
        self.ui.tableDescargas.setItem(0,0, self.cell_nombre)
        self.ui.tableDescargas.setItem(0,1, self.cell_url )
        self.ui.tableDescargas.setItem(0,2, self.progress_bar)
        
        self.thread.processSignal.connect(self.start_progress_bar)

        


    def start_progress_bar(self,evt):
        
        self.progress_bar.setText("{:.1f}%".format(evt*100))
        self.cell_nombre.setText(self.thread.video.title)
        self.cell_url.setText(self.thread.video.description)

        
        
        self.ui.tableDescargas.update()
    




        
        
        

