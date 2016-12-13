#import pymysql
import sqlite3 as sql
from carta import Carta
import sys
import pickle


def crea_conexion():
    # crea la conexion a la bd
    #bd = pymysql.connect('localhost','magicuser','magictfg','magicbd')
    bd = sql.connect('bd.sqlite')
    return bd


def ejecuta_query(query):
    # crea la conexion
    bd = crea_conexion()
    # obten el cursor
    cursor = bd.cursor()
    try:
        # query + commit
        cursor.execute(query)
        #bd.commit()
    except:
        return False
        # si error -> rollback
        print(sys.exc_info()[0])
        #bd.rollback()
    #devuelve el resultado del cursor para instrucciones select
    res = cursor.fetchall()
    bd.commit()
    bd.close()
    return res

def ejecuta_multiples_queries(queries):
    #crea la conexion
    bd = crea_conexion()
    # obten el cursor
    cursor = bd.cursor()
    try:
        for query in queries:
            # query + commit
            cursor.execute(query)
        #bd.commit()
    except:
        # si error -> rollback
        print(sys.exc_info()[0])
        #bd.rollback()
    #devuelve el resultado del cursor para instrucciones select
    res = cursor.fetchall()
    bd.commit()
    bd.close()
    return res

def crea_tablas_bd():
    # crea la conexion
    bd = crea_conexion()
    # lee el script de creación de la bd
    archivo = open('./magicbd.sql')
    script = archivo.read()
    archivo.close()
    # ahora lo ejecutamos como un query normal
    ejecuta_query(script)
    bd.close()

def insertar_carta(carta):
    # crea todo el query
    query = str("INSERT INTO Carta (nombre, nombre_original,coleccion, color, coste_mana, rareza,"
    +"nota_fireball, coste_medio, texto, tipo) VALUES('"+carta.nombre+"', '"+carta.nombre_original+"', '"+carta.coleccion+
    "', '"+carta.color+"', '"+carta.coste_mana+"', '"+carta.rareza+"', "+str(carta.nota_fireball)+
    ", "+str(carta.coste_medio)+", '"+carta.texto+"', '"+carta.tipo+"')")
    # ejecuto el query
    return ejecuta_query(query)

def introducir_coleccion_en_bd():
    '''
    Este método toma el path a el array con las cartas y las inserta en la bd
    '''
    cartas = pickle.load(open("data/output/cartas.p", "rb"))
    for elem in cartas:
        #print(elem)
        #print("------\n")
        if insertar_carta(elem) is False:
            print(elem.tostring())


def listar_cartas(coleccion):
    '''
    Este método devuelve un array con todas las cartas de la coleccion
    '''
    cartas = []
    query = "select * from Carta where coleccion = '"+coleccion+"'"
    #ejecutamos
    res = ejecuta_query(query)
    for linea in res:
        cartas.append(linea_cursor_a_carta(linea))
    return cartas

def linea_cursor_a_carta(lineacursor):
    '''
    Esta funcion convierte una linea recuperada del cursor en
    un objeto del tipo carta
    '''
    return Carta(
                nombre = lineacursor[0],
                nombre_original = lineacursor[1],
                coleccion = lineacursor[2],
                color = lineacursor[3],
                coste_mana = lineacursor[4],
                rareza = lineacursor[5],
                nota_fireball = lineacursor[6],
                coste_medio = lineacursor[7],
                tipo = lineacursor[8],
                texto = lineacursor[9]
    )

def insertar_relaciones_en_bd(relaciones):
    '''
    dada una lista de tuplas que representa las relaciones entre cartas
    (com_carta1, puntuacion, nom_carta2)
    las introduce en la bd
    '''
    queries = []
    for rel in relaciones:
        #crea el query cart1, cart2, valor
        query = "INSERT INTO Sinergias values('" + str(rel[0] +"', '"+rel[2]+
        "', "+str(rel[1]))+")"
        queries.append(query)
    ejecuta_multiples_queries(queries)

def valor_sinergia(carta1, carta2):
    query = str("select * from Sinergias where (carta1 ='" + carta1.nombre
    +"' and carta2='"+carta2.nombre+"') or (carta2 ='"+carta1.nombre+"'and carta1='"+carta2.nombre+"')")
    out = ejecuta_query(query)
    #si no hay lineas en la respuesta la sinergia entre 2 cartas es 0
    if len(out)==0:
        return 0
    #si existe una linea devuelvo es valor de su sinergia (linea 0 pos 2)
    else:
        return out[0][2]

# main
if __name__ == '__main__':
    print(valor_sinergia('aberrantresearcher', 'fleetingmemories'))
