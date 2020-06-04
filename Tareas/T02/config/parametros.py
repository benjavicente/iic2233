'''Todos los parámetors'''


from os.path import join
from os import getcwd

# Inicialmente tenia separado los diferentes tipos de parámetros
# (parámetros del juego, paths de datos y paths de sprites), pero
# se pide que todos estos estén en un mismo archivo :/


#Paths del backend

PATH_MAPA = 'mapa.csv'
PATH_DATOS = 'datos.csv'


# Parámetros del backend de DCCafé

PARAMETROS = {
    "tamaño": { # Se considera el tamaño horizontal como referencia
        "mesa": 1,
        "mesero": 1,
        "chef": 4,
    },
    "mapa": {
        "tamaño celda": 30,
        "alto": 420,
        "largo": 840,
        "reducción de hitbox": 0.2,
    },
    'personaje': {
        'velocidad': 7  # Celdas por segundo
    },
    "chef": {
        "nivel inicial": "principiante",
        "niveles": {
            "principiante": {
                "experiencia": 1,
                "platos siguiente nivel": 5,
                "siguiente nivel": "intermedio",
            },
            "intermedio": {
                "experiencia": 2,
                "platos siguiente nivel": 20,
                "siguiente nivel": "experto",
            },
            "experto": {
                "experiencia": 3,
                "platos siguiente nivel": float("inf"),
                "siguiente nivel": None,
            },
        },
        "probabilidad fallar": {
            "factor": 0.25,
            "suma": 1,
        },
    },
    "bocadillos": {
        "precio": 100,
        "calculos": {
            "tiempo preparación": {
                "mínimo": 0,
                "base": 15,
                "factor": 2,
            },
            "calidad pedido": {  # Prob de propina
                "mínimo": 0,
                "base": 1,
                "factor": 0.05,
                "divisor": 3,
            },
        },
    },
    "clientes": {
        "periodo de llegada": 6,
        "tiempo de salida": 2,
        "propina": 150,
        "tipos": {
            'básicos': {
                "relajado" : {
                    "tiempo de espera": 35,
                    "probabilidad": 0.4,
                },
                "apurado": {
                    "tiempo de espera": 20,
                    "probabilidad": 0.6,
                },
            },
            "especiales": {
                "presidente": {
                    "reputación": 2,
                    "min": 20,
                    "max": 40,
                    "probabilidad": 0.5,
                },
            },
        },
    },
    "DCCafé": {
        "calculos": {
            "reputación": {
                "mínimo": 0,
                "máximo": 5,
                "factor": 4,
                "resta": 2,
            },
            "clientes por ronda": {
                "factor": 2,
                "base": 3,
            },
        },
        "inicial": {
            "dinero": 1000,
            "reputación": 3,
            "clientes": 5,
            "chefs": 2,
            "mesas": 3,
            "disponibilidad": True,
        },
    },
    'trampas': {
        'dinero': 500,
        'reputación': 1,
    },
    "tienda": {
        'chef': 500,
        'mesa': 200,
    }
}


# Paths del frontend

_SPRITES = join(getcwd(), 'sprites')

SPRITE_PATH_DICT = {
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
        'table': join(_SPRITES, 'mapa', 'accesorios', 'silla_mesa_amarilla.png')
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
        'b': {
            'free': {
                'idle': {
                    'up': join(_SPRITES, 'mesero', 'otros', 'mesera_up_02.png'),
                    'right': join(_SPRITES, 'mesero', 'otros', 'mesera_right_02.png'),
                    'down': join(_SPRITES, 'mesero', 'otros', 'mesera_down_02.png'),
                    'left': join(_SPRITES, 'mesero', 'otros', 'mesera_left_03.png'),
                },
                'rightfoot': {
                    'up': join(_SPRITES, 'mesero', 'otros', 'mesera_up_01.png'),
                    'right': join(_SPRITES, 'mesero', 'otros', 'mesera_right_01.png'),
                    'down': join(_SPRITES, 'mesero', 'otros', 'mesera_down_01.png'),
                    'left': join(_SPRITES, 'mesero', 'otros', 'mesera_left_01.png'),
                },
                'leftfoot': {
                    'up': join(_SPRITES, 'mesero', 'otros', 'mesera_up_03.png'),
                    'right': join(_SPRITES, 'mesero', 'otros', 'mesera_right_03.png'),
                    'down': join(_SPRITES, 'mesero', 'otros', 'mesera_down_03.png'),
                    'left': join(_SPRITES, 'mesero', 'otros', 'mesera_left_02.png'),
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
        'cookingC0': join(_SPRITES, 'chef', 'meson_10.png'),
        'cookingC1': join(_SPRITES, 'chef', 'meson_11.png'),
        'cookingC2': join(_SPRITES, 'chef', 'meson_12.png'),
        'cookingD0': join(_SPRITES, 'chef', 'meson_06.png'),
        'cookingD1': join(_SPRITES, 'chef', 'meson_06.png'),
        'cookingD2': join(_SPRITES, 'chef', 'meson_06.png'),
    },
    'customer': {
        'basic': {
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
        },
        'special': {
            'president': {
                '0': join(_SPRITES, 'bonus', 'presidente.png'),
                '1': join('extras', 'presidente_impaciente.png'),
                '2': join('extras', 'presidente_rojo.png'),
                'H': join('extras', 'presidente_feliz.png'),
            }
        },
    }
}
