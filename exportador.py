
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
    #pinto el pool
    for k in pool:
        fich.write('\t<card number="'+str(pool[k])+'" price="0" name="'+k+'"/>\n')
    #cierre pool
    fich.write('</zone>\n')
    fich.write('<zone name="eleccion">\n')
    #pinto la eleccion
    for e in eleccion:
        fich.write('\t<card number="'+str(eleccion[e])+'" price="0" name="'+e+'"/>\n')
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
        if c.nombre_original in dicc:
            dicc[c.nombre_original] += 1
        else:
            dicc[c.nombre_original] = 1
    return dicc
