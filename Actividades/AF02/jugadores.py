from abc import ABC, abstractmethod
import random


class Jugador(ABC):
    def __init__(self, nombre, equipo, especialidad, energia):
        self.nombre = nombre
        self.equipo = equipo
        self.especialidad = especialidad
        self.energia = int(energia)

        self.audacia = 3
        self.inteligencia = 3
        self.nerviosismo = 3
        self.trampa = 3

    def __str__(self):
        if self.equipo == 'ayudante':
            return f'Ayudante {self.nombre} ({self.especialidad})'
        return f'Alumno(a) {self.nombre} ({self.especialidad})'

    def __repr__(self):
        return (f'({type(self).__name__}) {self.nombre}: '
                f'equipo={self.equipo}|'
                f'energia={self.energia}|'
                f'inteligencia={self.inteligencia}|'
                f'audacia={self.audacia}|'
                f'trampa={self.trampa}|'
                f'nerviosismo={self.nerviosismo}')

    @abstractmethod
    def enfrentar(self, tipo_de_juego, enemigo):
        print(f"{self}: ¡Desafió a {enemigo} a un {tipo_de_juego}!")


class JugadorMesa(Jugador):
    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
        self.nerviosismo = min(self.energia, random.randint(0, 3))

    def jugar_mesa(self, enemigo):
        if self.nerviosismo < enemigo.nerviosismo:
            return True
        return False


class JugadorCartas(Jugador):
    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
        self.inteligencia = self.energia * 2.5

    def jugar_cartas(self, enemigo):
        if self.inteligencia > enemigo.inteligencia:
            return True
        return False


class JugadorCombate(Jugador):
    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
        self.audacia = max(self.energia, random.randint(3, 5))

    def jugar_combate(self, enemigo):
        if self.audacia > enemigo.audacia:
            return True
        return False


class JugadorCarreras(Jugador):
    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
        self.trampa = self.energia * 3

    def jugar_carrera(self, enemigo):
        if self.trampa > enemigo.trampa:
            return True
        return False


class JugadorInteligente(JugadorMesa, JugadorCartas):
    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)


class JugadorIntrepido(JugadorCarreras, JugadorCombate):
    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
