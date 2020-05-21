'''
Simulador del DCCafé
'''

import sys
from PyQt5.QtWidgets import QApplication

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_juego import VentanaJuego
from backend.jugador import Jugador


if __name__ == "__main__":
    sys.__excepthook__ = lambda t, v, trace: print(t, trace, sep="\n")
    APP = QApplication(sys.argv)
    ################################

    VI = VentanaInicio()
    VJ = VentanaJuego()
    JUGADOR = Jugador()

    VI.signal_start.connect(VJ.partir)

    VJ.signal_keypress.connect(JUGADOR.mover)
    JUGADOR.signal_update_pos.connect(VJ.mover_jugador)

    VI.show()

    ################################
    sys.exit(APP.exec_())



