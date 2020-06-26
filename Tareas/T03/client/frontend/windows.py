'''Ventanas del juego'''

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QPixmap, QTransform
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
from PyQt5.uic import loadUi


class InitialWindow(QMainWindow):
    '''Ventana que se muestra al iniciar el programa'''

    signal_join = pyqtSignal(str)  # trata de unirse
    # TODO: el chat también tiene que estar implementado aquí
    # TODO: talvez sea menjor guardar todo en la aplicación?

    def __init__(self, pix_logo):
        super().__init__()
        self.setObjectName(type(self).__name__)
        self.setWindowTitle('Ventana Inicial')
        self.pix_logo = pix_logo
        self._set_up()

    def _set_up(self) -> None:
        'Agrega los elementos gráficos a la ventana'
        # Widget principal y layout centrado
        main = QWidget()
        self.setCentralWidget(main)
        self.setMaximumSize(500, 500)
        middler_layout = QGridLayout()

        expand = QSizePolicy.Expanding
        middler_layout.addItem(QSpacerItem(0, 0, hPolicy=expand, vPolicy=expand), 1, 0)
        middler_layout.addItem(QSpacerItem(0, 0, hPolicy=expand, vPolicy=expand), 1, 2)
        middler_layout.addItem(QSpacerItem(0, 0, hPolicy=expand, vPolicy=expand), 0, 1)
        middler_layout.addItem(QSpacerItem(0, 0, hPolicy=expand, vPolicy=expand), 2, 1)

        # Contenedor principal
        main_layout = QVBoxLayout()
        middler_layout.addLayout(main_layout, 1, 1)
        main.setLayout(middler_layout)

        #--> Ventana Inicial
        # Logo
        height = 200
        logo = QLabel(main)
        logo.setFixedHeight(height)
        logo.setPixmap(self.pix_logo.scaledToHeight(height))
        main_layout.addWidget(logo, alignment=Qt.AlignCenter)
        # Añade el campo de nombre
        self.name_entry = QWidget(main)
        entry_layout = QHBoxLayout()
        self.name_entry.setLayout(entry_layout)
        main_layout.addWidget(self.name_entry)
        # Nombre
        self.name = QLineEdit(self.name_entry)
        self.name.setPlaceholderText('Ingresa un nombre')
        self.name.setObjectName('Name')
        self.name.returnPressed.connect(self.action_joining)
        entry_layout.addWidget(self.name)
        # Botón para unirse
        self.join = QPushButton(self.name_entry)
        self.join.setText('Entrar')
        self.join.setObjectName('JoinButton')
        self.join.setCursor(QCursor(Qt.PointingHandCursor))
        self.join.clicked.connect(self.action_joining)
        entry_layout.addWidget(self.join)

        #--> Sala de espera
        self.wait_room = QWidget(main)
        wait_room_layout = QGridLayout()
        self.wait_room.setLayout(wait_room_layout)
        main_layout.addWidget(self.wait_room)
        # Etiqueta
        wait_label = QLabel('Jugadores conectados', self.wait_room)
        wait_label.setObjectName('WaitLabel')
        wait_room_layout.addWidget(wait_label, 0, 0, alignment=Qt.AlignCenter)
        # Cuadro de jugadores en espera
        players_frame = QWidget(self.wait_room)
        self.players_layout = QVBoxLayout()
        players_frame.setLayout(self.players_layout)
        wait_room_layout.addWidget(players_frame, 1, 0)
        # Chat
        # TODO: se tiene que agregar enb la columna de la derecha de wait_room_layout
        # Se esconde lo anterior
        self.wait_room.hide()

    def action_joining(self) -> None:
        '''Acción al entrar al servidor'''
        self.join.setDisabled(True)
        self.name.setDisabled(True)
        self.signal_join.emit(self.name.text())
        self.setWindowTitle('Cargando')

    def state_joining_failed(self, error: dict) -> None:
        '''Estado que se muestra al fallar entrar al servidor'''
        self.setWindowTitle('Ventana Inicial')
        QMessageBox.information(self, 'Error', error['display'])
        self.join.setDisabled(False)
        self.name.setDisabled(False)

    def action_waiting(self, players: list) -> None:
        '''Acción que muestra la sala de espera'''
        self.setWindowTitle('Sala de espera')
        # Se crean los widgets
        if self.wait_room.isHidden():
            self.name_entry.hide()
            self.wait_room.show()
            for _ in range(len(players)):
                self.players_layout.addWidget(QLabel(self.wait_room), alignment=Qt.AlignCenter)
        # Se añaden los nombres
        for i, ply in enumerate(players):
            widget = self.players_layout.itemAt(i).widget()
            if ply:
                widget.setObjectName('WaitingPlayer')
                widget.setText(ply)
            else:
                widget.setObjectName('EmptyPlayer')
                widget.setText('~~~')
            # Es raro como se debe cambiar el estilo...
            # https://stackoverflow.com/q/9066669
            self.style().polish(widget)



