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
import parametros as PT
import magizoologos as mzg
import dcc


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
        self._magizoologo_actual = None

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
        while self.__loop:
            numero = -1
            # Se imprime el menú actual
            print("\n" + f" {self.__actual} ".center(PT.UI_ANCHO, "-"))
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
                valor = self._menus[self.__actual][elegida]
                elegida = int(elegida) - 1
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
        # Archivo de DCCriaturas
        #criaturas = list()
        with open(PT.PATH_CRIATURAS, "r", encoding="UTF-8") as archivo_criaturas:
            datos_archivo_criaturas = archivo_criaturas.readlines()
        for fila_criatura in datos_archivo_criaturas:
            print(*fila_criatura.split(","), sep=" | ")
        # Archivo de Magizoólogos
        with open(PT.PATH_MAGIZOOLOGOS, "r", encoding="UTF-8") as archivo_magizoologos:
            datos_archivo_magizoologos = archivo_magizoologos.readlines()
        for fila_magizoologo in datos_archivo_magizoologos:
            print(*fila_magizoologo.split(","), sep="|")

    def _actualizar_archivos(self):
        pass

    """
    Inicio de Métodos de Procesos
    """

    def __crear_magizoologo(self):
        pass

    def __cargar_magizoologo(self):
        pass

    def __pasar_de_dia(self):
        pass

    def __alimentar_criatura(self):
        pass

    def __recuperar_criatura(self):
        pass

    def __sanar_criatura(self):
        pass

    def __habilidad_especial(self):
        pass

    def __empezar_pelea(self):
        pass

    def __adoptar_criatura(self):
        pass

    def __comprar_alimentos(self):
        pass

    def __ver_estado(self):
        pass


if __name__ == "__main__":
    ZoologicoMagico()._leer_archivos()
    # ZoologicoMagico().main_loop()
