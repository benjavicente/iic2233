import usermanager as um

"""
Código encargado de administrar los menus de DCCahuín
Usa un sistema de funciones dentro de funciones para
crear un sistema de menus.
`usermanager` es el módulo encargado de realizar operaciónes
en los datos, como editar seguidos, posts y usuarios
Logotipo DCCahuín modificado a partir de la fuente Big de TAAG
http://www.patorjk.com/software/taag/#f=Big&t=DCCahuin
"""

# Usuario actual
usuario_act = None


def banner():
    print(
        R"                                         _____  ",
        R"    Bienvenid@ a                        / ... \ ",
        R"  _____   _____ _____      _           / _____/ ",
        R" |  __ \ / ____/ ____|    | |         /_/       ",
        R" | |  | | |   | |     __ _| |__  _   _ _ _ __   ",
        R" | |  | | |   | |    / _` | '_ \| | | | | '_ \  ",
        R" | |__| | |___| |___| (_| | | | | |_| | | | | | ",
        R" |_____/ \_____\_____\__,_|_| |_|\__,_|_|_| |_| ",
        sep="\n", end="\n" * 2
    )


def menu_entrada():
    banner()
    while True:
        print(
            "  Seleccione una opción:",
            " " * 4 + "[1] Iniciar Sesión",
            " " * 4 + "[2] Registro de Usuario",
            " " * 4 + "[0] Salir",
            sep="\n"
        )
        acc = input(" " * 4 + "-----> ").strip()
        if acc == "1":
            menu_inicio()
        elif acc == "2":
            menu_registro()
        elif acc == "0":
            print("Saliendo...".center(um.ancho_ui))
            print()
            break
        else:
            print(" " * 4 + "Opción no valida")
        print()


def menu_inicio():
    global usuario_act
    print(" " * 4 + "Ingrese el nombre de su usuario:")
    acc = input(" " * 6 + "@").strip()
    print()
    if acc in um.set_usuarios:
        # el usuario existe y se inicia seción
        usuario_act = um.Usuario(acc)
        print("Iniciando seción...".center(um.ancho_ui), end="\n" * 2)
        # El usuario entra a el loop del menu principal
        menu_principal()
        # Banner se imprime nuevamente al cerrar seción
        banner()
    else:
        print(" " * 4 + "El usuario ingresado no existe")
    print()


def menu_registro():
    print(
        " " * 4 + "Ingrese el nombre del usuario:",
        " " * 4 + "El nombre de usuario debe contener",
        " " * 4 + "al menos una letra y un número, no",
        " " * 4 + "contener simbolos o espacios y debe tener",
        " " * 4 + "un largo de entre 8 y 32 caracteres",
        sep="\n", end="\n" * 2
    )
    usuario = input(" " * 6 + "@").strip()
    if usuario in um.set_usuarios:
        # el nombre ingresado ya existe
        print(" " * 4 + "El usuario ya existe, intenta otro nombre")
    elif um.usuario_valido(usuario):
        # el usuario es valido y no existe
        um.crear_usuario(usuario)
        print(" " * 4 + "Usuario creado!")
        print(" " * 4 + "Inicia seción para acceder")
    else:
        # el usuario no es valido y no existe
        print(" " * 4 + "EL usuario a crear no es valido")
    print()


def menu_principal():
    global usuario_act
    while True:
        # Es importante imprimir el `usuario_act` para
        # recordar el nombre de perfil al usuario
        print(f"  Hola {usuario_act}, que desea hacer hoy?")
        print(
            " " * 4 + "[1] Ver, crear o eliminar PrograPosts",
            " " * 4 + "[2] Ver y editar a quien sigues",
            " " * 4 + "[0] Cerrar sesión",
            sep="\n"
            )
        acc = input(" " * 4 + "-----> ").strip()
        if acc == "1":
            menu_prograposts()
        elif acc == "2":
            menu_seguidos()
        elif acc == "0":
            print()
            print("Cerrando seción".center(um.ancho_ui))
            print()
            # sale del loop y cierra seción
            break
        else:
            print(" " * 4 + "Acción no valida")
        print()
        # `Menu principal` se imprime aquí para que no se imprima
        # la primera vez que el usuario entre a este menu
        print(" Menú Principal ".center(um.ancho_ui, "-"))


