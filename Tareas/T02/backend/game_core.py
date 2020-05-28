'''Administrador del Juego'''

from random import choices, shuffle, random, randint
from functools import namedtuple

from PyQt5.QtCore import QObject, Qt, pyqtSignal

from backend.clock import GameClock
from backend.cafe import Cafe
from backend.game_objects import Chef, Player, Table
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
    signal_move_up = pyqtSignal(dict)

    signal_start_game_window = pyqtSignal(tuple)

    signal_update_cafe_stats = pyqtSignal(dict)

    signal_pause_objects = pyqtSignal()
    signal_resume_objects = pyqtSignal()

    signal_show_paused = pyqtSignal(bool)

    signal_show_end_screen = pyqtSignal(dict)

    signal_shop_enable = pyqtSignal(bool)

    signal_exit_game = pyqtSignal()

    object_classes = {'mesero': Player, 'chef': Chef, 'mesa': Table}
    shop_prices = {
        'table_price': PARAMETROS['tienda']['mesa'],
        'chef_price': PARAMETROS['tienda']['chef']}
    shop_names = {'table': Table, 'chef': Chef}

    cell_size = PARAMETROS['mapa']['tamaño celda']

    def __init__(self):
        super().__init__()
        self.cafe = Cafe()
        self._players = list()
        self._chefs = list()
        self._tables = list()
        self.paused = False
        self._key_access_rate = 1/30  # En segundos
        self.__set_up()

    def __set_up(self) -> None:
        '''Crea objetos para el manejo del juego'''
        #######################################################################
        # Lista que almacena los clientes de la ronda
        self.round_clients = list()
        # Mapa
        self._map_size = (
            int(PARAMETROS['mapa']['largo']), int(PARAMETROS['mapa']['alto'])
        )
        # Set de teclas precionadas
        self._pressed_keys = set()
        # Relojes de la simulación
        spawn_interval = PARAMETROS['clientes']['periodo de llegada']
        self._clock_customer_spawn = GameClock(self, self.__new_customer, spawn_interval)
        self._clock_check_keys = GameClock(self, self._check_movement_keys, self._key_access_rate)
        self._clock_check_special_keys = GameClock(self, self._check_special_keys)
        self._clock_check_if_empty = GameClock(self, self.check_if_empty)
        # Posibilidades de tipos del cliente, en referencia al archivo parámetros y paths
        client_real_types = {'relajado': 'hamster', 'apurado': 'dog', 'presidente': 'president'}
        self.posible_clients = list()  # Clientes normales
        self.client_tuple = namedtuple('PosibleClient', ['type', 'wait_time', 'prob'])
        for c_name, c_info in PARAMETROS['clientes']['tipos']['básicos'].items():
            self.posible_clients.append(self.client_tuple(
                client_real_types[c_name],
                int(c_info['tiempo de espera']),
                float(c_info['probabilidad'])
            ))
        self.posible_specials = list()  # Clientes especiales
        self.special_tuple = namedtuple('PosibleSpecial', ['type', 'rep', 'max', 'min', 'prob'])
        for c_name, c_info in PARAMETROS['clientes']['tipos']['especiales'].items():
            self.posible_specials.append(self.special_tuple(
                client_real_types[c_name],
                int(c_info['reputación']),
                int(c_info['max']),
                int(c_info['min']),
                float(c_info['probabilidad'])
            ))
        # Se inicia el reloj que revisa si se precionaron teclas especiales
        self._clock_check_special_keys.start()
        #######################################################################

    def add_key(self, key: int) -> None:
        '''Añade una tecla al las teclas precionadas'''
        self._pressed_keys.add(key)
        if Qt.Key_P == key:  # Pausa el juego
            self.pause_continue_game()

    def remove_key(self, key: int) -> None:
        '''Remueve una tecla al las teclas precionadas'''
        self._pressed_keys.remove(key)

    def _check_movement_keys(self) -> None:
        '''Revisa si hay teclas precionadas de  movimiento'''
        if self._pressed_keys:
            for player in self._players:  # Movimiento jugadores
                keys = set(filter(lambda k, p=player: k in p.movemet_keys, self._pressed_keys))
                if not keys:
                    continue # Las teclas precionadas no son del jugador, se continua
                next_pos = player.next_pos(keys, self._key_access_rate)
                colision_list = self.__check_colision(player.new_hitbox(next_pos), player.id)
                if colision_list:  # Si colisiona, interactúa con objetos
                    for object_type in colision_list:
                        if isinstance(object_type, (Chef, Table)):
                            object_type.interact(player)
                else:  # Si no es el caso, se mueve
                    player.move(next_pos)

    def _check_special_keys(self) -> None:
        '''Revisa si hay teclas especiales precionadas'''
        if self._pressed_keys:
            if all(key in self._pressed_keys for key in [Qt.Key_M, Qt.Key_O, Qt.Key_Y]):
                self.cafe.money += PARAMETROS['trampas']['dinero']
                self.update_ui_information()
            if all(key in self._pressed_keys for key in [Qt.Key_F, Qt.Key_I, Qt.Key_N]):
                self._clock_customer_spawn.stop()
                self._clock_check_if_empty.start()
            if all(key in self._pressed_keys for key in [Qt.Key_B, Qt.Key_T, Qt.Key_G]):
                self.cafe.rep += PARAMETROS['trampas']['reputación']
                self.update_ui_information()

    def new_game(self, info: dict) -> None:
        '''Carga un nuevo juego'''
        # Inicia la ventana
        self.signal_start_game_window.emit(self._map_size)
        # Datos del Café
        self.cafe.money = int(PARAMETROS['DCCafé']['inicial']['dinero'])
        self.cafe.rep = int(PARAMETROS['DCCafé']['inicial']['reputación'])
        self.cafe.clients = int(PARAMETROS['DCCafé']['inicial']['clientes'])
        # Parametros del mapa
        max_x, max_y = self._map_size
        # Creación de chefs aleatorias
        remaining_chefs = PARAMETROS['DCCafé']['inicial']['chefs']
        while remaining_chefs:
            x_pos, y_pos = randint_xy(max_x - 4 * self.cell_size, max_y - 4 * self.cell_size)
            if not self.__check_colision((x_pos, y_pos, 4 * self.cell_size, 4 * self.cell_size)):
                self._chefs.append(Chef(self, x_pos, y_pos))
                remaining_chefs -= 1
        # Creación de mesas aleatorias
        remaining_tables = PARAMETROS['DCCafé']['inicial']['mesas']
        while remaining_tables:
            x_pos, y_pos = randint_xy(max_x - 1 * self.cell_size, max_y - 2 * self.cell_size)
            if not self.__check_colision((x_pos, y_pos, 1 * self.cell_size, 2 * self.cell_size)):
                self._tables.append(Table(self, x_pos, y_pos))
                remaining_tables -= 1
        # Creación del jugador
        self.generate_players(info['players'], self.cell_size, max_x, max_y)
        # Inicio del juego
        self.start_round()

    def load_game(self, info: dict) -> None:
        '''Carga un juego'''
        # Inicia la ventana
        self.signal_start_game_window.emit(self._map_size)
        # Obtención de los datos guardados
        data = get_last_game_data()
        # Datos del Café
        self.cafe.money = int(data['money'])
        self.cafe.rep = int(data['rep'])
        self.cafe.round = int(data['round'])
        # Creación de entidades
        object_lists = {'mesero': self._players, 'chef': self._chefs, 'mesa': self._tables}
        for object_name, pos_x, pos_y in data['map']:
            new_object = self.object_classes[object_name](self, int(pos_x), int(pos_y))
            if isinstance(new_object, Chef):
                new_object.dishes = int(data['dishes'].pop(0))
            object_lists[object_name].append(new_object)
        # Creación del jugador adicional (si es que hay)
        self.generate_players(info['players'] - 1, self.cell_size, *self._map_size)
        # Inicio del juego
        self.start_round()

    def generate_players(self, players: int, cell_size: int, max_x: int, max_y: int) -> None:
        '''Método para unir la generación de clientes en load_game y new_game'''
        while players:
            x_pos, y_pos = randint_xy(max_x - 1 * cell_size, max_y - 2 * cell_size)
            if not self.__check_colision((x_pos, y_pos, 1 * cell_size, 2 * cell_size)):
                self._players.append(Player(self, x_pos, y_pos))
                players -= 1

    def exit_game(self) -> None:
        '''Sale del juego'''
        self.signal_exit_game.emit() #* Esto puede ser solo una señal

    def save_game(self) -> None:
        '''Guarda el juego'''
        game_data = [self.cafe.money, self.cafe.rep, self.cafe.round]
        chef_dishes = [chef.dishes for chef in self._chefs]
        map_data = []
        #! Invertir un diccionario
        #! https://stackoverflow.com/a/483833
        clases_objects = {obj_c: name for name, obj_c in self.object_classes.items()}
        for game_object in [self._players[0]] + self._tables + self._chefs:
            pos_x, pos_y = game_object.pos
            if isinstance(game_object, Table):
                pos_y -= self.cell_size
            # Se guarda el nombre del objeto con su posición
            map_data.append([clases_objects[type(game_object)], int(pos_x), int(pos_y)])
        save_game(game_data, chef_dishes, map_data)  # Función externa

    def continue_game(self) -> None:
        '''Continua el juego. Se habilita la tienda'''
        self.signal_shop_enable.emit(True)
        self._clock_check_keys.start()

    def reset_round(self) -> None:
        '''Elimina cualquier proceso de la ronda pasada'''
        for player in self._players:
            player.give_order_to_client()  # Bota el bocadillo
            player.orders = 0  # Elimina las ordenes pendientes
        for chef in self._chefs:
            chef.stop_cooking()  # Reinicia el estado del chef

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
        # Se cierra la tienda
        self.signal_shop_enable.emit(False)
        # Se reinician los valores de la ronda
        self.cafe.new_round_values()
        # Generación de clientes
        self.round_clients.clear()
        for pos_special in self.posible_specials:  # Especiales
            if pos_special.prob > random():
                self.round_clients.append(pos_special)
        for _ in range(self.cafe.round_clients - len(self.round_clients)):  # Básicos
            client = choices(self.posible_clients, [c.prob for c in self.posible_clients])[0]
            self.round_clients.append(client)
        shuffle(self.round_clients)  # Se revuelve, de modo que el especial no quede primero
        # Se inicia la información del ui
        self.update_ui_information(round_clients=len(self.round_clients), **self.shop_prices)
        # Se inicia el spawn de clientes
        self._clock_customer_spawn.start()
        # Se habilita el movimiento si es que no está activado
        self._clock_check_keys.start()

    def update_ui_information(self, **extras) -> None:
        '''Actualiza los datos del ui'''
        stats = {**self.cafe.stats, **extras, 'remaining_clients': len(self.round_clients)}
        self.signal_update_cafe_stats.emit(stats)

    def __new_customer(self) -> None:
        '''Llega un cliente a la tienda. Si hay mesas, se sienta y espera un pedido'''
        shuffle(self._tables)  # Cambia el orden de las mesas
        for table in self._tables:
            if table.free:
                client = self.round_clients.pop()
                if isinstance(client, self.special_tuple):
                    # Si es especial, se genera un tiempo de espera al azar
                    wait_time = randint(client.min, client.max)
                    table.add_customer('special', client.type, wait_time, client.rep)
                elif isinstance(client, self.client_tuple):
                    # Si es básico, solo se añaden los atributos
                    table.add_customer('basic', client.type, client.wait_time)
                # Ahora se revisa si quedan clientes
                if not self.round_clients:
                    print('Se han acabado los clientes!')
                    self._clock_check_if_empty.start()  # Cada segundo chekea si está vació
                    self._clock_customer_spawn.stop()  # Se para el generador
                self.update_ui_information()
                return  # Termina el método ya que se generó un cliente

    def __check_colision(self, moved_object_hitbox: tuple, moved_obj_id: str = '') -> list:
        '''
        Revisa si el objeto entregado colisiona con algo.
        Retorna una lista con los elementos que coliciona.
        '''
        collied = list()
        for game_object in self._players + self._tables + self._chefs:
            if moved_obj_id == game_object.id:
                continue  # Se omite las colisiones del objeto con si mismo
            if check_colision(moved_object_hitbox, game_object.hit_box):
                collied.append(game_object)
        # Colición con el bode del mapa del juego
        obj_x, obj_y, obj_w, obj_h = moved_object_hitbox
        map_width, map_height = self._map_size
        if obj_x < 0 or obj_y < 0 or obj_x + obj_w > map_width or obj_y + obj_h > map_height:
            collied.append('map')
        return collied

    def check_if_empty(self) -> None:
        '''Revisa si se acabarón los clientes, para luego terminar la ronda'''
        self.cafe.open = False
        self.update_ui_information()
        if all(map(lambda table: table.free, self._tables)):
            self._clock_check_if_empty.stop()
            self.cafe.get_new_rep()
            self.reset_round()
            self._clock_check_keys.stop()
            self.signal_show_end_screen.emit(self.cafe.stats)

    def buy_object(self, info: dict) -> None:
        '''Se compra un objeto y se añade al juego'''
        if not self.__check_colision((*info['pos'], *info['size'])):
            name = info['type']
            # Se reviza que alcance el dinero
            if self.shop_prices[name + '_price'] <= self.cafe.money:
                self.cafe.money -= self.shop_prices[name + '_price']
                new_object = self.shop_names[name](self, *info['pos'])
                if isinstance(new_object, Chef):
                    self._chefs.append(new_object)
                elif isinstance(new_object, Table):
                    self._tables.append(new_object)
                self.update_ui_information()

    def sell_object(self, pos: tuple) -> None:
        '''Se vende el objeto en la posición entregada'''
        for game_object in self.__check_colision((*pos, 0, 0)):
            # En el caso que quede un elemento, no se vende
            if isinstance(game_object, Chef) and len(self._chefs) > 1:
                self.cafe.money += self.shop_prices['chef_price']
                self._chefs.remove(game_object)
            elif isinstance(game_object, Table) and len(self._tables) > 1:
                self.cafe.money += self.shop_prices['table_price']
                self._tables.remove(game_object)
                game_object.chair.delete_object()
            else:
                return  # Si no es ni mesa ni chef, termina el método
            game_object.delete_object()
            self.update_ui_information()


