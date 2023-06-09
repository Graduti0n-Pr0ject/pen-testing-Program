import os
import platform
import subprocess
import sys

from bs4 import BeautifulSoup
import re, requests, pyfiglet
from subprocess import Popen
import threading

should_terminate = threading.Event()


####windows
# cwd=os.path.dirname(__file__) get dir
# os.system(f'cd {cwd}')
# os.system(f'"{cwd}\wsubfinder.exe"') exe script
# platform.system()

def subfinder_for_single_windows(Domain, place):  # single domain (collect subdomain)
    cwd = os.path.dirname(__file__)
    print(cwd)
    os.system(fr'{cwd}\wsubfinder.exe -d "{Domain}"  >> {place}\recon_result\domains.txt')


def subfinder_for_file_windows(path, place):  # list domain (collect subdomain)
    cwd = os.path.dirname(__file__)
    os.system(fr'{cwd}\wsubfinder.exe -dL {path}  >>{place}\recon_result\domains.txt')


def subfinder_single_linux(Domain):
    os.system(f'subfinder -d {Domain} >>domains')


def subfinder_multi_linux(path):
    os.system(f'subfinder -dL {path} >>domains')


def httprobe_w(place):  # live domain
    cwd = os.path.dirname(__file__)
    print("live subdomain is started")
    os.system(fr"type {place}\recon_result\domains.txt | {cwd}\httpx.exe >>{place}\recon_result\urls.txt")


def httprobe_l():
    os.system("cat domains |httprobe >>urls")


def screenwin(place):  # screenshot
    cwd = os.path.dirname(__file__)
    os.system(
        fr"type {place}\recon_result\domains.txt | {cwd}\httpx.exe | {cwd}\httpx.exe  -ss -o screens ")
    # os.system(fr"type {cwd}\urls.txt | {cwd}\waquatone.exe -chrome-path chrome.exe")


def screenlinux():
    os.system("cat urls | aquatone ")


def wwayback():  # endpoints
    cwd = os.path.dirname(__file__)
    os.system(f'type {cwd}\domains.txt | {cwd}\wwaybackurls.exe >>archive.txt')


# def Js_file():  # Js_files
#     banner = pyfiglet.figlet_format("JS")
#     print(banner)


def fetchjs(url, place):  # js Files

    print(" start js")
    regx = re.compile("[https:\/\/http:\/\/\/\/\/a-zA-Z0-9\.\/]+\.js")
    url = "https://" + url
    rq = requests.get(url)

    res = BeautifulSoup(rq.text, "html.parser").prettify()
    JS = regx.findall(res)
    myjs = set(JS)
    f = open(fr"{place}\recon_result\js.txt", "a+")
    for i in myjs:
        f.writelines(i + '\n')
    print("js end")


def Parameter(place):  # Parameter
    cwd = os.path.dirname(__file__)
    os.system(
        fr'type {place}\recon_result\domains.txt | {cwd}\wwaybackurls.exe | find "=" >>{place}\recon_result\prameter.txt')


def lwayback():
    os.system('cat domains | waybackurls >>archive')


def main():
    print("""

     1-single target
     2-list of targer




    """)
    choose = input()
    if choose == "1":
        Domain = input("Enter target:")
        if platform.system() == "Windows":
            print("windows")

        elif platform.system() == "Linux":
            print("Linux")

    else:
        path = input("Enter file path:")

    if platform.system() == "Windows":
        print("windows")
    elif platform.system() == "Linux":
        print("Linux")

    d = open("domains.txt", "r").readlines()
    for b in d:
        fetchjs(b)


if __name__ == '__main__':
    main()
