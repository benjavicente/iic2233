'''
Parámetros del backend de DCCafé
# TODO
Una vez ejecutado el problema, pueden ser
cambiados en la pantalla de inicio
'''


# El tamaño de la celda dicta el tamaño de
# las entidades, por lo que modificarla puede
# modificar como quedan las entidades en el mapa.
# Se al ubicar las entidades ocurre una colición,
# se entregará un mensaje de error
# y se terminará el programa (no se mostrará el menú de juego)

PARAMETROS = {
    "mapa": {
        "tamaño celda": 30,
        "alto": 450,
        "largo": 780,
        "reducción de hitbox": 0.2,
    },
    'personaje': {
        'velocidad': 150
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
            "factor": 0.3,
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
            "calidad pedido": {
                "mínimo": 0,
                "base": 1,
                "factor": 0.05,
                "divisor": 3,
            },
        },
    },
    "clientes": {
        "periodo de llegada": 10,
        "propina": 200,
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
                    "probabilidad": 0.1,
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
                "factor": 10,
                "base": 2,
            },
        },
        "inicial": {
            "dinero": 500,
            "reputación": 2,
            "clientes": 5,
            "chefs": 3,
            "mesas": 6,
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
