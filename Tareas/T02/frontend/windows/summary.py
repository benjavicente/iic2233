'''
Ventana Posterior del juego
'''

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QVBoxLayout, QWidget)

from ..themes import SUMMARY_THEME
from ..paths import PATH

class SummaryWindow(QWidget):
    '''Ventana que muestra los el resumen de la ronda'''
    def __init__(self, *args, **kwards):
        super().__init__(*args, **kwards)
        self.iniciar()

    def iniciar(self):
        '''Inicia la ventana'''
        self.setWindowTitle('DCCafé - Resumen Ronda')
        self.setStyleSheet(SUMMARY_THEME)
        # Grid principal
        main_layout = QGridLayout()
        self.setLayout(main_layout)
        # Bloque de información
        layout_resumen = QVBoxLayout()
        self.card_resumen = QFrame()
        self.card_resumen.setLayout(layout_resumen)
        self.card_resumen.setObjectName('bloque')
        main_layout.addWidget(self.card_resumen, 1, 1)
        # -> Título
        self.titulo = QLabel(self)
        self.titulo.setObjectName('titulo')
        self.titulo.setAlignment(Qt.AlignCenter)
        layout_resumen.addWidget(self.titulo)
        # -> Linea separadora
        self.linea = QFrame()
        self.linea.setObjectName('linea')
        self.linea.setFixedHeight(5)
        layout_resumen.addWidget(self.linea)
        layout_resumen.addSpacing(50)
        # -> Resultados
        grid_resultado = QGridLayout()
        grid_resultado.setColumnStretch(0, 3)
        grid_resultado.setColumnStretch(1, 2)
        grid_resultado.setContentsMargins(*[80, 0] * 2)
        layout_resumen.addLayout(grid_resultado)
        # --> Clientes perdidos
        # label
        self.label_perdidos = QLabel('Clientes Perdidos', self)
        self.label_perdidos.setObjectName('label_pedidos')
        self.label_perdidos.setAlignment(Qt.AlignRight)
        grid_resultado.addWidget(self.label_perdidos, 0, 0)
        # valor
        self.perdidos = QLabel('2', self)
        self.perdidos.setObjectName('pedidos')
        self.perdidos.setAlignment(Qt.AlignRight)
        grid_resultado.addWidget(self.perdidos, 0, 1)
        # --> Clientes atendidos
        # label
        self.label_atendidos = QLabel('Clientes Atendidos', self)
        self.label_atendidos.setObjectName('label_atendidos')
        self.label_atendidos.setAlignment(Qt.AlignRight)
        grid_resultado.addWidget(self.label_atendidos, 1, 0)
        # valor
        self.atendidos = QLabel('12', self)
        self.atendidos.setObjectName('atendidos')
        self.atendidos.setAlignment(Qt.AlignRight)
        grid_resultado.addWidget(self.atendidos, 1, 1)
        # --> Dinero acumulado
        # label
        self.label_dinero = QLabel('Dinero Acumulado', self)
        self.label_dinero.setObjectName('label_dinero')
        self.label_dinero.setAlignment(Qt.AlignRight)
        grid_resultado.addWidget(self.label_dinero, 2, 0)
        # valor
        self.dinero = QLabel('$100000', self)
        self.dinero.setObjectName('dinero')
        self.dinero.setAlignment(Qt.AlignRight)
        grid_resultado.addWidget(self.dinero, 2, 1)
        # -> Reputación
        self.label_reputacion = QLabel('Reputación', self)
        self.label_reputacion.setObjectName('rep')
        self.label_reputacion.setAlignment(Qt.AlignCenter)
        layout_resumen.addSpacing(30)
        layout_resumen.addWidget(self.label_reputacion)
        # --> Estrellas
        fila_estrellas = QHBoxLayout()
        fila_estrellas.setContentsMargins(30, 0, 30, 0)
        self.estrella_llena = QPixmap(PATH['star']['filed'])
        self.estrella_vacia = QPixmap(PATH['star']['empty'])
        self.estrellas = []
        for _ in range(5):
            estrella = QLabel()
            estrella.setFixedSize(40, 40)
            estrella.setScaledContents(True)
            fila_estrellas.addWidget(estrella)
            self.estrellas.append(estrella)
        layout_resumen.addLayout(fila_estrellas)
        # -> Botones
        fila_botones = QHBoxLayout()
        layout_resumen.addSpacing(50)
        layout_resumen.addLayout(fila_botones)
        # --> Salir
        self.salir = QPushButton('Salir', self)
        self.salir.setObjectName('salir')
        self.salir.setCursor(QCursor(Qt.PointingHandCursor))
        fila_botones.addWidget(self.salir)
        # --> Guardar
        self.guardar = QPushButton('Guardar', self)
        self.guardar.setObjectName('guardar')
        self.guardar.setCursor(QCursor(Qt.PointingHandCursor))
        fila_botones.addWidget(self.guardar)
        # --> Continuar
        self.continuar = QPushButton('Continuar', self)
        self.continuar.setObjectName('continuar')
        self.continuar.setCursor(QCursor(Qt.PointingHandCursor))
        fila_botones.addWidget(self.continuar)
        # -> Espacios
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 0, 1)
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 2, 1)
        main_layout.addItem(QSpacerItem(0, 0, hPolicy=QSizePolicy.Expanding), 1, 0)
        main_layout.addItem(QSpacerItem(0, 0, hPolicy=QSizePolicy.Expanding), 1, 2)

    def titulo_ronda(self, n_ronda: int = 0) -> None:
        '''Actualiza el título de la ronda'''
        if not isinstance(n_ronda, int):
            raise TypeError(f'El número de la ronda {n_ronda.__repr__()} no es valido')
        self.titulo.setText(f'Resumen ronda {n_ronda}')

    def mostrar_reputacion(self, rep: int) -> None:
        '''Muestra la reputacion con estrellas'''
        if not isinstance(rep, int) or not 0 <= rep <= 5:
            raise ValueError(f'La reputación {rep.__repr__()} no es un número entre 0 y 5')
        for indice in range(5):
            if rep > 0:
                self.estrellas[indice].setPixmap(self.estrella_llena)
            else:
                self.estrellas[indice].setPixmap(self.estrella_vacia)
            rep -= 1
