'''Módulo que posee la clase Server que administra el servidor'''

import socket
import threading
import json

from os import getcwd, path

from log import Log


class Server:
    '''El servidor del juego'''
    def __init__(self, host, port, **kwargs):
        # Se crea un socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Se abre el socket
        self.socket.bind((host, port))
        self.socket.listen()
        # Se crea un Log
        self.log = Log()
        # Se crea un diccionario para almacenar jugadores
        self.players = dict()
        # Se empieza a aceptar conesciones
        thread = threading.Thread(target=self.listen, daemon=True)
        thread.start()

    def __del__(self):
        '''Cierra el socket al eliminar el objeto de la memoria'''
        self.socket.close()
        self.log('saliendo')

    def listen(self):
        '''Escucha nuevas conexiones'''
        while True:
            client, (ip, direc) = self.socket.accept()
            self.log('se ha conectado', direc)

    def send_all(self):
        pass


if __name__ == "__main__":
    with open('server\\parametros.json', encoding='utf-8') as file:
        LOADED_DATA = json.load(file)
    SERVER = Server(**LOADED_DATA)
    while True:
        pass  # Este ciclo debe estar integrado con QApplication
