'''Servidor'''

from json import load

from server import Server
# from game import Game

# TODO

with open('parametros.json', encoding='utf-8') as file:
    PARAMETERS = load(file)

SERVER = Server(PARAMETERS['host'], PARAMETERS['port'])
# GAME = Game(**PARAMETERS)

SERVER.run()
# GAME.start()

# Este ciclo puede estar integrado en la clase Server
while True:
    pass
