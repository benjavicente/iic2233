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

    def partir(self):
        # TODO: iniciar backend con señales
        self.show()

    def keyPressEvent(self, event):
        self.key_signal.emit(event.key())




if __name__ == "__main__":
    sys.__excepthook__ = lambda t, v, trace: print(t, trace, sep="\n")
    APP = QApplication(sys.argv)
    VENTANA = VentanaJuego()
    VENTANA.show()
    sys.exit(APP.exec_())
