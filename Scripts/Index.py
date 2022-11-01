from PyQt5 import QtWidgets, uic, QtCore
import sys

class  MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        uic.loadUi("../GUI/Test.ui", self)   # Load Design File
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)                
        self.show() # GUI window



app = QtWidgets.QApplication(sys.argv) # Start App
window = MainWindow()
app.exec() # Exit app when Press X