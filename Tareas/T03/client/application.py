'''Módulo encargado de la aplicación'''

import sys
from os import path

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPixmap

from frontend.windows import InitialWindow, GameWindow
from backend.client import Client


class Application(QApplication):
    'Aplicación del Cliente'
    def __init__(self, paths, **kwargs):
        sys.__excepthook__ = lambda t, v, trace: print(t, v, trace, sep="\n")
        super().__init__(sys.argv)

        # Crea las ventanas
        self.initial_window = InitialWindow(QPixmap(path.join(*paths['logo'])))
        self.game_window = GameWindow(path.join(*paths['ui']))

        # Establece el estilo de la aplicación
        with open(path.join(*paths['theme'])) as theme_file:
            self.setStyleSheet(theme_file.read())

        # Crea el cliente
        self.client = Client(kwargs['host'], kwargs['port'])

        # Conecta las señales
        self.initial_window.signal_join.connect(self._join)

        self.client.signal_response.connect(self._manage_response)
        self.client.signal_connection_error.connect(self.error)

        self.game_window.signal_chat.connect(self._send_chat)
        self.game_window.signal_play.connect(self._play_card)
        self.game_window.signal_call.connect(self._call_uno)

    def run(self):
        'Corre la aplicación'
        if self.client.connect():
            self.initial_window.show()
            sys.exit(self.exec_())
        else:
            self.error('No ser ha podido conectar con el servidor')

    def error(self, info: str):
        'Maneja un error de conexión'
        error_box = QMessageBox(QMessageBox.Critical, 'Error', info)
        error_box.raise_()  #?
        error_box.exec()
        self.closeAllWindows()

    def _manage_response(self, response: dict):
        print('manejando respuesta del servidor')
        if   response[0] == 'join failed':
            self.initial_window.state_joining_failed(response[16])
        elif response[0] == 'players':
            self.initial_window.action_waiting(response[8])
        elif response[0] == 'setup':
            self.initial_window.close()
            self.game_window.set_reverse_card(response[24])
            self.game_window.setup_players(response[17])
            self.game_window.show()
        elif response[0] == 'add_player_card':
            self.game_window.add_player_card(
                c_color=response[1],
                c_type=response[2],
                c_pixmap=response[3]
            )
        elif response[0] == 'add_opponent_card':
            self.game_window.add_opponent_card(response[4])
        elif response[0] == 'update_pool':
            self.game_window.update_pool(
                c_color=response[1],
                c_type=response[2],
                c_pixmap=response[3],
                active_player=response[4]
            )
        elif response[0] == 'remove_card':
            self.game_window.remove_card(response[4], int(response[5]))
        elif response[0] == 'chat':
            self.game_window.add_chat_mesaje(response[6])

    def _join(self, name: str):
        'Manda al servidor la solicitud para unirse'
        self.client.send({
            0: 'join',
            4: name
        })

    def _send_chat(self, mesaje: str):
        'Manda un mensaje al chat'
        self.client.send({
            0: 'chat',
            6: mesaje
        })

    def _play_card(self, index: int):
        'El jugador juega una carta'
        self.client.send({
            0: 'play_card',
            5: str(index)
        })

    def _call_uno(self):
        'El jugador llamó UNO'
        self.client.send({
            0: 'uno'
        })
