'''Módulo encargado de la aplicación'''

import sys
from os import path

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap

from frontend.windows import InitialWindow, GameWindow
from backend.client import Client


class Application(QApplication):
    'Aplicación del Cliente'
    def __init__(self, paths, **kwargs):
        sys.__excepthook__ = lambda t, v, trace: print(t, v, trace, sep="\n")
        super().__init__(sys.argv)

        # Pixelmaps #??
        self.logo = QPixmap(path.join(*paths['logo']))

        # Crea las ventanas
        self.initial_window = InitialWindow(self.logo)
        self.game_window = GameWindow(path.join(*paths['ui']))

        # Establece el estilo de la aplicación
        with open(path.join(*paths['theme'])) as theme_file:
            self.setStyleSheet(theme_file.read())
    
        # Crea el cliente
        self.client = Client(kwargs['host'], kwargs['port'])

        # Conecta las señales
        self.initial_window.signal_join.connect(self._join)

        self.client.signal_response.connect(self._manage_response)


    def run(self):
        'Corre la aplicación'
        self.initial_window.show()
        self.client.connect()
        sys.exit(self.exec_())

    def _manage_response(self, response: dict):
        print('manejando respuesta del servidor')
        if   response[0] == 'join failed':
            self.initial_window.state_joining_failed()
        elif response[0] == 'players':
            self.initial_window.action_waiting(response[8])


    def _join(self, name: str):
        'Manda al servidor la solicitud para unirse'
        self.client.send({
            0: 'join',
            4: name
        })


