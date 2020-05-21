'''
Entidades del programa y
herramientas para el manejo de estas
'''

from math import floor
from .parametros import GAME_DATA
from .jugador import Jugador, Mesa, Chef

from PyQt5.QtCore import QObject, pyqtSignal


class DCCafe(QObject):
    '''
    Clase que simula la administración
    y atención de cafeterías
    '''

    signal_add_object = pyqtSignal(dict)
    signal_update_pos = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        # En un issue se hablo que usar condiciones
        # dentro de un `__init__` es mala practica,
        # por lo que los valores de las instancias
        # deben ser entregados en una función auxiliar
        self.rep = int()
        self.dinero = int()
        self.pedidos_exitosos = int()
        self.pedidos_totales = int()
        self.ronda_act = int()
        self.disponibilidad = bool()
        self.clientes_iniciales = int()
        self.rondas_terminadas = int()

        self.mesas = list()
        self.chefs = list()
        self.jugadores = list()

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


    def new_game(self):
        '''Inicia una infancia nueva de DCCafé'''
        parm = GAME_DATA["DCCAFE"]["INICIALES"]
        self.dinero = parm["DINERO"]
        self.rep = parm["REPUTACION"]
        self.chefs = parm["CHEFS"]
        self.mesas = parm["MESAS"]
        self.clientes_iniciales = parm["CLIENTES"]
        self.disponibilidad = parm["DISPONIBILIDAD"]

    def load_game(self, players: int = 1):
        self.load_dccafe(**get_last_game_data(), pl=players)


    def move_player(self, key):
        # * Signal de KeyPressEvent
        for player in self.jugadores:
            player.move(key)
            self.signal_update_pos.emit(player.data)


    def load_dccafe(self, money: int, rep: int, rounds: int,
                    dishes: list, map_data: list, pl: int):
        self.dinero = money
        self.rep = rep
        self.rondas_terminadas = rounds
        for clase, pos_x, pos_y in map_data:
            print(f'# ~ cargando: {clase}')
            print('# ~ señan `signal_add_object` emitida')
            self.signal_add_object.emit({'object': clase})
            if clase == 'mesero':
                objeto = Jugador(pos_x, pos_y)
                self.jugadores.append(objeto)
            elif clase == 'chef':
                objeto = Chef(pos_x, pos_y)
                objeto.dishes = dishes.pop(0)
                self.chefs.append(objeto)
            elif clase == 'mesa':
                objeto = Mesa(pos_x, pos_y)
                self.mesas.append(objeto)
            else:
                raise ValueError('clase no valida en mapa.csv')
            print('# ~ clase cargada\n')


def get_last_game_data() -> dict:
    data = {}
    # TODO: path relativos
    with open('mapa.csv', 'r', encoding='utf-8') as file:
        map_content = file.readlines()
    data['map_data'] = [s.strip().split(',') for s in map_content if s.strip()]
    with open('datos.csv', 'r', encoding='utf-8') as file:
        game_conten = file.readlines()
    data['money'], data['rep'], data['rounds'] = game_conten[0].split(',')
    data['dishes'] = game_conten[1].split(',')
    return data
