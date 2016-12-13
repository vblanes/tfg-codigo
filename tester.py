from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys
import re
from carta import Carta
import pickle
import pandas as pd
from os import listdir
import operacionesbd as obd

d1 = pickle.load(open("data/output/dictmagicinfo.p","rb"))
d2 = pickle.load(open("data/output/dicttcgplayer.p","rb"))
for k in d1:
    print(k)
print('##############')
for k in d2:
    print(k)
