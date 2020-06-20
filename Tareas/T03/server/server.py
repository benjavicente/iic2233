'''Módulo que posee la clase que administra el servidor'''

import socket
import threading
import json

from log import Log


class Server:
    '''El servidor del juego'''
    def __init__(self, host, port, **kwargs):
        # Creación del socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
        # Crea un Log
        self.log = Log()
        # Crea un diccionario para almacenar jugadores
        self.players = dict()
        # Empieza a aceptar conesciones


    def __del__(self):
        '''Cierra el socket al eliminar el objeto de la memoria'''
        self.socket.close()
        self.log.add('saliendo')

    def listen(self):
        while True:
            client, (ip, direc) = self.socket.accept()

    def send_all(self):
        pass


if __name__ == "__main__":
    with open('parametros.json', encoding='utf-8') as file:
        LOADED_DATA = json.load(file)
    SERVER = Server(**LOADED_DATA)
