'''
Simulador del DCCafé
'''

import sys

from PyQt5.QtWidgets import QApplication

from backend.game_core import GameCore
from backend.game_objects import GameObject
from frontend.windows.game import GameWindow
from frontend.windows.initial import InitialWindow
from frontend.windows.summary import SummaryWindow  # TODO

if __name__ == "__main__":
    sys.__excepthook__ = lambda t, v, trace: print(t, v, trace, sep="\n")
    APP = QApplication(sys.argv)
    ################################

    INITIAL_WINDOW = InitialWindow()
    GAME_WINDOW = GameWindow()
    FINAL_WINDOW = SummaryWindow()

    GAME_CORE = GameCore()

    # Señales de la ventana inicial
    INITIAL_WINDOW.signal_new.connect(GAME_CORE.new_game)
    INITIAL_WINDOW.signal_load.connect(GAME_CORE.load_game)

    # Señales de los objetos en el interfaz
    GAME_CORE.signal_add_new_object.connect(GAME_WINDOW.add_new_object)
    GAME_CORE.signal_update_object.connect(GAME_WINDOW.update_object)
    GAME_CORE.signal_delete_object.connect(GAME_WINDOW.delete_object)
    GAME_CORE.signal_stack_under.connect(GAME_WINDOW.stack_under)
    GAME_CORE.signal_move_up.connect(GAME_WINDOW.move_up)

    # Señales de control del interfaz y sus datos
    GAME_CORE.signal_start_game_window.connect(GAME_WINDOW.start)
    GAME_CORE.signal_update_cafe_stats.connect(GAME_WINDOW.update_cafe_stats)

    # Señales de teclas
    GAME_WINDOW.signal_key_press.connect(GAME_CORE.add_key)
    GAME_WINDOW.signal_key_relase.connect(GAME_CORE.remove_key)

    # Señales de pausa y resumir juego
    GAME_WINDOW.signal_pause_continue.connect(GAME_CORE.pause_continue_game)
    GAME_CORE.signal_show_paused.connect(GAME_WINDOW.paused_ui)

    # Señal para abrir la ventana final
    GAME_CORE.signal_show_end_screen.connect(FINAL_WINDOW.show_results)

    # Señales de la ventana final
    FINAL_WINDOW.signal_continue_game.connect(GAME_CORE.continue_game)
    FINAL_WINDOW.signal_exit_game.connect(GAME_CORE.exit_game)
    FINAL_WINDOW.signal_save_game.connect(GAME_CORE.save_game)

    ################################
    INITIAL_WINDOW.show()
    FINAL_WINDOW.show()
    sys.exit(APP.exec_())
