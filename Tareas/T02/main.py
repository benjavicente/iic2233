'''
Simulador del DCCafé
'''

import sys
from PyQt5.QtWidgets import QApplication

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_juego import VentanaJuego
from backend.jugador import GameObject
from backend.dccafe import DCCafe



if __name__ == "__main__":
    sys.__excepthook__ = lambda t, v, trace: print(t, v, trace, sep="\n")
    APP = QApplication(sys.argv)
    ################################

    VI = VentanaInicio()
    VJ = VentanaJuego()

    DCCAFE = DCCafe()
    DCCAFE.load_game() # TODO: cambiar esto

    VI.signal_start.connect(VJ.start)

    DCCAFE.signal_add_object.connect(VJ.add_new_object)
    DCCAFE.signal_update_pos.connect(VJ.move_object)

    VJ.signal_keypress.connect(DCCAFE.move_player)

    VI.show()

    ################################
    sys.exit(APP.exec_())