# Funciones de utilidad

def check_colision(hitbox1, hitbox2) -> True:
    '''Formula para calcular colisiones'''
    # Hay muchas páginas que mencionan como realizar
    # colisiones entre cuadrados. Mozilla tiene un ejemplo básico:
    # https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
    x_1, y_1, w_1, h_1 = hitbox1
    x_2, y_2, w_2, h_2 = hitbox2
    return all([x_1 + w_1 > x_2, x_1 < x_2 + w_2, y_1 + h_1 > y_2, y_1 < y_2 + h_2])


def get_last_game_data() -> dict:
    '''Obtiene en un diccionario la información de la partida guardada'''
    last_game_data = {}
    # Cargar la información de el DCCafé
    with open(PATH_DATOS, 'r', encoding='utf-8') as file:
        stats = file.readline()
        dishes = file.readline()
    for key, value in zip(('money', 'rep', 'round'), stats.split(',')):
        last_game_data[key] = value
    last_game_data['dishes'] = dishes.split(',')
    # Cargar la información del mapa
    with open(PATH_MAPA, 'r', encoding='utf-8') as file:
        map_content = file.readlines()
    last_game_data['map'] = [line.split(',') for line in map_content]
    return last_game_data


def save_game(game_data: list, chef_dishes: list, map_data: list):
    '''Guarda la partida'''
    # Guarda los datos del juego
    game_data = '\n'.join([','.join(map(str, game_data)), ','.join(map(str, chef_dishes))])
    with open(PATH_DATOS, 'w', encoding='utf-8') as file:
        file.write(game_data)
    # Guarda los datos del mapa
    map_data = '\n'.join([','.join(map(str, x)) for x in map_data])
    with open(PATH_MAPA, 'w', encoding='utf-8') as file:
        file.write(map_data)

def randint_xy(max_x, max_y):
    '''Obtiene coordenadas aleatorias para x e y entre (0, max_x) y (0, max_y)'''
    return (randint(0, max_x), randint(0, max_y))
