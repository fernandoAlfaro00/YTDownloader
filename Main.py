from Vista.window import Window
from PyQt5 import QtWidgets 
import sys

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())