import concurrent.futures
import re
import threading

import requests
from bs4 import BeautifulSoup
from sys import platform


# output = list()


class Engines:
    def worker_ask(self, target, i):
        output = []
        reg = re.compile(f"\"domain\":.*\.{target}.*\.com")
        ask = requests.get(f"https://www.ask.com/web?q={target}&qsrc=998&page={i}")
        ask_res = BeautifulSoup(ask.text, "html.parser").prettify()

        ask_subs = reg.findall(ask_res)

        for s in ask_subs:
            s = re.sub('.com.*||https://||www\.||"domain":"', "", s)
            print(s + ".com")
            output.append(s + ".com")
        return output

    def ask(self, target):
        output = []
        futures = []

        print("*********************search in ask**********************************")
        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            for i in range(20):
                futures.append(executor.submit(self.worker_ask, target, i).result())

        for f in futures:
            if f is not None:
                output += f

        return output

    @staticmethod
    def crt(target):
        output = []
        reg = re.compile(f".*\.{target}.*")
        print("*******************************search in crt*************************")
        crt = requests.get(f"https://crt.sh/?q={target}")
        crt_res = BeautifulSoup(crt.text, "html.parser").prettify()

        crt_subs = reg.findall(crt_res)

        for s in crt_subs:
            s = re.sub("\*\.|", "", s)
            output.append(s)
            print(s)
        return output


# def bf_t(site):
#     lock = threading.Lock
#     output = []
#     try:
#         req = requests.get(site)
#         if req.status_code == 200:
#             print(f"{req.status_code} {site}")
#             output.append(site)
#         else:
#             print(f"{req.status_code}  {site}")
#             print(f"{req.status_code}  {site}")
#
#     except:
#         pass
#     return output
def bf_t(site):
    output = []
    try:
        req = requests.get(site)
        if req.status_code == 200:
            print("200 ok  " + site)

            output.append(site)

        else:
            print(f"{req.status_code} {site}")
    except:
        print("cant get domain")

    return output


def choose_file_size(n):
    name = ""
    match n:
        case 0:
            name = "small"
        case 1:
            name = "meduim"
        case 2:
            name = "list"
    return name


# single brute force
# def bruteforce(target, choice):
#     result = []
#     futures = []
#     name_file = choose_file_size(choice)
#     path = rf"domainer_files/{name_file}.txt"
#     if platform == "linux" or platform == "linux2":
#         path = rf"domainer_files/{name_file}.txt"
#     else:
#         path = rf"domainer_files\{name_file}.txt"
#
#     with open(path, 'r') as file:
#         # print("#######################Start subdomains brute force#########################\n")
#         list_brute_force = file.readlines()
#         with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
#             for b in list_brute_force:
#                 b = b.split("\n")
#                 site = "https://" + b[0] + "." + target
#                 futures.append(executor.submit(bf_t, site))
#
#         for f in futures:
#             r = f.result()
#             if r is not None:
#                 result.append(r)
#         result = set(result)
#
#     return list(result)
def bruteforce(target, choice):
    name_file = choose_file_size(choice)
    path = rf"domainer_files/{name_file}.txt"
    if platform == "linux" or platform == "linux2":
        path = rf"domainer_files/{name_file}.txt"
    else:
        path = rf"domainer_files\{name_file}.txt"
    with open(path, 'r') as file:
        print("#######################Start subdomains brute force#########################\n")
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for b in file:
                b = b.split("\n")
                site = "https://" + b[0] + "." + target
                executor.submit(bf_t, site)


# ask user for file of brute force list
def bruteforcel(target, choice):
    sub_list = []
    with open(target) as file:
        sub_list = file.readlines()

    result = []
    name_file = choose_file_size(choice)
    path = rf"domainer_files/{name_file}.txt"
    if platform == "linux" or platform == "linux2":
        path = rf"domainer_files/{name_file}.txt"
    else:
        path = rf"domainer_files\{name_file}.txt"
    # print("#######################Start subdomains brute force#########################\n")
    with open(name_file, 'r') as list_brute:
        for s in sub_list:
            futures = []
            result.append(s + f"\n{'*' * 40}")
            s = s.split("\n")
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                for b in list_brute:
                    b = b.split("\n")
                    site = "https://" + b[0] + "." + s[0]
                    futures.append(executor.submit(bf_t, site))

            for f in futures:
                r = f.result()
                if r is not None:
                    result.append(r)
            result += set(result)
    result = set(result)

    return list(result)


def search_single(target):
    x = Engines()
    fiter_sub_domain = set(x.ask(target) + x.crt(target))

    return list(fiter_sub_domain)


def searchl(path):
    target = open(path, "r").readlines()
    x = Engines()
    my_sub_domains = []
    for t in target:
        my_sub_domains += x.crt(t) + x.ask(t)
    filter_sub_domains = set(my_sub_domains)

    return list(filter_sub_domains)


def start():
    print("choose single<1> or list<?>: ", end="")
    choice = int(input())
    type = int(input("Enter type of file you want work on\n"
                     "0. small file"
                     "1. medium file"
                     "2. list file\n"
                     "choose<?>: "))
    if choice == 1:
        target = input("Enter target ex 'google.com'>: ")
        r2 = bruteforce(target, type)
        r1 = search_single(target)
        final_result = r1 + r2


if __name__ == "__main__":
    start()
    # output = list(dict.fromkeys(output))
    # with open(r'subdomains.txt', 'w') as fp:
    #     for item in output:
    #         # write each item on a new line
    #         fp.write("%s\n" % item)
    #     print('Saved in subdomains.txt')
