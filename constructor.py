from carta import Carta
from graph import Graph
import operacionesbd as bd
import copy
import sys
import gestor_pool as gp
import exportador as xprt

'''
Clase principal para construir la baraja, necesita que la
base de datos este inicializada. Tiene parametros dinamicos para
que se pueden modificar sin tocar el codigo
'''

#global
global parametros
#carga de parametros
def carga_parametros():
    '''
    Carga la lista del parametros en el fichero
    'data/parametros/constructor.txt'
    '''
    global parametros
    parametros = {}
    with open('data/parametros/constructor.txt') as f_in:
        #lineas que no son ni comnetarios ni blancos
        lineas = [lin.rstrip() for lin in f_in if lin.rstrip() and not lin.strip().startswith('#')]
        for lin in lineas:
            aux = lin.split(':')
            parametros[aux[0].strip()] = float(aux[1].strip())


def construye_grafo(cartas):
    '''
    Dada una lista de cartas (las que tocan en el sobre)
    el metodo devuelve el grafo con los valores de la bd
    '''
    grafo = Graph()
    #anyado los vertices del grafo
    for carta in cartas:
        #si ya tengo un nodo con el mismo nombre hago tratamiento
        if grafo.get_node(carta) is None:
            grafo.add_node(carta)
        else:
            grafo.add_node(copy.copy(carta))
    #anyado las Sinergias
    nodos = grafo.nodes
    #todos contra todos
    for carta1 in nodos:
        pesos = []
        #dado un nodo calculamos los pesos para todo el resto
        for carta2 in nodos:
            pesos.append(bd.valor_sinergia(carta1.name, carta2.name))
        #anyadimos las aristas a dicho nodo
        carta1.add_multiple_edges(nodos, pesos)
    return grafo


def func_valor(arista):
    '''
    Funcion de evaluacion que da un valor subjetivo de una arista y un vertice
    '''
    global parametros
    return (arista[0].name.nota_fireball*parametros['peso_carta'] +
            arista[1]*parametros['peso_sinergia'] -
            arista[0].name.cmc()*parametros['contrapeso'])


def colores_compatibles(colores, carta):
    '''
    Funcion para saber si los colores de un vecino son compatibles con
    los colores sobre el que estoy construyendo el mazo
    '''
    #si la carta es de uno de los colores o es incolora es compatible
    if carta.color in colores or carta.color == 'I':
        return True
    #si es M, miro que todos sus colores esten entre mis elegidos
    elif carta.color == 'M':
        bandera = True
        for col in carta.colores():
            if col not in colores:
                bandera = False
        return bandera
    #si no es monocolor aceptada, ni M, es de otro color, descarto
    else:
        return False

def promedio_color(cart_col):
    '''
    Con el objetivo de calcular los colores que vamos a elegir
    esta funcion devuelve un promedio de lo buenas que son las cartas
    el numero de cartas queda truncado a las 16 primeras y debe tener
    minimo. Estas comprovaciones las hace la propia funcion
    '''
    max_num_cartas = parametros['max_num_cartas']
    #estas reglas van a cambiar
    if len (cart_col) < 10:
        return 0
    elif len(cart_col)> 16:
        cart_col = sorted(cart_col, key =lambda k:k.nota_fireball)[:16]
    #la combinacion de colores debe tener un numero minimo de criaturas
    if len([car for car in cart_col if 'creature' in car.tipo.lower()])<parametros['criaturas_min']:
        return 0
    #si supero las restricciones fuertes calculo el valor...
    sumador = 0
    #LAS CARTAS SIEMRE TENDRAN UN COLOR VALIDO
    for c in cart_col:
        if c.color == 'M':
            sumador += c.nota_fireball / len(c.colores())
        else:
            sumador += c.nota_fireball
    return float(sumador)/len(cart_col)


