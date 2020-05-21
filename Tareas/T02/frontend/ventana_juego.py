from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel



class VentanaJuego(*uic.loadUiType('frontend/data/juego.ui')):  # TODO: path relativo
    '''Ventana del juego'''
    signal_keypress = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.player = list()
        self.chefs = list()
        self.tables = list()

    def start(self):
        # TODO: iniciar backend con señales
        self.show()

    def keyPressEvent(self, event):
        self.signal_keypress.emit(event.text())

    def move_object(self, data: dict):
        print(data)
        getattr(self, data['object'])[data['id']].move(*data['pos'])

    def add_object(self, data: dict):
        # TODO: cambiar a Pixmap y mamaño
        print(object_type, 'añadido')
        new_object = QLabel(self)
        new_object.setStyleSheet('background-color:red')
        object_type = data['object']
        obj_names = {'mesero': 'players', 'chef': 'chefs', 'mesa': 'tables'}
        if object_type in obj_names:
            object_type = obj_names[object_type]
        getattr(self, object_type).append(new_object)




if __name__ == "__main__":
    sys.__excepthook__ = lambda t, v, trace: print(t, trace, sep="\n")
    APP = QApplication(sys.argv)
    VENTANA = VentanaJuego()
    VENTANA.show()
    sys.exit(APP.exec_())
