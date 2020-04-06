from datetime import datetime
from os import system


class ZoologicoMagico:
    def __init__(self):
        self.menu = {
            "menu 1": (
                "menu 2",
                "menu 3",
            ),
            "menu 2": (
                "menu 4",
                ("Dar la hora", self.dar_la_hora),
            ),
            "menu 3": (
                "menu 4",
                ("ingresar nombre y código", self.proceso_multipaso),
            ),
            "menu 4": (
                "menu 5",
                ("Printear Hola", self.print_hola),
            ),
            "menu 5": (
                "menu 2",
                ("Cambiar limpieza de menus", self.cambio_de_limpiar),
            )

        }
        self.anteriores = []
        self.actual = "menu 1"
        self.__loop = True
        # -- Variables Opcionales -- #
        self.limpiar = False

    def main_loop(self):
        while self.__loop:
            # Opción de limpiar
            if self.limpiar:
                system("cls")

            n = -1
            print(f" {self.actual} ".center(16, "-"))
            for n, opc in enumerate(self.menu[self.actual]):
                if type(opc) is tuple:
                    opc = opc[0]
                print(f"[{n+1}] - {opc}")
            if self.anteriores:
                print(f"[{n+2}] - Volver")
            print("[0] - Salir")

            acc = input("\nElegir:").strip()
            print()

            if acc == str(0):
                # Termina el loop
                break

            elif acc == str(n + 2) and self.anteriores:
                # Vuelve atrás
                self.actual = self.anteriores.pop()

            elif acc.isdecimal() and 0 < int(acc) < n+2:
                acc = int(acc) - 1
                if type(self.menu[self.actual][acc]) is str:
                    # Se cambia de menú
                    self.anteriores.append(self.actual)
                    self.actual = self.menu[self.actual][acc]
                elif type(self.menu[self.actual][acc]) is tuple:
                    # Se ejecuta el proceso
                    self.menu[self.actual][acc][1]()
                    if self.limpiar:
                        input("...")

            else:
                print(f"Opción '{acc}' no valida")

    def volver_intentarlo(self, invalido, *porque):
        # Imprime cual fue el input del usuario
        print(f"\n'{invalido}' no es valido porque:")
        # Lista las razones de porque no es valido
        for n, razon in enumerate(porque):
            print(f"{n + 1}.- {razon}")
        print("-"*15)
        # Entra al menú del proceso fallido
        while True:
            print(
                "[1] - Volver a intentarlo",
                "[2] - Volver al menú",
                "[0] - Salir",
                sep="\n"
                )
            acc = input("\nElegir:").strip()
            print()
            if acc == "1":
                return True
            elif acc == "0":
                self.__loop = False
            if acc == "0" or acc == "2":
                return False
            print(f"Opción '{acc}' no valida")

    def print_hola(self):
        print("Hola mundo!")

    def dar_la_hora(self):
        hora = datetime.today().strftime("%H:%M")
        print(f"Son las {hora} :)")

    def cambio_de_limpiar(self):
        self.limpiar = not self.limpiar

    def proceso_multipaso(self):
        while True:
            print("Ingrese un nombre alfanumérico")
            nombre = input().strip()
            if nombre.isalnum():
                break
            if not self.volver_intentarlo(nombre, "No es alfanumérico"):
                return
        while True:
            print("Ingrese un numero de cuatro dígitos")
            numero = input().strip()
            condiciones = (
                ("No es un número", numero.isdecimal()),
                ("No tiene 4 caracteres", len(numero) == 4),
            )
            condiciones = [razon for razon, b in condiciones if not b]
            if not len(condiciones):
                break
            if not self.volver_intentarlo(numero, *condiciones):
                return
        print(f"Tu nombre es {nombre} y tu número {numero}")


if __name__ == "__main__":
    ZoologicoMagico().main_loop()
