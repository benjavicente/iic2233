'''
Entidades del programa y
herramientas para el manejo de estas
'''

from math import floor
from parametros import GAME_DATA


class DCCafe:
    '''
    Clase que simula la administración
    y atención de cafeterías
    '''
    def __init__(self):
        # En un issue se hablo que usar condiciones
        # dentro de un `__init__` es mala practica,
        # por lo que los valores de las instancias
        # deben ser entregados en una función auxiliar
        self.nombre = str()
        self.rep = int()
        self.dinero = int()
        self.pedidos_exitosos = int()
        self.pedidos_totales = int()
        self.ronda_act = int()
        self.disponibilidad = bool()
        self.chefs = int()
        self.mesas = int()
        self.clientes_iniciales = int()
        self.rondas_terminadas = int()

    def __str__(self):
        return self.nombre

    def calcular_rep(self) -> None:
        '''Actualiza la reputación del DCCafé'''
        parm = GAME_DATA["DCCAFE"]["CAL_REP"]
        self.rep = max(
            parm["MAX"],
            min(
                parm["MAX"],
                self.rep + floor(
                    parm["FACTOR"] * (self.pedidos_exitosos/self.pedidos_totales) - 2
                )
            )
        )

    def clientes_ronda(self) -> int:
        '''Calcula la cantidad de clientes en la ronda actual y los retorna'''
        parm = GAME_DATA["DCCAFE"]["CLIENTES_RONDA"]
        return parm["FACTOR"] * (parm["BASE"] + self.ronda_act)


class Jugador:
    '''
    Jugador del juego que empeña el rol de mesero
    Bonus: Dos jugadores al mismo tiempo
    '''
    def __init__(self):
        pass

    def __str__(self):
        pass


def iniciar_dccafe() -> DCCafe:
    '''Crea una infancia nueva de DCCafé y la retorna'''
    instance = DCCafe()
    parm = GAME_DATA["DCCAFE"]["INICIALES"]
    instance.dinero = parm["DINERO"]
    instance.rep = parm["REPUTACION"]
    instance.chefs = parm["CHEFS"]
    instance.mesas = parm["MESAS"]
    instance.clientes_iniciales = parm["CLIENTES"]
    instance.disponibilidad = parm["DISPONIBILIDAD"]
    return instance


def cargar_dccafe(dinero: int, reputacion: int, rondas: int) -> DCCafe:
    '''Carga una instanciad de DCCafé con valores iniciales guardados'''
    instance = DCCafe()
    instance.dinero = dinero
    instance.rep = reputacion
    instance.rondas_terminadas = rondas
    return instance
