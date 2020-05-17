'''
Ventana principal
'''

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QToolButton, QVBoxLayout, QWidget, QToolTip)

from ui_tools import RUTA_LOGO, STYLE_SHEET_VENTANA_INICIO


class VentanaInicio(QWidget):
    '''Ventana que se abre al iniciar el programa'''
    def __init__(self, *args, **kwards):
        super().__init__(*args, **kwards)
        self.iniciar()

    def iniciar(self):
        '''Inicia la ventana'''
        self.setWindowTitle('DCCafé - Inicio')
        self.setStyleSheet(STYLE_SHEET_VENTANA_INICIO)
        #self.setWindowIcon(QIcon(QPixmap(RUTA_LOGO))) # TODO: Ver lo de loos íconos

        # Crear un Grid de 5x5
        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # Firma
        self.desarrollador = QLabel('benjavicente', self)
        self.desarrollador.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.desarrollador, 4, 0, 1, 5)

        # ----------------------- #
        # Botones de herramientas #
        # ----------------------- #
        barra_herramientas = QHBoxLayout()
        main_layout.addLayout(barra_herramientas, 0, 0, 1, 5)
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
        cuadro_principal_layout = QVBoxLayout()
        self.cuadro_principal.setLayout(cuadro_principal_layout)
        main_layout.addWidget(self.cuadro_principal, 2, 2)
        # -> Logo
        self.logo = QLabel(self)
        # Formato
        self.logo.setMinimumSize(520, 200)
        self.logo.setMaximumSize(520, 200)
        self.logo.setPixmap(QPixmap(RUTA_LOGO))
        self.logo.setScaledContents(True)
        # Añadilo al cuadro
        cuadro_principal_layout.addWidget(self.logo)
        # -> Texto de bienvenida
        self.bienvenida = QLabel('Hola!', self)
        # Formato
        self.bienvenida.setAlignment(Qt.AlignCenter)
        # Añadirlo al cuadro
        cuadro_principal_layout.addWidget(self.bienvenida)
        # Añadir espacio
        cuadro_principal_layout.addItem(QSpacerItem(0, 50))
        # -> Botones
        fila_botones = QHBoxLayout()
        cuadro_principal_layout.addLayout(fila_botones)
        fila_botones.setSpacing(0)
        # --> Cargar partida
        self.cargar = QPushButton('Cargar Partida', self)
        fila_botones.addWidget(self.cargar)
        self.cargar.setCursor(QCursor(Qt.PointingHandCursor))
        # --> Nueva pertida
        self.nueva = QPushButton('Nueva Partida', self)
        fila_botones.addWidget(self.nueva)
        self.nueva.setCursor(QCursor(Qt.PointingHandCursor))

        # -------- #
        # Espacios #
        # -------- #
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 1, 2)
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 3, 2)

        # ------- #
        # Mostrar #
        # ------- #
        self.show()


if __name__ == "__main__":
    sys.__excepthook__ = lambda t, v, trace: print(t, trace, sep="\n")
    APP = QApplication(sys.argv)
    VENTANA = VentanaInicio()
    VENTANA.show()
    sys.exit(APP.exec())
