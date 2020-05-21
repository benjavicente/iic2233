from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication
import sys


name, base_class = uic.loadUiType('frontend/datos/juego.ui')


class VentanaJuego(name, base_class):
    '''Ventana del juego'''
    signal_keypress = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        print('stop')

    def partir(self):
        # TODO: iniciar backend con señales
        self.show()

    def keyPressEvent(self, event):
        self.signal_keypress.emit(event.text())

    def mover_jugador(self, pos):
        self.player1.move(*pos)



if __name__ == "__main__":
    sys.__excepthook__ = lambda t, v, trace: print(t, trace, sep="\n")
    APP = QApplication(sys.argv)
    VENTANA = VentanaJuego()
    VENTANA.show()
    sys.exit(APP.exec_())
