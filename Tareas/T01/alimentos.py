"""
=========
Alimentos
=========
Contiene las Clases:
--------------------
    Alimentos
    TartaMelaza
    HigadoDragon
    BunueloGusarajo
Depende de:
-----------
    parametros
"""

from abc import ABC
import parametros as PMT


def retornar_clase_alimento(tipo_alimento: str):
    """
    Retorna la clase de el alimento
    """
    tipo_alimento = tipo_alimento.lower()
    for a, b in zip("áéíóúñ", "aeioun"):
        tipo_alimento = tipo_alimento.replace(a, b)
    tipos = {
        "tarta de melaza": TartaMelaza,
        "higado de dragon": HigadoDragon,
        "bunuelo de gusarajo": BunueloGusarajo,
    }
    if tipo_alimento in tipos:
        return tipos[tipo_alimento]


class Alimentos(ABC):
    """
    Son utilizados para mantener a las criaturas en buen estado
    y producen distintos efectos al ser consumidos.
    """
    def __init__(self):
        self._nombre = None
        self.pnt_vida = None

    def __str__(self):
        return self._nombre

    def __repr__(self):
        return self._nombre


class TartaMelaza(Alimentos):
    """
    Alimento muy apetecido por los Magizoólogos para dárselos a las DCCriaturas,
    pues posee buenas propiedades respecto al resto de los alimentos.
    - Efecto de salud de 15
    - Si es consumido por un Niffler, existe una probabilidad de 0.15
      en que la agresividad pase de arisca a inofensiva de manera permanente
    """
    def __init__(self):
        self._nombre = "Tarta de Melaza"
        self.pnt_vida = PMT.ALIMENTOS_TARTA_MALEZA_PNT


class HigadoDragon(Alimentos):
    """
    Conocido por ser un alimento con propiedades medicinales.
    - Efecto de salud de 10
    - Si la DCCriatura está enferma, se sanará
    """
    def __init__(self):
        self._nombre = "Hígado de Dragón"
        self.pnt_vida = PMT.ALIMENTOS_HIGADO_DRAGON_PNT


class BunueloGusarajo(Alimentos):
    """
    Es el alimento menos costoso.
    - Efecto de salud de 5
    - Existe una probabilidad de 0.35 que la criatura rechace el
      alimento y este se pierda.
    """
    def __init__(self):
        self._nombre = "Buñuelo de Gusarajo"
        self.pnt_vida = PMT.ALIMENTOS_BUNUELO_GUSARAJO
