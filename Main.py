import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QFileDialog, QMessageBox, QLineEdit, QRadioButton
import logo_rc
from Recon.recon import *


class Thread(QThread):
    finished = pyqtSignal()
    function = pyqtSignal()

    def __init__(self, domain=None):
        super().__init__()
        self.domain = domain

    def run(self) -> None:
        # super().sleep(1)
        print("Im in thread")
        subfinder_for_single_windows(self.domain)
        self.terminate()
        self.finished.emit()



class MainWindow(QMainWindow):
    path: str = None
    selected_directory: str = None

    def __init__(self):
        super().__init__()
        self.thread = None
        loadUi("design.ui", self)
        # ----------- Home ------------ #
        self.chooseProject.hide()
        self.widget_list_domain.hide()
        self.widget_single_domain.hide()
        self.WAFbtn.clicked.connect(self.do_work)
        self.BackHomebtn.clicked.connect(self.back_home)
        self.BackHomebtn_2.clicked.connect(self.back_home)
        self.filebtn.clicked.connect(self.open_file_dialog)

        # ------------- Recon ---------- #

        self.reconbtn.clicked.connect(self.start_single_list_task)

    def start_single_list_task(self):
        target: str = self.target_line.text()
        if self.singleRadio.isChecked():
            if target.strip() == '':
                QMessageBox.information(self, 'Information', f'Enter Right Target Plz')
            else:
                self.reconbtn.setEnabled(False)
                self.thread = Thread(target.strip())
                self.thread.finished.connect(self.on_finished)
                self.thread.start()

        elif self.listRadio.isChecked():
            pass
        else:
            QMessageBox.information(self, 'Information', f'Choosing Single or List Domain')

    def on_finished(self):
        self.reconbtn.setEnabled(True)
    def open_file_dialog(self):
        project_name: QLineEdit = self.projectName.text()
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if project_name.strip() != '':
            if file_dialog.exec_() == file_dialog.Accepted:
                self.selected_directory = file_dialog.selectedFiles()[0]
                self.path = self.selected_directory + r'/' + project_name

            else:
                QMessageBox.warning(self, 'Warning', 'No directory selected.')
        else:
            QMessageBox.information(self, 'Information', f'write project name correct.')

    def do_work(self):
        project_name: QLineEdit = self.projectName
        stack_widget: QStackedWidget = self.stackedWidget
        waf_widget: QRadioButton = self.WafRadio
        frame_widget: QRadioButton = self.FrameRadio
        if waf_widget.isChecked():
            stack_widget.setCurrentIndex(1)
        elif frame_widget.isChecked():
            # print(f"What's happen {self.path}")
            if self.selected_directory is None:
                QMessageBox.information(self, 'Information', f'Select Path.')
            elif os.path.exists(self.path):
                QMessageBox.information(self, 'Warning', f'Project is already in this {self.path} change project name')
            else:
                os.mkdir(self.path)
                stack_widget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, 'Warning', 'Choose Option')

    def back_home(self):
        # waf_widget: QtWidgets.QRadioButton = self.WafRadio
        # frame_widget: QtWidgets.QRadioButton = self.FrameRadio
        self.stackedWidget.setCurrentIndex(0)
        self.chooseProject.hide()
        # waf_widget.setChecked(False)
        # frame_widget.setChecked(False)


def main():
    app = QApplication([])  # Start App
    main_app = MainWindow()
    main_app.show()
    try:
        sys.exit(app.exec_())  # Exit app when Press X
    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()
