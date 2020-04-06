"""
=============================
Módulo principal del programa
=============================

Encargado del _front-end_ utilizando los
métodos `main_loop()` y `_volver_a_intentarlo()`
de la clase `ZoologicoMagico`.

Entrega instrucciones a los demás módulos
utilizando un sistema de procesos.
"""

# TODO: agrera método que actualize los archivos
# TODO: agregar atributo que almacene el Magizoólogo
# TODO: completar los procesos del programa
# TODO: revizar si hay párametros en este archivo


from os import system
import parametros as PMT
import magizoologos as mzg
import dcc
import dccriaturas as ctr
import alimentos as ams


class ZoologicoMagico:
    """
    ================
    Zoológico Magico
    ================

    Encargado de los menús del programa y
    realizar los procesos pedidos por el usuario

    Contiene los 5 métodos y 6 atributos encargados
    del funcionamiento del programa. Estos son:
      - _menus
      - __anteriores
      - __actual
      - __loop
      - _dcc
      - _magizoologo_actual
      - __init__()
      - main_loop()
      - _volver_a_intentarlo()
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
        menu_inicial = "Menú de Inicio"
        self.__anteriores = list()
        self.__actual = menu_inicial
        self.__loop = True
        self._menus = {
            menu_inicial: (
                ("Crear Magizoólogo", self.__crear_magizoologo),
                ("Cargar Magizoólogo", self.__cargar_magizoologo),
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
        self._magizoologo_actual = None  # mzg.Magizoólogo() # TODO REMOVER
        self.lista_criaturas = list()
        self.lista_magizoologos = list()

    def main_loop(self):
        """
        ===========================
        Loop principal del Programa
        ===========================

        Imprime las opciones disponibles en cada menú y
        las realiza la elegida del usuario.
        Entrega la posibilidad de volver atrás (si es posible)
        y la opción de salir del programa.
        """
        self._leer_archivos()
        while self.__loop:
            numero = -1
            # Se imprime el menú actual
            print("\n" + f" {self.__actual} ".center(PMT.UI_ANCHO, "-"))
            # Se imprimen las opciones
            for numero, opcion in enumerate(self._menus[self.__actual]):
                if type(opcion) is tuple:
                    opcion = opcion[0]
                print(f"[{numero + 1}] - {opcion}")
            if self.__anteriores:
                print(f"[{numero + 2}] - Volver al {self.__anteriores[-1]}")
            print("[0] - Salir\n")
            # Se pide el input
            elegida = input("--> ").strip()
            if elegida == "0":
                # Sale del programa
                break
            elif elegida == str(numero + 2):
                # Vuelve atrás
                self.__actual = self.__anteriores.pop()
            elif elegida.isdecimal() and 0 < int(elegida) < numero + 2:
                elegida = int(elegida) - 1
                valor = self._menus[self.__actual][elegida]
                if type(valor) is str:
                    # Se cambia de menú
                    self.__anteriores.append(self.__actual)
                    self.__actual = valor
                elif type(valor) is str:
                    # Se empieza un proceso
                    self._menus[self.__actual][elegida][1]()

    def _volver_a_intentarlo(self, valor_invalido, *razones_invalido):
        """
        ==========================
        Submenú de Proceso Fallido
        ==========================

        Encargado de mostrarle al usuario
        porque el valor ingresado no es valido.
        Entrega las opciones de volver a intentarlo,
        volver al menú anterior y salir.
        """
        # Imprime el input del usuario no valido
        print(f"\n'{valor_invalido}' no es valido porque:")
        # Lista las razones de porque no es valido
        for numero, razon in enumerate(razones_invalido):
            print(f"{numero + 1}.- {razon}")
        # Inicia el loop del sub-menú
        while True:
            print(
                "[1] - Volver a intentarlo",
                "[2] - Volver al menú",
                "[0] - Salir",
                sep="\n"
            )
            elegida = input("--> ").strip()
            if elegida == "1":
                return True
            elif elegida == "0" or elegida == "2":
                if elegida == "0":
                    self.__loop = False
                return False
            print(f"Opción '{elegida}' no valida")

    # TODO
    def _leer_archivos(self):
        # ----------------------- #
        # Archivo de DCCriaturas  #
        # ----------------------- #
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
        with open(PMT.PATH_MAGIZOOLOGOS, "r", encoding="UTF-8") as archivo_magizoologos:
            datos_archivo_magizoologos = archivo_magizoologos.readlines()
        for fila_magizoologo in datos_archivo_magizoologos:
            # Separo la fila en los valores
            fila_magizoologo = fila_magizoologo.strip().split(",")
            # Creo un diccionario con los valores
            parametros_magizoologo = {key: value for key, value
                                      in zip(PMT.FORMATO_MAGIZOOLOGOS, fila_magizoologo)}
            # Se define el tipo
            if parametros_magizoologo["tipo"] == "Docecio":
                clase_magizoologo = mzg.MagizoologoDocencio
            elif parametros_magizoologo["tipo"] == "Tareo":
                clase_magizoologo = mzg.MagizoologoTareo
            elif parametros_magizoologo["tipo"] == "Híbrido":
                clase_magizoologo = mzg.MagizoologoHibrido
            elif parametros_magizoologo["tipo"] == "Super":
                clase_magizoologo = mzg.MagizoologoSuper
            else:
                continue
            # Se agregan sus alimentos
            lista_alimentos_magizoologo = list()
            for nombre_alimento in parametros_magizoologo["alimentos"].split(";"):
                if nombre_alimento == "Buñuelo de Gusarajo":
                    tipo_alimento = ams.BunueloGusarajo
                elif nombre_alimento == "Hígado de Dragón":
                    tipo_alimento = ams.HigadoDragon
                elif nombre_alimento == "Tarta de Melaza":
                    tipo_alimento = ams.TartaMaleza
                else:
                    continue
                lista_alimentos_magizoologo.append(tipo_alimento())
            parametros_magizoologo["alimentos"] = lista_alimentos_magizoologo
            # Se agregan sus criaturas
            nombre_criaturas = parametros_magizoologo["criaturas"].split(";")
            lista_criaturas = list(filter(lambda criatura: criatura == nombre_criaturas,
                                     self.lista_criaturas))
            parametros_magizoologo["criaturas"] = lista_criaturas
            # Se crea el Magizoólogo
            self.lista_magizoologos.append(clase_magizoologo(**parametros_magizoologo))

    def _actualizar_archivos(self):
        pass

    """
    Inicio de Métodos de Procesos
    """

    def __crear_magizoologo(self):
        # Propio
        pass

    def __cargar_magizoologo(self):
        # Propio
        pass

    def __pasar_de_dia(self, _dcc):
        # Propio + DCC
        pass

    def __alimentar_criatura(self):
        # Magizoólogo
        pass

    def __recuperar_criatura(self):
        # Magizoólogo
        pass

    def __sanar_criatura(self):
        # Magizoólogo
        pass

    def __habilidad_especial(self):
        # Magizoólogo
        pass

    def __empezar_pelea(self):
        # Magizoólogo?
        pass

    def __adoptar_criatura(self):
        # Magizoólogo + DCC
        pass

    def __comprar_alimentos(self):
        # Magizoólogo + DCC
        pass

    def __ver_estado(self):
        # Magizoólogo + DDC
        pass


if __name__ == "__main__":
    ZoologicoMagico().main_loop()
