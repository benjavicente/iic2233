from os import path


CARPETA_DATOS = "data"

PATH_USUARIOS = path.join(CARPETA_DATOS, "usuarios.csv")
PATH_SEGUIDORES = path.join(CARPETA_DATOS, "seguidores.csv")

lista_usuarios = list()


class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        lista_usuarios.append(self)

    def __str__(self):
        return self.nombre

    def obtener_seguidores(self):
        # El usuario debe ya estar añadido a el archivo de seguidores
        with open(PATH_SEGUIDORES, "r") as archivo_seguidores:
            listado_seguidores = archivo_seguidores.readlines()
            # Leo la lista de seguidores
            for fila_seguidores in listado_seguidores:
                # Uso partition, ya que este no entrega errores al no encontrar
                # donde dividir en la fila
                usuario, _, seguidores = fila_seguidores.strip().partition(",")
                if usuario == self.nombre:
                    # Ve si tiene segudores (str no vacio)
                    if seguidores:
                        return seguidores.split(",")
                    return None


def new_user(name):
    # El nombre es validao anteriormente
    lista_usuarios


x = Usuario("m0quezada")
print(x.obtener_seguidores())
