from collections import namedtuple, deque


def cargar_animes(path):
    dict_anime = dict()
    datos_anime = namedtuple("Datos Anime", ["Rating", "Estudio", "Generos"])
    # Abrimos el archivo de animes
    with open(path, 'r', encoding="utf-8") as file:
        # Leemos las lineas
        for line in file.readlines():
            # Las separamos por coma
            anime = line.strip().split(",")
            # Separamos los generos por slash
            anime[3] = anime[3].split("/")
            # Se guardan en diccionarios
            datos = datos_anime(int(anime[1]), anime[2], set(anime[3]))
            dict_anime[anime[0]] = datos
    return dict_anime


def cargar_consultas(path):
    # Abrimos el archivo de animes
    with open(path, 'r', encoding="utf-8") as file:
        # Leemos las lineas
        for line in file.readlines():
            # Los separamos por coma
            consulta = line.strip().split(";")

    return
