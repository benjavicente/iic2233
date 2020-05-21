from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap



class VentanaJuego(*uic.loadUiType('frontend/data/juego.ui')):  # TODO: path relativo
    '''Ventana del juego'''
    signal_keypress = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.game_objects = dict()
        self.game_map.setStyleSheet('background-color:grey')

    def start(self):
        # TODO: iniciar backend con señales para no iniciarlo en main
        self.show()

    def keyPressEvent(self, event):
        self.signal_keypress.emit(event.text())

    def move_object(self, obj: dict):
       self.game_objects[obj['id']].move(*obj['pos'])

    def add_new_object(self, obj: dict):
        '''`obj`: dict con id e información del objeto'''
        new_object = QLabel(self.game_map)
        new_object.setGeometry(*obj['pos'], *obj['size'])
        new_object.setPixmap(QPixmap(obj['sprite_path']))
        new_object.setScaledContents(True)
        new_object.setStyleSheet('background-color:red')  # TODO: eliminar
        self.game_objects[obj['id']] = new_object
