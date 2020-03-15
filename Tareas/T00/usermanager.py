"""
Libreria para administrar datos relacionados con el usuario
Incluye:
    class Usuario
    set usuarios
    ------------
    str carpeta_datos
    str path_usuarios
    str path_seguidores
"""

# TODO simplificar la manera en la que leo  y escribo los archivos

from os import path


carpeta_datos = "data"

path_usuarios = path.join(carpeta_datos, "usuarios.csv")
path_seguidores = path.join(carpeta_datos, "seguidores.csv")


class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return str(self)

    def obtener_seguidores(self):
        """
        Busca sus seguidores
        Retorna una lista de sus seguidores
        """
        # El usuario debe ya estar añadido a el archivo de seguidores
        # Leo el archivo y lo guardo en una variable
        with open(path_seguidores, "r") as archivo_seguidores:
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
        with open(path_seguidores, "r") as archivo_seguidores:
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
        otro es un objeto de clase Usuario
        Retorna un string, el cual es un mensaje
        que indica si se pudo seguir al usuario,
        en el caso que no se pudo se retorna el porque
        """
        if self.nombre == otro.nombre:
            return "No puedes seguirte a ti mismo"
        # Leo el archivo y lo guardo en una variable,
        # al iguall que en obtener_seguidores()
        with open(path_seguidores, "r") as archivo_seguidores:
            listado_seguidores = archivo_seguidores.readlines()
        for fila_seguidores in listado_seguidores:
            fila_seguidores.strip()  # Elimino \n de las filas
            usuario, _, seguidores = fila_seguidores.strip().partition(",")
            if usuario == otro.nombre:
                # ahora veo si ya sigue al usuario
                if self.nombre in seguidores:
                    return f"Ya sigues a @{otro.nombre}"
                # Si no es el caso, añado el usuario a los seguidoes
                ubicación_cambio = listado_seguidores.index(fila_seguidores)
                original = listado_seguidores[ubicación_cambio].strip()
                nuevo = original + "," + self.nombre + "\n"
                listado_seguidores[ubicación_cambio] = nuevo
                # Ahora, reescribo el archivo original
                with open(path_seguidores, "w") as archivo_seguidores:
                    a_guardar = "".join(listado_seguidores)
                    archivo_seguidores.write(a_guardar)
                return f"Ahora sigues a @{otro.nombre}"
        # Si no es encontrado no se edita el archivo de seguidores
        return f"Usuario @{otro.nombre} no encontrado"

    def dejar_de_seguir(self, otro):
        """
        Elimina al usuario (self) de la lista de seguidores del otro
        otro es un objeto de clase Usuario
        Retorna un string, el cual es un mensaje
        que indica si se pudo parar de seguir al usuario,
        en el caso que no se pudo se retorna el porque
        """
        # Primero veo si se sigue al otro usuario
        if otro.nombre not in self.obtener_seguidos():
            return f"No sigues a @{otro.nombre}"
        # Ya que el otro si es seguido, busco su
        # lista de seguidores y la edito
        with open(path_seguidores, "r") as archivo_seguidores:
            listado_seguidores = archivo_seguidores.readlines()
        for fila_seguidores in listado_seguidores:
            usuario, _, seguidores = fila_seguidores.strip().partition(",")
            if usuario == otro.nombre:
                # Edito el archivo y lo guardo
                ubicación_cambio = listado_seguidores.index(fila_seguidores)
                original = listado_seguidores[ubicación_cambio].strip()
                nuevo = original.replace(f",{self.nombre}") + "\n"
                listado_seguidores[ubicación_cambio] = nuevo
                with open(path_seguidores, "w") as archivo_seguidores:
                    a_guardar = "".join(listado_seguidores)
                    archivo_seguidores.write(a_guardar)
                return f"Paraste de seguir a @{otro.nombre}"



# Leo los usuarios en usuarios.csv
with open(path_usuarios, "r") as archivo_usuarios:
    usuarios = {Usuario(n.strip()) for n in archivo_usuarios.readlines()}
