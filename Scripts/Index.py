import re
import requests
import logo_rc
from sys import platform
from PyQt5 import QtWidgets, uic
import JS as t1
import PortScanning as t3
import directory as t2
import decoder as t4
import domainer as t5

import UnionScripts
import Error_based_attack
import MIMA as ta2
import LFI as ta3
import Converter as ta4


class MainWindow(QtWidgets.QMainWindow):
    regex_url = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    payload = None
    is_orc = None

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        # ***************************Start Recon*********************************

        # First Tools in Recon
        self.get_url: QtWidgets.QLineEdit = None
        self.searchbtn: QtWidgets.QPushButton = None
        self.output_list: QtWidgets.QListWidget = None

        # Second Tool in Recon
        self.get_url2: QtWidgets.QLineEdit = None
        self.word_list: QtWidgets.QComboBox = None
        self.startbtn: QtWidgets.QPushButton = None
        self.output_word_list: QtWidgets.QListWidget = None

        # Third Tool in Recon
        self.get_url3: QtWidgets.QLineEdit = None
        self.search_port_btn: QtWidgets.QPushButton = None
        self.available_ports: QtWidgets.QListWidget = None

        # Fourth Tool in Recon
        self.get_string: QtWidgets.QLineEdit = None
        self.list_encode: QtWidgets.QComboBox = None
        self.list_decode: QtWidgets.QComboBox = None
        self.list_encode_output: QtWidgets.QListWidget = None
        self.list_decode_output: QtWidgets.QListWidget = None
        self.execute_codes: QtWidgets.QPushButton = None
        self.error_dialog: QtWidgets.QMessageBox = None

        # Fiftieth Tool in Recon
        self.domain: QtWidgets.QLineEdit = None
        self.file_sizes: QtWidgets.QComboBox = None
        self.type_input: QtWidgets.QComboBox = None
        self.start_btn: QtWidgets.QPushButton = None
        self.outputs_list: QtWidgets.QListWidget = None
        # **************************End Recon************************************

        # ***************************Start Attacks*********************************

        # First Tool in Attacks
        self.sql_url: QtWidgets.QLineEdit = None
        self.sql_btn: QtWidgets.QPushButton = None
        self.sql_output: QtWidgets.QListWidget = None
        self.tables_combobox: QtWidgets.QComboBox = None
        self.tables_btn: QtWidgets.QPushButton = None
        self.columns_combobox: QtWidgets.QComboBox = None
        self.columns_btn: QtWidgets.QPushButton = None

        # Second Tool in Attacks
        self.ip_text: QtWidgets.QLineEdit = None
        self.search_live_PCS: QtWidgets.QPushButton = None
        self.output_PCS: QtWidgets.QListWidget = None
        self.victim_ip: QtWidgets.QLineEdit = None
        self.victim_mac: QtWidgets.QLineEdit = None
        self.router_ip: QtWidgets.QLineEdit = None
        self.router_mac: QtWidgets.QLineEdit = None
        self.execute_MINA: QtWidgets.QPushButton = None
        self.error: QtWidgets.QMessageBox = None

        # Third Tool in Attacks
        self.url_pram: QtWidgets.QLineEdit = None
        self.search_payload: QtWidgets.QPushButton = None
        self.tests_outputs: QtWidgets.QListWidget = None
        self.payload_founded: QtWidgets.QListWidget = None
        self.error_apply: QtWidgets.QMessageBox = None

        # Fourth Tool in Attacks
        self.prepare_btn: QtWidgets.QPushButton = None
        self.prepare_outputs: QtWidgets.QListWidget = None
        self.listen_btn: QtWidgets.QListWidget = None

        # **************************End Attacks************************************
        self.init_ui()

    def init_ui(self):
        uic.loadUi("../GUI/app.ui", self)  # Load Design File
        # Tab of Recon tool 1
        self.get_url = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.searchbtn = self.findChild(QtWidgets.QPushButton, "Searchbtn")
        self.output_list = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.searchbtn.clicked.connect(self.recon_tool_1)

        # Tab of Recon Tool 2
        self.get_url2 = self.findChild(QtWidgets.QLineEdit, "lineEdit2")
        self.word_list = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.startbtn = self.findChild(QtWidgets.QPushButton, "startbtn")
        self.startbtn.clicked.connect(self.recon_tool_2)
        self.output_word_list = self.findChild(QtWidgets.QListWidget, "listWidget_2")

        # Tab of Recon Tool 3
        self.get_url3 = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")
        self.search_port_btn = self.findChild(QtWidgets.QPushButton, "searchportbtn")
        self.search_port_btn.clicked.connect(self.recon_tool_3)
        self.available_ports = self.findChild(QtWidgets.QListWidget, "listWidget_3")

        # Tab of Recon Tool 4
        self.get_string = self.findChild(QtWidgets.QLineEdit, "crypto_url")
        self.list_encode = self.findChild(QtWidgets.QComboBox, "combox_encode")
        self.list_decode = self.findChild(QtWidgets.QComboBox, "combox_decode")
        self.list_encode_output = self.findChild(QtWidgets.QListWidget, "enListView")
        self.list_decode_output = self.findChild(QtWidgets.QListWidget, "deListView")
        self.execute_codes = self.findChild(QtWidgets.QPushButton, "execute")
        self.execute_codes.clicked.connect(self.recon_tool_4)
        self.error_dialog = QtWidgets.QMessageBox()

        # Tab of Recon Tool 5
        self.domain = self.findChild(QtWidgets.QLineEdit, "domain")
        self.file_sizes = self.findChild(QtWidgets.QComboBox, "file_size")
        self.type_input = self.findChild(QtWidgets.QComboBox, "target")
        self.start_btn = self.findChild(QtWidgets.QPushButton, "DStart")
        self.start_btn.clicked.connect(self.recon_tool_5)
        self.outputs_list = self.findChild(QtWidgets.QListWidget, "subdomains_output")

        # Tab of attacks Tool 1
        self.sql_url = self.findChild(QtWidgets.QLineEdit, "Sql_url")
        self.sql_btn = self.findChild(QtWidgets.QPushButton, "sqlAttackbtn")
        self.sql_btn.clicked.connect(self.attack_tool_1)
        self.sql_output = self.findChild(QtWidgets.QListWidget, "sqlOutput")

        self.tables_combobox = self.findChild(QtWidgets.QComboBox, "combox_db")
        self.tables_btn = self.findChild(QtWidgets.QPushButton, "attackTablesbtn")
        self.tables_btn.clicked.connect(self.attack2_tool_1)

        self.columns_combobox = self.findChild(QtWidgets.QComboBox, "combox_cols")
        self.columns_btn = self.findChild(QtWidgets.QPushButton, "attackColumnbtn")
        self.columns_btn.clicked.connect(self.attack3_tool_1)

        # Tab of attacks Tool 2
        self.ip_text = self.findChild(QtWidgets.QLineEdit, "IP_text")
        self.search_live_PCS = self.findChild(QtWidgets.QPushButton, "ip_btn")
        self.search_live_PCS.clicked.connect(self.attack1_tool_2)
        self.output_PCS = self.findChild(QtWidgets.QListWidget, "sqlOutput_2")
        self.victim_ip = self.findChild(QtWidgets.QLineEdit, "victimIP")
        self.victim_mac = self.findChild(QtWidgets.QLineEdit, "VictimMAC")
        self.router_ip = self.findChild(QtWidgets.QLineEdit, "RouterIP")
        self.router_mac = self.findChild(QtWidgets.QLineEdit, "RouterMAC")
        self.execute_MINA = self.findChild(QtWidgets.QPushButton, "MIMA_btn")
        self.execute_MINA.clicked.connect(self.attack2_tool_2)
        self.error = QtWidgets.QMessageBox()

        # Tab of attack Tool 3
        self.url_pram = self.findChild(QtWidgets.QLineEdit, "url_pram")
        self.search_payload = self.findChild(QtWidgets.QPushButton, "scan_payload_btn")
        self.search_payload.clicked.connect(self.attack_tool_3)
        self.tests_outputs = self.findChild(QtWidgets.QListWidget, "payload_tests")
        self.payload_founded = self.findChild(QtWidgets.QListWidget, "found_payload")
        self.error_apply = QtWidgets.QMessageBox()

        # Tab of attack Tool 4
        self.prepare_btn = self.findChild(QtWidgets.QPushButton, "prepare_output")
        self.prepare_btn.clicked.connect(self.attack1_tool_4)
        self.prepare_outputs = self.findChild(QtWidgets.QListWidget, "prepare_outputs")
        self.listen_btn = self.findChild(QtWidgets.QPushButton, "listen_btn")
        self.listen_btn.clicked.connect(self.attack2_tool_4)
        self.show()  # GUI window

    def recon_tool_1(self):
        self.output_list.clear()
        url = self.get_url.text()
        check_url = re.match(self.regex_url, url) is not None
        if not url or not check_url:
            self.output_list.addItem("please Enter valid Url")
        else:
            js_files = t1.fetch_js(url)
            self.output_list.addItems(js_files)

    def recon_tool_2(self):
        self.output_word_list.clear()
        url1 = self.get_url2.text()
        check_url = re.match(self.regex_url, url1) is not None
        print(check_url)
        current_index = self.word_list.currentIndex()
        current_item = self.word_list.currentText()
        if not url1 or not check_url:
            # self.output_word_list.addItem("Please Enter Valid Url")
            msg = self.error
            msg.setIcon(msg.Warning)
            msg.setText("error")
            msg.setInformativeText("Please Enter Valid Url")
            msg.setWindowTitle("Error")
            msg.exec_()
            print("goes first")
        elif current_index == 0:
            # self.output_word_list.addItem("Please Choose your World List")
            msg = self.error
            msg.setIcon(msg.Warning)
            msg.setText("error")
            msg.setInformativeText("Please choose your world list")
            msg.setWindowTitle("Error")
            msg.exec_()
            print("goes second")
        else:

            new_url = url1 + '/'
            print(new_url)
            word_type, name = t2.choose_list(current_index)
            t2.check_brute_force(word_type, new_url, name)
            success_sub_domains = [current_item]
        if platform == "linux" or platform == "linux2":
            with open(rf"Results_{new_url.replace(':', '')}/urls_{name}.txt", "r") as u:
                success_sub_domains += u.readlines()
            if len(success_sub_domains) == 1:
                self.output_word_list.addItem(f"Nothing found for {success_sub_domains[0]} choose another one ")
            else:
                self.output_word_list.addItems(success_sub_domains)
        else:
            with open(rf"Results_{new_url.replace(':', '')}\urls_{name}.txt", "r") as u:
                success_sub_domains += u.readlines()
            if len(success_sub_domains) == 1:
                self.output_word_list.addItem(f"Nothing found for {success_sub_domains[0]} choose another one ")
            else:
                self.output_word_list.addItems(success_sub_domains)

    def recon_tool_3(self):
        self.available_ports.clear()
        url = self.get_url3.text()
        check_url = re.match(self.regex_url, url) is not None
        domain = url[url.rfind('/') + 1:]
        print(check_url)
        if not url or not check_url:
            # self.available_ports.addItem("Please Enter Valid Url")
            msg = self.error
            msg.setIcon(msg.Warning)
            msg.setText("error")
            msg.setInformativeText("Please Enter Valid Url")
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            result = t3.run(domain, t3.scan, 1025)
            self.available_ports.addItems(result)

    def recon_tool_4(self):
        text = self.get_string.text()
        encrypted_text = ""
        decrypted_text = ""
        current_encode = self.list_encode.currentIndex()
        current_decode = self.list_decode.currentIndex()
        output_encode = self.list_encode_output
        output_decode = self.list_decode_output
        try:
            if not text:
                raise IOError
            if current_encode == 0 and current_decode == 0:
                raise IndexError

            match current_encode:
                case 1:
                    encrypted_text = t4.Encode.url_encode(text)
                case 2:
                    encrypted_text = t4.Encode.base64_encode(text)
                case 3:
                    encrypted_text = t4.Encode.base32_encode(text)
                case 4:
                    encrypted_text = t4.Encode.md5_encode(text)
                case 5:
                    encrypted_text = t4.Encode.sha1_encode(text)
                case 6:
                    encrypted_text = t4.Encode.sha512_encode(text)
                case 7:
                    encrypted_text = t4.Encode.sha512_encode(text)
                case 8:
                    encrypted_text = t4.Encode.html_encode(text)

            match current_decode:
                case 1:
                    decrypted_text = t4.Decode.url_decode(encrypted_text)
                case 2:
                    decrypted_text = t4.Decode.base64_decode(encrypted_text)
                case 3:
                    decrypted_text = t4.Decode.base32_decode(encrypted_text)
                case 4:
                    decrypted_text = t4.Decode.html_decode(encrypted_text)

            output_encode.addItem(encrypted_text)
            output_decode.addItem(decrypted_text)
        except IOError as error:
            msg = self.error_dialog
            msg.setIcon(msg.Warning)
            msg.setText("Warning")
            msg.setInformativeText("write something in input filed")
            msg.setWindowTitle("Error")
            msg.exec_()
        except IndexError as ierror:
            msg = self.error_dialog
            msg.setIcon(msg.Warning)
            msg.setText("Warning")
            msg.setInformativeText("Choose encode or decode")
            msg.setWindowTitle("Error")
            msg.exec_()

        pass

    def recon_tool_5(self):
        domain = self.domain.text()
        file_size = self.file_sizes.currentIndex()
        target = self.type_input.currentIndex()
        output = self.outputs_list
        try:
            if not domain:
                raise TypeError
            result1 = t5.search_single(domain)
            output.addItems(result1)
            result2 = t5.bruteforce(domain, file_size)
            output.addItems(result2)
        except TypeError as Error:
            msg = self.error
            msg.setIcon(msg.Warning)
            msg.setText("Warning")
            msg.setInformativeText("Enter Valid domain")
            msg.setWindowTitle("Error")
            msg.exec_()

    def attack_tool_1(self):
        try:
            url = self.sql_url.text()
            response = requests.get(url)
            outputs, tables, pay, orc = Error_based_attack.sample_Get_inj(url)
            self.payload = pay
            self.is_orc = orc
            tables.insert(0, self.tables_combobox.currentText())
            self.tables_combobox.clear()
            self.tables_combobox.addItem("Tables")
            self.tables_combobox.addItems(tables)
            self.sql_output.addItems(outputs)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema,
                requests.exceptions.InvalidURL) as error:
            # self.sql_output.addItem(f"Enter Failed Url {error}")
            msg = self.error
            msg.setIcon(msg.Warning)
            msg.setText("error")
            msg.setInformativeText(f"Enter Failed Url {error}")
            msg.setWindowTitle("Error")
            msg.exec_()

    def attack2_tool_1(self):
        self.sql_output.clear()
        current_index = self.tables_combobox.currentIndex()
        url = self.sql_url.text()
        table_name = self.tables_combobox.currentText()
        try:
            if current_index == 0:
                raise IndexError
            columns = UnionScripts.figure_columns_in_table(url, self.payload, table_name, self.is_orc)
            self.columns_combobox.clear()
            self.columns_combobox.addItem("Columns")
            self.columns_combobox.addItems(columns)
            self.sql_output.addItem(
                f"[+] Exploiting {len(columns)} columns, this is names of this columns, insert one to show his data")

        except IndexError as error:
            # self.sql_output.addItem("plz choose table 📛")
            msg = self.error
            msg.setIcon(msg.Warning)
            msg.setText("Warning")
            msg.setInformativeText("Plz choose table 📛")
            msg.setWindowTitle("Error")
            msg.exec_()

    def attack3_tool_1(self):

        current_index_col = self.columns_combobox.currentIndex()
        current_index_tab = self.tables_combobox.currentIndex()
        url = self.sql_url.text()
        table_name = self.tables_combobox.currentText()
        column_name = self.columns_combobox.currentText()
        try:
            if current_index_col == 0 or current_index_tab == 0:
                raise IndexError
            data = UnionScripts.figure_data_in_columns(url, self.payload, table_name, column_name)
            data.insert(0, f"Data in column {column_name}")
            self.sql_output.addItems(data)
        except IndexError as error:
            # print("Plz choose column or table 📛")
            # self.sql_output.addItem("Plz choose column or table 📛")
            msg = self.error
            msg.setIcon(msg.Warning)
            msg.setText("Warning")
            msg.setInformativeText("Plz choose column or table 📛")
            msg.setWindowTitle("Error")
            msg.exec_()

    def attack1_tool_2(self):
        ip = self.ip_text.text()
        # try:
        etherHeader = ta2.Ether(dst="FF:FF:FF:FF:FF:FF")
        result = ta2.NetworkScanner(ip, etherHeader)
        results = ta2.PrintResult(result)
        self.output_PCS.addItems(results)
        # except:
        #     msg = self.error
        #     msg.setIcon(msg.Warning)
        #     msg.setText("Warning")
        #     msg.setInformativeText("Invalid Ip")
        #     msg.setWindowTitle("Error")
        #     msg.exec_()

    def attack2_tool_2(self):
        vip = self.victim_ip.text()
        vmac = self.victim_mac.text()
        rip = self.router_ip.text()
        rmac = self.router_mac.text()

        try:

            ta2.MITMAttack(vip, vmac, rip, rmac)
            # if attack_is_here == "[-] Attack not Performed":
            #     raise TypeError
            # self.output_PCS.addItem(attack_is_here)
        except TypeError:
            msg = self.error
            msg.setIcon(msg.Warning)
            msg.setText("Warning")
            msg.setInformativeText("no_attack happen")
            msg.setWindowTitle("Error")
            msg.exec_()

        pass

    def attack_tool_3(self):
        url_parm = self.url_pram.text()
        tests_outs = self.tests_outputs
        found_payload = self.payload_founded
        tests_outs.clear()
        found_payload.clear()
        try:
            is_has, extension = ta3.testExtention(url_parm)
            if not is_has:
                raise BlockingIOError
            tests_outs.addItem(f"URL querying file with extension {extension}")
            tests_outs.addItem("Start LFI injection")
            respone, pass_payload, fails = ta3.LFIinj(url_parm, extension)
            tests_outs.addItems(fails)
            found_payload.addItems(respone)
            found_payload.addItem(pass_payload)

        except BlockingIOError:
            msg = self.error_apply
            msg.setIcon(msg.Warning)
            msg.setText("Warning")
            msg.setInformativeText("[-] Must be querying file from server")
            msg.setWindowTitle("Error")
            msg.exec_()
        # except:
        #     msg = self.error_apply
        #     msg.setIcon(msg.Warning)
        #     msg.setText("Warning")
        #     msg.setInformativeText("Enter Valid URL")
        #     msg.setWindowTitle("Error")
        #     msg.exec_()
        pass

    def attack1_tool_4(self):
        torjan_output = self.prepare_outputs
        try:
            result = ta4.main()
            torjan_output.addItem(torjan_output)

        except:
            msg = self.error_apply
            msg.setIcon(msg.Warning)
            msg.setText("Warning")
            msg.setInformativeText("error Happened")
            msg.setWindowTitle("Error")
            msg.exec_()

    def attack2_tool_4(self):

        pass


def main():
    app = QtWidgets.QApplication([])  # Start App
    window = MainWindow()
    app.exec_()  # Exit app when Press X


if __name__ == "__main__":
    main()
