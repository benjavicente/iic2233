'''Módulo que posee la clase Server que administra el servidor'''

import socket
import threading
import json
import pickle

from log import Log
from protocol import recv_data, send_data

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
        thread = threading.Thread(target=self.listen_new, daemon=True)
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
            #* Por lo que tengo entendido, direc es garantizado
            #* de ser único en una red local (puedo probar con el ip también)
            self.players[direc] = {
                'socket': client
            }
            thread = threading.Thread(
                target=self.listen_active,
                daemon=True, args=(client, direc)
            )
            self._update_players()
            thread.start()

    def listen_active(self, client_socket, id_: int = 0):
        '''Escucha activamente a un socket dl servidor'''
        l_socket = client_socket
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

    def _update_players(self):
        '''Actualiza la información de los jugadores en tódos los clientes'''
        pass


if __name__ == "__main__":
    import time
    with open('parametros.json', encoding='utf-8') as file:
        LOADED_DATA = json.load(file)
    SERVER = Server(**LOADED_DATA)
    while True:  # Este ciclo debe estar integrado con QApplication
        time.sleep(60)