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
        # Datos del servidor
        self.host = host
        self.port = port
        self.connected = False

    def connect(self):
        '''Se conecta al servidor'''
        try:
            self.socket.connect((self.host, self.port))
            # Se empieza a escuchar al servidor
            thread = threading.Thread(target=self.listen, daemon=True)
            self.connected = True
            thread.start()
        except ConnectionError:
            print('Error al iniciar la coneción')

    def listen(self):
        '''Escucha activamente a un socket del servidor'''
        l_socket = self.socket
        try:
            while self.connected: # Parte igual server.py
                data = dict()
                n_obj = l_socket.recv(2)
                n_obj = int.from_bytes(n_obj, byteorder='big')
                for _ in range(n_obj):
                    # Tipo
                    object_id = l_socket.recv(4)
                    object_id = int.from_bytes(object_id, byteorder='big')
                    # Largo
                    object_size = l_socket.recv(4)
                    object_size = int.from_bytes(object_size, byteorder='big')
                    # Objeto serializado
                    content = bytearray()
                    reamining_size = object_size
                    chunk_size = 128
                    while reamining_size > 0:
                        chunk = min(reamining_size, chunk_size)
                        content += l_socket.recv(chunk)
                        reamining_size -= chunk_size
                    # Transformación de objetos
                    if object_id in {0, 1, 2}:  # Esto es un string
                        content = content.decode('utf-8')
                    # Se guarda en un diccionario
                    data[object_id] = content
                # Se toman las acciones necesarias
                # TODO

        except ConnectionError:
            print(f'Error en la coneción')
            #* Aquí puede mandarse una señal a la ventana
        finally:
            self.socket.close()

    def send(self, data):
        '''Manda información al servidor'''
        # Igual a send de server
        if not isinstance(data, dict):
            raise TypeError("'data' no es un diccionario")
        serialized_data = bytearray()
        serialized_data += len(data).to_bytes(2, 'big')
        for id_, obj in data.items():
            serialized_data += id_.to_bytes(4, 'big')
            # Serialización de objectos
            if isinstance(obj, str):
                b_obj = obj.encode('utf-8')
            # Tamaño de objetos
            serialized_data += len(b_obj).to_bytes(4, 'big')
            # Envío de objeto
            serialized_data += b_obj
        self.socket.send(serialized_data)
        print(f'el cliente ha enviado información ({data[0]})')


if __name__ == "__main__":
    import time
    with open('client\\parametros.json', encoding='utf-8') as file:
        LOADED_DATA = json.load(file)
    CLIENT = Client(**LOADED_DATA)
    while True:  # Este ciclo debe estar integrado con QApplication
        time.sleep(60)