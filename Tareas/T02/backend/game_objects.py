'''
Clases del los objetos del juego DCCafé
'''

from PyQt5.QtCore import QObject, pyqtSignal, QThread

from config.parametros import PARAMETROS_JUEGO

_CELL_SIZE = PARAMETROS_JUEGO['mapa']['tamaño celda']


class GameObject(QObject):
    '''Clase abstracta de un objeto del juego'''
    signal_update_sprite = pyqtSignal(dict)
    id_counter = 0
    def __init__(self, x, y, width, height):
        super().__init__()
        self.class_name = type(self).__name__.lower()
        self._id = self.class_name + str(self.id_counter)
        self.id_counter += 1
        self._x = int(x)
        self._y = int(y)
        self.size = (int(width) * _CELL_SIZE, int(height) * _CELL_SIZE)
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



class Player(GameObject):
    '''
    Jugador del juego que empeña el rol de mesero.
    Bonus: Dos jugadores al mismo tiempo.
    '''
    _movemet_direction = {'up': (0, -1), 'right': (1, 0), 'down': (0, 1), 'left': (-1, 0)}
    _move_speed = _CELL_SIZE/2

    def __init__(self, x, y):
        super().__init__(x, y, 1, 2)
        # estado = (jugador, disfraz, libre o ocupado, tipo movimiento, direc movimiento)
        self._object_state += ['a', 'free', 'idle', 'down']
        self._movemet_keys = {'w': 'up', 'd': 'right', 's': 'down', 'a': 'left'}

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
            self._x += move_x * self._move_speed
            self._y += move_y * self._move_speed
            return True
        return False



class Chef(GameObject):
    '''
    Preparan la comida.
    Tienen un nivel de experiencia relacionado con los platos preparador
    '''
    def __init__(self, x, y):
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
        self._dishes += value


class Table(GameObject):
    '''Mesa donde se pueden sentar los clientes'''
    def __init__(self, x, y):
        super().__init__(x, y, 1, 2)
        self.client = None


class Customer(GameObject):
    '''Cliente. Es asignado a una mesa aleatoria'''
    pass
