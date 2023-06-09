import os
import re
from bs4 import BeautifulSoup


def wsubtakeover_path(path, place=""): # choose file
    cwd = os.path.dirname(__file__)
    print(cwd)
    os.system(fr'python {cwd}\takeover.py -l {path} -o {place}\takeover_result\takeover.txt')


def wsubtakeover(domain, place=""): # for domain
    cwd = os.path.dirname(__file__)
    print(cwd)
    os.system(fr'python {cwd}\takeover.py -d {domain} -o {place}\takeover_result\takeover.txt')
