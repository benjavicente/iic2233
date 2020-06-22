'''Módulo que posee la clase Server que administra el servidor'''

from socket import socket as Socket, AF_INET as IPv4, SOCK_STREAM as TCP
from threading import Thread

from log import Log
from protocol import recv_data, send_data

class Server:
    '''El servidor del juego'''
    def __init__(self, host, port):
        # Se crea un socket
        self.socket = Socket(IPv4, TCP)
        # Se abre el socket
        self.socket.bind((host, port))
        self.socket.listen()
        # Se crea un Log
        self.log = Log()
        # Se crea un diccionario para almacenar jugadores
        self.players = dict()
        # Se empieza a aceptar conesciones
        thread = Thread(target=self.listen_new, daemon=True)
        thread.start()

    def __del__(self):
        '''Cierra el socket al eliminar el objeto de la memoria'''
        self.socket.close()
        self.log('saliendo')

    def listen_new(self):
        '''Escucha nuevas conexiones'''
        while True:  #* Esta condición puede cambiar
            self.log('esperando conexión')
            client, (ip, direc) = self.socket.accept()
            self.log('conectado con cliente', details=f'id del cliente: {direc}')
            self.players[direc] = {'socket': client}
            thread = Thread(target=self.listen_active, daemon=True, args=(client, direc))
            thread.start()

    def listen_active(self, client_socket, id_: int = 0):
        '''Escucha activamente a un socket dl servidor'''
        try:
            while True:  # Parte igual client.py
                data = recv_data(client_socket)
                self.log('datos recibidos', id_, f'Acción a realizar: {data[0]}')
                # Se toman las acciones necesarias
                if data[0] == 'joining':
                    self.players[id_]['name'] = data[4]
                    self.log(data[4], id_, f'se ha unido {data[4]}')

        except ConnectionError:
            print(f'Error en la coneción del cliente {id_}')
        finally:
            client_socket.close()

    def send(self, client_socket, data: dict, id_=''):
        '''Manda el diccionario data al socket'''
        send_data(client_socket, data)
        self.log('Se mandó información', id_, data[0])

    def send_all(self, data, exclude=None):
        '''
        Manda un json serializado a todos los jugadores
        Puede excluirse a un jugador
        '''
        for id_, client_socket in self.players.values():
            if exclude and id_ != exclude:
                self.send(client_socket, data, id_)


if __name__ == "__main__":
    import time
    import json
    with open('parametros.json', encoding='utf-8') as file:
        LOADED_DATA = json.load(file)
    SERVER = Server(**LOADED_DATA)
    while True:  # Este ciclo debe estar integrado con QApplication
        time.sleep(60)
