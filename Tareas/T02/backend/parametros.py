'''
Parámetros del backend de DCCafé
'''

GAME_DATA = {
    "CHEF": {
        "PRINCIPIANTE": {
            "EXPERIENCIA": 1,
            "PLATOS_SIG_NIVEL": 5,
            "SIG_NIVEL": "INTERMEDIO",
        },
        "INTERMEDIO": {
            "EXPERIENCIA": 2,
            "PLATOS_SIG_NIVEL": 20,
            "SIG_NIVEL": "EXPERTO",
        },
        "EXPERTO": {
            "EXPERIENCIA": 3,
            "PLATOS_SIG_NIVEL": float("inf"),
            "SIG_NIVEL": None,
        },
        "PROB_FALLAR": {
            "FACTOR": 0.3,
            "SUMA": 1,
        },
    },
    "BOCADILLOS": {
        "PRECIO": 100,
        "CALC_PREP": {
            "MINIMO": 0,
            "BASE": 15,
            "FACTOR": 2,
        },
        "CAL_CALIDAD": {
            "MINIMO": 0,
            "BASE": 1,
            "FACTOR": 0.05,
            "DIV": 3,
        },
    },
    "CLIENTES": {
        "LLAGADA_CLIENTES": 5,
        "PROPINA": 200,
        "RELAJADO" : {
            "TIEMPO_ESPERA": 6,
            "PROB": 0.3,
        },
        "APURADO": {
            "TIEMPO_ESPERA": 2,
            "PROB": 0.6,
        },
    },
    "DCCAFE": {
        "CAL_REP": {
            "MIN": 0,
            "MAX": 5,
            "FACTOR": 4,
            "RESTA": 2,
        },
        "CLIENTES_RONDA": {
            "FACTOR": 5,
            "BASE": 1,
        },
        "INICIALES": {
            "DINERO": 500,
            "REPUTACION": 2,
            "CHEFS": 1,
            "MESAS": 2,
            "CLIENTES": 5,
            "DISPONIBILIDAD": True,
        },
    },
}
