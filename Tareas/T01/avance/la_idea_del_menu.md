# La idea del menú

## Antecedentes

En la tarea anterior, realize un sistema de menus por funciones, en donde cada función se encargaba independientemente de imprimir y administrar las elecciones del usuario. Este tenia la siguiente estructura:

```python
def menu_1():
    print(
        "    menu 1   ",
        "[1] - opción 1",
        "[2] - opción 2",
        ,sep="\n"
    )
    acc = input("-->").strip()
    if acc == "1":
        pass
    if acc == "2":
        pass

def menu_2():
    print(
        "    menu 2   ",
        "[1] - opción 1",
        "[2] - opción 2",
        ,sep="\n"
    )
    acc = input("-->").strip()
    if acc == "1":
        pass
    if acc == "2":
        pass
```

Esto provocó qu repitierá mucho código, asi que para esta tarea decidí intentar hacer un sistema de menús.

## Los menus de la T01

Antes de empezar a crear un sistema para estos, estructuré como tendrán que funcionar los menús de esta tarea:

![Diagrama de menús](diagrama_menus.png?raw=true "Diagrama de menús")

Lo importante del diagrama es reconocer dos posibles estados en el que se puede encontrar el programa: **en menú y en proceso**.

En menús se puede entender como el estado donde al usuario se le otorga una opción a elegir (tanto nuevos menus como procesos y acciones), mientras que en proceso es donde el usuario debe completar un procedimientos entregando _inputs_ específicos.

## Estructuración

Para empezar, modelé los estados de menús.

### Menús

Para ahorrar código, armé el sintaxis lo más simple y adaptable posible. Por esto, elegí organizar los diferentes menús en un diccionario:

```python
menu = {
    "menu 1": (
        "menu 2",
        "menu 3",
    ),
    "menu 2": (
        "menu 4",
    ),
    "menu 3": (
    ),
    "menu 4": (
    ),
}
```

Para almacenar información del flujo del usuario entre los menús, utilicé dos variables:

```python
anteriores = []
actual = "menu 1"
```

Para unir los menús, creé el siguiente _loop_:

```python
while True:
    n = -1
    # Se imprime el menu actual
    print(f" {actual} ".center(16, "-"))
    # Se imprimen las opciones enumeradas
    for n, opc in enumerate(menu[actual]):
        print(f"[{n+1}] - {opc}")
    # Se imprime la opción volver si es posible
    if anteriores:
        print(f"[{n+2}] - Volver")
    print("[0] - Salir")

    acc = input("\nElegir:").strip()
    print()

    if acc == str(0):
        break
    elif acc == str(n + 2) and self.anteriores:
        actual = anteriores.pop()
    elif acc.isdecimal() and 0 < int(acc) < n + 2:
        anteriores.append(actual)
        actual = menu[actual][int(acc) - 1]
```

Este realiza el siguiente algoritmo:

1. Se imprime el menú actual
2. Se imprimen las opciones definidas en `menu` con la opción de volver y salir.
3. Se recibe un _input_.
4. Si eligió un menú, se cambia al menu elegido.

Esto crea un sistema de menus aprueba de errores, donde el sintaxis para crear y editar menús es compacto, el programa contiene las opciones de volver y salir en cada menu y el programa es aprueba de errores. Pero aún falta añadir la opción de realizar un proceso.

### Procesos

Cada proceso se puede guardar como dos elementos: el nombre del proceso y el proceso en si. Esto puede guardarse en un tupla con sintaxis `(nombre, proceso)`.

Decidí que el proceso sea un método de una clase `ZoologicoMagico`, la cual encapsulará también el código anterior. Ahora, para ejecutar este proceso, el programa debe diferenciar entre proceso y menú, tanto al imprimir las opciones como realizarlas.

Por esto, añado una condición tanto al imprimir las opciones (`opc`) y el ejecutarlas (`type(self.menu[self.actual][acc])`)

