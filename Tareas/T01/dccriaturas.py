from abc import ABC, abstractmethod
import random
import parametros as PMT

"""
TODO:
- Tengo que ver como utilizar valores predeterminados en
cada una de las clases.
- Revisar parámetors
"""


class DCCriaturas(ABC):
    """
    ===========
    DCCriaturas
    ===========
    Son las criaturas que cada Magizoólogo se dedica a cuidar.
    Todas las DCCriaturas pueden alimentarse, escapar e interactuar
    de forma negativa o positiva con su Magizoólogo.
    Poseen diversos atributos cuyos valores variarían según el tipo de criatura.

    Atributos
    ---------
    `nombre` : `str`
        Es el identificador único de cada criatura.
        No puede repetirse con ninguna criatura existente
        y debe estar estar formado exclusivamente por
        caracteres alfanuméricos, y sin distinción
        entre mayúsculas y minúsculas.
    `nivel_magico` : `int`
        Valor que indica cuán poderosa es la criatura.
        Este valor afecta en la cantidad de daño que
        puede hacer una criatura, en qué tan difícil
        es de capturar y en la cantidad de dinero que
        recibe el Magizoólogo por cuidarla. Varía de
        forma aleatoria y uniforme dentro de rangos
        específicos para cada nueva DCCriatura
    `vida_max` : `int`
        Valor que indica la cantidad de vida total que
        posee la DCCriatura. Varía de forma aleatoria
        y uniforme dentro de rangos específicos para
        cada nueva DCCriatura.
    `vida_actual` : `int`
        Valor que indica la cantidad de vida que posee
        la DCCriatura actualmente. Comienza como el
        valor de puntos de salud total. Su valor no
        puede superar los puntos de salud total,
        y tiene como valor mínimo 1.
    `prob_escaparse` : `float`
        Valor que indica la probabilidad base que tiene
        la criatura para escapar. Es distinto según tipo,
        algunas son mas propensas a permanecer junto a
        su amo, mientras que otras son más rebeldes.
        Se mantiene entre 0 y 1.
    `prob_enfermarse` : `float`
        Valor que indica la probabilidad base que tiene la
        criatura de enfermarse. Esta probabilidad varia por
        tipo de criatura y se mantiene entre 0 y 1.
    `enfermo` : `bool`
        Valor que indica si la criatura esta enferma o no.
        En caso de que una criatura se enferme debe ser
        sanada por su amo, de lo contrario, su salud
        disminuirá en 7 puntos por cada día
        que tenga esta condición.
    `nivel_hambre` : `str`
        Valor que indica el nivel de hambre de una criatura
        e influye en los puntos de salud de la misma criatura.
        Su valor puede ser "satisfecha" o "hambrienta". Se
        puede pasar de "satisfecha" a "hambrienta" si no se
        come en una cierta cantidad de días determinados por
        el tipo de cada criatura. Por otra parte se puede
        pasar de "hambrienta" a "satisfecha" si la criatura
        consume alguno de los alimentos que se detallan en
        Alimentos. Por cada día que una criatura esté
        "hambrienta" perderá 3 puntos de salud.
    `dias_ultima_comida` : `int`
        Valor que representa la cantidad de
        días que lleva sin comer la criatura.
    `agresividad` : `str`
        Indica el nivel de agresividad de una criatura e
        influye en la probabilidad de que la criatura ataque
        al Magizoólogo al momento de que este le da alimentos.
        Puede ser "inofensiva", "arisca" o "peligrosa".

    Acciones (Métodos)
    ------------------
        `alimentarse()`
        `escaparse()`
        `enfermarse()`
        `caracteristica_unica()`
    """
    def __init__(self,
                 nombre,
                 nivel_magico=None,
                 prob_escaparse=None,
                 prob_enfermarse=None,
                 enferma=None,
                 escapado=None,
                 vida_max=None,
                 vida_actual=None,
                 nivel_hambre=None,
                 agresividad=None,
                 dias_sin_comer=None,
                 tiempo_satisfecha=None,
                 **kwargs):
        # -------------- #
        # Valores únicos #
        # -------------- #
        self.nombre = str(nombre)
        self.tipo = type(self).__name__

        # ------------------------------------------ #
        # Valores predeterminados en las DCCriaturas #
        # ------------------------------------------ #
        if vida_actual is None:
            vida_actual = vida_max
        if escapado is None:
            escapado = "False"
        if enferma is None:
            enferma = "False"
        if nivel_hambre is None:
            nivel_hambre = "satisfecha"
        if dias_sin_comer is None:
            dias_sin_comer = "0"
        # Transformación de valores
        self.vida_actual = int(vida_actual)
        self.escapado = escapado == "True"
        self.enferma = enferma == "True"
        self.nivel_hambre = str(nivel_hambre)
        self.dias_sin_comer = int(dias_sin_comer)

        # ------------------------------------------------ #
        # Valores predeterminados en distintas DCCriaturas #
        # ------------------------------------------------ #
        self.nivel_magico = int(nivel_magico)
        self.prob_escape = float(prob_escaparse)
        self.prob_enfermarse = float(prob_enfermarse)
        self.vida_max = int(vida_max)
        self.tiempo_satisfecha = int(tiempo_satisfecha)
        self.agresividad = str(agresividad)

    def __str__(self):
        return self.nombre

    def __eq__(self, value):
        return value

    def __repr__(self):
        return "|".join([
                f"{type(self).__name__} '{self.nombre}':",
                f"nivel mágico ={self.nivel_magico}",
                f"vida = {self.vida_actual}",
                f"nivel hambre={self.nivel_hambre}",
                ])

    def alimentarse(self, magizoologo):
        """
        Magizoólogo alimenta a la criatura.
        """
        valor = (PMT.ALIMENTARSE_EFECTO_HAMBRE[self.nivel_hambre]
                 + PMT.ALIMENTARSE_EFECTO_AGRESIVIDAD[self.agresividad])
        probabilidad_atacar = min(1, valor/100)
        if probabilidad_atacar >= random.random():
            daño = max(0, magizoologo.nivel_magico - self.nivel_magico)
            magizoologo.energia_actual -= daño

    def escaparse(self, resp_magizoologo):
        """
        Las DCCriaturas tienden a ser un poco inquietas y suelen intentar
        escaparse, sobre todo si están hambrientas pues intentaran
        conseguir alimento por sus propias manos.
        """
        # Formulas en TODO
        efecto_hambre = PMT.ESCAPARSE_EFECTO_HAMBRE
        valor = (efecto_hambre[self.nivel_hambre] - resp_magizoologo)/100
        prob = min(1, self.prob_escape + max(0, valor))
        if prob >= random.random():
            # Se escapa
            self.escapado = True
            # Retorna que sí se escapó
            return True
        # Retorna que no se escapó
        return False

    def enfermarse(self, resp_magizoologo):
        """
        Las DCCriaturas corren el constante riesgo de enfermarse.
        """
        valor = (self.vida_max - self.vida_actual)/self.vida_max - resp_magizoologo/100
        prob = min(1, self.prob_enfermarse + max(0, valor))
        if prob >= random.random():
            # Se enferma
            self.enferma = True
            # Retorna que sí se enfermó
            return True
        # Retora que no se enfermó
        return False

    @abstractmethod
    def caracteristica_unica(self):
        """
        Caracteristica única de cada DCCriatura, la que define
        si esta realiza una acción especial al comienzo del día.
        """
        pass


