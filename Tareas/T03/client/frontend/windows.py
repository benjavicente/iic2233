'''Ventanas del juego'''

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QPixmap, QTransform
from PyQt5.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton, QTextEdit,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
from PyQt5.uic import loadUi


class InitialWindow(QMainWindow):
    '''Ventana que se muestra al iniciar el programa'''

    signal_join = pyqtSignal(str)  # trata de unirse
    signal_chat = pyqtSignal(str)  # manda un chat

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
        self.name_input = QLineEdit(self.name_entry)
        self.name_input.setPlaceholderText('Ingresa un nombre')
        self.name_input.setObjectName('name_input')
        self.name_input.returnPressed.connect(self.action_joining)
        entry_layout.addWidget(self.name_input)
        # Botón para unirse
        self.join_button = QPushButton(self.name_entry)
        self.join_button.setText('Entrar')
        self.join_button.setObjectName('join_button')
        self.join_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.join_button.clicked.connect(self.action_joining)
        entry_layout.addWidget(self.join_button)

        #--> Sala de espera
        self.wait_room = QWidget(main)
        wait_room_layout = QGridLayout()
        self.wait_room.setLayout(wait_room_layout)
        main_layout.addWidget(self.wait_room)
        # Etiqueta
        wait_label = QLabel('Jugadores\nconectados', self.wait_room)
        wait_label.setObjectName('wait_label')
        wait_room_layout.addWidget(wait_label, 0, 0, alignment=Qt.AlignCenter)
        # Cuadro de jugadores en espera
        players_frame = QWidget(self.wait_room)
        self.players_layout = QVBoxLayout()
        players_frame.setLayout(self.players_layout)
        wait_room_layout.addWidget(players_frame, 1, 0)
        # Chat
        self.chat_box = QTextEdit(self.wait_room)
        self.chat_box.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.chat_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_box.setPlaceholderText('Bienvenido! Se el primero en mandar un saludo!')
        self.chat_box.setObjectName('chat_box')
        self.chat_box.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse)
        wait_room_layout.addWidget(self.chat_box, 0, 1, 2, 1)
        # Chat input
        self.chat_input = QLineEdit(self.wait_room)
        self.chat_input.setPlaceholderText('Enviar mensaje al chat')
        self.chat_input.returnPressed.connect(self.send_chat)
        self.chat_input.setObjectName('chat_input')
        wait_room_layout.addWidget(self.chat_input, 2, 1)
        # Se esconde lo anterior
        self.wait_room.hide()

    def action_joining(self) -> None:
        '''Acción al entrar al servidor'''
        self.join_button.setDisabled(True)
        self.name_input.setDisabled(True)
        self.signal_join.emit(self.name_input.text())
        self.setWindowTitle('Cargando')

    def state_joining_failed(self, error: dict) -> None:
        '''Estado que se muestra al fallar entrar al servidor'''
        self.setWindowTitle('Ventana Inicial')
        QMessageBox.information(self, 'Error', error['display'])
        self.join_button.setDisabled(False)
        self.name_input.setDisabled(False)

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
                widget.setObjectName('waiting_player')
                widget.setText(ply)
            else:
                widget.setObjectName('empty_player')
                widget.setText('~~~')
            # Es raro como se debe cambiar el estilo...
            # https://stackoverflow.com/q/9066669
            self.style().polish(widget)

    def send_chat(self) -> None:
        'Manda un mensaje al chat'
        mesaje = self.chat_input.text()
        if mesaje:
            self.signal_chat.emit(mesaje)
            self.chat_input.clear()

    def update_chat(self, chat: str) -> None:
        'Recibe un mensaje'
        self.chat_box.setMarkdown(chat)

    def reset(self):
        'Vuelve al estado inicial'
        self.wait_room.hide()
        self.join_button.setDisabled(False)
        self.name_input.setDisabled(False)
        self.name_entry.show()


class GameCard(QLabel):
    'Carta del juego. Se le asigna un señal a emitir.'
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


class Deck(QLabel):
    'QLabel que emite una señal propia al ser precionado'
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()


class WinPopUp(QMessageBox):
    'PopUp que se muestra al terminar el juego'
    def __init__(self, pixmap_path):
        super().__init__()
        pixmap = QPixmap(pixmap_path)
        self.setIconPixmap(pixmap.scaled(80, 80))
        self.setWindowTitle('Tenemos ganador!')

    def set_winner(self, winner: str):
        'Añade al ganador'
        self.setText(f'Ha gandado {winner}. Felicitaciones!')


