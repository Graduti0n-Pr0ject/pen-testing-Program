from bs4 import BeautifulSoup
import re, requests


def fetch_js(url: str) -> list:
    regx = re.compile("[https:\/\/http:\/\/\/\/\/a-zA-Z0-9\.\/]+\.js")
    rq = requests.get(url)

    res = BeautifulSoup(rq.text, "html.parser").prettify()
    get_js_files = regx.findall(str(res))
    remove_repeated = set(get_js_files)

    return list(remove_repeated)


def start():
    url = input("Enter URL")
    fetch_js(url)


if __name__ == "__main__":
    start()
