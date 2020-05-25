'''
Ventana inicial del juego
'''

import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QToolButton, QVBoxLayout, QWidget, QToolTip)


from frontend.paths import PATH
from frontend.themes import INITIAL_THEME


class InitialWindow(QWidget):
    '''Ventana que se abre al iniciar el programa'''

    signal_load = pyqtSignal()
    signal_new = pyqtSignal()

    def __init__(self, *args, **kwards):
        super().__init__(*args, **kwards)
        self.init_ui()

    def init_ui(self):
        '''Inicia la ventana'''
        self.setWindowTitle('DCCafé - Inicio')
        self.setObjectName('VentanaInicio')
        self.setStyleSheet(INITIAL_THEME)
        # TODO: Ver lo de los íconos
        #self.setWindowIcon(QIcon(QPixmap(RUTA_LOGO)))

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
        self.info.setToolTip('Información')
        tool_bar.addWidget(self.info)
        # -> Botón Configuración
        self.config = QToolButton(self)
        self.config.setToolTip('Configuración')
        tool_bar.addWidget(self.config)

        # ---------------- #
        # Cuadro principal #
        # ---------------- #
        self.card_principal = QFrame(self)
        self.card_principal.setObjectName('card')
        card_principal_layout = QVBoxLayout()
        self.card_principal.setLayout(card_principal_layout)
        main_layout.addWidget(self.card_principal, 2, 1)
        # -> Logo
        self.logo = QLabel(self)
        self.logo.setFixedSize(520, 200)
        self.logo.setPixmap(QPixmap(PATH['logo']))
        self.logo.setScaledContents(True)
        # Añadilo al cuadro
        card_principal_layout.addWidget(self.logo)

        # -> Texto de bienvenida
        # TODO: esto podría estar en parámetros
        texto = ('Hola! Bienvenido al DCCafé!'
                 'No está completamente listo para su apertura aún')
        self.message = QLabel(texto, self)
        self.message.setWordWrap(True)
        self.message.setObjectName('message')
        self.message.setAlignment(Qt.AlignCenter)
        # Añadirlo al cuadro
        card_principal_layout.addWidget(self.message)
        # Añadir espacio
        card_principal_layout.addSpacing(50)

        # -> Botones
        fila_botones = QHBoxLayout()
        card_principal_layout.addLayout(fila_botones)
        fila_botones.setSpacing(20)
        fila_botones.setContentsMargins(30, 0, 30, 0)

        # --> Cargar partida
        self.cargar = QPushButton('Cargar Partida', self)
        self.cargar.setCursor(QCursor(Qt.PointingHandCursor))
        self.cargar.clicked.connect(self.load_game)
        fila_botones.addWidget(self.cargar)

        # --> Nueva pertida
        self.nueva = QPushButton('Nueva Partida', self)
        self.nueva.setCursor(QCursor(Qt.PointingHandCursor))
        self.nueva.clicked.connect(self.new_game)
        fila_botones.addWidget(self.nueva)

        # -------- #
        # Espacios #
        # -------- #
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 1, 1)
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 3, 1)

    def load_game(self):
        '''Se carga un juego'''
        self.signal_load.emit()
        self.hide()

    def new_game(self):
        '''Se empieza un nuevo juego'''
        self.signal_new.emit()
        self.hide()
