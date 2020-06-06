'''Ventana inicial del juego'''

from random import choice

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import (QFrame, QGridLayout, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSpacerItem,
                             QToolButton, QVBoxLayout, QWidget)

from frontend.paths import SPRITE_PATH
from frontend.themes import INITIAL_THEME


class InitialWindow(QWidget):
    '''Ventana que se abre al iniciar el programa'''

    signal_load = pyqtSignal(dict)
    signal_new = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.amount_of_players = 1
        self.init_ui()

    def init_ui(self):
        '''Inicia la ventana'''
        self.setWindowTitle('DCCafé - Inicio')
        self.setStyleSheet(INITIAL_THEME)

        # Crear un Grid de 5x3
        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # Firma
        self.developer = QLabel('benjavicente', self)
        self.developer.setAlignment(Qt.AlignCenter)
        self.developer.setObjectName('developer')
        main_layout.addWidget(self.developer, 4, 0, 1, 3)

        # ----------------------- #
        # Botones de herramientas #
        # ----------------------- #
        tool_bar = QHBoxLayout()
        main_layout.addLayout(tool_bar, 0, 0, 1, 3)
        tool_bar.addItem(QSpacerItem(0, 0, hPolicy=QSizePolicy.Expanding))
        # -> Botón Información
        self.info = QToolButton(self)
        self.info.setObjectName('info')
        self.info.setToolTip('Información')
        self.info.setText('i')
        self.info.pressed.connect(info)
        self.info.setCursor(QCursor(Qt.PointingHandCursor))
        tool_bar.addWidget(self.info)
        # -> Botón Información
        self.players = QToolButton(self)
        self.players.setObjectName('players')
        self.players.setToolTip('Jugadores')
        self.players.setText(str(self.amount_of_players))
        self.players.pressed.connect(self.change_players)
        self.players.setCursor(QCursor(Qt.PointingHandCursor))
        tool_bar.addWidget(self.players)

        # ---------------- #
        # Cuadro principal #
        # ---------------- #
        self.card = QFrame(self)
        self.card.setObjectName('card')
        card_layout = QVBoxLayout()
        self.card.setLayout(card_layout)
        main_layout.addWidget(self.card, 2, 1)
        # -> Logo
        self.logo = QLabel(self)
        self.logo.setFixedSize(520, 200)
        self.logo.setPixmap(QPixmap(SPRITE_PATH['logo']))
        self.logo.setScaledContents(True)
        # Añadilo al cuadro
        card_layout.addWidget(self.logo)
        card_layout.addSpacing(30)

        # -> Texto de bienvenida
        text = choice([
            'Del creador de DCCahuín y DCCriaturas mágicas',
            'Nada mejor que un DCCafé por la mañana',
            '¡DCCorre a 60fps!'
        ])
        self.message = QLabel(text, self)
        self.message.setWordWrap(True)
        self.message.setObjectName('message')
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setFixedHeight(100)
        # Añadirlo al cuadro
        card_layout.addWidget(self.message)
        # Añadir espacio
        card_layout.addSpacing(80)

        # -> Botones
        button_layout = QHBoxLayout()
        card_layout.addLayout(button_layout)
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(30, 0, 30, 0)

        # --> Cargar partida
        self.button_load_game = QPushButton('Cargar Partida', self)
        self.button_load_game.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_load_game.clicked.connect(self.load_game)
        button_layout.addWidget(self.button_load_game)

        # --> Nueva pertida
        self.button_new_game = QPushButton('Nueva Partida', self)
        self.button_new_game.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_new_game.clicked.connect(self.new_game)
        button_layout.addWidget(self.button_new_game)

        # -------- #
        # Espacios #
        # -------- #
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 1, 1)
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 3, 1)

    def load_game(self):
        '''Se carga un juego'''
        self.signal_load.emit({'players': self.amount_of_players})
        self.hide()

    def new_game(self):
        '''Se empieza un nuevo juego'''
        self.signal_new.emit({'players': self.amount_of_players})
        self.hide()

    def change_players(self):
        '''Cambia el número de jugadores'''
        self.amount_of_players = self.amount_of_players % 2 + 1
        self.players.setText(str(self.amount_of_players))


def info():
    '''Información'''
    print(  # https://en.wikipedia.org/wiki/Box-drawing_character
        '  ┌───────────────────────────┐  ',
        '  │        info DCCafé        │▒▒',
        '  ╞═══════════════════════════╡▒▒',
        '  │ - Para habilitar el modo  │▒▒',
        '  │ multijugador, apretar el  │▒▒',
        '  │ segundo botón, el número  │▒▒',
        '  │ indica los jugadores      │▒▒',
        '  │ actuales.                 │▒▒',
        '  │ - Los datos que no se     │▒▒',
        '  │ muestran en el UI son     │▒▒',
        '  │ mostrados en la consola,  │▒▒',
        '  │ como por ejemplo, cuando  │▒▒',
        '  │ los chef suben de nivel.  │▒▒',
        '  │ - Si el juego se queda    │▒▒',
        '  │ pegado, usar `Ctrl` + `C` │▒▒',
        '  │ en la consola.            │▒▒',
        '  │                           │▒▒',
        '  │    ¡Disfrute el Juego!    │▒▒',
        '  └───────────────────────────┘▒▒',
        '   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒',
        sep='\n', end='\n'*2
    )
