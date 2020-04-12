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

import operator as op
import random

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
                ("Pasar al día siguiente",
                 self.__pasar_de_dia),   # Propio del ZOO
                ("Guardar Progreso",
                 self._actualizar_archivos),   # Propio del ZOO
            ),
            "Menú cuidar DCCriaturas": (
                (f"Alimentar criatura: -{PMT.MAGIZOOLOGOS_COSTO_ALIMENTAR}E",
                 lambda: self.magizoologo_actual.alimentar_dccriatura()),
                (f"Recuperar criatura: -{PMT.MAGIZOOLOGOS_COSTO_RECUPERAR}E",
                 lambda: self.magizoologo_actual.recuperar_dccriatura()),
                (f"Sanar criatura: -{PMT.MAGIZOOLOGOS_COSTO_CURAR}E",
                 lambda: self.magizoologo_actual.sanar_dccriatura()),
                (f"Habilidad especial: -{PMT.MAGIZOOLOGOS_COSTO_HABILIDAD}E",
                 lambda: self.magizoologo_actual.habilidad_especial()),
                (f"Peleas: {PMT.PELEAS_APUESTA} Sickles",
                 self.__empezar_pelea),  # Propio del ZOO
            ),
            "Menú DCC": (
                ("Adoptar criaturas",
                 lambda: self._dcc.vernder_criaturas(self.magizoologo_actual,\
                                                     self.lista_criaturas)),
                ("Comprar alimentos",
                 lambda: self._dcc.vernder_alimentos(self.magizoologo_actual)),
                ("Ver estado",
                 lambda: self._dcc.mostrar_estado(self.magizoologo_actual)),
            ),
        }
        self._dcc = dcc.DCC()
        self.__indice_magizoologo_actual = None
        self.lista_criaturas = None
        self.lista_magizoologos = None

    @property
    def magizoologo_actual(self):
        return self.lista_magizoologos[self.__indice_magizoologo_actual]

    def main_loop(self):
        self._leer_archivos()
        pc.loop_menus(self._menus, "Menú de Inicio")
        self._actualizar_archivos()

    def _leer_archivos(self):
        print("Cargando...")
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
        print("Guardando...")
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
                (PMT.TEXTO_ES_ALFANUMERICO, str.isalnum),
                (PMT.TEXTO_ES_UNICO, lambda x: x not in self.lista_magizoologos),
                ), ),
            ("Elige el tipo de Magizoólogo que desea ser", (
                ("Es Docencio, Tareo o Hibrido",
                 lambda x: x.lower() in {"docencio", "tareo", "hibrido"}),
                ), ),
            ("Elige tu primera DCCriatura!", (
                ("Es Augurey, Niffler o Erkling",
                 lambda x: x.lower() in {"augurey", "niffler", "erkling"}),
                ), ),
            ("Elige un nombre único y alfanumérico para tu DCCriatura", (
                (PMT.TEXTO_ES_ALFANUMERICO, str.isalnum),
                (PMT.TEXTO_ES_UNICO, lambda x: x not in self.lista_magizoologos),
                ), ),
        )
        if valores:
            nombre_magizoologo, tipo_magizoologo, tipo_criatura, nombre_criatura = valores
            tipo_magizoologo = mzg.retornar_clase_magizoologo(tipo_magizoologo)
            tipo_criatura = ctr.retornar_clase_criatura(tipo_criatura)
            nueva_criatura = tipo_criatura(nombre_criatura)
            self.lista_criaturas.append(nueva_criatura)
            self.lista_magizoologos.append(tipo_magizoologo(nombre_magizoologo,
                                                            criaturas=[nueva_criatura]))
            self.__indice_magizoologo_actual = len(self.lista_magizoologos) - 1
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
            nombre = nombre[0]
            self.__indice_magizoologo_actual = self.lista_magizoologos.index(nombre)
            print("Accediendo...!")
            return True
        return False

    def __pasar_de_dia(self):
        print("*" * PMT.UI_ANCHO)
        print(" Has pasado al día siguiente! ".center(PMT.UI_ANCHO, "*"))
        print("*" * PMT.UI_ANCHO)
        # ---------------------------- DCC ---------------------------- #
        print(" DCC ".center(PMT.UI_ANCHO - 2, "-").center(PMT.UI_ANCHO, "*"))
        # Nivel de aprobación
        self._dcc.calcular_aprobación(self.magizoologo_actual)
        # Pagos
        self._dcc.pagar_magizoologo(self.magizoologo_actual)
        # Multas
        self._dcc.fiscalizar_magizoologo(self.magizoologo_actual)
        # ------------- Tranformación a SuperMagizoólogo ------------- #
        if PMT.SUPERMAGIZOOLOGO_ACTIVO and self.magizoologo_actual.nivel_aprobacion >= 100:
            print("Por tener 100 de aprobación, te transformaste en un SuperMagizoólogo!")
            nombres_atributos = ("nombre", "criaturas", "alimentos", "sickles", "licencia",
                                 "nivel_aprobacion", "nivel_magico", "destreza", "energia_max",
                                 "responsabilidad")  # energia_actual == energia_max
            extractor_atributos = op.attrgetter(*nombres_atributos)
            atributos = extractor_atributos(self.magizoologo_actual)
            diccionario_atributos = {k: v for k, v in zip(nombres_atributos, atributos)}
            nuevo_magizoologo = mzg.MagizoologoSuper(**diccionario_atributos)
            self.lista_magizoologos[self.__indice_magizoologo_actual] = nuevo_magizoologo
        # ----------------------- Día siguiente ----------------------- #
        print(("-" * (PMT.UI_ANCHO - 2)).center(PMT.UI_ANCHO, "*"))
        print(" Al día siguiente... ".center(PMT.UI_ANCHO - 2, "-").center(PMT.UI_ANCHO, "*"))
        print(("-" * (PMT.UI_ANCHO - 2)).center(PMT.UI_ANCHO, "*"))
        escapados = list()
        enfermas = list()
        for criatura in self.magizoologo_actual.criaturas:
            # Habilidades especial
            criatura.caracteristica_unica(self.magizoologo_actual)
            # Perder salud por enfermedad
            if criatura.enferma:
                criatura.vida_actual -= PMT.CRIATURAS_PENALISACION_VIDA_ENFERMEDAD
                print(f"{criatura} ha perdido salud por estar enferma!")
            # Perder salud por hambre
            if criatura.nivel_hambre == "hambrienta":
                criatura.vida_actual -= PMT.CRIATURAS_PENALISACION_VIDA_HAMBRIENTA
                print(f"{criatura} ha perdido salud por estar hambrienta!")
            # Mostrar su salud si perdió alguna
            if criatura.enferma or criatura.nivel_hambre == "hambrienta":
                print(f" su salud actual es {criatura.vida_actual}")
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
        print("-" * PMT.UI_ANCHO)
        if escapados:
            print("Criatura{0} escapada{0}:".format("s" * (len(escapados) > 1)),
                  ", ".join(escapados))
        if enfermas:
            print("Criatura{0} enferma{0}:".format("s" * (len(enfermas) > 1)),
                  ", ".join(enfermas))
        print("*" * PMT.UI_ANCHO)
        # ------------------------ Magizoólogo ------------------------ #
        # Recuperar su salud
        self.magizoologo_actual.energia_actual = self.magizoologo_actual.energia_max
        print()
        return True

    def __empezar_pelea(self):
        if len(self.magizoologo_actual.criaturas) < 2:
            print("No tienes suficientes criaturas!")
            return False
        if self.magizoologo_actual.sickles < PMT.PELEAS_APUESTA:
            print("No contienes suficientes Sickels!")
            return False
        print("Tus criaturas son:")
        for criatura in self.magizoologo_actual.criaturas:
            print(f" - {criatura}: {criatura.nivel_magico}NM, "
                  f"{criatura.vida_actual}HP, {criatura.prob_escaparse}PE")
        while True:
            # -------------- Selección de criaturas -------------- #
            # Magizoólogo
            print("Selecciona la criatura para que te represente")
            criatura_elegida = input("--> ").strip()
            if criatura_elegida not in self.magizoologo_actual.criaturas:
                if pc.volver_a_intentarlo(criatura_elegida, "Tienes esa criatura"):
                    continue
                else:
                    return False
            while True:
                # DCC
                if not PMT.PELEAS_EL_DCC_ELIGE:
                    criatura_dcc = pc.proceso_multipaso(
                        ("Selecciona la criatura para que represente al DCC", (
                            ("Tienes esa criatura",
                                lambda x: x in self.magizoologo_actual.criaturas),
                            ("Sea distinta a la elegida",
                                lambda x: ((x == criatura_elegida)
                                           != (x in self.magizoologo_actual.criaturas)))
                        ), ),
                    )
                    if not criatura_dcc:
                        break
                    else:
                        criatura_dcc = criatura_dcc[0]
                    criatura_dcc = random.choice(
                        [str(c) for c in self.magizoologo_actual.criaturas
                            if c != criatura_elegida]
                    )
                # -------------- Inicio de la pelea -------------- #
                c_mgz = self.magizoologo_actual.obtener_dccriatura(criatura_elegida)
                c_dcc = self.magizoologo_actual.obtener_dccriatura(criatura_dcc)
                turno = PMT.PELEAS_INICIAL
                criaturas = (c_mgz, c_dcc)
                nombres = (str(self.magizoologo_actual), "DCC")
                vida_inicial = (c_mgz.vida_actual, c_dcc.vida_actual)
                while (c_mgz.vida_actual > PMT.CRIATURAS_VIDA_MINIMA
                       and c_dcc.vida_actual > PMT.CRIATURAS_VIDA_MINIMA):
                    # Cambio de Turno
                    turno = (turno + 1) % 2
                    criatura_atacante = criaturas[turno]
                    criatura_defendida = criaturas[(turno + 1) % 2]
                    print(f"\nEs el turno de {nombres[turno]}")
                    print(f"{criatura_atacante} trata de atacar a {criatura_defendida}!")
                    # Esquivar
                    prob_esquivar = (1 - criatura_defendida.prob_escaparse)\
                        * PMT.PELEAS_PROB_ESQUIVAR
                    if prob_esquivar > random.random():
                        print(f"{criatura_defendida} ha esquivado el ataque!")
                        continue
                    # Atacar
                    daño = (criatura_atacante.nivel_magico
                            * PMT.PELEAS_ATAQUE[criatura_atacante.agresividad])
                    print(f"{criatura_atacante} realiza un ataque de {daño} daño!")
                    criatura_defendida.vida_actual -= daño
                    print(f"{criatura_defendida} ha quedado con "
                          f"{criatura_defendida.vida_actual} de vida")
                # -------------- Termino de la pelea -------------- #
                print("\nLa pelea ha terminado!")
                print(f"{criatura_atacante} ha derrotado a {criatura_defendida}!")
                if turno == 0:
                    print(f"Has ganado! Recibiste {PMT.PELEAS_APUESTA * 2} Sickles")
                    self.magizoologo_actual.sickles += PMT.PELEAS_APUESTA * 2
                elif turno == 1:
                    print(f"Has perdido :(  Perdiste {PMT.PELEAS_APUESTA * 2} Sickles")
                    self.magizoologo_actual.sickles -= PMT.PELEAS_APUESTA * 2
                # Recuperar la vida
                for indice in range(2):
                    criaturas[indice].vida_actual = vida_inicial[indice]
                return True


if __name__ == "__main__":
    ZoologicoMagico().main_loop()
