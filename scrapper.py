from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys
import re
from carta import Carta
import pickle
import pandas
from os import listdir

def combina_diccionarios(diccionarios):
    '''
    Metedo auxiliar que fusiona varios diccionarios
    usado en carga_panda_csv
    '''
    resultado = dict()
    for elem in diccionarios:
        #print(elem)
        resultado.update(elem)
    return resultado

def guarda_panda_csv(nombres, notas, color):
    '''
    Debido a que channel fireball tiene errores en los formatos este metodo
    crea una estructura pandas con los arrays de nombres y notas y lo guarda
    en csv para que el usuario pueda hacer cambios manualmente de
    manera sencilla
    '''
    while len(notas)<len(nombres):
        notas.append(-1)
    while len(nombres)<len(notas):
        nombres.append("null")
    d = {'Nombres': nombres, 'Notas':notas}
    data = pandas.DataFrame(d)
    data.to_csv("data/output/fireball/"+color+".csv")#, encoding='utf-8')

def carga_panda_csv():
    '''
    Carga y fusiona en un unico diccionario todos los csv de fireball
    '''
    path = "data/output/fireball/"
    archivos = listdir(path)
    diccionarios = []
    for elem in archivos:
        xx = pandas.read_csv(path+elem)
        di = dict(zip(map(limpia_nombre, xx['Nombres']), xx['Notas']))
        diccionarios.append(di)
    return combina_diccionarios(diccionarios)


def limpia_nombre(nombre_orig):
    '''
    Limpia los nombres de las cartas de caracteres extranyos
    '''
    if '//' in nombre_orig:
        nombre_orig = nombre_orig.split('//')[0].strip()
    nom = nombre_orig.replace("'", "")
    nom  = nom.replace("’", '')
    return re.sub('\s+', '', nom).lower().strip()


