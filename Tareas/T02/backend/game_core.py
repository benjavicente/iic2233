'''Administrador del Juego'''

from PyQt5.QtCore import QObject, pyqtSignal, QThread
#from random import randint

from backend.game_objects import Player, Chef, Table, Cafe
from backend.paths import PATH_DATOS, PATH_MAPA
from config.parametros import PARAMETROS



class GameCore(QObject):
    '''
    Objeto que se encarga de conctar todo el backend con el frontend
    Almacena todos los objetos del backend
    '''

    signal_add_new_object = pyqtSignal(dict)
    signal_update_pos = pyqtSignal(dict)
    signal_start_game_window = pyqtSignal()
    signal_update_cafe_stats = pyqtSignal(dict)

    object_classes = {'mesero': Player, 'chef': Chef, 'mesa': Table}

    def __init__(self):
        super().__init__()
        # Entidades
        self.cafe = Cafe()
        self.players = list()
        self.chefs = list()
        self.tables = list()
        self.customers = list()
        # Diccionario de acceso
        self.object_lists = {
            'mesero': self.players,
            'chef': self.chefs,
            'mesa': self.tables
        }
        # Mapa
        self.map_size = (
            int(PARAMETROS['mapa']['largo']), int(PARAMETROS['mapa']['ancho'])
        )

    def new_game(self) -> None:
        '''Carga un nuevo juego'''
        self.signal_start_game_window.emit()
        self.cafe.money = PARAMETROS['DCCafé']['inicial']['dinero']
        self.cafe.rep = PARAMETROS['DCCafé']['inicial']['reputación']
        self.cafe.clients = PARAMETROS['DCCafé']['inicial']['clientes']
        # Creación de chefs aleatorias
        # TODO
        for _ in range(PARAMETROS['DCCafé']['inicial']['chefs']):
            pass
        # Creación de mesas aleatorias
        # TODO
        for _ in range(PARAMETROS['DCCafé']['inicial']['mesas']):
            pass
        self.start_round()

    def load_game(self) -> None:
        '''Carga un juego'''
        self.signal_start_game_window.emit()
        data = get_last_game_data()
        self.cafe.money = data['money']
        self.cafe.rep = data['rep']
        self.cafe.rounds = data['rounds']
        for object_name, pos_x, pos_y in data['map']:
            new_object = self.object_classes[object_name](pos_x, pos_y)
            if isinstance(new_object, Chef):
                new_object.dishes = int(data['dishes'].pop(0))
            # TODO: ver si los objetos colisionan
            self.object_lists[object_name].append(new_object)
            self.signal_add_new_object.emit(new_object.display_info)
        self.start_round()

    def exit_game(self):
        '''Sale del juego'''
        pass

    def pause_game(self):
        '''Pausa el juego'''
        pass

    def save_game(self):
        '''Guarda el juego'''
        pass

    def start_round(self):
        '''Empieza una ronda'''
        # TODO: esto tiene que estar conectado a un thread que maneje los tiempos
        self.signal_update_cafe_stats.emit(self.cafe.stats)

    def move_player(self, key: str):
        # TODO: esto no evita que el jugador no colisione
        # TODO: buscar una manera de ver la posición final cantes de actualizarla
        '''Mueve al jugador'''
        for player in self.players:
            if player.move(key):  # Si el jugador se movió
                self.signal_update_pos.emit(player.display_info)


def get_last_game_data() -> dict:
    '''Obtiene en un diccionario la información de la partida guardada'''
    last_game_data = {}
    # Cargar la información del mapa
    with open(PATH_MAPA, 'r', encoding='utf-8') as file:
        map_content = file.readlines()
    last_game_data['map'] = list(map(lambda line: line.split(','), map_content))
    # Cargar la información de el DCCafé
    with open(PATH_DATOS, 'r', encoding='utf-8') as file:
        stats = file.readline()
        dishes = file.readline()
    for key, value in zip(('money', 'rep', 'rounds'), stats.split(',')):
        last_game_data[key] = value
    last_game_data['dishes'] = dishes.split(',')
    return last_game_data
