# Logotipo modificado a partir de la fuente Big de TAAG
# http://www.patorjk.com/software/taag/#f=Big&t=DCCahuin
LOGOTIPO = (
    R"  _____   _____ _____      _           _       " "\n"
    R" |  __ \ / ____/ ____|    | |         /_/      " "\n"
    R" | |  | | |   | |     __ _| |__  _   _ _ _ __  " "\n"
    R" | |  | | |   | |    / _` | '_ \| | | | | '_ \ " "\n"
    R" | |__| | |___| |___| (_| | | | | |_| | | | | |" "\n"
    R" |_____/ \_____\_____\__,_|_| |_|\__,_|_|_| |_|"
)

TEXTO_BIENVENIDA = "\nBienvenid@ a "

TEXTO_INCIO = (
    "\n"
    "Selecione una opción:\n"
    "    [1] Iniciar Seción\n"
    "    [2] Registro de Usuario\n"
    "    [0] Salir\n"
)

TEXTO_PRINCIPAL = ""


def menu_inicio():
    en_menu_inicio = True
    print(TEXTO_BIENVENIDA)
    print(LOGOTIPO)

    while en_menu_inicio:
        print(TEXTO_INCIO)
        opcion = input(" -----> ")
        print()
        if opcion == "1":
            menu_iniciar_secion()
        elif opcion == "2":
            menu_registro_de_usuario()
        elif opcion == "0":
            print("Saliendo...")
            en_menu_inicio = False
        else:
            print("Opción invalida")


if __name__ == "__main__":
    menu_inicio()
