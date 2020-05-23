'''
Paths de los archivos del UI
'''

from os.path import join
from os import getcwd


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
        # Si el index no es una lista (o tupla) se llama normalmente
        if not isinstance(index_values, (list, tuple)):
            return super().__getitem__(index_values)
        # En al caso que es una lista, se itera por la lista
        # donde cade elemento es la llave del valor anterior
        curret_level = dict(self)
        for key in index_values:
            if isinstance(curret_level, dict) and key in curret_level:
                # Si es un diccionario se obtiene el valor
                curret_level = curret_level.__getitem__(key)
            else:
                # Si la llave no está o no es valida,
                # se muestra el último nivel
                # obtenido para poder identificar el error
                last_level = '\n'.join(list(map(
                    lambda key, value: f'\t{repr(key)}: {repr(value)}',
                    curret_level.keys(), curret_level.values()
                )))
                error = '\n'.join([
                    f"La llave {repr(key)} no en existe en el último nivel obtenido.",
                    f"Ultimo nivel obtenido:", last_level
                ])
                raise ValueError(error)
        return curret_level


_SPRITES = join(getcwd(), 'sprites')



PATH = {
    'ui': {
        'game_window': join('frontend', 'layout', 'game.ui')
    },
    'logo': join(_SPRITES, 'otros', 'logo_blanco.png'),
    'star': {
        'filed': join(_SPRITES, 'otros', 'estrella_amarilla.png'),
        'empty': join(_SPRITES, 'otros', 'estrella_blanca.png'),
    },
    'map': {
        'window': join(_SPRITES, 'mapa', 'mapa_2_parte_01.png'),
        'tile': join(_SPRITES, 'mapa', 'mapa_2_parte_02.png'),
        'wall': join(_SPRITES, 'mapa', 'mapa_2_parte_03.png'),
        'border': join(_SPRITES, 'mapa', 'mapa_2_parte_04.png'),
    },
    'shop': {
        'chef': join(_SPRITES, 'chef', 'meson_00.png'),
        'table': join(_SPRITES, 'mapa', 'accesorios', 'silla_mesa_roja.png')
    },
    'table': join(_SPRITES, 'mapa', 'accesorios', 'silla_mesa_roja.png'),
    'player': {
        'a': {
            'free': {
                'idle': {
                    'up': join(_SPRITES, 'mesero', 'up_02.png'),
                    'right': join(_SPRITES, 'mesero', 'right_02.png'),
                    'down': join(_SPRITES, 'mesero', 'down_02.png'),
                    'left': join(_SPRITES, 'mesero', 'left_02.png'),
                },
                'mov1': {
                    'up': join(_SPRITES, 'mesero', 'up_01png'),
                    'right': join(_SPRITES, 'mesero', 'right_01.png'),
                    'down': join(_SPRITES, 'mesero', 'down_01.png'),
                    'left': join(_SPRITES, 'mesero', 'left_01.png'),
                },
                'mov2': {
                    'up': join(_SPRITES, 'mesero', 'up_03png'),
                    'right': join(_SPRITES, 'mesero', 'right_03.png'),
                    'down': join(_SPRITES, 'mesero', 'down_03.png'),
                    'left': join(_SPRITES, 'mesero', 'left_03.png'),
                },
            },
            'snack': {
                'idle': {
                    'up': join(_SPRITES, 'mesero', 'up_snack_02.png'),
                    'right': join(_SPRITES, 'mesero', 'right_snack_02.png'),
                    'down': join(_SPRITES, 'mesero', 'down_snack_02.png'),
                    'left': join(_SPRITES, 'mesero', 'left_snack_02.png'),
                },
                'moving': {
                    '1': {
                        'up': join(_SPRITES, 'mesero', 'up_snack_01png'),
                        'right': join(_SPRITES, 'mesero', 'right_snack_01.png'),
                        'down': join(_SPRITES, 'mesero', 'down_snack_01.png'),
                        'left': join(_SPRITES, 'mesero', 'left_snack_01.png'),
                    },
                    '2': {
                        'up': join(_SPRITES, 'mesero', 'up_snack_03png'),
                        'right': join(_SPRITES, 'mesero', 'right_snack_03.png'),
                        'down': join(_SPRITES, 'mesero', 'down_snack_03.png'),
                        'left': join(_SPRITES, 'mesero', 'left_snack_03.png'),
                    },
                },
            },
        },
    },
    'chef': {},
    'client': {},
}


SPRITE_PATH = SpritePath(PATH)


if __name__ == "__main__":
    # Ejemplos
    BEFORE = PATH['player']['a']['free']['idle']['down']
    AFTER = SPRITE_PATH[['player', 'a', 'free', 'idle', 'down']]
    print(BEFORE)
    print(AFTER)
    print(BEFORE == AFTER)
    print()
    print(SPRITE_PATH[['star', 'empty']])
    print()
    print(SPRITE_PATH[['star', 'hola']])
