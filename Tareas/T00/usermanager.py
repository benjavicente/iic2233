from datetime import date
from os import path
from operator import attrgetter


def get_set_usuarios():
    """
    Retorna el set de usuarios
    Antes set_usuarios era una variable global
    """
    set_usuarios = set()
    path_usuarios = path.join("data", "usuarios.csv")
    with open(path_usuarios, "r", encoding="utf8") as archivo:
        for fila_archivo in archivo.readlines():
            set_usuarios.add(fila_archivo.strip())
    return set_usuarios


def crear_usuario(nombre_usuario):
    """
    Agrega el usuario a usuarios.csv, seguidores
    Retorna un str sobre el resultado
    Se asume que el usuario ya es valido
    """
    # Se agrega el usuario al archivo de usuario y seguidores
    # En vez de rehacer el archivo, este se usa
    # la opción `a` append, y se agrega al final
    path_usuarios = path.join("data", "usuarios.csv")
    with open(path_usuarios, "a", encoding="utf8") as archivo:
        print(nombre_usuario, file=archivo)
    path_seguidores = path.join("data", "seguidores.csv")
    with open(path_seguidores, "a", encoding="utf8") as archivo:
        print(nombre_usuario, file=archivo)
    return "Bienvenido a DCCahuín!"


def usuario_valido(usuario):
    """
    El usuario debe:
        1 - Tener un número
        2 - Tener una letra
        3 - Ser entre 8 y 32 caractares
        4 - Ser alfanumérico
    """
    if not any([str(numero) in usuario for numero in range(10)]):
        # ve si no hay ningún numero en usuario
        return False
    if not usuario.upper().isupper():
        # https://stackoverflow.com/a/47453486
        # `isupper()` es falso si no existen
        # **letras** mayúsculas en un str
        return False
    if not (8 <= len(usuario) <= 32):
        return False
    if not usuario.isalnum():
        return False
    return True


def obtener_dict_seguidores():
    """
    Retorna un diccionario con los seguidores
        LLaves
            (str) Nombres de usuarios
        Valores
            (set) Listas de seguidores
    """
    dict_seg = dict()
    path_seguidores = path.join("data", "seguidores.csv")
    with open(path_seguidores, "r", encoding="utf8") as archivo:
        for fila_archivo in archivo.readlines():
            usuario, _, seguidores = fila_archivo.strip().partition(",")
            # Se transforma los seguidores a set
            if "," in seguidores:
                seguidores = set(seguidores.split(","))
            elif not seguidores:
                seguidores = set()
            else:
                seguidores = {seguidores}
            # Se crea la entrada en el diccionario
            dict_seg[usuario] = seguidores
        return dict_seg


def modificar_archvivo_seguidores(usuario, otro, func):
    """
    Modifica el archivo de seguidores, simplifica métodos
    empezar_a_seguir y dejar_de_seguir de la clase Usuario
    Argumentos
        usuario - nombre del usuario que realiza la acción
        otro - usuario al que se modifica sus seguidores
        func - acción a realizar, es `set.add` o `set.discard`
    """
    if func == set.add or func == set.discard:
        directorio_seguidores = obtener_dict_seguidores()
        # remplazando func (método), se añadirá o eliminara
        # el usuario de las lista de seguidores de otro
        # Se utiliza el sintax método(objeto, argumentos)
        # para los métodos `set.add` y `set.discard`
        func(directorio_seguidores[otro], usuario)
        path_seguidores = path.join("data", "seguidores.csv")
        with open(path_seguidores, "w", encoding="utf8") as archivo:
            for usuario, seguidores in directorio_seguidores.items():
                print(usuario, *seguidores, sep=",", file=archivo)


def extraer_posts():
    """
    Retorna una lista de objetos de clase PrograPost
    """
    lista_prograposts = list()
    path_posts = path.join("data", "posts.csv")
    with open(path_posts, "r", encoding="utf8") as archivo:
        for fila_archivo in archivo.readlines():
            data = fila_archivo.strip().split(",", 2)
            lista_prograposts.append(PrograPost(*data))
    return lista_prograposts


