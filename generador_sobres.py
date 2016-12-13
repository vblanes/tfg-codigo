import operacionesbd as bd
from carta import Carta
from random import choice
from random import randint

class Generador:
    def __init__(self):
        self.cartas = bd.listar_cartas('INS')


    #TODO
    #Hay que mejorar la simulacion del sobre con reglas extras
    def simular_sobre(self):
        selec = []
        comunes = [carta for carta in self.cartas if carta.rareza == 'C']
        infrecuentes = [carta for carta in self.cartas if carta.rareza == 'U']
        for i in range(10):
            selec.append(choice(comunes))
        for i in range(3):
            selec.append(choice(infrecuentes))
        raras = []
        decision = randint(1,8)
        if decision <= 7:
            raras = [carta for carta in self.cartas if carta.rareza == 'R']
        else:
            raras = [carta for carta in self.cartas if carta.rareza == 'M']
        selec.append(choice(raras))
        return selec


if __name__ == '__main__':
    g = Generador()
    print(g.simular_sobre())
