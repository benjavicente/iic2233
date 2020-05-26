'''Ventana Posterior del juego'''

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import (QFrame, QGridLayout, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSpacerItem,
                             QVBoxLayout, QWidget)

from frontend.paths import PATH
from frontend.themes import SUMMARY_THEME


class SummaryWindow(QWidget):

    signal_save_game = pyqtSignal()
    signal_continue_game = pyqtSignal()
    signal_exit_game = pyqtSignal()

    '''Ventana que muestra los el resumen de la ronda'''
    def __init__(self):
        super().__init__()
        self.load_ui()

    def load_ui(self):
        '''Inicia la ventana'''
        self.setWindowTitle('DCCafé - Resumen Ronda')
        self.setStyleSheet(SUMMARY_THEME)
        # Grid principal
        main_layout = QGridLayout()
        self.setLayout(main_layout)
        # Bloque de información
        layout_card = QVBoxLayout()
        layout_card.addSpacing(30)
        self.card_summary = QFrame()
        self.card_summary.setLayout(layout_card)
        self.card_summary.setObjectName('card_summary')
        main_layout.addWidget(self.card_summary, 1, 1)
        # -> Título
        self.title = QLabel(self)
        self.title.setObjectName('title')
        self.title.setText('Resumen')
        self.title.setAlignment(Qt.AlignCenter)
        layout_card.addWidget(self.title)
        # -> Linea separadora
        self.line = QFrame(self)
        self.line.setObjectName('line')
        self.line.setFixedHeight(5)
        layout_card.addWidget(self.line)
        layout_card.addSpacing(50)
        # -> Resultados
        grid_results = QGridLayout()
        grid_results.setColumnStretch(0, 3)
        grid_results.setColumnStretch(1, 2)
        grid_results.setContentsMargins(*[80, 0] * 2)
        layout_card.addLayout(grid_results)
        # --> Clientes perdidos
        # label
        self.label_failed = QLabel('Clientes Perdidos', self)
        self.label_failed.setObjectName('label_failed')
        self.label_failed.setAlignment(Qt.AlignRight)
        grid_results.addWidget(self.label_failed, 0, 0)
        # valor
        self.failed = QLabel('2', self)
        self.failed.setObjectName('failed')
        self.failed.setAlignment(Qt.AlignRight)
        grid_results.addWidget(self.failed, 0, 1)
        # --> Clientes atendidos
        # label
        self.label_completed = QLabel('Clientes Atendidos', self)
        self.label_completed.setObjectName('label_completed')
        self.label_completed.setAlignment(Qt.AlignRight)
        grid_results.addWidget(self.label_completed, 1, 0)
        # valor
        self.completed = QLabel('12', self)
        self.completed.setObjectName('completed')
        self.completed.setAlignment(Qt.AlignRight)
        grid_results.addWidget(self.completed, 1, 1)
        # --> Dinero acumulado
        # label
        self.label_money = QLabel('Dinero Acumulado', self)
        self.label_money.setObjectName('label_money')
        self.label_money.setAlignment(Qt.AlignRight)
        grid_results.addWidget(self.label_money, 2, 0)
        # valor
        self.money = QLabel('$100000', self)
        self.money.setObjectName('money')
        self.money.setAlignment(Qt.AlignRight)
        grid_results.addWidget(self.money, 2, 1)
        # -> Reputación
        self.label_rep = QLabel('Reputación', self)
        self.label_rep.setObjectName('label_rep')
        self.label_rep.setAlignment(Qt.AlignCenter)
        layout_card.addSpacing(30)
        layout_card.addWidget(self.label_rep)
        # --> Estrellas
        stars_layout = QHBoxLayout()
        stars_layout.setContentsMargins(30, 0, 30, 0)
        self.star_filed = QPixmap(PATH['star']['filed'])
        self.star_empty = QPixmap(PATH['star']['empty'])
        self.estrellas = []
        for _ in range(5):
            star = QLabel()
            star.setFixedSize(40, 40)
            star.setScaledContents(True)
            stars_layout.addWidget(star)
            self.estrellas.append(star)
        layout_card.addLayout(stars_layout)
        # -> Botones
        button_layout = QHBoxLayout()
        layout_card.addSpacing(50)
        layout_card.addLayout(button_layout)
        # --> Salir
        self.quit = QPushButton('Salir', self)
        self.quit.setObjectName('quit')
        self.quit.setCursor(QCursor(Qt.PointingHandCursor))
        self.quit.pressed.connect(self.signal_exit_game)
        self.quit.pressed.connect(self.hide)
        button_layout.addWidget(self.quit)
        # --> Guardar
        self.save = QPushButton('Guardar', self)
        self.save.setObjectName('save')
        self.save.setCursor(QCursor(Qt.PointingHandCursor))
        self.save.pressed.connect(self.signal_save_game)
        button_layout.addWidget(self.save)
        # --> Continuar
        self.continue_ = QPushButton('Continuar', self)
        self.continue_.setObjectName('continue_')
        self.continue_.setCursor(QCursor(Qt.PointingHandCursor))
        self.continue_.pressed.connect(self.hide)
        self.continue_.pressed.connect(self.signal_continue_game)
        button_layout.addWidget(self.continue_)
        # -> Espacios
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 0, 1)
        main_layout.addItem(QSpacerItem(0, 0, vPolicy=QSizePolicy.Expanding), 2, 1)
        main_layout.addItem(QSpacerItem(0, 0, hPolicy=QSizePolicy.Expanding), 1, 0)
        main_layout.addItem(QSpacerItem(0, 0, hPolicy=QSizePolicy.Expanding), 1, 2)

    def round_title(self, n_ronda: int = 0) -> None:
        '''Actualiza el título de la ronda'''
        if not isinstance(n_ronda, int):
            raise TypeError(f'El número de la ronda {n_ronda.__repr__()} no es valido')
        self.title.setText(f'Resumen ronda {n_ronda}')

    def show_rep(self, rep: int) -> None:
        '''Muestra la reputacion con estrellas'''
        if rep.isnumeric():
            rep = int(rep)
        if not isinstance(rep, int) or not 0 <= rep <= 5:
            raise ValueError(f'La reputación {rep.__repr__()} no es un número entre 0 y 5')
        for indice in range(5):
            if rep > 0:
                self.estrellas[indice].setPixmap(self.estar_filedstrella_llena)
            else:
                self.estrellas[indice].setPixmap(self.estar_emptystrella_vacia)
            rep -= 1

    def show_results(self, results: dict) -> None:
        '''Carga los resultados y muestra la ventana'''
        self.round_title(int(results['round']))
        self.show_rep(results['rep'])
        self.completed.setText(results['completed_orders'])
        self.failed.setText(results['failed_orders'])
        self.money.setText(results['money'])
        self.show()
