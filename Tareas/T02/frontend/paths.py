'''
Paths de los archivos del UI
'''

from os.path import join
from os import getcwd

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
                'moving': {
                    '1': {
                        'up': join(_SPRITES, 'mesero', 'up_01png'),
                        'right': join(_SPRITES, 'mesero', 'right_01.png'),
                        'down': join(_SPRITES, 'mesero', 'down_01.png'),
                        'left': join(_SPRITES, 'mesero', 'left_01.png'),
                    },
                    '2': {
                        'up': join(_SPRITES, 'mesero', 'up_03png'),
                        'right': join(_SPRITES, 'mesero', 'right_03.png'),
                        'down': join(_SPRITES, 'mesero', 'down_03.png'),
                        'left': join(_SPRITES, 'mesero', 'left_03.png'),
                    },
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