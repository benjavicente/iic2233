from collections import defaultdict


def cantidad_animes_genero(animes):
    # creo un diccionario para contar cada genero,
    # donde le valor por defecto es 0
    cantidad_genero = defaultdict(int)
    for anime in animes:
        for generos in anime.generos:
            cantidad_genero[generos] += 1
    # OPCIONAL: transformo a un diccionario normal
    return dict(cantidad_genero)


def generos_distintos(anime, animes):
    # creo un set para almacenar generos
    set_generos = set()
    for item_anime in animes:
        set_generos.update(item_anime.generos)
    # resto los generos del anime a el set de generos
    return set_generos - anime.generos


def promedio_rating_genero(animes):
    # Creo un diccionario para almacenar la cantidad de
    # ratings y la suma de rating para cada genero
    dict_generos = dict()
    for anime in animes:
        for genero in anime.generos:
            if genero not in dict_generos:
                # si el genero no estaba en el diccionario,
                # se crea con un diccionario de datos y
                # se agregan los datos
                dict_generos[genero] = {"total": anime.rating, "cant": 1}
            else:
                # si el genero se encuentra en el diccionario,
                # se agregan los datos
                dict_generos[genero]["total"] += anime.rating
                dict_generos[genero]["cant"] += 1
    # Creo un diccionario para almacenar el rating promedio
    dict_rating = dict()
    for genero, info in dict_generos.items():
        dict_rating[genero] = info["total"] / info["cant"]
    return dict_rating

