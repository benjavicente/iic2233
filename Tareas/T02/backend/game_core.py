'''Administrador del Juego'''

from random import choices, shuffle

from PyQt5.QtCore import QObject, Qt, pyqtSignal

from backend.clock import GameClock
from backend.game_objects import Cafe, Chef, GameObject, Player, Table
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
    signal_stack_under = pyqtSignal(dict, dict)

    signal_start_game_window = pyqtSignal(tuple)
    signal_update_cafe_stats = pyqtSignal(dict)

    signal_pause_objects = pyqtSignal()
    signal_resume_objects = pyqtSignal()

    signal_show_paused = pyqtSignal(bool)

    object_classes = {'mesero': Player, 'chef': Chef, 'mesa': Table}

    def __init__(self):
        super().__init__()
        self._cafe = Cafe()
        self._players = list()
        self._chefs = list()
        self._tables = list()
        self.__set_up()

    def __iter__(self):
        return iter(self._tables + self._chefs)

    def __set_up(self) -> None:
        '''Crea objetos para el manejo del juego'''
        # Parámetros especiales
        self._key_access_rate = 0.05  # En segundos
        self._remaining_clients = 0
        self.paused = False
        # Diccionario de acceso
        self._object_lists = {
            'mesero': self._players,
            'chef': self._chefs,
            'mesa': self._tables
        }
        # Mapa
        self._map_size = (
            int(PARAMETROS['mapa']['largo']), int(PARAMETROS['mapa']['ancho'])
        )
        # Set de teclas precionadas
        self._pressed_keys = set()
        # Relojes de la simulación
        self._clock_customer_spawn = GameClock(
            event=self.__new_customer,
            interval=PARAMETROS['clientes']['periodo de llegada'],
        )
        self._clock_check_keys = GameClock(
            event=self._check_keys,
            interval=self._key_access_rate,  # Frecuencia de obtención de teclas
        )
        # Posibilidades de tipos del cliente
        # TODO: el cliente especial aparece una vez, con una probabilidad determinada
        # TODO: y tiene un tiempo de espera aleatorio. Esto NO funciona con el método
        # TODO: actual para crear los clientes. Puede ser mejor generalos a todos
        # TODO: al comienzo de la ronda y no realizar este procedimiento aquí.
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

    def add_key(self, key: int) -> None:
        '''Añade una tecla al las teclas precionadas'''
        self._pressed_keys.add(key)
        # Pausa
        if Qt.Key_P == key:
            self.pause_continue_game()

    def remove_key(self, key: int) -> None:
        '''Remueve una tecla al las teclas precionadas'''
        self._pressed_keys.remove(key)

    def _check_keys(self) -> None:
        '''
        Revisa si hay teclas precionadas.
        Si es que hay, se revisa cuales y
        se se ejecutan las acciones asociadas.
        '''
        if self._pressed_keys:
            # Movimiento jugadores
            print(self._pressed_keys)
            for player in self._players:
                next_pos = player.next_pos(
                    filter(lambda k, p=player: p.has_key(k), self._pressed_keys),
                    self._key_access_rate
                )
                # TODO: los hitboxes son muy grandes
                colision_list = self.__check_colision(player.id, player.new_hitbox(next_pos))
                print(colision_list)
                if colision_list:
                    pass
                    # TODO: do something
                else:
                    player.move(next_pos)

    def new_game(self) -> None:
        '''Carga un nuevo juego'''
        self.signal_start_game_window.emit(self._map_size)
        self._cafe.money = int(PARAMETROS['DCCafé']['inicial']['dinero'])
        self._cafe.rep = int(PARAMETROS['DCCafé']['inicial']['reputación'])
        self._cafe.clients = int(PARAMETROS['DCCafé']['inicial']['clientes'])
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
        self.signal_start_game_window.emit(self._map_size)
        data = get_last_game_data()
        self._cafe.money = int(data['money'])
        self._cafe.rep = int(data['rep'])
        self._cafe.rounds = int(data['rounds'])
        for object_name, pos_x, pos_y in data['map']:
            new_object = self.object_classes[object_name](self, int(pos_x), int(pos_y))
            if isinstance(new_object, Chef):
                new_object.dishes = int(data['dishes'].pop(0))
            # TODO: ver si los objetos colisionan
            self._object_lists[object_name].append(new_object)
        self.start_round()

    def exit_game(self) -> None:
        '''Sale del juego'''
        # TODO
        pass

    def save_game(self) -> None:
        '''Guarda el juego'''
        # TODO
        pass

    def pause_continue_game(self) -> None:
        '''Pausa el juego'''
        if self.paused:
            self._clock_customer_spawn.continue_()
            self._clock_check_keys.start()
            self.signal_resume_objects.emit()
        else:
            self._clock_customer_spawn.pause_()
            self._clock_check_keys.stop()
            self.signal_pause_objects.emit()
        self.paused = not self.paused
        self.signal_show_paused.emit(self.paused)

    def start_round(self) -> None:
        '''Empieza una ronda'''
        self.signal_update_cafe_stats.emit(self._cafe.stats)
        self._remaining_clients = self._cafe.round_clients
        self._clock_customer_spawn.start()
        self._clock_check_keys.start()

    def __new_customer(self) -> None:
        '''Llega un cliente a la tienda. Si hay mesas, se sienta y espera un pedido'''
        print('Ha llegado un cliente!')
        shuffle(self._tables)
        for table in self._tables:
            if table.free:
                # Generar cliente
                new_client_type, new_client_wait_time, _ = choices(
                    self.posible_clients,
                    weights=[x[-1] for x in self.posible_clients]
                )[0]  # El [0] es porque choices retorna una lista de largo 1
                # Se añade el cliente a la mesa
                table.add_customer(new_client_type, new_client_wait_time)
                # Disminuye la cantidad de clientes restantes
                self._remaining_clients -= 1
                if not self._remaining_clients:
                    print('Se han acabado los clientes!')
                    self._clock_customer_spawn.stop()
                return
        print('El cliente se ha ido por falta de mesas, volverá luego')

    def __check_colision(self, moved_obj_id: str, moved_object_hitbox: tuple) -> list:
        '''
        Revisa si el objeto entregado colisiona con algo.
        Retorna una lista con los elementos que coliciona.
        '''
        x1, y1, w1, h1 = moved_object_hitbox
        collied = list()
        for game_object in self:
            if moved_obj_id == game_object.id:
                continue
            x2, y2, w2, h2 = game_object.hit_box
            # Hay muchas páginas que mencionan como realizar
            # colisiones entre cuadrados. Mozilla tiene un ejemplo básico:
            # https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
            if x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2:
                collied.append(game_object)
        return collied




def get_last_game_data() -> dict:
    '''Obtiene en un diccionario la información de la partida guardada'''
    last_game_data = {}
    # Cargar la información de el DCCafé
    with open(PATH_DATOS, 'r', encoding='utf-8') as file:
        stats = file.readline()
        dishes = file.readline()
    for key, value in zip(('money', 'rep', 'rounds'), stats.split(',')):
        last_game_data[key] = value
    last_game_data['dishes'] = dishes.split(',')
    # Cargar la información del mapa
    with open(PATH_MAPA, 'r', encoding='utf-8') as file:
        map_content = file.readlines()
    last_game_data['map'] = [line.split(',') for line in map_content]
    return last_game_data
