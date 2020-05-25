'''
Ventana del Juego DCCafé
'''

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QCursor, QKeyEvent, QTransform
from PyQt5.QtWidgets import QLabel

from frontend.paths import SPRITE_PATH
from frontend.themes import GAME_THEME


class GameWindow(*uic.loadUiType(SPRITE_PATH['ui', 'game_window'])):
    '''Ventana del juego'''

    signal_key_press = pyqtSignal(int)
    signal_key_relase = pyqtSignal(int)

    signal_pause_game = pyqtSignal()
    signal_continue_game = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_style()
        # Offset de la decoración en el cuadro de juego
        self.y_game_offset = 0
        # Objetos del juego a mostrar en el cuadro de juego
        self.game_objects = dict()
        # Pausa/Continuar
        self.paused = False
        self.button_time.pressed.connect(self.pause_continue)

    def add_style(self):
        '''
        Añade las imágenes, el estilo de la ventana y algunas animaciones.
        Se realiza en código ya que no se pudo realizar fácilmente en
        designer o porque permite cambios rápidos en algún path o estilo.
        '''
        # Imágenes
        self.logo.setPixmap(QPixmap(SPRITE_PATH['logo']))
        self.chef_icon.setPixmap(QPixmap(SPRITE_PATH['shop', 'chef']))
        self.table_icon.setPixmap(QPixmap(SPRITE_PATH['shop', 'table']))
        # Es raro que PointingHandCursor no este disponible en Designer...
        self.button_exit.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_time.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(GAME_THEME)

    def start(self):
        '''Inicia el juego'''
        # TODO: música?
        self.make_map()
        self.grabKeyboard()
        self.show()

    def keyPressEvent(self, key_event):
        # TODO: ver como implementar sin método los eventos
        '''Entrega las teclas apretadas al backend'''
        self.signal_key_press.emit(key_event.key())

    def keyReleaseEvent(self, key_event):
        # TODO: ver como implementar sin método los eventos
        '''Entrega las teclas soltadas al backend'''
        self.signal_key_relase.emit(key_event.key())

    def pause_continue(self):
        '''
        Pausa o continua el juego.
        Cambia el texto del botón.
        '''
        self.paused = not self.paused
        self.game_area.setDisabled(self.paused)
        if self.paused:
            self.signal_pause_game.emit()
            self.button_time.setText('Seguir')
        else:
            self.signal_continue_game.emit()
            self.button_time.setText('Pausar')

    def update_cafe_stats(self, stats: dict):
        '''Actualiza los datos del Café en la ventana'''
        self.rep.setText(stats['rep'])
        self.money.setText(stats['money'])
        self.round.setText(stats['round'])
        self.completed_orders.setText(stats['completed_orders'])
        self.total_orders.setText(stats['total_orders'])
        self.failed_orders.setText(stats['failed_orders'])

    def add_new_object(self, obj: dict):
        '''Crea un nuevo objeto en el area de juego'''
        new_object = QLabel(self.game_area)
        new_object.setAttribute(Qt.WA_DeleteOnClose)
        new_object.setGeometry(*obj['pos'], *obj['size'])
        new_object.setPixmap(QPixmap(SPRITE_PATH[obj['state']]))
        new_object.setScaledContents(True)
        new_object.show()
        self.game_objects[obj['id']] = new_object

    def update_object(self, obj: dict):
        '''Actualiza el sprite y la posición del objeto'''
        self.game_objects[obj['id']].setPixmap(QPixmap(SPRITE_PATH[obj['state']]))
        self.game_objects[obj['id']].move(*obj['pos'])

    def delete_object(self, obj: dict):
        '''Elimina un objeto'''
        self.game_objects[obj['id']].close()
        del self.game_objects[obj['id']]

    def stack_under(self, obj_below: dict, obj_above: dict):
        '''Mueve un objeto detrás de otro'''
        self.game_objects[obj_below['id']].stackUnder(self.game_objects[obj_above['id']])

    def make_map(self, width: int = 750, height: int = 450, cell_size: int = 25):
        '''Crea el mapa del juego a partir de los mapámetros dados'''
        if width % cell_size or height % cell_size:
            raise ValueError('El tamaño de la celda no es factor del tamaño del mapa')

        grid_width = width // cell_size
        grid_height = height // cell_size
        self.game_area.setFixedSize(width, height + cell_size * 4)

        area_grid = self.game_area.layout()

        window = QPixmap(SPRITE_PATH['map', 'window'])
        wall = QPixmap(SPRITE_PATH['map', 'wall'])
        tile = QPixmap(SPRITE_PATH['map', 'tile'])
        border = QPixmap(SPRITE_PATH['map', 'border'])

        # Se añade decoración
        for x_pos in range(0, grid_width, 2):
            decoration = QLabel(self.game_area)
            if x_pos % 4:
                decoration.setPixmap(window)
                decoration.setFixedSize(cell_size * 2, cell_size * 4)
            else:
                decoration.setPixmap(wall)
                decoration.setFixedSize(cell_size * 2, cell_size * 4)
            decoration.setScaledContents(True)
            area_grid.addWidget(decoration, 0, x_pos, 1, 2)

        # Se crean las celdas y se añaden al grid del juego
        for x_pos in range(grid_width):
            for y_pos in range(grid_height):
                if y_pos:
                    pixmap = tile
                else:
                    rotation = QTransform().rotate(90)
                    pixmap = border.transformed(rotation)
                cell = QLabel(self.game_area)
                cell.setFixedSize(cell_size, cell_size)
                cell.setPixmap(pixmap)
                cell.setScaledContents(True)
                area_grid.addWidget(cell, y_pos + 1, x_pos, 1, 1)
