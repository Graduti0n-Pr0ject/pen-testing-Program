import os
import re
from bs4 import BeautifulSoup


def wsubtakeover(path):
    cwd = os.path.dirname(__file__)
    os.system(f'{cwd}\\takeover.py -l {path} -o takeover.txt')


def wsubtakeover(domain):
    cwd = os.path.dirname(__file__)
    os.system(f'{cwd}\\takeover.py -d {domain} -o takeover.txt')


def arjun(url):
    os.system(fr"arjun -u {url}")