def eleccion_colores(pool):
    '''
    input: Todas las cartas de un pool
    output: Lista de cartas validas segun los colores elegidos
    '''
    #calculo de los dos mejores colores usando el promedio
    colores = ['B', 'W', 'G', 'U', 'R']
    prodcolores = list()
    #calculo el producto cartesiano de los colores
    for x in range(len(colores)):
        for y in range(x+1, len(colores)):
            prodcolores.append(tuple((colores[x],colores[y])))

    #fabrico una lista de cartas del pool compatibles con el primer par de colores
    cc = [c for c in pool if colores_compatibles(prodcolores[0], c)]
    for i in range(1, len(prodcolores)):
        #cartas de esa combinacion de colores
        aux = [c for c in pool if colores_compatibles(prodcolores[i], c)]
        #si encuentro una combinacion mejor a mi actual, la adopto
        if promedio_color(aux) > promedio_color(cc):
            cc = aux
    return cc


def algoritmo_constructor(pool, ncartas=23):
    '''
    Devuelve una lista de cartas escogidas por el algoritmo a
    partir de un pool
    '''
    #variables que controlan las restricciones
    costes_activos = [0]*6
    criaturas = 0
    no_criaturas = 0

    #cartas del pool original compatibles con los colores elegidos
    pool = eleccion_colores(pool)
    #monta el grafo
    grafo = construye_grafo(pool)
    #buscamos los dos colores con mejor puntuacion individual
    nodos = grafo.nodes

    #busco primer nodo (mejor del mejor color)
    visitados = []
    actual = sorted([n for n in nodos],
                    key=lambda k:k.name.nota_fireball, reverse=True)[0]
    visitados.append(actual)

    #busco los demas
    while(len(visitados)<ncartas):
        posibilidades = sorted(actual.edge_list(), key=lambda k:func_valor(k), reverse=True)
        #para todos los veciones ordenados por puntos...
        for pos in posibilidades:
            #Si no lo he visitado...
            if pos[0] not in visitados:
                coste_vec = pos[0].name.cmc()
                #y si ademas cumple mis exigencias sobre la curva de mana
                #variable auxiliar para que no casque por arrayindex
                ind = int(min(coste_vec-1, parametros['segmana']-1))
                #restriccion debil: curva de mana
                if (costes_activos[ind] < parametros['c'+str(int(coste_vec)) if coste_vec < 6 else 'cmax']):
                    #restriccion debil: numero maximo de criaturas
                    if 'creature' in pos[0].name.tipo.lower() and criaturas < parametros['max_criaturas']:
                        actual = pos[0]
                        visitados.append(actual)
                        costes_activos[ind] += 1
                        criaturas += 1
                        break
                    #restriccion debil: numero maximo de NO criaturas
                    elif 'creature' not in pos[0].name.tipo.lower() and  no_criaturas < parametros['max_no_criaturas']:
                            actual = pos[0]
                            visitados.append(actual)
                            costes_activos[ind] += 1
                            no_criaturas += 1
                            break


                # si he llegado al ultimo y no anyado algo no va bien
                #posiblemente demasiadas restricciones
                #me cargo todas las restricciones
                if pos == posibilidades[-1]:
                    print('Imposible cumplir las resticciones debiles')
                    costes_activos = [0]*6
                    criaturas = 0
                    no_criaturas = 0

    #el orden en que he escogido las cartas
    for n in visitados:
        print(n.name.nombre_original, '->', n.name.nota_fireball)
    return visitados



def imprime_resultados(pool, elegidos):
    f = open('resultado_algoritmo.txt', 'w')
    f.write('################\nPOOL\n################\n')
    for p in pool:
        f.write(str(p)+'\n')
    f.write('################\nELECCION\n################\n')
    for e in elegidos:
        f.write(str(e)+'\n')
    f.close()

def nodos_a_cartas(nodos):
    cartas = list()
    for n in nodos:
        cartas.append(n.name)
    return cartas


def main():
    carga_parametros()
    eleccion = int(sys.argv[1])
    pool = None
    if eleccion == -1:
        #-1 significa generame el pool
        pool = gp.crear_pool(retorno = True)
    else:
        #aqui se cargara un pool
        pool = gp.cargar_pool(eleccion)

    res = sorted(nodos_a_cartas(algoritmo_constructor(pool, parametros['ncartas'])), key=lambda k:(k.color,k.cmc(),k.nombre))

    pool = [p for p in pool if p not in res]
    pool = sorted(pool, key=lambda k:(k.color,k.cmc(), k.nombre))
    xprt.exportDoc(pool, res)
    imprime_resultados(pool, res)


if __name__ == '__main__':
    main()
