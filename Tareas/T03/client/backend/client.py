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
        '''Escucha activamente a un socket del servidor'''
        try:
            while self.connected:
                info = dict()
                for _ in range(3):
                    # Tipo
                    object_id = self.socket.recv(4)
                    object_id = int.from_bytes(object_id, byteorder='big')
                    # Largo
                    object_size = self.socket.recv(4)
                    object_size = int.from_bytes(object_size, byteorder='big')
                    # Objeto serializado
                    content = bytearray()
                    reamining_size = object_size
                    chunk_size = 128
                    while reamining_size:
                        chunk = min(reamining_size, chunk_size)
                        content += self.socket.recv(chunk)
                        reamining_size -= chunk_size
                    # Se guarda la información
                    #* Todavía no hay un procedimiento de
                    #* deserializasión de strings o imágenes
                    info[object_id] = content
            #* do something
        except ConnectionError:
            print(f'Error en la coneción')
        finally:
            self.socket.close()


if __name__ == "__main__":
    with open('client\\parametros.json', encoding='utf-8') as file:
        LOADED_DATA = json.load(file)
    CLIENT = Client(**LOADED_DATA)
    input('enter para cerrar\n')  # Este ciclo debe estar integrado con QApplication
