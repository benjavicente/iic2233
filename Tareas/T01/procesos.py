import collections


def volver_a_intentarlo(valor_invalido, *razones_invalido):
    """
    ==========================
    Submenú de Proceso Fallido
    ==========================

    Encargado de mostrarle al usuario
    porque el valor ingresado no es valido.
    Entrega las opciones de volver a intentarlo,
    volver al menú anterior y salir.
    Si se elige la opción 1 o 2 se retornará un Bool
    indicando si se quiere volver a intentarlo
    Si se elige la opción 0, se termina el programa
    """
    print(f"\n'{valor_invalido}' no es valido porque no se cumplió que:")
    for numero, razon in enumerate(razones_invalido):
        print(f"{numero + 1}.- {razon}")
    while True:
        print(
            "[1] - Volver a intentarlo",
            "[2] - Volver al menú",
            "[0] - Salir",
            sep="\n"
        )
        elegida = input("--> ").strip()
        if elegida == "0":
            exit()
        elif elegida == "1" or elegida == "2":
            return elegida == "1"
        print(f"Opción '{elegida}' no valida")


def proceso_multipaso(iterable, valores=[]):
    """
    =====================
    Submenú de un Proceso
    =====================

    Encargado de los procesos en los que
    se requieren realizar multiples validaciones.
    El iterable tiene que tener la siguiente estructura:

    `[0]: str` Input que se le pide al usuario

    `[1]: tuple -> (str, func)` Condiciones que debe cumplir el input

    Las funciones/métodos serán evaluarán de la forma:

    `if x(input)`

    Si no se cumplen las condiciones, se llama a
    `volver_a_intentarlo`para preguntarle al usuario
    si desea volver intentarlo, volver atrás o salir.

    `valores` es la lista donde se almacenan
    los valores que se retornarán.
    """
    # Valores preterminados
    if type(iterable) is not collections.deque:
        iterable = collections.deque(iterable)
    menu, condiciones = iterable.popleft()
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
            if not iterable:
                valores.append(elegida)
                return True
            seguir = proceso_multipaso(iterable.copy(), valores)
            if seguir:
                """
                Seguir puede ser dos opciones:
                `True` si se repite el ciclo y llega al punto donde el
                iterable se acaba (`return valores`)
                `False` si el usuario desea volver en `volver_a_intentarlo`
                """
                valores.append(elegida)
                break
    return valores[::-1]


if __name__ == "__main__":
    # Ejemplo de proceso
    proceso = [
        (
            "Elija un nombre alfanumérico y único",
            (
                ("Es alfanumérico", str.isalnum),
                ("Es único", lambda x: x not in {"benjamín", "vicente"}),
            ),
        ),
        (
            "Elija el tipo que más le guste entre azul y rojo",
            (
                ("Es Rojo o Azul", lambda x: x.lower() in {"azul", "rojo"}),
            ),
        ),
    ]
    v = proceso_multipaso(proceso)
    print(v)