class ColorPicker(QMessageBox):
    'PopUp que permite elegir colores'
    color_map = {'rojo': 'red', 'verde': 'green', 'azul': 'blue', 'amarillo': 'yellow'}
    def __init__(self, colors: tuple):
        super().__init__()
        self.setWindowTitle('Selecciona')
        self.setText('Selecciona un color')
        for color in colors:
            button = self.addButton('', QMessageBox.AcceptRole)
            button.setStyleSheet(f'background: {self.color_map[color]}')


class GameWindow(QMainWindow):
    '''Ventana principal dell juego'''

    signal_chat = pyqtSignal(str)  # manda un mensage
    signal_call = pyqtSignal()     # llama DCCuadrádo
    signal_play = pyqtSignal(int)  # id de la carta seleccionada

    def __init__(self, ui_path: str, card_size: tuple):
        super().__init__()
        loadUi(ui_path, self)
        # Tamaño de las carats
        self.card_size = QSize(*card_size)
        # Set-up del ui y sus señales
        self._set_up()
        # Referencia de las manos de los jugadores
        self._player_hands = dict()
        # Referencia al reverso de la carta
        self.reverse_card = None

    def _set_up(self) -> None:
        # Se sobreescribe el widget
        self.card_deck = Deck(self.Table)
        self.table_layout.replaceWidget(self.TempCardDeck, self.card_deck)
        self.card_deck.clicked.connect(lambda: self.signal_play.emit(-1))
        self.card_deck.setScaledContents(True)
        self.card_deck.setFixedSize(self.card_size)
        self.card_deck.setCursor(QCursor(Qt.OpenHandCursor))
        self.card_pool.setFixedSize(self.card_size)
        # Se prepara DCCuatro
        self.action_uno.setCursor(QCursor(Qt.PointingHandCursor))
        self.action_uno.pressed.connect(self.signal_call)
        # Se conecta el chat
        self.chat_input.returnPressed.connect(self.send_chat)

    def send_chat(self) -> None:
        'Manda un mensaje al chat'
        mesaje = self.chat_input.text()
        if mesaje:
            self.signal_chat.emit(mesaje)
            self.chat_input.clear()

    def update_chat(self, chat: str) -> None:
        'Recibe un mensaje'
        self.chat_box.setMarkdown(chat)

    def set_reverse_card(self, card_pixmap: object) -> None:
        'Establece el reverso de la carta'
        self.reverse_card = QPixmap()
        self.reverse_card.loadFromData(card_pixmap)
        self.card_deck.setPixmap(self.reverse_card)

    def setup_players(self, game_info: dict) -> None:
        'Prepara el interfaz de juego'
        for i in map(str, range(4)):
            # Limpia el espacio de las cartas
            hand = getattr(self, f'Player{i}Cards')
            self.clear_hand(hand)
            if i in game_info:
                # Cambia el nombre del label
                getattr(self, f'Player{i}Name').setText(game_info[i])
                # Añade la referencia de la mano
                self._player_hands[game_info[i]] = hand

    def update_pool(self, c_color: str, c_type: str, c_pixmap: object, active_player: str) -> None:
        'Añade la carta del pozo. Sigue lo establecido en el Enunciado'
        pixmap = QPixmap()
        pixmap.loadFromData(c_pixmap)
        self.card_pool.setPixmap(pixmap)
        self.active_color.setText(c_color)
        self.active_player.setText(active_player)

    def add_player_card(self, c_color: str, c_type: str, c_pixmap: object) -> None:
        'Añade la carta al jugador. Sigue lo establecido en el Enunciado'
        # Este es el único momento que uso atributos con camelCase, definidos en QtDesigner
        card = GameCard(self.Player0Cards, self.card_size, c_pixmap, 0, self.signal_play)
        self.Player0Cards.layout().addWidget(card)

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
        item = layout.itemAt(index)
        layout.removeItem(item)
        item.widget().close()

    def player_lossed(self, name: str):
        'Para de mostrar las castas de un jugador que perdió'
        self.clear_hand(self._player_hands[name])
        mesage = QLabel(':(', self._player_hands[name])
        mesage.setObjectName('player_lossed')
        mesage.setAlignment(Qt.AlignCenter)
        self._player_hands[name].layout().addWidget(mesage)

    def clear_hand(self, widget):
        'Vacía la mano del jugador, dado por el widget entregado'
        layout = widget.layout()
        for _ in range(layout.count()):
            item = layout.itemAt(0)
            layout.removeItem(item)
            item.widget().deleteLater()
