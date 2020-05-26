'''
Paths de los archivos del UI
'''

from os.path import join
from os import getcwd


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
    'table': join(_SPRITES, 'mapa', 'accesorios', 'mesa_pequena.png'),
    'chair': join(_SPRITES, 'mapa', 'accesorios', 'silla_cafe.png'),
    'player': {
        'a': {
            'free': {
                'idle': {
                    'up': join(_SPRITES, 'mesero', 'up_02.png'),
                    'right': join(_SPRITES, 'mesero', 'right_02.png'),
                    'down': join(_SPRITES, 'mesero', 'down_02.png'),
                    'left': join(_SPRITES, 'mesero', 'left_02.png'),
                },
                'rightfoot': {
                    'up': join(_SPRITES, 'mesero', 'up_01.png'),
                    'right': join(_SPRITES, 'mesero', 'right_01.png'),
                    'down': join(_SPRITES, 'mesero', 'down_01.png'),
                    'left': join(_SPRITES, 'mesero', 'left_01.png'),
                },
                'leftfoot': {
                    'up': join(_SPRITES, 'mesero', 'up_03.png'),
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
                'rightfoot': {
                    'up': join(_SPRITES, 'mesero', 'up_snack_01.png'),
                    'right': join(_SPRITES, 'mesero', 'right_snack_01.png'),
                    'down': join(_SPRITES, 'mesero', 'down_snack_01.png'),
                    'left': join(_SPRITES, 'mesero', 'left_snack_01.png'),
                },
                'leftfoot': {
                    'up': join(_SPRITES, 'mesero', 'up_snack_03.png'),
                    'right': join(_SPRITES, 'mesero', 'right_snack_03.png'),
                    'down': join(_SPRITES, 'mesero', 'down_snack_03.png'),
                    'left': join(_SPRITES, 'mesero', 'left_snack_03.png'),
                },
            },
        },
    },
    'chef': {
        'idle': join(_SPRITES, 'chef', 'meson_01.png'),
        'done': join(_SPRITES, 'chef', 'meson_16.png'),
        'reading': join(_SPRITES, 'chef', 'meson_17.png'),
        'cookingA0': join(_SPRITES, 'chef', 'meson_13.png'),
        'cookingA1': join(_SPRITES, 'chef', 'meson_14.png'),
        'cookingA2': join(_SPRITES, 'chef', 'meson_15.png'),
        'cookingB0': join(_SPRITES, 'chef', 'meson_07.png'),
        'cookingB1': join(_SPRITES, 'chef', 'meson_08.png'),
        'cookingB2': join(_SPRITES, 'chef', 'meson_09.png'),
    },
    'customer': {
        'dog': {
            '0': join(_SPRITES, 'clientes', 'perro', 'perro_31.png'),
            '1': join(_SPRITES, 'clientes', 'perro', 'perro_13.png'),
            '2': join(_SPRITES, 'clientes', 'perro', 'perro_16.png'),
            'H': join(_SPRITES, 'clientes', 'perro', 'perro_12.png'),
        },
        'hamster': {
            '0': join(_SPRITES, 'clientes', 'hamster', 'hamster_01.png'),
            '1': join(_SPRITES, 'clientes', 'hamster', 'hamster_26.png'),
            '2': join(_SPRITES, 'clientes', 'hamster', 'hamster_18.png'),
            'H': join(_SPRITES, 'clientes', 'hamster', 'hamster_17.png'),
        },
        'special': {
            '0': join(_SPRITES, 'bonus', 'presidente.png'),
            '1': join(_SPRITES, 'bonus', 'presidente.png'),
            '2': join(_SPRITES, 'bonus', 'presidente.png'),
            'H': join(_SPRITES, 'bonus', 'presidente.png'),
        },
    }
}


SPRITE_PATH = SpritePath(PATH)


if __name__ == "__main__":
    # Ejemplos
    BEFORE = PATH['player']['a']['free']['idle']['down']
    print(BEFORE)
    INFO = ['player', 'a', 'free', 'idle', 'down']
    AFTER = SPRITE_PATH[INFO]
    print(AFTER)
    print(BEFORE == AFTER)
    print()
    print(SPRITE_PATH[['star', 'empty']])
    print()
    print(SPRITE_PATH[['star', 'hola']])
