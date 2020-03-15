"""
Libreria para realizar accioones de usuario
Objetos marcados con * están destinadas para el uso externo

Incluye:
    variables
        carpeta_datos
        path_usuarios
        path_seguidores
        path_prograposts
        *set_usuarios
    -----------------------------
    funciones
        *agregar_usuario
        *es_valido
        obtener_dict_seguidores
        modificar_archvivo_usuarios
        extraer_posts
        posts_filtrar
    -----------------------------
    *clace Usuario
        atributos
            nombre
        metodos
            __init__
            __str__
            obtener_seguidores
            empezar_a_seguir
            dejar_de_seguir
            imprimir_muro
            imprimir_publicaciones
            publicar
            eliminar_post
    -----------------------------
    clase PrograPost
        atributos
            usuario
            fecha_emision
            mensaje
        metodos
            __init__
            __str__
            mprint
"""
# TODO: Simplificar el método mprint de la clase Prograpost
# TODO: Añadir la opción de crear y eliminar posts
# TODO: Ver la validación del nombre

import time
from datetime import date
from os import path
from operator import attrgetter

# Se obtiene el path de los archivos
carpeta_datos = "data"
path_usuarios = path.join(carpeta_datos, "usuarios.csv")
path_seguidores = path.join(carpeta_datos, "seguidores.csv")
path_prograposts = path.join(carpeta_datos, "posts.csv")

# set de usuarios a partir de usuarios.csv
set_usuarios = set()
with open(path_usuarios, "r", encoding="utf8") as archivo:
    for fila_archivo in archivo.readlines():
        set_usuarios.add(fila_archivo.strip())


def agregar_usuario(nombre_usuario):
    """
    Agrega el usuaio a usuarios.csv, seguidores y set_usuarios
    Retorna un str sobre el resultado
    Se asume que el usuario es valido
    """
    if nombre_usuario in set_usuarios:
        return "Usuario existente"
    else:
        set_usuarios.add(nombre_usuario)
        # Se agrega el usuario al archivo de usuario
        # Se asume que no tiene orden
        with open(path_usuarios, "w", encoding="utf8") as archivo:
            for usuario in set_usuarios:
                print(usuario, file=archivo)
        # Se agrega el usuario al archivo de seguidores
        directorio_seguidores = obtener_dict_seguidores().items()
        with open(path_seguidores, "w", encoding="utf8") as archivo:
            for usuario, seguidores in directorio_seguidores:
                print(usuario, *seguidores, sep=",", file=archivo)
        return "Bienvenido a DDCahuín!"


# TODO
def es_valido(usuario):
    """
    El usuario debe contener:
        1
        2
        3
    """
    pass


def obtener_dict_seguidores():
    """
    Retorna un diccionario con los segidores
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
            # Se crea la entrada en el ciccionario
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
        # remplazando func (método), se añadira o eliminara
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


def posts_filtrar(*usuarios, recientes=True,):
    """
    Extraer_post() se ejecuta para obtener el listado.
    Se filtra por usuario y los ordena por fecha,
    si la fecha es la misma, se ordena por usuario
    Se el usuario y la fecha son las mismas, se ordena por mensaje
    Argumento:
        *usuarios - lista de usuarios a mostrar
        recientes - mostrar ultimos los prograpost primeros
    Solución a partír de:
    https://docs.python.org/3/howto/sorting.html#operator-module-functions
    """
    lista = [post for post in extraer_posts() if post.usuario in usuarios]
    orden = ("fecha_emision", "usuario",  "mensaje")
    lista.sort(key=attrgetter(*orden), reverse=recientes)
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
        if otro not in set_usuarios:
            return "El usuario no existe"
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
        lista_posts = posts_filtrar(*self.obtener_seguidos(), recientes)
        print("".join([str(post) for post in lista_posts]))

    def imprimir_publicaciones(self, recientes=True):
        """
        Se imprime los post del usuario
        """
        print(" Tus publicaciones ".center(47, "-"))
        lista_posts = posts_filtrar(self.nombre, recientes)
        print("".join([str(post) for post in lista_posts]))

    def publicar(self, mensaje):
        """
        Se guarda la publicación del usuario en posts.cvs
        """
        # Se limpia
        mensaje = mensaje.strip()
        if 1 <= len(mensaje) <= 140:
            # Solución para evitar sobreescribir el archivo encontrado aquí:
            # https://stackoverflow.com/a/10640823
            with open(path_prograposts, "a", encoding="utf8") as archivo:
                fecha = str(date.today()).replace("-", "/")
                print(self.nombre, fecha, mensaje, sep=",", file=archivo)

    def eliminar_post(self, numero_post=0):
        """
        Elimina la publicación del usuario
        Por defecto se elimina la ultima realizada
        """
        lista_posts = extraer_posts()
        posts_propios = posts_filtrar(self.nombre)
        if - len(posts_propios) <= numero_post < len(posts_propios):
            with open(path_prograposts, "w", encoding="utf8") as archivo:
                orden = attrgetter("usuario", "fecha_emision",  "mensaje")
                for post in lista_posts:
                    if orden(posts_propios[numero_post]) != orden(post):
                        print(*orden(post), sep=",", file=archivo)
                    else:
                        print("\nEliminado:")
                        print(post)


class PrograPost:
    def __init__(self, usuario, fecha_emision, mensaje):
        self.usuario = usuario
        self.fecha_emision = fecha_emision
        self.mensaje = mensaje

    def __str__(self):
        return (
            f"_______________________________________________\n"
            f"|  0  | @{self.usuario.ljust(37)}"           "|\n"
            f"| /Y\\ | {self.fecha_emision.rjust(37)}"    " |\n"
            f"|=============================================|\n"
            f"{self.mprint()}\n"
            f"|_____________________________________________|\n"
        )

    def mprint(self):
        """
        Método para imprimir la parte "mensaje"
        de un PrograPost en el cuadro establecido en el
        método __str__
        Limita las palabras por fila de modo que
        solo existan 43 columnas
        """
        lista_palabras = self.mensaje.split(" ")
        # ancho total y ancho restante
        largo_max = 43
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
                    # Se añade el cambio de linia y el trozo (p) que ocupa
                    # todo el espacio disponible (largo_max - "...")
                    palabra_cortada += "\n" + p
                # se guardan los cortes
                palabra = palabra_cortada
            elif len(palabra) > largo_restante:
                # la palabra es muy larga para la sección
                # restante, se imprime en la siguiente linea
                columna += " "*largo_restante + "\n"
                largo_restante = largo_max - len(palabra) - 1
            else:
                largo_restante -= len(palabra) + 1
            # Finalmente se agrega la palabra a la columna
            columna += palabra + " "*(largo_restante != -1)
            # " "*(largo_restante != -1)` es usado para evitar que
            # un espacio (" ") sea agregado cuando se sobrepase
            # el largo resante
        columna = columna.replace('\n', ' |\n| ')
        return f"| {columna}{' '*largo_restante} |"

###
# ZONA DE TESTEO
# ELIMINAR AL FINALIZAR
###


x = Usuario("1gbasly")
x.imprimir_publicaciones()
x.eliminar_post(0)
x.imprimir_publicaciones()
