import socket
import threading
import concurrent.futures
import re
import time


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
            result = f"Port {port} is OPEN Running {socket.getservbyport(port)}"
            print(result)
            return result
    except:
        pass


def run(ip_num: str, scan_fn, nums_ports: int) -> list:
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(nums_ports):
            futures.append(executor.submit(scan_fn, ip_num, port + 1))
        # At this point all the futures are pending, and are running
        # in 100 other threads
    result = []
    for future in futures:
        r = future.result()   # Wait on each result
        if r is not None:     # Save only the non-None results
            result.append(r)
    return result


def main():
    t = time.time()
    run("google.com", scan, 1025)
    print("Total execution time", time.time() - t)


if __name__ == "__main__":
    main()