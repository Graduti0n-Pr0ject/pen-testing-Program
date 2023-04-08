import sys
import os
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QFileDialog, QMessageBox
import logo_rc


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("design.ui", self)
        self.widget.hide()
        self.WAFbtn.clicked.connect(self.do_work)
        self.BackHomebtn.clicked.connect(self.back_home)
        self.BackHomebtn_2.clicked.connect(self.back_home)
        self.filebtn.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        project_name: QtWidgets.QLineEdit = self.projectName.text()
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if project_name.strip() != '':
            if file_dialog.exec_() == file_dialog.Accepted:
                selected_directory = file_dialog.selectedFiles()[0]
                path = selected_directory + r'/' + project_name
                print(path)
            else:
                QMessageBox.warning(self, 'Warning', 'No directory selected.')
        else:
            QMessageBox.information(self, 'Information', f'The line edit contains "{project_name}".')

    def do_work(self):
        project_name: QtWidgets.QLineEdit = self.projectName
        stack_widget: QStackedWidget = self.stackedWidget
        waf_widget: QtWidgets.QRadioButton = self.WafRadio
        frame_widget: QtWidgets.QRadioButton = self.FrameRadio
        if waf_widget.isChecked():
            stack_widget.setCurrentIndex(1)
        elif frame_widget.isChecked():
            stack_widget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, 'Warning', 'Choose Option')

    def back_home(self):
        stack_widget: QStackedWidget = self.stackedWidget
        stack_widget.setCurrentIndex(0)
        self.widget.hide()
        waf_widget: QtWidgets.QRadioButton = self.WafRadio
        frame_widget: QtWidgets.QRadioButton = self.FrameRadio
        waf_widget.setChecked(False)
        frame_widget.setChecked(False)


app = QApplication([])  # Start App
main_app = MainWindow()
main_app.show()
try:
    sys.exit(app.exec_())  # Exit app when Press X
except Exception as error:
    print(error)
