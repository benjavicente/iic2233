'Jugador de DCCuadrádo'

import json

from application import Application

with open('parametros.json') as file:
    CONFIG = json.load(file)

GAME_APP = Application(**CONFIG)

GAME_APP.run()
