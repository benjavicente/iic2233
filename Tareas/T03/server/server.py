'''Módulo que posee la clase Server que administra el servidor'''

import socket
import threading
import json

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
        thread = threading.Thread(target=self.listen_new, daemon=True)
        thread.start()

    def __del__(self):
        '''Cierra el socket al eliminar el objeto de la memoria'''
        self.socket.close()
        self.log('saliendo')

    def listen_new(self):
        '''Escucha nuevas conexiones'''
        while True:
            self.log('esperando conexión')
            client, (ip, direc) = self.socket.accept()
            self.log('se ha conectado', direc)
            #* Por lo que tengo entendido, direc es garantizado
            #* de ser único en una red local (puedo probar con el ip también)
            self.players[direc] = client
            thread = threading.Thread(
                target=self.listen_active,
                daemon=True, args=(client, direc)
            )
            thread.start()

    def listen_active(self, client_socket, id_: int = 0):
        '''Escucha activamente a un socket dl servidor'''
        try:
            while True:
                pass
                #* do something
        except ConnectionError:
            print(f'Error en la coneción del cliente {id_}')
        finally:
            client_socket.close()

    def send_all(self):
        pass


if __name__ == "__main__":
    with open('server\\parametros.json', encoding='utf-8') as file:
        LOADED_DATA = json.load(file)
    SERVER = Server(**LOADED_DATA)
    input('enter para cerrar\n')  # Este ciclo debe estar integrado con QApplication
