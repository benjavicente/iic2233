from datetime import date
from os import path
from operator import attrgetter

# Se obtiene el path de los archivos
carpeta_datos = "data"
path_usuarios = path.join(carpeta_datos, "usuarios.csv")
path_seguidores = path.join(carpeta_datos, "seguidores.csv")
path_prograposts = path.join(carpeta_datos, "posts.csv")

# Ajuste de interfaz
ancho_ui = 48

# set de usuarios a partir de usuarios.csv
# utilizado para no leer usuarios.csv
# cada vez que sea necesario
set_usuarios = set()
with open(path_usuarios, "r", encoding="utf8") as archivo:
    for fila_archivo in archivo.readlines():
        set_usuarios.add(fila_archivo.strip())


def crear_usuario(nombre_usuario):
    """
    Agrega el usuario a usuarios.csv, seguidores y set_usuarios
    Retorna un str sobre el resultado
    Se asume que el usuario es valido
    """
    # Se agrega el usuario al archivo de usuario y seguidores
    # En vez de rehacer el archivo, este se usa
    # la opción `a` append, y se agrega al final
    set_usuarios.add(nombre_usuario)
    with open(path_usuarios, "a", encoding="utf8") as archivo:
        print(nombre_usuario, file=archivo)
    with open(path_seguidores, "a", encoding="utf8") as archivo:
        print(nombre_usuario, file=archivo)
    return "Bienvenido a DCCahuín!"


def usuario_valido(usuario):
    """
    El usuario debe:
        1 - Tener un número
        2 - Tener una letra
        3 - Ser entre 8 y 32 caractares
        4 - No contener símbolos (!#Q$%&)
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


def modificar_archvivo_usuarios(usuario, otro, func):
    """
    Modifica el archivo de usuarios, simplifica métodos
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
        # Se utiliza el sintax método(clase, argumentos)
        # para los métodos `set.add` y `set.discard`
        func(directorio_seguidores[otro], usuario)
        with open(path_seguidores, "w", encoding="utf8") as archivo:
            for usuario, seguidores in directorio_seguidores.items():
                print(usuario, *seguidores, sep=",", file=archivo)
        if func == set.add:
            return f"Ahora sigues a @{otro}"
        elif func == set.discard:
            return f"Dejaste de seguir a @{otro}"


def extraer_posts():
    """
    Retorna una lista de objetos clase PrograPost
    """
    lista_prograposts = list()
    with open(path_prograposts, "r", encoding="utf8") as archivo:
        for fila_archivo in archivo.readlines():
            data = fila_archivo.strip().split(",", 2)
            lista_prograposts.append(PrograPost(*data))
    return lista_prograposts


def posts_filtrar(*usuarios, rec):
    """
    Extraer_post() se ejecuta para obtener el listado.
    Se filtra por usuario y los ordena por fecha,
    si la fecha es la misma, se ordena por usuario
    Se el usuario y la fecha son las mismas, se ordena por mensaje
    Argumento:
        *usuarios - lista de usuarios a mostrar
        recientes - mostrar últimos los PrograPost primeros
    Solución a partír de:
    https://docs.python.org/3/howto/sorting.html#operator-module-functions
    """
    lista = [post for post in extraer_posts() if post.usuario in usuarios]
    orden = ("fecha", "usuario",  "mensaje")
    lista.sort(key=attrgetter(*orden), reverse=rec)
    return lista


