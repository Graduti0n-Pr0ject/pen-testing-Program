import os
import platform

import threading

should_terminate = threading.Event()


#### windows
# cwd=os.path.dirname(__file__) get dir
# os.system(f'cd {cwd}')
# os.system(f'"{cwd}\wsubfinder.exe"') exe script
# platform.system()

def subfinder_for_single_windows(Domain, place):  # single domain (collect subdomain)
    cwd = os.path.dirname(__file__)
    cwd = str(cwd).replace("\\\\", "\\")
    print(cwd)
    os.system(fr'{cwd}\wsubfinder.exe -d "{Domain}"  >> {place}\recon_result\domains.txt')


def subfinder_for_file_windows(path, place):  # list domain (collect subdomain)
    cwd = os.path.dirname(__file__)
    cwd = str(cwd).replace("\\\\", "\\")
    os.system(fr'{cwd}\wsubfinder.exe -dL {path}  >> {place}\recon_result\domains.txt')


def httprobe_w(place):  # live domain
    cwd = os.path.dirname(__file__)
    cwd = str(cwd).replace("\\\\", "\\")
    print("live subdomain is started")
    os.system(fr"{cwd}\httpx.exe -l {place}\recon_result\domains.txt -o {place}\recon_result\live_domains.txt")


def screenwin(place):  # screenshot
    cwd = os.path.dirname(__file__)
    cwd = str(cwd).replace("\\\\", "\\")
    os.system(
        fr" {cwd}\httpx.exe  -ss -l {place}\recon_result\domains.txt -srd {place}\recon_result\screen")
    # os.system(fr"type {cwd}\urls.txt | {cwd}\waquatone.exe -chrome-path chrome.exe")


def wwayback(place):
    # Normalize path and replace double backslashes with single ones
    cwd = os.path.abspath(os.path.dirname(__file__)).replace("\\\\", "\\")
    print(place)
    # os.system(fr'copy .\wwaybackurls.exe {place}\recon_result')
    # os.system(
    #     fr'type {place}\recon_result\domains.txt | {place}\recon_result\wwaybackurls.exe')

    # Enclose place argument in quotes to handle spaces or special characters
    archive_path = f'"{place}\\recon_result\\archive.txt"'

    # Call wwaybackurls.exe with input from domains.txt and output to archive.txt
    os.system(f'type "{place}\\recon_result\\domains.txt" | {cwd}\\wwaybackurls.exe >> {archive_path}')


def fetchjs(place):  # Parameter
    cwd = os.path.abspath(os.path.dirname(__file__)).replace("\\\\", "\\")

    os.system(
        fr'type "{place}\recon_result\domains.txt" | {cwd}\wwaybackurls.exe | findstr ".js" >>{place}\recon_result\js.txt')


def Parameter(place):  # Parameter
    cwd = os.path.dirname(__file__)
    cwd = str(cwd).replace("\\\\", "\\")
    os.system(
        fr'type "{place}\recon_result\domains.txt" | {cwd}\wwaybackurls.exe | findstr "=" >>{place}\recon_result\parameter.txt')


def main():
    print("""

     1-single target
     2-list of targer




    """)
    choose = input()
    if choose == "1":
        input("Enter target:")
        if platform.system() == "Windows":
            print("windows")

        elif platform.system() == "Linux":
            print("Linux")

    else:
        input("Enter file path:")

    if platform.system() == "Windows":
        print("windows")
    elif platform.system() == "Linux":
        print("Linux")

    d = open("domains.txt", "r").readlines()
    for b in d:
        fetchjs(b)


if __name__ == '__main__':
    main()
