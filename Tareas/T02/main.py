'''
Simulador del DCCafé
'''

import sys
from PyQt5.QtWidgets import QApplication

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_juego import VentanaJuego


if __name__ == "__main__":
    sys.__excepthook__ = lambda t, v, trace: print(t, trace, sep="\n")
    APP = QApplication(sys.argv)
    ################################

    VI = VentanaInicio()
    VJ = VentanaJuego()

    VI.signal_start.connect(VJ.partir)
    VI.show()

    ################################
    sys.exit(APP.exec_())



