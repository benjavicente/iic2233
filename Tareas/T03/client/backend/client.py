'''Módulo que posee la Client que administra la coneción con el servidor'''

from socket import socket as Socket, AF_INET as IPv4, SOCK_STREAM as TCP
from threading import Thread

from PyQt5.QtCore import QObject, pyqtSignal

from backend.protocol import recv_data, send_data  # Tira error en el lint...



class Client(QObject):
    'Cliente del servidor'
    signal_response = pyqtSignal(dict)
    signal_connection_error = pyqtSignal(str)

    def __init__(self, host, port):
        super().__init__()
        # Creación del socket
        self.socket = Socket(IPv4, TCP)
        # Datos del servidor
        self.host = host
        self.port = port

    def connect(self):
        'Se conecta al servidor (Al iniciar el programa)'
        try:
            self.socket.connect((self.host, self.port))
            # Se empieza a escuchar al servidor
            thread = Thread(target=self.listen, daemon=True)
            thread.start()
            return True
        except ConnectionError:
            return False

    def listen(self):
        'Escucha activamente a un socket del servidor'
        try:
            while True:
                data = recv_data(self.socket)
                print(f'recibiendo {data[0]}')
                self.signal_response.emit(data)
        except ConnectionError:
            self.signal_connection_error.emit('Se ha desconectado el servidor')
        finally:
            self.socket.close()

    def send(self, data):
        'Manda el diccionario al servidor siguiendo el protocolo establecido'
        try:
            send_data(self.socket, data)
            print(f'el cliente ha enviado información ({data[0]})')
        except ConnectionError:
            self.signal_connection_error.emit()
