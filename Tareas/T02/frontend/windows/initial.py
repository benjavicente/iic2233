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

    signal_start = pyqtSignal(bool) # True si se carga partida

    def __init__(self, *args, **kwards):
        super().__init__(*args, **kwards)
        self.iniciar()

    def iniciar(self):
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
        self.desarrollador = QLabel('benjavicente', self)
        self.desarrollador.setAlignment(Qt.AlignCenter)
        self.desarrollador.setObjectName('desarrollador')
        main_layout.addWidget(self.desarrollador, 4, 0, 1, 3)

        # ----------------------- #
        # Botones de herramientas #
        # ----------------------- #
        barra_herramientas = QHBoxLayout()
        main_layout.addLayout(barra_herramientas, 0, 0, 1, 3)
        barra_herramientas.addItem(QSpacerItem(0, 0, hPolicy=QSizePolicy.Expanding))
        # -> Botón Información
        self.info = QToolButton(self)
        self.info.setToolTip('Información')
        barra_herramientas.addWidget(self.info)
        # -> Botón Configuración
        self.config = QToolButton(self)
        self.config.setToolTip('Configuración')
        barra_herramientas.addWidget(self.config)

        # ---------------- #
        # Cuadro principal #
        # ---------------- #
        self.cuadro_principal = QFrame(self)
        self.cuadro_principal.setObjectName('cuadro')
        cuadro_principal_layout = QVBoxLayout()
        self.cuadro_principal.setLayout(cuadro_principal_layout)
        main_layout.addWidget(self.cuadro_principal, 2, 1)
        # -> Logo
        self.logo = QLabel(self)
        self.logo.setFixedSize(520, 200)
        self.logo.setPixmap(QPixmap(PATH['logo']))
        self.logo.setScaledContents(True)
        # Añadilo al cuadro
        cuadro_principal_layout.addWidget(self.logo)

        # -> Texto de bienvenida
        # TODO: esto podría estar en parámetros
        texto = ('Hola! Bienvenido al DCCafé!'
                 'No está completamente listo para su apertura aún')
        self.bienvenida = QLabel(texto, self)
        self.bienvenida.setWordWrap(True)
        self.bienvenida.setObjectName('bienvenida')
        self.bienvenida.setAlignment(Qt.AlignCenter)
        # Añadirlo al cuadro
        cuadro_principal_layout.addWidget(self.bienvenida)
        # Añadir espacio
        cuadro_principal_layout.addSpacing(50)

        # -> Botones
        fila_botones = QHBoxLayout()
        cuadro_principal_layout.addLayout(fila_botones)
        fila_botones.setSpacing(20)
        fila_botones.setContentsMargins(30, 0, 30, 0)

        # --> Cargar partida
        self.cargar = QPushButton('Cargar Partida', self)
        self.cargar.setCursor(QCursor(Qt.PointingHandCursor))
        self.cargar.clicked.connect(self.empezar_juego)
        fila_botones.addWidget(self.cargar)

        # --> Nueva pertida
        self.nueva = QPushButton('Nueva Partida', self)
        self.nueva.setCursor(QCursor(Qt.PointingHandCursor))
        self.nueva.clicked.connect(self.empezar_juego)
        fila_botones.addWidget(self.nueva)

        # -------- #
        # Espacios #
        # -------- #
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 1, 1)
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 3, 1)

    def empezar_juego(self):
        '''El juego se inicia inmediatamente al cerrar esta ventana'''
        self.signal_start.emit(True)
        self.hide()
