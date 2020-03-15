"""
Libreria para realizar accioones de usuario

Incluye:
    variables
        carpeta_datos
        path_usuarios
        path_seguidores
        set_usuarios
    -----------------------------
    funciones
        agregar_usuario
        se_valido
        obtener_dict_seguidores
        modificar_archvivo_usuarios
    -----------------------------
    clace Usuario
        atributos
            nombre
        metodos
            __init__
            __str__
            obtener_seguidores
            empezar_a_seguir
            dejar_de_seguir
    -----------------------------
    clase PrograPost
        atributos
            usuario
            fecha_de_emision
            mensaje
        metodos
            __init__
            __str__
            mprint
"""
# TODO: Eliminar el módulo time
# TODO: Simplificar el método mprint de la clase Prograpost
# TODO: Eliminar el testeo

import time  
from os import path

# Se obtiene el path de los archivos
carpeta_datos = "data"
path_usuarios = path.join(carpeta_datos, "usuarios.csv")
path_seguidores = path.join(carpeta_datos, "seguidores.csv")

# set de usuarios a partir de usuarios.csv
set_usuarios = set()
with open(path_usuarios, "r") as archivo:
    for fila_archivo in archivo.readlines():
        set_usuarios.add(fila_archivo.strip())


def agregar_usuario(nombre_usuario):
    """
    Agrega el usuaio a usuarios.csv y set_usuarios
    retorna un str sobre el resultado
    Se asume que el usuario es valido
    """
    if nombre_usuario in set_usuarios:
        return "Usuario existente"
    else:
        set_usuarios.add(nombre_usuario)
        # Se agrega el usuario al archivo
        # Se asume que no tiene orden
        with open(path_usuarios, "w") as archivo:
            for usuario in set_usuarios:
                print(usuario, file=archivo)
        return "Bienvenido a DDCahuín!"


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
        LLaves:
            (str) Nombres de usuarios
        Valores
            (set) Listas de seguidores
    """
    dict_seg = dict()
    with open(path_seguidores, "r") as archivo:
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
        func(directorio_seguidores[otro], usuario)
        with open(path_seguidores, "w") as archivo:
            for usuario, seguidores in directorio_seguidores.items():
                print(usuario, *seguidores, sep=",", file=archivo)
        if func == set.add:
            return f"Ahora sigues a @{otro}"
        elif func == set.discard:
            return f"Dejaste de seguir a @{otro}"


class Usuario:
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

    def imprimir_muro(self):
        muro = list()


    def imprimir_publicaciones(self):
        publicaciones = list()


class PrograPost:
    def __init__(self, usuario, fecha_emision, mensaje):
        self.usuario = usuario
        self.fecha_emision = fecha_emision
        self.mensaje = mensaje

    def mprint(self):
        """
        Método para imprimir la parte del mensaje
        de un PrograPost en el cuadro establecido en el 
        método __str__
        """
        lista_palabras = self.mensaje.split(" ")
        # ancho total y ancho restante
        largo_max = 43
        largo_restante = largo_max
        # string inicial reducido a {largo_max} columnas
        columna = ""
        for palabra in lista_palabras:
            if len(palabra) > largo_max:
                # La palabra es muy larga, se corta
                columna += " "*largo_restante
                palabra_cortada = ""
                cortes_necesarios = (len(palabra)-3)//largo_max
                for parte in range(cortes_necesarios + 1):
                    p = palabra[parte*(largo_max-3):(parte+1)*(largo_max-3)]
                    if parte != cortes_necesarios:
                        p += "..."  # Se agregan para mostrar que se cortó
                    else:
                        largo_restante = largo_max - len(p) - 1
                    palabra_cortada += "\n" + p
                palabra = palabra_cortada  # se guardan los cortes
            elif len(palabra) > largo_restante:
                # la palabra es muy larga para la sección
                # restante, se imprime en la siguiente linea
                columna += " "*largo_restante + "\n"
                largo_restante = largo_max - len(palabra) - 1
            else:
                largo_restante -= len(palabra) + 1
            # Se agrega la palabra
            columna += palabra + " "
        columna = columna.replace('\n', ' |\n| ')
        return f"| {columna}{' '*largo_restante} |"

    def __str__(self):
        return (
            f"_______________________________________________\n"
            f"|  0  | @{self.usuario.ljust(37)}"           "|\n"
            f"| /Y\\ | {self.fecha_emision.rjust(37)}"     " |\n"
            f"|=============================================|\n"
            f"{self.mprint()}\n"
            f"|_____________________________________________|\n"
        )


###
# ZONA DE TESTEO
# ELIMINAR AL FINALIZAR
###

mensaje = (
"hola a todos, este es un post en la nueva "
"plataforma que cree. Es muy util porque "
"permite escribir grandes posts "
"Estaesunapalabramuylargaquepuedecausarunerrorhaaaaaaaa "
"ya me calmé"
)


print(PrograPost("benjamin", "2002/03/20", mensaje))
