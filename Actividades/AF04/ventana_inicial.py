import sys

from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, \
    QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication

from parametros import ruta_logo


class VentanaInicial(QWidget):

    # Esta señal es para enviar un intento de nombre de usuario
    senal_revisar_nombre = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)
        self.crear_pantalla()


    def crear_pantalla(self):
        # Aqui deben crear la pantalla.
        self.setWindowTitle("Ventana Inicial DCCuent")
        # El logo, la caja de texto y el botón.
        # IMPORTANTE la caja de texto debe llamarse input_usuario
        # Si usas layout recuerda agregar los labels al layout y finalmente setear el layout
        columna_principal = QVBoxLayout(self)

        self.logo = QLabel(self)
        self.logo.setFixedSize(400, 400)
        self.logo.setPixmap(QPixmap(ruta_logo))
        columna_principal.addWidget(self.logo)

        # Inicio fila input
        fila_usuario = QHBoxLayout()

        self.etiqueta_usuario = QLabel('Ingrese su nombre de usuario:', self)
        fila_usuario.addWidget(self.etiqueta_usuario)

        self.input_usuario = QLineEdit(self)
        self.input_usuario.setPlaceholderText("usuario")
        fila_usuario.addWidget(self.input_usuario)

        columna_principal.addLayout(fila_usuario)
        # Fin fila input

        self.boton = QPushButton('Ingresar', self)
        self.boton.clicked.connect(self.revisar_input)
        columna_principal.addWidget(self.boton)

        self.setLayout(columna_principal)

    def revisar_input(self):
        # Aquí deben enviar el nombre de usuario, para verificar si es un usuario valido
        # Para esto utilizar senal_revisar_nombre
        usuario = self.input_usuario.text()
        self.senal_revisar_nombre.emit(usuario)



    def recibir_revision(self, error):
        # Resetea la ventana si es que ocurre algun error,en caso contrario comienza el juego
        # IMPORTANTE la caja de text debe llamarse input_usuario
        if error:
            self.input_usuario.clear()
            self.input_usuario.setPlaceholderText("¡Inválido! Debe ser alfa-numérico.")
        else:
            usuario = self.input_usuario.text()
            self.hide()


if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    a = QApplication(sys.argv)
    ventana_inicial = VentanaInicial()

    ventana_inicial.show()
    sys.exit(a.exec())
