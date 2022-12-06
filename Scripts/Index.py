from PyQt5 import QtWidgets, uic
import sys
import logo_rc  # load icons in Gui
import webbrowser


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi("../GUI/app.ui", self)  # Load Design File
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("Pen. Testing")
        # gitbtn = self.findChild(QtWidgets.QPushButton, "Githubbtn")  # find object in gui
        # load Github URL
        # gitbtn.clicked.connect(lambda x: webbrowser.open_new_tab(
        #     'https://github.com/Graduti0n-Pr0ject/pen-testing-Program'))
        self.show()  # GUI window


def main():
    app = QtWidgets.QApplication([])  # Start App
    window = MainWindow()
    app.exec()  # Exit app when Press X


if __name__ == "__main__":
    main()
