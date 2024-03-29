import os
from threading import Thread
from time import sleep

from cargar_tweets import cargar_tweets
from parametros import BOMBA_NUCLEAR, TIEMPO_INICIAL, VELOCIDAD_INICIAL, TADA


class DoomsdayClock(Thread):

    def __init__(self, velocidad, tiempo_restante):
        # Completar
        super().__init__()

        # No modificar siguientes líneas
        self.velocidad = velocidad
        self._tiempo_restante = tiempo_restante
        self.quedan_lideres = True

    @property
    def tiempo_restante(self):
        return self._tiempo_restante

    @tiempo_restante.setter
    def tiempo_restante(self, value):
        if value < 0:
            value = 0
        self._tiempo_restante = value

    def contar(self):
        self.tiempo_restante -= 1
        if not self.tiempo_restante:
            print("12:00")
        elif (self.tiempo_restante % 5 == 0 or self.tiempo_restante < 5):
            print(f"11:{60 - self.tiempo_restante}")

    def run(self):
        # Completar o modificar si es necesario
        while self.tiempo_restante and self.quedan_lideres:
            self.contar()  # Avanza
            sleep(1/self.velocidad)

        # No modificar siguientes líneas
        if self.tiempo_restante == 0 and self.quedan_lideres:
            print(BOMBA_NUCLEAR)
        else:
            print("Se ha detenido el Doomsday Clock")
            print(TADA)

    def acelerar(self, nombre, enojo):
        # Completar o modificar si es necesario
        cambio_velocidad = enojo / 10
        print(f"{nombre} ha acelerado el reloj en {cambio_velocidad}")
        self.velocidad += cambio_velocidad


if __name__ == "__main__":
    # Creamos una instancia de prueba
    reloj_de_prueba = DoomsdayClock(VELOCIDAD_INICIAL, TIEMPO_INICIAL)
    tweets_trumpzini = cargar_tweets(os.path.join("datos", "trumpzini_tweets.csv"))
    # Puedes empezar el thread de reloj_de_prueba aqui:
    reloj_de_prueba.start()
    # Con esto podremos ver si tu reloj se acelera y si esta funcionando bien
    for tweet in tweets_trumpzini:
        if reloj_de_prueba.tiempo_restante > 1:
            reloj_de_prueba.acelerar("Persona de prueba", tweet.enojo)
            print(f"Velocidad actual: {reloj_de_prueba.velocidad}")
            print(f"Minutos hasta la medianoche: {reloj_de_prueba.tiempo_restante}")
            sleep(1)
