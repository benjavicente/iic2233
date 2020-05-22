'''
Ventana del Juego DCCafé
'''

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QLabel

from frontend.data.ui_tools import (RUTA_CELDA, RUTA_DEC_1, RUTA_DEC_2,
                                    RUTA_LOGO, RUTA_TIENDA_CHEF,
                                    RUTA_TIENDA_MESA,
                                    STYLE_SHEET_VENTANA_JUEGO)


class GameWindow(*uic.loadUiType('frontend/data/juego.ui')):  # TODO: path relativo
    '''Ventana del juego'''
    signal_keypress = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_style()
        self.y_game_offset = 0
        self.game_objects = dict()

    def add_style(self):
        '''
        Añade las imágenes, el estilo de la ventana y algunas animaciones.
        Se realiza en código ya que no se pudo realizar fácilmente en
        designer o porque permite cambios rápidos en algún path o estilo.
        '''
        self.logo.setPixmap(QPixmap(RUTA_LOGO))
        self.chef_icon.setPixmap(QPixmap(RUTA_TIENDA_CHEF))
        self.table_icon.setPixmap(QPixmap(RUTA_TIENDA_MESA))
        # Es raro que PointingHandCursor no este disponible en Designer...
        self.button_exit.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_time.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(STYLE_SHEET_VENTANA_JUEGO)


    def start(self):
        '''Inicia el juego'''
        # TODO: iniciar backend con señales para no iniciarlo en main
        self.show()

    def keyPressEvent(self, event):
        self.signal_keypress.emit(event.text())

    def move_object(self, obj: dict):
        print(obj)  # TODO: remove
        self.game_objects[obj['id']].raise_()
        self.game_objects[obj['id']].move(*obj['pos'])

    def add_new_object(self, obj: dict):
        '''`obj`: dict con id e información del objeto'''
        new_object = QLabel(self.game_area)
        new_object.setGeometry(*obj['pos'], *obj['size'])
        new_object.setPixmap(QPixmap(obj['sprite_path']))
        new_object.setScaledContents(True)
        self.game_objects[obj['id']] = new_object

    def make_map(self, width: int = 800, height: int = 400, cell_size: int = 20):
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
                decoration.setPixmap(QPixmap(RUTA_DEC_2))
                decoration.setFixedSize(cell_size * 2, cell_size * 4)
            else:
                decoration.setPixmap(QPixmap(RUTA_DEC_1))
                decoration.setFixedSize(cell_size * 2, cell_size * 4)
            decoration.setScaledContents(True)
            area_grid.addWidget(decoration, 0, x_pos, 1, 2)

        # Se crean las celdas y se añaden al grid del juego
        for x_pos in range(grid_width):
            for y_pos in range(grid_height):
                cell = QLabel(self.game_area)
                cell.setFixedSize(cell_size, cell_size)
                cell.setPixmap(QPixmap(RUTA_CELDA))
                cell.setScaledContents(True)
                area_grid.addWidget(cell, y_pos + 1, x_pos, 1, 1)
