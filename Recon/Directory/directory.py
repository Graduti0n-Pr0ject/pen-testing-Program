import sys
from sys import platform
import requests
import os
import threading
import concurrent.futures


def brute_force(Url, v, name, output):
    urls = open(fr"{output}\Results_{Url.replace(':', '')}\urls_{name}.txt", 'a')
    try:
        url_subdomain = (Url + v).strip()
        req = requests.get(url_subdomain)
        if req.status_code == 200:
            print("200 ok :" + url_subdomain)
            urls.write(url_subdomain + "\n")
            urls.close()
        else:
            print(f"{req.status_code}  {url_subdomain}")
    except:
        pass


def check_brute_force(type_brute_force: list, Url: str, name, output):
    os.makedirs(fr"{output}\Results_{Url.replace(':', '')}", exist_ok=True)
    for v in type_brute_force:
        brute_force(Url, v, name, output)


def choose_list(n: int) -> list:
    cwd = os.path.dirname(__file__)
    search_type = list()
    name_type = None
    if n == 1:
        with open(fr"{cwd}\Dirctories.txt", 'r') as a:
            search_type = a.readlines()

        name_type = "Directories"
    elif n == 2:
        with open(fr"{cwd}\PHP.txt", 'r') as a:
            search_type = a.readlines()
        name_type = "PHP"
    elif n == 3:
        with open(fr"{cwd}\JS.txt", 'r') as a:
            search_type = a.readlines()
        name_type = "JS"
    elif n == 4:
        with open(fr"{cwd}\asp.txt", 'r') as a:
            search_type = a.readlines()
        name_type = "ASP.net"
    elif n == 5:
        with open(fr"{cwd}\HTML.txt", 'r') as a:
            search_type = a.readlines()
        name_type = "HTML"
    elif n == 6:
        with open(fr"{cwd}\XML.txt", 'r') as a:
            search_type = a.readlines()
        name_type = "XML"
    # elif path is not None:
    #     with open(path, 'r') as a:
    #         search_type = a.readlines()
    #     name_type = "SELF"
    else:
        print("error")

    return search_type, name_type


def proccess():
    url = input("Enter target url Example https://target.com: ")  # first put in lineEdit
    print("""
          Choose brute force wordlist:
            1-Directories wordlist
            2-Php files wordlist
            3-JS files wordlist
            4-Asp.net files wordlist
            5-HTML files wordlist
            6-XML files wordlist
            7-Self wordlist

         """)  # Combo box
    num = input("Enter :")
    print(num)
    choose, name = choose_list(int(num))  # choose file to brute force on it.
    check_brute_force(choose, url, name)


if __name__ == '__main__':
    proccess()
