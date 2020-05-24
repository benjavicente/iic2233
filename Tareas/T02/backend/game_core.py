'''Administrador del Juego'''

from random import choices, shuffle

from PyQt5.QtCore import QObject, pyqtSignal, Qt

from backend.game_objects import GameObject, Player, Chef, Table, Cafe
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
        # Parámetros especiales
        self.key_access_rate = 0.05  # En segundos
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
        # Set de teclas precionadas
        self.pressed_keys = set()
        # Relojes de la simulación
        self.clock_customer_spawn = GameClock(
            event=self.new_customer,
            interval=PARAMETROS['clientes']['periodo de llegada'],
        )
        self.clock_check_keys = GameClock(
            event=self.check_keys,
            interval=0.01,  # Frecuencia de obtención de teclas
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

    # 24/05
    # La idea de usar sets para crear un _API_ de teclas apretadas
    # está en multiples foros. Se menciona la aplicación de un event-filter,
    # pero creo que no es compatible con la forma ehn que estoy modelando el
    # backend y frontend.

    def add_key(self, key: str):
        '''Añade una tecla al las teclas precionadas'''
        self.pressed_keys.add(key)

    def remove_key(self, key: str):
        '''Remueve una tecla al las teclas precionadas'''
        self.pressed_keys.remove(key)

    def check_keys(self):
        '''
        Revisa si hay teclas precionadas.
        Si es que hay, se revisa cuales y
        se se ejecutan las acciones asociadas.
        '''
        # TODO
        if self.pressed_keys:
            print(self.pressed_keys)
            for key in self.pressed_keys:
                for player in self.players:
                    #! Aquí debe verse las colisiones del jugador
                    if player.move(key):
                        pass
                    self.signal_update_object.emit(player.display_info)

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
        self.clock_check_keys.start()

    def new_customer(self):
        '''Llega un cliente a la tienda. Si hay mesas, se sienta y espera un pedido'''
        print('Ha llegado un cliente!')
        # Revuelve las mesas para que el la mesa sea al azar
        shuffle(self.tables)
        # Buscar si hay mesas
        for table in self.tables:
            if table.free:
                # Generar cliente
                new_client_type, new_client_wait_time, _ = choices(
                    self.posible_clients,
                    weights=[x[-1] for x in self.posible_clients]
                )[0]
                print(new_client_type, new_client_wait_time)
                customer = table.add_customer(new_client_type, new_client_wait_time)
                #! TEST
                customer.signal_delete_object.connect(self.signal_delete_object.emit)
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



