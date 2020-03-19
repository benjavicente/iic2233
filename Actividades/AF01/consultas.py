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
    # los 
    dict_generos = defaultdict(int)
    pass

