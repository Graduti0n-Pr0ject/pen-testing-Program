from bs4 import BeautifulSoup
import re, requests


def fetch_js(url: str) -> list:
    regx = re.compile(r'[(https)(http)(\.com)(-_)(\?=)(a-z)(A-Z)/(0-9)]*\.js')    #[(https)(http)(-_)(\?=)(a-z)(A-Z)/(0-9)]*\.js
    res=""
    try:
     rq = requests.get(url)
    except:
        print(" not valid")
    try:
     res = BeautifulSoup(rq.text, "html.parser").prettify()
    
     
    except:
        print(" not valid")
    get_js_files = regx.findall(str(res))
    remove_repeated = set(get_js_files)
    print(remove_repeated)
    return list(remove_repeated)


def start():
    url = input("Enter URL")
    try:
     fetch_js(url)
    except:
        pass


if __name__ == "__main__":
    start()
