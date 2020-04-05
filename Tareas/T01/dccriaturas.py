from abc import ABC, abstractmethod
import random

"""
TODO:
- Tengo que ver como utilizar valorespredeterminados en
cada una de las clases.
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
    `prob_escape` : `float`
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
    def __init__(self, nombre, nivel_magico, prob_escape, prop_enfermarse,
                 enferma, escapado, vida_max, vida_actual, nivel_hambre,
                 dias_sin_comer, agresividad, tiempo_satisfecha):
        self.nombre = str(nombre)
        # Tipo definido por subclase --> type(self).__name__
        # -- Valores predeterminados en distintas DCCriaturas -- #
        self.nivel_magico = int(nivel_magico)
        self.prob_escape = float(prob_escape)
        self.prob_enfermarse = float(prop_enfermarse)
        self.vida_max = int(vida_max)
        self.tiempo_satisfecha = int(tiempo_satisfecha)
        self.agresividad = str(agresividad)
        # -- Valores predeterminados en todas lass DCCriaturas -- #
        # predeterminado = {
        #     "vida_actual": self.vida_max,
        #     "escapado": False,
        #     "enferma": False,
        #     "nivel_hambre": "satisfecha",
        #     "dias_sin_comer": 0
        # }
        self.vida_actual = int(vida_actual)
        self.escapado = bool(escapado)
        self.enferma = bool(enferma)
        self.nivel_hambre = str(nivel_hambre)
        self.dias_ultima_comida = int(dias_sin_comer)

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f"{type(self).__name__} {self.nombre}: vida={self.vida_actual}"

    @abstractmethod
    def alimentarse(self):
        """
        Todas las DCCriaturas comen al momento de que su Magizoólogo
        les da alimentos. Las DCCriaturas que estén "hambrientas" y
        sean alimentadas pasarán a estar "satisfechas". Por otro lado,
        a la hora de comer existe una posibilidad de que la criatura
        ataque al Magizoólogo y pierda puntos de su energía actual.
        """
        # Formulas en TODO
        pass

    def escaparse(self, resp_magizoologo):
        """
        Las DCCriaturas tienden a ser un poco inquietas y suelen intentar
        escaparse, sobre todo si están hambrientas pues intentaran
        conseguir alimento por sus propias manos.
        """
        # Formulas en TODO
        efecto_hambre = {"satisfecha": 0, "hambrienta": 20}
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
    def __init__(self, **kwargs):
        # predeterminado = {
        #     "nivel_magico": random.randint(20, 50),
        #     "prob_escarse": 0.2,
        #     "prob_enfermarse": 0.3,
        #     "vida_max": random.randint(35, 45),
        #     "tiempo_satisfecha": 3,
        #     "nivel_agresividad": "inofensiva",
        # }
        super().__init__()

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
    def __init__(self, **kwargs):
        # predeterminado = {
        #     "nivel_magico": random.randint(10, 20),
        #     "prob_escarse": 0.3,
        #     "prob_enfermarse": 0.2,
        #     "vida_max": random.randint(20, 30),
        #     "tiempo_satisfecha": 2,
        #     "nivel_agresividad": "arisca",
        # }
        super().__init__()

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
    def __init__(self, **kwargs):
        # predeterminado = {
        #     "nivel_magico": random.randint(30, 45),
        #     "prob_escarse": 0.5,
        #     "prob_enfermarse": 0.3,
        #     "vida_max": random.randint(50, 60),
        #     "tiempo_satisfecha": 2,
        #     "nivel_agresividad": "peligrosa",
        #     "nivel_cleptomania": random.randint(5, 10),
        # }
        super().__init__()

    def alimentarse(self):
        pass

    def caracteristica_unica(self):
        pass
