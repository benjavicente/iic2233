from collections import namedtuple, deque

# TESTEO
path_animes = "animes.csv"
path_consultas = "consultas.csv"

def cargar_animes(path=path_animes):
    dict_anime = dict()
    datos_anime = namedtuple("datos_anime", ["Rating", "Estudio", "Generos"])
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


def cargar_consultas(path=path_consultas):
    cola_consultas = deque()
    # Abrimos el archivo de animes
    with open(path, 'r', encoding="utf-8") as file:
        # Leemos las lineas
        for line in file.readlines():
            # Los separamos por coma #.replace("/",";")
            consulta = line.strip().split(";")
            numero = int(consulta[0])
            lista = consulta[1:]
            cola_consultas.append((numero, lista))
    return cola_consultas


# TESTEO
if __name__ == "__main__":
    a = cargar_animes()
    print(type(a))
    for anime, data in a.items():
        print("key:", anime, "value:", data)
    b = cargar_consultas()
    print()
    print(type(b))
    for consulta in b:
        print(consulta)

