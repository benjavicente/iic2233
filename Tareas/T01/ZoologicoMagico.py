"""
=============================
Módulo principal del programa
=============================
Contiene la clase:
------------------
    ZoologicoMagico
Depende de:
-----------
    parametros
    magizoologos
    dccriaturas
    alimentos
    dcc
    procesos
"""

# TODO:
# Completar los procesos del programa
# Revizar si hay párametros en este archivo
# Documentar lo que ya está hecho}
# Mostrar en README los que es funcional
# Completar pasar día
# Completar pelea

from os import system
import operator as op

import parametros as PMT
import magizoologos as mzg
import dccriaturas as ctr
import alimentos as ams
import dcc
import procesos as pc


class ZoologicoMagico:
    """
    ================
    Zoológico Magico
    ================

    Encargado de los menús del programa y
    realizar los procesos pedidos por el usuario

    Los métodos y atributos encargados
    del funcionamiento del módulo son:
      - _menus
      - __anteriores
      - _dcc
      - _magizoologo_actual
      - __init__()
      - main_loop()
      - _leer_archivos()
      - _actualizar_archivos()

    El resto de los métodos corresponden a los procesos
    que el usuario puede realizar. Estos son:
      - __crear_magizoologo()
      - __cargar_magizoologo()
      - __pasar_de_dia()
      - __alimentar_criatura()
      - __recuperar_criatura()
      - __sanar_criatura()
      - __habilidad_especial()
      - __empezar_pelea()
      - __adoptar_criatura()
      - __comprar_alimentos()
      - __ver_estado()
    """
    def __init__(self):
        self._menus = {
            "Menú de Inicio": (
                ("Crear Magizoólogo", self.__crear_magizoologo, "Menú de Acciones"),
                ("Cargar Magizoólogo", self.__cargar_magizoologo, "Menú de Acciones"),
            ),
            "Menú de Acciones": (
                "Menú cuidar DCCriaturas",
                "Menú DCC",
                ("Pasar al día siguiente", self.__pasar_de_dia)
            ),
            "Menú cuidar DCCriaturas": (
                ("Alimentar criatura", self.__alimentar_criatura),
                ("Recuperar criatura", self.__recuperar_criatura),
                ("Sanar criatura", self.__sanar_criatura),
                ("Habilidad especial", self.__habilidad_especial),
                ("Peleas", self.__empezar_pelea),
            ),
            "Menú DCC": (
                ("Adoptar criaturas", self.__adoptar_criatura),
                ("Comprar alimentos", self.__comprar_alimentos),
                ("Ver estado", self.__ver_estado),
            ),
        }
        self._dcc = dcc.DCC()
        self._magizoologo_actual = None
        self._leer_archivos()

    def main_loop(self):
        pc.loop_menus(self._menus, "Menú de Inicio",
                      self._leer_archivos, self._actualizar_archivos)

    def _leer_archivos(self):
        # ----------------------- #
        # Archivo de DCCriaturas  #
        # ----------------------- #
        self.lista_criaturas = list()
        with open(PMT.PATH_CRIATURAS, "r", encoding="UTF-8") as archivo_criaturas:
            datos_archivo_criaturas = archivo_criaturas.readlines()
        for fila_criatura in datos_archivo_criaturas:
            # Separo las filas en valores
            fila_criatura = fila_criatura.strip().split(",")
            # Creo un diccionario con los valores
            parametros_criatura = {key: value for key, value
                                   in zip(PMT.FORMATO_CRIATURAS, fila_criatura)}
            # Se define el tipo
            if parametros_criatura["tipo"] == "Augurey":
                clase_criatura = ctr.Augurey
            elif parametros_criatura["tipo"] == "Erkling":
                clase_criatura = ctr.Erkling
            elif parametros_criatura["tipo"] == "Niffler":
                clase_criatura = ctr.Niffler
            else:
                continue
            # Se crea la DCCriatura
            self.lista_criaturas.append(clase_criatura(**parametros_criatura))
        # ----------------------- #
        # Archivo de Magizoólogos #
        # ----------------------- #
        self.lista_magizoologos = list()
        with open(PMT.PATH_MAGIZOOLOGOS, "r", encoding="UTF-8") as archivo_magizoologos:
            datos_archivo_magizoologos = archivo_magizoologos.readlines()
        for fila_magizoologo in datos_archivo_magizoologos:
            # Separo la fila en los valores
            fila_magizoologo = fila_magizoologo.strip().split(",")
            # Creo un diccionario con los valores
            parametros_magizoologo = {key: value for key, value
                                      in zip(PMT.FORMATO_MAGIZOOLOGOS, fila_magizoologo)}
            # Se define el tipo
            clase_magizoologo = pc.retornar_clase_magizoologo(parametros_magizoologo["tipo"])
            # Se agregan sus alimentos
            lista_alimentos_magizoologo = list()
            for nombre_alimento in parametros_magizoologo["alimentos"].split(";"):
                tipo_alimento = pc.retornar_clase_alimento(nombre_alimento)
                lista_alimentos_magizoologo.append(tipo_alimento())
            parametros_magizoologo["alimentos"] = lista_alimentos_magizoologo
            # Se agregan sus criaturas
            nombre_criaturas = parametros_magizoologo["criaturas"].split(";")
            lista_criaturas = list(filter(lambda criatura: criatura in nombre_criaturas,
                                   self.lista_criaturas))
            parametros_magizoologo["criaturas"] = lista_criaturas
            # Se crea el Magizoólogo
            self.lista_magizoologos.append(clase_magizoologo(**parametros_magizoologo))

    def _actualizar_archivos(self):
        with open(PMT.PATH_MAGIZOOLOGOS, "w", encoding="UTF-8") as archivo_magizoologos:
            for magizoologo in self.lista_magizoologos:
                extractor_atributos = op.attrgetter(*PMT.FORMATO_MAGIZOOLOGOS)
                atributos_magizoologo = list(extractor_atributos(magizoologo))
                for indice in range(len(atributos_magizoologo)):
                    if type(atributos_magizoologo[indice]) is list:
                        atributos_magizoologo[indice] = \
                            ";".join([str(v) for v in atributos_magizoologo[indice]])
                print(*atributos_magizoologo, sep=",", file=archivo_magizoologos)

        with open(PMT.PATH_CRIATURAS, "w", encoding="UTF-8") as archivo_criaturas:
            for criatura in self.lista_criaturas:
                extractor_atributos = op.attrgetter(*PMT.FORMATO_CRIATURAS)
                atributos_criatura = list(extractor_atributos(criatura))
                print(*atributos_criatura, sep=",", file=archivo_criaturas)

    """
    Inicio de Métodos de Procesos
    """

    def __crear_magizoologo(self):
        valores = pc.proceso_multipaso(
            ("Elige un nombre único y alfanumérico", (
                ("Es alfanumérico", str.isalnum),
                ("Es único", lambda x: x not in self.lista_magizoologos),
                ),),
            ("Elige el tipo de Magizoólogo que desea ser", (
                ("Es Docencio, Tareo o Hibrido",
                 lambda x: x.lower() in {"docencio", "tareo", "Hibrido"}),
                ),),
            ("Elige tu primera DCCriatura!", (
                ("Es Augurey, Niffler o Erkling",
                 lambda x: x.lower() in {"augurey", "niffler", "erkling"}),
                ),),
            ("Elige un nombre único y alfanumérico para tu DCCriatura", (
                ("Es alfanumérico", str.isalnum),
                ("Es único", lambda x: x not in self.lista_magizoologos),
                ),),
        )
        if valores:
            nombre_magizoologo, tipo_magizoologo, tipo_criatura, nombre_criatura = valores
            tipo_magizoologo = pc.retornar_clase_magizoologo(tipo_magizoologo)
            tipo_criatura = pc.retornar_clase_criatura(tipo_criatura)
            nueva_criatura = tipo_criatura(nombre_criatura)
            self.lista_criaturas.append(nueva_criatura)
            self._magizoologo_actual = tipo_magizoologo(nombre_magizoologo,
                                                        criaturas=[nueva_criatura])
            self.lista_magizoologos.append(self._magizoologo_actual)
            return True
        return False

    def __cargar_magizoologo(self):
        nombre = pc.proceso_multipaso(
            ("Ingresa tu nombre", (
                ("El Magizoólogo existe", lambda x: x in self.lista_magizoologos),
                ),),
        )
        if nombre:
            index = self.lista_magizoologos.index(*nombre)
            self._magizoologo_actual = self.lista_magizoologos[index]
            return True
        return False

    def __pasar_de_dia(self, _dcc):
        # Propio + DCC
        pass

    def __alimentar_criatura(self):
        self._magizoologo_actual.alimentar_dccriatura()

    def __recuperar_criatura(self):
        self._magizoologo_actual.recuperar_dccriatura()

    def __sanar_criatura(self):
        self._magizoologo_actual.sanar_dccriatura()

    def __habilidad_especial(self):
        self._magizoologo_actual.habilidad_especial()

    def __empezar_pelea(self):
        # Magizoólogo?
        pass

    def __adoptar_criatura(self):
        self._dcc.vernder_criaturas(self._magizoologo_actual)

    def __comprar_alimentos(self):
        self._dcc.vernder_alimentos(self._magizoologo_actual)

    def __ver_estado(self):
        self._dcc.mostrar_estado(self._magizoologo_actual)


if __name__ == "__main__":
    ZoologicoMagico().main_loop()