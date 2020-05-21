
from PyQt5.QtCore import QObject, pyqtSignal

class Jugador(QObject):
    '''
    Jugador del juego que empeña el rol de mesero
    Bonus: Dos jugadores al mismo tiempo
    '''
    signal_update_pos = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.__x = 0
        self.__y = 0
        self._move_speed = 10
        self._movemet_keys = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}

    def set_position(self, x, y):
        self.__x = y
        self.__y = x

    def move(self, x, y):
        self.__x += x * self._move_speed
        self.__y += y * self._move_speed
        self.signal_update_pos.emit(self.position)

    @property
    def position(self):
        return (self.__x, self.__y)

    def mover(self, key):
        if key in self._movemet_keys:
            self.move(*self._movemet_keys[key.lower()])
