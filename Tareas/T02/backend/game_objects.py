'''
Clases del los objetos del juego DCCafé
'''

from PyQt5.QtCore import QObject, pyqtSignal, QThread
from math import floor


from config.parametros import PARAMETROS



class GameObject(QObject):
    '''
    Clase abstracta de un objeto del juego.
    Crea un identificador único al objeto.
    Como atributo tiene display_info, que retorna
    toda la información necesaria para
    mostrar el objeto en la pantalla.
    '''
    signal_update_sprite = pyqtSignal(dict)
    _CELL_SIZE = PARAMETROS['mapa']['tamaño celda']
    id_counter = 0
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.class_name = type(self).__name__.lower()
        self._id = self.class_name + str(self.id_counter)
        self.id_counter += 1
        self._x = int(x)
        self._y = int(y)
        self.size = (int(width) * self._CELL_SIZE, int(height) * self._CELL_SIZE)
        self._object_state = [self.class_name]

    def __repr__(self):
        return self.id

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



class Player(GameObject):
    '''
    Jugador del juego que empeña el rol de mesero.
    Bonus: Dos jugadores al mismo tiempo.
    '''
    _movemet_direction = {'up': (0, -1), 'right': (1, 0), 'down': (0, 1), 'left': (-1, 0)}
    _movement_speed = PARAMETROS['personaje']['velocidad']

    def __init__(self, x: int, y: int):
        # TODO: parametros de disfraz y teclas
        super().__init__(x, y, 1, 2)
        # estado = (jugador, disfraz, libre o ocupado, tipo movimiento, direc movimiento)
        self._object_state += ['a', 'free', 'idle', 'down']
        self._movemet_keys = {'w': 'up', 'd': 'right', 's': 'down', 'a': 'left'}
        self.orders = 0

    def move(self, key) -> bool:
        '''
        Mueve al jugador según la tecla `key`
        Retorna si se pudo mover le jugador con esa tecla
        '''
        # * Signal de KeyPressEvent
        if key in self._movemet_keys:
            direction = self._movemet_keys[key]
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
        super().__init__(x, y, 4, 4)
        self._object_state += ['idle']
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


class Table(GameObject):
    '''Mesa donde se pueden sentar los clientes'''
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 1, 2)
        self.client = False


class Customer(GameObject):
    '''Cliente. Es asignado a una mesa aleatoria'''
    def __init__(self, x: int, y: int, customer_type: str):
        super().__init__(x, y, 1, 1)
        self.customer_type = customer_type
