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
        self._indice_magizoologo_actual = None
        self.lista_criaturas = None
        self.lista_magizoologos = None
        self._leer_archivos()

    @property
    def magizoologo_actual(self):
        return self.lista_magizoologos[self._indice_magizoologo_actual]

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
            clase_magizoologo = mzg.retornar_clase_magizoologo(parametros_magizoologo["tipo"])
            # Se agregan sus alimentos
            lista_alimentos_magizoologo = list()
            if parametros_magizoologo["alimentos"]:
                for nombre_alimento in parametros_magizoologo["alimentos"].split(";"):
                    tipo_alimento = ams.retornar_clase_alimento(nombre_alimento)
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
        # Encontré esto en la documentación
        # https://docs.python.org/3/reference/compound_stmts.html#with
        with open(PMT.PATH_MAGIZOOLOGOS, "w", encoding="UTF-8") as archivo_magizoologos,\
             open(PMT.PATH_CRIATURAS, "w", encoding="UTF-8") as archivo_criaturas:
            for magizoologo in self.lista_magizoologos:
                # Atributos magizoólogo
                extractor_atributos = op.attrgetter(*PMT.FORMATO_MAGIZOOLOGOS)
                atributos_magizoologo = list(extractor_atributos(magizoologo))
                for indice in range(len(atributos_magizoologo)):
                    # Si es uha lista se unen los elementos con ";"
                    if type(atributos_magizoologo[indice]) is list:
                        atributos_magizoologo[indice] = \
                            ";".join([str(v) for v in atributos_magizoologo[indice]])
                # Guarda los atributos del magizoólogo
                print(*atributos_magizoologo, sep=",", file=archivo_magizoologos)
                # Guarda sus criaturas en el archivo de criaturas
                for criatura in magizoologo.criaturas:
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
            tipo_magizoologo = mzg.retornar_clase_magizoologo(tipo_magizoologo)
            tipo_criatura = ctr.retornar_clase_criatura(tipo_criatura)
            nueva_criatura = tipo_criatura(nombre_criatura)
            self.lista_criaturas.append(nueva_criatura)
            self.lista_magizoologos.append(tipo_magizoologo(nombre_magizoologo,
                                                            criaturas=[nueva_criatura]))
            self._indice_magizoologo_actual = len(self.lista_magizoologos) - 1
            print("Magizoólogo creado!")
            return True
        return False

    def __cargar_magizoologo(self):
        nombre = pc.proceso_multipaso(
            ("Ingresa tu nombre", (
                ("El Magizoólogo existe", lambda x: x in self.lista_magizoologos),
                ),),
        )
        if nombre:
            self._indice_magizoologo_actual = self.lista_magizoologos.index(*nombre)
            print("Accediendo...!")
            return True
        return False

    def __pasar_de_dia(self):
        print("*" * PMT.UI_ANCHO)
        print(" Has pasado al día siguiente! ".center(PMT.UI_ANCHO, "*"))
        print("*" * PMT.UI_ANCHO)
        print("Resumen de los eventos de hoy...")
        escapados = list()
        enfermas = list()
        for criatura in self.magizoologo_actual.criaturas:
            # Habilidades especial
            criatura.caracteristica_unica(self.magizoologo_actual)
            # Perder salud por enfermedad
            if criatura.enferma:
                criatura.vida_actual -= PMT.CRIATURAS_PENALISACION_VIDA_ENFERMEDAD
                print(f"{criatura} ha perdido salud por estar enferma! "
                      f"Su salud actual es {criatura.vida_actual}")
            # Perder salud por hambre
            if criatura.nivel_hambre == "hambrienta":
                criatura.vida_actual -= PMT.CRIATURAS_PENALISACION_VIDA_HAMBRIENTA
                print(f"{criatura} ha perdido salud por estar hambrienta! "
                      f"Su salud actual es {criatura.vida_actual}")
            # Enfermarse
            if criatura.enfermarse(self.magizoologo_actual.responsabilidad):
                print(f"{criatura} se ha enfermado :(")
            # Escaparse
            if criatura.escaparse(self.magizoologo_actual.responsabilidad):
                print(f"{criatura} se ha escapado!")
            # Días sin comer, se actualiza el nivel de hambre en la property
            criatura.dias_sin_comer += 1
            # Listas de datos de enfermados y escapados
            if criatura.enferma:
                enfermas.append(str(criatura))
            if criatura.escapado:
                escapados.append(str(criatura))
        if escapados:
            print("Criatura{0} escapada{0}:".format("s" * (len(escapados) > 1)),
                  ", ".join(escapados))
        if enfermas:
            print("Criatura{0} enferma{0}:".format("s" * (len(enfermas) > 1)),
                  ", ".join(enfermas))
        print("*" * PMT.UI_ANCHO)
        print("El DCC...")
        # Nivel de aprobación
        self._dcc.calcular_aprobación(self.magizoologo_actual)
        # Pagos
        self._dcc.pagar_magizoologo(self.magizoologo_actual)
        # Multas
        self._dcc.fiscalizar_magizoologo(self.magizoologo_actual)
        # Al retornar true se actualiza el archivo
        return True

    def __alimentar_criatura(self):
        self.magizoologo_actual.alimentar_dccriatura()

    def __recuperar_criatura(self):
        self.magizoologo_actual.recuperar_dccriatura()

    def __sanar_criatura(self):
        self.magizoologo_actual.sanar_dccriatura()

    def __habilidad_especial(self):
        self.magizoologo_actual.habilidad_especial()

    def __empezar_pelea(self):
        # Magizoólogo?
        pass

    def __adoptar_criatura(self):
        self._dcc.vernder_criaturas(self.magizoologo_actual, self.lista_criaturas)

    def __comprar_alimentos(self):
        self._dcc.vernder_alimentos(self.magizoologo_actual)

    def __ver_estado(self):
        self._dcc.mostrar_estado(self.magizoologo_actual)


if __name__ == "__main__":
    ZoologicoMagico().main_loop()
