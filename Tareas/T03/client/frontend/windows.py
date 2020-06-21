'''Ventanas del juego'''

import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QVBoxLayout, QWidget)


class Game(QApplication):
    '''Clase que conecta las ventanas del juego'''
    def __init__(self, paths):
        sys.__excepthook__ = lambda t, v, trace: print(t, v, trace, sep="\n")
        super().__init__(sys.argv)
        # Pixelmaps
        self.logo = QPixmap(paths['logo'])
        # Crea las ventanas con un tamaño adecuado
        screen = self.primaryScreen()
        window_size = screen.availableSize() / 2
        self.initial_window = InitialWindow(window_size, self.logo)
        self.game_window = GameWindow(window_size, self.logo)
        # Aplica el estilo a las ventanas
        with open('theme.css') as theme_file:
            theme = theme_file.read()
        self.setStyleSheet(theme)

    def run(self):
        '''Core el juego'''
        self.initial_window.show()
        sys.exit(self.exec_())



class Window(QMainWindow):
    '''Clase abstractas para las ventanas'''
    def __init__(self, name, size, pix_logo):
        super().__init__()
        self.setMaximumSize(size)
        self.setObjectName(type(self).__name__)
        self.setWindowTitle(name)
        self.pix_logo = pix_logo
        self._set_up()

    def _set_up(self):
        raise NotImplementedError



class InitialWindow(Window):
    '''Ventana que se muestra al iniciar el programa'''
    signal_join = pyqtSignal(dict)

    def __init__(self, *args):
        super().__init__('Ventana Inicial', *args)

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
        self.join.setObjectName('join')
        self.join.clicked.connect(self.action_join)
        entry_layout.addWidget(self.join)

        #--> Sala de espera
        # Etiqueta
        self.wait_label = QLabel('Jugadores conectados')
        self.wait_label.setObjectName('wait_label')

    def action_join(self):
        '''Acción al entrar al servidor'''
        # TODO verificación de usuario
        self.signal_join.emit(
            {
                'name': self.name.text()
            }
        )
        self.name_entry.deleteLater()
        self.setWindowTitle('Entrando a la sala')
        #! TEMOPAL
        self.action_wait()

    def action_wait(self, *args):
        '''Acción que muestra la sala de espera'''
        # TODO: debe actualizarse los nombres de los labels
        #* Podría entregarse un diccionario con la cantidad e jugadores
        #* esperados y los jugadores ya ingresados.
        #* Debe existir una función que actualice los labels a medida que
        #* salgan y entren jugadores
        # Etiqueta de jugadores conectados
        layout = self.centralWidget().layout()
        layout.addWidget(self.wait_label, alignment=Qt.AlignCenter)
        players_layout = QVBoxLayout()



class GameWindow(Window):
    '''Ventana principal dell juego'''
    def __init__(self, *args):
        super().__init__('DCCuadrado', *args)

    def _set_up(self):
        pass


if __name__ == "__main__":
    import json

    with open('../parametros.json') as file:
        content = json.load(file)
    DCC = Game(content['paths'])
    DCC.run()
