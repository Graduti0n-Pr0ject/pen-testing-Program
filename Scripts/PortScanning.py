import os
import socket
import threading
import concurrent.futures
import re


def scan(ip, port):
    lock = threading.Lock()
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(.1)
    ip = re.sub("(https:// | http:// | \/)", '', ip)
    ip = socket.gethostbyname(ip)

    try:
        scanner.connect((ip, port))
        scanner.close()
        with lock:
            os.mkdir("Result-port_scan")
            with open(f"Result-port_scan/ports.txt", "a") as file:
                result = f"Port {port} is OPEN Running {socket.getservbyport(port)}"
                file.write(result)
            print(f"Port {port} is OPEN Running {socket.getservbyport(port)}")


    except:
        pass


def run(ip_num: str, scan_fn, nums_ports: int) -> list:
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(nums_ports):
            executor.submit(scan_fn, ip_num, port + 1)


def main():
    ip = input("target> ")
    run(ip, scan, 1025)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    #     for port in range(1025):
    #         executor.submit(scan, ip, port + 1)


if __name__ == "__main__":
    main()
