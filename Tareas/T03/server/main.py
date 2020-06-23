'''Servidor'''

from json import load

from server import Server
# from game import Game

# TODO: Tengo que empezar a implementar una clase que administra el flujo del juego

with open('parametros.json', encoding='utf-8') as file:
    PARAMETERS = load(file)

SERVER = Server(PARAMETERS['host'], PARAMETERS['port'])
# GAME = Game(**PARAMETERS)

SERVER.run()
# GAME.start()

# Este ciclo puede estar integrado en la clase Server
while True:
    pass
