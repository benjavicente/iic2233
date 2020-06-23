'''Módulo que posee la Client que administra la coneción con el servidor'''

from socket import socket as Socket, AF_INET as IPv4, SOCK_STREAM as TCP
from threading import Thread

from PyQt5.QtCore import QObject, pyqtSignal

from backend.protocol import recv_data, send_data  # Tira error en el lint...



class Client(QObject):
    'Cliente del servidor'
    signal_response = pyqtSignal(dict)

    def __init__(self, host, port):
        super().__init__()
        # Creación del socket
        self.socket = Socket(IPv4, TCP)
        # Datos del servidor
        self.host = host
        self.port = port

    def connect(self):
        'Se conecta al servidor'
        try:
            self.socket.connect((self.host, self.port))
            # Se empieza a escuchar al servidor
            thread = Thread(target=self.listen, daemon=True)
            thread.start()
        except ConnectionError:
            print('Error al iniciar la coneción')

    def listen(self):
        'Escucha activamente a un socket del servidor'
        try:
            while True:
                print('esperando datos')
                data = recv_data(self.socket)
                print(f'recibiendo {data[0]}')
                self.signal_response.emit(data)
        except ConnectionError:
            print(f'Error en la coneción')
            #* Aquí puede mandarse una señal a la ventana
        finally:
            self.socket.close()

    def send(self, data):
        'Manda el diccionario al servidor siguiendo el protocolo establecido'
        send_data(self.socket, data)
        print(f'el cliente ha enviado información ({data[0]})')