def fireball_scrap(url, diccionario, color):
    # peticion web
    req = Request(url,
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    # parsea con beautifulsoup
    html = BeautifulSoup(webpage, 'lxml')
    # h1 son los nombres, h3 las notas
    nombres = html.find_all('h1')
    # tratamiento de los nombres
    nombres = nombres[3:-1]
    for i in range(len(nombres)):
        nombres[i] = limpia_nombre(nombres[i].text)
    #tratamiento de las notas
    splitted = html.find_all('h3')
    # array donde guardar las notas
    notas = []
    splitted = splitted[1:-3]
    for elem in splitted:
        if "Limited" not in elem.text:
            continue
        nota = elem.text.split(":")[1][:4]
        try:
            nota = float(nota)
        except ValueError:
            continue
        notas.append(nota)
    guarda_panda_csv(nombres, notas, color)


def tcg_player_scrap(url, diccionario):
    req = Request(url,
                  headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    html = BeautifulSoup(webpage, 'lxml')
    tdtags = html.find_all('td')
    # bandera tiene tres valores 0 = morralla principio, 1 = info, 2 = morralla final
    bandera = 0
    # este buccle sirve para eliminar la morralla del principio
    limpio = []
    estado = 0
    for celda in tdtags:
        if estado == 0 and 'SortOrder' in str(celda):
            estado = 1
        elif estado == 1 and '<b>Color</b>' in str(celda):
            estado = 2
        elif estado == 1 and 'SortOrder' not in str(celda):
            limpio.append(str(celda))

    # a partir de este punto tenemos solo las lineas que contienen la info
    puntero = 0
    while puntero < len(limpio):
        # puntero es la direccion base de la info de cada carta
        nombre = BeautifulSoup(limpio[puntero], 'lxml').find('a').getText()
        coste = BeautifulSoup(limpio[puntero + 1], 'lxml').find('td').getText()
        coste = re.sub('\s+', '', coste)
        rareza = BeautifulSoup(limpio[puntero + 3], 'lxml').find('td').getText()
        rareza = re.sub('\s+', '', rareza)
        costemedio = BeautifulSoup(limpio[puntero + 5], 'lxml').find('a').getText()
        diccionario[limpia_nombre(nombre)] = [coste, rareza, costemedio, nombre]
        puntero += 7


def magicinfo_scrap(url, diccionario):
    globaltagsa = []
    globaltagsp = []
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    # parsea con beautifulsoup
    html = BeautifulSoup(webpage, 'lxml')
    # nos interesan las a's para los nombres
    atags = html.find_all('a')
    # y las p's para el texto de la carta
    ptags = html.find_all('p')
    # en una primera pasada metemos los nombres
    inicio = False
    array_a_limpio = []
    for tag in atags:
        if '[' in tag.text:
            inicio = True
        elif '[' not in tag.text and inicio:
            array_a_limpio.append(tag)

    bandera = True
    for elem in array_a_limpio:
        if bandera:
            globaltagsa.append(elem.text)
            bandera = False
        elif str(elem.text) in 'all prints in all languages':
            bandera = True
    # en este punto tenemos introducidos los nombres de las cartas
    # ahora debemos coger los textos
    aux = []
    for i in range(len(ptags)):
        if i % 5 == 0:
            aux.append(re.sub('\s+', ' ', ptags[i].text).split(',')[0])
        elif i % 5 == 1:
            aux.append(re.sub('\s+', ' ', ptags[i].text))
        elif i % 5 == 2:
            globaltagsp.append(aux)
            aux = []
    # ahora combinamos
    for i in range(len(globaltagsp)):
        diccionario[limpia_nombre(globaltagsa[i])] = globaltagsp[i]


def substring(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def validacion_cruzada_scrapping(dicc_fireball, dicc_tcg_player, dicc_magic_info):
    '''
    Una vez obtenida toda la informacion este metodo la combina
    dicc_fireball: nombre : nota
    dicc_tcg_player: nombre : [coste, rareza, coste_medio, nombre_original]
    dicc_magic_info: nombre : [tipo, texto]
    '''
    array_cartas=[]
    cartas_error = open("errores.txt", "w")
    '''
    print(sorted(dicc_fireball.keys()))
    print('------------\n')
    print(sorted(dicc_tcg_player.keys()))
    print('------------\n')
    print(sorted(dicc_magic_info.keys()))
    '''
    for key in dicc_magic_info:
        try:
            elementostcg = dicc_tcg_player[limpia_nombre(key)]
            elementosinfo = dicc_magic_info[limpia_nombre(key)]
            if elementostcg[0] == '':
                continue
            #hay que eliminar algunos caracteres molestos
            nombre_original = elementostcg[3].replace("'", "''")
            costemedio = elementostcg[2].replace("$", '')
            rareza = elementostcg[1].replace("[", "")
            rareza = rareza.replace("]", "")
            tipo = elementosinfo[0].replace("—", "-")
            texto = elementosinfo[1].replace("'", "")
            texto = texto.replace("—", "-")
            texto = texto.replace("−", "-")
            texto = texto.replace("•", "")

            if key not in dicc_fireball:
                nf = 0
            else:
                nf = dicc_fireball[key]

            # constructor carta
            cartaux = Carta(nombre=key, nombre_original=nombre_original,coleccion='INS',
            color=calcular_color(elementostcg[0]), tipo=tipo,
            coste_mana=elementostcg[0], rareza=rareza, texto=texto,
            nota_fireball=nf, coste_medio=costemedio)
            array_cartas.append(cartaux)
        except:
                cartas_error.write(key+"\n")
    print(len(array_cartas))
    cartas_error.close()
    return array_cartas


def calcular_color(coste):
    conjunto = set()
    for character in coste:
        if not character.isdigit():
            conjunto.add(character)
    if len(conjunto) == 0:
        return 'I'
    elif len(conjunto) >= 2:
        return 'M'
    else:
        return str(list(conjunto)[0])


def enlaces_fireball():
    return open('data/parametros/enlaces_fireball.txt').read().split('\n')[:-1]


def enlaces_magicinfo(numeropags, url):
    enlaces = []
    for i in range(1, numeropags + 1):
        enlaces.append(url + str(i))
    return enlaces

def calcular_info():
    '''
    Este metodo utiliza la informacion ya descargada, se llamara si es usuario
    utiliza el primer parametro "calcular"
    '''
    dictfireball = carga_panda_csv()
    dicttcgplayer = pickle.load(open("data/output/dicttcgplayer.p", "rb"))
    dictmagicinfo = pickle.load(open("data/output/dictmagicinfo.p", "rb"))
    return validacion_cruzada_scrapping(dicc_fireball=dictfireball,
    dicc_tcg_player=dicttcgplayer, dicc_magic_info=dictmagicinfo)

def recopilar_info():
    '''
    Este metodo hace el scrapping, se llamara si el usuario usa como primer
    parametro "recopilar"
    '''
    # crea los diccionarios que van a recibir la información
    dictfireball = {}nombresycorreos])

    # ahora la informacion de fireball
    enl_fireball = enlaces_fireball()
    for link in enl_fireball:
        # link = color:link
        parametros = link.split('|')
        fireball_scrap(diccionario=dictfireball, url=parametros[1], color=parametros[0])

    # por ultimo la informacion de magic info
    enl_magicinfo = enlaces_magicinfo(url=sys.argv[3], numeropags=int(sys.argv[4]))
    for link in enl_magicinfo:
        magicinfo_scrap(url=link, diccionario=dictmagicinfo)

    pickle.dump(dicttcgplayer, open("data/output/dicttcgplayer.p", "wb"))
    #pickle.dump(dictfireball, open("dictfireball.p", "wb"))
    pickle.dump(dictmagicinfo, open("data/output/dictmagicinfo.p", "wb"))


# main
if __name__ == '__main__':
    if sys.argv[1] == 'recopilar' and len(sys.argv)==5:
        recopilar_info()
        print("Archivos descargados correctamente!")
    elif sys.argv[1] == 'calcular' and len(sys.argv) == 2:
        res = calcular_info()
        print("Se ha podido consegir información sobre", len(res), 'cartas')
        pickle.dump(res, open("data/output/cartas.p", "wb"))
        print("Archivo disponible en data/output/cartas.p")
    else:
        print("Este programa tiene dos posibles usos:")
        print("python3 scrapper recopilar url_tcg url_magicinfo_sin_pagina pags_magicinfo")
        print("python3 scrapper calcular")
