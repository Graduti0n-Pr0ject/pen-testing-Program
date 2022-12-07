from PyQt5 import QtWidgets, uic
import re
import logo_rc
import JS as t1


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        # First Tools in Recon
        self.get_url: QtWidgets.QLineEdit = None
        self.searchbtn: QtWidgets.QPushButton = None
        self.output_list: QtWidgets.QListWidget = None

        # Second Tool in Recon


        self.init_ui()

    def init_ui(self):
        uic.loadUi("../GUI/app.ui", self)  # Load Design File
        # Tab of Recon tool 1
        self.get_url = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.searchbtn = self.findChild(QtWidgets.QPushButton, "Searchbtn")
        self.output_list = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.searchbtn.clicked.connect(self.show_result)

        self.show()  # GUI window

    def show_result(self):
        url = self.get_url.text()
        regex_url = re.compile(
                    r'^(?:http|ftp)s?://'  # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
                    r'localhost|'  #localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                    r'(?::\d+)?'  # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        check_url = re.match(regex_url, url) is not None
        print(check_url)
        js_files = None
        show = self.output_list
        if not url or not check_url:
            show.addItem("please Enter valid Url")
        else:
            show.clear()
            js_files = t1.fetch_js(url)
            show.addItems(js_files)


def main():
    app = QtWidgets.QApplication([])  # Start App
    window = MainWindow()
    app.exec_()  # Exit app when Press X


if __name__ == "__main__":
    main()
