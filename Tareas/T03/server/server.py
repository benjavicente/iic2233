'Módulo que posee la clase Server que administra el servidor'

from socket import socket as Socket, AF_INET as IPv4, SOCK_STREAM as TCP
from threading import Thread

from log import Log
from protocol import recv_data, send_data

class Server:
    'El servidor del juego'
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # Se crea un socket
        self.socket = Socket(IPv4, TCP)
        # Se crea un Log
        self.log = Log()
        # Se crea un diccionario para almacenar jugadores
        self.clients = dict()

    def run(self):
        'Corre el servidor'
        # Se abre el socket
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        # Se empieza a aceptar conesciones
        thread = Thread(target=self.listen_new, daemon=True)
        thread.start()

    def __del__(self):
        'Cierra el socket al eliminar el objeto de la memoria'
        self.socket.close()
        self.log('saliendo')

    def listen_new(self):
        'Escucha nuevas conexiones'
        while True:  #* Esta condición puede cambiar
            self.log('esperando conexión')
            client, (ip, direc) = self.socket.accept()
            self.log('conectado con cliente', details=f'id del cliente: {direc}')
            self.clients[direc] = {'socket': client}
            thread = Thread(target=self.listen_active, daemon=True, args=(client, direc))
            thread.start()

    def listen_active(self, client_socket, id_):
        'Escucha activamente a un socket dl servidor'
        try:
            while True:
                data = recv_data(client_socket)
                self.log('datos recibidos', id_, f'Acción a realizar: {data[0]}')
                self.manage_response(data, id_)
        except ConnectionError:
            self.log('Error de conexión', id_)
        finally:
            del self.clients[id_]
            client_socket.close()

    def send(self, client_socket, id_, data: dict):
        'Manda el diccionario data al socket'
        send_data(client_socket, data)
        self.log('Se mandó información', id_, data[0])

    def send_all(self, data, exclude=None, with_name=True):
        '''
        Manda un json serializado a todos los jugadores
        Puede excluirse a un jugador
        '''
        for id_, values in self.clients.items():
            if (not (exclude and id_ == exclude)) and (with_name and 'name' in values):
                self.send(values['socket'], id_, data)

    def manage_response(self, data, id_):
        'Maneja la respuesta del socket'
        if data[0] == 'join':
            for client_info in self.clients.values():
                if 'name' in client_info and client_info['name'] == data[4]:
                    self.send(self.clients[id_]['socket'], id_, {
                        0: 'join failed',
                        16: {
                            'why': 'name used by another player',
                            'display': f'El nombre {data[4]} ya está ocupado'
                        }
                    })
                    return  # Termina por error
            # Se guarda el nombre del jugador
            self.clients[id_]['name'] = data[4]
            self.log(data[0], id_, f'se ha unido {data[4]}')
            # Se envían los jugadores a los unidos
            self.send_all({
                0: 'players',
                8: [v['name'] for v in self.clients.values() if 'name' in v]
                # Falta agragr los espacios vacios al esperar jugadores
            })
            return


if __name__ == "__main__":
    import time
    import json
    with open('parametros.json', encoding='utf-8') as file:
        LOADED_DATA = json.load(file)
    SERVER = Server(LOADED_DATA['host'], LOADED_DATA['port'])
    while True:  # Este ciclo debe estar integrado con QApplication
        time.sleep(60)
