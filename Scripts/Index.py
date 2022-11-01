from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys
import logs_rc
import webbrowser
class  MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        uic.loadUi("../GUI/Test.ui", self)   # Load Design File
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)     
        gitbtn = self.findChild(QtWidgets.QPushButton, "Githubbtn") # find object in gui
        # load Github URL
        gitbtn.clicked.connect(lambda x: webbrowser.open_new_tab('https://github.com/Graduti0n-Pr0ject/pen-testing-Program'))
        self.show() # GUI window
        




app = QtWidgets.QApplication(sys.argv) # Start App
window = MainWindow()
app.exec() # Exit app when Press X