import sys
from sys import platform
import requests
import os


def brute_force(Url):
    if platform == "linux" or platform == "linux2":
        urls = open(r"Results/urls.txt", 'a')
    else:
        urls = open(r"Results\urls.txt", 'a')
    try:
        req = requests.get(Url)
        if req.status_code == 200:
            print("200 ok" + Url)
            urls.write(Url)
            urls.close()
        else:
            print(f"{req.status_code}  {Url}")
    except:
        pass


def check_brute_force(type_brute_force: list, Url: str):
    os.makedirs("Results", exist_ok=True)
    for i, v in enumerate(type_brute_force):
        brute_force(Url + v)
        if i == 40:
            break


def choose_list(n: int) -> list:
    search_type = list()

    if n == 1:
        search_type = open("Dirctories.txt", 'r').readlines()
    elif n == 2:
        search_type = open("PHP.txt", 'r').readlines()
    elif n == 3:
        search_type = open("js.txt", 'r').readlines()
    elif n == 4:
        search_type = open("asp.txt", 'r').readlines()
    elif n == 5:
        search_type = open("HTML.txt", 'r').readlines()
    elif n == 6:
        search_type = open("XML.txt", 'r').readlines()
    elif n == 7:
        # there is work ask where to get path you to brute force
        path = input("Enter your path:")
        search_type = open(path, 'r').readlines()
    else:
        print("error")

    return search_type


def proccess():
    url = input("Enter target url Example https://target.com/:")  # first put in lineEdit
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
    choose = choose_list(int(num))  # choose file to brute force on it.
    check_brute_force(choose, url)


if __name__ == '__main__':
    proccess()
