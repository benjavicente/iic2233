from os import path
import json

from itertools import product

def traducir_modulos(modulos_string):
    mods = dict()
    for m in map(lambda m: m.split('#'), modulos_string.split(';')):
        if len(m) - 1:
            prod = product(*map(lambda s: s.split(','), m[1].split(':')))
            mods[m[0]] = [(x, int(y)) for x, y in prod]
        else:
            mods[m[0]] = list()
    return mods


def cargar_cursos(semestre: str):
    with open(path.join('datos', semestre + '.json'), encoding='utf-8') as file:
        courses = json.load(file)
    for course in courses.values():
        course['Prerrequisitos'] = list(filter(None, course['Prerrequisitos'].split(';')))
        for secc in course['Secciones'].values():
            secc['Modulos'] = traducir_modulos(secc['Modulos'])
    return courses


if __name__ == "__main__":

    horario_ejemplo_1 = "AYU#M:4;CLAS#J:4,5;LAB;PRA;TAL;TER;TES"
    print(traducir_modulos(horario_ejemplo_1))
    horario_ejemplo_2 = "AYU;CLAS#L,W,V:3;LAB;LIB;PRA;SUP;TAL;TER;TES"
    print(traducir_modulos(horario_ejemplo_2))

    semestre = "2019-2" # Cambiar para probar

    cursos = cargar_cursos(semestre)

    with open("resultado_cargado.json", "wt", encoding="utf-8") as archivo:
        json.dump(cursos, archivo, indent=2)
