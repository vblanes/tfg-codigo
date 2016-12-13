from carta import Carta
import operacionesbd as obd
from nltk.corpus import stopwords


def extraer_tipo(carta):
    '''
    Dada una carta, si se trata de una criatura extrae su tipo
    '''
    tipo = carta.tipo
    if "Creature" in tipo:
        #recortamos la palabra Creature
        tipo = tipo.split('-')[1].strip()
        #buscamos donde aparece el ataque
        for i in range(len(tipo)):
            if tipo[i].isdigit():
                return tipo[:i].strip()


def obtener_tipos_criaturas(coleccion):
    '''
    Este metodo devuelve una lista de cadenas con los distintos
    tipos de criaturas existentes en la coleccion.
    Esta informacion es necesaria para evaluar las interacciones
    entre cartas
    '''
    cartas = obd.listar_cartas(coleccion)
    col_tipos = set()
    #por cada carta, si criatura queremos saber su tipo
    for c in cartas:
        tipo = extraer_tipo(c)
        #si no era una critura, sera nonetype
        if tipo is not None:
            col_tipos.add(tipo)
    return sorted(list(col_tipos))

#TODO
def calcular_sinergia(carta1, carta2):
    '''
    calcula la puntuacion entre dos cartas
    '''
    puntuacion = 0
    for color in carta1.color:
        if color in carta2.color:
            puntuacion+=1
    for subtipo in carta1.tipo.split():
        if subtipo in carta2.tipo:
            puntuacion = puntuacion + 0.5
    return puntuacion



def crear_relaciones(cartas):
    '''
    este metodo devuelve una lista de tuplas para poder ser insertada en la bd
    (nombre_carta_1, puntuacion, nombre_carta_2) : puntuacion > 0
    la manera de explorar asegura que no exista la misma relacion
    con orden distinto en las cartas, ej:
    (tragic slip, 2, gravecrawler) y (gravecrawler, 2, tragic slip)
    '''
    relaciones = []
    #ATENCION A LOS INDICES
    for i in range(len(cartas)):
        for j in range(i, len(cartas)):
            puntuacion = calcular_sinergia(cartas[i], cartas[j])
            if puntuacion == 0:
                continue
            relaciones.append((cartas[i].nombre, puntuacion, cartas[j].nombre))
    return relaciones

def extraer_palabras_clave(texto):
    palabras_limp = set()
    #quizás necesitemos tratamiento previo
    #descompon en palabras
    palabras = texto.split()
    #stopwords del ingles
    #usando un set porque tiene coste 1
    swords = set(stopwords.words('english'))
    for pal in palabras:
        if pal not in swords:
            palabras_limp.add(pal)
    #ahora tengo un palabras_limp (set) todas las palabras que no sean sw         


if __name__ == '__main__':
    cartas = obd.listar_cartas("INS")
    relaciones = crear_relaciones(cartas)
    obd.insertar_relaciones_en_bd(relaciones)
