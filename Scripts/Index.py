import os
import sys

from PyQt5 import QtWidgets, uic
import re
import logo_rc
import JS as t1
import directory as t2
from threading import Thread


class MainWindow(QtWidgets.QMainWindow):
    regex_url = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        # First Tools in Recon
        self.get_url: QtWidgets.QLineEdit = None
        self.searchbtn: QtWidgets.QPushButton = None
        self.output_list: QtWidgets.QListWidget = None

        # Second Tool in Recon
        self.get_url2: QtWidgets.QLineEdit = None
        self.word_list: QtWidgets.QComboBox = None
        self.startbtn: QtWidgets.QPushButton = None
        self.output_word_list: QtWidgets.QListWidget = None

        self.init_ui()

    def init_ui(self):
        uic.loadUi("../GUI/app.ui", self)  # Load Design File
        # Tab of Recon tool 1
        self.get_url = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.searchbtn = self.findChild(QtWidgets.QPushButton, "Searchbtn")
        self.output_list = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.searchbtn.clicked.connect(self.Recon_Tool_1)

        # Tab of Recon Tool 2
        self.get_url2 = self.findChild(QtWidgets.QLineEdit, "lineEdit2")
        self.word_list = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.startbtn = self.findChild(QtWidgets.QPushButton, "startbtn")
        self.startbtn.clicked.connect(self.Recon_Tool_2)
        self.output_word_list = self.findChild(QtWidgets.QListWidget, "listWidget_2")

        self.show()  # GUI window

    def Recon_Tool_1(self):
        self.output_list.clear()
        url = self.get_url.text()
        check_url = re.match(self.regex_url, url) is not None
        print(check_url)
        js_files = None
        show = self.output_list
        if not url or not check_url:
            show.addItem("please Enter valid Url")
        else:
            show.clear()
            js_files = t1.fetch_js(url)
            show.addItems(js_files)

    def Recon_Tool_2(self):
        self.output_word_list.clear()
        url = self.get_url2.text()
        check_url = re.match(self.regex_url, url) is not None
        print(check_url)
        current_index = self.word_list.currentIndex()
        current_item = self.word_list.currentText()
        if not url or not check_url:
            self.output_word_list.addItem("Please Enter Valid Url")
            print("goes first")
        elif current_index == 0:
            self.output_word_list.addItem("Please Choose your World List")
            print("goes second")
        else:
            os.remove("Results/urls.txt")
            new_url = url + '/'
            print(new_url)
            word_type = t2.choose_list(current_index)
            t2.check_brute_force(word_type, new_url)
            success_sub_domains = [current_item]

            with open("Results/urls.txt", "r") as u:
                success_sub_domains += u.readlines()
            if len(success_sub_domains) == 1:
                self.output_word_list.addItem(f"Nothing found for {success_sub_domains[0]} choose another one ")
            else:
                self.output_word_list.addItems(success_sub_domains)

    # def stop_and_show_result(self):
    #     url = self.get_url2.text()
    #     check_url = re.match(self.regex_url, url) is not None
    #     current_index = self.word_list.currentIndex()
    #
    #     if not url or not check_url:
    #         self.error_place.setText("Please Enter Valid Url")
    #     elif current_index == 0:
    #         self.error_place.setText("Please Choose your World List")
    #     else:
    #         self.error_place.clear()
    #         modify_index = current_index - 1 if\
    #         (current_index-1) < 0 else\
    #         self.error_place.setText("Please Choose your World List")
    #
    #         success_sub_domains = []
    #
    #         with open("Results/urls.txt", "r") as u:
    #             success_sub_domains = u.readlines()
    #
    #         for i, v in enumerate(success_sub_domains):
    #             self.table.setItem(i, modify_index, v)


def main():
    app = QtWidgets.QApplication([])  # Start App
    window = MainWindow()
    app.exec_()  # Exit app when Press X


if __name__ == "__main__":
    main()
