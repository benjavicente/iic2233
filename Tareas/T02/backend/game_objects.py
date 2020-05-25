'''
Clases del los objetos del juego DCCafé
'''

from PyQt5.QtCore import QObject, pyqtSignal, Qt
from math import floor


from config.parametros import PARAMETROS
from backend.clock import GameClock


def generate_ids():
    '''Genera un id para cada objeto'''
    counter = 0
    while True:
        yield counter
        counter += 1


class GameObject(QObject):
    '''
    Clase abstracta de un objeto del juego.
    Crea un identificador único al objeto.
    Como atributo tiene display_info, que retorna
    toda la información necesaria para
    mostrar el objeto en la pantalla.
    '''

    signal_create_object = pyqtSignal(dict)
    signal_update_object = pyqtSignal(dict)
    signal_delete_object = pyqtSignal(dict)

    _CELL_SIZE = PARAMETROS['mapa']['tamaño celda']
    id_counter = generate_ids()

    def __init__(self, x: int, y: int, width: int, height: int, initial_state: list):
        super().__init__()
        self.class_name = type(self).__name__.lower()
        self._id = str(next(GameObject.id_counter))
        self._x = int(x)
        self._y = int(y)
        self.size = (int(width) * self._CELL_SIZE, int(height) * self._CELL_SIZE)
        self._object_state = [self.class_name] + initial_state

    def __repr__(self):
        return self._id

    @property
    def position(self):
        '''Posición del objeto'''
        return (self._x, self._y)

    @property
    def display_info(self):
        '''Información que se manda al frontend'''
        return {
            'id': self._id,
            'pos': self.position,
            'size': self.size,
            'state': tuple(self._object_state),
        }



class Cafe(QObject):
    '''Café que se administra en el juego'''
    def __init__(self):
        super().__init__()
        # Parámetros guardados
        self.money = int()
        self.rep = int()
        self.rounds = int()
        # Parámetros de la ronda
        self.open = True
        self.completed_orders = 0
        self.total_orders = 0

    @property
    def stats(self):
        '''Estadísticas a mostrar en el interfaz'''
        return {
            'money': str(self.money),
            'rep': str(self.rep),
            'round': str(self.rounds),
            'open': str(self.open),
            'completed_orders': str(self.completed_orders),
            'total_orders': str(self.total_orders),
            'failed_orders': str(self.total_orders - self.completed_orders),
        }

    @property
    def round_clients(self):
        '''Clientes de la ronda'''
        alpha = int(PARAMETROS['DCCafé']['calculos']['clientes por ronda']['factor'])
        beta = int(PARAMETROS['DCCafé']['calculos']['clientes por ronda']['base'])
        return alpha * (beta + self.rounds)

    def get_new_rep(self) -> int:
        '''
        Calcula la nueva reputación del Café.
        Guarda el valor en el objeto y lo retorna.
        Solo debe ejecutarse al terminar la ronda.
        '''
        min_value = int(PARAMETROS['DCCafé']['calculos']['reputación']['mínimo'])
        max_value = int(PARAMETROS['DCCafé']['calculos']['reputación']['máximo'])
        alpha = int(PARAMETROS['DCCafé']['calculos']['reputación']['factor'])
        beta = int(PARAMETROS['DCCafé']['calculos']['reputación']['resta'])
        expr = self.rep + floor(alpha * self.completed_orders/self.total_orders - beta)
        self.rep = max(min_value, min(max_value, expr))
        return self.rep


# Game Objects

class Player(GameObject):
    '''
    Jugador del juego que empeña el rol de mesero.
    Bonus: Dos jugadores al mismo tiempo.
    '''
    _movemet_direction = {'up': (0, -1), 'right': (1, 0), 'down': (0, 1), 'left': (-1, 0)}
    _movement_speed = PARAMETROS['personaje']['velocidad']

    def __init__(self, x: int, y: int):
        # TODO: parametros de disfraz y teclas
        # estado = (jugador, disfraz, libre o ocupado, tipo movimiento, direc movimiento)
        super().__init__(x, y, 1, 2, ['a', 'free', 'idle', 'down'])
        self.movemet_keys = {Qt.Key_W: 'up', Qt.Key_D: 'right', Qt.Key_S: 'down', Qt.Key_A: 'left'}
        self.orders = 0

    def move(self, key) -> bool:
        #! Este método debe re-implementarse.
        #! La forma actual no puede detectar colisiones
        #! y no es muy eficaz con la implementación nueva
        #! de la obtención de teclas en GameCore.
        '''
        Mueve al jugador según la tecla `key`
        Retorna si se pudo mover le jugador con esa tecla
        '''
        if key in self.movemet_keys:
            direction = self.movemet_keys[key]
            self._object_state[4] = direction
            move_x, move_y = self._movemet_direction[direction]
            self._x += move_x * self._movement_speed
            self._y += move_y * self._movement_speed
            return True
        return False



class Chef(GameObject):
    '''
    Preparan la comida.
    Tienen un nivel de experiencia relacionado con los platos preparador
    '''
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 4, 4, ['idle'])
        # TODO
        self._exp = int()
        self._dishes = int()

    @property
    def dishes(self):
        '''Platos preparados por el Chef'''
        return self._dishes

    @dishes.setter
    def dishes(self, value):
        # TODO: condiciones de experiencia
        self._dishes = value


class Customer(GameObject):
    '''Cliente. Es asignado a una mesa aleatoria'''
    def __init__(self, x: int, y: int, table, customer_type: str, wait_time: int):
        super().__init__(x, y, 1, 2, [customer_type])
        self.table = table
        self.wait_time = wait_time
        self.customer_type = customer_type
        self.clock = GameClock(interval=wait_time, final_event=self.exit_cafe, rep=1)
        self.clock.start()

    def exit_cafe(self):
        '''Cliente se retira de la mesa'''
        print('me voy >:(')
        self.signal_delete_object.emit(self.display_info)
        self.table.free = True
        self.table.customer = None



class Table(GameObject):
    '''Mesa donde se pueden sentar los clientes'''
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 1, 2, [])
        self.free = True
        self.customer = None

    def add_customer(self, customer_type: str, wait_time: int) -> Customer:
        '''Añade un cliente a la mesa y lo retorna'''
        self.free = False
        self.customer = Customer(*self.position, self, customer_type, wait_time)
        print(f'Cliente {customer_type} asignado en la mesa {self._id}')
        #! La mesa debe encargarse del manejo del cliente, no el GameCore
        return self.customer

