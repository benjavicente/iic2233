"""
Código encargado de administrar los menus de DDCahupín
Usa un sistema de funciones dentro de funciones para
crear un sistema de menus.
Logotipo DCCahuín modificado a partir de la fuente Big de TAAG
http://www.patorjk.com/software/taag/#f=Big&t=DCCahuin
"""
import usermanager as um


# Usuario actual
usuario_act = None

def banner():
    print(
        R"Bienvenid@ a...                          _____  ",
        R"                                        / ... \ ",
        R"  _____   _____ _____      _           / _____/ ",
        R" |  __ \ / ____/ ____|    | |         /_/       ",
        R" | |  | | |   | |     __ _| |__  _   _ _ _ __   ",
        R" | |  | | |   | |    / _` | '_ \| | | | | '_ \  ",
        R" | |__| | |___| |___| (_| | | | | |_| | | | | | ",
        R" |_____/ \_____\_____\__,_|_| |_|\__,_|_|_| |_| ",
        sep="\n", end="\n"*2
    )

def menu_entrada():
    banner()
    while True:
        print(
            "  Selecione una opción:",
            " "*4 + "[1] Iniciar Seción",
            " "*4 + "[2] Registro de Usuario",
            " "*4 + "[0] Salir",
            sep="\n"
        )
        acc = input(" "*4 + "-----> ").strip()
        if acc == "1":
            menu_inicio()
        elif acc == "2":
            menu_registro()
        elif acc == "0":
            print("Saliendo...".center(um.ancho_max))
            break
        else:
            print(" "*4 + "Opción no valida")


def menu_inicio():
    global usuario_act
    print(" "*4 + "Ingrese el nombre de su usuario:")
    acc = input(" "*6 + "@").strip()
    print()
    if acc in um.set_usuarios:
        usuario_act = um.Usuario(acc)
        print("Iniciando seción...".center(um.ancho_max), end="\n"*2)
        menu_principal()
        # Baner se imprime de nuevo al cerrar seción
        banner()
    else:
        print(" "*4 + "El usuario ingresado no existe")
    print()


def menu_registro():
    print(" "*4 + "Ingrese el nombre del usuario:")
    print(" "*4 + "El nombre de usuario debe contener")
    print(" "*4 + "al menos un numero y debe tener un")
    print(" "*4 + "largo de entre 4 y 32 caracteres")
    print()
    usuario = input(" "*6 + "@").strip()
    if (usuario not in um.set_usuarios) and um.usuario_valido(usuario):
        um.crear_usuario(usuario)
        print(" "*4 + "Usuario creado!")
        print(" "*4 + "Inicia seción para acceder", end="\n"*2)
    else:
        print(" "*4 + "EL usuario a crear no es valido")
    print()


def menu_principal():
    global usuario_act
    print(f"  Hola {usuario_act}, que desea hacer hoy?")
    while True:
        print(
            " "*4 + "[1] Ver, añadir o eliminar Prograposts",
            " "*4 + "[2] Ver y editar a quien sigues",
            " "*4 + "[0] Cerrar seción",
            sep="\n"
            )
        acc = input(" "*4 + "-----> ").strip()
        if acc == "1":
            menu_prograposts()
        elif acc == "2":
            menu_seguidos()
        elif acc == "0":
            print()
            print("Cerrendo seción".center(um.ancho_max))
            print()
            break
        else:
            print(" "*4 + "Acción no valida")
        print()
        # `Menu principal` se imprime aqui para que no se imrpima
        # la primera vez que el usuaio entre a este menu
        print(" Menú Principal ".center(um.ancho_max, "-"))