class Augurey(DCCriaturas):
    """
    Pájaro delgado, pequeño y triste, con plumaje brillante.
    Es capaz de predecir la lluvia con muchos días de anticipación y
    le gusta volar solo cuando esta bien cuidado.
    Es poco probable que ataque a su dueño.
    """
    def __init__(self, nombre, **kwargs):
        # Predeterminados #
        if "nivel_magico" not in kwargs:
            kwargs["nivel_magico"] = random.randint(*PMT.AUGUREY_RANGO_NIVEL_MAGICO)
        if "prob_escaparse" not in kwargs:
            kwargs["prob_escaparse"] = PMT.AUGUREY_PROB_ESCAPARSE
        if "prob_enfermarse" not in kwargs:
            kwargs["prob_enfermarse"] = PMT.AUGUREY_PROP_ENFERMARSE
        if "vida_max" not in kwargs:
            kwargs["vida_max"] = random.randint(*PMT.AUGUREY_RANGO_VIDA_MAXIMA)
        if "tiempo_satisfecha" not in kwargs:
            kwargs["tiempo_satisfecha"] = PMT.AUGUREY_TIEMPO_SATISFECHA
        if "agresividad" not in kwargs:
            kwargs["agresividad"] = PMT.AUGUREY_NIVEL_AGRESIVIDAD
        # Inicia la clase
        super().__init__(nombre, **kwargs)

    def alimentarse(self):
        pass

    def caracteristica_unica(self):
        pass