class Usuario:
    """
    El usuario debe ser creado en Crear Usuario, luego
    se debe crear el objeto Usuario al iniciar seción
    """
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return f"@{self.nombre}"

    def obtener_seguidores(self):
        return obtener_dict_seguidores()[self.nombre]

    def obtener_seguidos(self):
        set_seguidos = set()
        for usuario, seguidos in obtener_dict_seguidores().items():
            if self.nombre in seguidos:
                set_seguidos.add(usuario)
        return set_seguidos

    def empezar_a_seguir(self, otro):
        """
        Se empieza a seguir al usuario `otro`
        Retorna un str confirmando la acción
        """
        if otro == self.nombre:
            return "    No te puedes seguir a ti mismo!"
        elif otro not in set_usuarios:
            return f"    El usuario @{otro} no existe"
        else:
            # Mensaje de respuesta integrado en la función
            return modificar_archvivo_usuarios(self.nombre, otro, set.add)

    def dejar_de_seguir(self, otro):
        if otro not in set_usuarios:
            return "El usuario no existe"
        elif otro not in self.obtener_seguidos():
            return "No sigues al usuario"
        else:
            # Mensaje de respuesta integrado en la función
            return modificar_archvivo_usuarios(self.nombre, otro, set.discard)

    def imprimir_muro(self, recientes=True):
        """
        Se imprime el muro del usuario
        Se asume que:
            Se necesita imprimir todos los posts
            No se muestra los post del usuario
                (en caso de tener que mostrarlos,
                 agregar el argumento self.user
                 antes de self.obtener.seguidores())
        """
        # header
        print(" Tu Muro ".center(47, "-"))
        lista_posts = posts_filtrar(*self.obtener_seguidos(), rec=recientes)
        if lista_posts:
            print("".join([str(post) for post in lista_posts]))
        # Si la lista esta vaciá, invita al
        # usuario a seguir a más usuarios
        else:
            print()
            print("Tu Múro está vació".center(ancho_ui))
            print()
            print("Trata de seguir a más usuarios!".center(ancho_ui))
        print()


    def existen_publicaciones(self, recientes=True):
        """
        Verifica si el usuario ha publicado
        Evita que el usuario borre una publicación
        Cuando este no posee una
        """
        return bool(posts_filtrar(self.nombre, rec=recientes))

    def imprimir_publicaciones(self, recientes=True):
        """
        Se imprime los post del usuario
        """
        print(" Tus publicaciones ".center(47, "-"))
        lista_posts = posts_filtrar(self.nombre, rec=recientes)
        if lista_posts:
            print("".join([str(post) for post in lista_posts]))
        else:
            print()
            print("Tu perfil está vació".center(ancho_ui))
            print()
            print("Crea tu primera publicación!".center(ancho_ui))
        print()

    def publicar(self, mensaje):
        """
        Se guarda la publicación del usuario en posts.cvs
        Retorna el mensaje de confirmación
        """
        # Se limpia
        mensaje = mensaje.strip()
        if 1 <= len(mensaje) <= 140:
            # Solución para evitar sobreescribir el archivo encontrado aquí:
            # https://stackoverflow.com/a/10640823
            with open(path_prograposts, "a", encoding="utf8") as archivo:
                fecha = str(date.today()).replace("-", "/")
                print(self.nombre, fecha, mensaje, sep=",", file=archivo)
            print(PrograPost(self.nombre, fecha, mensaje))
            return "Mensaje publicado"
        elif 140 < len(mensaje):
            return "Mensaje muy largo para publicar"
        return ""

    def eliminar_post(self, numero_post=-1):
        """
        Elimina la publicación del usuario
        Por defecto se elimina la ultima realizada
        Retorna un mensaje de confirmación
        """
        lista_posts = extraer_posts()
        posts_propios = posts_filtrar(self.nombre, recientes=False)
        if - len(posts_propios) <= numero_post < len(posts_propios):
            # Se muestra el post y se confirma la acción
            print(posts_propios[numero_post])
            confirmar = input("(Sí) / (No) ----> ").strip().lower()
            if confirmar in {"sí", "si", "s", "y", "yes", "ok"}:
                with open(path_prograposts, "w", encoding="utf8") as archivo:
                    # `orden` es el orden en el que los datos se
                    # guardan en el archivo
                    orden = attrgetter("usuario", "fecha",  "mensaje")
                    for post in lista_posts:
                        if orden(posts_propios[numero_post]) != orden(post):
                            print(*orden(post), sep=",", file=archivo)
                    return "PrograPost eliminado"
            return "Acción cancelada"
        else:
            return f"No existe el post con indice {numero_post}"


class PrograPost:
    def __init__(self, usuario, fecha, mensaje):
        self.usuario = usuario
        self.fecha = fecha
        self.mensaje = mensaje

    def __str__(self):
        return (
            f"{'_' * ancho_ui}\n"
            f"|  0  | @{self.usuario.ljust(ancho_ui - 10)}"    "|\n"
            f"| /Y\\ | {self.fecha.rjust(ancho_ui - 10)}|\n"
            f"|{'=' * (ancho_ui- 2)}|\n"
            f"{self.contenedor_de_mensaje()}\n"
            f"|{'_' * (ancho_ui-2)}|\n"
        )

    def contenedor_de_mensaje(self):
        # TODO: Simplificar el método
        """
        Método para imprimir la parte "mensaje"
        de un PrograPost en el cuadro establecido en el
        método __str__
        Limita las palabras por fila
        """
        lista_palabras = self.mensaje.split(" ")
        # ancho total y ancho restante
        largo_max = ancho_ui - 4
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