```python
class Zoologico:
    def __init__(self):
        self.menu = {
            ...
            "menu 4": (
                # Proceso de ejemplo
                ("Printear Hola", self.print_hola)
            ),
        }
        ...

    def main_loop(self):
        while True:
            ...
            for n, opc in enumerate(menu[actual]):
                if type(opc) is tuple:
                    # Se usa el nombre del proceso
                    opc = opc[0]
                ...
            ...
            elif acc.isdecimal() and 0 < int(acc) < n + 2:
                acc = int(acc) - 1
                if type(self.menu[self.actual][acc]) is str:
                    self.anteriores.append(self.actual)
                    self.actual = self.menu[self.actual][acc]
                elif type(self.menu[self.actual][acc]) is tuple:
                    # Se ejecuta el proceso
                    self.menu[self.actual][acc][1]()

    def print_hola(self):
        # Método del proceso
        print("Hola mundo!")
```

Ahora tanto los menús como los procesos pueden funcionar correctamente. Pero aún así falta algo: el menú del proceso fallido.

### Menú proceso fallido

En el enunciado se pide que si el usuario ingresa un valor invalido en medio de un proceso se le debe derivar a un menu donde pueda elegir intentar ingresar un valor nuevamente, volver al menu anterior o salir del programa.

En este menú dos aspectos son importantes:

1. Incitarle al usuario porque se equivocó
2. Indicarle que puede hacer

El caso que use para testear fue el siguiente:

```python
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
            if self.volver_intentarlo(numero, *condiciones):
                return
        print(f"Tu nombre es {nombre} y tu número {numero}")
```

Cuando los valores son válidos, el ciclo se rompe con `break` y continua el proceso. `self.volver_intentarlo(n, *r)` debe ser un método que muestre porque el valor `n` no es valido por las razones `r`. Si el usuario decide volver a intentarlo, el ciclo debe volver a empezar. En el caso que decide volver al menú anterior o salir del programa, debe salir del método con `return`. Además, si decide salir, el programa debe terminar.

Para satisfacer esto, primero cambie la condición para que el programa siga:

```python
    def main_loop(self):
        while self.__loop:
            ...
```

Esto permite al método `volver_intentarlo` terminar el programa, como se pide en la pauta.

Luego cree el método:

```python
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
```

## Resultados

Todo el código anterior se puede probar en el archivo [`prototipo_menus.py`](prototipo_menus.py). 

El prototipo final tiene la siguiente estructura:

```python
class ZoologicoMagico:
    def __init__(self):
        self.menu = {
            # ...
            # Menús y procesos
        }
        self.anteriores = []
        self.actual = "menu 1"
        self.__loop = True

    def main_loop(self):
        while self.__loop:
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
            if acc == str(0):
                break
            elif acc == str(n + 2) and self.anteriores:
                self.actual = self.anteriores.pop()
            elif acc.isdecimal() and 0 < int(acc) < n+2:
                acc = int(acc) - 1
                if type(self.menu[self.actual][acc]) is str:
                    self.anteriores.append(self.actual)
                    self.actual = self.menu[self.actual][acc]
                elif type(self.menu[self.actual][acc]) is tuple:
                    self.menu[self.actual][acc][1]()
            else:
                print(f"Opción '{acc}' no valida")

    def volver_intentarlo(self, invalido, *porque):
        print(f"\n'{invalido}' no es valido porque:")
        for n, razon in enumerate(porque):
            print(f"{n + 1}.- {razon}")
        print("-"*15)
        while True:
            print(
                "[1] - Volver a intentarlo",
                "[2] - Volver al menú",
                "[0] - Salir",
                sep="\n"
                )
            acc = input("\nElegir:").strip()
            if acc == "1":
                return True
            elif acc == "0":
                self.__loop = False
            if acc == "0" or acc == "2":
                return False
            print(f"Opción '{acc}' no valida")

    # ...
    # Métodos de los procesos
```
