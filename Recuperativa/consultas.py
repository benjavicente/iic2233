import json
from collections import defaultdict
from cargar_cursos import cargar_cursos

from functools import reduce

### Espacio para funciones auxiliares ###


### --------------------------------- ###


def filtrar_por_prerrequisitos(curso, dicc_de_cursos):
    filtrado = dict()
    for sigla, c in dicc_de_cursos.items():
        if curso['Sigla'] in c['Prerrequisitos']:
            filtrado[sigla] = c
    return filtrado


def filtrar_por_cupos(cupos, dicc_de_cursos):
    filtrado = dict()
    for sigla, c in dicc_de_cursos.items():
        secciones = dict()
        for i, seccion in c['Secciones'].items():
            if cupos <= seccion['Vacantes disponibles']:
                secciones[i] = seccion
        if secciones:
            filtrado[sigla] = c
            filtrado[sigla]['Secciones'] = secciones
    return filtrado


def filtrar_por(llave: str, string: str, dicc_de_cursos):
    '''llave puede ser 'Nombre', 'Profesor', 'NRC' o 'Sigla'''
    filtrado = dict()
    for sigla, c in dicc_de_cursos.items():
        # Se revisa el curso
        if llave in c:
            if string.lower() in c[llave].lower():
                filtrado[sigla] = c
        # Se revisa cada sección
        else:
            secciones = dict()
            for i, seccion in c['Secciones'].items():
                if string.lower() in seccion[llave].lower():
                    secciones[i] = seccion
            if secciones:
                filtrado[sigla] = c
                filtrado[sigla]['Secciones'] = secciones
    return filtrado


def filtrar_por_modulos(modulos_deseados: list, dicc_de_cursos):
    filtrado = dict()
    for sigla, c in dicc_de_cursos.items():
        secciones = dict()
        for i, seccion in c['Secciones'].items():
            # Se revisa si por cada módulo deseado
            tiene = True
            for deseado in modulos_deseados:
                if deseado not in reduce(lambda x, y: x + y, seccion['Modulos'].values()):
                    tiene = False
                    break
            if tiene:
                secciones[i] = seccion
        if secciones:
            filtrado[sigla] = c
            filtrado[sigla]['Secciones'] = secciones
    return filtrado


def filtrar_por_cursos_compatibles(lista_nrc, dicc_de_cursos):
    # Se listan los módulos ocupados
    modulos_ocupados = set()
    for sigla, c in dicc_de_cursos.items():
        for seccion in filter(lambda s, l=lista_nrc: s['NRC'] in l, c['Secciones'].values()):
            modulos_ocupados.update(reduce(lambda x, y: x + y, seccion['Modulos'].values()))
    # Se buscan cursos disponibles
    filtrado = dict()
    for sigla, c in dicc_de_cursos.items():
        secciones = dict()
        # Se revisa por sección
        for i, seccion in c['Secciones'].items():
            mods_secc = set(reduce(lambda x, y: x + y, seccion['Modulos'].values()))
            if not mods_secc & modulos_ocupados:  # Si no hay intersección se agrega
                secciones[i] = seccion
        # Se agrega el curso si es que tiene sección
        if secciones:
            filtrado[sigla] = c
            filtrado[sigla]['Secciones'] = secciones
    return filtrado


if __name__ == "__main__":
    from pprint import pprint

    semestre = "2020-1"
    cursos = cargar_cursos(semestre)

    # Filtrar por Prerrequisitos
    # avanzada = cursos['IIC2233']
    # for sigla, info_curso in filtrar_por_prerrequisitos(avanzada, cursos).items():
    #     pprint(sigla)
    #     pprint(info_curso)

    # Filtar por Cupos
    # for sigla, info_curso in filtrar_por_cupos(25, cursos).items():
    #     for nr_seccion, info_seccion in info_curso['Secciones'].items():
    #         print(sigla, nr_seccion, info_seccion['Vacantes disponibles'])

    # Filtrar por Profesor
    # resultado = filtrar_por('Profesor', 'cris', cursos)
    # for sigla, info_curso in resultado.items():
    #     for info_seccion in info_curso['Secciones'].values():
    #         print(info_seccion['Profesor'])

    # Filtrar por Sigla
    # resultado = filtrar_por('Sigla', 'iic2', cursos)
    # for sigla, info_curso in resultado.items():
    #     print(sigla)

    # Filtrar por NRC
    # resultado = filtrar_por('NRC', '211', cursos)
    # for sigla, info_curso in resultado.items():
    #     for info_seccion in info_curso['Secciones'].values():
    #         print(info_seccion['NRC'])

    # Filtrar por Nombre
    # resultado = filtrar_por('Nombre', 'cri', cursos)
    # for sigla, info_curso in resultado.items():
    #     print(info_curso['Nombre'])

    # Filtar por Modulo
    # for sigla, info_curso in filtrar_por_modulos([('W', 6), ('M', 2)], cursos).items():
    #     for nr_seccion, info_seccion in info_curso['Secciones'].items():
    #         print(sigla, nr_seccion, info_seccion['Modulos'])
    #         pprint(info_seccion['Modulos'])

    # Filtar por horarios
    for sigla, info_curso in filtrar_por_cursos_compatibles(['10732', '10791', '21116', '15169', '10923', '18871', '23685', '10892', '10660', '10881'], cursos).items():
        for nr_seccion, info_seccion in info_curso['Secciones'].items():
            print(sigla, info_seccion['NRC'], info_seccion['Modulos'])

    