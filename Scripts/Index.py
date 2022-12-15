from PyQt5 import QtWidgets, uic
import re, requests
import logo_rc
import JS as t1
import directory as t2
import PortScanning as t3
import Error_based_attack
import UnionScripts


class MainWindow(QtWidgets.QMainWindow):
    regex_url = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    out1 = []
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
        # **************************End Attacks************************************
        self.init_ui()

    def init_ui(self):
        uic.loadUi("../GUI/app.ui", self)  # Load Design File
        # Tab of Recon tool 1
        self.get_url = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.searchbtn = self.findChild(QtWidgets.QPushButton, "Searchbtn")
        self.output_list = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.searchbtn.clicked.connect(self.recon_too_1)

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
        self.show()  # GUI window

    def recon_too_1(self):
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
            self.output_word_list.addItem("Please Enter Valid Url")
            print("goes first")
        elif current_index == 0:
            self.output_word_list.addItem("Please Choose your World List")
            print("goes second")
        else:

            new_url = url1 + '/'
            print(new_url)
            word_type, name = t2.choose_list(current_index)
            t2.check_brute_force(word_type, new_url, name)
            success_sub_domains = [current_item]

            with open(f"Results-{new_url}/urls-{name}.txt", "r") as u:
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
            self.available_ports.addItem("Please Enter Valid Url")
        else:
            result = t3.run(domain, t3.scan, 1025)
            self.available_ports.addItems(result)

    def attack_tool_1(self):
        self.sql_output.clear()
        try:
            url = self.sql_url.text()
            response = requests.get(url)
            outputs, tables, pay, orc = Error_based_attack.sample_Get_inj(url)
            self.out1 = outputs
            self.payload = pay
            self.is_orc = orc
            tables.insert(0, self.tables_combobox.currentText())
            self.tables_combobox.clear()
            self.tables_combobox.addItems(tables)
            self.sql_output.addItems(outputs)
        except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema,
                requests.exceptions.InvalidURL) as error:
            self.sql_output.addItem(f"Enter Failed Url {error}")

    def attack2_tool_1(self):
        self.columns_combobox.clear()
        self.columns_combobox.addItem("Columns")
        out = self.out1
        current_index = self.tables_combobox.currentIndex()
        url = self.sql_url.text()
        table_name = self.tables_combobox.currentText()
        try:
            if current_index == 0:
                raise IndexError
            columns = UnionScripts.figure_columns_in_table(url, self.payload, table_name, self.is_orc)
            self.columns_combobox.addItems(columns)
            out.append(
                f"[+] Exploiting {len(columns)} columns, this is names of this columns, insert one to show his data")
            self.sql_output.addItems(out)

        except IndexError as error:
            self.sql_output.addItem("plz choose table 📛")

    def attack3_tool_1(self):
        self.tables_combobox.clear()
        self.tables_combobox.addItem("Tables")
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
            print("Plz choose column or table 📛")
            self.sql_output.addItem("Plz choose column or table 📛")

    def __del__(self):
        self.out1.clear()


def main():
    app = QtWidgets.QApplication([])  # Start App
    window = MainWindow()
    app.exec_()  # Exit app when Press X


if __name__ == "__main__":
    main()
