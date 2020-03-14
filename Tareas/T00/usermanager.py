"""
Libreria para administrar datos relacionados con el usuario
"""

from os import path


CARPETA_DATOS = "data"

PATH_USUARIOS = path.join(CARPETA_DATOS, "usuarios.csv")
PATH_SEGUIDORES = path.join(CARPETA_DATOS, "seguidores.csv")

lista_usuarios = list()


class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        # agrego a la lista automaticamente
        lista_usuarios.append(self)

    def __str__(self):
        return self.nombre

    def obtener_seguidores(self):
        """
        Busca sus seguidores
        Retorna una lista de sus seguidores
        """
        # El usuario debe ya estar añadido a el archivo de seguidores
        # Leo el archivo y lo guardo en una variable
        with open(PATH_SEGUIDORES, "r") as archivo_seguidores:
            listado_seguidores = archivo_seguidores.readlines()
        # Leo la lista de seguidores
        for fila_seguidores in listado_seguidores:
            # Uso partition, ya que este no entrega errores al no encontrar
            # donde dividir en la fila
            # La variable _ no es usada
            usuario, _, seguidores = fila_seguidores.strip().partition(",")
            if usuario == self.nombre:
                # Ve si tiene segudores (str no vacio)
                if seguidores:
                    return seguidores.split(",")
                return []

    def obtener_seguidos(self):
        """
        Busca a los usuarios que sigue
        Retorna una lista con el nombre de cada usuario seguido
        """
        seguidos = list()
        # Guardo el archivo en una lista
        with open(PATH_SEGUIDORES, "r") as archivo_seguidores:
            listado_seguidores = archivo_seguidores.readlines()
        # itero por cada fila para buscar los usuarios seguidos
        for fila_seguidores in listado_seguidores:
            usuario, _, seguidores = fila_seguidores.strip().partition(",")
            # Si se encuentra en los seguidos, se añade el usuario de la fila
            if self.nombre in seguidores:
                seguidos.append(usuario)
        return seguidos

    def seguir_a_usuario(self, otro):
        """
        Añade al usuario (self) a la lista de seguidores de otro
        Retorna un string, el cual es un mensaje
        que indica si se pudo seguir al usuario,
        en el caso que no se pudo se retorna el porque
        """
        if self.nombre == otro:
            return "No puedes seguirte a ti mismo"
        # Leo el archivo y lo guardo en una variable,
        # al iguall que en obtener_seguidores()
        with open(PATH_SEGUIDORES, "r") as archivo_seguidores:
            listado_seguidores = archivo_seguidores.readlines()
        for fila_seguidores in listado_seguidores:
            fila_seguidores.strip()  # Elimino \n de las filas
            usuario, _, seguidores = fila_seguidores.strip().partition(",")
            if usuario == otro:
                # ahora veo si ya sigue al usuario
                if self.nombre in seguidores:
                    return "Ya sigues a este usuario!"
                # Si no es el caso, añado el usuario a los seguidoes
                ubicación_cambio = listado_seguidores.index(fila_seguidores)
                original = listado_seguidores[ubicación_cambio].strip()
                nuevo = original + "," + self.nombre + "\n"
                listado_seguidores[ubicación_cambio] = nuevo
                # Ahora, reescribo el archivo original
                with open(PATH_SEGUIDORES, "w") as archivo_seguidores:
                    a_guardar = "".join(listado_seguidores)
                    archivo_seguidores.write(a_guardar)
                return f"Ahora sigues a @{otro}"
        # Si no es encontrado no se edita el archivo de seguidores
        return f"Usuario @{otro} no encontrado"

    def dejar_de_seguir(self, otro):
        """
        Elimina al usuario (self) de la lista de seguidoresl de otro
        Retorna un string, el cual es un mensaje
        que indica si se pudo parar de seguir al usuario,
        en el caso que no se pudo se retorna el porque
        """

    def crear_post(self):
        pass


def new_user(name):
    # El nombre es validao anteriormente
    lista_usuarios


x = Usuario("m0quezada")
print(x.obtener_seguidores())
print(x.obtener_seguidos())
