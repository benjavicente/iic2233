'''
Simulador del DCCafé
'''

import sys

from PyQt5.QtWidgets import QApplication

from backend.game_core import GameCore
from backend.game_objects import GameObject
from frontend.windows.game import GameWindow
from frontend.windows.initial import InitialWindow
# from frontend.windows.summary import SummaryWindow  # TODO

if __name__ == "__main__":
    sys.__excepthook__ = lambda t, v, trace: print(t, v, trace, sep="\n")
    APP = QApplication(sys.argv)
    ################################

    INITIAL_WINDOW = InitialWindow()
    GAME_WINDOW = GameWindow()

    GAME_CORE = GameCore()

    INITIAL_WINDOW.signal_new.connect(GAME_CORE._new_game)
    INITIAL_WINDOW.signal_load.connect(GAME_CORE._load_game)

    GAME_CORE.signal_add_new_object.connect(GAME_WINDOW.add_new_object)
    GAME_CORE.signal_update_object.connect(GAME_WINDOW.update_object)
    GAME_CORE.signal_delete_object.connect(GAME_WINDOW.delete_object)

    GAME_CORE.signal_start_game_window.connect(GAME_WINDOW.start)
    GAME_CORE.signal_update_cafe_stats.connect(GAME_WINDOW.update_cafe_stats)

    GAME_WINDOW.signal_key_press.connect(GAME_CORE.add_key)
    GAME_WINDOW.signal_key_relase.connect(GAME_CORE.remove_key)

    GAME_WINDOW.signal_pause_game.connect(GAME_CORE.pause_game)
    GAME_WINDOW.signal_continue_game.connect(GAME_CORE.continue_game)



    INITIAL_WINDOW.show()

    ################################
    sys.exit(APP.exec_())
