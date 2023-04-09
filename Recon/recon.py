import os
import platform


####windows
# cwd=os.path.dirname(__file__) get dir
# os.system(f'cd {cwd}')
# os.system(f'"{cwd}\wsubfinder.exe"') exe script
# platform.system()

def subfinder_for_single_windows(Domain):  # single domain (collect subdomain)
    cwd = os.path.dirname(__file__)
    print(cwd)
    # os.system(f'{cwd}\wsubfinder.exe -d {Domain} -o domains.txt')
    # Create Dictectory (domain_result)
    os.system(fr'{cwd}\wsubfinder.exe -d "{Domain}"  >>{cwd}\domains.txt')


def subfinder_for_file_windows(path):  # list domain (collect subdomain)
    cwd = os.path.dirname(__file__)
    os.system(f'{cwd}\wsubfinder.exe -dL {path}  >>{cwd}\\domains.txt')


def subfinder_single_linux(Domain):
    os.system(f'subfinder -d {Domain} >>domains')


def subfinder_multi_linux(path):
    os.system(f'subfinder -dL {path} >>domains')


def httprobe_w():  # live domain
    cwd = os.path.dirname(__file__)
    os.system(f"type {cwd}\domains.txt | {cwd}\whttprobe.exe >>{cwd}\\urls.txt")


def httprobe_l():
    os.system("cat domains |httprobe >>urls")


def screenwin():  # screenshot
    cwd = os.path.dirname(__file__)
    os.system(fr"type {cwd}\domains.txt | {cwd}\whttprobe.exe | {cwd}\waquatone.exe -chrome-path C:\Program Files\Google\Chrome\Application\chrome.exe ")
    #os.system(fr"type {cwd}\urls.txt | {cwd}\waquatone.exe -chrome-path chrome.exe")


def screenlinux():
    os.system("cat urls | aquatone ")


def wwayback():  # endpoints
    cwd = os.path.dirname(__file__)
    os.system(f'type {cwd}\domains.txt | {cwd}\wwaybackurls.exe >>archive.txt')


def Js_file():  # Js_files
    cwd = os.path.dirname(__file__)
    os.system(f'type {cwd}\domains.txt | {cwd}\wwaybackurls.exe | find ".js" >>js.txt')


def Parameter():  # Parameter
    cwd = os.path.dirname(__file__)
    os.system(f'type {cwd}\domains.txt | {cwd}\wwaybackurls.exe | find "=" >>prameter.txt')



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


if __name__ == '__main__':
    main()
