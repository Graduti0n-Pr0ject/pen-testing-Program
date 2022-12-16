import sys
import getopt
import requests
import re
from bs4 import BeautifulSoup

output = list()


class engines:
    def ask(self, target):
        global ouput
        reg = re.compile(f"\"domain\":.*\.{target}.*\.com")
        print("*********************search in ask**********************************")
        for i in range(20):
            ask = requests.get(f"https://www.ask.com/web?q={target}&qsrc=998&page={i}")
            ask_res = BeautifulSoup(ask.text, "html.parser").prettify()

            ask_subs = reg.findall(ask_res)

            for s in ask_subs:
                s = re.sub('.com.*||https://||www\.||"domain":"', "", s)
                print(s + ".com")
                output.append(s + ".com")

    def crt(self, target):
        reg = re.compile(f".*\.{target}.*")
        global output
        print("*******************************search in crt*************************")
        crt = requests.get(f"https://crt.sh/?q={target}")
        crt_res = BeautifulSoup(crt.text, "html.parser").prettify()

        crt_subs = reg.findall(crt_res)

        for s in crt_subs:
            s = re.sub("\*\.|", "", s)
            output.append(s)
            print(s)

    def yahoo(self, target):
        reg = re.compile(f".*\.{target}.*")
        global output
        print("***********************search in yahoo*********************")
        for i in range(20):
            yahoo = requests.get(f"https://search.yahoo.com/search?p={target}&pz=7&bct=0&b={i + 7}&pz=7&bct=0&xargs=0")
            yahoo_res = BeautifulSoup(yahoo.text, "html.parser").prettify()

            y_subs = reg.findall(yahoo_res)

            for s in y_subs:
                s = re.sub("<a.*>|\s|</span>", "", s)
                output.append(s)
                print(s)


def bruteforce(target):
    list = open("list.txt", "r").readlines()
    print("#######################Start subdomains brute force#########################\n")
    for b in list:

        b = b.split("\n")
        site = ("https://" + b[0] + "." + target).strip()
        try:
            req = requests.get(site)
            if req.status_code == 200:
                print("200 ok  " + site)
                global output
                output.append(site)

            else:
                pass
        except:
            pass

    sys.exit(0)


def bruteforcel(target):
    list = open("list.txt", "r").readlines()

    sublist = open(target).readlines()

    print("#######################Start subdomains brute force#########################\n")
    for s in sublist:

        s = s.split("\n")

        for b in list:
            b = b.split("\n")
            site = ("https://" + b[0] + "." + s[0]).strip()
            try:
                req = requests.get(site)
                if req.status_code == 200:
                    print("200 ok  " + site)
                    global output
                    output.append(site)


                else:
                    pass
            except:
                pass


def search(target):
    x = engines()
    x.yahoo(target)
    x.ask(target)
    x.crt(target)


def searchl(path):
    target = open(path, "r").readlines()
    for t in target:
        x = engines()
        x.yahoo(t)
        x.ask(t)
        x.crt(t)


def start():
    print("""
       1- Enter target
       2-List of targets
    """)
    num = input()
    if num == "1":
        target = input("Enter target ex google.com")
        print("""
         1-Brute force
         2- search engines
         3-both
        """)
        n = input()
        if (n == "1"):
            bruteforce(target)
        elif n == "2":
            search(target)
        else:
            bruteforce(target)
            search(target)
    else:
        path = input(" Enter path of txt:")
        print("""
         1-Brute force
         2- search engines
         3-both
        """)
        n = input()
        if (n == "1"):
            bruteforcel(path)
        elif n == "2":
            searchl(path)
        else:
            bruteforcel(path)
            searchl(path)


if __name__ == "__main__":
    start()
    output = list(dict.fromkeys(output))

    with open(r'subdomains.txt', 'w') as fp:
        for item in output:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Saved in subdomains.txt')
