import json

from backend.client import Client
from frontend.windows import Game


with open('parametros.json') as file:
    data = json.load(file)

GAME = Game(data['paths'])
CLIENT = Client(data['host'], data['port'])

GAME.initial_window.signal_join.connect(CLIENT.send)

GAME.run()
