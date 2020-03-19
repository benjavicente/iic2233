from collections import defaultdict


def cantidad_animes_genero(animes):
    cantidad_genero = defaultdict(int)
    for anime in animes:
        for generos in anime.Generos:
            cantidad_genero[generos] += 1
    return cantidad_genero


def generos_distintos(anime, animes):
    gereros_anime = anime.Generos
    set_generos = set()
    for ani in animes:
        set_generos = set_generos | ani.Generos
    return set_generos - gereros_anime


def promedio_rating_genero(animes):
    dict_generos = dict()
    for ani in animes:
        for genero in ani.Generos:
            dict_generos[genero][total] += 1
            dict_generos[genero][cant] += ani.Rating

    dict_rating = dict()
    for genero, info in dict_generos.items():
        dict_rating[genero] = info[total] / info[cant]
    print(dict_rating)

