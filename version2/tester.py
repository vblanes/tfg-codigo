from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys
import re
from carta import Carta
import pickle
import pandas as pd
from os import listdir
import operacionesbd as obd

def fireball_scrap():
    url = 'http://www.channelfireball.com/articles/shadows-over-innistrad-limited-set-review-white/'

    diccionario = dict()
    # peticion web
    req = Request(url,
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    # parsea con beautifulsoup
    html = BeautifulSoup(webpage, 'lxml')
    # interesa p y h1
    h1tags = html.find_all('h1')
    # tratamiento de los nombres
    h1tags = h1tags[3:-1]
    nombres = []
    for i in range(len(h1tags)):
        if "Blue" in h1tags[i].text:
            continue
        nombres.append(h1tags[i].text)
        #print(h1tags[i])

    splitted = html.find_all('h3')

    # array donde guardar las notas
    notas = []
    splitted = splitted[1:-3]
    for elem in splitted:
        if "Limited" not in elem.text:
            continue
        nota = elem.text.split(":")[1][:4]
        #print(nota)
        try:
            nota = float(nota)
        except ValueError:
            continue
        notas.append(nota)


    #for i in range (len(notas)):
    #    print(nombres[i+1]+" - "+str(notas[i]))
    print("Notas", len(notas))
    print("Nombres", len(nombres))
    test_panda(nombres, notas)
    '''
    for i in range(len(h1tags)):
        diccionario[h1tags[i]] = notas[i]
    '''

def test_panda(nombres, notas):
    while len(notas)<len(nombres):
        notas.append(-1)
    while len(nombres)<len(notas):
        nombres.append("null")
    d = {'Nombres': nombres, 'Notas':notas}
    data = pd.DataFrame(d)
    data.to_csv("./../data/output/fireball/test.csv", encoding='utf-8')

def carga_panda_csv():
    path = "./../data/output/fireball/"
    archivos = listdir(path)
    diccionarios = []
    for elem in archivos:
        xx = pd.read_csv(path+elem)
        di = dict(zip(xx['Nombres'], xx['Notas']))
        diccionarios.append(di)

def test_final():
    cartas = pickle.load(open("./../data/output/cartas.p", "rb"))
    print(cartas)
    for cart in cartas:
        print(cart.nombre, cart.coste_mana, cart.nota_fireball, cart.coste_medio)

def test_tcg():

    dicc = pickle.load(open("./../data/output/dicttcgplayer.p","rb"))
    print(len(dicc))
    for el in dicc:
        print(el)
def test_info():
    dicc = pickle.load(open("./../data/output/dictmagicinfo.p","rb"))
    print(len(dicc))
    for el in dicc:
        print(el)
if __name__ == '__main__':
    #test_tcg()
    #print("---------\n")
    #test_info()
    #test_final()
    # fireball_scrap()
    #carga_panda_csv()
    obd.listar_cartas("INS")
