from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

import Interface
import sys
#Helloo
class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("Nyquist.ui",self)
        Interface.initConnectors(self)
        self.show()


app=QApplication(sys.argv)
UIWindow=UI()
app.exec_() 