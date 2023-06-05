import requests
import os

url = ""


def brute_force(Url):
    urls = open("dir.txt", 'a')

    try:
        req = requests.get(Url)
        if req.status_code == 200:
            print("200 ok  " + Url)

            urls.write(Url)

            urls.close()

        else:
            print(f"{req.status_code}  {Url}")
            print("fff")
    except:
        pass


def List(B_list, Url):
    for i in B_list:
        print("list")
        brute_force(Url + i)


def choose_List(n):
    List = list()

    # List=open("Dirctories.txt",'r').readlines()

    if n == "1":
        List = open("Dirctories.txt", 'r').readlines()
    elif n == "2":
        List = open("PHP.txt", 'r').readlines()
    elif n == "3":
        List = open("JS.txt", 'r').readlines()
    elif n == "4":
        List = open("asp.txt", 'r').readlines()
    elif n == "5":
        List = open("HTML.txt", 'r').readlines()
    elif n == "6":
        List = open("XML.txt", 'r').readlines()
    elif n == "7":
        path = input("Enter your path:")
        List = open(path, 'r').readlines()
    else:
        print("error")

    return List


def proccess():
    url = input("Enter:url ")
    print("""
          Choose brute force wordlist:
            1-Directories wordlist
            2-Php files wordlist
            3-JS files wordlist
            4-Asp.net files wordlist
            5-HTML files wordlist
            6-XML files wordlist
            7-Self wordlist
        
             """)
    num = input("Enter :")
    print(num)
    List(choose_List(num), url)
    print(choose_List(num))


if __name__ == '__main__':
    proccess()
