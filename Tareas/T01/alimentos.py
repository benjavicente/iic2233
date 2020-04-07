from abc import ABC


class Alimentos(ABC):
    """
    Son utilizados para mantener a las criaturas en buen estado
    y producen distintos efectos al ser consumidos.
    """
    def __init__(self):
        self.__nombre = None
        self.pnt_vida = None

    def __str__(self):
        return self.__nombre

    def __repr__(self):
        return self.__nombre

    def __eq__(self, value):
        return self.__nombre == value


class TartaMaleza(Alimentos):
    """
    Alimento muy apetecido por los Magizoólogos para dárselos a las DCCriaturas,
    pues posee buenas propiedades respecto al resto de los alimentos.
    - Efecto de salud de 15
    - Si es consumido por un Niffler, existe una probabilidad de 0.15
      en que la agresividad pase de arisca a inofensiva de manera permanente
    """
    def __init__(self):
        self.__nombre = "Tarta de Maleza"
        self.pnt_vida = 15


class HigadoDragon(Alimentos):
    """
    Conocido por ser un alimento con propiedades medicinales.
    - Efecto de salud de 10
    - Si la DCCriatura está enferma, se sanará
    """
    def __init__(self):
        self.__nombre = "Hígado de Dragón"
        self.pnt_vida = 10


class BunueloGusarajo(Alimentos):
    """
    Es el alimento menos costoso.
    - Efecto de salud de 5
    - Existe una probabilidad de 0.35 que la criatura rechace el
      alimento y este se pierda.
    """
    def __init__(self):
        self.__nombre = "Buñuelo de Gusarajo"
        self.pnt_vida = 5
