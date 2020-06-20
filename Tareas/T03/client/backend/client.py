'''Módulo que posee la Client que administra la coneción con el servidor'''

import socket
import threading
import json

from PyQt5.QtCore import QObject, pyqtSignal

class Client(QObject):
    '''Cliente del servidor'''
    signal_update = pyqtSignal(dict)

    def __init__(self, host, port, **kwargs):
        super().__init__()
        # Creación del socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Se conecta al servidor
        try:
            self.socket.connect((host, port))
            # Se empieza a escuchar al servidor
            thread = threading.Thread(target=self.listen, daemon=True)
            self.connected = True
            thread.start()
        except ConnectionError:
            print('Error al iniciar la coneción')
    
    def listen(self):
        try:
            print('escuchando servidor')
            while self.connected:
                pass
        except ConnectionError:
            print('error al escuchar servidor')


if __name__ == "__main__":
    with open('client\\parametros.json', encoding='utf-8') as file:
        LOADED_DATA = json.load(file)
    CLIENT = Client(**LOADED_DATA)