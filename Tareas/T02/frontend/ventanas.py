'''
Ventana principal
'''

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSpacerItem,
                             QToolButton, QVBoxLayout, QWidget)

RUTA_LOGO = R'sprites\otros\logo_blanco.png'  # TODO: Cambiar!

class VentanaInicio(QWidget):
    '''Ventana que se abre al iniciar el programa'''
    def __init__(self, *args, **kwards):
        super().__init__(*args, **kwards)
        self.iniciar()

    def iniciar(self):
        '''Inicia la ventana'''
        self.setWindowTitle('DCCafé - Inicio')
        #self.setWindowIcon(QIcon(QPixmap(RUTA_LOGO))) # TODO: Ver lo de loos íconos

        # Crear un Grid de 5x5
        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # ----------------------- #
        # Botones de herramientas #
        # ----------------------- #
        barra_herramientas = QHBoxLayout()
        main_layout.addLayout(barra_herramientas, 0, 0, 1, 5)
        barra_herramientas.addItem(QSpacerItem(0, 0, hPolicy=QSizePolicy.Expanding))
        # -> Botón Información
        self.info = QToolButton(self)
        barra_herramientas.addWidget(self.info)
        # -> Botón Configuración
        self.config = QToolButton(self)
        barra_herramientas.addWidget(self.config)

        # ---------------- #
        # Cuadro principal #
        # ---------------- #
        cuadro_principal = QVBoxLayout()
        main_layout.addLayout(cuadro_principal, 2, 2)
        # -> Logo
        self.logo = QLabel(self)
        # Formato
        self.logo.setMinimumSize(520, 200)
        self.logo.setMaximumSize(520, 200)
        self.logo.setPixmap(QPixmap(RUTA_LOGO))
        self.logo.setScaledContents(True)
        # Añadilo al cuadro
        cuadro_principal.addWidget(self.logo)
        # -> Texto de bienvenida
        self.bienvenida = QLabel('Hola!', self)
        # Formato
        self.bienvenida.setAlignment(Qt.AlignCenter)
        self.bienvenida.setStyleSheet('''
            font: 24px "Roboto Slab";
        ''')
        # Añadirlo al cuadro
        cuadro_principal.addWidget(self.bienvenida)
        # Añadir espacio
        cuadro_principal.addItem(QSpacerItem(0, 50))
        # -> Botones
        fila_botones = QHBoxLayout()
        cuadro_principal.addLayout(fila_botones)
        # --> Cargar partida
        self.cargar = QPushButton('Cargar partida', self)
        fila_botones.addWidget(self.cargar)
        self.cargar.setStyleSheet('''
            font: 18px "Roboto Slab";
        ''')
        # --> Nueva pertida
        self.nueva = QPushButton('Nueva Partida', self)
        fila_botones.addWidget(self.nueva)
        self.nueva.setStyleSheet('''
            font: 18px "Roboto Slab";
        ''')

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
