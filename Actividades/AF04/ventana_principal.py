import os
import sys
from random import choice

from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, \
    QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication


class VentanaPrincipal(QWidget):

    # Aquí debes crear una señal que usaras para enviar la jugada al back-end
    senal_enviar_jugada = pyqtSignal(dict)

    def __init__(self, *args):
        super().__init__(*args)
        self.crear_pantalla()


    def crear_pantalla(self):
        # Aquí deben crear la ventana vacia.
        self.setWindowTitle("DCCuent")
        # Es decir, agregar y crear labels respectivos a datos del juego, pero sin contenido
        # Si usas layout recuerda agregar los labels al layout y finalmente setear el layout

        main_layout = QGridLayout()

        self.nombre_usuario = QLabel('Usuario:', self)
        main_layout.addWidget(self.nombre_usuario, 0, 0)
        self.victorias = QLabel('Victorias', self)
        main_layout.addWidget(self.victorias, 0, 1)
        self.derrotas = QLabel('Derrotas', self)
        main_layout.addWidget(self.derrotas, 0, 2)

        self.tecla_infanteria = QLabel('Q', self)
        main_layout.addWidget(self.tecla_infanteria, 1, 0)
        self.tecla_rango = QLabel('W', self)
        main_layout.addWidget(self.tecla_rango, 1, 1)
        self.tecla_artilleria = QLabel('E', self)
        main_layout.addWidget(self.tecla_artilleria, 1, 2)

        self.carta_infanteria = QLabel(self)
        self.carta_infanteria.setFixedSize(238, 452)
        # pixmap_infanteria = QPixmap()
        # self.carta_infanteria.setPixmap(pixmap_infanteria)
        main_layout.addWidget(self.carta_infanteria, 2, 0)

        self.carta_rango = QLabel(self)
        self.carta_rango.setFixedSize(238, 452)
        # pixmap_rango = QPixmap()
        # self.carta_rango.setPixmap(pixmap_rango)
        main_layout.addWidget(self.carta_rango, 2, 1)

        self.carta_artilleria = QLabel(self)
        self.carta_artilleria.setFixedSize(238, 452)
        # pixmap_artilleria = QPixmap()
        # self.carta_artilleria.setPixmap(pixmap_artilleria)
        main_layout.addWidget(self.carta_artilleria, 2, 2)

        self.setLayout(main_layout)


    def actualizar(self, datos):
        # Esta es la funcion que se encarga de actualizar el contenido de la ventana y abrirla
        # Recibe las nuevas cartas y la puntuación actual en un diccionario

        # Al final, se muestra la ventana.
        self.show()

    def keyPressEvent(self, evento):
        # Aquí debes capturar la techa apretara,
        # y enviar la carta que es elegida
        pass


class VentanaCombate(QWidget):

    # Esta señal es para volver a la VentanaPrincipal con los datos actualizados
    senal_regresar = pyqtSignal(dict)
    # Esta señal envia a la ventana final con el resultado del juego
    senal_abrir_ventana_final = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)
        self.crear_pantalla()

    def crear_pantalla(self):
        self.setWindowTitle("DCCuent")
        self.vbox = QVBoxLayout()
        self.layout_principal = QHBoxLayout()
        self.label_carta_usuario = QLabel()
        self.label_victoria = QLabel()
        self.label_carta_enemiga = QLabel()
        self.boton_regresar = QPushButton("Regresar")

        self.layout_principal.addWidget(self.label_carta_usuario)
        self.layout_principal.addWidget(self.label_victoria)
        self.layout_principal.addWidget(self.label_carta_enemiga)

        self.boton_regresar.clicked.connect(self.regresar)
        self.vbox.addLayout(self.layout_principal)
        self.vbox.addWidget(self.boton_regresar)

        self.setLayout(self.vbox)

    def mostrar_resultado_ronda(self, datos):
        self.datos = datos
        mensaje = datos["mensaje"]
        carta_enemiga = datos["enemigo"]
        carta_jugador = datos["jugador"]
        self.label_carta_usuario.setPixmap(QPixmap(carta_jugador["ruta"]).scaled(238,452))
        self.label_carta_enemiga.setPixmap(QPixmap(carta_enemiga["ruta"]).scaled(238,452))
        self.label_victoria.setText(mensaje)
        self.show()

    def regresar(self):
        resultado = self.datos["resultado"]
        if resultado == "victoria" or resultado == "derrota":
            self.senal_abrir_ventana_final.emit(resultado)
        else:
            self.senal_regresar.emit(self.datos)
        self.hide()


if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    a = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()

    ventana_principal.show()
    sys.exit(a.exec())
