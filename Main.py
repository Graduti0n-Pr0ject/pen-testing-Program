import webbrowser
from subprocess import Popen, CREATE_NEW_CONSOLE

import pyqtcss
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QFileDialog, QMessageBox, QLineEdit, \
    QRadioButton, QCheckBox
from PyQt5.uic import loadUi

from Attacks.LFI_files.LFI import testExtention, LFIinj
from Attacks.sqlInjection.Error_based_attack import *
from Recon.Directory.directory import *
from ThreadsApp import *


# from Attacks.UnionScripts import figure_columns_in_table, figure_data_in_columns
# from Attacks.Error_based_attack import *


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
        self.proxy_process = None
        self.direct_process = None
        self.timer = QTimer()
        self.directory_timer = QTimer()
        loadUi("design.ui", self)
        self.ip_address_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        self.port_pattern = r"\b\d{1,5}\b"
        self.url_pattern = r"(https?|ftp)://[^\s/$.?#].[^\s]*"
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
        3. start_D -> button
        '''
        self.start_D.clicked.connect(self.search_directories)
        self.directory_timer.timeout.connect(self.check_directory_status)

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

        ### LFI
        '''
        1. LFI_URL -> EditText
        2. LFI_btn -> pushbutton
        3. payload_list -> QListWidget
        4. LFI_output_list -> QListWidget
        '''
        self.LFI_btn.clicked.connect(self.LFI_task)

        #### Takeover
        '''
        1. takeover_url -> Input
        2. choose_take_over_file -> choose file
        3. takeover_btn -> pushbutton
        '''
        self.takeover_btn.clicked.connect(self.takeover_task)
        self.choose_take_over_file.clicked.connect(self.open_choose_file)

        ##### WAF
        '''
        1. Ip, port -> input
        2. Savebtn -> button
        3. ap_port -> input
        '''
        self.Savebtn.clicked.connect(self.WAF_start)
        self.timer.timeout.connect(self.check_proxy_status)
        # Help btn
        self.helpbtn.clicked.connect(lambda _: webbrowser.open(
            r"https://abdullahsaid.notion.site/Documentation-e5c11a21dc2d40b2bd372ec66be964b9?pvs=4"))

    def validate_ip_address(self, ip_address):
        return re.fullmatch(self.ip_address_pattern, ip_address) is not None

    def validate_port(self, port):
        return re.fullmatch(self.port_pattern, port) is not None

    def WAF_start(self):

        try:
            ip_input = self.Ip.text().strip()
            port_input = self.port.text().strip()
            app_port = self.ap_port.text().strip()
            if ip_input == '' and port_input == '' and \
                    app_port == '' and \
                    not self.validate_port(port_input) and \
                    not self.validate_ip_address(ip_input) and self.validate_port(app_port):
                raise QMessageBox.warning(self, 'Warning', f'Enter  valid ip and port valid plz')
            else:
                if ip_input == '' or not self.validate_ip_address(ip_input):
                    raise QMessageBox.warning(self, 'Warning', f'Enter valid ip plz')
                if port_input == '' or not self.validate_port(port_input):
                    raise QMessageBox.warning(self, 'Warning', f'Enter  valid port plz')
                if app_port == '' or not self.validate_port(app_port):
                    raise QMessageBox.warning(self, 'Warning', f'Enter valid  application port plz')
            # mitmdump(["-s", p.__file__, "-p", app_port, "--listen-host", ip_input, "--mode",
            #           f"reverse:http://{ip_input}:{port_input}"])
            # thread_worker = ProxyThread(ip=ip_input, port=port_input, app_port=app_port)
            # thread_worker.run()
            self.proxy_process = Popen(
                ["mitmdump", "-s", __file__, "-p", app_port, "--listen-host", ip_input, "--mode",
                 f"reverse:http://{ip_input}:{port_input}"],
                creationflags=CREATE_NEW_CONSOLE
            )
            self.timer.start(1000)  # Check the proxy status every 1 second

        except Exception as error:
            QMessageBox.warning(self, 'Warning', f'Error occur in waf {error}')

    def check_directory_status(self):
        if self.direct_process.poll() is not None:
            # Proxy process has terminated
            self.directory_timer.stop()
            self.direct_process = None

    def check_proxy_status(self):
        if self.proxy_process.poll() is not None:
            # Proxy process has terminated
            self.timer.stop()
            self.proxy_process = None

    def takeover_task(self):
        try:
            domain_url = self.takeover_url.text()
            thread = ThreadAttackTakeover(url=domain_url, path=self.file_location, location_result=self.path)
            thread.run()
        except Exception as error:
            QMessageBox.warning(self, 'Warning', f'Error occur in takeover {error}')

    def LFI_task(self):
        self.payload_list.clear()
        self.LFI_output_list.clear()
        url_parm = self.LFI_URL.text()

        try:
            print("I")
            is_has, extension = testExtention(url_parm)
            # response = requests.get()
            if not is_has:
                raise BlockingIOError

            # self.LFI_output_list.addItem(f"URL querying file with extension {extension}")
            self.LFI_output_list.addItem("Start LFI injection")
            respone, pass_payload, fails = LFIinj(url_parm, extension)
            # self.LFI_output_list.addItems(fails)
            self.LFI_output_list.addItems(respone)
            self.payload_list.addItem(pass_payload)
        except BlockingIOError:
            QMessageBox.warning(self, 'Warning', f'[-] Must be querying file from server')

    def apply_Sql_Injection(self):
        try:
            sure_url = self.sql_url.text().strip()
            outputs, tables, pay, orc = sample_Get_inj(sure_url)
            self.payload = pay
            self.is_orc = orc
            # tables.insert(0, self.table_list.currentText())
            self.table_list.clear()
            self.table_list.addItem("Tables")
            self.table_list.addItems(tables)
            self.output_list.addItems(outputs)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema,
                requests.exceptions.InvalidURL) as error:

            QMessageBox.warning(self, 'Warning', f'Write Valid URL {error}')

    def check_tables_sql(self):
        self.output_list.clear()
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
            self.output_list.addItem(
                f"[+] Exploiting {len(columns)} columns, this is names of this columns, insert one to show his data")

        except IndexError as error:
            QMessageBox.Warning(self, 'Warning', f'Plz choose table')

    def check_columns_data(self):
        current_index_col = self.column_list.currentIndex()
        current_index_tab = self.table_list.currentIndex()
        url = self.sql_url.text()
        table_name = self.table_list.currentText()
        column_name = self.column_list.currentText()
        try:
            if current_index_col == 0 or current_index_tab == 0:
                raise IndexError
            data = figure_data_in_columns(url, self.payload, table_name, column_name)
            data.insert(0, f"Data in column {column_name}")
            self.output_list.addItems(data)
        except IndexError as error:
            QMessageBox.Warning(self, 'Warning', f'Plz choose column or table')

    def search_directories(self):
        cwd = os.path.dirname(__file__)
        try:
            sure_url = self.URL_D.text().strip()
            current_index_drop_box = self.list_D.currentIndex()
            current_item_drop_box = self.list_D.currentText()
            if not sure_url:
                QMessageBox.information(self, 'Information', f'Enter Right URL Plz')
            if not current_index_drop_box:
                QMessageBox.information(self, 'Information', f'Enter Choose directory Plz')
            self.path += r'\attack_result'
            command = ['python', fr'{cwd}\Recon\Directory\directory.py', sure_url, str(current_index_drop_box),
                       self.path]
            self.direct_process = Popen(command, creationflags=CREATE_NEW_CONSOLE)
            self.directory_timer.start(1000)
            # what_search, type_search = choose_list(current_index_drop_box)
            # thread = ThreadAttackDirectory(search=what_search, name=type_search, url=sure_url, path_result=self.path)
            # thread.run()
        except Exception as error:
            QMessageBox.warning(self, 'Warning', f'Error occur in directory {error}')

    def start_single_list_task(self):
        target: str = self.target_line.text().strip()
        is_live: QCheckBox = self.Live_subdomain
        is_endpoint: QCheckBox = self.Endpoint
        is_JS: QCheckBox = self.Js_files
        is_screen: QCheckBox = self.Screenshot
        is_parameter: QCheckBox = self.Parameter
        try:
            if self.singleRadio.isChecked():
                if target.strip() == '':
                    QMessageBox.information(self, 'Information', f'Enter Right Target Plz')
            elif not self.listRadio.isChecked() and not self.singleRadio.isChecked():
                QMessageBox.information(self, 'Information', f'Choosing Single or List Domain')

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
        except Exception as error:
            QMessageBox.warning(self, 'Warning', f'Error occur in recon {error}')

    def on_finished(self):
        try:
            self.reconbtn.setEnabled(True)
            if self.is_live_subdomain:
                self.Live_subdomain.setEnabled(True)
                self.is_live_subdomain = False
            if self.is_parameter:
                self.Parameter.setEnabled(True)
                self.is_parameter = False
            if self.is_screenshot:
                self.Screenshot.setEnabled(True)
                self.is_screenshot = False
            if self.is_endpoints:
                self.Endpoint.setEnabled(True)
                self.is_endpoints = False
            if self.is_Js_files:
                self.Js_files.setEnabled(True)
                self.is_endpoints = False
        except Exception as error:
            QMessageBox.warning(self, 'Warning', f'Error occur in finished {error}')

    def open_choose_file(self):
        try:
            file_dialog = QFileDialog(self)
            file_dialog.setWindowTitle("Open TXT File")
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("Text Files (*.txt)")

            if file_dialog.exec_():
                selected_file = file_dialog.selectedFiles()[0]
                if selected_file.endswith(".txt"):
                    self.file_location = selected_file
                    print("Selected file:", selected_file)
                else:
                    QMessageBox.warning(self, 'Warning', f'Invalid file format. Please choose a TXT file.')
                    print("Invalid file format. Please choose a TXT file.")
        except Exception as error:
            QMessageBox.warning(self, 'Warning', f'Error occur in choosing file {error}')

    def open_file_dialog(self):
        try:
            project_name: QLineEdit = self.projectName.text()
            file_dialog = QFileDialog(self)
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
        except Exception as error:
            QMessageBox.warning(self, 'Warning', f'Error occur in Choosing Project {error}')

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
                os.mkdir(self.path + '/' + "takeover_result")
                os.mkdir(self.path + '/' + "waf_result")
                os.mkdir(self.path + '/' + "directory_result")
                stack_widget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, 'Warning', 'Choose Option')

    def back_home(self):
        try:
            # waf_widget: QtWidgets.QRadioButton = self.WafRadio
            # frame_widget: QtWidgets.QRadioButton = self.FrameRadio
            self.stackedWidget.setCurrentIndex(0)
            self.chooseProject.hide()
            # waf_widget.setChecked(False)
            # frame_widget.setChecked(False)
        except Exception as error:
            QMessageBox.warning(self, 'Warning', f'Error occur in backing {error}')


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
