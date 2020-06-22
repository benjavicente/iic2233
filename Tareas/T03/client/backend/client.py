'''Módulo que posee la Client que administra la coneción con el servidor'''

import socket
import threading

from PyQt5.QtCore import QObject, pyqtSignal

from backend.protocol import recv_data, send_data


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

    def connect(self):
        '''Se conecta al servidor'''
        try:
            self.socket.connect((self.host, self.port))
            # Se empieza a escuchar al servidor
            thread = threading.Thread(target=self.listen, daemon=True)
            thread.start()
        except ConnectionError:
            print('Error al iniciar la coneción')

    def listen(self):
        '''Escucha activamente a un socket del servidor'''
        try:
            while True:
                data = recv_data(self.socket)
                # TODO: do something
        except ConnectionError:
            print(f'Error en la coneción')
            #* Aquí puede mandarse una señal a la ventana
        finally:
            self.socket.close()

    def send(self, data):
        send_data(self.socket, data)
        print(f'el cliente ha enviado información ({data[0]})')


if __name__ == "__main__":
    import time
    with open('client\\parametros.json', encoding='utf-8') as file:
        LOADED_DATA = json.load(file)
    CLIENT = Client(**LOADED_DATA)
    while True:  # Este ciclo debe estar integrado con QApplication
        time.sleep(60)