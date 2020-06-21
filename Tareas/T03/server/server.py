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
                data = dict()
                self.log('esperando datos', id_)
                n_obj = l_socket.recv(2)
                n_obj = int.from_bytes(n_obj, byteorder='big')
                self.log('recibiendo datos', id_, f'cantidad de objectos: {n_obj}')
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
                    if object_id in {0, 1}:  # strings
                        content = content.decode('utf-8')
                    # Se guarda en un diccionario
                    data[object_id] = content
                self.log('datos recibidos', id_, f'Acción a realizar: {data[0]}')

                # Se toman las acciones necesarias
                if data[0] == 'joining':
                    self.players[id_]['name'] = data[1]
                    self.log(data[0], id_, f'se ha unido {data[1]}')

    
        except ConnectionError:
            print(f'Error en la coneción del cliente {id_}')
        finally:
            client_socket.close()

    def send(self, data: dict, client_socket):
        '''Manda el diccionario data al socket'''
        #> Igual a send de client
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

    def send_all(self, data, exclude=None):
        '''
        Manda un json serializado a todos los jugadores
        Puede excluirse a un jugador
        '''
        for id_, client_socket in self.players.values():
            if exclude and id_ != exclude:
                self.send(data, client_socket)

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