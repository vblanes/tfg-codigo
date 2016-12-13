class Carta:

    # esto es un variable estatica
    numeroCartas = 0
    # constructor de la clase
    def __init__(self, nombre, nombre_original, coleccion, color, tipo, coste_mana, rareza, texto, nota_fireball, coste_medio):
        #asignaciones
        self.nombre = nombre
        self.nombre_original = nombre_original
        self.coleccion = coleccion
        self.color = color
        self.tipo = tipo
        self.coste_mana = coste_mana
        self.rareza = rareza
        self.texto = texto
        self.nota_fireball = nota_fireball
        self.coste_medio = coste_medio


    def __str__(self):
        return str(self.nombre_original+" -> "+self.coste_mana)

    def cmc(self):
        '''
        Devuelve el coste de mana convertido de una carta
        '''
        cmc = 0
        for el in list(self.coste_mana):
            if el.isdigit():
                cmc+=int(el)
            elif el != 'X':
                cmc+=1
        return cmc

    def colores(self):
        if self.color == 'M':
            colrs = set()
            for m in self.coste_mana:
                if not m.isdigit() and m != 'X':
                    colrs.add(m)
            return list(colrs)
        else:
            return  self.color


    # aqui tocara escribir algun metodo auxiliar
    def tostring(self):
        return str(self.nombre+' - '+self.nombre_original+' - '+self.coleccion+' - ' + self.color +
        ' - '+self.tipo+' - '+self.coste_mana+' - '+self.rareza+' - '+self.texto
        +' - '+str(self.nota_fireball)+' - '+str(self.coste_medio))
