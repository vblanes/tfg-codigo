
'''
Esta clase dispone de funciones para exportar a diferentes formatos
(por ahora solo .cod para visualizacion en cockatrice)
'''
def exportDoc(pool, eleccion, nombrefich = 'res_algoritmo.cod'):

    # abro el fichero
    fich = open(nombrefich, 'w')
    # copio el esquema basico
    fich.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    fich.write('<cockatrice_deck version="1">\n')
    fich.write('<deckname></deckname>\n')
    fich.write('<comments></comments>\n')
    fich.write('<zone name="pool">\n')

    pool = convertir_diccionario(pool)
    eleccion = convertir_diccionario(eleccion)

    llavesp = sorted(pool.keys(),key=lambda k:(k.cmc(), k.color))
    #pinto el pool
    for k in llavesp:
        fich.write('\t<card number="'+str(pool[k])+'" price="0" name="'+k.nombre_original+'"/>\n')
    #cierre pool
    fich.write('</zone>\n')
    fich.write('<zone name="eleccion">\n')
    #pinto la eleccion
    llavese = sorted(eleccion.keys(),key=lambda k:(k.cmc(), k.color))
    for e in llavese:
        print(e.cmc())
        fich.write('\t<card number="'+str(eleccion[e])+'" price="0" name="'+e.nombre_original+'"/>\n')
    fich.write('</zone>\n')
    #cierro el fichero
    fich.write('</cockatrice_deck>')
    fich.close()


def convertir_diccionario(cartas):
    '''
    Esta funcion convierte una lista de cartas en un diccionario
    para facilitar la expotacion a .cod y derivados
    '''
    dicc = {}
    for c in cartas:
        if c in dicc:
            dicc[c] += 1
        else:
            dicc[c] = 1
    return dicc