def menu_prograposts():
    global usuario_act
    print()
    print(" Menú de PrograPosts ".center(um.ancho_ui, "-"))
    while True:
        print(
            " " * 4 + "[1] Ver tu Muro",
            " " * 4 + "[2] Ver tus publicaciones",
            " " * 4 + "[3] Crear un PrograPost",
            " " * 4 + "[4] Eliminar un PrograPost",
            " " * 4 + "[0] Volver",
            sep="\n"
        )
        acc = input(" " * 4 + "-----> ").strip()
        if acc == "1":
            # Muro
            print(
                " " * 6 + "[1] De más nuevo a más antiguo",
                " " * 6 + "[2] De más antiguo a más nuevo",
                " " * 6 + "[0] Volver",
                sep="\n"
            )
            acc = input(" " * 6 + "-----> ")
            if acc == "1":
                usuario_act.imprimir_muro(recientes=True)
            elif acc == "2":
                usuario_act.imprimir_muro(recientes=False)
        elif acc == "2":
            # Publicaciones propias
            print(
                " " * 6 + "[1] De más nuevo a más antiguo",
                " " * 6 + "[2] De más antiguo a más nuevo",
                " " * 6 + "[0] Volver",
                sep="\n"
            )
            acc = input(" " * 6 + "-----> ")
            if acc == "1":
                usuario_act.imprimir_publicaciones(recientes=True)
            elif acc == "2":
                usuario_act.imprimir_publicaciones(recientes=False)
        elif acc == "3":
            # Crear PrograPost
            print(
                " " * 4 + "Cual es el mensaje que deseas publicar?",
                " " * 4 + "Puedes publicar entre 1 a 140 caracteres",
                " " * 4 + "Si quieres cancelar el mensaje,",
                " " * 4 + "no escribas nada",
                sep="\n", end="\n" * 2
            )
            mensaje = input()
            # NOTA: En los issues del curso se mencionó que los espacios que
            # rodean al mensaje deben ser considerados en el post,
            # por lo que no se usa ´.strip()´ en el ´input()´ anterior
            if 1 <= len(mensaje) < 140:
                print(usuario_act.publicar(mensaje))
            elif len(mensaje) > 140:
                print()
                print(" " * 4 + "El tamaño del post es muy largo!")
        elif acc == "4":
            # Eliminar Post
            cantidad_de_posts = usuario_act.cantidad_publicaciones()
            if cantidad_de_posts > 0:
                # Solo se continua si hay posts
                if cantidad_de_posts == 1:
                    # Como existe solo un post, se elimina el más reciente
                    cual = "r"
                else:
                    # Se pregunta el post a eliminar
                    print(
                        " " * 4 + "Cual es el post que deseas eliminar?",
                        " " * 4 + f"Elija entre 0 y {cantidad_de_posts - 1}",
                        " " * 4 + "donde 0 es el post más antiguo",
                        " " * 4 + f"y {cantidad_de_posts - 1} es el más nuevo",
                        " " * 4 + "Para eliminar el más reciente, use \"r\"",
                        " " * 4 + "Para volver, deje el campo vacío",
                        sep="\n", end="\n" * 2
                    )
                    cual = input(" " * 4 + "Post a eliminar: ")
                    # NOTA: este input no contiene el método strip ya que en
                    # los issues del syllabus se menciona que un post con un
                    # mensaje vacío debe ser permitido
                if cual.isdigit() or cual == "r":
                    if cual == "r":
                        cual = None
                    print()
                    print("ELiminar?")
                    # Dentro de la función eliminar_post se
                    # realiza la confirmación para eliminarlo
                    print(usuario_act.eliminar_post())
            else:
                print(" " * 4 + "No puedes eliminar: No tienes PrograPosts")
        elif acc == "0":
            break
        else:
            print("Acción no valida")
        print()


def menu_seguidos():
    global usuario_act
    print()
    print(" Menú de Seguidos y Seguidores ".center(um.ancho_ui, "-"))
    print(
        (
            f"Seguidores: {len(usuario_act.obtener_seguidores())}    "
            f"Seguidos: {len(usuario_act.obtener_seguidos())}"
        ).center(um.ancho_ui)
    )
    while True:
        print(
            "  Que desea hacer?",
            " " * 4 + "[1] Seguir a un usuario",
            " " * 4 + "[2] Dejar de seguir a un usuario",
            " " * 4 + "[3] Ver usuarios seguidos",
            " " * 4 + "[4] Ver seguidores",
            " " * 4 + "[0] Volver",
            sep="\n"
        )
        acc = input(" " * 4 + "-----> ")
        if acc == "1":
            print(
                "Cual usuario desea seguir?",
                "Deje el campo vacío para volver",
                sep="\n"
            )
            cual = input("  -----> @").strip()
            if cual:
                print(usuario_act.empezar_a_seguir(cual))
        elif acc == "2":
            if usuario_act.obtener_seguidos():
                print(
                    "Cual usuario desea parar de seguir?",
                    "Deje el campo vacío para volver",
                    sep="\n"
                )
                cual = input("  -----> @").strip()
                if cual:
                    print(usuario_act.dejar_de_seguir(cual))
            else:
                # No hay usuarios
                print(
                    " " * 4 + "No puedes dejar de seguir:",
                    " " * 4 + "No sigues a nadie",
                    sep="\n"
                )
        elif acc == "3":
            seguidos = usuario_act.obtener_seguidos()
            if seguidos:
                print(" " * 4 + "Seguidos:")
                print("\n".join([" " * 6 + "@" + usr for usr in seguidos]))
            else:
                print("No sigues a nadie aun")
        elif acc == "4":
            seguidores = usuario_act.obtener_seguidores()
            if seguidores:
                print(" " * 4 + "Seguidores:")
                print("\n".join([" " * 6 + "@" + usr for usr in seguidores]))
            else:
                print("No te sigue nadie aun")
        elif acc == "0":
            break
        else:
            print(" " * 4 + "Acción no valida")
        print()


if __name__ == "__main__":
    menu_entrada()
