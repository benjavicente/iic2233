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
                if not data:
                    raise ConnectionError
                log_from = self.clients_names[id_] if id_ in self.clients_names else id_
                self.log('datos recibidos', log_from, f'Acción a realizar: {data[0]}')
                self.manage_response(id_, data)
        except ConnectionError:
            self.log('Error de conexión', id_)
        finally:
            # Se elimina el cliente
            with self.lock_edit_client:
                del self.clients[id_]
                if id_ in self.clients_names:
                    self.game.remove_player(self.clients_names[id_])
                    del self.clients_names[id_]
            if not self.game.started:
                self.send_all({
                    0: 'players',
                    8: self.game.get_player_names()
                })
            client_socket.close()

    def send(self, id_: int, data: dict):
        'Manda el diccionario data al socket'
        client_socket = self.clients[id_]
        send_data(client_socket, data)
        log_from = self.clients_names[id_] if id_ in self.clients_names else id_
        self.log('se mandó información', log_from, data[0])

    def send_all(self, data: dict):
        '''
        Manda un json serializado a todos los jugadores
        que posean un nombre
        '''
        with self.lock_edit_client:
            for id_ in self.clients:
                if id_ in self.clients_names:
                    self.send(id_, data)

    def setup_game(self):
        'Actualiza la información del juego a todos los clientes'
        self.log('Actualizando juego')
        for id_, name in self.clients_names.items():
            game_data = self.game.set_up_names(name)
            data = {
                0: 'setup',
                17: game_data,
                24: self.get_card_pixmap(('reverso', ''))
            }
            self.send(id_, data)
        for owner_id, card in self.game.cards_to_add():
            for id_ in self.clients_names:
                if owner_id == id_:
                    data = {
                        0: 'add_player_card',
                        1: card[0],
                        2: card[1],
                        3: self.get_card_pixmap(card)
                    }
                    self.send(id_, data)
                else:
                    pass # Entregar carta dada vuelta

    def update_cards(self):
        'Actualiza las cartas'
        pass

    def get_card_pixmap(self, card):
        'Obtiene el pixmap de la carta'
        card_type = '_'.join([n for n in filter(None, card)])
        with open(path.join('sprites', self.game.theme, card_type + '.png'), 'rb') as file:
            return file.read()

    def manage_response(self, id_: int, data: dict):
        'Maneja la respuesta del socket'

        # El jugador trata de unirse
        if data[0] == 'join':
            name = data[4]
            # El jugador trató de unirse con el el juego en desarrollo
            if self.game.started:
                self.send(id_, {
                    0: 'join failed',
                    16: {
                        'why': 'game already started',
                        'display': f'El juego ya empezó'
                    }
                })
            # El jugador se une con un nombre ya existente
            elif not self.game.valid_name(name):
                self.send(id_, {
                    0: 'join failed',
                    16: {
                        'why': 'invalid name',
                        'display': f'El nombre {name} no es válido'
                    }
                })
            # En jugador pudo ingresar
            else:
                # Se guarda el nombre del jugador
                self.game.add_player(name, id_)
                with self.lock_edit_client:
                    self.clients_names[id_] = name
                self.log('nombre establecido', id_, f'Nuevo nombre: {name}')
                # Se envían los jugadores a los unidos
                self.send_all({
                    0: 'players',
                    8: self.game.get_player_names()
                })
                if self.game.started:
                    self.setup_game()

        # El jugador trata de mandar un chat
        elif data[0] == 'chat':
            name = self.clients_names[id_]
            formated_mesaje = f'{name}: {data[6]}'
            self.send_all({
                0: 'chat',
                6: formated_mesaje
            })

        # El jugador trata de robar
        elif data[0] == 'draw_card':
            pass

        # El jugador trata de jugar una carta
        elif data[0] == 'play_card':
            pass
