import os
import random
import types
from threading import Thread, Lock
from time import sleep

from cargar_tweets import cargar_tweets
from parametros import ENOJO_INICIAL, PROBABILIDAD_DESAPARECER, PROBABILIDAD_HACKEO

# Lock para evitar que lideres se manden tweets al mismo tiempo
lock_tweet_lideres = Lock()


class LiderMundial(Thread):

    def __init__(self, nombre, tweets, enojo, reloj):
        # Completar
        super().__init__(daemon=True)  # Creado como daemon directamente

        # No modificar
        self.nombre = nombre
        self.tweets = tweets
        self._enojo = enojo
        self.reloj = reloj
        self.puede_twitear = True
        random.shuffle(self.tweets)

    @property
    def enojo(self):
        return self._enojo

    @enojo.setter
    def enojo(self, value):
        if value < 0:
            value = 0
        self._enojo = value

    def run(self):
        # Completar o modificar si es necesario
        while self.puede_twitear:
            self.twitear()
            sleep(max(5 * (1.05)**(-self.enojo), 0.25))

    def twitear(self):
        # Completar o modificar si es necesario
        with lock_tweet_lideres:
            tweet = random.choice(self.tweets)  # Named tuple
            print(f'{self.nombre}: {tweet.texto}')
            self.enojo += tweet.enojo
            self.reloj.acelerar(self.nombre, self.enojo)



class Hacker(LiderMundial, Thread):

    def __init__(self, nombre, trumpzini, dr_pinto, reloj):
        # No modificar
        Thread.__init__(self)
        self.daemon = True
        self.nombre = nombre
        self.trumpzini = trumpzini
        self.dr_pinto = dr_pinto
        self.reloj = reloj

    def run(self):
        while self.reloj.quedan_lideres:
            # Completar
            with lock_tweet_lideres:
                if PROBABILIDAD_HACKEO > random.random() and self.trumpzini.puede_twitear:
                    self.trumpzini.puede_twitear = False
                    print(f'{self.nombre} ha hackeado el teléfono de Trumpzini!')
                    print('Trumpzini ya no podrá seguir twiteando :(')
                if PROBABILIDAD_DESAPARECER > random.random() and self.dr_pinto.puede_twitear:
                    self.dr_pinto.puede_twitear = False
                    print(f'{self.nombre} ha boicoteado la cirugía de Dr. Pin Tong-Um!')
                    print('Dr. Pin Tong-Um ya no podrá seguir twiteando :(')

            # No modificar
            if not self.trumpzini.puede_twitear and not self.dr_pinto.puede_twitear:
                self.reloj.quedan_lideres = False
            sleep(0.5)

        print("Se ha detenido el Doomsday Clock")


if __name__ == "__main__":
    # Instanciamos al lider mundial
    tweets_pinto = cargar_tweets(os.path.join("datos", "pin_tweets.csv"))
    lider_de_prueba = LiderMundial("Dr. Pin Tong-Un", tweets_pinto, ENOJO_INICIAL, None)

    # Ahora necesitamos un reloj que maneje al lider mundial
    # Necesitamos una función que corra al empezar el thread
    def probar_reloj(lider):
        while lider.enojo < 50:
            sleep(0.1)
        print(f"{lider.nombre} se enojó tanto que se rompió el reloj :(.")

    # Se crea un thread que representará al reloj
    reloj_de_prueba = Thread(target=probar_reloj, args=(lider_de_prueba,))

    # Además, el reloj necesita un método acelerar para funcionar dentro de LiderMundial
    acelerar = lambda reloj, nombre, enojo: print(f"{nombre} ha acelerado el reloj por {enojo / 10}.")
    reloj_de_prueba.acelerar = types.MethodType(acelerar, reloj_de_prueba)

    # Le pasamos el reloj creado al lider mundial
    lider_de_prueba.reloj = reloj_de_prueba

    # Empezamos los threads!
    print("Iniciando prueba...")
    reloj_de_prueba.start()
    lider_de_prueba.start()
    reloj_de_prueba.join()

    if not lider_de_prueba.daemon:
        print(f"{lider_de_prueba.nombre} está twitteando sin control!")
