"""
=====================
Clases de DCCriaturas
=====================
Contiene las Clases:
--------------------
    DCCriaturas
    Augurey
    Niffler
    Erkling
Depende de:
-----------
    parametros
    alimentos
"""

from abc import ABC, abstractmethod
import random

import parametros as PMT
import alimentos as alm


def retornar_clase_criatura(tipo_criatura: str):
    """
    Retorna la clase de la criatura
    """
    tipo_criatura = tipo_criatura.lower()
    for a, b in zip("áéíúóñ", "aeioun"):
        tipo_criatura = tipo_criatura.replace(a, b)
    tipos = {
        "augurey": Augurey,
        "erkling": Erkling,
        "niffler": Niffler,
    }
    if tipo_criatura in tipos:
        return tipos[tipo_criatura]


class DCCriaturas(ABC):
    """
    ===========
    DCCriaturas
    ===========
    Son las criaturas que cada Magizoólogo se dedica a cuidar.
    Todas las DCCriaturas pueden alimentarse, escapar e interactuar
    de forma negativa o positiva con su Magizoólogo.
    Poseen diversos atributos cuyos valores variarían según el tipo de criatura.
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
                 nivel_cleptomania=None,
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
        self.__vida_actual = int(vida_actual)
        self.escapado = escapado == "True"
        self.enferma = enferma == "True"
        self.nivel_hambre = str(nivel_hambre)
        self.__dias_sin_comer = int(dias_sin_comer)

        # ------------------------------------------------ #
        # Valores predeterminados en distintas DCCriaturas #
        # ------------------------------------------------ #
        self.tiempo_satisfecha = kwargs["tiempo_satisfecha"]
        self.nivel_magico = int(nivel_magico)
        self.prob_escaparse = float(prob_escaparse)
        self.prob_enfermarse = float(prob_enfermarse)
        self.vida_max = int(vida_max)
        self.agresividad = str(agresividad)
        # Atributos especiales #
        if nivel_cleptomania is None:
            nivel_cleptomania = 0
        self.nivel_cleptomania = int(nivel_cleptomania)

    def __str__(self):
        return self.nombre

    def __eq__(self, value):
        if type(value) is str:
            value = value.lower()
        return self.nombre.lower() == value

    def __repr__(self):
        return f"{self} en {id(self)}"

    @property
    def dias_sin_comer(self):
        return self.__dias_sin_comer

    @dias_sin_comer.setter
    def dias_sin_comer(self, value):
        self.__dias_sin_comer = value
        if self.__dias_sin_comer > self.tiempo_satisfecha:
            self.nivel_hambre = "hambrienta"
        elif not self.__dias_sin_comer:
            self.nivel_hambre = "satisfecha"

    @property
    def vida_actual(self):
        return self.__vida_actual

    @vida_actual.setter
    def vida_actual(self, value):
        if value > self.vida_max:
            self.__vida_actual = self.vida_max
        elif value < 1:
            self.__vida_actual = 1
        else:
            self.__vida_actual = value

    def alimentarse(self, alimento, magizoologo):
        """
        Magizoólogo alimenta a la criatura.

        Retorna la criatura si se alimento y
        False en el caso contrario.
        """
        # Inicio ataque
        valor = (PMT.ALIMENTARSE_EFECTO_HAMBRE[self.nivel_hambre]
                 + PMT.ALIMENTARSE_EFECTO_AGRESIVIDAD[self.agresividad])
        probabilidad_atacar = min(1, valor/100)
        if probabilidad_atacar >= random.random():
            daño = max(0, magizoologo.nivel_magico - self.nivel_magico)
            print(f"{self} te ha atacado! Perdiste {daño} de energía")
            magizoologo.energia_actual -= daño
        # Características especiales de los alimentos
        if type(alimento) is alm.TartaMelaza:
            if type(self) is Niffler:
                print(f"el {alimento} ha pacificado a {self}!")
                if 0.15 > random.random():
                    self.agresividad = "inofensiva"
        elif type(alimento) is alm.HigadoDragon:
            print(f"El {alimento} ha sanado a tu criatura!")
            self.enferma = False
        elif type(alimento) is alm.BunueloGusarajo:
            if 0.35 > random.random():
                print("La criatura ha rechazado el alimento!")
                return False  # Retorna False --> No se consumió el alimento
        # Alimentarse
        self.vida_actual += alimento.pnt_vida
        self.dias_sin_comer = 0
        print(f"{self} ha consumido el {alimento} "
              f"y ha recuperado {alimento.pnt_vida} de vida")
        return self

    def escaparse(self, resp_magizoologo):
        """
        Las DCCriaturas tienden a ser un poco inquietas y suelen intentar
        escaparse, sobre todo si están hambrientas pues intentaran
        conseguir alimento por sus propias manos.
        """
        # Formulas en TODO
        if not self.escapado:
            efecto_hambre = PMT.ESCAPARSE_EFECTO_HAMBRE
            valor = (efecto_hambre[self.nivel_hambre] - resp_magizoologo)/100
            prob = min(1, self.prob_escaparse + max(0, valor))
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
        if not self.enferma:
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
    def caracteristica_unica(self, magizoologo):
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

    def caracteristica_unica(self, magizoologo):
        if (self.nivel_hambre == "satisfecha"
                and not self.enferma
                and self.vida_actual == self.vida_max):
            ofrenda = random.choice((alm.BunueloGusarajo,
                                     alm.HigadoDragon,
                                     alm.TartaMelaza))()
            print(f"{self} te ha ofrendado un {ofrenda}!")
            magizoologo.alimentos.append(ofrenda)


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
        if "tiempo_satisfecha" not in kwargs:
            kwargs["tiempo_satisfecha"] = PMT.AUGUREY_TIEMPO_SATISFECHA
        if "nivel_magico" not in kwargs:
            kwargs["nivel_magico"] = random.randint(*PMT.NIFFLER_RANGO_NIVEL_MAGICO)
        if "prob_escaparse" not in kwargs:
            kwargs["prob_escaparse"] = PMT.NIFFLER_PROB_ESCAPARSE
        if "prob_enfermarse" not in kwargs:
            kwargs["prob_enfermarse"] = PMT.NIFFLER_PROP_ENFERMARSE
        if "vida_max" not in kwargs:
            kwargs["vida_max"] = random.randint(*PMT.NIFFLER_RANGO_VIDA_MAXIMA)
        if "agresividad" not in kwargs:
            kwargs["agresividad"] = PMT.NIFFLER_NIVEL_AGRESIVIDAD
        # Inicia la clase
        super().__init__(nombre, **kwargs)
        # Atributo único
        if "nivel_cleptomania" not in kwargs:
            kwargs["nivel_cleptomania"] = random.randint(*PMT.NIFFLER_RANGO_CLEPTOMANIA)
        else:
            kwargs["nivel_cleptomania"] = int(kwargs["nivel_cleptomania"])

    def caracteristica_unica(self, magizoologo):
        # factor decide se regala (* +1) o roba (* -1)
        factor = (self.nivel_hambre == "satisfecha") * 2 - 1
        sickles = factor * self.nivel_cleptomania * PMT.NIFFLER_PESO_SICKLES_ROBADOS
        if sickles > 0:
            print(f"{self} te ha regalado {sickles} sickles!")
        elif sickles < 0:
            print(f"{self} te ha robado {- sickles} sickles :(")
        magizoologo.sickles += sickles


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

    def caracteristica_unica(self, magizoologo):
        if self.nivel_hambre == "hambrienta" and magizoologo.alimentos:
            alimento_robado = random.randint(0, len(magizoologo.alimentos) - 1)
            robado = magizoologo.alimentos.pop(alimento_robado)
            print(f"{self} te ha robado un {robado}!")
            self.dias_sin_comer = 0
