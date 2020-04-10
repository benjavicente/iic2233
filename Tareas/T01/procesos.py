"""
=================
Procesos de menús
=================
Contiene las funciones:
-----------------------
    loop_menus
    volver_a_intentarlo
    proceso_multipaso
Depende de:
-----------
    parametros
"""

import parametros as PMT


def loop_menus(menus: dict, menu_inicial: str, inc_prc=None, fin_prc=None):
    """
    ==========
    Loop Menus
    ==========

    Función para crear un menú a partir de un diccionario.

    Argumentos
    ----------
     - menus: dict
    Diccionario con los menús. Tiene que tener la siguiente estructura:

    `key: str` Nombre del menú

    `value: str or tuple` Acción a realizar

    La acción `value` es un `str` cuando esta es ir al menu llamado `value`.

    La acción `value` es un `tuple` cuando la acción es una función.
    Esta tupla tiene que poseer la estructura (nombre, función, menu), donde:

    `nombre: str` es el nombre de la acción

    `función: func` es la acción a realiar

    `menu: str` es el menu siguiente, se mantiene en el mismo menú si es omitido.
    Solo se dirige al nuevo menú si el valor retornado por la funcione es `True`.

    - menu_inicial: str
    Menú inicial

    - inc_prc: func
    Función a realizar antes de iniciar un proceso.
    Útil para cuando se necesitan respaldar datos.

    - fin_prc: func
    Función a realizar luego de terminar un proceso.
    Útil para cuando se necesitan respaldar datos.
    Solo se ejecuta cuando el valor retornado por
    la función del menú es `True`
    """
    menu_actual = menu_inicial
    menus_anteriores = list()
    while True:
        numero = -1
        # Se imprimen las opciones
        print("\n" + f" {menu_actual} ".center(PMT.UI_ANCHO, "-"))
        for numero, opcion in enumerate(menus[menu_actual]):
            if type(opcion) is tuple:
                opcion = opcion[0]
            print(f"[{numero + 1}] - {opcion}")
        if menus_anteriores:
            print(f"[{numero + 2}] - Volver al {menus_anteriores[-1]}")
        print("[0] - Salir\n")
        # Se pide el input
        elegida = input("--> ").strip()
        print()
        if elegida == "0":
            # Sale del loop
            return
        elif menus_anteriores and elegida == str(numero + 2):
            # Vuelve al menú anterior
            menu_actual = menus_anteriores.pop()
        elif elegida.isdecimal() and 0 < int(elegida) < numero + 2:
            # Realiza la acción
            elegida = int(elegida) - 1
            valor = menus[menu_actual][elegida]
            if type(valor) is str:
                # Ir a menú
                menus_anteriores.append(menu_actual)
                menu_actual = valor
            elif type(valor) is tuple:
                # Realizar acción
                if inc_prc:
                    inc_prc()
                out = valor[1]()
                if out:
                    if len(valor) == 3:
                        menus_anteriores.append(menu_actual)
                        menu_actual = valor[2]
                # Esto puede ejecutarse siempre o
                # Cuando se retorne True en out
                if fin_prc:
                    fin_prc()
        else:
            print(f"Opción '{elegida}' no valida\n")


def volver_a_intentarlo(valor_invalido: str, *razones_invalido):
    """
    ==========================
    Submenú de Proceso Fallido
    ==========================

    Encargado de mostrarle al usuario
    porque el valor ingresado no es valido.
    Entrega las opciones de volver a intentarlo,
    volver al menú anterior y salir.
    Si se elige la opción 1 o 2 se retornará un Bool
    indicando si se quiere volver a intentarlo.
    Si se elige la opción 0, se termina el programa.

    Argumentos
    ----------
     - valor_invalido: str
    El valor invalido.

     - razones_invalido: iterable
    Las razones de porque es invalido.
    """
    print(f"\n'{valor_invalido}' no es valido porque NO se cumplió que:")
    for numero, razon in enumerate(razones_invalido):
        print(f"{numero + 1}.- {razon}")
    while True:
        print(
            "[1] - Volver a intentarlo",
            "[2] - Volver atrás",
            "[0] - Salir",
            sep="\n"
        )
        elegida = input("--> ").strip()
        if elegida == "0":
            exit()
        elif elegida == "1" or elegida == "2":
            return elegida == "1"
            print()
        print(f"Opción '{elegida}' no valida\n")


def proceso_multipaso(*iterable):
    """
    =====================
    Submenú de un Proceso
    =====================

    Encargado de los procesos en los que
    se requieren realizar multiples validaciones.

    Si no se cumplen las condiciones, se llama a
    `volver_a_intentarlo`para preguntarle al usuario
    si desea volver intentarlo, volver atrás o salir.

    Argumentos
    ----------
     - iterable: tuple
    Sub-procesos a realizar. La tupla tiene que tener la estructura:

    `[0]: str` Input que se le pide al usuario

    `[1]: tuple -> (str, func)` Condiciones que debe cumplir el input,
    donde `str` es el nombre de esta y `func` le función para evaluarla.

    Las funciones/métodos son evaluados con la forma if x(input)`.

     - v: ist
    Lista donde se almacenan los valores que se retornarán.
    """
    menu, condiciones = iterable[0]
    while True:
        print(menu)
        elegida = input("--> ").strip()
        no_cumplidas = tuple(condicion for condicion, funcion
                             in condiciones
                             if not funcion(elegida))
        if no_cumplidas:
            if not volver_a_intentarlo(elegida, *no_cumplidas):
                return False
        else:
            if len(iterable) == 1:
                return [elegida]
            seguir = proceso_multipaso(*iterable[1:])
            if seguir:
                return [elegida] + seguir
