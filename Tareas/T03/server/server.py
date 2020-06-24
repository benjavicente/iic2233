'Módulo que posee la clase Server que administra el servidor'

from socket import socket as Socket, AF_INET as IPv4, SOCK_STREAM as TCP
from threading import Thread, Lock
from os import path

from log import Log
from protocol import recv_data, send_data
from game import Game

# TODO: revisar si se necesitan locks

class Server:
    'El servidor del juego'
    lock_edit_client = Lock()

    def __init__(self, host, port, **kwargs):
        self.host = host
        self.port = port
        # Se crea un socket
        self.socket = Socket(IPv4, TCP)
        # Se crea un Log
        self.log = Log()
        # Se crea un diccionario para almacenar los sockets
        self.clients = dict()
        self.clients_names = dict()
        # Entidad que maneja el juego
        self.game = Game(**kwargs)

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
        while True:
            self.log('esperando conexión')
            #* Se podria hacer un hash con el ip y la dirección del socket
            client, (_, direc) = self.socket.accept()  # ip, direc
            self.log('conectado con cliente', details=f'id del cliente: {direc}')
            with self.lock_edit_client:
                self.clients[direc] = client
            thread = Thread(target=self.listen_active, daemon=True, args=(client, direc))
            thread.start()

    def listen_active(self, client_socket, id_: int):
        'Escucha activamente a un socket dl servidor'
        try:
            while True:
                data = recv_data(client_socket)
                self.log('datos recibidos', id_, f'Acción a realizar: {data[0]}')
                log_from = self.clients_names[id_] if id_ in self.clients_names else id_
                self.manage_response(client_socket, log_from, data)
        except ConnectionError:
            self.log('Error de conexión', id_)
        finally:
            # Se elimina el cliente
            with self.lock_edit_client:
                self.game.remove_player(self.clients_names[id_])
                del self.clients[id_]
                del self.clients_names[id_]
            if not self.game.started:
                self.send_all({
                    0: 'players',
                    8: self.game.get_player_names()
                })
            client_socket.close()

    def send(self, client_socket, id_: int, data: dict):
        'Manda el diccionario data al socket'
        send_data(client_socket, data)
        log_from = self.clients_names[id_] if id_ in self.clients_names else id_
        self.log('se mandó información', log_from, data[0])

    def send_all(self, data: dict, exclude=None, with_name: bool = True):
        '''
        Manda un json serializado a todos los jugadores
        Puede excluirse a un jugador
        '''
        for id_, socket in self.clients.items():
            if (not (exclude and id_ == exclude)) and (with_name and id_ in self.clients_names):
                self.send(socket, id_, data)

    def setup_game(self):
        'Actualiza la información del juego a todos los clientes'
        self.log('Actualizando juego')
        for id_, name in self.clients_names.items():
            socket = self.clients[id_]
            game_data = self.game.set_up(name)
            data = {
                0: 'setup',
                17: game_data,
                24: self.get_card_pixmap('reverso')
            }
            self.send(socket, id_, data)

    def get_card_pixmap(self, card_type):
        'Obtiene el pixmap de la carta'
        # Esta parte tiene que estar en español
        if isinstance(card_type, tuple):
            card_type = '_'.join(card_type)
        with open(path.join('sprites', self.game.theme, card_type + '.png'), 'rb') as file:
            return file.read()

    def manage_response(self, socket, id_: int, data: dict):
        'Maneja la respuesta del socket'

        # El jugador trata de unirse
        if data[0] == 'join':
            name = data[4]
            # El jugador trató de unirse con el el juego en desarrollo
            if self.game.started:
                self.send(socket, id_, {
                    0: 'join failed',
                    16: {
                        'why': 'game already started',
                        'display': f'El juego ya empezó'
                    }
                })
            # El jugador se une con un nombre ya existente
            elif not self.game.valid_name(name):
                self.send(socket, id_, {
                    0: 'join failed',
                    16: {
                        'why': 'invalid name',
                        'display': f'El nombre {name} no es válido'
                    }
                })
            # En jugador pudo ingresar
            else:
                # Se guarda el nombre del jugador
                self.game.add_player(name)
                self.clients_names[id_] = name
                self.log('nombre establecido', id_, f'Nuevo nombre: {name}')
                # Se envían los jugadores a los unidos
                self.send_all({
                    0: 'players',
                    8: self.game.get_player_names()
                })
                if self.game.started:
                    self.setup_game()

        # El jugador trata de ...
