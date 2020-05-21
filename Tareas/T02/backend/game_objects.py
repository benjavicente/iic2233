
from PyQt5.QtCore import QObject, pyqtSignal

PATH_MESERO = R'sprites\mesero\down_02.png'
PATH_MESA = R'sprites\mapa\accesorios\silla_mesa_roja.png'
PATH_CHEF = R'sprites\chef\meson_01.png'

class GameObject(QObject):
    signal_update_sprite = pyqtSignal(dict)
    id_counter = 0
    def __init__(self, x, y, width, height, sprite_path):
        super().__init__()
        self._class_name = type(self).__name__
        self._id = self._class_name + str(self.id_counter)
        self.id_counter += 1
        self._x = int(x)
        self._y = int(y)
        self._width = int(width)
        self._height = int(height)
        self._sprite_path = str(sprite_path)

    def __repr__(self):
        return self._id

    @property
    def position(self):
        return (self._x, self._y)

    @property
    def size(self):
        return (self._width, self._height)

    @property
    def data(self):
        return {
            'id': self._id,
            'pos': self.position,
            'size': self.size,
            'sprite_path': self._sprite_path
        }



class Player(GameObject):
    '''
    Jugador del juego que empeña el rol de mesero
    Bonus: Dos jugadores al mismo tiempo
    '''
    def __init__(self, x, y):
        super().__init__(x, y, 30, 50, PATH_MESERO)
        self._move_speed = 10
        self._movemet_keys = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}

    def move(self, key):
        # * Signal de KeyPressEvent
        if key in self._movemet_keys:
            move_x, move_y = self._movemet_keys[key]
            self._x += move_x * self._move_speed
            self._y += move_y * self._move_speed


class Table(GameObject):
    '''Mesa donde se pueden sentar los clientes'''
    def __init__(self, x, y):
        super().__init__(x, y, 30, 45, PATH_MESA)
        self.client = None


class Chef(GameObject):
    '''
    Preparan la comida.
    Tienen un nivel de experiencia relacionado con los platos preparador
    '''
    def __init__(self, x, y):
        super().__init__(x, y, 60, 70, PATH_CHEF)
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
