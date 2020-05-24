'''Administrador del Juego'''

from random import choices, shuffle

from PyQt5.QtCore import QObject, pyqtSignal

from backend.game_objects import Player, Chef, Table, Cafe
from backend.clock import GameClock
from backend.paths import PATH_DATOS, PATH_MAPA

from config.parametros import PARAMETROS


class GameCore(QObject):
    '''
    Objeto que se encarga de conctar todo el backend con el frontend
    Almacena todos los objetos del backend
    '''

    signal_add_new_object = pyqtSignal(dict)
    signal_update_object = pyqtSignal(dict)
    signal_delete_object = pyqtSignal(dict)

    signal_start_game_window = pyqtSignal()
    signal_update_cafe_stats = pyqtSignal(dict)

    object_classes = {'mesero': Player, 'chef': Chef, 'mesa': Table}

    def __init__(self):
        super().__init__()
        self.cafe = Cafe()
        self.players = list()
        self.chefs = list()
        self.tables = list()
        self.set_up()

    def set_up(self):
        '''Crea objetos para el manejo del juego'''
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
        # Señales y theads de la simulación simulación
        self.clock_customer_spawn = GameClock(
            event=self.new_customer,
            interval=PARAMETROS['clientes']['periodo de llegada'],
        )
        # Posibilidades de tipos del cliente
        #* El formato puede mejorar
        self.posible_clients = list()
        client_types = {'relajado': 'hamster', 'apurado': 'dog', 'especial': 'special'}
        for c_name, c_info in PARAMETROS['clientes']['tipos'].items():
            client_type = client_types[c_name]
            wait_time = float(c_info['tiempo de espera'])
            probability = float(c_info['probabilidad'])
            self.posible_clients.append((client_type, wait_time, probability))

    # TODO: _API_ para el movimiento y las teclas especiales
    def add_key(self, key: str):
        # TODO
        pass

    def remove_key(self, key: str):
        # TODO
        pass

    def new_game(self) -> None:
        '''Carga un nuevo juego'''
        self.signal_start_game_window.emit()
        self.cafe.money = int(PARAMETROS['DCCafé']['inicial']['dinero'])
        self.cafe.rep = int(PARAMETROS['DCCafé']['inicial']['reputación'])
        self.cafe.clients = int(PARAMETROS['DCCafé']['inicial']['clientes'])
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
        self.cafe.money = int(data['money'])
        self.cafe.rep = int(data['rep'])
        self.cafe.rounds = int(data['rounds'])
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
        # TODO
        pass

    def save_game(self):
        '''Guarda el juego'''
        # TODO
        pass

    def pause_game(self):
        '''Pausa el juego'''
        self.clock_customer_spawn.pause_()

    def continue_game(self):
        '''Continua el juego'''
        self.clock_customer_spawn.continue_()

    def start_round(self):
        '''Empieza una ronda'''
        self.signal_update_cafe_stats.emit(self.cafe.stats)
        self.clock_customer_spawn.set_rep(self.cafe.round_clients)
        self.clock_customer_spawn.start()

    def move_player(self, key: str):
        # TODO: esto no evita que el jugador no colisione
        # TODO: buscar una manera de ver la posición final cantes de actualizarla
        #! Mejor rehacer el movimiento de los jugadores de 0
        '''Mueve al jugador'''
        for player in self.players:
            if player.move(key):  # Si el jugador se movió
                print(player.display_info)
                self.signal_update_object.emit(player.display_info)

    def new_customer(self):
        '''Llega un cliente a la tienda. Si hay mesas, se sienta y espera un pedido'''
        print('Ha llegado un cliente!')
        # Revuelve las mesas para que el la mesa sea al azar
        shuffle(self.tables)
        # Buscar si hay mesas
        for table in self.tables:
            if table.free:
                # Generar cliente
                print(self.posible_clients)
                new_client_type, new_client_wait_time, _ = choices(
                    self.posible_clients,
                    weights=[x[-1] for x in self.posible_clients]
                )[0]
                print(new_client_type, new_client_wait_time)
                customer = table.add_customer(new_client_type, new_client_wait_time)
                self.signal_add_new_object.emit(customer.display_info)
                return



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



