'''
Ventana del Juego DCCafé
'''

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QLabel

from frontend.paths import PATH, SPRITE_PATH
from frontend.themes import GAME_THEME


class GameWindow(*uic.loadUiType(PATH['ui']['game_window'])):
    '''Ventana del juego'''
    signal_keypress = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_style()
        # Offset de la decoración en el cuadro de juego
        self.y_game_offset = 0
        # Objetos del juego a mostrar en el cuadro de juego
        self.game_objects = dict()

    def add_style(self):
        '''
        Añade las imágenes, el estilo de la ventana y algunas animaciones.
        Se realiza en código ya que no se pudo realizar fácilmente en
        designer o porque permite cambios rápidos en algún path o estilo.
        '''
        # Imágenes
        self.logo.setPixmap(QPixmap(PATH['logo']))
        self.chef_icon.setPixmap(QPixmap(PATH['shop']['chef']))
        self.table_icon.setPixmap(QPixmap(PATH['shop']['table']))
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

    def keyPressEvent(self, event):
        # TODO: este método no entrega señales completamente continuas
        self.signal_keypress.emit(event.text())

    def move_object(self, obj: dict):
        print(obj)  # TODO: remove
        self.game_objects[obj['id']].raise_()
        self.game_objects[obj['id']].setPixmap(QPixmap(SPRITE_PATH[obj['state']]))
        self.game_objects[obj['id']].move(*obj['pos'])
        self.game_objects[obj['id']].raise_()

    def add_new_object(self, obj: dict):
        '''`obj`: dict con id e información del objeto'''
        new_object = QLabel(self.game_area)
        new_object.setGeometry(*obj['pos'], *obj['size'])
        new_object.setPixmap(QPixmap(SPRITE_PATH[obj['state']]))
        new_object.setScaledContents(True)
        self.game_objects[obj['id']] = new_object
        new_object.show()

    def make_map(self, width: int = 750, height: int = 450, cell_size: int = 25):
        '''Crea el mapa del juego a partir de los mapámetros dados'''
        if width % cell_size or height % cell_size:
            mesage = 'Los valores del tamaño del mapa no son divisibles por el tamaño de la celda'
            raise ValueError(mesage)
        grid_width = width // cell_size
        grid_height = height // cell_size

        self.game_area.setFixedSize(width, height + cell_size * 4)
        area_grid = self.game_area.layout()

        # Se añade decoración
        for x_pos in range(0, grid_width, 2):
            decoration = QLabel(self.game_area)
            decoration.setStyleSheet('background: blue')
            if x_pos % 4:
                decoration.setPixmap(QPixmap(PATH['map']['window']))
                decoration.setFixedSize(cell_size * 2, cell_size * 4)
            else:
                decoration.setPixmap(QPixmap(PATH['map']['wall']))
                decoration.setFixedSize(cell_size * 2, cell_size * 4)
            decoration.setScaledContents(True)
            area_grid.addWidget(decoration, 0, x_pos, 1, 2)

        # Se crean las celdas y se añaden al grid del juego
        for x_pos in range(grid_width):
            for y_pos in range(grid_height):
                cell = QLabel(self.game_area)
                cell.setFixedSize(cell_size, cell_size)
                cell.setPixmap(QPixmap(PATH['map']['tile']))
                cell.setScaledContents(True)
                area_grid.addWidget(cell, y_pos + 1, x_pos, 1, 1)