def menu_prograposts():
    global usuario_act
    print()
    print(" Menú PrograPosts ".center(um.ancho_max, "-"))
    while True:
        print(
            " "*4 + "[1] Ver tu Muro",
            " "*4 + "[2] Ver tus publicaciones",
            " "*4 + "[3] Crear un PrograPost",
            " "*4 + "[4] Eliminar un PrograPost",
            " "*4 + "[0] Volver",
            sep="\n"
        )
        acc = input(" "*4 + "-----> ").strip()
        if acc == "1":
            print(
                " "*6 + "[1] De más nuevo a más antiguo",
                " "*6 + "[2] De más antiguo a más nuevo",
            sep="\n"
            )
            acc = input(" "*6 + "-----> ")
            if acc == "1":
                usuario_act.imprimir_muro()
            elif acc == "2":
                usuario_act.imprimir_muro(recientes=False)
        elif acc == "2":
            print(
                " "*6 + "[1] De más nuevo a más antiguo",
                " "*6 + "[2] De más antiguo a más nuevo",
            sep="\n"
            )
            acc = input(" "*6 + "-----> ")
            if acc == "1":
                usuario_act.imprimir_publicaciones()
            elif acc == "2":
                usuario_act.imprimir_publicaciones(recientes=False)
        elif acc == "3":
            print(" "*4 + "Cual es el mensaje que deseas publicar?")
            print(" "*4 + "Puedes publicar entre 1 a 140 caracteres")
            print(" "*4 + "Si quieres cancelar el mensaje,")
            print(" "*4 + "no escribas nada")
            print()
            mensaje = input().strip()
            if 1 < len(mensaje) < 140:
                print(usuario_act.publicar(mensaje))
        elif acc == "4":
            print(" "*4 + "Cual es el post que deseas eliminar?")
            print(" "*4 + "El indice se encuentra entre 0 y uno")
            print(" "*4 + "menos que la cantidad de post propios")
            print(" "*4 + "Para eliminar el más reciente, use \"r\"")
            print(" "*4 + "Para volver, deje el campo vacio")
            print()
            cual = input(" "*4 + "Indice del post a eliminar: ").strip()
            if cual.isdigit() or cual == "r":
                if cual == "r":
                    cual = None
                print()
                print("ELiminar?")
                # Dentro de la función eliminar_post se
                # realiza la confirmación para eliminarlo
                print(usuario_act.eliminar_post())
        elif acc == "0":
            break
        else:
            print("Acción no valida")
        print()


def menu_seguidos():
    global usuario_act
    print()
    print(" Menú Seguidos y Seguidores ".center(um.ancho_max, "-"))
    print(
        (
            f"Seguidores: {len(usuario_act.obtener_seguidores())}    "
            f"Seguidos: {len(usuario_act.obtener_seguidos())}"
        ).center(um.ancho_max)
    )
    while True:
        print(
            "  Que desea hacer?",
            " "*4 + "[1] Seguir a un usuario",
            " "*4 + "[2] Dejar de seguir a un usuario",
            " "*4 + "[3] Ver usuarios seguidos",
            " "*4 + "[4] Ver seguidores",
            " "*4 + "[0] Volver",
            sep="\n"
        )
        acc = input(" "*4 + "-----> ")
        if acc == "1":
            print("Cual usuario desea seguir?")
            cual = input("  -----> @").strip()
            if cual.isalnum():
                print(usuario_act.empezar_a_seguir(cual))
        elif acc == "2":
            if usuario_act.obtener_seguidores():
                print("Cual usuario desea parar de seguir?")
                cual = input("  -----> @").strip()
                if cual.isalnum():
                    print(usuario_act.dejar_de_seguir(cual))
            else:
                # No hay usuarios
                print("No puedes dejar de seguir:")
                print("No sigues a nadie")
        elif acc == "3":
            seguidos = usuario_act.obtener_seguidos()
            if seguidos:
                print(" "*4 + "Seguidos:")
                print("\n".join([" "*6 + "@" + usr for usr in seguidos]))
            else:
                print("No sigues a nadie aun")
        elif acc == "4":
            seguidores = usuario_act.obtener_seguidores()
            if seguidores:
                print(" "*4 + "Seguidores:")
                print("\n".join([" "*6 + "@" + usr for usr in seguidores]))
            else:
                print("No te sigue nadie aun")
        elif acc == "0":
            break
        else:
            print(" "*4 + "Acción no valida")
        print()


if __name__ == "__main__":
    menu_entrada()
