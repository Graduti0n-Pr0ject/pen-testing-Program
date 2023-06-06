from PyQt5.QtCore import QThread, pyqtSignal, QDir
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QFileDialog, QMessageBox, QLineEdit, \
    QRadioButton, QCheckBox, QDialog
from PyQt5.uic import loadUi


from ThreadsApp import *

import logo_rc

from Recon.Directory.directory import choose_list
from Attacks.SqlInjecation.Error_based_attack import sample_Get_inj
from Attacks.SqlInjecation.UnionScripts import figure_columns_in_table, figure_data_in_columns



import pyqtcss


class MainWindow(QMainWindow):
    path: str = None
    file_location = None
    thread = Thread()
    selected_directory: str = None
    is_live_subdomain: bool = None
    is_endpoints: bool = None
    is_Js_files: bool = None
    is_parameter: bool = None
    is_screenshot: bool = None

    def __init__(self):
        super().__init__()
        loadUi("design.ui", self)

        style_string = pyqtcss.get_style("dark_blue")
        self.setStyleSheet(style_string)
        # ----------- Home ------------ #
        self.chooseProject.hide()
        self.widget_list_domain.hide()
        self.widget_single_domain.hide()
        self.WAFbtn.clicked.connect(self.do_work)
        self.BackHomebtn.clicked.connect(self.back_home)
        self.BackHomebtn_2.clicked.connect(self.back_home)
        self.filebtn.clicked.connect(self.open_file_dialog)

        # ------------- Recon ---------- #
        # self.Screenshot
        # self.Parameter
        # self.Js_files
        # self.Endpoint
        # self.Live_subdomain
        # self.toolButton
        self.reconbtn.hide()
        self.sr: QRadioButton = self.singleRadio
        self.reconbtn.clicked.connect(self.start_single_list_task)
        self.chooseFile.clicked.connect(self.open_choose_file)

        # -------------- Attacks ----------- #

        ## Directory

        '''
        1. URL_D -> Input
        2. list_D -> Combobox
        3. file_D -> button
        4. start_D -> button
        '''
        self.start_D.clicked.connect(self.search_directories)

        ## Sql injection
        '''
        1. output_list -> listQ widget
        2. table_list -> comboBox
        3. column_list -> combox
        4. check_tbtn -> pushbutton
        5. check_cbtn -> pushbutton
        6. sql_url -> QLineEdit
        7. attack_btn -> pushbutton
        '''
        self.attack_btn.clicked.connect(self.apply_Sql_Injection)
        self.check_tbtn.clicked.connect(self.check_tables_sql)
        self.check_cbtn.clicked.connect(self.check_columns_data)

        ###

    def apply_Sql_Injection(self):
        try:
            sure_url = self.URL_D.text().strip()
            response = requests.get(sure_url)
            outputs, tables, pay, orc = sample_Get_inj(sure_url)
            self.payload = pay
            self.is_orc = orc
            tables.insert(0, self.table_list.currentText())
            self.table_list.clear()
            self.table_list.addItem("Tables")
            self.table_list.addItems(tables)
            self.output_list.addItems(outputs)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema,
                requests.exceptions.InvalidURL) as error:

            QMessageBox.warning(self, 'Warning', f'Write Valid URL {error}')

    def check_tables_sql(self):
        self.sql_output.clear()
        current_index = self.table_list.currentIndex()
        url = self.sql_url.text()
        table_name = self.table_list.currentText()
        try:
            if current_index == 0:
                raise IndexError
            columns = figure_columns_in_table(url, self.payload, table_name, self.is_orc)
            self.column_list.clear()
            self.column_list.addItem("Columns")
            self.column_list.addItems(columns)
            self.sql_output.addItem(
                f"[+] Exploiting {len(columns)} columns, this is names of this columns, insert one to show his data")

        except IndexError as error:
            QMessageBox.Warning(self, 'Warning', f'Plz choose table')

    def check_columns_data(self):
        current_index_col = self.column_list.currentIndex()
        current_index_tab = self.tables_combobox.currentIndex()
        url = self.sql_url.text()
        table_name = self.table_list.currentText()
        column_name = self.column_list.currentText()
        try:
            if current_index_col == 0 or current_index_tab == 0:
                raise IndexError
            data = figure_data_in_columns(url, self.payload, table_name, column_name)
            data.insert(0, f"Data in column {column_name}")
            self.sql_output.addItems(data)
        except IndexError as error:
            QMessageBox.Warning(self, 'Warning', f'Plz choose column or table')

    def search_directories(self):
        sure_url = self.URL_D.text().strip()
        current_index_drop_box = self.list_D.currentIndex()
        current_item_drop_box = self.list_D.currentText()
        if not sure_url:
            QMessageBox.information(self, 'Information', f'Enter Right URL Plz')
        if not current_index_drop_box:
            QMessageBox.information(self, 'Information', f'Enter Choose directory Plz')

        what_search, type_search = choose_list(current_item_drop_box)

        self.worker_bruteForce = ThreadAttackDirectory(search=what_search, name=type_search, url=sure_url)
        self.worker_bruteForce.run()

    def start_single_list_task(self):
        target: str = self.target_line.text().strip()
        is_live: QCheckBox = self.Live_subdomain
        is_endpoint: QCheckBox = self.Endpoint
        is_JS: QCheckBox = self.Js_files
        is_screen: QCheckBox = self.Screenshot
        is_parameter: QCheckBox = self.Parameter

        if self.singleRadio.isChecked():
            if target.strip() == '':
                self.stopbtn.hide()
                QMessageBox.information(self, 'Information', f'Enter Right Target Plz')
            else:
                # Subdomain Checkbox
                if is_live.isChecked():
                    self.is_live_subdomain = True
                    is_live.setEnabled(False)

                if is_endpoint.isChecked():
                    self.is_endpoints = True
                    is_endpoint.setEnabled(False)

                if is_JS.isChecked():
                    self.is_Js_files = True
                    is_JS.setEnabled(False)

                if is_screen.isChecked():
                    self.is_screenshot = True
                    is_screen.setEnabled(False)

                if is_parameter.isChecked():
                    self.is_parameter = True
                    is_parameter.setEnabled(False)

                self.reconbtn.setEnabled(False)
                self.thread = Thread(target.strip(),
                                     is_live=self.is_live_subdomain,
                                     is_end=self.is_endpoints,
                                     is_par=self.is_parameter,
                                     is_screen=self.is_screenshot,
                                     is_JS=self.is_Js_files, url=target, project_place=self.path,
                                     path=self.file_location)
                self.thread.start()
                self.thread.finished.connect(self.on_finished)


        elif self.listRadio.isChecked():

            pass
        else:
            self.stopbtn.hide()
            QMessageBox.information(self, 'Information', f'Choosing Single or List Domain')

    def on_finished(self):
        self.reconbtn.setEnabled(True)
        if self.is_live_subdomain:
            self.Live_subdomain.setEnabled(True)
        if self.is_parameter:
            self.Parameter.setEnabled(True)
        if self.is_screenshot:
            self.Screenshot.setEnabled(True)
        if self.is_endpoints:
            self.Endpoint.setEnabled(True)
        if self.is_Js_files:
            self.JS_files.setEnabled(True)

    # def on_finished_subdomain(self):
    #     # QMessageBox.information(self, 'Information', f'Collect Subdomain is finished')
    #     msg = QMessageBox()
    #     msg.setIcon(msg.Information)
    #     msg.setText("ok")
    #     msg.setInformativeText("Collect Subdomain is finished")
    #     msg.setWindowTitle("Subdomain")
    #     msg.exec_()

    def open_choose_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.DontUseCustomDirectoryIcons
        dialog = QFileDialog()
        dialog.setOptions(options)

        dialog.setFilter(dialog.filter() | QDir.Hidden)

        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)

        dialog.setNameFilters([f'(*.txt)'])

        if dialog.exec_() == QDialog.Accepted:
            path = dialog.selectedFiles()[0]  # returns a list
            self.file_location = path
        else:
            QMessageBox.warning(self, 'Warning', 'No File selected.')

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
                os.mkdir(self.path + '/' + "recon_result")
                os.mkdir(self.path + '/' + "attack_result")
                os.mkdir(self.path + '/' + "waf_result")
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
