'''Paths de los archivos del UI'''

from config.parametros import SPRITE_PATH_DICT


class SpritePathError(Exception):
    '''Error en el mal manejo de SpritePath'''
    def __init__(self, key, curret_level):
        last_level = '\n'.join([f'\t{repr(key)}: {repr(value)}'
                                for key, value in curret_level.items()])
        mesage = '\n'.join([
            f"La llave {repr(key)} no en existe en el último nivel obtenido.",
            f"Ultimo nivel obtenido:", last_level
        ])
        super().__init__(mesage)



class SpritePath(dict):
    '''
    Clase Auxiliar que permite obtener valores
    de un diccionario de una manera distinta.

    En vez de dict['key1']['key2']['key3]
    permite dict[['key1', 'key2', 'key3']].

    Esto hace la comunicación del backend al
    frontend del sprite a mostrar mucho más fácil,
    ya que el backend solo necesita entregar al
    frontend una lista con el estado de la entidad.

    Por ejemplo, ['player', 'a', 'free', 'idle', 'down']
    retorna el sprite del jugador usando el personaje 'a',
    sin un snack, quieto y mirando hacia abajo.
    '''
    def __getitem__(self, index_values: list):
        curret_level = dict(self)
        # Si el index no es una lista (o tupla) se llama normalmente
        if not isinstance(index_values, (list, tuple)):
            return curret_level[index_values]
        # En al caso que es una lista, se itera por la lista
        # donde cade elemento es la llave del valor anterior
        for key in index_values:
            if isinstance(curret_level, dict) and key in curret_level:
                # Si es un diccionario se obtiene el valor
                curret_level = curret_level[key]
            else:
                # Si no es el caso, se levanta un error
                raise SpritePathError(key, curret_level)
        return curret_level


SPRITE_PATH = SpritePath(SPRITE_PATH_DICT)