class GameCard(QLabel):
    'Carta del juego'
    __angle = {0: 0, 1: 90, 2: 180, 3: 270}
    def __init__(self, parent, size: QSize, pixmap_data, position: int = 0, click_signal=None):
        super().__init__(parent)
        # Guarda si es del jugador principal
        self.__accesible = bool(click_signal)
        # Ve si inicia un nuevo pixmap o toma uno entregado
        if isinstance(pixmap_data, QPixmap):
            pixmap = pixmap_data
        elif isinstance(pixmap_data, (bytearray, bytes)):
            pixmap = QPixmap()
            pixmap.loadFromData(pixmap_data)
        # Rota el pixmap y lo añade
        flip = QTransform()
        flip.rotate(self.__angle[position])
        self.setPixmap(pixmap.transformed(flip))
        # Cambia el tamaño para que coincida con la rotación
        self.setScaledContents(True)
        if position % 2:
            card_size = size.transposed()
        else:
            card_size = size
        self.setFixedSize(card_size)
        # Configuración adicional si la carta es del jugador principal
        if self.__accesible:
            self.setCursor(QCursor(Qt.PointingHandCursor))
            self.__click_signal = click_signal

    def mousePressEvent(self, event):
        'Maneja el click en la carta'
        if self.__accesible:
            # Se tiene que encontrar el indice de la carta en el layout
            index = self.parentWidget().layout().indexOf(self)
            # Se emite la señal al servidor
            self.__click_signal.emit(index)


class GameWindow(QMainWindow):
    '''Ventana principal dell juego'''

    signal_chat = pyqtSignal(str)  # manda un mensage
    signal_call = pyqtSignal()     # TODO llama DCCuadrádo
    signal_draw = pyqtSignal()     # TODO roba una carta
    signal_drop = pyqtSignal(int)  # id de la carta seleccionada

    def __init__(self, ui_path):
        super().__init__()
        loadUi(ui_path, self)
        self._set_up()
        # Referencia de las manos de los jugadores
        self._player_hands = dict()
        # Referencia al reverso de la carta
        self.reverse_card = None

    def _set_up(self) -> None:
        self.card_size = QSize(80, 112)
        self.CardPool.setFixedSize(self.card_size)
        self.CardDeck.setFixedSize(self.card_size)
        self.ActionUNO.setCursor(QCursor(Qt.PointingHandCursor))
        self.ChatInput.returnPressed.connect(self.send_chat)

    def send_chat(self) -> None:
        'Manda un mensaje al chat'
        mesaje = self.ChatInput.text()
        if mesaje:
            self.signal_chat.emit(mesaje)
            self.ChatInput.clear()

    def add_chat_mesaje(self, mesaje: str) -> None:
        'Recibe un mensaje'
        new = self.Chat.toMarkdown() + '\n' + mesaje
        self.Chat.setMarkdown(new.strip())

    def set_reverse_card(self, card_pixmap: object) -> None:
        'Establece el reverso de la carta'
        self.reverse_card = QPixmap()
        self.reverse_card.loadFromData(card_pixmap)
        self.CardDeck.setPixmap(self.reverse_card)

    def setup_players(self, game_info: dict) -> None:
        'Prepara el interfaz de juego'
        for i in map(str, range(4)):
            if i in game_info:
                # Cambia el nombre del label
                getattr(self, f'Player{i}Name').setText(game_info[i])
                # Añade la referencia de la mano
                self._player_hands[game_info[i]] = getattr(self, f'Player{i}Cards')

    def update_pool(self, c_color: str, c_type: str, c_pixmap: object, active_player: str) -> None:
        'Añade la carta del pozo. Sigue lo establecido en el Enunciado'
        pixmap = QPixmap()
        pixmap.loadFromData(c_pixmap)
        self.CardPool.setPixmap(pixmap)
        self.ActiveColor.setText(c_color)
        self.ActivePlayer.setText(active_player)

    def add_player_card(self, c_color: str, c_type: str, c_pixmap: object) -> None:
        'Añade la carta al jugador. Sigue lo establecido en el Enunciado'
        card = GameCard(self.Player0Cards, self.card_size, c_pixmap, 0, self.signal_drop)
        self.Player0Cards.layout().addWidget(card)
        self.ActiveColor.setText(c_color)

    def add_opponent_card(self, name: str) -> None:
        'Añade una carta al oponente'
        #* Esto es bien parche, pero funciona para rotar las cartas
        pos = list(self._player_hands).index(name)
        card = GameCard(self._player_hands[name], self.card_size, self.reverse_card, pos)
        self._player_hands[name].layout().addWidget(card)

    def remove_card(self, name: str, index: int) -> None:
        'Remueve la carta con indice `index` del jugador con nombre `name`'
        # https://doc.qt.io/qt-5/qlayout.html#removeItem
        # https://stackoverflow.com/q/43343773
        layout = self._player_hands[name].layout()
        widget = layout.itemAt(index).widget()
        widget.close()
        layout.removeWidget(widget)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from sys import argv
    from os.path import join
    APP = QApplication(argv)
    with open('theme.css') as file:
        APP.setStyleSheet(file.read())
    INITIAL_WINDOW = InitialWindow(QPixmap(join('sprites', 'logo')))
    GAME_WINDOW = GameWindow('game_window.ui')
    INITIAL_WINDOW.show()
    GAME_WINDOW.show()
    APP.exec_()
