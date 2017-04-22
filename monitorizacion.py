def histograma(cartas, texto=True):
    '''
    Dado un conjunto de cartas seleccionadas devuelve
    un histograma. Si se espeficica texto = false devuelve un diccionario con
    las frecuencias. En caso contrario un string con la informacion
    '''
    frec = dict()
    for c in cartas:
        if c.cmc() in frec:
            frec[c.cmc()] += 1
        else:
            frec[c.cmc()] = 1
    if texto:
        cadena = '#####\nHISTOGRAMA\n#####\n'
        llaves = sorted(frec.keys())
        for k in llaves:
            cadena+= "Coste "+str(k)+" -> "+str(frec[k])+"\n"
        return cadena
    else:
        return frec


def imprime_resultados(pool, elegidos):
    f = open('resultado_algoritmo.txt', 'w')
    f.write('################\nPOOL\n################\n')
    for p in pool:
        f.write(str(p)+' -> '+str(p.nota_fireball)+'\n')
    f.write('################\nELECCION\n################\n')
    for e in elegidos:
        f.write(str(e)+' -> '+str(p.nota_fireball)+'\n')
    f.close()
