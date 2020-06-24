'''Ventanas del juego'''

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QPushButton, QVBoxLayout, QWidget, QMessageBox)
from PyQt5.uic import loadUi


class InitialWindow(QMainWindow):
    '''Ventana que se muestra al iniciar el programa'''

    signal_join = pyqtSignal(str)  # trata de unirse

    def __init__(self, pix_logo):
        super().__init__()
        self.setObjectName(type(self).__name__)
        self.setWindowTitle('Ventana Inicial')
        self.pix_logo = pix_logo
        self._set_up()

    def _set_up(self) -> None:
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
        self.join.setCursor(QCursor(Qt.PointingHandCursor))
        self.join.clicked.connect(self.action_joining)
        entry_layout.addWidget(self.join)

        #--> Sala de espera
        # Etiqueta
        self.wait_label = QLabel('Jugadores conectados')
        self.wait_label.setObjectName('WaitLabel')
        layout.addWidget(self.wait_label, alignment=Qt.AlignCenter)
        self.wait_label.hide()  # Se oculta hasta que sea necesario
        # Cuadro de jugadores en espera
        self.players_frame = QWidget(self)
        layout.addWidget(self.players_frame)
        self.players_frame.hide()
        self.players_layout = QVBoxLayout()
        self.players_frame.setLayout(self.players_layout)

    def action_joining(self) -> None:
        '''Acción al entrar al servidor'''
        # TODO verificación de usuario
        self.join.setDisabled(True)
        self.signal_join.emit(self.name.text())
        self.setWindowTitle('Cargando')

    def state_joining_failed(self, error: dict) -> None:
        '''Estado que se muestra al fallar entrar al servidor'''
        self.setWindowTitle('Ventana Inicial')
        QMessageBox.information(self, 'Error', error['display'])
        self.join.setDisabled(False)

    def action_waiting(self, players: list) -> None:
        '''Acción que muestra la sala de espera'''
        self.setWindowTitle('Sala de espera')
        # Se crean los widgets
        if self.wait_label.isHidden():
            self.wait_label.show()
            self.players_frame.show()
            self.name_entry.hide()
            for _ in range(len(players)):
                self.players_layout.addWidget(QLabel(self.players_frame), alignment=Qt.AlignCenter)
        # Se añaden los nombres
        print(players)
        for i, ply in enumerate(players):
            widget = self.players_layout.itemAt(i).widget()
            if ply:
                widget.setObjectName('WaitingPlayer')
                widget.setText(ply)
            else:
                widget.setObjectName('EmptyPlayer')
                widget.setText('~~~')
            # https://stackoverflow.com/q/9066669
            self.style().polish(widget)  # Es raro como se debe cambiar el estilo...


class GameWindow(QMainWindow):
    '''Ventana principal dell juego'''

    signal_chat = pyqtSignal(str)  # manda un mensage
    signal_call = pyqtSignal()     # llama DCCuadrádo
    signal_draw = pyqtSignal()     # roba una carta
    signal_drop = pyqtSignal(int)  # id de la carta seleccionada

    def __init__(self, ui_path):
        super().__init__()
        loadUi(ui_path, self)
        self.card_size = QSize(105, 147)
        self.reverse_card = None
        self._set_up()

    def _set_up(self) -> None:
        self.CardPool.setFixedSize(self.card_size)
        self.CardDeck.setFixedSize(self.card_size)
        self.ActionUNO.setCursor(QCursor(Qt.PointingHandCursor))

    def set_reverse_card(self, card_pixmap: object) -> None:
        'Establece el reverso de la carta'
        pixmap = QPixmap()
        pixmap.loadFromData(card_pixmap)
        self.reverse_card = pixmap
        self.CardDeck.setPixmap(pixmap)

    def setup_players(self, game_info: dict) -> None:
        'Prepara el interfaz de juego'
        self.ActivePlayer.setText(game_info['active_player'])
        for i in map(str, range(4)):
            name_label = getattr(self, f'Player{i}Name', None)
            if i in game_info:
                name_label.setText(game_info[i]['name'])
            else:
                name_label.clear()

    def add_card(self, c_color: str, c_type: str, c_pixmap: object) -> None:
        'Añade la carta al jugador. Sigue lo establecido en el Enunciado'


    def update_pool(self, c_color: str, c_type: str, c_pixmap: object) -> None:
        'Añade la carta al pozo. Sigue lo establecido en el Enunciado'
        self.ActiveColor.setText(c_color)