def posts_filtrar(*usuarios, rec=True):
    """
    Extraer_post() se ejecuta para obtener el listado.
    Se filtra por usuario y los ordena por fecha,
    si la fecha es la misma, se ordena por usuario
    Se el usuario y la fecha son las mismas, se ordena por mensaje
    Argumento:
        *usuarios - usuario(s) a mostrar
        rec - orden, muestra por defecto los post más nuevos primeros
    Solución a partír de:
    https://docs.python.org/3/howto/sorting.html#operator-module-functions
    """
    lista = [post for post in extraer_posts() if post.usuario in usuarios]
    orden = ("fecha", "usuario",  "mensaje")
    lista.sort(key=attrgetter(*orden), reverse=rec)
    return lista


class Usuario:
    """
    Usuario - Herramientas para administrar el usuario actual
    """
    def __init__(self, nombre):
        """
        El usuario debe ser creado en Crear Usuario, luego
        se debe crear el objeto Usuario al iniciar seción
        """
        self.nombre = nombre

    def __str__(self):
        return f"@{self.nombre}"

    def obtener_seguidores(self):
        return obtener_dict_seguidores()[self.nombre]

    def obtener_seguidos(self):
        """
        Por cada usuario y sus seguidores, se agrega al usuario al set
        si el usuario es seguido por el usuario actual
        """
        items = obtener_dict_seguidores().items()
        return {usr for usr, seguidos in items if self.nombre in seguidos}

    def empezar_a_seguir(self, otro):
        """
        Se empieza a seguir al usuario `otro`
        Retorna un str confirmando la accións
        """
        if otro == self.nombre:
            return "No te puedes seguirte a ti mismo!"
        elif otro not in get_set_usuarios():
            return f"El usuario @{otro} no existe"
        modificar_archvivo_seguidores(self.nombre, otro, set.add)
        print f"Ahora sigues a @{otro}"

    def dejar_de_seguir(self, otro):
        if otro not in get_set_usuarios():
            return "El usuario no existe"
        elif otro not in self.obtener_seguidos():
            return "No sigues al usuario"
        modificar_archvivo_seguidores(self.nombre, otro, set.discard)
        return f"Dejaste de seguir a @{otro}"

    def cantidad_publicaciones(self):
        """
        Retorna la cantidad de publicaciones del usuario
        """
        return len(posts_filtrar(self.nombre))

    def imprimir_publicaciones(self, recientes=True):
        """
        Se imprime los post del usuario
        """
        print(" Tus publicaciones ".center(47, "-"))
        lista_posts = posts_filtrar(self.nombre, rec=recientes)
        if lista_posts:
            print(*lista_posts, sep="")
        else:
            # Se invita al usuario a publicar un PrograPost
            print(
                "",
                "Tu perfil está vació".center(48),
                "Crea tu primera publicación!".center(48),
                sep="\n\n"
            )
        print()

    def imprimir_muro(self, recientes=True):
        """
        Se imprime el muro del usuario
        Se asume que:
            1- Se necesita imprimir todos los post inmediatamente
            2- No se muestra los post del usuario
                En caso de tener que mostrarlos,
                agregar el argumento self.user
                antes de *self.obtener.seguidores()
        """
        print(" Tu Muro ".center(47, "-"))
        lista_posts = posts_filtrar(*self.obtener_seguidos(), rec=recientes)
        if lista_posts:
            print(*lista_posts, sep="")
        # Si la lista esta vaciá, invita al
        # usuario a seguir a más usuarios
        else:
            print(
                "",
                "Tu Múro está vació".center(48),
                "Trata de seguir a más usuarios!".center(48),
                sep="\n\n"
                )
        print()

    def publicar(self, mensaje):
        """
        Se guarda la publicación del usuario en posts.cvs
        Retorna el mensaje de confirmación
        """
        if 1 <= len(mensaje) <= 140:
            # Solución para evitar sobreescribir el archivo encontrado aquí:
            # https://stackoverflow.com/a/10640823
            path_posts = path.join("data", "posts.csv")
            with open(path_posts, "a", encoding="utf8") as archivo:
                fecha = str(date.today()).replace("-", "/")
                print(self.nombre, fecha, mensaje, sep=",", file=archivo)
            # Se muestra el PrograPost
            print(PrograPost(self.nombre, fecha, mensaje))
            return "Mensaje publicado"
        elif 140 < len(mensaje):
            return "Mensaje muy largo para publicar"
        return ""  # No se retorna nada, el usuario cancelo la acción

    def eliminar_post(self, numero_post=-1):
        """
        Elimina la publicación del usuario
        Por defecto se elimina la ultima realizada
        Retorna un mensaje de confirmación
        """
        # Se extraen las listas
        lista_posts = extraer_posts()
        posts_propios = posts_filtrar(self.nombre, rec=False)
        if - len(posts_propios) <= numero_post < len(posts_propios):
            # Se muestra el post y se confirma la acción
            print(posts_propios[numero_post])
            confirmar = input("(Sí) / (No) ----> ").strip().lower()
            if confirmar in {"sí", "si", "s"}:
                path_posts = path.join("data", "posts.csv")
                with open(path_posts, "w", encoding="utf8") as archivo:
                    # `orden` es el orden en el que los datos se
                    # guardan en el archivo. Sirve también para eliminar
                    # el (o los) posts que contienen la misma información
                    # mostrada en confirmar
                    orden = attrgetter("usuario", "fecha",  "mensaje")
                    for post in lista_posts:
                        if orden(posts_propios[numero_post]) != orden(post):
                            print(*orden(post), sep=",", file=archivo)
                return "PrograPost eliminado"
            return "Acción cancelada"
        return f"No existe el post con indice {numero_post}"


