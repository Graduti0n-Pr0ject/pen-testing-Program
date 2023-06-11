import sys
import requests
import os
import threading
import concurrent.futures
import argparse


def brute_force(url, v, name, output):
    urls = open(fr"{output}\Results_{url.replace(':', '')}\urls_{name}.txt", 'a')
    try:
        url_subdomain = (url + v).strip()
        req = requests.get(url_subdomain)
        if req.status_code == 200:
            print("200 ok :" + url_subdomain)
            urls.write(url_subdomain + "\n")
            urls.close()
        else:
            print(f"{req.status_code}  {url_subdomain}")
    except:
        pass


def check_brute_force(type_brute_force: list, url: str, name, output):
    os.makedirs(fr"{output}\Results_{url.replace(':', '')}", exist_ok=True)
    for v in type_brute_force:
        brute_force(url, v, name, output)


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
    else:
        print("error")

    return search_type, name_type


def process(url, num, output):
    choose, name = choose_list(int(num))
    check_brute_force(choose, url, name, output)


def main():
    parser = argparse.ArgumentParser(description='Brute Force URL')
    parser.add_argument('url', help='Target URL (Example: https://target.com: )')
    parser.add_argument('num', help='Brute force wordlist number (1-6)')
    parser.add_argument('output', help='Output directory')
    args = parser.parse_args()
    process(args.url, args.num, args.output)


if __name__ == '__main__':
    main()
