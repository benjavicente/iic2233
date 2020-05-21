
from PyQt5.QtCore import QObject, pyqtSignal


class GameObject(QObject):
    signal_update_sprite = pyqtSignal(dict)
    id_counter = 0
    def __init__(self, type_name, x, y):
        super().__init__()
        self._type = type_name
        self._id = self.id_counter
        self.id_counter += 1
        self._x = y
        self._y = y

    @property
    def position(self):
        return (self._x, self._y)

    @property
    def data(self):
        return {'object': self._type, 'id': self._id, 'pos': self.position}



class Jugador(GameObject):
    '''
    Jugador del juego que empeña el rol de mesero
    Bonus: Dos jugadores al mismo tiempo
    '''
    def __init__(self, x, y):
        super().__init__('player', 0, 0)
        self._move_speed = 10
        self._movemet_keys = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}

    def move(self, key):
        # * Signal de KeyPressEvent
        if key in self._movemet_keys:
            move_x, move_y = self._movemet_keys[key]
            self._x += move_x * self._move_speed
            self._y += move_y * self._move_speed


class Mesa(GameObject):
    '''Mesa donde se pueden sentar los clientes'''
    def __init__(self, x, y):
        super().__init__('table', x, y)
        self.client = None


class Chef(GameObject):
    '''
    Preparan la comida.
    Tienen un nivel de experiencia relacionado con los platos preparador
    '''
    def __init__(self, x, y):
        super().__init__('chef', x, y)
        self._exp = int()
        self._platos_preparador = int()

    @property
    def platos_preparados(self):
        return self._platos_preparador

    @platos_preparados.setter
    def platos_preparados(self, value):
        # TODO: condiciones de experiencia
        self._platos_preparador += value
