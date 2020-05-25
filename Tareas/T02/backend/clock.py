'''
Clase GameClock que permite manejar el tiempo del juego.
'''
# Es más eficiente QTimer que QThread ya que *no es un thread aparte*,
# se ejecuta junto al main loop del programa. Además, el uso es más sencillo.

from PyQt5.QtCore import QTimer


class GameClockError(Exception):
    '''Error mostrado en el mal manejo del reloj'''


class GameClock(QTimer):
    '''
    Implementación de un QTimer con un método de pausa y continuar,
    además de la posibilidad de añadir un número de repeticiones y
    eventos al terminar las repeticiones, pararlo o continuarlo.

    El evento principal también es llamado al iniciar el reloj.
    '''
    def __init__(self, event=None, interval: int = 1, rep: int = -1,
                 final_event=None, paused_event=None, continue_event=None):
        '''
        Parámetros:
            event, final_event, paused_event, continue_event
        Evaluable (función o método)
            interval
        Tiempo en segundos en el que se realiza el evento principal
            rep
        Repeticiones que realiza el reloj.
        Por defecto se repite indefinidamente
        '''
        super().__init__()
        # Parámetros
        self._counter = rep
        self._interval = interval * 1000
        self._remaining_time = False
        self.__started = False
        # Eventos
        self._event = event
        self._final_event = final_event
        self._paused_event = paused_event
        self._continue_event = continue_event
        # QTimer setup
        self.setInterval(self._interval)
        self.timeout.connect(self.__call_event)

    def start(self, *args):
        '''Overrite de start. Ejecuta el evento si es que tiene uno.'''
        if not self.__started and self._event:
            self.__started = True
            self._event()
        super().start(*args)

    def is_paused(self) -> bool:
        '''Verifica que si el reloj esta pausado'''
        return not self._remaining_time

    def set_rep(self, value: int) -> None:
        '''Redefine el número de repeticiones que realiza el reloj'''
        if not self.isActive():
            self._counter = value

    def pause_(self) -> None:
        '''Pausa el reloj'''
        if not self.isActive():
            raise GameClockError('El reloj está pausado o no ha empezado')
        else:
            self._remaining_time = self.remainingTime()
            if self._paused_event:
                self._paused_event()
            self.stop()

    def continue_(self) -> None:
        '''Continua el reloj'''
        if self.isActive():
            raise GameClockError('El reloj ya está activo')
        else:
            if self._continue_event:
                self._continue_event()
            self.start(self._remaining_time)

    def __call_event(self):
        '''
        En vez de llamar al evento directamente, el GameClock
        realiza unos procesos antes para permitir la pausa, la
        limitación de iteraciones y poder llamar a un método final.
        '''
        # Disminuye el contador en uno si es que el contador es mayor que 0
        if self._counter != -1:
            self._counter -= 1
        # Vuelve nuevamente al tiempo normal si es que se pausó
        if self._remaining_time:
            self.setInterval(self._interval)
            self._remaining_time = False
        # Ejecuta el evento si es que existe
        if self._event:
            self._event()
        # Al terminar las repeticiones ejecuta el evento final si es que existe
        if not self._counter:
            if self._final_event:
                self._final_event()
            self.stop()



if __name__ == "__main__":
    # Ejemplo del funcionamiento de GameClock
    # ---------------------------------------
    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
    import sys

    sys.__excepthook__ = lambda t, v, trace: print(t, v, trace, sep="\n")
    APP = QApplication(sys.argv)

    EVENT = lambda: print('Hola! Terminé un ciclo de 5 segundos')
    FINAL_EVENT = lambda: print('Me voy')
    PAUSE_EVENT = lambda: print('Esperando...')
    CONTINUE_EVENT = lambda: print('Aquí volví')

    TEST = GameClock(
        event=EVENT,
        interval=5,
        rep=10,
        final_event=FINAL_EVENT,
        paused_event=PAUSE_EVENT,
        continue_event=CONTINUE_EVENT
    )

    WIDGET = QWidget()
    LAYOUT = QGridLayout()
    WIDGET.setLayout(LAYOUT)

    PAUSE_BUTTON = QPushButton('pause', WIDGET)
    CONTINUE_BUTTON = QPushButton('continue', WIDGET)

    PAUSE_BUTTON.pressed.connect(TEST.pause_)
    CONTINUE_BUTTON.pressed.connect(TEST.continue_)

    LAYOUT.addWidget(PAUSE_BUTTON)
    LAYOUT.addWidget(CONTINUE_BUTTON)

    WIDGET.show()
    TEST.start()

    sys.exit(APP.exec_())
