import os
import re
from bs4 import BeautifulSoup


def wsubtakeover(path): # choose file
    cwd = os.path.dirname(__file__)
    os.system(f'{cwd}\\takeover.py -l {path} -o takeover.txt')


def wsubtakeover(domain): # for domain
    cwd = os.path.dirname(__file__)
    os.system(f'{cwd}\\takeover.py -d {domain} -o takeover.txt')
