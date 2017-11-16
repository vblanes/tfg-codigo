import pickle
from os import listdir
from generador_sobres import Generador
import sys
import operacionesbd as obd
'''
Este fichero proporciona los recursos para gestionar
pools de cartas predefinidos con el objetivo de hcer pruebas
de forma "derterminista"
'''
global path
path = 'data/pools'
def crear_pool(retorno = False):
    '''
    Crea un pool aleatorio. Si retorno es falso, lo escribe en la
    carpeta /data/pool. Si es true lo devuelve con un return
    '''
    pool = []
    g = Generador()
    for i in range(6):
        pool = pool+g.simular_sobre()
    pool = sorted(pool, key=lambda k:(k.color, k.cmc(), k.nombre))
    if retorno:
        return pool
    else:
        global path
        numeracion = len(listdir(path))
        pickle.dump(pool, open(path+'/pool'+str(numeracion)+'.p', 'wb'))

def cargar_pool(numpool):
    '''
    Carga y devuelve un pool de cartas
    '''
    global path
    return pickle.load(open(path+'/pool'+str(numpool)+'.p', 'rb'))

def print_pool(pool):
    '''
    Pinta por pantalla un pool dado
    en sistema unix se puede redireccion con '>'
    '''
    for p in pool:
        print(p)

def cargar_lista(path):
    lineas = open(path, 'r').read().split('\n')
    #print(lineas)
    cartas = []
    for lin in lineas:
        if not lin.strip():
            continue
        query = "select * from Carta where nombre='"+lin.strip()+"'"
        c = obd.ejecuta_query(query)
        if c:
            cartas.append(obd.linea_cursor_a_carta(c[0]))
    return cartas

def cargar(abspath):
    return pickle.load(open(abspath, 'rb'))

if __name__ == '__main__':
    print_pool(cargar_lista('test.txt'))
    #print_pool(cargar_pool(sys.argv[1]))
    '''
    if len(sys.argv)==2:
        print_pool(cargar_pool(sys.argv[1]))
    else:
        crear_pool()
    '''
