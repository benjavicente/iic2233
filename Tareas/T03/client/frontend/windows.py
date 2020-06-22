'''Ventanas del juego'''

import sys
from os import path

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QVBoxLayout, QWidget)
from PyQt5.uic import loadUi


class Game(QApplication):
    '''Clase que conecta las ventanas del juego'''
    def __init__(self, paths):
        sys.__excepthook__ = lambda t, v, trace: print(t, v, trace, sep="\n")
        super().__init__(sys.argv)
        # Pixelmaps
        self.logo = QPixmap(path.join(*paths['logo']))
        # Paths
        ui_path = path.join(*paths['ui'])
        # Crea las ventanas
        self.initial_window = InitialWindow(self.logo)
        self.game_window = GameWindow(ui_path)
        # Aplica el estilo a las ventanas
        with open(path.join(*paths['theme'])) as theme_file:
            theme = theme_file.read()
        self.setStyleSheet(theme)

    def run(self):
        '''Core el juego'''
        self.initial_window.show()
        sys.exit(self.exec_())



class InitialWindow(QMainWindow):
    '''Ventana que se muestra al iniciar el programa'''

    signal_join = pyqtSignal(dict)

    def __init__(self, pix_logo):
        super().__init__()
        self.setObjectName(type(self).__name__)
        self.setWindowTitle('Ventana Inicial')
        self.pix_logo = pix_logo
        self._set_up()

    def _set_up(self):
        '''Agrega los elementos gráficos a la ventana'''
        main = QWidget()
        self.setCentralWidget(main)
        layout = QVBoxLayout()
        main.setLayout(layout)

        #--> Ventana Inicial
        # Logo
        height = 300
        self.logo = QLabel(main)
        self.logo.setFixedHeight(height)
        self.logo.setPixmap(self.pix_logo.scaledToHeight(height))
        layout.addWidget(self.logo, alignment=Qt.AlignCenter)
        # Añade el campo de nombre
        self.name_entry = QWidget()
        entry_layout = QHBoxLayout()
        self.name_entry.setLayout(entry_layout)
        layout.addWidget(self.name_entry)
        # Nombre
        self.name = QLineEdit(self.name_entry)
        self.name.setPlaceholderText('Ingresa un nombre')
        self.name.setObjectName('name')
        entry_layout.addWidget(self.name)
        # Botón para unirse
        self.join = QPushButton(self.name_entry)
        self.join.setText('Entrar')
        self.join.setObjectName('JoinButton')
        self.join.clicked.connect(self.action_joining)
        entry_layout.addWidget(self.join)

        #--> Sala de espera
        # Etiqueta
        self.wait_label = QLabel('Jugadores conectados')
        self.wait_label.setObjectName('WaitLabel')
        layout.addWidget(self.wait_label)
        self.wait_label.hide()  # Se oculta hasta que sea necesario
        # Cuadro de jugadores en espera
        self.players_frame = QWidget(self)
        layout.addWidget(self.players_frame)
        self.players_frame.hide()
        self.players_layout = QVBoxLayout()
        self.players_frame.setLayout(self.players_layout)

    def action_joining(self):
        '''Acción al entrar al servidor'''
        # TODO verificación de usuario
        self.signal_join.emit(
            {
                0: 'joining',
                1: self.name.text()
            }
        )
        self.setWindowTitle('Cargando')

    def action_waiting(self, players: list):
        '''Acción que muestra la sala de espera'''
        # TODO: debe actualizarse los nombres de los labels
        self.windowTitle('Sala de espera')
        if self.wait_label.isHidden():
            self.wait_label.show()
            self.players_frame.show()
            for ply in players:
                self.players_layout.addWidget(QWidget(ply, ))

        else:
            for i, ply in enumerate(players):
                self.players_layout.itemAt(i).text(ply)


class GameWindow(QMainWindow):
    '''Ventana principal dell juego'''

    signal_UNO = pyqtSignal()

    def __init__(self, ui_path):
        super().__init__()
        loadUi(ui_path, self)
        self._set_up()

    def _set_up(self):
        self.setWindowTitle('DCCuadrado')
        self.ActionUNO.pressed.connect(self.signal_UNO.emit)


if __name__ == "__main__":
    # Debe ejecutarse a nivel de client
    import json

    with open('parametros.json') as file:
        content = json.load(file)
    DCC = Game(content['paths'])
    DCC.run()