class Niffler(DCCriaturas):
    """
    Criatura pequeña, de pelaje sedoso y hocico
    largo, similar a un ornitorrinco.
    Es increíblemente inquieto y le encantan las cosas brillantes,
    por lo que suele robar Sickles para luego guardarlos en su pelaje.
    Tiende a ser agresivo.
    """
    def __init__(self, nombre, **kwargs):
        # Predeterminados #
        if "nivel_magico" not in kwargs:
            kwargs["nivel_magico"] = random.randint(*PMT.NIFFLER_RANGO_NIVEL_MAGICO)
        if "prob_escaparse" not in kwargs:
            kwargs["prob_escaparse"] = PMT.NIFFLER_PROB_ESCAPARSE
        if "prob_enfermarse" not in kwargs:
            kwargs["prob_enfermarse"] = PMT.NIFFLER_PROP_ENFERMARSE
        if "vida_max" not in kwargs:
            kwargs["vida_max"] = random.randint(*PMT.NIFFLER_RANGO_VIDA_MAXIMA)
        if "tiempo_satisfecha" not in kwargs:
            kwargs["tiempo_satisfecha"] = PMT.NIFFLER_TIEMPO_SATISFECHA
        if "agresividad" not in kwargs:
            kwargs["agresividad"] = PMT.NIFFLER_NIVEL_AGRESIVIDAD
        # Atributo único
        if "nivel_cleptomania" not in kwargs:
            self.nivel_cleptomania = random.randint(*PMT.NIFFLER_RANGO_CLEPTOMANIA)
        else:
            self.nivel_cleptomania = int(kwargs["nivel_cleptomania"])
        # Inicia la clase
        super().__init__(nombre, **kwargs)

    def alimentarse(self):
        pass

    def caracteristica_unica(self):
        pass


class Erkling(DCCriaturas):
    """
    Las criaturas más peligrosas de todas.
    Con un parecido a los elfos, suelen parecer desapercibidos,
    pero son violentos.
    """
    def __init__(self, nombre, **kwargs):
        # Predeterminados #
        if "nivel_magico" not in kwargs:
            kwargs["nivel_magico"] = random.randint(*PMT.ERKLING_RANGO_NIVEL_MAGICO)
        if "prob_escaparse" not in kwargs:
            kwargs["prob_escaparse"] = PMT.ERKLING_PROB_ESCAPARSE
        if "prob_enfermarse" not in kwargs:
            kwargs["prob_enfermarse"] = PMT.ERKLING_PROP_ENFERMARSE
        if "vida_max" not in kwargs:
            kwargs["vida_max"] = random.randint(*PMT.ERKLING_RANGO_VIDA_MAXIMA)
        if "tiempo_satisfecha" not in kwargs:
            kwargs["tiempo_satisfecha"] = PMT.ERKLING_TIEMPO_SATISFECHA
        if "agresividad" not in kwargs:
            kwargs["agresividad"] = PMT.ERKLING_NIVEL_AGRESIVIDAD
        # Inicia la clase
        super().__init__(nombre, **kwargs)

    def alimentarse(self):
        pass

    def caracteristica_unica(self):
        pass


if __name__ == "__main__":
    x = Erkling("augerrrrey")
    y = Niffler("augerrrrey")
    z = Augurey("augerrrrey")
    print(x.__repr__())
    print(y.__repr__())
    print(z.__repr__())