class PrograPost:
    """
    PrograPost - Contenedor de PrograPosts
    """
    def __init__(self, usuario, fecha, mensaje):
        self.usuario = usuario
        self.fecha = fecha
        self.mensaje = mensaje

    def __str__(self):
        """
        Retorna un cuadro de post formateado
        """
        return (
            f"{'_' * 48}\n"
            f"|  0  | @{self.usuario.ljust(38)}|\n"
            f"| /Y\\ | {self.fecha.rjust(38)} |\n"
            f"|{'=' * (46)}|\n"
            f"{self.cuadro_de_mensaje()}\n"
            f"|{'_' * (46)}|\n"
        )

    def cuadro_de_mensaje(self):
        """
        Método para imprimir la parte "mensaje"
        de un PrograPost en el cuadro establecido en el
        método __str__
        Limita las palabras por fila, de modo que leer
        un post sea cómodo
        """
        lista_palabras = self.mensaje.split(" ")
        # ancho total y ancho restante
        largo_max = 44
        largo_restante = largo_max
        # string inicial reducido a {largo_max} columnas
        columna = str()
        for palabra in lista_palabras:
            # Se itera por cada palabra y se añaden
            # de izquierda a derecha y de arriba a abajo
            if len(palabra) > largo_max:
                # La palabra es muy larga, se corta
                # Completa el espacio restante
                columna += " "*largo_restante
                # Se crea palabra_cortada para almacenar el nuevo str
                palabra_cortada = str()
                cortes_necesarios = (len(palabra)-3)//largo_max
                for parte in range(cortes_necesarios + 1):
                    # Se obtiene el trozo de la palabra larga
                    p = palabra[parte*(largo_max-3):(parte+1)*(largo_max-3)]
                    if parte != cortes_necesarios:
                        # Se agregan puntos para mostrar que se cortó
                        p += "..."
                    else:
                        # se ve el espacio que ocupa la "cola"
                        largo_restante = largo_max - len(p) - 1
                    # Se añade el cambio de linea y el trozo (p) que ocupa
                    # todo el espacio disponible (largo_max - "...")
                    palabra_cortada += "\n" + p
                # se guardan los cortes
                palabra = palabra_cortada
            elif len(palabra) > largo_restante:
                # la palabra es muy larga para la sección
                # restante, se imprime en la siguiente linea
                columna += " " * largo_restante + "\n"
                largo_restante = largo_max - len(palabra) - 1
            else:
                largo_restante -= len(palabra) + 1
            # Finalmente se agrega la palabra a la columna
            columna += palabra + " " * (largo_restante != -1)
            # " "*(largo_restante != -1)` es usado para evitar que
            # un espacio (" ") sea agregado cuando se sobrepase
            # el largo resante
        columna = columna.replace('\n', ' |\n| ')
        return f"| {columna}{' ' * largo_restante} |"
